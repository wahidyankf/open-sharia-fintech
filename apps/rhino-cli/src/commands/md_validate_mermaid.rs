//! `md validate-mermaid` — validates Mermaid diagram blocks in markdown files.
//!
//! Port of `apps/rhino-cli/cmd/docs_validate_mermaid.go`.

use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

use anyhow::{Context, Error, anyhow};
use clap::Args;
use walkdir::WalkDir;

use crate::domain::cliout::OutputFormat;
use crate::domain::mermaid::{MermaidBlock, ValidateOptions, extract_blocks, validate_blocks};
use crate::infrastructure::mermaid::reporter::{format_json, format_markdown, format_text};
use crate::internal::git;

/// CLI arguments for `docs validate-mermaid`.
#[derive(Args, Debug)]
pub struct ValidateMermaidArgs {
    /// Only validate staged files (pre-commit use).
    #[arg(long = "staged-only")]
    pub staged_only: bool,
    /// Only validate files changed since upstream (pre-push use).
    #[arg(long = "changed-only")]
    pub changed_only: bool,
    /// Max characters in a node label.
    #[arg(long = "max-label-len", default_value_t = 30)]
    pub max_label_len: usize,
    /// Max nodes at the same rank.
    #[arg(long = "max-width", default_value_t = 4)]
    pub max_width: usize,
    /// Depth threshold for the both-exceeded warning (0 = unlimited).
    #[arg(long = "max-depth", default_value_t = 0)]
    pub max_depth: usize,
    /// Max direct child nodes per subgraph.
    #[arg(long = "max-subgraph-nodes", default_value_t = 6)]
    pub max_subgraph_nodes: usize,
    /// Repository-relative path prefixes to exclude from scanning.
    /// May be specified multiple times.
    #[arg(long = "exclude")]
    pub exclude: Vec<String>,
    /// Optional positional paths to scan.
    pub positional: Vec<String>,
}

/// Directory names skipped during recursive markdown file collection.
///
/// This is the standardized cross-repo noise-skip set shared by the markdown
/// gate validators (mermaid, links, heading-hierarchy).
const SKIP_DIRS: &[&str] = &[
    "node_modules",
    "dist",
    "target",
    ".next",
    "coverage",
    "generated-reports",
    "local-tmp",
    "archived",
    "apps-labs",
    "worktrees",
    ".terraform",
    "generated-contracts",
    ".nx",
    ".git",
];

/// Run the `docs validate-mermaid` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, staged/changed file
/// listing fails, or Mermaid violations are found.
pub fn run(
    args: &ValidateMermaidArgs,
    output_format: OutputFormat,
    verbose: bool,
    quiet: bool,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;

    let md_files: Vec<PathBuf> = if args.staged_only {
        get_staged_files(&repo_root)?
    } else if args.changed_only {
        get_changed_files(&repo_root)?
    } else if !args.positional.is_empty() {
        collect_md_files(&repo_root, &args.positional)
    } else {
        collect_md_repo_wide(&repo_root)
    };
    let md_files = apply_excludes(&repo_root, md_files, &args.exclude);

    let mut all_blocks: Vec<MermaidBlock> = Vec::new();
    let mut file_set: std::collections::HashSet<String> = std::collections::HashSet::new();
    for f in &md_files {
        let Ok(content) = fs::read_to_string(f) else {
            continue;
        };
        let blocks = extract_blocks(&f.to_string_lossy(), &content);
        if !blocks.is_empty() {
            file_set.insert(f.to_string_lossy().to_string());
        }
        all_blocks.extend(blocks);
    }

    let max_depth = if args.max_depth == 0 {
        usize::MAX
    } else {
        args.max_depth
    };
    let opts = ValidateOptions {
        max_label_len: args.max_label_len,
        max_width: args.max_width,
        max_depth,
        max_subgraph_nodes: args.max_subgraph_nodes,
    };
    let mut result = validate_blocks(all_blocks, opts);
    result.files_scanned = file_set.len();

    match output_format {
        OutputFormat::Text => print!("{}", format_text(&result, verbose, quiet)),
        OutputFormat::Json => print!("{}", format_json(&result)?),
        OutputFormat::Markdown => print!("{}", format_markdown(&result)),
    }

    if !result.violations.is_empty() {
        return Err(anyhow!("found {} violation(s)", result.violations.len()));
    }
    Ok(())
}

/// Return paths of staged markdown files via `git diff --cached`.
///
/// # Errors
///
/// Returns an error if the `git` process cannot be spawned.
fn get_staged_files(repo_root: &Path) -> std::result::Result<Vec<PathBuf>, Error> {
    let out = Command::new("git")
        .args([
            "-C",
            &repo_root.to_string_lossy(),
            "diff",
            "--cached",
            "--name-only",
            "--diff-filter=ACMR",
        ])
        .output()
        .context("git diff --cached")?;
    let text = String::from_utf8_lossy(&out.stdout);
    Ok(filter_md_paths(repo_root, text.lines()))
}

/// Return paths of changed markdown files since upstream; falls back to full scan.
///
/// # Errors
///
/// Never returns an error — a git failure causes a fallback to the default scan.
fn get_changed_files(repo_root: &Path) -> std::result::Result<Vec<PathBuf>, Error> {
    let out = Command::new("git")
        .args([
            "-C",
            &repo_root.to_string_lossy(),
            "diff",
            "--name-only",
            "@{u}..HEAD",
        ])
        .output();
    let text = match out {
        Ok(o) => String::from_utf8_lossy(&o.stdout).to_string(),
        Err(_) => return Ok(collect_md_repo_wide(repo_root)),
    };
    let files = filter_md_paths(repo_root, text.lines());
    if files.is_empty() {
        Ok(collect_md_repo_wide(repo_root))
    } else {
        Ok(files)
    }
}

/// Filters `files` to those whose repository-relative path does not start with
/// any of the `exclude` prefixes. An empty `exclude` list is a no-op.
fn apply_excludes(repo_root: &Path, files: Vec<PathBuf>, exclude: &[String]) -> Vec<PathBuf> {
    if exclude.is_empty() {
        return files;
    }
    files
        .into_iter()
        .filter(|f| {
            let rel = f
                .strip_prefix(repo_root)
                .unwrap_or(f)
                .to_string_lossy()
                .replace('\\', "/");
            !exclude.iter().any(|e| {
                let prefix = e.trim_end_matches('/');
                // Component-wise via `path_is_under`, not a string-prefix
                // test: a doubled separator in `prefix` or `rel` (e.g. a
                // trailing `//` typo in `--exclude`) must not silently defeat
                // this check the way it did before the crate's other
                // path-containment predicates were unified onto
                // `path_is_under` (cycle-3 thread 12).
                rel == prefix || crate::application::repo_config::path_is_under(&rel, prefix)
            })
        })
        .collect()
}

/// Filter an iterator of relative paths to those ending in `.md`.
fn filter_md_paths<'a, I: IntoIterator<Item = &'a str>>(
    repo_root: &Path,
    paths: I,
) -> Vec<PathBuf> {
    paths
        .into_iter()
        .filter(|p| !p.is_empty() && p.ends_with(".md"))
        .map(|p| repo_root.join(p))
        .collect()
}

/// Collect markdown files from explicit `paths` (relative or absolute).
fn collect_md_files(repo_root: &Path, paths: &[String]) -> Vec<PathBuf> {
    let mut files = Vec::new();
    for p in paths {
        let abs = if Path::new(p).is_absolute() {
            PathBuf::from(p)
        } else {
            repo_root.join(p)
        };
        files.extend(walk_md_files(&abs));
    }
    files
}

/// Collect markdown files repo-wide, skipping the standardized noise-skip set.
fn collect_md_repo_wide(repo_root: &Path) -> Vec<PathBuf> {
    walk_md_files(repo_root)
}

/// Recursively walk `dir` and return paths of all `.md` files, skipping [`SKIP_DIRS`].
fn walk_md_files(dir: &Path) -> Vec<PathBuf> {
    if !dir.exists() {
        return Vec::new();
    }
    let mut files = Vec::new();
    let walker = WalkDir::new(dir).into_iter().filter_entry(|e| {
        if e.file_type().is_dir() {
            let name = e.file_name().to_string_lossy().to_string();
            !SKIP_DIRS.contains(&name.as_str())
        } else {
            true
        }
    });
    for entry in walker.flatten() {
        if entry.file_type().is_file() && entry.path().extension().is_some_and(|e| e == "md") {
            files.push(entry.path().to_path_buf());
        }
    }
    files
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[test]
    fn filter_md_paths_filters_md_only() {
        let tmp = TempDir::new().unwrap();
        let inputs = ["a.md", "b.txt", "", "docs/c.md"];
        let filtered = filter_md_paths(tmp.path(), inputs.iter().copied());
        assert_eq!(filtered.len(), 2);
    }

    #[test]
    fn walk_md_files_skips_node_modules() {
        let tmp = TempDir::new().unwrap();
        let nm = tmp.path().join("node_modules");
        std::fs::create_dir(&nm).unwrap();
        std::fs::write(nm.join("ignored.md"), "x").unwrap();
        std::fs::write(tmp.path().join("kept.md"), "x").unwrap();
        let files = walk_md_files(tmp.path());
        assert_eq!(files.len(), 1);
        assert!(files[0].to_string_lossy().ends_with("kept.md"));
    }

    #[test]
    fn collect_md_repo_wide_walks_all_dirs() {
        let tmp = TempDir::new().unwrap();
        std::fs::create_dir_all(tmp.path().join("specs/apps")).unwrap();
        std::fs::create_dir_all(tmp.path().join("apps/foo")).unwrap();
        std::fs::create_dir_all(tmp.path().join("node_modules")).unwrap();
        std::fs::write(tmp.path().join("specs/apps/a.md"), "x").unwrap();
        std::fs::write(tmp.path().join("apps/foo/b.md"), "x").unwrap();
        std::fs::write(tmp.path().join("root.md"), "x").unwrap();
        std::fs::write(tmp.path().join("node_modules/skip.md"), "x").unwrap();
        let files = collect_md_repo_wide(tmp.path());
        let names: Vec<String> = files
            .iter()
            .map(|p| p.to_string_lossy().to_string())
            .collect();
        assert_eq!(files.len(), 3, "got: {names:?}");
    }

    #[test]
    fn apply_excludes_filters_by_repo_relative_prefix() {
        let tmp = TempDir::new().unwrap();
        let files = vec![
            tmp.path().join("plans/done/x.md"),
            tmp.path().join("plans/in-progress/y.md"),
            tmp.path().join("docs/z.md"),
        ];
        let kept = apply_excludes(tmp.path(), files, &["plans/done".to_string()]);
        assert_eq!(kept.len(), 2);
        assert!(
            kept.iter()
                .all(|p| !p.to_string_lossy().contains("plans/done"))
        );
    }

    #[test]
    fn apply_excludes_noop_when_empty() {
        let tmp = TempDir::new().unwrap();
        let files = vec![tmp.path().join("docs/z.md")];
        let kept = apply_excludes(tmp.path(), files, &[]);
        assert_eq!(kept.len(), 1);
    }

    #[test]
    fn collect_md_files_handles_absolute_paths() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("foo.md");
        std::fs::write(&p, "x").unwrap();
        let collected = collect_md_files(
            Path::new("/nonexistent"),
            &[p.to_string_lossy().to_string()],
        );
        assert_eq!(collected.len(), 1);
    }
}
