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

#[test]
fn large_report_completes_over_an_inherited_nonblocking_stdout_pipe() {
    let tmp = TempDir::new().expect("tempdir");
    let root = tmp.path();

    Command::new("git")
        .args(["init", "--quiet"])
        .current_dir(root)
        .status()
        .expect("git init must succeed");

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
