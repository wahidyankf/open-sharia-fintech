//! In-memory [`Fs`] double for repo-governance validator unit tests.
//!
//! Deliberately shared (not inlined per-consumer like
//! earlier command-specific doubles) because it is
//! consumed by multiple `application::repo_governance::*` validators.

use std::collections::BTreeMap;
use std::io::{Error, ErrorKind, Result};
use std::path::{Path, PathBuf};
use std::sync::Mutex;

use super::port::{DirEntry, Fs};

/// In-memory filesystem double backed by a flat map of absolute path to
/// UTF-8 content.
///
/// Directories are implicit: any path that is a strict ancestor of a stored
/// file's path is treated as an existing directory. Empty directories (no
/// descendant files) cannot be represented — validators under test must not
/// depend on directory existence alone.
#[derive(Debug, Default)]
pub struct MockFs {
    /// Absolute path to UTF-8 file content. `Mutex`-wrapped (not `RefCell`)
    /// so [`Fs::write_string`] can mutate through a shared `&self` reference
    /// while `MockFs` still satisfies `Fs: Send + Sync` — `RefCell` is never
    /// `Sync`.
    files: Mutex<BTreeMap<PathBuf, String>>,
}

impl Clone for MockFs {
    fn clone(&self) -> Self {
        Self {
            files: Mutex::new(self.files.lock().expect("mock fs lock poisoned").clone()),
        }
    }
}

/// Builds a "not found" `io::Error` for a missing path, matching the error
/// kind real `std::fs` calls return for absent files.
fn not_found(path: &Path) -> Error {
    Error::new(
        ErrorKind::NotFound,
        format!("no such file or directory: {}", path.display()),
    )
}

impl MockFs {
    /// Creates an empty `MockFs` with no files.
    #[must_use]
    pub fn new() -> Self {
        Self::default()
    }

    /// Adds (or overwrites) a file at `path` with `content`, returning `self`
    /// for chaining.
    ///
    /// # Panics
    ///
    /// Panics if the internal lock is poisoned (only possible if an earlier
    /// call already panicked while holding it).
    #[must_use]
    pub fn with_file(self, path: impl Into<PathBuf>, content: impl Into<String>) -> Self {
        self.files
            .lock()
            .expect("mock fs lock poisoned")
            .insert(path.into(), content.into());
        self
    }

    /// Returns `true` when `dir` is a strict ancestor directory of at least
    /// one stored file.
    fn has_descendant(&self, dir: &Path) -> bool {
        self.files
            .lock()
            .expect("mock fs lock poisoned")
            .keys()
            .any(|p| p != dir && p.starts_with(dir))
    }
}

impl Fs for MockFs {
    fn read_to_string(&self, path: &Path) -> Result<String> {
        self.files
            .lock()
            .expect("mock fs lock poisoned")
            .get(path)
            .cloned()
            .ok_or_else(|| not_found(path))
    }

    fn read_lines(&self, path: &Path) -> Result<Vec<Result<String>>> {
        let content = self.read_to_string(path)?;
        Ok(content.lines().map(|l| Ok(l.to_string())).collect())
    }

    fn file_size(&self, path: &Path) -> Result<u64> {
        self.files
            .lock()
            .expect("mock fs lock poisoned")
            .get(path)
            .map(|c| c.len() as u64)
            .ok_or_else(|| not_found(path))
    }

    fn exists(&self, path: &Path) -> bool {
        self.files
            .lock()
            .expect("mock fs lock poisoned")
            .contains_key(path)
            || self.has_descendant(path)
    }

    fn is_dir(&self, path: &Path) -> bool {
        !self
            .files
            .lock()
            .expect("mock fs lock poisoned")
            .contains_key(path)
            && self.has_descendant(path)
    }

    fn read_dir(&self, path: &Path) -> Result<Vec<DirEntry>> {
        if !self.exists(path) {
            return Err(not_found(path));
        }
        let mut seen: BTreeMap<String, bool> = BTreeMap::new();
        for p in self.files.lock().expect("mock fs lock poisoned").keys() {
            let Ok(rel) = p.strip_prefix(path) else {
                continue;
            };
            let mut components = rel.components();
            let Some(first) = components.next() else {
                continue;
            };
            let name = first.as_os_str().to_string_lossy().to_string();
            let is_dir = components.next().is_some();
            let entry = seen.entry(name).or_insert(false);
            *entry = *entry || is_dir;
        }
        Ok(seen
            .into_iter()
            .map(|(name, is_dir)| DirEntry { name, is_dir })
            .collect())
    }

    fn walk_files(&self, root: &Path, skip_dirs: &[&str]) -> Vec<PathBuf> {
        let mut out: Vec<PathBuf> = self
            .files
            .lock()
            .expect("mock fs lock poisoned")
            .keys()
            .filter(|p| p.starts_with(root))
            .filter(|p| {
                p.strip_prefix(root).is_ok_and(|rel| {
                    !rel.components()
                        .any(|c| skip_dirs.contains(&c.as_os_str().to_string_lossy().as_ref()))
                })
            })
            .cloned()
            .collect();
        out.sort();
        out
    }

    fn write_string(&self, path: &Path, content: &str) -> Result<()> {
        self.files
            .lock()
            .expect("mock fs lock poisoned")
            .insert(path.to_path_buf(), content.to_string());
        Ok(())
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn read_to_string_returns_stored_content() {
        let fs = MockFs::new().with_file("/repo/AGENTS.md", "hello");
        assert_eq!(
            fs.read_to_string(Path::new("/repo/AGENTS.md")).unwrap(),
            "hello"
        );
    }

    #[test]
    fn read_to_string_missing_file_is_not_found() {
        let fs = MockFs::new();
        let err = fs.read_to_string(Path::new("/nope")).unwrap_err();
        assert_eq!(err.kind(), ErrorKind::NotFound);
    }

    #[test]
    fn file_size_matches_content_length() {
        let fs = MockFs::new().with_file("/repo/AGENTS.md", "x".repeat(42));
        assert_eq!(fs.file_size(Path::new("/repo/AGENTS.md")).unwrap(), 42);
    }

    #[test]
    fn exists_and_is_dir_distinguish_files_from_directories() {
        let fs = MockFs::new().with_file("/repo/docs/a.md", "a");
        assert!(fs.exists(Path::new("/repo/docs/a.md")));
        assert!(!fs.is_dir(Path::new("/repo/docs/a.md")));
        assert!(fs.exists(Path::new("/repo/docs")));
        assert!(fs.is_dir(Path::new("/repo/docs")));
        assert!(!fs.exists(Path::new("/repo/missing")));
    }

    #[test]
    fn read_lines_splits_content() {
        let fs = MockFs::new().with_file("/repo/a.md", "one\ntwo\n");
        let lines = fs.read_lines(Path::new("/repo/a.md")).unwrap();
        let collected: Vec<String> = lines.into_iter().map(std::result::Result::unwrap).collect();
        assert_eq!(collected, vec!["one".to_string(), "two".to_string()]);
    }

    #[test]
    fn read_dir_lists_shallow_children_only() {
        let fs = MockFs::new()
            .with_file("/repo/README.md", "r")
            .with_file("/repo/docs/a.md", "a")
            .with_file("/repo/docs/nested/b.md", "b");
        let mut entries = fs.read_dir(Path::new("/repo")).unwrap();
        entries.sort_by(|a, b| a.name.cmp(&b.name));
        assert_eq!(entries.len(), 2);
        assert_eq!(entries[0].name, "README.md");
        assert!(!entries[0].is_dir);
        assert_eq!(entries[1].name, "docs");
        assert!(entries[1].is_dir);
    }

    #[test]
    fn write_string_makes_content_readable_and_existent() {
        let fs = MockFs::new();
        fs.write_string(Path::new("/repo/docs/new.md"), "hello")
            .unwrap();
        assert_eq!(
            fs.read_to_string(Path::new("/repo/docs/new.md")).unwrap(),
            "hello"
        );
        assert!(fs.exists(Path::new("/repo/docs")));
        assert!(fs.is_dir(Path::new("/repo/docs")));
    }

    #[test]
    fn write_string_overwrites_existing_content() {
        let fs = MockFs::new().with_file("/repo/a.md", "old");
        fs.write_string(Path::new("/repo/a.md"), "new").unwrap();
        assert_eq!(fs.read_to_string(Path::new("/repo/a.md")).unwrap(), "new");
    }

    #[test]
    fn walk_files_skips_named_directories() {
        let fs = MockFs::new()
            .with_file("/repo/a.md", "a")
            .with_file("/repo/node_modules/b.md", "b")
            .with_file("/repo/docs/c.md", "c");
        let files = fs.walk_files(Path::new("/repo"), &["node_modules"]);
        assert_eq!(files.len(), 2);
        assert!(files.contains(&PathBuf::from("/repo/a.md")));
        assert!(files.contains(&PathBuf::from("/repo/docs/c.md")));
    }
}
