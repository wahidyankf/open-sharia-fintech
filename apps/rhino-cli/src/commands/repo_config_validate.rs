//! `repo-config validate` — schema-parity gate for `repo-config.yml`.
//!
//! Strict-deserializes `repo-config.yml` against the canonical
//! [`RepoConfig`](crate::application::repo_config::RepoConfig) schema
//! (`#[serde(deny_unknown_fields)]`), then applies semantic checks:
//! required-non-empty on `harness` and `coverage.projects`, and enum checks on
//! `harness[].tier` and `coverage.projects[].levels`. Every failure names the
//! offending key and its path.
//!
//! Because the parsing struct is byte-identical source across ose-public,
//! ose-primer, and ose-private, each repo validating its own `repo-config.yml`
//! against its own copy of that struct is equivalent to all three files carrying
//! an identical key set (values may differ).

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::repo_config::{self, RepoConfig};
use crate::domain::cliout::OutputFormat;
use crate::internal::git;

/// Accepted values for `harness[].tier`.
const VALID_TIERS: &[&str] = &["source", "generated", "source-config", "native"];

/// Accepted values for `coverage.projects[].levels[]`.
const VALID_LEVELS: &[&str] = &["unit", "integration", "e2e"];

/// CLI arguments for `repo-config validate` (none required).
#[derive(Args, Debug)]
pub struct ValidateArgs {}

/// Run the `repo-config validate` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, `repo-config.yml` cannot be
/// strict-deserialized, or any semantic check fails.
pub fn run(_args: &ValidateArgs, _output: OutputFormat) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    run_at_root(&repo_root, &mut std::io::stdout())
}

/// Run `repo-config validate` from a known `repo_root` (testable entry point).
///
/// # Errors
///
/// Returns an error when `repo-config.yml` fails strict deserialization or any
/// semantic check produces a finding.
pub fn run_at_root(
    repo_root: &std::path::Path,
    w: &mut dyn std::io::Write,
) -> std::result::Result<(), Error> {
    // Strict deserialize (deny_unknown_fields): an unknown or misspelled key here
    // is reported by serde with the offending key named.
    let config = repo_config::load(repo_root).map_err(|e| {
        anyhow!("repo-config validate: repo-config.yml failed strict schema deserialization: {e:#}")
    })?;

    let findings = semantic_findings(&config);

    if findings.is_empty() {
        writeln!(
            w,
            "repo-config validate: repo-config.yml matches the canonical schema (key set + enums OK)"
        )?;
        return Ok(());
    }

    for f in &findings {
        writeln!(w, "{f}")?;
    }
    Err(anyhow!(
        "repo-config validate: {} schema finding(s); fix the key(s) listed above",
        findings.len()
    ))
}

/// Collect semantic findings (required-non-empty + enum checks) for `config`.
///
/// Each finding names the offending key and its path.
fn semantic_findings(config: &RepoConfig) -> Vec<String> {
    let mut findings = Vec::new();

    if config.harness.is_empty() {
        findings.push(
            "harness: required key is missing or empty (expected at least one harness entry)"
                .to_string(),
        );
    }
    if config.coverage.projects.is_empty() {
        findings.push(
            "coverage.projects: required key is missing or empty \
             (expected at least one project entry)"
                .to_string(),
        );
    }

    for (i, entry) in config.harness.iter().enumerate() {
        if !VALID_TIERS.contains(&entry.tier.as_str()) {
            findings.push(format!(
                "harness[{i}].tier: invalid value {:?} (expected one of {})",
                entry.tier,
                VALID_TIERS.join(" | ")
            ));
        }
    }

    for (i, project) in config.coverage.projects.iter().enumerate() {
        for level in &project.levels {
            if !VALID_LEVELS.contains(&level.as_str()) {
                findings.push(format!(
                    "coverage.projects[{i}].levels: invalid value {:?} (expected one of {})",
                    level,
                    VALID_LEVELS.join(" | ")
                ));
            }
        }
    }

    findings
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::TempDir;

    /// A minimal but schema-complete, valid `repo-config.yml`.
    const VALID: &str = concat!(
        "harness:\n",
        "  - { name: claude-code, tier: source, agent-dir: .claude/agents }\n",
        "coverage:\n",
        "  projects:\n",
        "    - name: rhino-cli\n",
        "      levels: [unit, integration]\n",
        "      specs: \"specs/apps/rhino/behavior/rhino-cli/**\"\n",
        "specs:\n  ddd-areas: []\n  domain-areas: []\n",
    );

    fn write_and_run(content: &str) -> (bool, String) {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("repo-config.yml"), content).unwrap();
        let mut buf: Vec<u8> = Vec::new();
        let result = run_at_root(tmp.path(), &mut buf);
        (result.is_ok(), String::from_utf8_lossy(&buf).into_owned())
    }

    #[test]
    fn valid_config_passes() {
        let (ok, out) = write_and_run(VALID);
        assert!(ok, "valid config must pass; got: {out}");
    }

    #[test]
    fn value_only_difference_still_passes() {
        let mutated = VALID.replace("rhino-cli", "some-other-project");
        let (ok, _) = write_and_run(&mutated);
        assert!(ok, "a value-only change (same key set) must still pass");
    }

    #[test]
    fn unknown_key_is_rejected() {
        let with_unknown = format!("{VALID}bogus-unknown-section: true\n");
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("repo-config.yml"), &with_unknown).unwrap();
        let mut buf: Vec<u8> = Vec::new();
        let result = run_at_root(tmp.path(), &mut buf);
        assert!(result.is_err(), "unknown top-level key must be rejected");
        let msg = format!("{:#}", result.unwrap_err());
        assert!(
            msg.contains("bogus-unknown-section"),
            "error must name the offending key; got: {msg}"
        );
    }

    #[test]
    fn empty_coverage_projects_is_rejected() {
        let empty = "harness:\n  - { name: claude-code, tier: source, agent-dir: .claude/agents }\ncoverage:\n  projects: []\nspecs:\n  ddd-areas: []\n  domain-areas: []\n";
        let (ok, out) = write_and_run(empty);
        assert!(!ok, "empty coverage.projects must be rejected");
        assert!(
            out.contains("coverage.projects"),
            "finding must name coverage.projects; got: {out}"
        );
    }

    #[test]
    fn empty_harness_is_rejected() {
        let empty = "harness: []\ncoverage:\n  projects:\n    - name: p\n      levels: [unit]\n      specs: \"x\"\nspecs:\n  ddd-areas: []\n  domain-areas: []\n";
        let (ok, out) = write_and_run(empty);
        assert!(!ok, "empty harness must be rejected");
        assert!(
            out.contains("harness"),
            "finding must name harness; got: {out}"
        );
    }

    #[test]
    fn invalid_tier_enum_is_rejected() {
        let bad = VALID.replace("tier: source", "tier: bogus-tier");
        let (ok, out) = write_and_run(&bad);
        assert!(!ok, "invalid harness tier must be rejected");
        assert!(
            out.contains("tier") && out.contains("bogus-tier"),
            "finding must name the offending tier value; got: {out}"
        );
    }

    #[test]
    fn invalid_level_enum_is_rejected() {
        let bad = VALID.replace("[unit, integration]", "[unit, bogus-level]");
        let (ok, out) = write_and_run(&bad);
        assert!(!ok, "invalid coverage level must be rejected");
        assert!(
            out.contains("levels") && out.contains("bogus-level"),
            "finding must name the offending level value; got: {out}"
        );
    }

    #[test]
    fn args_constructible() {
        let _ = ValidateArgs {};
    }
}
