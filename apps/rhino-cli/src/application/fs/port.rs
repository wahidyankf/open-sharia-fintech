//! Port for filesystem I/O used by repository-governance validators.
//!
//! Mirrors the pattern established by `application::git::port::StagedFileProvider`:
//! a trait defines the seam, a real (imperative-shell) adapter lives under
//! `infrastructure::fs`, and a shared in-memory double
//! (`application::fs::mock::MockFs`) lets validators be exercised in-process.

use std::path::{Path, PathBuf};

/// A single shallow directory entry returned by [`Fs::read_dir`].
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DirEntry {
    /// The entry's file or directory name (not the full path).
    pub name: String,
    /// `true` when the entry is itself a directory.
    pub is_dir: bool,
}

/// Port for filesystem access used by repository-governance validators.
///
/// Abstracts file reads, metadata, and directory traversal so validators can
/// be exercised in-process against an in-memory [`crate::application::fs::mock::MockFs`]
/// instead of the real filesystem.
pub trait Fs: Send + Sync {
    /// Reads the full UTF-8 contents of the file at `path`.
    ///
    /// # Errors
    /// Returns an error when the file does not exist, cannot be read, or is
    /// not valid UTF-8.
    fn read_to_string(&self, path: &Path) -> std::io::Result<String>;

    /// Reads the file at `path` line by line, mirroring `BufReader::lines()`:
    /// one `Result` per line, where an individual line that is not valid UTF-8
    /// yields an `Err` for that line only (not the whole read).
    ///
    /// # Errors
    /// Returns an error when the file cannot be opened.
    fn read_lines(&self, path: &Path) -> std::io::Result<Vec<std::io::Result<String>>>;

    /// Returns the size in bytes of the file at `path`.
    ///
    /// # Errors
    /// Returns an error when the file cannot be stat-ed (e.g. it does not exist).
    fn file_size(&self, path: &Path) -> std::io::Result<u64>;

    /// Returns `true` when a filesystem entry (file or directory) exists at `path`.
    fn exists(&self, path: &Path) -> bool;

    /// Returns `true` when `path` exists and is a directory.
    fn is_dir(&self, path: &Path) -> bool;

    /// Lists the direct children of the directory at `path` (shallow, not recursive).
    ///
    /// # Errors
    /// Returns an error when `path` cannot be read as a directory.
    fn read_dir(&self, path: &Path) -> std::io::Result<Vec<DirEntry>>;

    /// Recursively lists every file (not directory) under `root`, skipping any
    /// directory whose name matches one of `skip_dirs`.
    ///
    /// Returns an empty list when `root` does not exist. The result is not
    /// required to be sorted; callers that need a deterministic order sort it
    /// themselves.
    fn walk_files(&self, root: &Path, skip_dirs: &[&str]) -> Vec<PathBuf>;

    /// Writes `content` to the file at `path`, creating any missing parent
    /// directories and overwriting any existing file at `path` in full.
    ///
    /// # Errors
    /// Returns an error when the parent directories cannot be created or the
    /// file cannot be written.
    fn write_string(&self, path: &Path, content: &str) -> std::io::Result<()>;
}
