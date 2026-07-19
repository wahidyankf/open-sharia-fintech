//! Cucumber-rs integration tests for the `doctor` command.
//!
//! Wires the behavior-contract feature file at
//! `specs/apps/rhino/behavior/rhino-cli/gherkin/system/doctor.feature` to step
//! definitions that build a synthetic repo (config files) plus a controlled
//! `PATH` of stub tool scripts, then drive the compiled `rhino-cli` binary.
//! This mirrors the Go integration test's PATH-manipulation strategy but makes
//! every scenario host-independent: the stubs deterministically supply tool
//! versions satisfying the synthetic config, so "all present" never depends on
//! what the host happens to have installed. Step-definition text mirrors the
//! gherkin verbatim for `spec-coverage --shared-steps` coverage.

// Test step-definition scaffolding: private World state and step fns are
// self-documenting via their #[given]/#[when]/#[then] gherkin strings.
#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]

use std::path::{Path, PathBuf};
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use tempfile::TempDir;

/// Each probed tool: (binary-name, stdout-or-stderr the stub prints). The
/// versions satisfy the config written by [`DoctorWorld::write_config`].
const STUB_TOOLS: &[(&str, &str)] = &[
    ("git", "git version 2.43.0"),
    ("volta", "2.0.2"),
    ("node", "v24.11.1"),
    ("npm", "11.0.0"),
    // java writes to stderr.
    ("mvn", "Apache Maven 3.9.6"),
    ("go", "go version go1.24.2 linux/amd64"),
    ("python3", "Python 3.13.1"),
    ("rustc", "rustc 1.90.0 (abc 2025-01-01)"),
    // cargo is special: `cargo llvm-cov --version` → "cargo-llvm-cov 0.6.0".
    (
        "elixir",
        "Erlang/OTP 27\n\nElixir 1.19.5 (compiled with Erlang/OTP 27)",
    ),
    // erl prints just the OTP release.
    ("dotnet", "10.0.103"),
    ("clj", "Clojure CLI version 1.12.0.1488"),
    ("dart", "Dart SDK version: 3.11.1 (stable)"),
    ("flutter", "Flutter 3.41.0"),
    ("docker", "Docker version 29.0.0, build abc"),
    ("jq", "jq-1.7.1"),
    ("shellcheck", "version: 0.10.0"),
    ("hadolint", "Haskell Dockerfile Linter 2.12.0"),
    ("actionlint", "1.7.7"),
    ("shfmt", "v3.13.1"),
    ("tofu", "OpenTofu v1.10.2"),
    ("clang-format", "clang-format version 18.1.0"),
    // npx playwright --version → "Version 1.58.0".
];

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct DoctorWorld {
    repo: TempDir,
    bin: TempDir,
    /// Override the node requirement to force a version mismatch (warning).
    node_req_override: Option<String>,
    scope: Option<String>,
    fix: bool,
    dry_run: bool,
    json: bool,
    output: Option<Output>,
}

impl std::fmt::Debug for DoctorWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("DoctorWorld").finish_non_exhaustive()
    }
}

impl DoctorWorld {
    fn new() -> Self {
        let repo = TempDir::new().expect("temp repo");
        std::fs::create_dir_all(repo.path().join(".git")).expect("mk .git");
        Self {
            repo,
            bin: TempDir::new().expect("temp bin"),
            node_req_override: None,
            scope: None,
            fix: false,
            dry_run: false,
            json: false,
            output: None,
        }
    }

    fn repo_path(&self) -> &Path {
        self.repo.path()
    }

    /// Writes all doctor config files into the synthetic repo. `node_req` lets
    /// the warning scenario inject a mismatching requirement.
    fn write_config(&self, node_req: &str) {
        let w = |rel: &str, content: &str| {
            let p = self.repo_path().join(rel);
            std::fs::create_dir_all(p.parent().expect("parent")).expect("mkdir");
            std::fs::write(p, content).expect("write");
        };
        w(
            "package.json",
            &format!("{{\"name\":\"t\",\"volta\":{{\"node\":\"{node_req}\",\"npm\":\"11.0.0\"}}}}"),
        );
        w(
            "apps/crud-be-fsharp-giraffe-jasb/pom.xml",
            "<project><properties><java.version>21</java.version></properties></project>",
        );
        w(
            "go.work",
            "go 1.24.0\n\nuse (\n\t./apps/crud-be-golang-gin\n)\n",
        );
        w("apps/crud-be-python-fastapi/.python-version", "3.13\n");
        w(".tool-versions", "erlang 27.0\nelixir 1.19.0-otp-27\n");
        w(
            "apps/crud-be-fsharp-giraffe/global.json",
            "{\"sdk\":{\"version\":\"10.0.100\",\"rollForward\":\"latestMinor\"}}",
        );
        w(
            "apps/crud-fe-dart-flutterweb/pubspec.yaml",
            "name: d\n\nenvironment:\n  sdk: ^3.11.0\n  flutter: \">=3.41.0\"\n",
        );
        w(
            "apps/crud-be-rust-axum/Cargo.toml",
            "[package]\nname = \"t\"\nrust-version = \"1.80\"\n",
        );
    }

    /// Creates executable stub scripts for every probed tool in `self.bin`.
    fn write_stubs(&self) {
        for (name, out) in STUB_TOOLS {
            if *name == "git" {
                // `git` gets a smarter stub — see `write_git_stub`.
                continue;
            }
            self.write_stub(name, &format!("printf '%s\\n' {}", shell_quote(out)));
        }
        self.write_git_stub();
        // java -version → stderr.
        self.write_stub("java", "printf 'openjdk version \"21.0.1\" 2024\\n' 1>&2");
        // cargo llvm-cov --version → stdout.
        self.write_stub("cargo", "printf 'cargo-llvm-cov 0.6.0\\n'");
        // erl -noshell ... → prints OTP release.
        self.write_stub("erl", "printf '27'");
        // npx playwright --version → stdout.
        self.write_stub("npx", "printf 'Version 1.58.0\\n'");
    }

    /// Writes a `git` stub smarter than the generic version-echo stub used
    /// for every other probed tool.
    ///
    /// `rhino-cli doctor` discovers its own repo root via
    /// `git rev-parse --show-toplevel` *before* running any tool checks
    /// (see `infrastructure::git::root::find_root`). With `PATH` restricted
    /// to this synthetic `bin` directory, that call resolves to this very
    /// stub, so a stub that always echoes a fixed version string
    /// (ignoring its arguments, like every other stub) would make
    /// `rev-parse --show-toplevel` print `"git version 2.43.0"` instead of a
    /// real path — `doctor` would then fail before printing anything rather
    /// than running its tool checks. This stub special-cases `rev-parse` to
    /// echo the real synthetic repo path and falls through to the fixed
    /// version string for `--version` (the "is git installed" probe).
    fn write_git_stub(&self) {
        let repo_path = self.repo_path().to_string_lossy().into_owned();
        self.write_stub(
            "git",
            &format!(
                "case \"$1\" in\n  rev-parse) printf '%s\\n' {} ;;\n  *) printf '%s\\n' 'git version 2.43.0' ;;\nesac",
                shell_quote(&repo_path)
            ),
        );
    }

    fn write_stub(&self, name: &str, body: &str) {
        let path = self.bin.path().join(name);
        // `#!/bin/sh` (an absolute path the kernel execs directly) rather
        // than `#!/usr/bin/env bash`: with `PATH` restricted to this
        // synthetic `bin` directory (no system bin dirs), `env` cannot
        // resolve `bash` via `PATH`, so every stub would fail at
        // interpreter-launch time with "env: bash: No such file or
        // directory" — before `body` (a POSIX `sh`-compatible one-liner)
        // ever runs.
        std::fs::write(&path, format!("#!/bin/sh\n{body}\n")).expect("write stub");
        #[cfg(unix)]
        {
            use std::os::unix::fs::PermissionsExt as _;
            std::fs::set_permissions(&path, std::fs::Permissions::from_mode(0o755))
                .expect("chmod stub");
        }
    }

    fn exec(&mut self) {
        // Default config if a Given did not set one.
        if !self.repo_path().join("package.json").exists() {
            let node_req = self
                .node_req_override
                .clone()
                .unwrap_or_else(|| "24.11.1".to_string());
            self.write_config(&node_req);
        }

        let mut args = vec!["doctor".to_string()];
        if let Some(s) = &self.scope {
            args.push("--scope".to_string());
            args.push(s.clone());
        }
        if self.fix {
            args.push("--fix".to_string());
        }
        if self.dry_run {
            args.push("--dry-run".to_string());
        }
        if self.json {
            args.push("--output".to_string());
            args.push("json".to_string());
        }
        args.push("--no-color".to_string());

        let path_value = self.bin.path().to_string_lossy().into_owned();

        let out = std::process::Command::new(cargo_bin("rhino-cli"))
            .args(&args)
            .current_dir(self.repo_path())
            .env("PATH", path_value)
            .output()
            .expect("run rhino-cli");
        self.output = Some(out);
    }

    fn stdout(&self) -> String {
        String::from_utf8_lossy(&self.output.as_ref().expect("ran").stdout).into_owned()
    }

    fn exit_code(&self) -> i32 {
        self.output
            .as_ref()
            .expect("ran")
            .status
            .code()
            .unwrap_or(-1)
    }
}

fn shell_quote(s: &str) -> String {
    format!("'{}'", s.replace('\'', "'\\''"))
}

// ===========================================================================
// Given
// ===========================================================================

#[given("all required development tools are present with matching versions")]
fn given_all_present(w: &mut DoctorWorld) {
    w.write_config("24.11.1");
    w.write_stubs();
}

#[given("a required development tool is not found in the system PATH")]
fn given_tool_missing(w: &mut DoctorWorld) {
    // `doctor` resolves its repo root via `git rev-parse` before checking tools,
    // so an entirely empty PATH would fail root-discovery before any tool report
    // is printed. Instead, keep every stub present except one probed tool
    // (`shellcheck`) so `doctor` runs and reports exactly that tool missing.
    w.write_config("24.11.1");
    w.write_stubs();
    let _ = std::fs::remove_file(w.bin.path().join("shellcheck"));
}

#[given("a required development tool is installed with a non-matching version")]
fn given_tool_mismatch(w: &mut DoctorWorld) {
    // node requirement "1.0.0" but the stub reports v24.11.1 → warning.
    w.write_config("1.0.0");
    w.write_stubs();
}

// ===========================================================================
// When
// ===========================================================================

#[when("the developer runs the doctor command")]
fn when_run_doctor(w: &mut DoctorWorld) {
    w.exec();
}

#[when("the developer runs the doctor command with JSON output")]
fn when_run_doctor_json(w: &mut DoctorWorld) {
    w.json = true;
    w.exec();
}

#[when("the developer runs the doctor command with minimal scope")]
fn when_run_doctor_minimal(w: &mut DoctorWorld) {
    w.scope = Some("minimal".to_string());
    w.exec();
}

#[when("the developer runs the doctor command with the fix flag")]
fn when_run_doctor_fix(w: &mut DoctorWorld) {
    w.fix = true;
    w.exec();
}

#[when("the developer runs the doctor command with fix and dry-run flags")]
fn when_run_doctor_fix_dry_run(w: &mut DoctorWorld) {
    w.fix = true;
    w.dry_run = true;
    w.exec();
}

// ===========================================================================
// Then
// ===========================================================================

#[then("the command exits successfully")]
fn then_exit_ok(w: &mut DoctorWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

#[then("the command exits with a failure code")]
fn then_exit_fail(w: &mut DoctorWorld) {
    assert_ne!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

#[then("the output reports each tool as passing")]
fn then_each_passing(w: &mut DoctorWorld) {
    let out = w.stdout();
    assert!(out.contains("Doctor Report"), "got: {out}");
    assert!(!out.contains('\u{2717}'), "unexpected cross-mark in: {out}");
}

#[then("the output identifies the missing tool")]
fn then_identifies_missing(w: &mut DoctorWorld) {
    let out = w.stdout().to_lowercase();
    assert!(
        out.contains('\u{2717}') || out.contains("missing") || out.contains("not found"),
        "got: {}",
        w.stdout()
    );
}

#[then("the output reports the tool as a warning rather than a failure")]
fn then_reports_warning(w: &mut DoctorWorld) {
    assert_eq!(w.exit_code(), 0, "warnings must not fail: {}", w.stdout());
    let out = w.stdout();
    assert!(
        out.contains('\u{26a0}') || out.to_lowercase().contains("warning"),
        "got: {out}"
    );
}

#[then("the output is valid JSON")]
fn then_valid_json(w: &mut DoctorWorld) {
    let out = w.stdout();
    let parsed = serde_json::from_str::<serde_json::Value>(&out);
    assert!(parsed.is_ok(), "invalid JSON: {out}");
}

#[then("the JSON lists every checked tool with its status")]
fn then_json_lists_tools(w: &mut DoctorWorld) {
    let out = w.stdout();
    let v: serde_json::Value = serde_json::from_str(&out).expect("valid JSON");
    let tools = v
        .get("tools")
        .and_then(|t| t.as_array())
        .expect("tools array");
    assert_eq!(tools.len(), 16, "expected 16 tools, got {}", tools.len());
    for t in tools {
        assert!(t.get("status").is_some(), "tool missing status: {t}");
    }
}

#[then("the output checks only the minimal tool set")]
fn then_minimal_set(w: &mut DoctorWorld) {
    let out = w.stdout();
    assert!(out.contains("(scope: minimal)"), "got: {out}");
    // Scope the exclusion check to the doctor tool report itself — text
    // after the "Target-share:" marker belongs to the unrelated
    // cargo-target-share doctor step and may legitimately mention crate
    // directory names (e.g. `crud-be-rust-axum`) that coincidentally
    // contain an excluded tool's name as a substring.
    let report = out.split("Target-share:").next().unwrap_or(&out);
    for excluded in [
        "java", "maven", "rust", "elixir", "dotnet", "clojure", "flutter",
    ] {
        assert!(
            !report.contains(excluded),
            "minimal should exclude {excluded}: {report}"
        );
    }
}

#[then("the output contains fix progress")]
fn then_fix_progress(w: &mut DoctorWorld) {
    let out = w.stdout();
    assert!(
        out.contains("Fix summary") || out.contains("Installing") || out.contains("Skip:"),
        "got: {out}"
    );
}

#[then("the output contains a dry-run preview")]
fn then_dry_run_preview(w: &mut DoctorWorld) {
    let out = w.stdout();
    assert!(
        out.contains("Would install") || out.contains("Skip:"),
        "got: {out}"
    );
}

#[then("the output reports nothing to fix")]
fn then_nothing_to_fix(w: &mut DoctorWorld) {
    assert!(w.stdout().contains("Nothing to fix"), "got: {}", w.stdout());
}

#[tokio::main]
async fn main() {
    DoctorWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_file())
        .await;
}

/// Points at the single `doctor.feature` file, not its parent `system/`
/// directory — that directory also holds `cargo-target-share.feature` (its
/// own binder, `tests/cargo_target_share.rs`, defines a disjoint step
/// vocabulary). Cucumber's `Basic` parser runs exactly one file, rather than
/// glob-walking every `*.feature` sibling, whenever the given path resolves
/// to a file (see `cucumber::parser::basic::Basic::parse`'s
/// `feats_path.is_file()` branch) — this keeps the two binders' step
/// vocabularies from cross-contaminating.
fn feature_file() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/system/doctor.feature")
        .canonicalize()
        .expect("feature file resolvable")
}
