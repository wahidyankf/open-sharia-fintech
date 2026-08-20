//! `rhino-cli governance word-budget validate` — checks instruction files
//! against their word budgets defined in the `governance-word-budget:`
//! section of `repo-config.yml`.
//!
//! Merged command file (`tech-docs.md` §1.4 "Command file merge note"):
//! absorbs `commands/convention_validate_instruction_size.rs`'s
//! implementation (schema, `run_for_root`, formatters) and
//! `commands/harness_validate_instruction_size.rs`'s CLI-arg-parsing entry
//! point — the delegation indirection between the two is removed.
//!
//! Reads the per-surface and resolved-tree budgets, globs for each surface
//! file, classifies word counts, and returns exit code 1 when any file
//! exceeds its fail threshold.

use std::fmt::Write as _;
use std::path::Path;

use anyhow::{Error, anyhow};
use clap::Args;
use serde::Serialize;

use crate::application::governance::word_budget::{
    BudgetConfig, Finding, Severity, check_instruction_sizes, check_resolved_tree,
    merged_budget_config, severity_label,
};
use crate::domain::cliout::OutputFormat;
use crate::infrastructure::fs::real::RealFs;
use crate::internal::git;

/// JSON output schema identifier for this command.
pub const SCHEMA: &str = "rhino-cli/governance-word-budget/v1";

/// CLI arguments for `governance word-budget validate`.
#[derive(Args, Debug)]
pub struct ValidateWordBudgetArgs {
    /// Repository-relative path **prefix** to exclude from scanning
    /// (repeatable), matched via `str::starts_with` — not a glob, unlike the
    /// identically-named `--exclude` flag on `md links validate`/`md mermaid
    /// validate`. `.opencode/skills/` excludes the whole tree;
    /// `.opencode/skills/*` matches nothing. Keeps the catch-all
    /// `**/README.md` surface from reaching trees the
    /// `governance-word-budget:` surfaces list was never meant to cover
    /// (e.g. `plans/`, `docs/`, `specs/`, a local `.fvm/` cache) — not a
    /// per-file waiver on an in-scope surface (FR-1.5 still forbids that).
    #[arg(long = "exclude")]
    pub exclude: Vec<String>,
}

// ---------------------------------------------------------------------------
// JSON serialization types
// ---------------------------------------------------------------------------

/// A single finding in the JSON envelope.
#[derive(Serialize)]
struct FindingPayload<'a> {
    /// Repo-relative path of the instruction file (or `"resolved-tree"`).
    path: &'a str,
    /// Measured size in words.
    size: u64,
    /// Target budget in words.
    target: u64,
    /// Warning threshold in words.
    warn: u64,
    /// Fail threshold in words.
    fail: u64,
    /// Severity label: `"ok"`, `"warn"`, or `"fail"`.
    severity: &'a str,
    /// Human-readable description.
    message: &'a str,
}

/// JSON envelope wrapping the word-budget audit result.
#[derive(Serialize)]
struct Envelope<'a> {
    /// Output schema identifier.
    schema: &'a str,
    /// `"passed"` or `"failed"`.
    status: &'a str,
    /// Summary counts.
    total_findings: usize,
    /// Individual findings.
    findings: Vec<FindingPayload<'a>>,
}

// ---------------------------------------------------------------------------
// Public command entry-point
// ---------------------------------------------------------------------------

/// Run the `governance word-budget validate` command.
///
/// Discovers the git repository root and delegates to [`run_for_root`].
///
/// # Errors
///
/// Returns an error when the git root cannot be found, the budget config
/// cannot be loaded, or any instruction file exceeds its fail budget.
pub fn run(
    args: &ValidateWordBudgetArgs,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    // Merge the gate-registration `args.exclude` list (see
    // `registered_excludes`) with any explicit `--exclude` flags so the bare
    // CLI command excludes the same trees the pre-push/CI surface does,
    // without requiring the caller to repeat the registered list by hand.
    let mut excludes =
        crate::application::governance::word_budget::registered_excludes(&repo_root)?;
    excludes.extend(args.exclude.iter().cloned());
    run_for_root(&repo_root, output_format, &excludes)
}

/// Core logic for `governance word-budget validate`, exposed for testing.
///
/// Reads the `governance-word-budget:` section of `repo-config.yml` (see
/// [`merged_budget_config`]). When the section is absent, the command skips
/// gracefully.
///
/// # Errors
///
/// Returns an error when the budget config cannot be loaded or any
/// instruction file exceeds its fail budget.
pub fn run_for_root(
    repo_root: &Path,
    output_format: OutputFormat,
    excludes: &[String],
) -> std::result::Result<(), Error> {
    let Some(merged_config) = merged_budget_config(repo_root)? else {
        if output_format == OutputFormat::Text {
            println!(
                "WORD BUDGET: SKIPPED (no governance-word-budget: section in repo-config.yml)"
            );
        }
        return Ok(());
    };

    let mut findings = check_instruction_sizes(&RealFs, repo_root, &merged_config, excludes);
    if let Some(tree_finding) = check_resolved_tree(&RealFs, repo_root, &merged_config) {
        findings.push(tree_finding);
    }

    let has_fail = findings.iter().any(|f| f.severity == Severity::Fail);

    match output_format {
        OutputFormat::Text => print!("{}", format_text(&findings)),
        OutputFormat::Json => print!("{}", format_json(&findings, &merged_config)?),
        OutputFormat::Markdown => print!("{}", format_markdown(&findings)),
    }

    if has_fail {
        let fail_count = findings
            .iter()
            .filter(|f| f.severity == Severity::Fail)
            .count();
        return Err(anyhow!(
            "word-budget audit failed: {fail_count} Fail finding(s); apply progressive disclosure \
             — see repo-governance/principles/content/progressive-disclosure.md"
        ));
    }
    Ok(())
}

// ---------------------------------------------------------------------------
// Formatters (pure functions — testable without I/O)
// ---------------------------------------------------------------------------

/// Format word-budget findings as human-readable text.
fn format_text(findings: &[Finding]) -> String {
    if findings.is_empty() {
        return "WORD BUDGET: PASSED — all surfaces within budget\n".to_string();
    }
    let mut sb = String::new();
    let _ = writeln!(sb, "WORD BUDGET: {} finding(s)", findings.len());
    for f in findings {
        let label = match f.severity {
            Severity::Ok => "PASS",
            Severity::Warn => "WARN",
            Severity::Fail => "FAIL",
        };
        let _ = writeln!(sb, "  [{}] {} — {}", label, f.path, f.message);
    }
    sb
}

/// Serialize word-budget findings as a JSON envelope string.
///
/// # Errors
///
/// Returns an error if JSON serialization fails.
fn format_json(findings: &[Finding], _config: &BudgetConfig) -> std::result::Result<String, Error> {
    let has_fail = findings.iter().any(|f| f.severity == Severity::Fail);
    let status = if has_fail { "failed" } else { "passed" };
    let payloads: Vec<FindingPayload<'_>> = findings
        .iter()
        .map(|f| FindingPayload {
            path: &f.path,
            size: f.size,
            target: f.target,
            warn: f.warn,
            fail: f.fail,
            severity: severity_label(&f.severity),
            message: &f.message,
        })
        .collect();
    let env = Envelope {
        schema: SCHEMA,
        status,
        total_findings: findings.len(),
        findings: payloads,
    };
    let mut s = serde_json::to_string_pretty(&env)?;
    s.push('\n');
    Ok(s)
}

/// Format word-budget findings as a Markdown table.
fn format_markdown(findings: &[Finding]) -> String {
    let mut sb = String::new();
    sb.push_str("## Word Budget Audit\n\n");
    if findings.is_empty() {
        sb.push_str("**PASSED**: all surfaces within budget\n");
        return sb;
    }
    let _ = writeln!(
        sb,
        "**{}**: {} finding(s)\n",
        if findings.iter().any(|f| f.severity == Severity::Fail) {
            "FAILED"
        } else {
            "WARN"
        },
        findings.len()
    );
    sb.push_str("| Path | Size (words) | Severity | Message |\n");
    sb.push_str("| --- | --- | --- | --- |\n");
    for f in findings {
        let sev = severity_label(&f.severity);
        let _ = writeln!(
            sb,
            "| `{}` | {} | {} | {} |",
            f.path, f.size, sev, f.message
        );
    }
    sb
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::application::governance::word_budget as wb;
    use std::fs;
    use tempfile::TempDir;

    fn n_words(n: usize) -> String {
        vec!["w"; n].join(" ")
    }

    fn write_budget_yaml(dir: &Path) {
        let yaml = concat!(
            "harness: []\n",
            "coverage:\n  projects: []\n",
            "specs:\n  ddd-areas: []\n  domain-areas: []\n",
            "governance-word-budget:\n",
            "  surfaces:\n",
            "    - glob: \"AGENTS.md\"\n",
            "      target: 400\n",
            "      warn: 500\n",
            "      fail: 500\n",
            "  resolved_tree:\n",
            "    root: \"CLAUDE.md\"\n",
            "    target: 1200\n",
            "    warn: 1500\n",
            "    fail: 1500\n",
        );
        fs::write(dir.join("repo-config.yml"), yaml).unwrap();
    }

    fn write_small_claude(dir: &Path) {
        fs::write(dir.join("CLAUDE.md"), "small content\n").unwrap();
    }

    // ---- run_for_root ----

    #[test]
    fn run_returns_ok_when_within_budget() {
        let tmp = TempDir::new().unwrap();
        write_budget_yaml(tmp.path());
        fs::write(tmp.path().join("AGENTS.md"), n_words(200)).unwrap();
        write_small_claude(tmp.path());
        let result = run_for_root(tmp.path(), OutputFormat::Text, &[]);
        assert!(result.is_ok(), "within-budget should pass: {result:?}");
    }

    #[test]
    fn run_returns_err_when_agents_md_exceeds_fail() {
        let tmp = TempDir::new().unwrap();
        write_budget_yaml(tmp.path());
        fs::write(tmp.path().join("AGENTS.md"), n_words(600)).unwrap();
        write_small_claude(tmp.path());
        let result = run_for_root(tmp.path(), OutputFormat::Text, &[]);
        assert!(result.is_err(), "fail-budget exceeded should return Err");
    }

    #[test]
    fn run_returns_ok_when_no_word_budget_section() {
        let tmp = TempDir::new().unwrap();
        // No governance-word-budget: section in repo-config.yml — should skip gracefully
        let result = run_for_root(tmp.path(), OutputFormat::Text, &[]);
        assert!(result.is_ok());
    }

    // Regression for the thread-2 fix: a syntactically broken repo-config.yml
    // must not be reported as "SKIPPED (no governance-word-budget: section)" —
    // that message affirmatively misattributes a parse failure as "unarmed".
    #[test]
    fn run_errs_naming_the_parse_failure_when_repo_config_is_broken_not_skipped() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("repo-config.yml"), "harness: [\n").unwrap();
        let err = run_for_root(tmp.path(), OutputFormat::Text, &[])
            .expect_err("a broken repo-config.yml must fail loudly, not report SKIPPED");
        let msg = err.to_string();
        assert!(
            !msg.contains("SKIPPED"),
            "must not misattribute a parse failure as an unarmed gate: {msg}"
        );
    }

    // ---- format_text ----

    #[test]
    fn format_text_passed_when_no_findings() {
        let s = format_text(&[]);
        assert!(s.contains("PASSED"));
    }

    #[test]
    fn format_text_shows_fail_findings() {
        let finding = Finding {
            path: "AGENTS.md".to_string(),
            size: 600,
            target: 400,
            warn: 500,
            fail: 500,
            severity: Severity::Fail,
            message: "AGENTS.md is too large; apply progressive disclosure — see repo-governance/principles/content/progressive-disclosure.md".to_string(),
        };
        let s = format_text(&[finding]);
        assert!(s.contains("[FAIL]"));
        assert!(s.contains("AGENTS.md"));
    }

    // ---- format_json ----

    #[test]
    fn format_json_passed() {
        let config = BudgetConfig {
            surfaces: vec![],
            resolved_tree: wb::ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 1_200,
                warn: 1_500,
                fail: 1_500,
            },
        };
        let s = format_json(&[], &config).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["schema"], SCHEMA);
        assert_eq!(v["status"], "passed");
        assert_eq!(v["total_findings"], 0);
    }

    #[test]
    fn format_json_failed_contains_finding() {
        let finding = Finding {
            path: "AGENTS.md".to_string(),
            size: 600,
            target: 400,
            warn: 500,
            fail: 500,
            severity: Severity::Fail,
            message: "too large; apply progressive disclosure — see repo-governance/principles/content/progressive-disclosure.md".to_string(),
        };
        let config = BudgetConfig {
            surfaces: vec![],
            resolved_tree: wb::ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 1_200,
                warn: 1_500,
                fail: 1_500,
            },
        };
        let s = format_json(&[finding], &config).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["status"], "failed");
        assert_eq!(v["total_findings"], 1);
        assert_eq!(v["findings"][0]["path"], "AGENTS.md");
        assert_eq!(v["findings"][0]["severity"], "fail");
    }

    // ---- format_markdown ----

    #[test]
    fn format_markdown_passed() {
        let s = format_markdown(&[]);
        assert!(s.contains("## Word Budget Audit"));
        assert!(s.contains("PASSED"));
    }

    #[test]
    fn format_markdown_with_findings() {
        let finding = Finding {
            path: "AGENTS.md".to_string(),
            size: 600,
            target: 400,
            warn: 500,
            fail: 500,
            severity: Severity::Fail,
            message: "too large; apply progressive disclosure — see repo-governance/principles/content/progressive-disclosure.md".to_string(),
        };
        let s = format_markdown(&[finding]);
        assert!(s.contains("FAILED"));
        assert!(s.contains("`AGENTS.md`"));
        assert!(s.contains("fail"));
    }

    // ---- fail message contains progressive disclosure ----

    #[test]
    fn fail_message_in_run_contains_progressive_disclosure() {
        let tmp = TempDir::new().unwrap();
        write_budget_yaml(tmp.path());
        fs::write(tmp.path().join("AGENTS.md"), n_words(600)).unwrap();
        write_small_claude(tmp.path());
        let err = run_for_root(tmp.path(), OutputFormat::Text, &[]).unwrap_err();
        let msg = err.to_string();
        assert!(
            msg.contains("progressive disclosure"),
            "error must mention progressive disclosure: {msg}"
        );
        assert!(
            msg.contains("repo-governance/principles/content/progressive-disclosure.md"),
            "error must include governance path: {msg}"
        );
    }

    // ── governance-word-budget: section in repo-config.yml ───────────

    #[test]
    fn run_reads_word_budget_section_from_repo_config_yml() {
        let tmp = TempDir::new().unwrap();
        let repo_cfg = concat!(
            "harness: []\n",
            "coverage:\n  projects: []\n",
            "specs:\n  ddd-areas: []\n  domain-areas: []\n",
            "governance-word-budget:\n",
            "  surfaces:\n",
            "    - glob: \"AGENTS.md\"\n",
            "      target: 400\n",
            "      warn: 500\n",
            "      fail: 500\n",
            "  resolved_tree:\n",
            "    root: \"CLAUDE.md\"\n",
            "    target: 1200\n",
            "    warn: 1500\n",
            "    fail: 1500\n",
        );
        fs::write(tmp.path().join("repo-config.yml"), repo_cfg).unwrap();
        // AGENTS.md exceeds fail=500 words
        fs::write(tmp.path().join("AGENTS.md"), n_words(600)).unwrap();
        fs::write(tmp.path().join("CLAUDE.md"), "small\n").unwrap();
        let result = run_for_root(tmp.path(), OutputFormat::Text, &[]);
        assert!(
            result.is_err(),
            "should read governance-word-budget: from repo-config.yml and flag oversized AGENTS.md"
        );
    }
}
