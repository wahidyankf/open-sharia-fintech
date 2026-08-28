//! Formats Mermaid validation results as text, JSON, or Markdown.

use std::collections::BTreeMap;
use std::fmt::Write as _;

use anyhow::Error;
use serde::Serialize;

use crate::domain::mermaid::{ValidationResult, Violation, ViolationKind, Warning, WarningKind};

/// Returns a human-readable description of a single [`Violation`].
fn violation_detail(v: &Violation) -> String {
    match v.kind {
        ViolationKind::LabelTooLong => format!(
            "[{}] node \"{}\" label \"{}\" is {} chars (max {})",
            v.kind.code(),
            v.node_id,
            v.label_text,
            v.label_len,
            v.max_label_len
        ),
        ViolationKind::WidthExceeded => format!(
            "[{}] span {} exceeds max-width {}",
            v.kind.code(),
            v.actual_width,
            v.max_width
        ),
        ViolationKind::MultipleDiagrams => format!(
            "[{}] block contains multiple flowchart/graph headers",
            v.kind.code()
        ),
    }
}

/// Returns a human-readable description of a single [`Warning`].
fn warning_detail(w: &Warning) -> String {
    match w.kind {
        WarningKind::SubgraphDense => {
            let label = if w.subgraph_label.is_empty() {
                "(unnamed)".to_string()
            } else {
                w.subgraph_label.clone()
            };
            format!(
                "[{}] subgraph \"{label}\" has {} children; recommend ≤ {} for mobile rendering",
                w.kind.code(),
                w.subgraph_node_count,
                w.max_subgraph_nodes
            )
        }
        WarningKind::ComplexDiagram => format!(
            "[{}] span {} (max {}) and depth {} (max {}) both exceeded",
            w.kind.code(),
            w.actual_width,
            w.max_width,
            w.actual_depth,
            w.max_depth
        ),
    }
}

/// Formats a [`ValidationResult`] as human-readable text.
///
/// When `quiet` is `true` and there are no findings, returns an empty string.
/// When `verbose` is `true` or there are findings, per-file details are included.
pub fn format_text(result: &ValidationResult, verbose: bool, quiet: bool) -> String {
    let has_findings = !result.violations.is_empty() || !result.warnings.is_empty();
    if quiet && !has_findings {
        return String::new();
    }
    let mut sb = String::new();
    if verbose || has_findings {
        // `BTreeMap`, not a `HashMap` — deterministic key order matters
        // here: this grouping feeds the per-file `[FAIL]`/`[WARN]`/`[OK]`
        // block order directly, and `std::collections::HashMap`'s
        // randomized per-process iteration order made that order
        // nondeterministic across runs of the same binary, breaking
        // shadow-diff byte-identity (Wave D integration,
        // rewrite-rhino-cli-to-fsharp) — the same class of bug already
        // fixed in `links.rs`'s `broken_by_category`.
        let mut file_violations: BTreeMap<String, Vec<&Violation>> = BTreeMap::new();
        let mut file_warnings: BTreeMap<String, Vec<&Warning>> = BTreeMap::new();
        for v in &result.violations {
            file_violations
                .entry(v.file_path.clone())
                .or_default()
                .push(v);
        }
        for w in &result.warnings {
            file_warnings
                .entry(w.file_path.clone())
                .or_default()
                .push(w);
        }
        let mut file_set: std::collections::BTreeSet<String> = std::collections::BTreeSet::new();
        for k in file_violations.keys() {
            file_set.insert(k.clone());
        }
        for k in file_warnings.keys() {
            file_set.insert(k.clone());
        }
        for fp in file_set {
            let vs = file_violations.get(&fp);
            let ws = file_warnings.get(&fp);
            if vs.is_some_and(|v| !v.is_empty()) {
                let _ = writeln!(sb, "[FAIL] {fp}");
            } else if ws.is_some_and(|w| !w.is_empty()) {
                let _ = writeln!(sb, "[WARN] {fp}");
            } else {
                let _ = writeln!(sb, "[OK] {fp}");
            }
            if let Some(vs) = vs {
                for v in vs {
                    let _ = writeln!(
                        sb,
                        "  block {} (line {}): {}",
                        v.block_index,
                        v.start_line,
                        violation_detail(v)
                    );
                }
            }
            if let Some(ws) = ws {
                for w in ws {
                    let _ = writeln!(
                        sb,
                        "  block {} (line {}): {}",
                        w.block_index,
                        w.start_line,
                        warning_detail(w)
                    );
                }
            }
        }
    }
    let _ = writeln!(
        sb,
        "Found {} violation(s) and {} warning(s) in {} file(s) ({} block(s) scanned).",
        result.violations.len(),
        result.warnings.len(),
        result.files_scanned,
        result.blocks_scanned
    );
    sb
}

/// JSON representation of a single violation.
#[derive(Serialize)]
struct JsonViolation<'a> {
    /// Violation kind string (e.g., `"label_too_long"`).
    kind: &'a str,
    /// File path containing the diagram.
    #[serde(rename = "filePath")]
    file_path: &'a str,
    /// Zero-based index of the block within the file.
    #[serde(rename = "blockIndex")]
    block_index: usize,
    /// One-based line number where the block starts.
    #[serde(rename = "startLine")]
    start_line: usize,
    /// ID of the violating node (empty for width violations).
    #[serde(rename = "nodeId", skip_serializing_if = "str::is_empty")]
    node_id: &'a str,
    /// Full label text of the violating node (empty for width violations).
    #[serde(rename = "labelText", skip_serializing_if = "str::is_empty")]
    label_text: &'a str,
    /// Computed character length of the label.
    #[serde(rename = "labelLen", skip_serializing_if = "is_zero_usize")]
    label_len: usize,
    /// Configured maximum allowed label length.
    #[serde(rename = "maxLabelLen", skip_serializing_if = "is_zero_usize")]
    max_label_len: usize,
    /// Computed diagram width (nodes at widest rank).
    #[serde(rename = "actualWidth", skip_serializing_if = "is_zero_usize")]
    actual_width: usize,
    /// Configured maximum allowed diagram width.
    #[serde(rename = "maxWidth", skip_serializing_if = "is_zero_usize")]
    max_width: usize,
}

/// JSON representation of a single warning.
#[derive(Serialize)]
struct JsonWarning<'a> {
    /// Warning kind string.
    kind: &'a str,
    /// File path containing the diagram.
    #[serde(rename = "filePath")]
    file_path: &'a str,
    /// Zero-based index of the block within the file.
    #[serde(rename = "blockIndex")]
    block_index: usize,
    /// One-based line number where the block starts.
    #[serde(rename = "startLine")]
    start_line: usize,
    /// Computed horizontal span of the diagram.
    #[serde(rename = "actualWidth", skip_serializing_if = "is_zero_usize")]
    actual_width: usize,
    /// Computed vertical depth of the diagram.
    #[serde(rename = "actualDepth", skip_serializing_if = "is_zero_usize")]
    actual_depth: usize,
    /// Configured maximum allowed width.
    #[serde(rename = "maxWidth", skip_serializing_if = "is_zero_usize")]
    max_width: usize,
    /// Configured maximum allowed depth.
    #[serde(rename = "maxDepth", skip_serializing_if = "is_zero_usize")]
    max_depth: usize,
    /// Label of the dense subgraph (for subgraph density warnings).
    #[serde(rename = "subgraphLabel", skip_serializing_if = "str::is_empty")]
    subgraph_label: &'a str,
    /// Number of nodes in the dense subgraph.
    #[serde(rename = "subgraphNodeCount", skip_serializing_if = "is_zero_usize")]
    subgraph_node_count: usize,
    /// Configured maximum nodes per subgraph.
    #[serde(rename = "maxSubgraphNodes", skip_serializing_if = "is_zero_usize")]
    max_subgraph_nodes: usize,
}

/// Returns `true` when `n` is zero; used to omit zero-valued fields from JSON output.
#[allow(clippy::trivially_copy_pass_by_ref)]
fn is_zero_usize(n: &usize) -> bool {
    *n == 0
}

/// Top-level JSON document for the mermaid validation result.
#[derive(Serialize)]
struct JsonResult<'a> {
    /// Total number of distinct files scanned.
    #[serde(rename = "filesScanned")]
    files_scanned: usize,
    /// Total number of diagram blocks scanned.
    #[serde(rename = "blocksScanned")]
    blocks_scanned: usize,
    /// All violations found across scanned blocks.
    violations: Vec<JsonViolation<'a>>,
    /// All warnings found across scanned blocks.
    warnings: Vec<JsonWarning<'a>>,
}

/// Serialises the validation result to a pretty-printed JSON string.
///
/// # Errors
///
/// Returns an error when `serde_json` serialisation fails.
pub fn format_json(result: &ValidationResult) -> std::result::Result<String, Error> {
    let violations: Vec<JsonViolation> = result
        .violations
        .iter()
        .map(|v| JsonViolation {
            kind: v.kind.code(),
            file_path: &v.file_path,
            block_index: v.block_index,
            start_line: v.start_line,
            node_id: &v.node_id,
            label_text: &v.label_text,
            label_len: v.label_len,
            max_label_len: v.max_label_len,
            actual_width: v.actual_width,
            max_width: v.max_width,
        })
        .collect();
    let warnings: Vec<JsonWarning> = result
        .warnings
        .iter()
        .map(|w| JsonWarning {
            kind: w.kind.code(),
            file_path: &w.file_path,
            block_index: w.block_index,
            start_line: w.start_line,
            actual_width: w.actual_width,
            actual_depth: w.actual_depth,
            max_width: w.max_width,
            max_depth: w.max_depth,
            subgraph_label: &w.subgraph_label,
            subgraph_node_count: w.subgraph_node_count,
            max_subgraph_nodes: w.max_subgraph_nodes,
        })
        .collect();
    let out = JsonResult {
        files_scanned: result.files_scanned,
        blocks_scanned: result.blocks_scanned,
        violations,
        warnings,
    };
    Ok(serde_json::to_string_pretty(&out)?)
}

/// Formats the validation result as a Markdown table.
///
/// Returns a single-line "all passed" message when there are no findings.
pub fn format_markdown(result: &ValidationResult) -> String {
    if result.violations.is_empty() && result.warnings.is_empty() {
        return format!(
            "All {} block(s) in {} file(s) passed mermaid validation.\n",
            result.blocks_scanned, result.files_scanned
        );
    }
    let mut sb = String::new();
    sb.push_str("| File | Block | Line | Severity | Kind | Detail |\n");
    sb.push_str("|------|-------|------|----------|------|--------|\n");
    for v in &result.violations {
        let _ = writeln!(
            sb,
            "| {} | {} | {} | error | {} | {} |",
            v.file_path,
            v.block_index,
            v.start_line,
            v.kind.code(),
            violation_detail(v)
        );
    }
    for w in &result.warnings {
        let _ = writeln!(
            sb,
            "| {} | {} | {} | warning | {} | {} |",
            w.file_path,
            w.block_index,
            w.start_line,
            w.kind.code(),
            warning_detail(w)
        );
    }
    sb
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::domain::mermaid::{ViolationKind, WarningKind};

    fn label_violation() -> Violation {
        Violation {
            kind: ViolationKind::LabelTooLong,
            file_path: "a.md".to_string(),
            block_index: 0,
            start_line: 5,
            node_id: "A".to_string(),
            label_text: "too long".to_string(),
            label_len: 35,
            max_label_len: 30,
            actual_width: 0,
            max_width: 0,
        }
    }

    fn width_violation() -> Violation {
        Violation {
            kind: ViolationKind::WidthExceeded,
            file_path: "a.md".to_string(),
            block_index: 0,
            start_line: 10,
            node_id: String::new(),
            label_text: String::new(),
            label_len: 0,
            max_label_len: 0,
            actual_width: 5,
            max_width: 4,
        }
    }

    fn multi_violation() -> Violation {
        Violation {
            kind: ViolationKind::MultipleDiagrams,
            file_path: "a.md".to_string(),
            block_index: 0,
            start_line: 1,
            node_id: String::new(),
            label_text: String::new(),
            label_len: 0,
            max_label_len: 0,
            actual_width: 0,
            max_width: 0,
        }
    }

    fn dense_warning() -> Warning {
        Warning {
            kind: WarningKind::SubgraphDense,
            file_path: "a.md".to_string(),
            block_index: 0,
            start_line: 7,
            actual_width: 0,
            actual_depth: 0,
            max_width: 0,
            max_depth: 0,
            subgraph_label: "Foo".to_string(),
            subgraph_node_count: 8,
            max_subgraph_nodes: 6,
        }
    }

    fn complex_warning() -> Warning {
        Warning {
            kind: WarningKind::ComplexDiagram,
            file_path: "a.md".to_string(),
            block_index: 0,
            start_line: 3,
            actual_width: 6,
            actual_depth: 5,
            max_width: 4,
            max_depth: 4,
            subgraph_label: String::new(),
            subgraph_node_count: 0,
            max_subgraph_nodes: 0,
        }
    }

    #[test]
    fn format_text_quiet_with_no_findings_empty() {
        let result = ValidationResult {
            files_scanned: 1,
            blocks_scanned: 1,
            violations: Vec::new(),
            warnings: Vec::new(),
        };
        assert!(format_text(&result, false, true).is_empty());
    }

    #[test]
    fn format_text_non_quiet_with_no_findings_shows_summary() {
        let result = ValidationResult {
            files_scanned: 1,
            blocks_scanned: 2,
            violations: Vec::new(),
            warnings: Vec::new(),
        };
        let s = format_text(&result, false, false);
        assert!(s.contains("Found 0 violation(s) and 0 warning(s)"));
    }

    #[test]
    fn format_markdown_clean_yields_passed_message() {
        let result = ValidationResult {
            files_scanned: 3,
            blocks_scanned: 5,
            violations: Vec::new(),
            warnings: Vec::new(),
        };
        let s = format_markdown(&result);
        assert!(s.contains("passed mermaid validation"));
    }

    #[test]
    fn format_json_serializes_clean_result() {
        let result = ValidationResult {
            files_scanned: 2,
            blocks_scanned: 3,
            violations: Vec::new(),
            warnings: Vec::new(),
        };
        let s = format_json(&result).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["filesScanned"], 2);
        assert_eq!(v["blocksScanned"], 3);
    }

    #[test]
    fn format_text_with_violations_renders() {
        let result = ValidationResult {
            files_scanned: 1,
            blocks_scanned: 1,
            violations: vec![label_violation(), width_violation(), multi_violation()],
            warnings: Vec::new(),
        };
        let s = format_text(&result, false, false);
        assert!(s.contains("[FAIL] a.md"));
        assert!(s.contains("label_too_long"));
        assert!(s.contains("width_exceeded"));
        assert!(s.contains("multiple_diagrams"));
    }

    #[test]
    fn format_text_with_warnings_only_uses_warn_marker() {
        let result = ValidationResult {
            files_scanned: 1,
            blocks_scanned: 1,
            violations: Vec::new(),
            warnings: vec![dense_warning(), complex_warning()],
        };
        let s = format_text(&result, false, false);
        assert!(s.contains("[WARN] a.md"));
        assert!(s.contains("subgraph_density"));
        assert!(s.contains("complex_diagram"));
    }

    #[test]
    fn format_text_verbose_with_no_findings_shows_summary() {
        let result = ValidationResult {
            files_scanned: 2,
            blocks_scanned: 3,
            violations: Vec::new(),
            warnings: Vec::new(),
        };
        let s = format_text(&result, true, false);
        assert!(s.contains("Found 0 violation"));
    }

    #[test]
    fn format_markdown_with_findings_renders_table() {
        let result = ValidationResult {
            files_scanned: 1,
            blocks_scanned: 1,
            violations: vec![label_violation()],
            warnings: vec![dense_warning()],
        };
        let s = format_markdown(&result);
        assert!(s.contains("| File | Block | Line | Severity | Kind | Detail |"));
        assert!(s.contains("error"));
        assert!(s.contains("warning"));
    }

    #[test]
    fn format_json_with_findings_serializes() {
        let result = ValidationResult {
            files_scanned: 1,
            blocks_scanned: 1,
            violations: vec![label_violation(), width_violation()],
            warnings: vec![complex_warning()],
        };
        let s = format_json(&result).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["violations"].as_array().unwrap().len(), 2);
        assert_eq!(v["warnings"].as_array().unwrap().len(), 1);
    }
}
