//! Real filesystem adapter — implements [`Fs`] via `std::fs` and `walkdir`.

use std::io::{BufRead, BufReader, Result};
use std::path::{Path, PathBuf};

use walkdir::WalkDir;

use crate::application::fs::port::{DirEntry, Fs};

/// Adapter that performs filesystem I/O directly against the real filesystem.
pub struct RealFs;

impl Fs for RealFs {
    fn read_to_string(&self, path: &Path) -> Result<String> {
        std::fs::read_to_string(path)
    }

    fn read_lines(&self, path: &Path) -> Result<Vec<Result<String>>> {
        let file = std::fs::File::open(path)?;
        Ok(BufReader::new(file).lines().collect())
    }

    fn file_size(&self, path: &Path) -> Result<u64> {
        Ok(std::fs::metadata(path)?.len())
    }

    fn exists(&self, path: &Path) -> bool {
        path.exists()
    }

    fn is_dir(&self, path: &Path) -> bool {
        path.is_dir()
    }

    fn read_dir(&self, path: &Path) -> Result<Vec<DirEntry>> {
        let entries = std::fs::read_dir(path)?;
        let mut out = Vec::new();
        for entry in entries.flatten() {
            let name = entry.file_name().to_string_lossy().to_string();
            let is_dir = entry.file_type().is_ok_and(|t| t.is_dir());
            out.push(DirEntry { name, is_dir });
        }
        Ok(out)
    }

    fn walk_files(&self, root: &Path, skip_dirs: &[&str]) -> Vec<PathBuf> {
        if !root.exists() {
            return Vec::new();
        }
        WalkDir::new(root)
            .into_iter()
            .filter_entry(|e| {
                if e.file_type().is_dir() {
                    let name = e.file_name().to_string_lossy();
                    !skip_dirs.contains(&name.as_ref())
                } else {
                    true
                }
            })
            .filter_map(std::result::Result::ok)
            .filter(|e| e.file_type().is_file())
            .map(walkdir::DirEntry::into_path)
            .collect()
    }

    fn write_string(&self, path: &Path, content: &str) -> Result<()> {
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent)?;
        }
        std::fs::write(path, content)
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[test]
    fn read_to_string_reads_real_file() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("a.md");
        std::fs::write(&p, "hello").unwrap();
        assert_eq!(RealFs.read_to_string(&p).unwrap(), "hello");
    }

    #[test]
    fn file_size_matches_real_metadata() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("a.md");
        std::fs::write(&p, "x".repeat(10)).unwrap();
        assert_eq!(RealFs.file_size(&p).unwrap(), 10);
    }

    #[test]
    fn exists_and_is_dir_reflect_real_fs() {
        let tmp = TempDir::new().unwrap();
        assert!(RealFs.exists(tmp.path()));
        assert!(RealFs.is_dir(tmp.path()));
        assert!(!RealFs.exists(&tmp.path().join("missing")));
    }

    #[test]
    fn walk_files_skips_named_dirs() {
        let tmp = TempDir::new().unwrap();
        std::fs::create_dir_all(tmp.path().join("node_modules")).unwrap();
        std::fs::write(tmp.path().join("node_modules/x.md"), "x").unwrap();
        std::fs::write(tmp.path().join("a.md"), "a").unwrap();
        let files = RealFs.walk_files(tmp.path(), &["node_modules"]);
        assert_eq!(files.len(), 1);
        assert!(files[0].ends_with("a.md"));
    }

    #[test]
    fn walk_files_missing_root_returns_empty() {
        let tmp = TempDir::new().unwrap();
        let missing = tmp.path().join("does-not-exist");
        assert!(RealFs.walk_files(&missing, &[]).is_empty());
    }

    #[test]
    fn write_string_creates_parent_dirs_and_writes_content() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("sub/dir/README.md");
        RealFs.write_string(&p, "hello").unwrap();
        assert_eq!(std::fs::read_to_string(&p).unwrap(), "hello");
    }

    #[test]
    fn write_string_overwrites_existing_content() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("a.md");
        std::fs::write(&p, "old").unwrap();
        RealFs.write_string(&p, "new").unwrap();
        assert_eq!(std::fs::read_to_string(&p).unwrap(), "new");
    }

    #[test]
    fn read_dir_lists_shallow_entries() {
        let tmp = TempDir::new().unwrap();
        std::fs::create_dir_all(tmp.path().join("sub")).unwrap();
        std::fs::write(tmp.path().join("a.md"), "a").unwrap();
        let mut entries = RealFs.read_dir(tmp.path()).unwrap();
        entries.sort_by(|a, b| a.name.cmp(&b.name));
        assert_eq!(entries.len(), 2);
        assert_eq!(entries[0].name, "a.md");
        assert!(!entries[0].is_dir);
        assert_eq!(entries[1].name, "sub");
        assert!(entries[1].is_dir);
    }
}
