//! Regression test for the wiring `src/main.rs:10` provides around
//! [`rhino_cli::infrastructure::stdio_blocking::make_std_streams_blocking`].
//!
//! `src/infrastructure/stdio_blocking.rs`'s own unit tests exercise
//! `clear_nonblock` directly against a synthetic pipe, but nothing exercises
//! `make_std_streams_blocking()` through the one call site that actually
//! wires it into the binary. A regression that deletes that call from
//! `main.rs` leaves those unit tests green while reintroducing the original
//! bug: a large report over an inherited non-blocking stdout panics
//! mid-write with `failed printing to stdout: ... (os error 35)` instead of
//! completing.
//!
//! This test builds the pipe itself (rather than `Stdio::piped()`, which
//! never carries `O_NONBLOCK`) so the write end's flag can be set BEFORE the
//! child inherits it — reproducing exactly what a git hook hands the real
//! binary — then spawns the compiled binary against a fixture large enough
//! to exceed the OS pipe buffer while this test deliberately delays
//! draining it.

use std::fs;
use std::io::Read;
use std::os::fd::AsFd;
use std::path::Path;
use std::process::{Command, Stdio};
use std::time::Duration;

use assert_cmd::cargo::cargo_bin;
use rustix::fs::{OFlags, fcntl_getfl, fcntl_setfl};
use tempfile::TempDir;

/// Number of broken-link fixture files. Each contributes a detail line (plus
/// shared category/summary text) to `md links validate`'s report. Empirically
/// tuned on this repo's CI/dev hardware to reliably exceed the OS pipe
/// buffer (observed 64 KiB on macOS under load) across the several
/// `write(2)` calls Rust's line-buffered stdout performs per `print!` — 400
/// files (~22 KiB of report) was insufficient and passed even with the
/// `main.rs` wiring under test deliberately removed; 6000 reliably fails
/// without it.
const BROKEN_LINK_FILE_COUNT: usize = 6000;

/// Pre-write escape guard (Git Fixture Isolation convention, Standard 4).
/// Panics unless git, under the same isolation env as [`run_git`], resolves
/// its top-level to `dir` (canonicalized). Mirrors `tests/governance.rs`'s
/// and `tests/specs_tree.rs`'s `assert_no_escape` exactly — see those copies'
/// doc comments for the full rationale. `GIT_WORK_TREE` is deliberately NOT
/// set: it would make `--show-toplevel` merely echo the variable, defeating
/// the guard.
fn assert_no_escape(dir: &Path) {
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
    let want = fs::canonicalize(dir).unwrap_or_else(|_| dir.to_path_buf());
    let got = fs::canonicalize(&top).unwrap_or_else(|_| Path::new(&top).to_path_buf());
    assert_eq!(
        got,
        want,
        "escape-guard: fixture git resolves to {}, not the intended tempdir {} — refusing to \
         proceed to avoid corrupting the real repository",
        got.display(),
        want.display()
    );
}

/// Runs `git` with `args` inside `dir`, under full Git Fixture Isolation
/// (all six mandatory layers — see
/// `repo-governance/development/quality/git-fixture-isolation.md`). Mirrors
/// `tests/governance.rs`'s `run_git` exactly: explicit `GIT_DIR` closes
/// ambient upward discovery (Standard 2), `GIT_CEILING_DIRECTORIES` caps any
/// residual walk (Standard 1), the nulled `GIT_CONFIG_GLOBAL`/
/// `GIT_CONFIG_SYSTEM` keep identity deterministic and out of the developer's
/// real config (Standard 3), the pre-write escape guard runs before every
/// write once `dir/.git` exists (Standard 4), and the exit status is checked
/// via `status.success()` rather than a bare `.expect()` on the spawn result
/// (Standard 5). Standard 6 is a process rule for whoever runs this test:
/// diagnose failures in a throwaway clone, never in the primary worktree.
///
/// Hand-rolling a bare `Command::new("git").args(["init", "--quiet"])` here
/// instead is not a lesser variant of this helper, it is a live escape: with
/// an ambient `GIT_DIR` exported, `git init` exits 0, creates nothing in
/// `dir`, and reinitializes the ambient repository's `config`/`HEAD`/`hooks`
/// templates.
fn run_git(dir: &Path, args: &[&str]) {
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
}

#[test]
fn large_report_completes_over_an_inherited_nonblocking_stdout_pipe() {
    let tmp = TempDir::new().expect("tempdir");
    let root = tmp.path();

    run_git(root, &["init", "-q"]);
    // The repository must actually exist in the fixture root afterwards: a
    // `git init` that silently retargeted an ambient repo would leave this
    // absent while still exiting zero.
    assert!(
        root.join(".git").is_dir(),
        "git init must have created a repository inside the fixture root {}",
        root.display()
    );
    assert_no_escape(root);

    for i in 0..BROKEN_LINK_FILE_COUNT {
        fs::write(
            root.join(format!("broken-{i}.md")),
            format!("[missing link {i}](./does-not-exist-{i}.md)\n"),
        )
        .expect("write fixture file");
    }

    // A pipe this test owns end-to-end, so `O_NONBLOCK` can be forced on the
    // write end before the child process inherits it as its stdout.
    let (mut reader, writer) = std::io::pipe().expect("create pipe");
    let flags = fcntl_getfl(writer.as_fd()).expect("fcntl getfl");
    fcntl_setfl(writer.as_fd(), flags | OFlags::NONBLOCK).expect("fcntl setfl NONBLOCK");

    let child = Command::new(cargo_bin("rhino-cli"))
        .args(["md", "links", "validate"])
        .current_dir(root)
        // The subject must resolve the fixture repository, not an ambient one
        // inherited from the caller's environment — otherwise this test
        // silently stops testing what it claims (and can report on the real
        // checkout). Mirrors the `env -u GIT_DIR -u GIT_WORK_TREE
        // -u GIT_COMMON_DIR` prefix every rhino-cli Nx target already carries.
        .env_remove("GIT_DIR")
        .env_remove("GIT_WORK_TREE")
        .env_remove("GIT_COMMON_DIR")
        .env("GIT_CEILING_DIRECTORIES", root)
        .stdout(writer)
        .stderr(Stdio::piped())
        .spawn()
        .expect("spawn rhino-cli");

    // Deliberately do not drain the pipe immediately. The whole point is to
    // let the OS pipe buffer fill while the child bursts many `write(2)`
    // calls — exactly the condition that produced `os error 35` in
    // production before `main.rs` started clearing `O_NONBLOCK` at startup.
    std::thread::sleep(Duration::from_millis(300));

    let mut stdout_buf = Vec::new();
    reader
        .read_to_end(&mut stdout_buf)
        .expect("drain child stdout to EOF");

    let output = child.wait_with_output().expect("wait for child");
    let stderr = String::from_utf8_lossy(&output.stderr);
    let stdout = String::from_utf8_lossy(&stdout_buf);

    assert!(
        !stderr.contains("failed printing to stdout"),
        "the binary must not panic on EAGAIN even when it inherits a \
         non-blocking stdout — that is exactly what \
         `make_std_streams_blocking()` at `main.rs`'s first line exists to \
         prevent; stderr was:\n{stderr}"
    );
    // `md links validate` exits non-zero because every fixture file is a
    // deliberately broken link; the assertion that matters here is the
    // ABSENCE of the EAGAIN panic above, not the exit code — a regression
    // that deletes the `main.rs` wiring call would still exit non-zero, it
    // would just also panic before finishing the report.
    assert!(
        stdout.contains("Broken Links Report") && stdout.contains("Total broken links"),
        "the full report must have been written to completion despite the \
         inherited non-blocking descriptor:\n{stdout}"
    );
}
