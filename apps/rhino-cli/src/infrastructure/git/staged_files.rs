//! Git staged-file provider — implements [`StagedFileProvider`] via `git diff --cached`.

use std::path::Path;
use std::process::Command;

use anyhow::{Error, anyhow};

use crate::application::git::port::StagedFileProvider;

/// Adapter that reads staged files by running `git diff --cached --name-only`.
pub struct GitStagedFileProvider;

impl StagedFileProvider for GitStagedFileProvider {
    fn get_staged(&self, git_root: &Path) -> Result<Vec<String>, Error> {
        let out = Command::new("git")
            .arg("diff")
            .arg("--cached")
            .arg("--name-only")
            .current_dir(git_root)
            .output()?;
        if !out.status.success() {
            return Err(anyhow!("git diff --cached failed"));
        }
        let s = String::from_utf8_lossy(&out.stdout);
        let trimmed = s.trim();
        if trimmed.is_empty() {
            return Ok(Vec::new());
        }
        Ok(trimmed
            .split('\n')
            .map(std::string::ToString::to_string)
            .collect())
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used)]
mod tests {
    use tempfile::tempdir;

    use super::*;
    use crate::test_support::CwdLock;

    #[test]
    fn get_staged_files_empty_no_repo() {
        let _cwd = CwdLock::acquire();
        let dir = tempdir().unwrap();
        let provider = GitStagedFileProvider;
        let r = provider.get_staged(dir.path());
        assert!(r.is_err());
    }
}
