//! Git repository root locator — IO adapter for `git rev-parse --show-toplevel`.

use std::path::PathBuf;
use std::process::Command;

use anyhow::{Context, Error, anyhow};

/// Returns the absolute path to the Git repository root from an optional working directory.
///
/// Executes `git rev-parse --show-toplevel` from `cwd` when provided, or from the
/// current working directory when `None`. Using `--show-toplevel` makes this
/// worktree-aware: from a linked worktree, it returns the worktree path, not the
/// main repo path.
///
/// # Errors
///
/// Returns an error when `git` is not found, the command fails, or the output
/// is empty or not valid UTF-8.
pub fn find_root_from(cwd: Option<&std::path::Path>) -> std::result::Result<PathBuf, Error> {
    let mut cmd = Command::new("git");
    cmd.args(["rev-parse", "--show-toplevel"]);
    if let Some(dir) = cwd {
        cmd.current_dir(dir);
    }
    let output = cmd.output().context("failed to invoke git rev-parse")?;
    if !output.status.success() {
        return Err(anyhow!(
            "git rev-parse failed: {}",
            String::from_utf8_lossy(&output.stderr).trim()
        ));
    }
    let path = String::from_utf8(output.stdout)?.trim().to_string();
    if path.is_empty() {
        return Err(anyhow!("git rev-parse returned empty path"));
    }
    Ok(PathBuf::from(path))
}

/// Returns the absolute path to the Git repository root.
///
/// Executes `git rev-parse --show-toplevel` from the current working directory.
///
/// # Errors
///
/// Returns an error when `git` is not found, the command fails, or the output
/// is empty or not valid UTF-8.
pub fn find_root() -> std::result::Result<PathBuf, Error> {
    find_root_from(None)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::test_support::CwdLock;
    use std::path::Path;
    use std::process::Command as Cmd;
    use tempfile::TempDir;

    #[test]
    fn find_root_returns_repo_root() {
        let _cwd = CwdLock::acquire();
        let root = find_root().expect("git root resolvable in test");
        assert!(
            root.join("Cargo.toml").exists() || root.join("AGENTS.md").exists(),
            "expected repo root to contain Cargo.toml or AGENTS.md, got {root:?}"
        );
    }

    /// Builds a `git` [`Cmd`] targeting `repo_dir` with full ambient-discovery
    /// isolation, per the [Git Fixture Isolation] convention. This is the
    /// deeper fix for the corruption class this plan addresses: exit-status
    /// checking alone was necessary but NOT sufficient — a fixture `git` call
    /// can still escape into the real repository if git resolves against the
    /// wrong working directory (a process-global CWD race under concurrency).
    /// Setting `GIT_DIR` explicitly makes git use exactly `repo_dir/.git` and
    /// perform ZERO discovery — it ignores the process CWD entirely — so the
    /// command cannot reach any other repository. `GIT_CEILING_DIRECTORIES`
    /// caps any residual upward walk at `repo_dir`, and nulling the global and
    /// system config keeps the developer's real identity from bleeding in (and
    /// the throwaway identity from bleeding out).
    ///
    /// [Git Fixture Isolation]: repo-governance/development/quality/git-fixture-isolation.md
    fn iso_git(repo_dir: &Path) -> Cmd {
        let mut cmd = Cmd::new("git");
        cmd.current_dir(repo_dir)
            .env("GIT_DIR", repo_dir.join(".git"))
            .env("GIT_CEILING_DIRECTORIES", repo_dir)
            .env("GIT_CONFIG_GLOBAL", "/dev/null")
            .env("GIT_CONFIG_SYSTEM", "/dev/null");
        cmd
    }

    /// Pre-write escape-guard. Panics unless git, under [`iso_git`] isolation,
    /// resolves its top level to `repo_dir` (canonicalized). Run this before
    /// EVERY write (once `repo_dir/.git` exists), so a would-be escape — a
    /// missed isolation env on a future write, or any discovery path not
    /// enumerated — fails loud instead of silently corrupting the real
    /// repository. Per the convention's Standard 4, guarding once is not enough.
    fn assert_no_escape(repo_dir: &Path) {
        let out = iso_git(repo_dir)
            .args(["rev-parse", "--show-toplevel"])
            .output()
            .expect("escape-guard: git rev-parse must spawn");
        assert!(
            out.status.success(),
            "escape-guard: `git rev-parse --show-toplevel` failed in {repo_dir:?} \
             (git could not confirm an isolated repository here): {}",
            String::from_utf8_lossy(&out.stderr)
        );
        let top = String::from_utf8_lossy(&out.stdout).trim().to_string();
        let want = std::fs::canonicalize(repo_dir).unwrap_or_else(|_| repo_dir.to_path_buf());
        let got = std::fs::canonicalize(&top).unwrap_or_else(|_| Path::new(&top).to_path_buf());
        assert_eq!(
            got, want,
            "escape-guard: fixture git resolves to {got:?}, not the intended tempdir \
             {want:?} — refusing to proceed to avoid corrupting the real repository"
        );
    }

    /// Builds the throwaway git repository plus linked worktree shared by
    /// [`find_root_from_worktree_returns_worktree_path`] and
    /// [`find_root_from_worktree_survives_concurrent_execution`].
    ///
    /// Mirrors, step-for-step, the git command sequence audited in
    /// `tech-docs.md`'s "Confirmed mechanism" section for this plan. **Isolation
    /// guarantee**: every step checks `output.status.success()` (or, for the
    /// final `git worktree add`, `ExitStatus::success()`) and panics loudly the
    /// instant any step fails, instead of only checking that the `git`
    /// subprocess spawned. This closes the historical race: when an earlier,
    /// unchecked step (e.g. `git init`) failed transiently, `main` was left
    /// without its own `.git`, so every later "isolated" git command silently
    /// fell back to whichever repository was `main`'s nearest ancestor via
    /// git's own upward repository-discovery walk — corrupting that ancestor's
    /// `HEAD` and local `user.*` config (observed 4 times against this
    /// repository's real checkout under `nx affected`'s parallel fanout).
    /// Failing loudly on the first bad exit status means a transient failure
    /// now surfaces as a clean test panic instead of a silent write into an
    /// unrelated repository.
    ///
    /// When `force_init_failure` is `true`, `git init` runs with a
    /// deliberately-invalid flag so it exits non-zero without creating `.git`
    /// in `main` — reproducing the confirmed root cause's empirical scratchpad
    /// finding that a failed, unchecked `git init` leaves `main` without its
    /// own `.git`. Post-fix, this is expected to panic here rather than
    /// silently proceed.
    fn build_worktree_fixture(main: &Path, wt_path: &Path, force_init_failure: bool) {
        // Every git call runs through `iso_git` so it is pinned to `main`'s own
        // `.git` (explicit `GIT_DIR`) and can never resolve to an ancestor/real
        // repository via CWD or discovery — the deeper fix for this plan's
        // corruption class (exit-status checking alone was insufficient).
        let run_checked = |args: &[&str]| {
            // Standard 4 (pre-write escape guard), applied before EVERY write:
            // once `main/.git` exists, prove git still resolves to `main` and
            // not an ancestor before running. `git init` is the sole pre-repo
            // command (no `.git` yet) and is exempt — its own failure is caught
            // by the exit-status assert below.
            if main.join(".git").is_dir() {
                assert_no_escape(main);
            }
            let output = iso_git(main)
                .args(args)
                .output()
                .expect("git command must spawn");
            assert!(
                output.status.success(),
                "git {args:?} in {main:?} must exit zero, got: {}",
                String::from_utf8_lossy(&output.stderr)
            );
        };

        if force_init_failure {
            // Deliberately-invalid flag: `git init` exits non-zero (129) and
            // never creates `.git` in `main`, without needing filesystem
            // permission tricks. The `run_checked` assert below panics here,
            // by design — see the doc comment above.
            run_checked(&["init", "--not-a-real-git-init-flag"]);
        } else {
            run_checked(&["init"]);
        }
        // Every subsequent write goes through `run_checked`, which re-runs the
        // escape guard before each one. In the `force_init_failure` path we
        // never reach here — the exit-status assert has already panicked.
        run_checked(&["config", "user.email", "test@test.com"]);
        run_checked(&["config", "user.name", "Test"]);
        std::fs::write(main.join("README.md"), "test").expect("write README");
        run_checked(&["add", "."]);
        run_checked(&["commit", "-m", "init"]);

        // Create a linked worktree (isolated to `main`'s own `.git`). Guard
        // before this write too, per Standard 4 (it does not go through
        // `run_checked`).
        assert_no_escape(main);
        let status = iso_git(main)
            .args(["worktree", "add", &wt_path.to_string_lossy(), "HEAD"])
            .status()
            .expect("git worktree add");
        assert!(status.success(), "git worktree add must succeed");
    }

    /// Regression lock: `find_root_from` uses `--show-toplevel` which is worktree-aware.
    /// A linked worktree's root resolves to the worktree path, not the main repo.
    ///
    /// Gherkin:
    ///   Given a synthetic linked worktree in the rhino-cli test suite
    ///   When a guardrail command runs inside it
    ///   Then it succeeds, proving repo-root resolution is worktree-aware
    #[test]
    fn find_root_from_worktree_returns_worktree_path() {
        let main_repo = TempDir::new().expect("tempdir");
        let main = main_repo.path();
        let wt_dir = TempDir::new().expect("tempdir wt");
        let wt_path = wt_dir.path();

        build_worktree_fixture(main, wt_path, false);

        // find_root_from the worktree path must return the WORKTREE path, not main.
        let resolved = find_root_from(Some(wt_path))
            .expect("find_root_from must succeed inside a linked worktree");
        let resolved_canonical = std::fs::canonicalize(&resolved).expect("canonicalize resolved");
        let wt_canonical = std::fs::canonicalize(wt_path).expect("canonicalize wt_path");
        assert_eq!(
            resolved_canonical, wt_canonical,
            "find_root_from must return the linked worktree path when invoked from it"
        );
    }

    /// Snapshot of the five git-identity/state signals the confirmed root
    /// cause corrupts: local `user.name`, local `user.email`, `worktree list
    /// --porcelain`, `HEAD`, and `reflog` (PRD AC-1, AC-2, and AC-3's
    /// git-identity non-contamination criterion). `reflog` is captured
    /// alongside `HEAD` because the documented real-incident corruption is a
    /// commit-then-`git reset` that can move the branch pointer back to its
    /// original value (see this plan's `tech-docs.md`): a net-unchanged `HEAD`
    /// that only the reflog's churn reveals. PRD AC-2 names `git reflog`
    /// explicitly for exactly this reason.
    #[derive(Debug, PartialEq, Eq)]
    struct GitIdentitySnapshot {
        /// Effective `git config --get user.name` in `dir`.
        user_name: String,
        /// Effective `git config --get user.email` in `dir`.
        user_email: String,
        /// `git worktree list --porcelain` output for the repo rooted at `dir`.
        worktree_list: String,
        /// `git rev-parse HEAD` output for the repo rooted at `dir`.
        head: String,
        /// `git reflog` output for the repo rooted at `dir` — catches a
        /// commit-then-reset that leaves `HEAD` net-unchanged but churns the ref.
        reflog: String,
    }

    /// Captures a [`GitIdentitySnapshot`] for the repository rooted at `dir`.
    fn snapshot_git_identity(dir: &Path) -> GitIdentitySnapshot {
        let capture = |args: &[&str]| -> String {
            let output = Cmd::new("git")
                .args(args)
                .current_dir(dir)
                .output()
                .expect("git snapshot command must spawn");
            String::from_utf8_lossy(&output.stdout).trim().to_string()
        };
        GitIdentitySnapshot {
            user_name: capture(&["config", "--get", "user.name"]),
            user_email: capture(&["config", "--get", "user.email"]),
            worktree_list: capture(&["worktree", "list", "--porcelain"]),
            head: capture(&["rev-parse", "HEAD"]),
            reflog: capture(&["reflog"]),
        }
    }

    /// Concurrency + fail-loud integration test for the corruption class
    /// documented in this plan's `tech-docs.md`. It exercises the full,
    /// hardened `build_worktree_fixture` under the same shape as the real
    /// incident — a fixture whose `main` sits *under* an ancestor repository's
    /// tree, whose `git init` fails, run on a spawned thread concurrently with
    /// a `find_root()` call in this thread — and asserts that neither the
    /// synthetic `ancestor` nor this suite's own real checkout observes any
    /// git-identity/HEAD/reflog/worktree drift.
    ///
    /// The `force_init_failure` path makes `git init` exit non-zero without
    /// creating `main/.git`. Two independent layers keep this safe: the
    /// exit-status check (Standard 5) panics `build_worktree_fixture` on that
    /// failure before any write is attempted, and the explicit `GIT_DIR` pin
    /// (Standard 2) would prevent any write that *did* run from resolving into
    /// the ancestor. This test proves the composed fixture is safe under
    /// concurrency; the isolated discriminator for the `GIT_DIR` layer
    /// specifically is [`iso_git_refuses_to_escape_into_ambient_ancestor_repo`],
    /// which fails RED if that pin is removed. A disposable `TempDir`-backed
    /// `ancestor`, rather than this suite's own checkout, keeps the reproduction
    /// safe regardless; a sanity snapshot of `real_root` proves no leakage into
    /// the actual working repository.
    ///
    /// Gherkin:
    ///   Given a synthetic "ancestor" repository with one real commit
    ///   And its `git init` step is forced to fail deterministically
    ///   When the worktree fixture setup runs concurrently with a `find_root()` call
    ///   Then the ancestor's `user.name`, `user.email`, `HEAD`, `reflog`, and
    ///     `worktree list` are unchanged before and after
    #[test]
    fn find_root_from_worktree_survives_concurrent_execution() {
        let _cwd = CwdLock::acquire();

        // Sanity check: this test's own probing must never leak into the
        // repository this test binary itself is running inside of.
        let real_root = find_root().expect("real repo root resolvable in test");
        let real_before = snapshot_git_identity(&real_root);

        // `ancestor` stands in for "the real repository" the confirmed defect
        // silently falls back into. One real commit plus a distinctive
        // identity (`Ancestor Real Repo`) makes any bleed-through unambiguous.
        let ancestor = TempDir::new().expect("tempdir ancestor");
        let ancestor_path = ancestor.path();
        // Seed `ancestor` through `iso_git` too, so even this stand-in repo is
        // pinned to its own `.git` and cannot itself escape.
        let run_checked = |args: &[&str]| {
            // Standard 4: guard before every write once `ancestor/.git` exists;
            // `git init` is exempt (no `.git` yet).
            if ancestor_path.join(".git").is_dir() {
                assert_no_escape(ancestor_path);
            }
            let status = iso_git(ancestor_path)
                .args(args)
                .status()
                .expect("git seed command must spawn");
            assert!(
                status.success(),
                "git {args:?} must succeed while seeding ancestor"
            );
        };
        run_checked(&["init"]);
        run_checked(&["config", "user.email", "ancestor@example.com"]);
        run_checked(&["config", "user.name", "Ancestor Real Repo"]);
        std::fs::write(ancestor_path.join("README.md"), "ancestor").expect("write ancestor readme");
        run_checked(&["add", "."]);
        run_checked(&["commit", "-m", "ancestor init"]);

        let ancestor_before = snapshot_git_identity(ancestor_path);

        // `main` sits under `ancestor`'s own tree (the temp dir "sits under the
        // real repo tree") but, via `force_init_failure`, never gets its own
        // `.git` — reproducing the confirmed root cause's empirical scratchpad
        // finding ("left without its own `.git`").
        let main = ancestor_path.join("main-worktree-fixture");
        std::fs::create_dir(&main).expect("create main dir");
        let wt_dir = TempDir::new().expect("tempdir wt");
        let wt_path = wt_dir.path().to_path_buf();

        // Run the fixture setup on a spawned thread, concurrently with a
        // `CwdLock`-guarded `find_root()` call in this thread (mirroring
        // `find_root_returns_repo_root`'s locking pattern) — wrapped so
        // capture below still runs even if the spawned thread panics.
        let handle = std::thread::spawn(move || {
            build_worktree_fixture(&main, &wt_path, true);
        });
        let _ = find_root().expect("find_root concurrently resolvable in test");
        let fixture_outcome = handle.join();

        // Re-capture regardless of whether the spawned thread panicked.
        let ancestor_after = snapshot_git_identity(ancestor_path);
        let real_after = snapshot_git_identity(&real_root);

        assert_eq!(
            real_before, real_after,
            "this test suite's own repository must never observe git-identity/HEAD/reflog/worktree \
             drift from this reproduction"
        );
        assert_eq!(
            ancestor_before, ancestor_after,
            "ancestor repository (user.name, user.email, worktree list, HEAD, reflog) must survive the \
             worktree fixture setup unchanged even when its git init step fails — the exit-status \
             check fails the fixture loud before any write, and the explicit GIT_DIR pin would keep \
             any write that did run out of the ancestor"
        );

        // A post-fix fixture is expected to fail loudly (panic) the moment its
        // forced `git init` failure is detected, rather than silently
        // corrupting `ancestor` while still "succeeding". Either outcome is
        // acceptable here — only the snapshot equality assertions above prove
        // isolation held.
        let _ = fixture_outcome;
    }

    /// Deterministic regression lock for the DEEPER fix ([`iso_git`], per the
    /// Git Fixture Isolation convention). Exit-status checking alone did not
    /// prevent the real incident: a fixture git write can still escape into an
    /// ancestor repository when the target dir has no `.git` of its own and git
    /// walks *up* the directory tree to find one. Here `inner` is nested
    /// directly under an `outer` stand-in "real" repo and deliberately has no
    /// `.git`. Plain `git` run there would discover `outer` and mutate it;
    /// [`iso_git`] pins `GIT_DIR` to `inner/.git` (which does not exist), so git
    /// refuses instead of escaping. This reproduces the escape condition without
    /// relying on a concurrency race, so it fails RED if the `GIT_DIR` pin is
    /// ever removed from `iso_git`.
    #[test]
    fn iso_git_refuses_to_escape_into_ambient_ancestor_repo() {
        let _cwd = CwdLock::acquire();

        let outer = TempDir::new().expect("tempdir outer");
        let outer_path = outer.path();
        let seed = |args: &[&str]| {
            assert!(
                iso_git(outer_path)
                    .args(args)
                    .status()
                    .expect("git seed must spawn")
                    .success(),
                "seeding outer stand-in repo must succeed: {args:?}"
            );
        };
        seed(&["init"]);
        seed(&["config", "user.email", "outer@example.com"]);
        seed(&["config", "user.name", "Outer Repo"]);
        std::fs::write(outer_path.join("keep.txt"), "outer").expect("write outer file");
        seed(&["add", "."]);
        seed(&["commit", "-m", "outer init"]);
        let outer_before = snapshot_git_identity(outer_path);

        // `inner` sits UNDER `outer` with no `.git` — the exact condition under
        // which plain git discovery walks up into `outer`.
        let inner = outer_path.join("inner-no-git");
        std::fs::create_dir(&inner).expect("create inner dir");

        // Under iso_git, GIT_DIR points at the non-existent `inner/.git`, so git
        // must refuse rather than discover `outer`. The write MUST fail and MUST
        // NOT touch `outer`.
        let out = iso_git(&inner)
            .args(["commit", "--allow-empty", "-m", "would-escape"])
            .output()
            .expect("git commit must spawn");
        assert!(
            !out.status.success(),
            "an isolated commit in a repo-less dir must fail loudly, not escape into an ancestor repo"
        );

        let outer_after = snapshot_git_identity(outer_path);
        assert_eq!(
            outer_before, outer_after,
            "iso_git must not let a git write in an ancestor-nested dir escape into the outer \
             repository (HEAD/reflog/worktree list/identity must be unchanged)"
        );
    }
}
