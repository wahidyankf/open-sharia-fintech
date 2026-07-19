//! Git infrastructure adapters — repository root and staged-file provider.

/// Git common-directory locator adapter.
pub mod common_dir;
/// Git repository root locator adapter.
pub mod root;
/// Git staged-file provider adapter.
pub mod staged_files;

use std::path::PathBuf;

use crate::application::git::pre_commit::Deps;
use crate::infrastructure::git::staged_files::GitStagedFileProvider;

/// Creates a [`Deps`] instance wired with the real git staged-file provider
/// and the process's `stdout`/`stderr`.
pub fn make_default_deps(git_root: PathBuf) -> Deps {
    Deps {
        git_root,
        stdout: Box::new(std::io::stdout()),
        stderr: Box::new(std::io::stderr()),
        staged_file_provider: Box::new(GitStagedFileProvider),
    }
}
