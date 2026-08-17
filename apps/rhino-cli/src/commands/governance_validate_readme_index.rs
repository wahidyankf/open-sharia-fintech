//! `rhino-cli governance readme-index validate` — checks that every covered
//! directory has a README index, that every entry is linked, resolves, and
//! carries a derived annotation.
//!
//! Rename-and-extend of `commands/md_validate_readme_index.rs`
//! (`tech-docs.md` §1.4/§4): shares one implementation across two
//! `repo-config.yml` gate registrations — `governance-readme-index`
//! (`orphan`/`ghost`, continuity-preserving) and
//! `governance-readme-completeness` (`missing`/`unannotated`, dark-launched)
//! — differentiated entirely by each registration's `args:` block, via
//! `--paths` and `--fail-kinds` (FR-1.10/FR-1.11/FR-5.8).

use std::fmt::Write as _;
use std::path::Path;

use anyhow::{Context, Error, anyhow};
use clap::Args;
use serde::Serialize;

use crate::application::governance::readme_index::{ReadmeIndexFinding, audit_readme_index};
use crate::domain::cliout::OutputFormat;
use crate::infrastructure::fs::real::RealFs;
use crate::internal::git;

/// JSON output schema identifier for this command.
const SCHEMA: &str = "rhino-cli/readme-index-audit/v1";

/// Default paths scanned when no `--paths` flag is supplied.
///
/// Every content tree the repository governs, so a bare invocation matches
/// what the `governance-readme-index` gate enforces rather than a narrower
/// legacy subset. The generated harness mirrors (`.opencode/`, `.cursor/`,
/// `.amazonq/`) are deliberately absent: they are emitted from `.claude/` by
/// `harness bindings generate`, are never hand-edited, and an index written
/// into them would be regenerated away — `.claude/`, their source of truth,
/// is scanned instead.
///
/// `pub(crate)` — reused as-is by `governance readme-index generate`
/// (`commands::governance_generate_readme_index`, FR-3.12) so `generate` and
/// `validate` default to exactly the same scan scope, per the same "one
/// constant, no drift" rationale [`resolve_scan_paths`]'s doc comment states.
pub(crate) const DEFAULT_PATHS: &[&str] = &["docs/", "repo-governance/", "specs/", ".claude/"];

/// CLI arguments for `governance readme-index validate`.
#[derive(Args, Debug)]
pub struct ReadmeIndexAuditArgs {
    /// Glob to exclude from audit (repeatable).
    #[arg(long = "exclude")]
    pub exclude: Vec<String>,
    /// Path to scan (repeatable). Overrides `DEFAULT_PATHS` when given;
    /// `DEFAULT_PATHS` is used unchanged when absent (FR-1.10).
    #[arg(long = "paths")]
    pub paths: Vec<String>,
    /// Finding kind that contributes to the nonzero exit code (repeatable;
    /// `orphan`/`ghost`/`missing`/`unannotated`). Every kind is still
    /// discovered and printed regardless — when absent, all kinds fail,
    /// preserving today's standalone-CLI behavior (FR-1.11).
    #[arg(long = "fail-kinds")]
    pub fail_kinds: Vec<String>,
    /// Positional paths (legacy override, same effect as `--paths`).
    pub positional: Vec<String>,
}

/// Single README index finding in JSON output.
#[derive(Serialize)]
struct JsonFinding<'a> {
    /// Path of the file containing the finding.
    file: &'a str,
    /// Severity label.
    severity: &'a str,
    /// Finding category (e.g. `"orphan"`, `"ghost"`, `"missing"`, `"unannotated"`).
    kind: &'a str,
    /// Human-readable description.
    message: &'a str,
}

/// Inner result payload in JSON output.
#[derive(Serialize)]
struct InnerResult<'a> {
    /// Individual findings.
    findings: Vec<JsonFinding<'a>>,
}

/// JSON envelope wrapping the README index audit result.
#[derive(Serialize)]
struct Envelope<'a> {
    /// Output schema identifier.
    schema: &'a str,
    /// `"passed"` or `"failed"`.
    status: &'a str,
    /// Detailed result.
    result: InnerResult<'a>,
}

/// Resolves the scan-path list for this invocation.
///
/// `--paths` (repeatable) wins when given; the legacy `positional` argument
/// is honored next; `DEFAULT_PATHS` is used, unchanged, when neither is
/// given (FR-1.10 — this is how `governance-readme-index`'s continuity
/// guarantee falls out of "don't pass the flag," not a second constant to
/// keep in sync).
#[must_use]
pub fn resolve_scan_paths(args: &ReadmeIndexAuditArgs) -> Vec<String> {
    if !args.paths.is_empty() {
        return args.paths.clone();
    }
    if !args.positional.is_empty() {
        return args.positional.clone();
    }
    DEFAULT_PATHS
        .iter()
        .map(std::string::ToString::to_string)
        .collect()
}

/// Returns `true` when at least one finding's `kind` is in `fail_kinds`
/// (FR-1.11). When `fail_kinds` is empty, every kind contributes **except**
/// `unannotated` (FR-3.20): that kind is dark-launched — discoverable and
/// printed, but never contributes to the exit code until it is explicitly
/// named in `--fail-kinds` (Phase 9's `governance-readme-completeness` gate
/// arms it that way). `orphan`/`ghost`/`missing` preserve today's
/// standalone-CLI behavior: any occurrence fails.
#[must_use]
pub fn has_failing_finding(findings: &[ReadmeIndexFinding], fail_kinds: &[String]) -> bool {
    if fail_kinds.is_empty() {
        return findings.iter().any(|f| f.kind != "unannotated");
    }
    findings
        .iter()
        .any(|f| fail_kinds.iter().any(|k| k == &f.kind))
}

/// Run the `governance readme-index validate` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, the audit fails, or a
/// finding whose kind is in `--fail-kinds` (or, when absent, any finding) is
/// detected.
pub fn run(
    args: &ReadmeIndexAuditArgs,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    let rel_paths = resolve_scan_paths(args);
    let full_paths: Vec<String> = rel_paths
        .iter()
        .map(|p| {
            if Path::new(p).is_absolute() {
                p.clone()
            } else {
                repo_root.join(p).to_string_lossy().to_string()
            }
        })
        .collect();

    let findings = audit_readme_index(&RealFs, &full_paths, &args.exclude)
        .context("readme-index audit failed")?;

    match output_format {
        OutputFormat::Text => print!("{}", format_text(&findings)),
        OutputFormat::Json => print!("{}", format_json(&findings)?),
        OutputFormat::Markdown => print!("{}", format_markdown(&findings)),
    }

    if has_failing_finding(&findings, &args.fail_kinds) {
        return Err(anyhow!("{} readme-index finding(s) found", findings.len()));
    }
    Ok(())
}

/// Format README index findings as human-readable text.
fn format_text(findings: &[ReadmeIndexFinding]) -> String {
    if findings.is_empty() {
        return "README INDEX AUDIT PASSED: no orphan or ghost references found\n".to_string();
    }
    let mut sb = String::new();
    let _ = writeln!(
        sb,
        "README INDEX AUDIT FAILED: {} finding(s)",
        findings.len()
    );
    for f in findings {
        let _ = writeln!(
            sb,
            "  {}  [{}/{}]  {}",
            f.file, f.severity, f.kind, f.message
        );
    }
    sb
}

/// Serialize README index findings as a JSON envelope string.
///
/// # Errors
///
/// Returns an error if JSON serialization fails.
fn format_json(findings: &[ReadmeIndexFinding]) -> std::result::Result<String, Error> {
    let jf: Vec<JsonFinding> = findings
        .iter()
        .map(|f| JsonFinding {
            file: &f.file,
            severity: &f.severity,
            kind: &f.kind,
            message: &f.message,
        })
        .collect();
    let status = if findings.is_empty() {
        "passed"
    } else {
        "failed"
    };
    let env = Envelope {
        schema: SCHEMA,
        status,
        result: InnerResult { findings: jf },
    };
    let mut s = serde_json::to_string_pretty(&env)?;
    s.push('\n');
    Ok(s)
}

/// Format README index findings as a Markdown table.
fn format_markdown(findings: &[ReadmeIndexFinding]) -> String {
    if findings.is_empty() {
        return "## README Index Audit\n\n**PASSED**: no orphan or ghost references found\n"
            .to_string();
    }
    let mut sb = String::new();
    let _ = writeln!(
        sb,
        "## README Index Audit\n\n**FAILED**: {} finding(s)\n",
        findings.len()
    );
    sb.push_str("| File | Severity | Kind | Message |\n");
    sb.push_str("|------|----------|------|---------|\n");
    for f in findings {
        let _ = writeln!(
            sb,
            "| {} | {} | {} | {} |",
            f.file, f.severity, f.kind, f.message
        );
    }
    sb
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    fn sample() -> ReadmeIndexFinding {
        ReadmeIndexFinding {
            file: "a.md".to_string(),
            severity: "high".to_string(),
            kind: "orphan".to_string(),
            message: "msg".to_string(),
        }
    }

    #[test]
    fn format_text_passed() {
        assert!(format_text(&[]).starts_with("README INDEX AUDIT PASSED"));
    }

    #[test]
    fn format_text_failed() {
        let s = format_text(&[sample()]);
        assert!(s.contains("README INDEX AUDIT FAILED: 1"));
        assert!(s.contains("a.md  [high/orphan]"));
    }

    #[test]
    fn format_json_passed() {
        let s = format_json(&[]).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["status"], "passed");
        assert_eq!(v["schema"], SCHEMA);
    }

    #[test]
    fn format_json_failed() {
        let s = format_json(&[sample()]).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["status"], "failed");
        assert_eq!(v["result"]["findings"][0]["kind"], "orphan");
    }

    #[test]
    fn format_markdown_passed() {
        assert!(format_markdown(&[]).contains("**PASSED**"));
    }

    #[test]
    fn format_markdown_failed() {
        let s = format_markdown(&[sample()]);
        assert!(s.contains("**FAILED**: 1"));
        assert!(s.contains("| a.md | high | orphan | msg |"));
    }

    // -----------------------------------------------------------------------
    // Phase 1a (TDD RED) — plans/done/2026-08-15__optimize-governance-md
    //
    // FR-1.10/FR-1.11/FR-5.8: two new repeatable flags land on
    // `ReadmeIndexAuditArgs` — `--paths` (overrides `DEFAULT_PATHS`) and
    // `--fail-kinds` (restricts which discovered finding kinds contribute to
    // the nonzero exit code). Both `resolve_scan_paths` and
    // `has_failing_finding` are the natural pure-function extraction points
    // Phase 1b introduces for this.
    // -----------------------------------------------------------------------

    #[test]
    fn paths_flag_overrides_default_paths_when_given() {
        let args = ReadmeIndexAuditArgs {
            exclude: vec![],
            paths: vec!["repo-governance/".to_string()],
            fail_kinds: vec![],
            positional: vec![],
        };
        let resolved = resolve_scan_paths(&args);
        assert_eq!(
            resolved,
            vec!["repo-governance/".to_string()],
            "FR-1.10: --paths must override DEFAULT_PATHS when given"
        );
    }

    #[test]
    fn paths_flag_falls_back_to_default_paths_when_absent() {
        let args = ReadmeIndexAuditArgs {
            exclude: vec![],
            paths: vec![],
            fail_kinds: vec![],
            positional: vec![],
        };
        let resolved = resolve_scan_paths(&args);
        let expected: Vec<String> = DEFAULT_PATHS
            .iter()
            .map(std::string::ToString::to_string)
            .collect();
        assert_eq!(
            resolved, expected,
            "FR-1.10: with no --paths flag, the unwidened DEFAULT_PATHS list must be used \
             unchanged — this is how FR-3.19's continuity guarantee falls out of 'don't pass \
             the flag'"
        );
    }

    #[test]
    fn fail_kinds_flag_restricts_which_findings_contribute_to_the_exit_code() {
        let orphan_finding = ReadmeIndexFinding {
            file: "orphan.md".to_string(),
            severity: "high".to_string(),
            kind: "orphan".to_string(),
            message: "m".to_string(),
        };
        let missing_finding = ReadmeIndexFinding {
            file: "some-dir".to_string(),
            severity: "high".to_string(),
            kind: "missing".to_string(),
            message: "m".to_string(),
        };
        let findings = vec![orphan_finding.clone(), missing_finding];

        assert!(
            has_failing_finding(&findings, &["orphan".to_string()]),
            "FR-1.11: an 'orphan' finding must contribute to the exit code when \
             --fail-kinds orphan is set"
        );
        assert!(
            !has_failing_finding(
                std::slice::from_ref(&orphan_finding),
                &["missing".to_string()]
            ),
            "FR-1.11: an 'orphan' finding must NOT contribute to the exit code when \
             --fail-kinds is scoped to 'missing' only — mirrors governance-readme-index's \
             continuity guarantee (FR-3.19)"
        );
    }

    #[test]
    fn every_finding_kind_is_still_printed_regardless_of_fail_kinds() {
        // FR-1.11: "the command still discovers and reports every finding
        // kind on the scanned scope" — format_text is unfiltered by
        // --fail-kinds, so a 'missing' finding must still appear in the text
        // report even when --fail-kinds is scoped to 'orphan' only.
        let missing_finding = ReadmeIndexFinding {
            file: "some-dir".to_string(),
            severity: "high".to_string(),
            kind: "missing".to_string(),
            message: "directory lacks a README.md".to_string(),
        };
        let text = format_text(&[missing_finding]);
        assert!(
            text.contains("missing"),
            "a 'missing' finding must be printed even when --fail-kinds excludes it: {text}"
        );
        assert!(
            !has_failing_finding(
                &[ReadmeIndexFinding {
                    file: "some-dir".to_string(),
                    severity: "high".to_string(),
                    kind: "missing".to_string(),
                    message: "m".to_string(),
                }],
                &["orphan".to_string()]
            ),
            "the same finding must not contribute to the exit code when its kind is excluded \
             from --fail-kinds"
        );
    }

    #[test]
    fn scenario_unannotated_finding_kind_fails_once_armed_and_in_scope() {
        // FR-3.20: the "unannotated" kind is discoverable at Phase 1
        // (`readme_index.rs`'s `scenario_unannotated_finding_kind_is_discoverable`)
        // but does not fail the build until a gate registration explicitly
        // arms it via `--fail-kinds unannotated` (the
        // `governance-readme-completeness` gate id, Phase 9). This test
        // proves the CLI-level mechanism that makes that later arming a
        // config-only flip: once `--fail-kinds` includes "unannotated", a
        // discovered unannotated finding does contribute to the exit code.
        let unannotated_finding = ReadmeIndexFinding {
            file: "linking.md".to_string(),
            severity: "high".to_string(),
            kind: "unannotated".to_string(),
            message: "m".to_string(),
        };
        assert!(
            !has_failing_finding(
                std::slice::from_ref(&unannotated_finding),
                &["orphan".to_string(), "ghost".to_string()]
            ),
            "before arming: governance-readme-index's fail-kinds (orphan, ghost) must not fail \
             on an unannotated finding"
        );
        assert!(
            has_failing_finding(
                std::slice::from_ref(&unannotated_finding),
                &["missing".to_string(), "unannotated".to_string()]
            ),
            "once armed: governance-readme-completeness's fail-kinds (missing, unannotated) \
             must fail on an unannotated finding"
        );
    }
}
