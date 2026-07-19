//! `rhino-cli doctor` target-share + prune-cache GC step.
//!
//! Redirects each Rust crate's `target/` directory to a symlink into a shared,
//! persistent cache keyed by repo name and crate leaf name
//! (`<cache_root>/<repo_name>/<crate_leaf>`), so every git worktree of the
//! same repo shares one physical build directory per crate. See
//! `plans/in-progress/rust-cargo-target-dir-sharing/tech-docs.md` for the
//! full design (DD-1 through DD-8).
//!
//! # Deviation from the design doc's "Implementation shape" reference
//!
//! Several functions here take an explicit `bool`/parameter instead of
//! reading `CI`/`GITHUB_ACTIONS`/`OSE_CARGO_TARGET_CACHE` directly, and the
//! CI/cache-root/PATH decisions are threaded through as plain arguments
//! rather than read ad hoc inside each function. This is a deliberate,
//! forced deviation from the tech-docs' zero-argument sketch signatures:
//! `std::env::set_var`/`remove_var` have been `unsafe fn` since Rust 1.82
//! (a soundness fix, not edition-gated), and this crate forbids `unsafe`
//! code crate-wide (`#![forbid(unsafe_code)]` in `lib.rs`/`main.rs`,
//! `[lints.rust] unsafe_code = "forbid"` in `Cargo.toml`). A unit test
//! cannot deterministically simulate "CI is set" / "the cache root is this
//! tempdir" by mutating the real process environment without `unsafe`, and
//! even if it could, mutating shared process-global environment state would
//! race concurrently-running tests exactly as documented for the cwd in
//! `crate::test_support::CwdLock`. Parameterizing the decision keeps every
//! function here a pure, deterministic, unsafe-free unit under test — the
//! same dependency-injection shape already used by
//! `application::severity::resolve`'s `env_val: &str` parameter. Each
//! parameterized function has a matching `_ambient` (or PATH-probing)
//! sibling that reads the real environment once, at the single call site in
//! `commands/doctor.rs` (a file already excluded from the coverage
//! threshold, matching the existing `dirs_home()`/`binary_in_path()`
//! precedent in `checker.rs`).

use std::collections::HashSet;
use std::path::{Path, PathBuf};

/// Returns `true` when the process should be treated as running under CI.
///
/// `ci_env_set` and `gha_env_set` report whether the `CI` and
/// `GITHUB_ACTIONS` environment variables are set, respectively (either one
/// being set is sufficient). See the module-level "Deviation" note for why
/// this takes explicit booleans instead of reading the environment itself.
pub fn is_ci(ci_env_set: bool, gha_env_set: bool) -> bool {
    ci_env_set || gha_env_set
}

/// Reads the real `CI`/`GITHUB_ACTIONS` environment variables and returns
/// [`is_ci`]'s verdict for the current process.
pub fn is_ci_ambient() -> bool {
    is_ci(
        std::env::var_os("CI").is_some(),
        std::env::var_os("GITHUB_ACTIONS").is_some(),
    )
}

/// Discovers every Rust crate directory under `repo_root/apps/*` and
/// `repo_root/libs/*` that contains a `Cargo.toml`.
///
/// Walks the two top-level directories with `std::fs::read_dir` — no
/// hardcoded crate list — so a newly-added crate is picked up automatically.
/// A top-level directory that does not exist (e.g. a repo with no `libs/`)
/// contributes zero entries rather than an error. The returned list is
/// sorted and deduplicated for deterministic iteration order.
pub fn discover_crates(repo_root: &Path) -> Vec<PathBuf> {
    let mut found = Vec::new();
    for top in ["apps", "libs"] {
        let Ok(entries) = std::fs::read_dir(repo_root.join(top)) else {
            continue;
        };
        for entry in entries.flatten() {
            let path = entry.path();
            if path.is_dir() && path.join("Cargo.toml").is_file() {
                found.push(path);
            }
        }
    }
    found.sort();
    found.dedup();
    found
}

/// Resolves the shared-cache root directory.
///
/// `override_dir` mirrors the `OSE_CARGO_TARGET_CACHE` environment variable
/// (an explicit override wins outright); `home` mirrors `HOME`, used to
/// build the default `<home>/.cache/ose-cargo-target` when no override is
/// given. Returns an empty relative path (`.cache/ose-cargo-target`) when
/// neither is available — a degenerate case the real
/// [`cache_root_ambient`] caller never hits in practice (`HOME` is always
/// set in a real shell), kept total rather than panicking.
pub fn cache_root_from(override_dir: Option<&Path>, home: Option<&Path>) -> PathBuf {
    if let Some(dir) = override_dir {
        return dir.to_path_buf();
    }
    match home {
        Some(h) => h.join(".cache").join("ose-cargo-target"),
        None => PathBuf::from(".cache").join("ose-cargo-target"),
    }
}

/// Reads the real `OSE_CARGO_TARGET_CACHE`/`HOME` environment variables and
/// returns [`cache_root_from`]'s verdict for the current process.
pub fn cache_root_ambient() -> PathBuf {
    let override_dir = std::env::var_os("OSE_CARGO_TARGET_CACHE").map(PathBuf::from);
    let home = std::env::var_os("HOME").map(PathBuf::from);
    cache_root_from(override_dir.as_deref(), home.as_deref())
}

/// Returns the basename of the directory containing the git common dir.
///
/// `common_dir` is the value of
/// `git rev-parse --path-format=absolute --git-common-dir` (typically
/// `<repo-root>/.git`). Using the common dir — rather than
/// `--show-toplevel`, which resolves to the *worktree* path — is what makes
/// every linked worktree of the same repo resolve to the same cache
/// namespace (`crate::infrastructure::git::common_dir::find_common_dir`).
/// Returns an empty string when `common_dir` has no parent (degenerate
/// input; not expected from a real git invocation).
pub fn repo_name(common_dir: &Path) -> String {
    common_dir
        .parent()
        .and_then(Path::file_name)
        .map(|s| s.to_string_lossy().into_owned())
        .unwrap_or_default()
}

/// Returns the shared-cache path a crate's `target/` should be symlinked
/// to: `<cache_root>/<repo_name>/<crate_leaf>`, where `crate_leaf` is
/// `crate_dir`'s final path component (e.g. `rhino-cli`).
pub fn shared_target_path(cache_root: &Path, repo_name: &str, crate_dir: &Path) -> PathBuf {
    let leaf = crate_dir
        .file_name()
        .map(|s| s.to_string_lossy().into_owned())
        .unwrap_or_default();
    cache_root.join(repo_name).join(leaf)
}

/// One crate whose `target/` is not yet the correct shared-cache symlink.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TargetShareStatus {
    /// Absolute path to the crate directory (e.g. `apps/rhino-cli`).
    pub crate_dir: PathBuf,
    /// The shared-cache path this crate's `target/` should be symlinked to.
    pub shared_path: PathBuf,
}

/// Returns `true` when `link` is a symlink whose target equals `expected_target`.
fn is_correct_symlink(link: &Path, expected_target: &Path) -> bool {
    std::fs::read_link(link).is_ok_and(|actual| actual == expected_target)
}

/// Reports every crate under `repo_root` whose `target/` is not yet the
/// correct symlink into the shared cache. Read-only — never mutates the
/// filesystem. Returns an empty list under CI (`ci == true`).
pub fn check_target_shares(
    repo_root: &Path,
    cache_root: &Path,
    repo_name: &str,
    ci: bool,
) -> Vec<TargetShareStatus> {
    if ci {
        return Vec::new();
    }
    let mut result = Vec::new();
    for crate_dir in discover_crates(repo_root) {
        let target = crate_dir.join("target");
        let shared_path = shared_target_path(cache_root, repo_name, &crate_dir);
        if !is_correct_symlink(&target, &shared_path) {
            result.push(TargetShareStatus {
                crate_dir,
                shared_path,
            });
        }
    }
    result
}

/// Outcome of a [`fix_target_shares`] run.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct FixOutcome {
    /// Number of crates whose `target/` was (re)created as a symlink.
    pub created: usize,
    /// Number of crates whose `target/` was already the correct symlink.
    pub already_correct: usize,
    /// Number of crates whose plain `target/` directory was discarded and
    /// replaced with a symlink.
    pub replaced_plain_dir: usize,
    /// `true` when the run was a CI no-op (nothing was touched).
    pub skipped_ci: bool,
}

/// Creates or repairs each discovered crate's `target/` symlink into the
/// shared cache. No-ops entirely under CI (`ci == true`).
pub fn fix_target_shares(
    repo_root: &Path,
    cache_root: &Path,
    repo_name: &str,
    ci: bool,
) -> FixOutcome {
    let mut outcome = FixOutcome::default();
    if ci {
        outcome.skipped_ci = true;
        return outcome;
    }
    for crate_dir in discover_crates(repo_root) {
        let target = crate_dir.join("target");
        let shared_path = shared_target_path(cache_root, repo_name, &crate_dir);
        let _ = std::fs::create_dir_all(&shared_path);
        if is_correct_symlink(&target, &shared_path) {
            outcome.already_correct += 1;
            continue;
        }
        let replaced_plain_dir = match std::fs::symlink_metadata(&target) {
            Ok(meta) if meta.file_type().is_symlink() => {
                // A symlink pointing somewhere else — discard before relinking.
                let _ = std::fs::remove_file(&target);
                false
            }
            Ok(meta) if meta.is_dir() => {
                // A plain, rebuildable directory (stale artifacts) — discard entirely.
                let _ = std::fs::remove_dir_all(&target);
                true
            }
            Ok(_) => {
                let _ = std::fs::remove_file(&target);
                false
            }
            Err(_) => false, // nothing at `target` yet
        };
        if std::os::unix::fs::symlink(&shared_path, &target).is_ok() {
            outcome.created += 1;
            if replaced_plain_dir {
                outcome.replaced_plain_dir += 1;
            }
        }
    }
    outcome
}

/// Returns the shared-cache path currently referenced by every crate's
/// `target/` symlink across every live worktree (plus the main checkout) of
/// the repo rooted at `repo_root`.
///
/// Queries `git worktree list --porcelain` from `repo_root` — this
/// production call intentionally operates on the caller's real repository
/// (or, in tests, an already-isolated throwaway fixture built per the [Git
/// Fixture Isolation
/// Convention](../../../../../../repo-governance/development/quality/git-fixture-isolation.md));
/// it is a read query with an explicit `current_dir`, not a fixture that
/// creates or mutates a repo, so the convention's six-layer isolation
/// applies to the fixture *construction* in tests, not to this call itself
/// (see that convention's "Read-only git commands" scope carve-out). `git
/// worktree list` always reports the main checkout as its first entry, so no
/// separate "plus the main checkout" step is needed.
///
/// Returns `None` when the query itself fails (spawn error or non-zero exit —
/// e.g. `repo_root` is not a git repository). `None` is distinct from
/// `Some(empty set)`: a successful enumeration that finds no referencing
/// symlinks is a genuine empty live set (prune may delete orphans), whereas a
/// *failed* enumeration means we cannot know what is referenced, so the caller
/// must fail closed and delete nothing rather than treat every entry as an
/// orphan.
fn live_referenced_entries(repo_root: &Path) -> Option<HashSet<PathBuf>> {
    let mut live = HashSet::new();
    let Ok(output) = std::process::Command::new("git")
        .args(["worktree", "list", "--porcelain"])
        .current_dir(repo_root)
        .output()
    else {
        return None;
    };
    if !output.status.success() {
        return None;
    }
    let stdout = String::from_utf8_lossy(&output.stdout);
    for worktree in stdout
        .lines()
        .filter_map(|line| line.strip_prefix("worktree "))
        .map(PathBuf::from)
    {
        for crate_dir in discover_crates(&worktree) {
            let target = crate_dir.join("target");
            let Ok(meta) = std::fs::symlink_metadata(&target) else {
                continue;
            };
            if !meta.file_type().is_symlink() {
                continue;
            }
            let Ok(resolved) = std::fs::read_link(&target) else {
                continue;
            };
            let canonical = resolved.canonicalize().unwrap_or(resolved);
            live.insert(canonical);
        }
    }
    Some(live)
}

/// Outcome of a [`prune_orphans`] run.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct PruneOutcome {
    /// Shared-cache entries actually deleted.
    pub deleted: Vec<PathBuf>,
    /// Shared-cache entries preserved because a live checkout references them.
    pub preserved: Vec<PathBuf>,
    /// Under `dry_run`, entries that *would* be deleted (nothing removed).
    pub candidates: Vec<PathBuf>,
    /// `true` when the run was a CI no-op (nothing was inspected or touched).
    pub skipped_ci: bool,
    /// `true` when `git worktree list` could not be enumerated, so the run
    /// failed closed (deleted nothing) rather than risk treating live entries
    /// as orphans.
    pub enumeration_failed: bool,
}

/// Deletes shared-cache entries under `<cache_root>/<repo_name>/*` that no
/// live worktree or checkout of the repo references. Never touches an entry
/// present in [`live_referenced_entries`]'s result.
pub fn prune_orphans(
    repo_root: &Path,
    cache_root: &Path,
    repo_name: &str,
    dry_run: bool,
    ci: bool,
) -> PruneOutcome {
    let mut outcome = PruneOutcome::default();
    if ci {
        outcome.skipped_ci = true;
        return outcome;
    }
    let Some(live) = live_referenced_entries(repo_root) else {
        // Worktree enumeration failed — we cannot know which entries are still
        // referenced, so fail closed and delete nothing rather than treat
        // every entry as an orphan (which would wipe live caches).
        outcome.enumeration_failed = true;
        return outcome;
    };
    let Ok(entries) = std::fs::read_dir(cache_root.join(repo_name)) else {
        return outcome;
    };
    for entry in entries.flatten() {
        let path = entry.path();
        if !path.is_dir() {
            continue;
        }
        let canonical = path.canonicalize().unwrap_or_else(|_| path.clone());
        if live.contains(&canonical) {
            outcome.preserved.push(path);
        } else if dry_run {
            outcome.candidates.push(path);
        } else {
            let _ = std::fs::remove_dir_all(&path);
            outcome.deleted.push(path);
        }
    }
    outcome
}

/// Outcome of a [`sweep_stale`] run.
#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct SweepOutcome {
    /// `true` when the sweep was skipped because `cargo-sweep` is absent
    /// from `PATH` — never an error, per DD-6's graceful-degrade contract.
    pub skipped: bool,
    /// `true` when the sweep was skipped because CI was detected. Mirrors the
    /// CI guard on check/fix/prune (DD-4: the whole prune step, cargo-sweep
    /// branch included, is a no-op under CI so a runner's shared cache is
    /// never mutated).
    pub skipped_ci: bool,
    /// `true` when `cargo-sweep` was actually invoked.
    pub ran: bool,
}

/// Returns `true` when the `cargo-sweep` binary is present on `PATH`.
///
/// Mirrors the `binary_in_path` pattern in `checker.rs` (that helper is
/// private to its own module, so this is a small, deliberate duplicate
/// rather than a cross-module dependency).
pub fn cargo_sweep_present() -> bool {
    let Some(path_var) = std::env::var_os("PATH") else {
        return false;
    };
    std::env::split_paths(&path_var).any(|dir| dir.join("cargo-sweep").is_file())
}

/// The repo-scoped subtree `cargo-sweep` reclaims within —
/// `<cache_root>/<repo_name>`, never the whole shared `cache_root` (which
/// spans every repo's caches). Matches prune's `<cache_root>/<repo_name>`
/// namespace and DD-7 step 5 ("over the surviving entries" of *this* repo), so
/// a sweep launched from one repo never reclaims another repo's artifacts.
fn sweep_scope(cache_root: &Path, repo_name: &str) -> PathBuf {
    cache_root.join(repo_name)
}

/// Runs `cargo-sweep`'s stale-artifact reclamation over this repo's cache
/// namespace (`<cache_root>/<repo_name>`, via [`sweep_scope`]) when the binary
/// is present, degrading gracefully to `Skipped` (never an error) when it is
/// absent. Scoping to the repo's own namespace — rather than the whole
/// `cache_root` — keeps the sweep from touching sibling repos' caches.
/// `cargo_sweep_present` is threaded in explicitly by the caller (see the
/// module-level "Deviation" note) rather than probed here, so this function
/// stays a deterministic, unsafe-free unit under test.
///
/// When `dry_run` is `true` and the binary is present, no subprocess is
/// invoked at all (a conservative preview: this cleanup lever is optional
/// and manual per DD-6, so a dry-run never needs to actually shell out).
pub fn sweep_stale(
    cache_root: &Path,
    repo_name: &str,
    dry_run: bool,
    cargo_sweep_present: bool,
    ci: bool,
) -> SweepOutcome {
    // CI guard FIRST — before the cargo-sweep-present probe — so that even a
    // runner with cargo-sweep installed never shells out and mutates the
    // shared cache (DD-4: the whole prune step is a no-op under CI).
    if ci {
        return SweepOutcome {
            skipped: false,
            skipped_ci: true,
            ran: false,
        };
    }
    if !cargo_sweep_present {
        return SweepOutcome {
            skipped: true,
            skipped_ci: false,
            ran: false,
        };
    }
    if dry_run {
        return SweepOutcome {
            skipped: false,
            skipped_ci: false,
            ran: false,
        };
    }
    let _ = std::process::Command::new("cargo-sweep")
        .args(["--time", "30", "--recursive"])
        .arg(sweep_scope(cache_root, repo_name))
        .output();
    SweepOutcome {
        skipped: false,
        skipped_ci: false,
        ran: true,
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use std::path::Path;

    /// `is_ci` returns `true` when either signal is set, `false` when
    /// neither is.
    ///
    /// Gherkin (underpins) — "the doctor symlink step no-ops under CI":
    ///   Given the environment variable CI is set
    ///   When the developer runs the doctor command with the fix flag
    ///   Then no target symlink is created for any crate
    ///   And the command exits successfully with a message that CI was detected
    #[test]
    fn is_ci_true_when_env_set() {
        assert!(super::is_ci(true, false), "CI set alone must report true");
        assert!(
            super::is_ci(false, true),
            "GITHUB_ACTIONS set alone must report true"
        );
        assert!(super::is_ci(true, true), "both set must report true");
        assert!(!super::is_ci(false, false), "neither set must report false");
    }

    /// `discover_crates` walks `apps/*/Cargo.toml` + `libs/*/Cargo.toml`
    /// (no hardcoded crate list) and returns every crate directory found.
    ///
    /// Gherkin (underpins) — "dynamic discovery covers every crate under
    /// apps and libs":
    ///   Given a repo checkout contains multiple Rust crates under apps and libs outside CI
    ///   When the developer runs the doctor command with the fix flag
    ///   Then every discovered crate's target is a symlink into the shared cache
    ///   And no crate is skipped due to a hardcoded crate list
    #[test]
    fn discover_crates_walks_apps_and_libs() {
        let root = tempfile::tempdir().unwrap();
        for rel in ["apps/a", "apps/b", "libs/c"] {
            let dir = root.path().join(rel);
            std::fs::create_dir_all(&dir).unwrap();
            std::fs::write(dir.join("Cargo.toml"), "[package]\nname = \"x\"\n").unwrap();
        }
        // A non-crate directory (no Cargo.toml) must NOT be discovered.
        std::fs::create_dir_all(root.path().join("apps/not-a-crate")).unwrap();

        let mut found = super::discover_crates(root.path());
        found.sort();
        let mut expected = vec![
            root.path().join("apps/a"),
            root.path().join("apps/b"),
            root.path().join("libs/c"),
        ];
        expected.sort();
        assert_eq!(found, expected);
    }

    /// `cache_root_from` honors an explicit override (mirroring
    /// `OSE_CARGO_TARGET_CACHE`) or falls back to `<home>/.cache/ose-cargo-target`;
    /// `repo_name` returns the basename of the directory containing the git
    /// common dir; the composed shared path is
    /// `<cache_root>/<repo_name>/<crate_leaf>`.
    ///
    /// Gherkin (underpins) — "two worktrees of the same repo share one
    /// physical target":
    ///   Given two worktrees of the same repo each have a crate's target symlinked by the doctor
    ///   When both symlinks are resolved
    ///   Then both point at the same shared-cache directory for that repo and crate
    ///   And a disk usage measurement across the worktrees counts that directory only once
    #[test]
    fn cache_path_uses_common_dir_basename() {
        let cache_override = tempfile::tempdir().unwrap();
        assert_eq!(
            super::cache_root_from(Some(cache_override.path()), None),
            cache_override.path(),
            "an explicit override must win outright"
        );

        let home = tempfile::tempdir().unwrap();
        assert_eq!(
            super::cache_root_from(None, Some(home.path())),
            home.path().join(".cache").join("ose-cargo-target"),
            "with no override, falls back to $HOME/.cache/ose-cargo-target"
        );

        let common_dir = Path::new("/some/path/my-repo/.git");
        assert_eq!(super::repo_name(common_dir), "my-repo");

        let crate_dir = Path::new("/some/path/my-repo/apps/rhino-cli");
        assert_eq!(
            super::shared_target_path(cache_override.path(), "my-repo", crate_dir),
            cache_override.path().join("my-repo").join("rhino-cli")
        );
    }

    /// `check_target_shares` reports a crate whose `target/` is a plain
    /// directory as needing to be shared, without mutating anything; under
    /// CI it reports nothing.
    ///
    /// Gherkin (binds) — "doctor check reports a crate whose target is not
    /// yet shared":
    ///   Given a crate's target is a plain directory not yet symlinked into the shared cache
    ///   When the developer runs the doctor command without the fix flag
    ///   Then the output reports that crate's target as needing to be shared
    ///   And the plain target directory is left unchanged
    #[test]
    fn check_reports_unshared_target() {
        let repo_root = tempfile::tempdir().unwrap();
        let crate_dir = repo_root.path().join("apps/foo");
        std::fs::create_dir_all(&crate_dir).unwrap();
        std::fs::write(crate_dir.join("Cargo.toml"), "[package]\nname = \"x\"\n").unwrap();
        let target_dir = crate_dir.join("target");
        std::fs::create_dir_all(&target_dir).unwrap();
        std::fs::write(target_dir.join("marker.txt"), "stale").unwrap();

        let cache_root = tempfile::tempdir().unwrap();

        let report =
            super::check_target_shares(repo_root.path(), cache_root.path(), "myrepo", false);
        assert_eq!(report.len(), 1, "expected exactly one crate needing share");
        assert_eq!(report[0].crate_dir, crate_dir);
        assert_eq!(
            report[0].shared_path,
            cache_root.path().join("myrepo").join("foo")
        );

        // No mutation: the plain directory and its stale marker file survive.
        assert!(target_dir.is_dir() && !target_dir.is_symlink());
        assert!(target_dir.join("marker.txt").exists());

        let ci_report =
            super::check_target_shares(repo_root.path(), cache_root.path(), "myrepo", true);
        assert!(ci_report.is_empty(), "CI must report nothing");
    }

    /// Builds a synthetic crate directory `<repo_root>/apps/<name>` with a
    /// `Cargo.toml`, returning its path. Does not create a `target/` dir.
    fn make_crate(repo_root: &Path, name: &str) -> std::path::PathBuf {
        let crate_dir = repo_root.join("apps").join(name);
        std::fs::create_dir_all(&crate_dir).unwrap();
        std::fs::write(crate_dir.join("Cargo.toml"), "[package]\nname = \"x\"\n").unwrap();
        crate_dir
    }

    /// `fix_target_shares` turns a crate's absent `target/` into a symlink
    /// resolving into the shared cache, under `OSE_CARGO_TARGET_CACHE`-style
    /// tempdir isolation (never the real `$HOME/.cache/ose-cargo-target`).
    ///
    /// Gherkin (binds) — "doctor --fix symlinks a crate's target into the
    /// shared cache":
    ///   Given a Rust crate with a plain target directory exists in a repo checkout outside CI
    ///   When the developer runs the doctor command with the fix flag
    ///   Then the crate's target becomes a symlink into the shared cargo-target cache
    ///   And the symlink resolves under the repo's own shared-cache namespace
    #[test]
    fn fix_creates_symlink() {
        let repo_root = tempfile::tempdir().unwrap();
        let cache_root = tempfile::tempdir().unwrap();
        let crate_dir = make_crate(repo_root.path(), "foo");

        let outcome =
            super::fix_target_shares(repo_root.path(), cache_root.path(), "myrepo", false);
        assert_eq!(outcome.created, 1);

        let target = crate_dir.join("target");
        let expected_shared = cache_root.path().join("myrepo").join("foo");
        assert!(target.is_symlink(), "target must become a symlink");
        assert_eq!(
            std::fs::read_link(&target).unwrap(),
            expected_shared,
            "the symlink must resolve under the repo's own shared-cache namespace"
        );
    }

    /// A second `fix_target_shares` run on an already-correct symlink must
    /// not recreate or alter it.
    ///
    /// Gherkin (binds) — "the doctor fix step is idempotent":
    ///   Given a crate's target is already the correct symlink into the shared cache
    ///   When the developer runs the doctor command with the fix flag a second time
    ///   Then the command exits successfully without recreating or altering the symlink
    #[test]
    fn fix_is_idempotent() {
        let repo_root = tempfile::tempdir().unwrap();
        let cache_root = tempfile::tempdir().unwrap();
        let crate_dir = make_crate(repo_root.path(), "foo");

        let first = super::fix_target_shares(repo_root.path(), cache_root.path(), "myrepo", false);
        assert_eq!(first.created, 1);

        let target = crate_dir.join("target");
        let link_before = std::fs::read_link(&target).unwrap();

        let second = super::fix_target_shares(repo_root.path(), cache_root.path(), "myrepo", false);
        assert_eq!(
            second.already_correct, 1,
            "second run must recognize the symlink as already correct"
        );
        assert_eq!(second.created, 0, "second run must not recreate anything");

        let link_after = std::fs::read_link(&target).unwrap();
        assert_eq!(
            link_before, link_after,
            "the symlink target must be unchanged"
        );
    }

    /// A pre-existing plain `target/` directory (containing stale build
    /// artifacts) is discarded — not merged — and replaced with the shared
    /// symlink.
    ///
    /// Gherkin (binds) — "doctor --fix replaces an existing plain target
    /// directory with a symlink":
    ///   Given a crate's target is a plain rebuildable directory containing stale artifacts
    ///   When the developer runs the doctor command with the fix flag outside CI
    ///   Then the plain directory is discarded and the target becomes a symlink into the shared cache
    #[test]
    fn fix_replaces_plain_dir() {
        let repo_root = tempfile::tempdir().unwrap();
        let cache_root = tempfile::tempdir().unwrap();
        let crate_dir = make_crate(repo_root.path(), "foo");
        let target = crate_dir.join("target");
        std::fs::create_dir_all(&target).unwrap();
        std::fs::write(target.join("stale.txt"), "stale artifact").unwrap();

        let outcome =
            super::fix_target_shares(repo_root.path(), cache_root.path(), "myrepo", false);
        assert_eq!(outcome.replaced_plain_dir, 1);

        assert!(
            target.is_symlink(),
            "the plain directory must be replaced by a symlink"
        );
        let shared_path = cache_root.path().join("myrepo").join("foo");
        assert!(
            !shared_path.join("stale.txt").exists(),
            "the stale plain-dir content must be discarded, not merged into the shared cache"
        );
    }

    /// Under CI, `fix_target_shares` creates no symlink for any crate and
    /// leaves the filesystem untouched.
    ///
    /// Gherkin (binds) — "the doctor symlink step no-ops under CI":
    ///   Given the environment variable CI is set
    ///   When the developer runs the doctor command with the fix flag
    ///   Then no target symlink is created for any crate
    ///   And the command exits successfully with a message that CI was detected
    #[test]
    fn fix_noops_under_ci() {
        let repo_root = tempfile::tempdir().unwrap();
        let cache_root = tempfile::tempdir().unwrap();
        let crate_dir = make_crate(repo_root.path(), "foo");
        let target = crate_dir.join("target");
        std::fs::create_dir_all(&target).unwrap();

        let outcome = super::fix_target_shares(repo_root.path(), cache_root.path(), "myrepo", true);
        assert!(outcome.skipped_ci, "outcome must report CI was detected");
        assert_eq!(outcome.created, 0);
        assert_eq!(outcome.replaced_plain_dir, 0);
        assert!(
            target.is_dir() && !target.is_symlink(),
            "target must remain the untouched plain directory under CI"
        );
    }

    /// `prune_orphans` deletes a shared-cache entry that no live checkout
    /// references. `repo_root` is a real (fully-isolated) throwaway repo, so
    /// `live_referenced_entries` *succeeds* and returns a genuine empty live
    /// set (the main checkout has no crate symlinking the orphan) — the
    /// deletion is driven by "no referrer", NOT by a failed enumeration (which
    /// now fails closed, see `prune_skips_deletion_when_enumeration_fails`).
    ///
    /// Gherkin (binds) — "prune removes an orphaned shared-cache entry":
    ///   Given the shared cache holds an entry for a crate that no longer exists in the repo outside CI
    ///   When the developer runs the doctor command with the prune flag
    ///   Then the orphaned cache entry is deleted
    ///   And every entry still referenced by a live worktree or checkout is preserved
    #[test]
    fn prune_removes_orphan() {
        let repo = tempfile::tempdir().unwrap();
        build_throwaway_repo(repo.path());
        let cache_root = tempfile::tempdir().unwrap();
        let orphan_dir = cache_root.path().join("myrepo").join("orphan-crate");
        std::fs::create_dir_all(&orphan_dir).unwrap();
        std::fs::write(orphan_dir.join("marker.txt"), "stale").unwrap();

        let outcome = super::prune_orphans(repo.path(), cache_root.path(), "myrepo", false, false);
        assert_eq!(outcome.deleted, vec![orphan_dir.clone()]);
        assert!(!orphan_dir.exists(), "the orphaned entry must be deleted");
    }

    /// Regression guard (cycle-2 MEDIUM): when `git worktree list` cannot be
    /// enumerated (here, `repo_root` has no `.git` at all), `prune_orphans`
    /// fails **closed** — it deletes nothing and flags `enumeration_failed` —
    /// rather than treating every cache entry as an orphan and wiping live
    /// caches. This is the exact scenario the old `prune_removes_orphan`
    /// accidentally relied on; the two now assert opposite, correct behaviors.
    #[test]
    fn prune_skips_deletion_when_enumeration_fails() {
        let non_repo = tempfile::tempdir().unwrap(); // no .git → git worktree list fails
        let cache_root = tempfile::tempdir().unwrap();
        let entry_dir = cache_root.path().join("myrepo").join("some-crate");
        std::fs::create_dir_all(&entry_dir).unwrap();
        std::fs::write(entry_dir.join("marker.txt"), "keep").unwrap();

        let outcome =
            super::prune_orphans(non_repo.path(), cache_root.path(), "myrepo", false, false);
        assert!(
            outcome.enumeration_failed,
            "a failed worktree enumeration must be reported"
        );
        assert!(
            outcome.deleted.is_empty(),
            "nothing may be deleted when enumeration fails (fail closed)"
        );
        assert!(
            entry_dir.exists(),
            "the entry must survive a failed enumeration"
        );
    }

    /// Builds a `git` [`std::process::Command`] targeting `repo_dir` with
    /// full ambient-discovery isolation, per the [Git Fixture Isolation
    /// Convention](../../../../../../repo-governance/development/quality/git-fixture-isolation.md)
    /// (Standards 1-3). `GIT_WORK_TREE` is deliberately NOT set — see that
    /// convention's Standard 2 note on why it must stay absent here.
    fn iso_git(repo_dir: &Path) -> std::process::Command {
        let mut cmd = std::process::Command::new("git");
        cmd.current_dir(repo_dir)
            .env("GIT_DIR", repo_dir.join(".git"))
            .env("GIT_CEILING_DIRECTORIES", repo_dir)
            .env("GIT_CONFIG_GLOBAL", "/dev/null")
            .env("GIT_CONFIG_SYSTEM", "/dev/null");
        cmd
    }

    /// Pre-write escape guard (Standard 4): panics unless `git`, under
    /// [`iso_git`] isolation, resolves its top level to `repo_dir`
    /// (canonicalized).
    fn assert_no_escape(repo_dir: &Path) {
        let out = iso_git(repo_dir)
            .args(["rev-parse", "--show-toplevel"])
            .output()
            .expect("escape-guard: git rev-parse must spawn");
        assert!(
            out.status.success(),
            "escape-guard: git rev-parse --show-toplevel failed in {repo_dir:?}: {}",
            String::from_utf8_lossy(&out.stderr)
        );
        let top = String::from_utf8_lossy(&out.stdout).trim().to_string();
        let want = std::fs::canonicalize(repo_dir).unwrap_or_else(|_| repo_dir.to_path_buf());
        let got = std::fs::canonicalize(&top).unwrap_or_else(|_| Path::new(&top).to_path_buf());
        assert_eq!(
            got, want,
            "escape-guard: fixture git resolves to {got:?}, not the intended tempdir {want:?}"
        );
    }

    /// Builds a throwaway one-commit git repository at `repo_dir`, applying
    /// all six Git Fixture Isolation layers (Standards 1-5; Standard 6 is a
    /// process rule with no code-level expression). No `git worktree add` is
    /// needed: `git worktree list --porcelain` always reports the main
    /// checkout as a live worktree, which is exactly the property
    /// `live_referenced_entries` relies on.
    fn build_throwaway_repo(repo_dir: &Path) {
        let run_checked = |args: &[&str]| {
            if repo_dir.join(".git").is_dir() {
                assert_no_escape(repo_dir); // Standard 4, before every write once .git exists
            }
            let output = iso_git(repo_dir)
                .args(args)
                .output()
                .expect("git command must spawn");
            assert!(
                output.status.success(), // Standard 5
                "git {args:?} in {repo_dir:?} must exit zero, got: {}",
                String::from_utf8_lossy(&output.stderr)
            );
        };
        run_checked(&["init"]);
        run_checked(&["config", "user.email", "fixture@test.local"]);
        run_checked(&["config", "user.name", "Fixture"]);
        std::fs::write(repo_dir.join("README.md"), "throwaway fixture").expect("write README");
        run_checked(&["add", "."]);
        run_checked(&["commit", "-m", "init"]);
    }

    /// `prune_orphans` preserves a shared-cache entry that is the symlink
    /// target of a crate in a live worktree (here, the main checkout of a
    /// throwaway, fully-isolated fixture repo).
    ///
    /// Gherkin (binds) — "prune preserves a cache entry referenced by a live
    /// worktree":
    ///   Given a shared-cache entry is the symlink target of a crate in a live worktree
    ///   When the developer runs the doctor command with the prune flag
    ///   Then that referenced cache entry is left in place
    ///   And only entries with no live referrer are removed
    #[test]
    fn prune_preserves_live_referenced() {
        let repo = tempfile::tempdir().unwrap();
        build_throwaway_repo(repo.path());

        let cache_root = tempfile::tempdir().unwrap();
        let live_dir = cache_root.path().join("myrepo").join("foo");
        std::fs::create_dir_all(&live_dir).unwrap();

        let crate_dir = make_crate(repo.path(), "foo");
        std::os::unix::fs::symlink(&live_dir, crate_dir.join("target")).unwrap();

        let outcome = super::prune_orphans(repo.path(), cache_root.path(), "myrepo", false, false);
        assert_eq!(
            outcome.deleted,
            Vec::<std::path::PathBuf>::new(),
            "a live-referenced entry must never be deleted"
        );
        assert!(live_dir.exists(), "the live-referenced entry must survive");
    }

    /// Under CI, `prune_orphans` deletes nothing, even with an orphaned
    /// entry present.
    ///
    /// Gherkin (binds) — "the prune step no-ops under CI":
    ///   Given the environment variable CI is set
    ///   When the developer runs the doctor command with the prune flag
    ///   Then no cache entry is deleted
    ///   And the command exits successfully with a message that CI was detected
    #[test]
    fn prune_noops_under_ci() {
        let repo_root = tempfile::tempdir().unwrap();
        let cache_root = tempfile::tempdir().unwrap();
        let orphan_dir = cache_root.path().join("myrepo").join("orphan-crate");
        std::fs::create_dir_all(&orphan_dir).unwrap();

        let outcome =
            super::prune_orphans(repo_root.path(), cache_root.path(), "myrepo", false, true);
        assert!(outcome.skipped_ci, "outcome must report CI was detected");
        assert!(
            outcome.deleted.is_empty(),
            "no cache entry may be deleted under CI"
        );
        assert!(
            orphan_dir.exists(),
            "the orphan entry must survive under CI"
        );
    }

    /// `--dry-run` reports the orphaned candidate without deleting it.
    ///
    /// Gherkin (binds) — "prune dry-run previews deletions without removing
    /// anything":
    ///   Given the shared cache holds at least one orphaned entry outside CI
    ///   When the developer runs the doctor command with the prune and dry-run flags
    ///   Then the orphaned entry is reported as a candidate for deletion
    ///   And no cache entry is actually removed
    #[test]
    fn prune_dry_run_reports_without_deleting() {
        let repo = tempfile::tempdir().unwrap();
        build_throwaway_repo(repo.path());
        let cache_root = tempfile::tempdir().unwrap();
        let orphan_dir = cache_root.path().join("myrepo").join("orphan-crate");
        std::fs::create_dir_all(&orphan_dir).unwrap();

        let outcome = super::prune_orphans(repo.path(), cache_root.path(), "myrepo", true, false);
        assert_eq!(
            outcome.candidates,
            vec![orphan_dir.clone()],
            "the orphan must be reported as a deletion candidate"
        );
        assert!(
            outcome.deleted.is_empty(),
            "dry-run must not actually delete anything"
        );
        assert!(orphan_dir.exists(), "the orphan entry must survive dry-run");
    }

    /// `sweep_stale` reports `Skipped` (not an error) when `cargo-sweep` is
    /// not present, rather than failing the command. `cargo_sweep_present`
    /// is threaded in explicitly (never probed via the real `PATH` inside
    /// the test) so the outcome is deterministic regardless of whether the
    /// host machine happens to have `cargo-sweep` installed.
    ///
    /// Gherkin (underpins) — "stale-artifact sweep degrades gracefully when
    /// cargo-sweep is absent":
    ///   Given cargo-sweep is not installed on the developer's PATH
    ///   When the developer runs the doctor command with the prune flag
    ///   Then the sweep step is reported as skipped rather than failing the command
    ///   And the command exits successfully
    #[test]
    fn sweep_skips_when_cargo_sweep_absent() {
        let cache_root = tempfile::tempdir().unwrap();
        let outcome = super::sweep_stale(cache_root.path(), "myrepo", false, false, false);
        assert!(
            outcome.skipped,
            "sweep must report Skipped, not fail, when cargo-sweep is absent"
        );
        assert!(!outcome.ran, "an absent binary must never be invoked");
    }

    /// Regression guard (cycle-2 MEDIUM): the sweep is scoped to this repo's
    /// own cache namespace (`<cache_root>/<repo_name>`), never the whole
    /// shared `cache_root` — so a sweep launched from one repo never reclaims
    /// a sibling repo's artifacts.
    #[test]
    fn sweep_scope_is_repo_namespaced() {
        let cache_root = Path::new("/tmp/ose-cargo-target");
        assert_eq!(
            super::sweep_scope(cache_root, "ose-public"),
            cache_root.join("ose-public"),
            "sweep must target the repo namespace, not the shared root"
        );
        assert_ne!(
            super::sweep_scope(cache_root, "ose-public"),
            cache_root.to_path_buf(),
            "sweep must never target the whole cache_root (all repos)"
        );
    }

    /// Regression guard (cycle-1 HIGH): under CI, `sweep_stale` must be a
    /// no-op EVEN WHEN cargo-sweep is present on the runner's PATH — it must
    /// never shell out `cargo-sweep --time 30 --recursive <cache>` and mutate
    /// the runner's shared cache. The CI guard is checked before the
    /// present-probe, so `cargo_sweep_present = true` must still yield a
    /// non-running, CI-skipped outcome (DD-4: the whole prune step no-ops
    /// under CI).
    #[test]
    fn sweep_is_ci_guarded_even_when_cargo_sweep_present() {
        let cache_root = tempfile::tempdir().unwrap();
        let outcome = super::sweep_stale(cache_root.path(), "myrepo", false, true, true);
        assert!(
            outcome.skipped_ci,
            "under CI the sweep must report skipped_ci"
        );
        assert!(
            !outcome.ran,
            "under CI cargo-sweep must never be invoked, even when present"
        );
        assert!(
            !outcome.skipped,
            "the CI skip is distinct from the cargo-sweep-absent skip"
        );
    }
}
