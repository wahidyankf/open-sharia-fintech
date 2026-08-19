//! Shared Git Fixture Isolation helper for cucumber-rs integration suites.
//!
//! Every suite that shells out to `git` against a synthetic `TempDir` fixture
//! must run every invocation through [`run_git`], which carries all six
//! mandatory layers from
//! `repo-governance/development/quality/git-fixture-isolation/enforcement.md`:
//!
//! 1. `GIT_DIR` pinned to `dir/.git` — no upward repository-discovery walk.
//! 2. `GIT_CEILING_DIRECTORIES` capping any residual walk at `dir`.
//! 3. `GIT_CONFIG_GLOBAL` / `GIT_CONFIG_SYSTEM` nulled — deterministic
//!    identity, no bleed-in from the developer's own git config.
//! 4. A pre-write escape guard ([`assert_no_escape`]) proving, before every
//!    write once `dir/.git` exists, that git still resolves to `dir` and
//!    nowhere else.
//! 5. A real exit-status assertion — not just that the process spawned.
//! 6. `GIT_AUTHOR_NAME`/`EMAIL` and `GIT_COMMITTER_NAME`/`EMAIL` set to a
//!    fixed synthetic identity, so commits never depend on (or pollute) the
//!    developer's real git identity.
//!
//! Not a `#[test]`-harness binary itself — cargo only autodiscovers files
//! directly under `tests/`, so this file in `tests/support/` is invisible to
//! target discovery and is instead pulled in with
//! `#[path = "support/git_fixture.rs"] mod git_fixture;` by every suite that
//! needs it. That keeps "what Git Fixture Isolation means" defined exactly
//! once rather than re-derived per suite, the gap this module closes.
//!
//! cucumber-rs runs scenarios concurrently (up to 64 by default), so a
//! silently-failed `git init` — or any write reached without every layer
//! above — could let a later "isolated" fixture fall back to whichever
//! repository is `dir`'s nearest ancestor via git's own upward-discovery walk.
//! That is the documented motivating incident this convention exists to
//! prevent.

#![allow(dead_code)] // Not every importing suite calls every function.

use std::path::Path;
use std::process::{Command, Output};

/// Pre-write escape guard (Standard 4). Panics unless git, under the same
/// isolation env as [`run_git`], resolves its top-level to `dir`
/// (canonicalized). Called before every write once `dir/.git` exists, so a
/// would-be escape fails loud instead of silently corrupting the real
/// repository. `GIT_WORK_TREE` is deliberately NOT set: it would make
/// `--show-toplevel` merely echo the variable, defeating the guard.
///
/// `pub`, not private: at least one suite (`specs_tree.rs`'s
/// `worktree-agnostic.feature` steps) needs the guard standalone, ahead of a
/// `git worktree add` write that cannot go through [`run_git`] itself because
/// its isolation env differs (no `GIT_WORK_TREE`, an explicit destination
/// argument instead).
pub fn assert_no_escape(dir: &Path) {
    let out = Command::new("git")
        .args(["rev-parse", "--show-toplevel"])
        .current_dir(dir)
        .env("GIT_DIR", dir.join(".git"))
        .env("GIT_CEILING_DIRECTORIES", dir)
        .env("GIT_CONFIG_GLOBAL", "/dev/null")
        .env("GIT_CONFIG_SYSTEM", "/dev/null")
        .output()
        .expect("escape-guard: git rev-parse must spawn");
    assert!(
        out.status.success(),
        "escape-guard: `git rev-parse --show-toplevel` failed in {} (git could not confirm an \
         isolated repository here): {}",
        dir.display(),
        String::from_utf8_lossy(&out.stderr)
    );
    let top = String::from_utf8_lossy(&out.stdout).trim().to_string();
    let want = std::fs::canonicalize(dir).unwrap_or_else(|_| dir.to_path_buf());
    let got = std::fs::canonicalize(&top).unwrap_or_else(|_| Path::new(&top).to_path_buf());
    assert_eq!(
        got,
        want,
        "escape-guard: fixture git resolves to {}, not the intended tempdir {} — \
         refusing to proceed to avoid corrupting the real repository",
        got.display(),
        want.display()
    );
}

/// Runs `git` with `args` inside `dir`, under full Git Fixture Isolation.
///
/// `dir` is always a repository root (or the destination's containing
/// directory for `clone`), so `dir/.git` is the repo's git directory. Pinning
/// `GIT_DIR` explicitly makes git perform NO upward repository-discovery
/// walk: even if this process's cwd races to the real worktree under
/// cucumber-rs's concurrency, git operates on exactly `dir/.git` and can
/// never fall back to an ancestor repository. `GIT_CEILING_DIRECTORIES` caps
/// any residual walk, and nulling global/system config keeps identity
/// deterministic.
///
/// Before every write, once `dir/.git` exists, [`assert_no_escape`] proves
/// git still resolves to `dir`. `git init` (and `git clone` into a directory
/// that has no `.git` of its own yet) are the sole pre-repo commands and are
/// exempt — their own failure is caught by the exit-status assert below.
///
/// # Panics
///
/// Panics if the process fails to spawn, if it exits non-zero, or if the
/// pre-write escape guard fails.
pub fn run_git(dir: &Path, args: &[&str]) -> Output {
    if dir.join(".git").is_dir() {
        assert_no_escape(dir);
    }
    let output = Command::new("git")
        .args(args)
        .current_dir(dir)
        .env("GIT_DIR", dir.join(".git"))
        .env("GIT_CEILING_DIRECTORIES", dir)
        .env("GIT_CONFIG_GLOBAL", "/dev/null")
        .env("GIT_CONFIG_SYSTEM", "/dev/null")
        .env("GIT_AUTHOR_NAME", "t")
        .env("GIT_AUTHOR_EMAIL", "t@t")
        .env("GIT_COMMITTER_NAME", "t")
        .env("GIT_COMMITTER_EMAIL", "t@t")
        .output()
        .expect("git command must spawn");
    assert!(
        output.status.success(),
        "git {args:?} in {} must exit zero, got: {}",
        dir.display(),
        String::from_utf8_lossy(&output.stderr)
    );
    output
}
