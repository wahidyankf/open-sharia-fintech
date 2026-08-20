//! Golden-master harness: replays every CLI invocation from tests/golden-master/manifest.json
//! and diffs stdout/stderr/exit-code byte-for-byte against the captured corpus.
//!
//! WHY: behavior-freezes the command surface before the hexagonal migration (Phases 7–9) so
//! any unintended output regression fails fast.
//!
//! To refresh the corpus after intentional changes:
//!   cargo run --release --manifest-path apps/rhino-cli/Cargo.toml -- <cmd> <subcmd> --help \
//!     > apps/rhino-cli/tests/golden-master/<file>.stdout
//!   echo $? > apps/rhino-cli/tests/golden-master/<file>.exit
#![allow(clippy::panic)]

use assert_cmd::Command;
use serde::Deserialize;
use std::{fs, path::PathBuf};
use tempfile::TempDir;

#[derive(Deserialize)]
struct Entry {
    file: String,
    args: Vec<String>,
}

/// Sentinel substituted with a freshly created, empty scratch directory before
/// replaying an entry. Some leaf commands (e.g. `specs scaffold dart`) write
/// files relative to their `--dir` target unconditionally; running those bare
/// against the crate's own working directory (the default `cargo test` cwd)
/// would corrupt the checked-out source tree. The commands that use this
/// sentinel print only counts/basenames, never the directory path itself, so
/// their stdout is scratch-path-independent and safe to freeze byte-for-byte.
const TMPDIR_SENTINEL: &str = "{{TMPDIR}}";

/// Resolves `{{TMPDIR}}` sentinels in `args` to `scratch`'s path, leaving
/// every other argument untouched.
fn resolve_args(args: &[String], scratch: &TempDir) -> Vec<String> {
    args.iter()
        .map(|a| {
            if a == TMPDIR_SENTINEL {
                scratch.path().to_string_lossy().into_owned()
            } else {
                a.clone()
            }
        })
        .collect()
}

fn corpus_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/golden-master")
}

fn read_corpus(name: &str, ext: &str) -> Vec<u8> {
    let path = corpus_dir().join(format!("{name}.{ext}"));
    fs::read(&path).unwrap_or_else(|e| panic!("missing corpus file {}: {e}", path.display()))
}

fn read_exit(name: &str) -> i32 {
    let raw = read_corpus(name, "exit");
    let s = String::from_utf8(raw)
        .expect("exit file is not UTF-8")
        .trim()
        .to_string();
    s.parse::<i32>()
        .unwrap_or_else(|_| panic!("invalid exit code in {name}.exit: {s:?}"))
}

#[test]
fn golden_master_replay() {
    let manifest_path = corpus_dir().join("manifest.json");
    let manifest_bytes = fs::read(&manifest_path)
        .unwrap_or_else(|e| panic!("missing manifest at {}: {e}", manifest_path.display()));
    let entries: Vec<Entry> =
        serde_json::from_slice(&manifest_bytes).expect("manifest.json is not valid JSON");

    for entry in &entries {
        let expected_stdout = read_corpus(&entry.file, "stdout");
        let expected_stderr = read_corpus(&entry.file, "stderr");
        let expected_exit = read_exit(&entry.file);

        let scratch = TempDir::new().expect("create scratch dir for golden-master replay");
        let resolved_args = resolve_args(&entry.args, &scratch);

        let output = Command::cargo_bin("rhino-cli")
            .expect("binary not found")
            .args(&resolved_args)
            .arg("--no-color")
            // `clap` reads `COLUMNS` from the environment to choose its
            // `--help` wrap width, and this process inherits the caller's
            // entire environment. zsh exports and updates `COLUMNS` on
            // `SIGWINCH` (terminal resize), so different invocations of this
            // same test inherited different values and made a byte-exact
            // `--help` comparison flake — reproduced diverging on the `md`
            // row's line wrap. Pin the width as a declared constant, matching
            // the width the corpus fixtures were captured at, rather than
            // clearing the variable: `.env_remove("COLUMNS")` would leave the
            // width implicit in clap's own default and re-break the moment
            // that default changes.
            .env("COLUMNS", "100")
            .output()
            .unwrap_or_else(|e| panic!("failed to run {:?}: {e}", entry.args));

        let actual_exit = output.status.code().unwrap_or(-1);

        assert_eq!(
            output.stdout,
            expected_stdout,
            "stdout mismatch for {:?}\nexpected:\n{}\ngot:\n{}",
            entry.args,
            String::from_utf8_lossy(&expected_stdout),
            String::from_utf8_lossy(&output.stdout),
        );

        assert_eq!(
            output.stderr,
            expected_stderr,
            "stderr mismatch for {:?}\nexpected:\n{}\ngot:\n{}",
            entry.args,
            String::from_utf8_lossy(&expected_stderr),
            String::from_utf8_lossy(&output.stderr),
        );

        assert_eq!(
            actual_exit, expected_exit,
            "exit code mismatch for {:?}: expected {expected_exit}, got {actual_exit}",
            entry.args
        );
    }
}
