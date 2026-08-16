//! `repo-governance audit` — runs all governance audit categories.
//!
//! Port of `apps/rhino-cli/cmd/governance_audit.go`.

use std::fmt::Write as _;

use anyhow::{Error, anyhow};
use clap::Args;

use crate::domain::cliout::OutputFormat;
use crate::infrastructure::fs::real::RealFs;
use crate::internal::git;
use crate::internal::repo_governance::audit_orchestrator::{
    AuditEnvelope, AuditOptions, run_audit,
};

/// CLI arguments for `repo-governance audit`.
#[derive(Args, Debug)]
pub struct AuditArgs {
    /// Category to skip (repeatable).
    #[arg(long = "skip")]
    pub skip: Vec<String>,
    /// Category to include (repeatable); when set, only listed categories run.
    #[arg(long = "include-category")]
    pub include_category: Vec<String>,
    /// Exclude paths matching this glob pattern (repeatable).
    #[arg(long = "exclude")]
    pub exclude: Vec<String>,
}

/// Run the `repo-governance audit` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, the audit fails, or
/// any governance findings are reported.
pub fn run(args: &AuditArgs, output_format: OutputFormat) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    let mut opts = AuditOptions {
        repo_root,
        skip: args.skip.clone(),
        include_only: args.include_category.clone(),
        exclude_globs: args.exclude.clone(),
        ..Default::default()
    };
    #[allow(clippy::collapsible_if)]
    if let Ok(v) = std::env::var("RHINO_AUDIT_NOW") {
        if !v.is_empty() {
            opts.now = Some(v);
        }
    }
    let env = run_audit(&RealFs, &opts)?;

    match output_format {
        OutputFormat::Text => print!("{}", format_text(&env)),
        OutputFormat::Json => println!("{}", format_json(&env)?),
        OutputFormat::Markdown => print!("{}", format_markdown(&env)),
    }

    if env.result.total_findings > 0 {
        return Err(anyhow!(
            "{} governance finding(s) reported across {} categor(ies)",
            env.result.total_findings,
            env.result.categories.len()
        ));
    }
    Ok(())
}

/// Format the audit result as human-readable text.
fn format_text(env: &AuditEnvelope) -> String {
    let mut sb = String::new();
    if env.result.total_findings == 0 {
        let _ = writeln!(
            sb,
            "GOVERNANCE AUDIT PASSED: 0 findings across {} categories (git_sha={}, ran_at={})",
            env.result.categories.len(),
            env.result.git_sha,
            env.result.ran_at
        );
    } else {
        let _ = writeln!(
            sb,
            "GOVERNANCE AUDIT FAILED: {} finding(s) across {} categories (git_sha={}, ran_at={})",
            env.result.total_findings,
            env.result.categories.len(),
            env.result.git_sha,
            env.result.ran_at
        );
    }
    for c in &env.result.categories {
        let state = if c.passed { "PASS" } else { "FAIL" };
        let _ = writeln!(
            sb,
            "  [{}] {:<32} {} finding(s)",
            state,
            c.name,
            c.findings.len()
        );
        for f in &c.findings {
            let line = if f.line > 0 {
                format!("{}:{}", f.file, f.line)
            } else {
                f.file.clone()
            };
            let _ = writeln!(sb, "         {}  {}", line, f.message);
        }
    }
    if !env.result.skipped_false_positives.is_empty() {
        let _ = writeln!(
            sb,
            "  {} skipped false-positive(s)",
            env.result.skipped_false_positives.len()
        );
    }
    sb
}

/// Serialize the audit result as a JSON string.
///
/// # Errors
///
/// Returns an error if JSON serialization fails.
fn format_json(env: &AuditEnvelope) -> std::result::Result<String, Error> {
    Ok(serde_json::to_string_pretty(env)?)
}

/// Format the audit result as a Markdown summary table.
fn format_markdown(env: &AuditEnvelope) -> String {
    let mut sb = String::new();
    sb.push_str("## Governance Audit\n\n");
    if env.result.total_findings == 0 {
        let _ = writeln!(
            sb,
            "**PASSED**: 0 findings across {} categories (git_sha=`{}`, ran_at=`{}`)\n",
            env.result.categories.len(),
            env.result.git_sha,
            env.result.ran_at
        );
    } else {
        let _ = writeln!(
            sb,
            "**FAILED**: {} finding(s) across {} categories (git_sha=`{}`, ran_at=`{}`)\n",
            env.result.total_findings,
            env.result.categories.len(),
            env.result.git_sha,
            env.result.ran_at
        );
    }
    sb.push_str("| Category | Status | Findings |\n");
    sb.push_str("|----------|--------|---------:|\n");
    for c in &env.result.categories {
        let state = if c.passed { "PASS" } else { "FAIL" };
        let _ = writeln!(sb, "| {} | {} | {} |", c.name, state, c.findings.len());
    }
    if !env.result.skipped_false_positives.is_empty() {
        let _ = writeln!(
            sb,
            "\n_{} skipped false-positive(s)._",
            env.result.skipped_false_positives.len()
        );
    }
    sb
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::internal::repo_governance::audit_orchestrator::{
        AuditCategoryResult, AuditFinding, AuditResult,
    };
    use std::collections::BTreeMap;

    fn sample_passing() -> AuditEnvelope {
        AuditEnvelope {
            schema: "rhino-cli/repo-governance-audit/v1".into(),
            status: "ok".into(),
            result: AuditResult {
                git_sha: "abcd123".into(),
                ran_at: "2026-05-23T00:00:00Z".into(),
                total_findings: 0,
                by_severity: BTreeMap::new(),
                by_category: BTreeMap::new(),
                categories: vec![AuditCategoryResult {
                    name: "governance-word-budget".into(),
                    command: "governance word-budget validate".into(),
                    passed: true,
                    findings: vec![],
                }],
                skipped_false_positives: vec![],
            },
        }
    }

    fn sample_failing() -> AuditEnvelope {
        let mut env = sample_passing();
        env.status = "failed".into();
        env.result.total_findings = 1;
        env.result.categories[0].passed = false;
        env.result.categories[0].findings.push(AuditFinding {
            key: "governance-word-budget|AGENTS.md|abcd1234".into(),
            severity: "high".into(),
            criticality: "HIGH".into(),
            file: "AGENTS.md".into(),
            line: 0,
            message: "AGENTS.md exceeds the word-budget fail threshold".into(),
        });
        env
    }

    #[test]
    fn text_passing() {
        let s = format_text(&sample_passing());
        assert!(s.contains("PASSED"));
        assert!(s.contains("[PASS]"));
        assert!(s.contains("governance-word-budget"));
    }

    #[test]
    fn text_failing() {
        let s = format_text(&sample_failing());
        assert!(s.contains("FAILED"));
        assert!(s.contains("[FAIL]"));
        assert!(s.contains("AGENTS.md exceeds"));
    }

    #[test]
    fn json_passes() {
        let s = format_json(&sample_passing()).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["status"], "ok");
        assert_eq!(v["schema"], "rhino-cli/repo-governance-audit/v1");
    }

    #[test]
    fn markdown_passing() {
        let s = format_markdown(&sample_passing());
        assert!(s.contains("## Governance Audit"));
        assert!(s.contains("PASSED"));
        assert!(s.contains("| governance-word-budget | PASS"));
    }

    #[test]
    fn markdown_failing_with_skipped() {
        let mut env = sample_failing();
        env.result.skipped_false_positives.push(AuditFinding {
            key: "x".into(),
            severity: "high".into(),
            criticality: "HIGH".into(),
            file: String::new(),
            line: 0,
            message: String::new(),
        });
        let s = format_markdown(&env);
        assert!(s.contains("FAILED"));
        assert!(s.contains("1 skipped false-positive"));
    }
}
