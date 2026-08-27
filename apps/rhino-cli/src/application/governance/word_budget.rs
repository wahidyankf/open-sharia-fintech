//! Instruction-file word budget gate.
//!
//! Loads per-surface word budgets from the `governance-word-budget:` section of
//! `repo-config.yml`, globs for instruction files, classifies each against a
//! three-tier threshold, and optionally resolves the transitive `@`-import
//! tree to check aggregate size.
//!
//! Word count is the raw whole-file count of Rust Unicode-whitespace-separated
//! tokens (`tech-docs.md` §1.2). Frontmatter, fenced code, Mermaid, tables,
//! and URLs all count; the validator's result is authoritative.

use std::collections::{HashMap, HashSet};
use std::path::{Path, PathBuf};

use anyhow::{Context, Error};
use serde::Deserialize;

use crate::application::fs::port::Fs;

/// Directory names excluded from surface-glob matching. Mirrors the
/// `SKIP_DIRS` convention already used by `governance::readme_index`,
/// `docs::naming`, and `docs::frontmatter` — vendored/generated trees are
/// never first-party governance surfaces, and (unlike those walkers, which
/// use `Fs::walk_files`'s own `skip_dirs` parameter) `glob::glob` has no
/// built-in ignore semantics, so matched paths are filtered post hoc against
/// this list. `node_modules` is the one that matters in practice — the
/// `**/README.md` surface glob otherwise descends into every vendored
/// dependency tree in the workspace, producing findings that are unfixable
/// by construction (a third-party README this repo does not author).
const SKIP_DIRS: &[&str] = &["node_modules", "target", "dist", "build", ".next", ".git"];

/// Returns `true` when any path component of `path` matches a name in
/// [`SKIP_DIRS`] — i.e. the path lives inside a vendored/generated tree that
/// must never be treated as a first-party governance surface.
fn is_in_skipped_dir(path: &Path) -> bool {
    path.components().any(|c| {
        c.as_os_str()
            .to_str()
            .is_some_and(|s| SKIP_DIRS.contains(&s))
    })
}

// ---------------------------------------------------------------------------
// Configuration types
// ---------------------------------------------------------------------------

/// Budget thresholds for a single glob surface.
#[derive(Debug, Clone, Deserialize)]
pub struct Surface {
    /// Glob pattern (relative to repo root) to match instruction files.
    pub glob: String,
    /// Ideal maximum size in words.
    pub target: u64,
    /// Warning threshold: files between target and warn are flagged `Warn`.
    pub warn: u64,
    /// Hard upper bound: files exceeding this fail the gate.
    pub fail: u64,
}

/// Budget thresholds for the fully-resolved transitive `@`-import tree.
#[derive(Debug, Clone, Deserialize)]
pub struct ResolvedTree {
    /// Root file to start import resolution from (relative to repo root).
    pub root: String,
    /// Ideal maximum resolved size in words.
    pub target: u64,
    /// Warning threshold in words.
    pub warn: u64,
    /// Hard upper bound in words.
    pub fail: u64,
}

/// Top-level configuration loaded from the `governance-word-budget:` section
/// of `repo-config.yml` (or a standalone budget YAML file in tests).
///
/// `deny_unknown_fields` enforces FR-1.5: no `exempt`, `allow`, `ignore`,
/// `waiver`, or `override` key — or any other unrecognized key — is admitted
/// by the schema.
#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct BudgetConfig {
    /// Per-surface budget entries.
    pub surfaces: Vec<Surface>,
    /// Resolved-tree budget entry.
    pub resolved_tree: ResolvedTree,
}

// ---------------------------------------------------------------------------
// Domain types
// ---------------------------------------------------------------------------

/// Severity classification for a single size finding.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Severity {
    /// File is within the target budget.
    Ok,
    /// File exceeds the target but stays within the fail limit.
    Warn,
    /// File exceeds the fail limit.
    Fail,
}

/// Human-readable label for a [`Severity`].
pub fn severity_label(sev: &Severity) -> &'static str {
    match sev {
        Severity::Ok => "ok",
        Severity::Warn => "warn",
        Severity::Fail => "fail",
    }
}

/// A single finding produced by [`check_instruction_sizes`] or
/// [`check_resolved_tree`].
#[derive(Debug, Clone)]
pub struct Finding {
    /// Repo-relative path of the file (or `"resolved-tree"` for the tree check).
    pub path: String,
    /// Measured size in words.
    pub size: u64,
    /// Target budget in words.
    pub target: u64,
    /// Warning threshold in words.
    pub warn: u64,
    /// Fail threshold in words.
    pub fail: u64,
    /// Severity classification.
    pub severity: Severity,
    /// Human-readable description.
    pub message: String,
}

// ---------------------------------------------------------------------------
// Progressive disclosure reference
// ---------------------------------------------------------------------------

/// Reference text appended to every `Fail` finding message.
///
/// Both "progressive disclosure" and the full governance path must appear so
/// that lint tests can verify them with simple substring checks.
const PROGRESSIVE_DISCLOSURE_REF: &str =
    "progressive disclosure — see repo-governance/principles/content/progressive-disclosure.md";

// ---------------------------------------------------------------------------
// word_count
// ---------------------------------------------------------------------------

/// Raw whole-file word count: the number of Rust Unicode-whitespace-separated
/// tokens in `contents`.
///
/// Frontmatter, fenced code, Mermaid, tables, and URLs all count; there is no
/// "prose-only" carve-out (`tech-docs.md` §1.2). Byte-safe for non-ASCII
/// content — `split_whitespace` operates on `char` boundaries.
#[must_use]
pub fn word_count(contents: &str) -> u64 {
    contents.split_whitespace().count() as u64
}

// ---------------------------------------------------------------------------
// Config loader
// ---------------------------------------------------------------------------

/// Load and parse a budget config YAML document from `path`.
///
/// # Errors
///
/// Returns an error when the file cannot be read or contains invalid YAML,
/// including an unrecognized top-level key (FR-1.5).
pub fn load_budget_config(fs: &dyn Fs, path: &Path) -> Result<BudgetConfig, Error> {
    let data = fs
        .read_to_string(path)
        .with_context(|| format!("cannot read {}", path.display()))?;
    serde_norway::from_str(&data).with_context(|| format!("failed to parse {}", path.display()))
}

// ---------------------------------------------------------------------------
// Merged config: repo-config.yml `governance-word-budget:` section
// ---------------------------------------------------------------------------

/// Loads the `governance-word-budget:` section of `repo-config.yml`.
///
/// FR-1.15: this no longer merges the harness-registry `instruction:` glob
/// lists — FR-1.3's explicit glob list already supersedes every
/// registry-declared `.md`-extension surface that resolves to an existing
/// file. Returns `Ok(None)` when the section is genuinely absent from a
/// registry that parsed successfully (or the registry is genuinely absent).
///
/// Deliberately `load_optional`, not `load_or_default`: a present-but-broken
/// `repo-config.yml` must surface as `Err` here, not collapse into
/// `RepoConfig::default()`'s empty `harness`/`governance_word_budget: None`,
/// which would make this indistinguishable from "no section declared" and
/// let `governance word-budget validate` print `SKIPPED` and exit 0 over a
/// registry that never parsed.
///
/// # Errors
///
/// Returns an error when `repo-config.yml` exists but cannot be read or
/// parsed.
pub fn merged_budget_config(repo_root: &Path) -> Result<Option<BudgetConfig>, Error> {
    let repo_config = crate::application::repo_config::load_optional(repo_root)?;
    Ok(repo_config.and_then(|config| config.governance_word_budget))
}

/// Returns the `args.exclude` list registered against the `governance-word-budget`
/// gate in `repo-config.yml`'s `gates:` registry, or an empty vector when no such
/// gate is registered (e.g. before Phase 9 arms it, or in a standalone test
/// config that omits `gates:` entirely).
///
/// This is the single source [`check_instruction_sizes`]'s `excludes` parameter
/// should be seeded from at every call site — not only the `gate run`
/// pre-push/CI path, which already sees this list because `fixed_arguments`
/// materializes `args.exclude` into `--exclude` flags before invoking the
/// command. The bare `governance word-budget validate` CLI entry point and the
/// `repo-governance audit --include-category governance-word-budget` path both
/// read `repo-config.yml` directly through this function instead of silently
/// defaulting to no exclusions.
///
/// Deliberately `load_optional`, not `load_or_default` — see
/// [`merged_budget_config`]'s doc comment for why a broken registry must not
/// collapse into an empty exclude list.
///
/// # Errors
///
/// Returns an error when `repo-config.yml` exists but cannot be read or
/// parsed.
pub fn registered_excludes(repo_root: &Path) -> Result<Vec<String>, Error> {
    let repo_config = crate::application::repo_config::load_optional(repo_root)?;
    Ok(repo_config
        .and_then(|config| {
            config
                .gates
                .iter()
                .find(|gate| gate.id == "governance-word-budget")
                .and_then(|gate| gate.args.get("exclude").cloned())
        })
        .unwrap_or_default())
}

// ---------------------------------------------------------------------------
// classify
// ---------------------------------------------------------------------------

/// Classify a word `size` against three-tier budget thresholds.
///
/// The `warn` parameter is used for message generation (see
/// [`surface_message`]) but does not create a separate `Severity` level:
/// both "over target" and "over warn threshold" map to [`Severity::Warn`].
///
/// - [`Severity::Ok`] when `size <= target`
/// - [`Severity::Warn`] when `target < size <= fail`
/// - [`Severity::Fail`] when `size > fail`
pub fn classify(size: u64, target: u64, _warn: u64, fail: u64) -> Severity {
    if size <= target {
        Severity::Ok
    } else if size <= fail {
        Severity::Warn
    } else {
        Severity::Fail
    }
}

// ---------------------------------------------------------------------------
// Message builders
// ---------------------------------------------------------------------------

/// Build a human-readable message for a surface finding.
fn surface_message(
    path: &str,
    size: u64,
    target: u64,
    warn: u64,
    fail: u64,
    severity: &Severity,
) -> String {
    match severity {
        Severity::Ok => format!("{path} is {size} words (within {target}-word target)"),
        Severity::Warn if size <= warn => {
            format!("{path} is {size} words (over {target}-word target)")
        }
        Severity::Warn => {
            format!("{path} is {size} words (over {warn}-word warn threshold)")
        }
        Severity::Fail => format!(
            "{path} is {size} words (over {fail}-word fail limit); apply {PROGRESSIVE_DISCLOSURE_REF}",
        ),
    }
}

/// Build a human-readable message for the resolved-tree finding.
fn resolved_tree_message(size: u64, rt: &ResolvedTree, severity: &Severity) -> String {
    match severity {
        Severity::Ok => format!("resolved tree ({}) is {size} words (ok)", rt.root),
        Severity::Warn if size <= rt.warn => {
            format!(
                "resolved tree ({}) is {size} words (over {}-word target)",
                rt.root, rt.target
            )
        }
        Severity::Warn => {
            format!(
                "resolved tree ({}) is {size} words (over {}-word warn threshold)",
                rt.root, rt.warn
            )
        }
        Severity::Fail => format!(
            "resolved tree ({}) is {size} words (over {}-word fail limit); apply {PROGRESSIVE_DISCLOSURE_REF}",
            rt.root, rt.fail
        ),
    }
}

// ---------------------------------------------------------------------------
// check_instruction_sizes
// ---------------------------------------------------------------------------

/// Check all instruction file surfaces against their budgets.
///
/// **Select-then-classify overlap precedence** (`tech-docs.md` §1.1/§1.3):
/// when a path matches more than one surface, the *last-declared* matching
/// surface wins. Pass 1 glob-matches every surface in `config.surfaces`
/// declaration order and records, per resolved path, the most recently
/// matched surface — a later-declared surface's match naturally overwrites an
/// earlier one for the same path. Pass 2 classifies each `(path,
/// winning_surface)` pair exactly once, using only the winning surface's own
/// `target`/`warn`/`fail`. An earlier-declared surface matching the same path
/// is never classified at all, so it can never contribute a stray finding —
/// this holds regardless of whether the winning surface's own verdict is
/// `Ok`, `Warn`, or `Fail`.
///
/// Returns one [`Finding`] per matched file that is not within budget (`Warn`
/// or `Fail`). Globs that match no files produce no findings. `Ok`-severity
/// files are not included in the result. `excludes` holds repo-relative path
/// **prefixes**, matched with a plain `str::starts_with` — not globs, unlike
/// the identically-named `--exclude` flag on `md links validate`/`md mermaid
/// validate` (`readme_index.rs`'s `matches_any_glob`,
/// `governance_audit.rs`'s `exclude_globs`). `.opencode/skills/` excludes
/// everything under that directory; `.opencode/skills/*` matches nothing
/// (there is no literal path starting with a `*` character). Not a per-file
/// waiver on an in-scope surface (FR-1.5 still forbids that), but a way to
/// keep a broad glob like `**/README.md` from reaching trees the
/// `governance-word-budget:` surfaces list was never meant to cover (e.g.
/// `plans/done/`, a local `.fvm/` cache).
pub fn check_instruction_sizes(
    fs: &dyn Fs,
    repo_root: &Path,
    config: &BudgetConfig,
    excludes: &[String],
) -> Vec<Finding> {
    // Pass 1: select the winning surface per path.
    let mut winners: HashMap<PathBuf, &Surface> = HashMap::new();
    for surface in &config.surfaces {
        let pattern = repo_root.join(&surface.glob);
        let pattern_str = pattern.to_string_lossy().to_string();
        // NOTE: glob pattern matching stays on the real filesystem — the `Fs`
        // seam has no virtual-glob equivalent; only the subsequent content
        // read goes through the injected port.
        let Ok(paths) = glob::glob(&pattern_str) else {
            continue;
        };
        for entry in paths.flatten() {
            // Skip vendored/generated trees (`node_modules` in practice) —
            // see `SKIP_DIRS`. `glob::glob` has no ignore semantics of its
            // own, so this filters matched paths post hoc.
            if is_in_skipped_dir(&entry) {
                continue;
            }
            let rel = entry.strip_prefix(repo_root).unwrap_or(&entry);
            let rel_str = rel.to_string_lossy();
            if excludes
                .iter()
                .any(|prefix| rel_str.starts_with(prefix.as_str()))
            {
                continue;
            }
            // Later-declared surfaces overwrite earlier ones for the same
            // path — declaration-order iteration means this naturally holds
            // the last-declared (winning) surface per path.
            winners.insert(entry, surface);
        }
    }

    // Pass 2: classify each winning path exactly once.
    let mut resolved_paths: Vec<&PathBuf> = winners.keys().collect();
    resolved_paths.sort();

    let mut findings: Vec<Finding> = Vec::new();
    for entry in resolved_paths {
        let surface = winners[entry];
        let contents = fs.read_to_string(entry).unwrap_or_default();
        let size = word_count(&contents);
        let severity = classify(size, surface.target, surface.warn, surface.fail);
        if severity == Severity::Ok {
            continue;
        }
        let rel_path = entry.strip_prefix(repo_root).map_or_else(
            |_| entry.to_string_lossy().to_string(),
            |p| p.to_string_lossy().to_string(),
        );
        let message = surface_message(
            &rel_path,
            size,
            surface.target,
            surface.warn,
            surface.fail,
            &severity,
        );
        findings.push(Finding {
            path: rel_path,
            size,
            target: surface.target,
            warn: surface.warn,
            fail: surface.fail,
            severity,
            message,
        });
    }
    findings
}

// ---------------------------------------------------------------------------
// resolve_tree_size + check_resolved_tree
// ---------------------------------------------------------------------------

/// Compute the total word count of `root` and all transitively imported files.
///
/// Files declare imports via lines starting with `@`; the remainder of the
/// line (after trimming whitespace) is the relative import path.  The
/// recursion depth is capped at 4.  Cycles are detected via a set of
/// canonicalized absolute paths; a cycle returns 0 words for the repeated
/// node.
pub fn resolve_tree_size(fs: &dyn Fs, root: &Path) -> u64 {
    let mut visited: HashSet<PathBuf> = HashSet::new();
    resolve_recursive(fs, root, 0, &mut visited)
}

/// Recursive helper for [`resolve_tree_size`].
///
/// Returns 0 when the `depth` limit is exceeded or the `path` has already
/// been visited (cycle guard).
fn resolve_recursive(
    fs: &dyn Fs,
    path: &Path,
    depth: usize,
    visited: &mut HashSet<PathBuf>,
) -> u64 {
    if depth > 4 {
        return 0;
    }
    // NOTE: `canonicalize` stays on the real filesystem (no virtual-symlink
    // equivalent in the `Fs` seam); it already falls back to the raw path on
    // failure, so a mocked `Fs` still gets a stable cycle-guard key.
    let canonical = path.canonicalize().unwrap_or_else(|_| path.to_path_buf());
    if !visited.insert(canonical) {
        return 0; // cycle guard
    }
    let content = fs.read_to_string(path).unwrap_or_default();
    let size = word_count(&content);
    let parent = path.parent().unwrap_or_else(|| Path::new("."));
    let imported: u64 = content
        .lines()
        .filter(|line| line.starts_with('@'))
        .map(|line| {
            let import_path = line[1..].trim();
            resolve_recursive(fs, &parent.join(import_path), depth + 1, visited)
        })
        .sum();
    size + imported
}

/// Check the resolved import tree of `config.resolved_tree.root` against its
/// budget.
///
/// Returns `None` when the resolved size is within the target.  Returns
/// `Some(Finding)` when the resolved size exceeds the target or fail
/// threshold.
pub fn check_resolved_tree(
    fs: &dyn Fs,
    repo_root: &Path,
    config: &BudgetConfig,
) -> Option<Finding> {
    let root_path = repo_root.join(&config.resolved_tree.root);
    let size = resolve_tree_size(fs, &root_path);
    let rt = &config.resolved_tree;
    let severity = classify(size, rt.target, rt.warn, rt.fail);
    if severity == Severity::Ok {
        return None;
    }
    let message = resolved_tree_message(size, rt, &severity);
    Some(Finding {
        path: "resolved-tree".to_string(),
        size,
        target: rt.target,
        warn: rt.warn,
        fail: rt.fail,
        severity,
        message,
    })
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::infrastructure::fs::real::RealFs;
    use std::fs;
    use tempfile::TempDir;

    /// Builds `n` single-character, single-space-separated "words" — content
    /// whose `split_whitespace().count()` is exactly `n`, used to build
    /// word-count-precise fixtures throughout this module's tests.
    fn n_words(n: usize) -> String {
        vec!["w"; n].join(" ")
    }

    // ---- classify ----

    #[test]
    fn classify_ok_at_target() {
        assert_eq!(classify(24_000, 24_000, 27_000, 30_000), Severity::Ok);
    }

    #[test]
    fn classify_warn_over_target_under_fail() {
        assert_eq!(classify(28_000, 24_000, 27_000, 30_000), Severity::Warn);
    }

    #[test]
    fn classify_fail_over_fail() {
        assert_eq!(classify(31_000, 24_000, 27_000, 30_000), Severity::Fail);
    }

    #[test]
    fn classify_ok_below_target() {
        assert_eq!(classify(1_000, 24_000, 27_000, 30_000), Severity::Ok);
    }

    #[test]
    fn classify_warn_at_warn_boundary() {
        // Exactly at warn is still Warn (not Fail — fail is 30_000)
        assert_eq!(classify(27_000, 24_000, 27_000, 30_000), Severity::Warn);
    }

    #[test]
    fn classify_fail_at_fail_boundary_plus_one() {
        assert_eq!(classify(30_001, 24_000, 27_000, 30_000), Severity::Fail);
    }

    // ---- severity_label ----

    #[test]
    fn severity_label_ok() {
        assert_eq!(severity_label(&Severity::Ok), "ok");
    }

    #[test]
    fn severity_label_warn() {
        assert_eq!(severity_label(&Severity::Warn), "warn");
    }

    #[test]
    fn severity_label_fail() {
        assert_eq!(severity_label(&Severity::Fail), "fail");
    }

    // ---- word_count ----

    #[test]
    fn word_count_counts_whitespace_separated_tokens() {
        assert_eq!(word_count("a b c"), 3);
        assert_eq!(word_count(""), 0);
        assert_eq!(word_count("   "), 0);
        assert_eq!(word_count("one\ntwo\tthree"), 3);
    }

    // ---- load_budget_config ----

    #[test]
    fn load_budget_config_parses_agents_md_surface() {
        let tmp = TempDir::new().unwrap();
        let yaml = r#"
surfaces:
  - glob: "AGENTS.md"
    target: 400
    warn: 500
    fail: 500
resolved_tree:
  root: "CLAUDE.md"
  target: 1200
  warn: 1500
  fail: 1500
"#;
        let path = tmp.path().join("governance-word-budget.yaml");
        fs::write(&path, yaml).unwrap();
        let config = load_budget_config(&RealFs, &path).unwrap();
        assert_eq!(config.surfaces.len(), 1);
        assert_eq!(config.surfaces[0].glob, "AGENTS.md");
        assert_eq!(config.surfaces[0].fail, 500);
    }

    #[test]
    fn load_budget_config_error_on_missing_file() {
        let tmp = TempDir::new().unwrap();
        let path = tmp.path().join("nonexistent.yaml");
        let result = load_budget_config(&RealFs, &path);
        assert!(result.is_err());
    }

    // ---- check_instruction_sizes ----

    fn simple_config(glob: &str, target: u64, warn: u64, fail: u64) -> BudgetConfig {
        BudgetConfig {
            surfaces: vec![Surface {
                glob: glob.to_string(),
                target,
                warn,
                fail,
            }],
            resolved_tree: ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 1_200,
                warn: 1_500,
                fail: 1_500,
            },
        }
    }

    #[test]
    fn check_finds_fail_for_large_agents_md() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("AGENTS.md"), n_words(600)).unwrap();
        let config = simple_config("AGENTS.md", 400, 500, 500);
        let findings = check_instruction_sizes(&RealFs, tmp.path(), &config, &[]);
        assert_eq!(findings.len(), 1);
        assert_eq!(findings[0].severity, Severity::Fail);
        assert_eq!(findings[0].path, "AGENTS.md");
    }

    #[test]
    fn check_no_finding_for_absent_glob() {
        let tmp = TempDir::new().unwrap();
        let config = simple_config(".github/copilot-instructions.md", 400, 500, 500);
        let findings = check_instruction_sizes(&RealFs, tmp.path(), &config, &[]);
        assert!(findings.is_empty());
    }

    #[test]
    fn check_no_finding_when_within_target() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("AGENTS.md"), n_words(200)).unwrap();
        let config = simple_config("AGENTS.md", 400, 500, 500);
        let findings = check_instruction_sizes(&RealFs, tmp.path(), &config, &[]);
        assert!(findings.is_empty(), "ok-severity files produce no finding");
    }

    #[test]
    fn check_finds_warn_for_medium_size() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("AGENTS.md"), n_words(450)).unwrap();
        let config = simple_config("AGENTS.md", 400, 500, 500);
        let findings = check_instruction_sizes(&RealFs, tmp.path(), &config, &[]);
        assert_eq!(findings.len(), 1);
        assert_eq!(findings[0].severity, Severity::Warn);
    }

    #[test]
    fn fail_message_contains_progressive_disclosure() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("AGENTS.md"), n_words(600)).unwrap();
        let config = simple_config("AGENTS.md", 400, 500, 500);
        let findings = check_instruction_sizes(&RealFs, tmp.path(), &config, &[]);
        assert_eq!(findings.len(), 1);
        let msg = &findings[0].message;
        assert!(
            msg.contains("progressive disclosure"),
            "message must contain 'progressive disclosure': {msg}"
        );
        assert!(
            msg.contains("repo-governance/principles/content/progressive-disclosure.md"),
            "message must contain governance path: {msg}"
        );
    }

    // ---- resolve_tree_size ----

    #[test]
    fn resolve_tree_sums_file_and_imports() {
        let tmp = TempDir::new().unwrap();
        let agents_words = 200usize;
        fs::write(tmp.path().join("AGENTS.md"), n_words(agents_words)).unwrap();
        let claude_content = "@AGENTS.md\n";
        let claude_words = word_count(claude_content);
        fs::write(tmp.path().join("CLAUDE.md"), claude_content).unwrap();
        let total = resolve_tree_size(&RealFs, &tmp.path().join("CLAUDE.md"));
        assert_eq!(total, claude_words + agents_words as u64);
    }

    #[test]
    fn resolve_tree_missing_import_counts_zero() {
        let tmp = TempDir::new().unwrap();
        let content = "@NONEXISTENT.md\nsome text";
        let content_words = word_count(content);
        fs::write(tmp.path().join("CLAUDE.md"), content).unwrap();
        let total = resolve_tree_size(&RealFs, &tmp.path().join("CLAUDE.md"));
        // Only CLAUDE.md words — nonexistent import contributes 0
        assert_eq!(total, content_words);
    }

    #[test]
    fn resolve_tree_handles_cycle() {
        let tmp = TempDir::new().unwrap();
        // A.md imports B.md, B.md imports A.md
        let a_content = "@B.md\naaa";
        let b_content = "@A.md\nbbb";
        fs::write(tmp.path().join("A.md"), a_content).unwrap();
        fs::write(tmp.path().join("B.md"), b_content).unwrap();
        // Should not infinite-loop; result should be finite
        let total = resolve_tree_size(&RealFs, &tmp.path().join("A.md"));
        assert!(total > 0, "should count at least A.md and B.md words");
        // A + B counted once each (cycle guard stops re-entry)
        assert_eq!(total, word_count(a_content) + word_count(b_content));
    }

    // ---- check_resolved_tree ----

    #[test]
    fn check_resolved_tree_returns_fail_when_large() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("AGENTS.md"), n_words(30_000)).unwrap();
        let claude_content = format!("@AGENTS.md\n{}", n_words(9_000));
        fs::write(tmp.path().join("CLAUDE.md"), &claude_content).unwrap();
        let config = BudgetConfig {
            surfaces: vec![],
            resolved_tree: ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 30_000,
                warn: 34_000,
                fail: 38_000,
            },
        };
        let finding = check_resolved_tree(&RealFs, tmp.path(), &config);
        assert!(finding.is_some());
        let f = finding.unwrap();
        assert_eq!(f.path, "resolved-tree");
        assert_eq!(f.severity, Severity::Fail);
        assert!(f.message.contains("progressive disclosure"));
        assert!(
            f.message
                .contains("repo-governance/principles/content/progressive-disclosure.md")
        );
    }

    #[test]
    fn check_resolved_tree_returns_none_when_within_budget() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("CLAUDE.md"), "small content").unwrap();
        let config = BudgetConfig {
            surfaces: vec![],
            resolved_tree: ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 30_000,
                warn: 34_000,
                fail: 38_000,
            },
        };
        let finding = check_resolved_tree(&RealFs, tmp.path(), &config);
        assert!(finding.is_none());
    }

    // ---- merged_budget_config ----

    #[test]
    fn merged_budget_config_none_when_no_sources() {
        let tmp = TempDir::new().unwrap();
        assert!(merged_budget_config(tmp.path()).unwrap().is_none());
    }

    #[test]
    fn merged_budget_config_errs_on_a_broken_registry_instead_of_reporting_none() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("repo-config.yml"), "harness: [\n").unwrap();
        let error = merged_budget_config(tmp.path())
            .expect_err("an unparseable repo-config.yml must not be reported as \"no section\"");
        assert!(!error.to_string().is_empty());
    }

    #[test]
    fn registered_excludes_errs_on_a_broken_registry_instead_of_reporting_empty() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("repo-config.yml"), "harness: [\n").unwrap();
        let error = registered_excludes(tmp.path())
            .expect_err("an unparseable repo-config.yml must not be reported as \"no excludes\"");
        assert!(!error.to_string().is_empty());
    }

    #[test]
    fn merged_budget_config_reads_yaml_section_from_repo_config() {
        let tmp = TempDir::new().unwrap();
        let repo_cfg = concat!(
            "harness: []\n",
            "coverage:\n  projects: []\n",
            "specs:\n  ddd-areas: []\n  domain-areas: []\n",
            "governance-word-budget:\n",
            "  surfaces:\n",
            "    - glob: \"AGENTS.md\"\n",
            "      target: 400\n",
            "      warn: 500\n",
            "      fail: 500\n",
            "  resolved_tree:\n",
            "    root: \"CLAUDE.md\"\n",
            "    target: 1200\n",
            "    warn: 1500\n",
            "    fail: 1500\n",
        );
        fs::write(tmp.path().join("repo-config.yml"), repo_cfg).unwrap();
        let config = merged_budget_config(tmp.path()).unwrap().unwrap();
        assert_eq!(config.surfaces.len(), 1);
        assert_eq!(config.surfaces[0].glob, "AGENTS.md");
        assert_eq!(config.resolved_tree.root, "CLAUDE.md");
    }

    // -----------------------------------------------------------------------
    // Phase 1a (TDD RED) — plans/done/2026-08-15__optimize-governance-md
    //
    // Tests below cover every FR-1/FR-2 Gherkin scenario in `prd.md`, plus the
    // new select-then-classify overlap logic from `tech-docs.md` §1.1/§1.3.
    // -----------------------------------------------------------------------

    // ---- FR-1: word_count() itself ----

    #[test]
    fn scenario_file_within_target_passes_silently() {
        let content = n_words(650);
        assert_eq!(
            classify(word_count(&content), 650, 750, 750),
            Severity::Ok,
            "FR-1.2: 650 words must classify Ok against a 650-word target"
        );
    }

    #[test]
    fn scenario_file_between_target_and_fail_warns_without_blocking() {
        let content = n_words(750);
        assert_eq!(
            classify(word_count(&content), 650, 750, 750),
            Severity::Warn,
            "FR-1.2: 750 words must classify Warn (between the 650-word target and the \
             750-word fail ceiling)"
        );
    }

    #[test]
    fn scenario_file_over_the_ceiling_fails_the_gate() {
        let content = n_words(14_720);
        assert_eq!(word_count(&content), 14_720);
        assert_eq!(
            classify(word_count(&content), 650, 750, 750),
            Severity::Fail,
            "FR-1.2: 14720 words must classify Fail over the 750-word ceiling"
        );
    }

    #[test]
    fn scenario_non_prose_content_counts_toward_the_budget() {
        // 200 prose words + a fenced "mermaid" block: 598 body words plus the
        // two fence-marker tokens ("```mermaid" and "```", each one
        // whitespace-delimited token) sum to exactly 800, matching the
        // "Non-prose content counts toward the budget" scenario.
        let content = format!("{}\n\n```mermaid\n{}\n```\n", n_words(200), n_words(598));
        assert_eq!(
            word_count(&content),
            800,
            "FR-1.1: fenced Mermaid block content must count toward the budget, not be excluded"
        );
    }

    // ---- FR-1: check_instruction_sizes with word-shaped fixtures ----

    #[test]
    fn scenario_every_covered_surface_is_scanned() {
        let tmp = TempDir::new().unwrap();
        let cases: &[(&str, &str)] = &[
            (
                "repo-governance/**/*.md",
                "repo-governance/principles/example.md",
            ),
            (".claude/**/*.md", ".claude/agents/example.md"),
            (".claude/**/*.md", ".claude/skills/example/SKILL.md"),
            (".opencode/**/*.md", ".opencode/agents/example.md"),
            (".cursor/**/*.md", ".cursor/agents/example.md"),
            (".amazonq/**/*.md", ".amazonq/rules/example.md"),
            ("AGENTS.md", "AGENTS.md"),
            ("CLAUDE.md", "CLAUDE.md"),
        ];
        let mut surfaces: Vec<Surface> = Vec::new();
        let mut seen_globs: HashSet<&str> = HashSet::new();
        for (glob, path) in cases {
            let full = tmp.path().join(path);
            fs::create_dir_all(full.parent().unwrap()).unwrap();
            fs::write(&full, n_words(900)).unwrap();
            if seen_globs.insert(glob) {
                surfaces.push(Surface {
                    glob: (*glob).to_string(),
                    target: 650,
                    warn: 750,
                    fail: 750,
                });
            }
        }
        let config = BudgetConfig {
            surfaces,
            resolved_tree: ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 1_200,
                warn: 1_500,
                fail: 1_500,
            },
        };
        let findings = check_instruction_sizes(&RealFs, tmp.path(), &config, &[]);
        for (_, path) in cases {
            let f = findings
                .iter()
                .find(|f| f.path == *path)
                .unwrap_or_else(|| panic!("FR-1.3: no finding for covered surface {path}"));
            assert_eq!(f.severity, Severity::Fail, "{path} must be a Fail finding");
            assert_eq!(
                f.size, 900,
                "FR-1.1: the finding for {path} must report the word count (900), not bytes"
            );
        }
    }

    #[test]
    fn scenario_out_of_scope_file_is_never_scanned() {
        let tmp = TempDir::new().unwrap();
        fs::create_dir_all(tmp.path().join("apps/ayokoding-www/content")).unwrap();
        fs::write(
            tmp.path().join("apps/ayokoding-www/content/lesson.md"),
            n_words(5_000),
        )
        .unwrap();
        // A covered-surface file is also planted, so the assertion below
        // distinguishes "the config has no surfaces" from "the gate correctly
        // ignored the out-of-scope path."
        fs::create_dir_all(tmp.path().join("repo-governance/principles")).unwrap();
        fs::write(
            tmp.path().join("repo-governance/principles/example.md"),
            n_words(900),
        )
        .unwrap();
        let config = BudgetConfig {
            surfaces: vec![Surface {
                glob: "repo-governance/**/*.md".to_string(),
                target: 650,
                warn: 750,
                fail: 750,
            }],
            resolved_tree: ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 1_200,
                warn: 1_500,
                fail: 1_500,
            },
        };
        let findings = check_instruction_sizes(&RealFs, tmp.path(), &config, &[]);
        assert!(
            findings.iter().all(|f| !f.path.contains("ayokoding-www")),
            "FR-1.3: apps/ is not a covered surface and must never produce a finding: {findings:?}"
        );
        assert_eq!(
            findings.len(),
            1,
            "the in-scope repo-governance file must still be scanned: {findings:?}"
        );
        assert_eq!(
            findings[0].size, 900,
            "FR-1.1: report the word count (900), not the byte count"
        );
    }

    #[test]
    fn scenario_generated_mirror_file_is_still_subject_to_the_word_budget() {
        let tmp = TempDir::new().unwrap();
        fs::create_dir_all(tmp.path().join(".opencode/agents")).unwrap();
        fs::write(
            tmp.path().join(".opencode/agents/plan-checker.md"),
            n_words(900),
        )
        .unwrap();
        let config = BudgetConfig {
            surfaces: vec![Surface {
                glob: ".opencode/**/*.md".to_string(),
                target: 650,
                warn: 750,
                fail: 750,
            }],
            resolved_tree: ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 1_200,
                warn: 1_500,
                fail: 1_500,
            },
        };
        let findings = check_instruction_sizes(&RealFs, tmp.path(), &config, &[]);
        let f = findings
            .iter()
            .find(|f| f.path == ".opencode/agents/plan-checker.md")
            .expect(
                "FR-1.4/FR-3.17: a generated mirror file must still be gated by the word budget",
            );
        assert_eq!(f.severity, Severity::Fail);
        assert_eq!(f.size, 900, "FR-1.1: report word count, not byte count");
    }

    // ---- FR-1.5: config schema rejects an exemption key ----

    #[test]
    fn scenario_config_schema_rejects_an_exemption_key() {
        let tmp = TempDir::new().unwrap();
        let yaml = concat!(
            "surfaces:\n",
            "  - glob: \"AGENTS.md\"\n",
            "    target: 400\n",
            "    warn: 500\n",
            "    fail: 500\n",
            "resolved_tree:\n",
            "  root: \"CLAUDE.md\"\n",
            "  target: 1200\n",
            "  warn: 1500\n",
            "  fail: 1500\n",
            "exempt:\n",
            "  - \"AGENTS.md\"\n",
        );
        let path = tmp.path().join("governance-word-budget.yaml");
        fs::write(&path, yaml).unwrap();
        let result = load_budget_config(&RealFs, &path);
        assert!(
            result.is_err(),
            "FR-1.5: the config schema must reject an unrecognized 'exempt' key, not silently \
             ignore it"
        );
    }

    // ---- FR-2: old command / config block / gate id are gone ----
    // (proxy checks against the live repo-config.yml — full CLI-dispatch and
    // gate-registry-list assertions belong to cli.rs/gate tests, out of this
    // module's scope; these confirm the config-level half of FR-2.1-FR-2.3.)

    fn read_live_repo_config() -> String {
        let repo_root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        fs::read_to_string(repo_root.join("repo-config.yml"))
            .expect("repo-config.yml must exist at the repo root")
    }

    #[test]
    fn scenario_old_config_block_is_gone() {
        let cfg = read_live_repo_config();
        assert!(
            !cfg.contains("\ninstruction-size:\n"),
            "FR-2.2: repo-config.yml must no longer declare an instruction-size: block"
        );
        assert!(
            cfg.contains("governance-word-budget:"),
            "FR-1.6: repo-config.yml must declare a governance-word-budget: block"
        );
    }

    #[test]
    fn scenario_old_gate_id_is_replaced() {
        let cfg = read_live_repo_config();
        assert!(
            !cfg.contains("id: instruction-size"),
            "FR-2.3: the instruction-size gate id must be removed from the gates: registry"
        );
        assert!(
            cfg.contains("id: governance-word-budget"),
            "FR-2.3: the governance-word-budget gate id must be registered in gates: \
             (armed at Phase 9, superseding the removed instruction-size entry)"
        );
    }

    #[test]
    fn scenario_old_command_is_gone() {
        let cfg = read_live_repo_config();
        assert!(
            !cfg.contains("command: harness instruction-size validate"),
            "FR-2.1: no gate may still invoke the removed 'harness instruction-size validate' \
             command"
        );
    }

    // ---- FR-2.6/FR-2.7: resolved tree measured in words ----

    #[test]
    fn scenario_resolved_tree_is_measured_in_words() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("AGENTS.md"), n_words(490)).unwrap();
        // CLAUDE.md's own word count (480) includes the "@AGENTS.md" import
        // directive line itself (one whitespace-delimited token) — FR-1.1 is a
        // raw whole-file count, no exclusions.
        let claude_content = format!("@AGENTS.md\n{}", n_words(479));
        fs::write(tmp.path().join("CLAUDE.md"), &claude_content).unwrap();
        let total = resolve_tree_size(&RealFs, &tmp.path().join("CLAUDE.md"));
        assert_eq!(
            total, 970,
            "FR-2.6: resolved-tree size must be measured in words (480 + 490 = 970), not bytes"
        );
    }

    #[test]
    fn scenario_an_oversized_resolved_tree_fails() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("CLAUDE.md"), n_words(1_600)).unwrap();
        let config = BudgetConfig {
            surfaces: vec![],
            resolved_tree: ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 1_200,
                warn: 1_500,
                fail: 1_500,
            },
        };
        let finding = check_resolved_tree(&RealFs, tmp.path(), &config)
            .expect("a 1600-word tree must exceed the 1500-word fail ceiling");
        assert_eq!(finding.severity, Severity::Fail);
        assert_eq!(
            finding.size, 1_600,
            "FR-2.7: the resolved-tree finding must report the word count (1600), not bytes"
        );
    }

    #[test]
    fn scenario_import_cycles_terminate_and_count_words_once() {
        let tmp = TempDir::new().unwrap();
        // A.md imports B.md, B.md imports A.md — the cycle guard must stop
        // re-entry so each file's words are counted exactly once.
        let a_content = format!("@B.md\n{}", n_words(5));
        let b_content = format!("@A.md\n{}", n_words(7));
        fs::write(tmp.path().join("A.md"), &a_content).unwrap();
        fs::write(tmp.path().join("B.md"), &b_content).unwrap();
        let total = resolve_tree_size(&RealFs, &tmp.path().join("A.md"));
        // A.md = 1 ("@B.md") + 5 = 6 words; B.md = 1 ("@A.md") + 7 = 8 words.
        assert_eq!(
            total, 14,
            "FR-2.6: cyclic imports must terminate and count each file's words exactly once"
        );
    }

    // ---- FR-2.5: no inbound link to the renamed convention is left broken ----

    #[test]
    fn scenario_no_inbound_link_to_the_renamed_convention_is_left_broken() {
        let repo_root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        let mut offenders: Vec<String> = Vec::new();
        for dir in ["repo-governance", ".claude", "docs"] {
            let root = repo_root.join(dir);
            if !root.exists() {
                continue;
            }
            for entry in walkdir::WalkDir::new(&root)
                .into_iter()
                .filter_map(std::result::Result::ok)
            {
                if !entry.file_type().is_file() {
                    continue;
                }
                let path = entry.path();
                if path.extension().and_then(|e| e.to_str()) != Some("md") {
                    continue;
                }
                if let Ok(content) = fs::read_to_string(path)
                    && content.contains("instruction-file-size-budget.md")
                {
                    offenders.push(path.display().to_string());
                }
            }
        }
        if let Ok(agents_md) = fs::read_to_string(repo_root.join("AGENTS.md"))
            && agents_md.contains("instruction-file-size-budget.md")
        {
            offenders.push("AGENTS.md".to_string());
        }
        assert!(
            offenders.is_empty(),
            "FR-2.5: every inbound link to the renamed convention doc must be rewritten in the \
             same commit; still referenced by: {offenders:?}"
        );
    }

    // -----------------------------------------------------------------------
    // Overlap-precedence: select-then-classify (tech-docs.md §1.1/§1.3)
    // -----------------------------------------------------------------------

    /// Declaration-order invariant for `repo-config.yml`'s
    /// `governance-word-budget.surfaces` list: `check_instruction_sizes`'s
    /// select-then-classify pass has last-declared-wins semantics with no
    /// mechanical glob-specificity comparison (`tech-docs.md` §1.1/§1.3), so
    /// a more-specific surface glob MUST be declared after any more-general
    /// surface glob it overlaps with, or it silently loses the overlap and
    /// every file matching it is misclassified under the general surface's
    /// (wrong) budget instead. `**/README.md` is the only surface today that
    /// overlaps others (`repo-governance/**/*.md`, `.claude/**/*.md`, etc.
    /// all match README.md files too) — see the comment on that entry in
    /// `repo-config.yml`. This test enforces the invariant mechanically so a
    /// future reorder or a new general glob inserted after `**/README.md`
    /// fails loud here rather than silently misclassifying every README.
    #[test]
    fn surfaces_declares_readme_glob_last() {
        let repo_root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        let config = merged_budget_config(&repo_root)
            .expect("repo-config.yml must load")
            .expect("repo-config.yml must declare a governance-word-budget: section");
        let last = config
            .surfaces
            .last()
            .expect("governance-word-budget.surfaces must be non-empty");
        assert_eq!(
            last.glob, "**/README.md",
            "the `**/README.md` surface must be declared last in \
             repo-config.yml's governance-word-budget.surfaces list — it is the only surface \
             glob that overlaps others, and last-declared wins the select-then-classify pass \
             (see check_instruction_sizes doc comment); a reorder here silently misclassifies \
             every README.md under a general surface's budget instead of the more-specific one"
        );
    }

    #[test]
    fn check_instruction_sizes_selects_winning_surface_before_classifying_warn_case() {
        let tmp = TempDir::new().unwrap();
        // 1000 words: over the general surface's 750-word fail ceiling, but only
        // Warn against the more-specific README surface's 1000-word fail ceiling.
        fs::write(tmp.path().join("README.md"), n_words(1_000)).unwrap();
        let config = BudgetConfig {
            surfaces: vec![
                Surface {
                    glob: "*.md".to_string(),
                    target: 650,
                    warn: 750,
                    fail: 750,
                },
                Surface {
                    glob: "README.md".to_string(),
                    target: 900,
                    warn: 1_000,
                    fail: 1_000,
                },
            ],
            resolved_tree: ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 1_200,
                warn: 1_500,
                fail: 1_500,
            },
        };
        let findings = check_instruction_sizes(&RealFs, tmp.path(), &config, &[]);
        assert_eq!(
            findings.len(),
            1,
            "select-then-classify: exactly one finding must survive for an overlapping path, \
             not one per matching surface: {findings:?}"
        );
        let f = &findings[0];
        assert_eq!(f.severity, Severity::Warn);
        assert_eq!(f.target, 900);
        assert_eq!(f.warn, 1_000);
        assert_eq!(f.fail, 1_000);
    }

    #[test]
    fn check_instruction_sizes_selects_winning_surface_before_classifying_ok_case() {
        let tmp = TempDir::new().unwrap();
        // 900 words: over the general surface's 750-word fail ceiling, but Ok
        // against the more-specific README surface's own 900-word target — the
        // winning surface's Ok verdict must suppress the general surface's Fail
        // candidate entirely, not merely outrank it.
        fs::write(tmp.path().join("README.md"), n_words(900)).unwrap();
        let config = BudgetConfig {
            surfaces: vec![
                Surface {
                    glob: "*.md".to_string(),
                    target: 650,
                    warn: 750,
                    fail: 750,
                },
                Surface {
                    glob: "README.md".to_string(),
                    target: 900,
                    warn: 1_000,
                    fail: 1_000,
                },
            ],
            resolved_tree: ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 1_200,
                warn: 1_500,
                fail: 1_500,
            },
        };
        let findings = check_instruction_sizes(&RealFs, tmp.path(), &config, &[]);
        assert!(
            findings.is_empty(),
            "select-then-classify: the winning (more specific) surface's own Ok verdict must \
             suppress the earlier, less-specific surface's Fail candidate entirely: {findings:?}"
        );
    }

    // -----------------------------------------------------------------------
    // `node_modules` exclusion — regression test for the `**/README.md`
    // surface glob descending into vendored dependency trees.
    // -----------------------------------------------------------------------

    #[test]
    fn check_instruction_sizes_skips_node_modules() {
        let tmp = TempDir::new().unwrap();
        // A vendored README that would fail the budget if scanned — this
        // finding is unfixable by construction (a third-party dependency's
        // README, not authored by this repo).
        fs::create_dir_all(tmp.path().join("node_modules/some-pkg")).unwrap();
        fs::write(
            tmp.path().join("node_modules/some-pkg/README.md"),
            n_words(1_000),
        )
        .unwrap();
        // A first-party README at the same depth, over budget too, so the
        // test would fail loud if the exclusion swallowed more than
        // `node_modules`.
        fs::write(tmp.path().join("README.md"), n_words(1_000)).unwrap();
        let config = BudgetConfig {
            surfaces: vec![Surface {
                glob: "**/README.md".to_string(),
                target: 400,
                warn: 900,
                fail: 900,
            }],
            resolved_tree: ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 1_200,
                warn: 1_500,
                fail: 1_500,
            },
        };
        let findings = check_instruction_sizes(&RealFs, tmp.path(), &config, &[]);
        assert!(
            findings.iter().all(|f| !f.path.contains("node_modules")),
            "no finding path may contain node_modules: {findings:?}"
        );
        assert_eq!(
            findings.len(),
            1,
            "the first-party README.md at repo root must still be reported: {findings:?}"
        );
        assert_eq!(findings[0].path, "README.md");
    }

    // -----------------------------------------------------------------------
    // `excludes` — path-prefix exemption for the gate/command layer, not the
    // config schema (FR-1.5 still forbids an exempt/allow/ignore key there).
    // -----------------------------------------------------------------------

    #[test]
    fn check_instruction_sizes_excludes_matching_prefixes() {
        let tmp = TempDir::new().unwrap();
        fs::create_dir_all(tmp.path().join("plans/done/some-plan")).unwrap();
        fs::write(
            tmp.path().join("plans/done/some-plan/README.md"),
            n_words(1_000),
        )
        .unwrap();
        fs::write(tmp.path().join("README.md"), n_words(1_000)).unwrap();
        let config = BudgetConfig {
            surfaces: vec![Surface {
                glob: "**/README.md".to_string(),
                target: 400,
                warn: 900,
                fail: 900,
            }],
            resolved_tree: ResolvedTree {
                root: "CLAUDE.md".to_string(),
                target: 1_200,
                warn: 1_500,
                fail: 1_500,
            },
        };
        let excludes = vec!["plans/".to_string()];
        let findings = check_instruction_sizes(&RealFs, tmp.path(), &config, &excludes);
        assert!(
            findings.iter().all(|f| !f.path.starts_with("plans/")),
            "no finding path may start with an excluded prefix: {findings:?}"
        );
        assert_eq!(
            findings.len(),
            1,
            "the first-party README.md at repo root must still be reported: {findings:?}"
        );
        assert_eq!(findings[0].path, "README.md");
    }
}
