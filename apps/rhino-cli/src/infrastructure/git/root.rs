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
        let run_checked = |args: &[&str]| {
            let output = Cmd::new("git")
                .args(args)
                .current_dir(main)
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
        run_checked(&["config", "user.email", "test@test.com"]);
        run_checked(&["config", "user.name", "Test"]);
        std::fs::write(main.join("README.md"), "test").expect("write README");
        run_checked(&["add", "."]);
        run_checked(&["commit", "-m", "init"]);

        // Create a linked worktree.
        let status = Cmd::new("git")
            .args(["worktree", "add", &wt_path.to_string_lossy(), "HEAD"])
            .current_dir(main)
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

    /// Snapshot of the four git-identity/state signals the confirmed root
    /// cause corrupts: local `user.name`, local `user.email`, `worktree list
    /// --porcelain`, and `HEAD` (PRD AC-1, AC-2, and AC-3's git-identity
    /// non-contamination criterion).
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
        }
    }

    /// Regression test for the confirmed root cause documented in this plan's
    /// `tech-docs.md` ("Confirmed mechanism: unchecked git exit status enables
    /// upward repository-discovery fallback"): `build_worktree_fixture` issues
    /// 5 of 6 `git` `Command`s via `.output().expect(...)`, which only checks
    /// that the subprocess spawned — never that `git` itself exited zero. The
    /// moment `git init` fails for any reason, every later "isolated" git
    /// command silently falls back to whichever repository is `main`'s nearest
    /// ancestor via `git`'s own upward repository-discovery walk.
    ///
    /// This test forces that `git init` failure deterministically (an
    /// intentionally-invalid flag — see `build_worktree_fixture`'s
    /// `force_init_failure` parameter) inside a synthetic `ancestor`
    /// repository standing in for "the real repository" the 4 real incidents
    /// corrupted. A disposable `TempDir`-backed `ancestor`, rather than this
    /// test suite's own checkout, keeps the reproduction fully safe: whatever
    /// gets corrupted is deleted with `ancestor`'s `TempDir` when the test
    /// ends. A sanity snapshot of this test suite's own repository
    /// (`real_root`) proves no leakage into the actual working repository
    /// regardless.
    ///
    /// Gherkin:
    ///   Given a synthetic "ancestor" repository with one real commit
    ///   And its `git init` step is forced to fail deterministically
    ///   When the worktree fixture setup runs concurrently with a `find_root()` call
    ///   Then the ancestor's `user.name`, `user.email`, `HEAD`, and `worktree list`
    ///     are unchanged before and after
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
        let run_checked = |args: &[&str]| {
            let status = Cmd::new("git")
                .args(args)
                .current_dir(ancestor_path)
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
            "this test suite's own repository must never observe git-identity/HEAD/worktree drift \
             from this reproduction"
        );
        assert_eq!(
            ancestor_before, ancestor_after,
            "ancestor repository (user.name, user.email, worktree list, HEAD) must survive the \
             worktree fixture setup unchanged even when its git init step fails — fails against the \
             pre-fix fixture because git's own upward repository-discovery silently redirects every \
             subsequent \"isolated\" git command into ancestor once git init's exit status goes \
             unchecked"
        );

        // A post-fix fixture is expected to fail loudly (panic) the moment its
        // forced `git init` failure is detected, rather than silently
        // corrupting `ancestor` while still "succeeding". Either outcome is
        // acceptable here — only the snapshot equality assertions above prove
        // isolation held.
        let _ = fixture_outcome;
    }
}
