//! Git common-directory locator — IO adapter for
//! `git rev-parse --path-format=absolute --git-common-dir`.
//!
//! Distinct from [`crate::infrastructure::git::root::find_root`], which
//! resolves the **worktree** root (`--show-toplevel`, worktree-specific — a
//! linked worktree resolves to its own path). The common dir instead
//! resolves to the **main** repository's `.git` regardless of which
//! worktree the command runs from: every linked worktree of the same repo
//! shares one common dir. This is exactly the property the cargo
//! target-share cache needs — every worktree of `ose-public` must resolve
//! to the same `ose-public` cache segment
//! (`application::doctor::target_share::repo_name`).

use std::path::PathBuf;
use std::process::Command;

use anyhow::{Context, Error, anyhow};

/// Returns the absolute path to the git common directory from an optional working directory.
///
/// Executes `git rev-parse --path-format=absolute --git-common-dir` from
/// `cwd` when provided, or from the current working directory when `None`.
/// From a linked worktree this returns the **main** repository's `.git`
/// directory, not the worktree's own path.
///
/// # Errors
///
/// Returns an error when `git` is not found, the command fails, or the
/// output is empty or not valid UTF-8.
pub fn find_common_dir_from(cwd: Option<&std::path::Path>) -> std::result::Result<PathBuf, Error> {
    let mut cmd = Command::new("git");
    cmd.args(["rev-parse", "--path-format=absolute", "--git-common-dir"]);
    if let Some(dir) = cwd {
        cmd.current_dir(dir);
    }
    let output = cmd
        .output()
        .context("failed to invoke git rev-parse --git-common-dir")?;
    if !output.status.success() {
        return Err(anyhow!(
            "git rev-parse --git-common-dir failed: {}",
            String::from_utf8_lossy(&output.stderr).trim()
        ));
    }
    let path = String::from_utf8(output.stdout)?.trim().to_string();
    if path.is_empty() {
        return Err(anyhow!(
            "git rev-parse --git-common-dir returned empty path"
        ));
    }
    Ok(PathBuf::from(path))
}

/// Returns the absolute path to the git common directory.
///
/// Executes `git rev-parse --path-format=absolute --git-common-dir` from the
/// current working directory.
///
/// # Errors
///
/// Returns an error when `git` is not found, the command fails, or the
/// output is empty or not valid UTF-8.
pub fn find_common_dir() -> std::result::Result<PathBuf, Error> {
    find_common_dir_from(None)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::test_support::CwdLock;

    /// Read-only call against this suite's own real repository — out of
    /// scope for the [Git Fixture Isolation
    /// Convention](../../../../../../repo-governance/development/quality/git-fixture-isolation.md),
    /// which governs fixtures that **create or mutate** throwaway
    /// repositories; nothing is written here.
    #[test]
    fn find_common_dir_returns_git_dir() {
        let _cwd = CwdLock::acquire();
        let common = find_common_dir().expect("git common dir resolvable in test");
        assert!(
            common.ends_with(".git"),
            "expected the common dir to end in .git, got {common:?}"
        );
        assert!(
            common.is_dir(),
            "expected {common:?} to exist as a directory"
        );
    }
}
