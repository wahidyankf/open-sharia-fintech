//! Cucumber-rs integration tests for the `convention` command group:
//! `convention emoji validate`, `convention license validate`, and
//! `convention audit`.
//!
//! Wires the behavior-contract feature files at
//! `specs/apps/rhino/behavior/rhino-cli/gherkin/convention/` to step
//! definitions that synthesize source-tree and licensing fixtures inside a
//! fresh git-rooted temp workspace and drive the compiled `rhino-cli` binary,
//! asserting on its output and exit code.

// Test step-definition scaffolding: private World state and step fns are
// self-documenting via their #[given]/#[when]/#[then] gherkin strings.
#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]

use std::path::PathBuf;
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use tempfile::TempDir;

/// Shared scenario state. Each scenario gets a fresh git-rooted temp workspace
/// so the binary's `findGitRoot` resolves inside the fixture.
#[derive(cucumber::World)]
#[world(init = Self::new)]
struct ConventionWorld {
    work: TempDir,
    /// Repo-relative path of the fixture file or directory the emoji audit
    /// targets. Left empty for `convention license validate`, which takes no
    /// positional path.
    target: String,
    /// Full CLI subcommand path under test (e.g.
    /// `["convention", "emoji", "validate"]`), excluding the trailing target
    /// path and `--no-color` flag.
    subcommand: Vec<&'static str>,
    output: Option<Output>,
}

impl std::fmt::Debug for ConventionWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ConventionWorld")
            .field("target", &self.target)
            .finish_non_exhaustive()
    }
}

impl ConventionWorld {
    fn new() -> Self {
        let work = TempDir::new().expect("temp workspace");
        init_git_repo(work.path());
        Self {
            work,
            target: String::new(),
            subcommand: vec!["convention", "emoji", "validate"],
            output: None,
        }
    }

    fn write(&self, rel: &str, content: &str) {
        let p = self.work.path().join(rel);
        if let Some(parent) = p.parent() {
            std::fs::create_dir_all(parent).expect("mk fixture dir");
        }
        std::fs::write(p, content).expect("write fixture");
    }

    /// Writes a minimal MIT `LICENSE` file under the directory `rel` (e.g.
    /// `apps/foo`).
    fn write_mit_license(&self, rel: &str) {
        self.write(&format!("{rel}/LICENSE"), "MIT License\n\nCopyright.\n");
    }

    /// Sets `target` to `rel` and writes `content` at that same repo-relative
    /// path — the shared shape of every single-file emoji-audit fixture.
    fn set_target_and_write(&mut self, rel: &str, content: &str) {
        self.target = rel.to_string();
        self.write(rel, content);
    }

    fn exec(&mut self) {
        let mut args: Vec<String> = self.subcommand.iter().map(|s| (*s).to_string()).collect();
        if !self.target.is_empty() {
            args.push(self.target.clone());
        }
        args.push("--no-color".to_string());

        let mut cmd = std::process::Command::new(cargo_bin("rhino-cli"));
        cmd.args(&args).current_dir(self.work.path());
        let out = cmd.output().expect("run rhino-cli");
        self.output = Some(out);
    }

    fn stdout(&self) -> String {
        String::from_utf8_lossy(&self.output.as_ref().expect("ran").stdout).into_owned()
    }

    /// Concatenates stdout and stderr, mirroring how a developer watching the
    /// terminal sees both streams interleaved. `convention audit`'s aggregate
    /// pass/fail summary and per-member failure lines are written to stderr.
    fn combined_output(&self) -> String {
        let out = self.output.as_ref().expect("ran");
        format!(
            "{}{}",
            String::from_utf8_lossy(&out.stdout),
            String::from_utf8_lossy(&out.stderr)
        )
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

fn init_git_repo(dir: &std::path::Path) {
    std::process::Command::new("git")
        .args(["init", "-q"])
        .current_dir(dir)
        .env("GIT_AUTHOR_NAME", "t")
        .env("GIT_AUTHOR_EMAIL", "t@t")
        .env("GIT_COMMITTER_NAME", "t")
        .env("GIT_COMMITTER_EMAIL", "t@t")
        .output()
        .expect("git init");
}

// ===========================================================================
// Given steps — convention emoji validate
// ===========================================================================

#[given("a source tree containing no emoji codepoints in forbidden file types")]
fn given_emoji_clean_tree(w: &mut ConventionWorld) {
    w.target = ".".to_string();
    w.write("src/clean.go", "package main\n\nfunc main() {}\n");
    w.write("config/settings.json", "{\n  \"key\": \"value\"\n}\n");
}

#[given("a JSON file containing an emoji codepoint")]
fn given_emoji_json_finding(w: &mut ConventionWorld) {
    w.set_target_and_write("conf.json", "{\n  \"label\": \"hi \u{2713} there\"\n}\n");
}

#[given("a Go source file containing an emoji codepoint")]
fn given_emoji_go_finding(w: &mut ConventionWorld) {
    w.set_target_and_write(
        "main.go",
        "package main\n\n// \u{1F680} launch\nfunc main() {}\n",
    );
}

#[given("a forbidden file containing multibyte non-emoji unicode such as Arabic")]
fn given_emoji_arabic_no_finding(w: &mut ConventionWorld) {
    w.set_target_and_write(
        "doc.json",
        "{\n  \"label\": \"\u{0645}\u{0631}\u{062D}\u{0628}\u{0627}\"\n}\n",
    );
}

#[given("a source tree with an emoji-containing file inside the archived directory")]
fn given_emoji_archived_skip(w: &mut ConventionWorld) {
    w.target = ".".to_string();
    w.write("archived/old.json", "{\n  \"label\": \"\u{2713}\"\n}\n");
}

#[given("a source tree with an emoji-containing agent skill source file")]
fn given_emoji_agent_skill_skip(w: &mut ConventionWorld) {
    w.target = ".".to_string();
    w.write(
        ".agents/skills/example/scripts/tool.py",
        "message = '\u{2713}'\n",
    );
}

// ===========================================================================
// Given steps — convention license validate
// ===========================================================================

#[given("a repository where every required directory has a matching MIT LICENSE file")]
fn given_license_all_clean(w: &mut ConventionWorld) {
    w.write("apps/foo/main.rs", "// app\n");
    w.write_mit_license("apps/foo");
    w.write("libs/bar/lib.rs", "// lib\n");
    w.write_mit_license("libs/bar");
    w.write("specs/spec.md", "# Spec\n");
    w.write_mit_license("specs");
    w.write(
        "LICENSING-NOTICE.md",
        "# Notice\n\n| Path | License |\n| --- | --- |\n| apps/foo | MIT |\n| libs/bar | MIT |\n| specs | MIT |\n",
    );
}

#[given("a repository where one app directory is missing its LICENSE file")]
fn given_license_app_missing(w: &mut ConventionWorld) {
    w.write("apps/foo/main.rs", "// app\n");
}

#[given("a repository where one lib directory is missing its LICENSE file")]
fn given_license_lib_missing(w: &mut ConventionWorld) {
    w.write("libs/bar/lib.rs", "// lib\n");
}

#[given(
    "a repository where a LICENSING-NOTICE.md table row claims a license that disagrees with the on-disk LICENSE file"
)]
fn given_license_spdx_mismatch(w: &mut ConventionWorld) {
    w.write("apps/foo/main.rs", "// app\n");
    w.write_mit_license("apps/foo");
    w.write(
        "LICENSING-NOTICE.md",
        "# Notice\n\n| Path | License |\n| --- | --- |\n| apps/foo | Apache-2.0 |\n",
    );
}

// ===========================================================================
// When steps
// ===========================================================================

#[when("the developer runs convention emoji validate on the tree")]
#[when("the developer runs convention emoji validate on the file")]
fn when_run_emoji_validate(w: &mut ConventionWorld) {
    w.subcommand = vec!["convention", "emoji", "validate"];
    w.exec();
}

#[when("the developer runs convention license validate")]
fn when_run_license_validate(w: &mut ConventionWorld) {
    w.subcommand = vec!["convention", "license", "validate"];
    w.target = String::new();
    w.exec();
}

#[when(regex = r#"^the developer runs "rhino-cli convention audit"$"#)]
fn when_run_convention_audit(w: &mut ConventionWorld) {
    w.subcommand = vec!["convention", "audit"];
    w.target = String::new();
    w.exec();
}

// ===========================================================================
// Then steps — shared exit-code assertions
// ===========================================================================

#[then("the command exits with a failure code")]
fn then_exit_fail(w: &mut ConventionWorld) {
    assert_eq!(w.exit_code(), 1, "stdout: {}", w.stdout());
}

#[then("the command exits successfully")]
fn then_exit_ok(w: &mut ConventionWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

// ===========================================================================
// Then steps — convention emoji validate
// ===========================================================================

#[then("the output reports zero emoji findings")]
fn then_emoji_zero_findings(w: &mut ConventionWorld) {
    let out = w.stdout();
    assert!(out.contains("EMOJI AUDIT PASSED"), "got: {out}");
}

#[then("the output identifies the offending file line and codepoint")]
fn then_emoji_identifies_finding(w: &mut ConventionWorld) {
    let out = w.stdout();
    assert!(out.contains("EMOJI AUDIT FAILED"), "got: {out}");
    assert!(out.contains(&w.target), "got: {out}");
    assert!(out.contains("U+"), "got: {out}");
}

// ===========================================================================
// Then steps — convention license validate
// ===========================================================================

#[then("the output reports zero license findings")]
fn then_license_zero_findings(w: &mut ConventionWorld) {
    let out = w.stdout();
    assert!(out.contains("LICENSE AUDIT PASSED"), "got: {out}");
}

// Matches both "app" and "lib" wording, sharing one assertion body since the
// two scenarios differ only in which fixture directory (`apps/foo` vs.
// `libs/bar`) is expected to appear in the finding.
#[then(regex = r"^the output identifies the missing LICENSE (app|lib) directory$")]
#[allow(clippy::needless_pass_by_value)] // cucumber-rs binds the capture by value
fn then_license_missing_dir(w: &mut ConventionWorld, kind: String) {
    let expected_dir = if kind == "app" {
        "apps/foo"
    } else {
        "libs/bar"
    };
    let out = w.stdout();
    assert!(out.contains("LICENSE AUDIT FAILED"), "got: {out}");
    assert!(out.contains("missing-license"), "got: {out}");
    assert!(out.contains(expected_dir), "got: {out}");
}

#[then("the output identifies the SPDX mismatch")]
fn then_license_spdx_mismatch(w: &mut ConventionWorld) {
    let out = w.stdout();
    assert!(out.contains("LICENSE AUDIT FAILED"), "got: {out}");
    assert!(out.contains("spdx-mismatch"), "got: {out}");
    assert!(out.contains("apps/foo"), "got: {out}");
}

// ===========================================================================
// convention audit steps (convention-audit.feature)
// ===========================================================================

#[then(regex = r#"^the output names the failing "([a-z-]+)" validator$"#)]
#[allow(clippy::needless_pass_by_value)] // cucumber-rs binds the capture by value
fn then_convention_audit_names_failure(w: &mut ConventionWorld, member: String) {
    let out = w.combined_output();
    assert!(out.contains("CONVENTION AUDIT FAILED"), "got: {out}");
    assert!(out.contains(&member), "got: {out}");
}

#[tokio::main]
async fn main() {
    ConventionWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/convention")
        .canonicalize()
        .expect("feature dir resolvable")
}
