//! Frontmatter and body date-annotation audit.
//!
//! Byte-for-byte port of `apps/rhino-cli/internal/repo-governance/frontmatter_audit.go`.

use std::path::Path;
use std::sync::OnceLock;

use anyhow::{Context, Error, anyhow};
use regex::Regex;

use crate::application::fs::port::Fs;

/// A violation found by the frontmatter or body-annotation audit.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FrontmatterFinding {
    /// Path of the file containing the violation.
    pub file: String,
    /// 1-based line number of the offending content.
    pub line: usize,
    /// Severity; currently always `"high"`.
    pub severity: String,
    /// Human-readable description of the violation.
    pub message: String,
}

/// Returns a compiled `Regex` matching a `**Last Updated**` bold marker in
/// body text.
fn last_updated_footer_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"\*\*Last Updated\*\*").expect("valid hardcoded regex"))
}

/// Returns a compiled `Regex` matching an inline bullet `**Created**:` or
/// `**Last Updated**:` date annotation in body text.
fn inline_date_annotation_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(r"^\s*-\s+\*\*(Created|Last Updated)\*\*:\s*\d{4}-\d{2}-\d{2}")
            .expect("valid hardcoded regex")
    })
}

/// Audits each directory in `paths` for YAML frontmatter violations and
/// forbidden body-level date annotations.
///
/// Skips files under the configured exclusion prefixes. Findings are sorted by
/// `file`, then by `line`.
///
/// # Errors
///
/// Returns an error when `paths` is empty or when a file cannot be read.
pub fn audit_frontmatter(
    fs: &dyn Fs,
    paths: &[String],
    excluded_prefixes: &[String],
) -> std::result::Result<Vec<FrontmatterFinding>, Error> {
    if paths.is_empty() {
        return Err(anyhow!("at least one path is required"));
    }
    let mut findings = Vec::new();
    for root in paths {
        let files = walk_paths(fs, root, excluded_prefixes);
        let mut more = scan_paths(fs, &files)?;
        findings.append(&mut more);
    }
    findings.sort_by(|a, b| a.file.cmp(&b.file).then(a.line.cmp(&b.line)));
    Ok(findings)
}

/// Recursively walks `root` and returns sorted paths of `.md` files that are
/// not inside a website-app directory.
fn walk_paths(fs: &dyn Fs, root: &str, excluded_prefixes: &[String]) -> Vec<String> {
    let root_p = Path::new(root);
    let mut files: Vec<String> = fs
        .walk_files(root_p, &[])
        .into_iter()
        .filter(|p| {
            p.file_name()
                .is_some_and(|n| n.to_string_lossy().ends_with(".md"))
        })
        .map(|p| p.to_string_lossy().to_string())
        .filter(|p| !is_excluded(p, excluded_prefixes))
        .collect();
    files.sort();
    files
}

/// Reads each file in `paths` and scans its content for frontmatter and body
/// violations.
///
/// # Errors
///
/// Returns an error when a file cannot be read.
fn scan_paths(
    fs: &dyn Fs,
    paths: &[String],
) -> std::result::Result<Vec<FrontmatterFinding>, Error> {
    let mut findings = Vec::new();
    for p in paths {
        let data = fs
            .read_to_string(Path::new(p))
            .with_context(|| format!("read {p}"))?;
        findings.append(&mut scan_frontmatter_content(p, &data));
    }
    Ok(findings)
}

/// Extracts the frontmatter and body from `content` and delegates to the
/// per-section checkers.
fn scan_frontmatter_content(path: &str, content: &str) -> Vec<FrontmatterFinding> {
    let mut findings = Vec::new();
    let (frontmatter, frontmatter_end_line, body) = split_frontmatter(content);
    findings.extend(check_frontmatter_updated_field(path, &frontmatter));
    findings.extend(check_body_annotations(path, &body, frontmatter_end_line));
    findings
}

/// Splits `content` into `(frontmatter, end_line, body)`.
///
/// `end_line` is the 1-based line number of the closing `---` fence, or `0`
/// when no valid frontmatter is present.  An unclosed block is treated as if
/// there is no frontmatter.
fn split_frontmatter(content: &str) -> (String, usize, String) {
    let lines: Vec<&str> = content.split('\n').collect();
    if lines.is_empty() || lines[0].trim() != "---" {
        return (String::new(), 0, content.to_string());
    }
    for i in 1..lines.len() {
        if lines[i].trim() == "---" {
            let fm = lines[1..i].join("\n");
            let body_start = i + 1;
            if body_start >= lines.len() {
                return (fm, i + 1, String::new());
            }
            return (fm, i + 1, lines[body_start..].join("\n"));
        }
    }
    // Unclosed frontmatter: treat as no frontmatter.
    (String::new(), 0, content.to_string())
}

/// Returns a finding when the parsed `frontmatter` YAML contains a forbidden
/// `updated:` field.
fn check_frontmatter_updated_field(path: &str, frontmatter: &str) -> Vec<FrontmatterFinding> {
    if frontmatter.is_empty() {
        return Vec::new();
    }
    let Ok(parsed): std::result::Result<serde_norway::Value, _> =
        serde_norway::from_str(frontmatter)
    else {
        return Vec::new(); // unparseable YAML is out of scope
    };
    let serde_norway::Value::Mapping(mapping) = parsed else {
        return Vec::new();
    };
    if !mapping.contains_key(serde_norway::Value::String("updated".to_string())) {
        return Vec::new();
    }
    let line = find_field_line(frontmatter, "updated");
    vec![FrontmatterFinding {
        file: path.to_string(),
        line,
        severity: "high".to_string(),
        message: r#"forbidden "updated:" field in YAML frontmatter; remove per no-date-metadata convention"#.to_string(),
    }]
}

/// Returns the 1-based file-level line number of the first occurrence of
/// `field:` within `frontmatter`.
///
/// Falls back to line `2` (the first line after the opening `---`) when the
/// field is not found.
fn find_field_line(frontmatter: &str, field: &str) -> usize {
    let prefix = format!("{field}:");
    for (i, line) in frontmatter.split('\n').enumerate() {
        if line.trim_start_matches(' ').starts_with(&prefix) {
            return i + 2;
        }
    }
    2
}

/// Scans `body` for forbidden inline date annotations and `**Last Updated**`
/// footer markers.
///
/// `frontmatter_end_line` is added to each relative line index to produce
/// absolute file-level line numbers.
fn check_body_annotations(
    path: &str,
    body: &str,
    frontmatter_end_line: usize,
) -> Vec<FrontmatterFinding> {
    if body.is_empty() {
        return Vec::new();
    }
    let mut findings = Vec::new();
    let start_line = if frontmatter_end_line == 0 {
        1
    } else {
        frontmatter_end_line + 1
    };
    for (i, line) in body.split('\n').enumerate() {
        let line_num = start_line + i;
        if inline_date_annotation_re().is_match(line) {
            findings.push(FrontmatterFinding {
                file: path.to_string(),
                line: line_num,
                severity: "high".to_string(),
                message: "forbidden inline date annotation in body; remove per no-date-metadata convention".to_string(),
            });
            continue;
        }
        if last_updated_footer_re().is_match(line) {
            findings.push(FrontmatterFinding {
                file: path.to_string(),
                line: line_num,
                severity: "high".to_string(),
                message: "forbidden **Last Updated** footer marker in body; remove per no-date-metadata convention".to_string(),
            });
        }
    }
    findings
}

/// Returns `true` when `path` contains a configured exclusion prefix.
fn is_excluded(path: &str, excluded_prefixes: &[String]) -> bool {
    let slashed = path.replace('\\', "/");
    excluded_prefixes
        .iter()
        .any(|prefix| slashed.contains(prefix))
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::infrastructure::fs::real::RealFs;
    use std::fs;
    use tempfile::TempDir;

    #[test]
    fn audit_frontmatter_empty_paths_errors() {
        let err = audit_frontmatter(&RealFs, &[], &[]).unwrap_err();
        assert!(err.to_string().contains("at least one path"));
    }

    #[test]
    fn detects_forbidden_updated_frontmatter_field() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("doc.md");
        fs::write(&p, "---\ntitle: Doc\nupdated: 2026-01-01\n---\n\n# Body\n").unwrap();
        let findings =
            audit_frontmatter(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert_eq!(findings.len(), 1);
        assert!(findings[0].message.contains("updated:"));
        assert_eq!(findings[0].line, 3);
        assert_eq!(findings[0].severity, "high");
    }

    #[test]
    fn detects_last_updated_footer() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("doc.md");
        fs::write(&p, "# Title\n\nBody.\n\n**Last Updated**: 2026-01-01\n").unwrap();
        let findings =
            audit_frontmatter(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert_eq!(findings.len(), 1);
        assert!(findings[0].message.contains("**Last Updated**"));
        assert_eq!(findings[0].line, 5);
    }

    #[test]
    fn detects_inline_date_annotation() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("doc.md");
        fs::write(
            &p,
            "# Title\n\n- **Created**: 2026-01-01\n- **Last Updated**: 2026-02-02\n",
        )
        .unwrap();
        let findings =
            audit_frontmatter(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert_eq!(findings.len(), 2);
        assert!(findings[0].message.contains("inline date annotation"));
        assert!(findings[1].message.contains("inline date annotation"));
    }

    #[test]
    fn skips_configured_exclusions() {
        let tmp = TempDir::new().unwrap();
        let dir = tmp.path().join("apps/ose-www/content");
        fs::create_dir_all(&dir).unwrap();
        fs::write(dir.join("post.md"), "---\nupdated: 2026-01-01\n---\n").unwrap();
        let findings = audit_frontmatter(
            &RealFs,
            &[tmp.path().to_string_lossy().to_string()],
            &["apps/ose-www/".to_string()],
        )
        .unwrap();
        assert!(findings.is_empty());
    }

    #[test]
    fn passes_clean_file() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("doc.md");
        fs::write(&p, "---\ntitle: Doc\n---\n\nClean body.\n").unwrap();
        let findings =
            audit_frontmatter(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(findings.is_empty());
    }

    #[test]
    fn sorts_findings_by_file_then_line() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("b.md"), "---\nupdated: 2026-01-01\n---\n").unwrap();
        fs::write(
            tmp.path().join("a.md"),
            "# T\n\n**Last Updated**: 2026-01-01\n",
        )
        .unwrap();
        let findings =
            audit_frontmatter(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert_eq!(findings.len(), 2);
        assert!(findings[0].file.ends_with("a.md"));
        assert!(findings[1].file.ends_with("b.md"));
    }

    #[test]
    fn unclosed_frontmatter_treated_as_body() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("doc.md");
        // Unclosed frontmatter — entire content treated as body.
        fs::write(&p, "---\ntitle: Doc\n\n**Last Updated**: x\n").unwrap();
        let findings =
            audit_frontmatter(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert_eq!(findings.len(), 1);
        assert_eq!(findings[0].line, 4);
    }

    #[test]
    fn split_frontmatter_returns_close_line() {
        let (fm, end, body) = split_frontmatter("---\ntitle: x\n---\nbody\n");
        assert_eq!(fm, "title: x");
        assert_eq!(end, 3);
        assert_eq!(body, "body\n");
    }

    #[test]
    fn split_frontmatter_no_fence() {
        let (fm, end, body) = split_frontmatter("just body\n");
        assert!(fm.is_empty());
        assert_eq!(end, 0);
        assert_eq!(body, "just body\n");
    }

    #[test]
    fn find_field_line_locates_updated() {
        let fm = "title: x\nfoo: bar\nupdated: 2026-01-01\n";
        // updated is line 3 inside frontmatter = line 4 in file (line 1 = ---).
        // findFieldLine returns i+2 where i=2 (0-based) → 4.
        assert_eq!(find_field_line(fm, "updated"), 4);
    }
}
