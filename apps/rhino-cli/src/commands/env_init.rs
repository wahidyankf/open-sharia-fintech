//! `env init` — copies `.env.example` files to `.env.local` files under `infra/dev/` and `apps/`.
//!
//! Port of `apps/rhino-cli/cmd/env_init.go`.

use std::fs;
use std::path::{Path, PathBuf};

use anyhow::{Error, anyhow};
use clap::Args;
use walkdir::WalkDir;

use crate::domain::cliout::OutputFormat;
use crate::internal::git;

/// Directories under `repo_root` that are scanned for `.env.example` files.
const SCAN_ROOTS: &[&str] = &["infra/dev", "apps"];

/// The tier `env init` bootstraps: local development, never committed.
const ENV_TIER_DEFAULT: &str = ".env.local";

/// Compute the target env file path for a discovered `.env.example` file,
/// sitting alongside it in the same directory.
fn target_env_path(example_path: &Path) -> Option<PathBuf> {
    Some(example_path.parent()?.join(ENV_TIER_DEFAULT))
}

/// Collect all `.env.example` files found under `SCAN_ROOTS` in `repo_root`.
pub fn collect_examples(repo_root: &Path) -> Vec<PathBuf> {
    let mut results = Vec::new();
    for root in SCAN_ROOTS {
        let scan_dir = repo_root.join(root);
        for entry in WalkDir::new(&scan_dir).into_iter().flatten() {
            if entry.file_type().is_dir() {
                continue;
            }
            if entry.file_name() == ".env.example" {
                results.push(entry.path().to_owned());
            }
        }
    }
    results
}

/// CLI arguments for `env init`.
#[derive(Args, Debug)]
pub struct EnvInitArgs {
    /// Overwrite existing .env files.
    #[arg(long = "force")]
    pub force: bool,
}

/// Run the `env init` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found or if a path operation
/// fails unexpectedly.
///
/// # Panics
///
/// Panics if a `walkdir` entry path has no filename component, which cannot
/// happen for entries produced by `WalkDir`.
pub fn run(args: &EnvInitArgs, _output: OutputFormat) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    let mut created = 0usize;
    let mut skipped = 0usize;
    let mut errs: Vec<String> = Vec::new();

    for path in collect_examples(&repo_root) {
        let env_path = target_env_path(&path).ok_or_else(|| anyhow!("invalid path"))?;
        let rel = env_path.strip_prefix(&repo_root).unwrap_or(&env_path);
        if !args.force && env_path.exists() {
            println!(
                "Skipped: {} (already exists, use --force to overwrite)",
                rel.display()
            );
            skipped += 1;
            continue;
        }
        let data = match fs::read(&path) {
            Ok(d) => d,
            Err(e) => {
                errs.push(format!("failed to read {}: {e}", path.display()));
                continue;
            }
        };
        if let Err(e) = fs::write(&env_path, data) {
            errs.push(format!("failed to write {}: {e}", env_path.display()));
            continue;
        }
        println!(
            "Created: {} (from {})",
            rel.display(),
            path.file_name()
                .expect("walkdir entry always has file_name")
                .to_string_lossy()
        );
        created += 1;
    }

    println!("\nSummary: {created} created, {skipped} skipped");
    for e in &errs {
        eprintln!("Error: {e}");
    }
    Ok(())
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    fn make_fixture(tmp: &TempDir, rel: &str) {
        let p = tmp.path().join(rel);
        fs::create_dir_all(p.parent().unwrap()).unwrap();
        fs::write(&p, b"# fixture").unwrap();
    }

    #[test]
    fn args_default() {
        let _ = EnvInitArgs { force: false };
    }

    #[test]
    fn collect_examples_finds_apps_env_example() {
        let tmp = TempDir::new().unwrap();
        make_fixture(&tmp, "infra/dev/organiclever/.env.example");
        make_fixture(&tmp, "apps/ose-be/.env.example");

        let found: Vec<String> = collect_examples(tmp.path())
            .into_iter()
            .map(|p| {
                p.strip_prefix(tmp.path())
                    .unwrap()
                    .to_string_lossy()
                    .replace('\\', "/")
            })
            .collect();

        assert!(
            found.contains(&"apps/ose-be/.env.example".to_string()),
            "apps/ose-be/.env.example must be discovered; got: {found:?}"
        );
    }

    #[test]
    fn target_env_path_uses_env_local_suffix() {
        let example = Path::new("apps/ose-be/.env.example");
        let target = target_env_path(example).unwrap();
        assert_eq!(target, Path::new("apps/ose-be/.env.local"));
    }

    #[test]
    fn env_init_does_not_create_bare_dot_env() {
        let example = Path::new("apps/ose-be/.env.example");
        let target = target_env_path(example).unwrap();
        assert_ne!(
            target.file_name(),
            Some(std::ffi::OsStr::new(".env")),
            "env init must never produce a bare .env file"
        );
    }
}
