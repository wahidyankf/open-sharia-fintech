//! `env staged-guard validate` — block commits that stage real `.env` files.
//!
//! Ports `scripts/check-no-env-staged.sh`: runs `git diff --cached --name-only
//! --diff-filter=AM`, rejects any path whose basename matches `.env*` except exactly
//! `.env.example`. Emits each offending path and a policy message; exits non-zero on any hit.

use anyhow::{Error, anyhow};
use clap::Args;
use std::path::Path;
use std::process::Command;

use crate::domain::cliout::OutputFormat;
use crate::internal::git;

/// CLI arguments for `env staged-guard validate`.
#[derive(Args, Debug)]
pub struct EnvStagedGuardValidateArgs {}

/// Returns true if `path` (any segment) looks like a real `.env*` file that is NOT
/// `.env.example`.
///
/// The **commit** policy deliberately stays deny-all across every `.env*` variant, even though
/// the read policy narrowed to only restrict `.env.prod`/`.env.stag` — see `tech-docs.md` DD-1
/// (Read policy and commit policy are decoupled).
fn is_offending(path: &str) -> bool {
    let basename = Path::new(path)
        .file_name()
        .and_then(|s| s.to_str())
        .unwrap_or(path);
    basename.starts_with(".env") && basename != ".env.example"
}

/// Run `env staged-guard validate` against the current git index.
///
/// # Errors
///
/// Returns an error if the git root cannot be found or any real `.env` file is staged.
pub fn run(
    _args: &EnvStagedGuardValidateArgs,
    output: OutputFormat,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    let out = Command::new("git")
        .args(["diff", "--cached", "--name-only", "--diff-filter=AM"])
        .current_dir(&repo_root)
        .output()
        .map_err(|e| anyhow!("failed to run git diff --cached: {e}"))?;
    if !out.status.success() {
        return Err(anyhow!("git diff --cached failed"));
    }
    let text = String::from_utf8_lossy(&out.stdout);
    let staged: Vec<&str> = text.lines().filter(|l| !l.is_empty()).collect();
    run_with_staged_files(&staged, output, &mut std::io::stdout())
}

/// Testable entry point — checks the given list of staged file paths.
///
/// # Errors
///
/// Returns an error if any path is a real `.env*` file other than `.env.example`.
pub fn run_with_staged_files(
    staged_files: &[&str],
    _output: OutputFormat,
    w: &mut dyn std::io::Write,
) -> std::result::Result<(), Error> {
    let offending: Vec<&str> = staged_files
        .iter()
        .copied()
        .filter(|p| is_offending(p))
        .collect();

    if offending.is_empty() {
        return Ok(());
    }

    writeln!(
        w,
        "ERROR: refusing to commit real .env* files (policy: guard-env-file-access):"
    )?;
    for path in &offending {
        writeln!(w, "  {path}")?;
    }
    writeln!(w, "Only .env.example may be committed.")?;
    writeln!(w, "Unstage with: git restore --staged <file>")?;

    Err(anyhow!(
        "{} offending .env file(s) staged (policy: guard-env-file-access)",
        offending.len()
    ))
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn is_offending_detects_dot_env() {
        assert!(is_offending(".env"));
        assert!(is_offending("apps/my-app/.env"));
        assert!(is_offending(".env.local"));
        assert!(is_offending(".env.production"));
        assert!(is_offending("nested/path/.env.secret"));
    }

    #[test]
    fn is_offending_detects_new_tier_names() {
        assert!(is_offending(".env.prod"));
        assert!(is_offending(".env.stag"));
        assert!(is_offending(".env.test"));
        assert!(is_offending("apps/x/.env.local"));
    }

    #[test]
    fn is_offending_allows_dot_env_example() {
        assert!(!is_offending(".env.example"));
        assert!(!is_offending("apps/my-app/.env.example"));
    }

    #[test]
    fn is_offending_allows_non_env_files() {
        assert!(!is_offending("src/main.rs"));
        assert!(!is_offending("README.md"));
        assert!(!is_offending("env-config.yaml"));
    }

    // ---- P1-1b-RED7 / GREEN7: env staged-guard validate ----

    #[test]
    fn staged_env_file_is_rejected() {
        let mut out = Vec::new();
        let result = run_with_staged_files(&[".env"], OutputFormat::Text, &mut out);
        let output = String::from_utf8(out).unwrap();
        assert!(
            result.is_err(),
            "staging .env must be rejected (policy: guard-env-file-access); got: {output}"
        );
    }

    #[test]
    fn staged_env_file_output_names_the_file() {
        let mut out = Vec::new();
        let _ = run_with_staged_files(&["apps/my-app/.env"], OutputFormat::Text, &mut out);
        let output = String::from_utf8(out).unwrap();
        assert!(
            output.contains(".env"),
            "output must name the offending file; got: {output}"
        );
    }

    #[test]
    fn staged_env_local_is_rejected() {
        let mut out = Vec::new();
        let result = run_with_staged_files(&[".env.local"], OutputFormat::Text, &mut out);
        assert!(result.is_err(), "staging .env.local must be rejected");
    }

    #[test]
    fn staged_env_prod_is_rejected() {
        let mut out = Vec::new();
        let result = run_with_staged_files(&[".env.prod"], OutputFormat::Text, &mut out);
        assert!(result.is_err(), "staging .env.prod must be rejected");
    }

    #[test]
    fn staged_env_example_is_allowed() {
        let mut out = Vec::new();
        let result = run_with_staged_files(&[".env.example"], OutputFormat::Text, &mut out);
        assert!(result.is_ok(), "staging .env.example must be allowed");
    }

    #[test]
    fn empty_staged_set_is_allowed() {
        let mut out = Vec::new();
        let result = run_with_staged_files(&[], OutputFormat::Text, &mut out);
        assert!(result.is_ok(), "no staged files must be allowed");
    }

    #[test]
    fn policy_message_contains_guard_env_file_access() {
        let mut out = Vec::new();
        let _ = run_with_staged_files(&[".env"], OutputFormat::Text, &mut out);
        let output = String::from_utf8(out).unwrap();
        assert!(
            output.contains("guard-env-file-access"),
            "policy string must appear in output; got: {output}"
        );
    }

    #[test]
    fn multiple_env_files_all_named() {
        let mut out = Vec::new();
        let result = run_with_staged_files(
            &[".env", ".env.local", ".env.example", "src/main.rs"],
            OutputFormat::Text,
            &mut out,
        );
        let output = String::from_utf8(out).unwrap();
        assert!(result.is_err(), "must error when any .env file staged");
        assert!(
            output.contains(".env.local"),
            "must name .env.local; got: {output}"
        );
        assert!(
            !output.contains("src/main.rs"),
            "must not name non-env file"
        );
    }
}
