//! Cucumber-rs suite for `rhino-cli repo-config validate` — the schema-parity
//! gate. Drives the compiled binary against synthetic git repos whose
//! `repo-config.yml` is a copy of the canonical file (valid), a value-only
//! variant (must pass), and key-set variants (unknown key / empty required —
//! must fail). Step text mirrors the gherkin verbatim.

#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::unwrap_used, clippy::panic)]

use std::path::{Path, PathBuf};
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use tempfile::TempDir;

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct RepoConfigValidateWorld {
    /// Synthetic git repo carrying a copy of the canonical repo-config.yml.
    repo: TempDir,
    /// Result of validating the canonical (valid) config.
    valid_output: Option<Output>,
}

impl std::fmt::Debug for RepoConfigValidateWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("RepoConfigValidateWorld")
            .finish_non_exhaustive()
    }
}

impl RepoConfigValidateWorld {
    fn new() -> Self {
        Self {
            repo: TempDir::new().expect("temp repo"),
            valid_output: None,
        }
    }
}

/// The canonical repo-config.yml (this repo's own file), used as the "valid" baseline.
fn canonical_repo_config() -> String {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    let path = manifest.join("../../repo-config.yml");
    std::fs::read_to_string(&path).expect("read canonical repo-config.yml")
}

fn init_git_repo(dir: &Path) {
    let out = std::process::Command::new("git")
        .args(["init", "-q"])
        .current_dir(dir)
        .output()
        .expect("run git init");
    assert!(out.status.success(), "git init failed: {out:?}");
}

/// Write `content` as `repo-config.yml` in a fresh git repo and run
/// `repo-config validate` there, returning the process output.
fn validate_config(content: &str) -> Output {
    let dir = TempDir::new().expect("temp repo");
    init_git_repo(dir.path());
    std::fs::write(dir.path().join("repo-config.yml"), content).unwrap();
    std::process::Command::new(cargo_bin("rhino-cli"))
        .args(["repo-config", "validate", "--no-color"])
        .current_dir(dir.path())
        .env("PWD", dir.path())
        .output()
        .expect("run rhino-cli repo-config validate")
}

#[given("\"rhino-cli repo-config validate\" in each repo's pre-commit and pre-push/PR")]
fn given_command_wired(w: &mut RepoConfigValidateWorld) {
    init_git_repo(w.repo.path());
    std::fs::write(
        w.repo.path().join("repo-config.yml"),
        canonical_repo_config(),
    )
    .unwrap();
}

#[when("repo-config.yml is validated")]
fn when_validated(w: &mut RepoConfigValidateWorld) {
    let out = std::process::Command::new(cargo_bin("rhino-cli"))
        .args(["repo-config", "validate", "--no-color"])
        .current_dir(w.repo.path())
        .env("PWD", w.repo.path())
        .output()
        .expect("run rhino-cli repo-config validate");
    w.valid_output = Some(out);
}

#[then("the command strict-deserializes it against the canonical RepoConfig schema")]
fn then_strict_deserializes(w: &mut RepoConfigValidateWorld) {
    let out = w.valid_output.as_ref().expect("validation ran");
    assert!(
        out.status.success(),
        "canonical repo-config.yml must validate cleanly; stdout={} stderr={}",
        String::from_utf8_lossy(&out.stdout),
        String::from_utf8_lossy(&out.stderr)
    );
}

#[then("it passes when only values differ")]
fn then_passes_when_values_differ(_w: &mut RepoConfigValidateWorld) {
    // Same key set, different values: flip a coverage `specs` glob value.
    let mutated = canonical_repo_config().replacen(
        "specs/apps/rhino/behavior/rhino-cli/**",
        "specs/apps/rhino/behavior/rhino-cli/gherkin/**",
        1,
    );
    let out = validate_config(&mutated);
    assert!(
        out.status.success(),
        "a value-only change (identical key set) must still pass; stderr={}",
        String::from_utf8_lossy(&out.stderr)
    );
}

#[then("it fails when a required key is missing or an unknown key is present")]
fn then_fails_on_key_set_drift(_w: &mut RepoConfigValidateWorld) {
    // Unknown top-level key.
    let with_unknown = format!("{}\nbogus-unknown-section: true\n", canonical_repo_config());
    let out_unknown = validate_config(&with_unknown);
    assert!(
        !out_unknown.status.success(),
        "an unknown top-level key must be rejected; stdout={}",
        String::from_utf8_lossy(&out_unknown.stdout)
    );

    // Missing required content: empty coverage.projects.
    let empty_coverage = "harness:\n  - { name: claude-code, tier: source, agent-dir: .claude/agents }\ncoverage:\n  projects: []\nspecs:\n  ddd-areas: []\n  domain-areas: []\n";
    let out_missing = validate_config(empty_coverage);
    assert!(
        !out_missing.status.success(),
        "empty coverage.projects (missing required content) must be rejected; stdout={}",
        String::from_utf8_lossy(&out_missing.stdout)
    );
}

#[then(
    "running it independently against the byte-identical schema in both repos is equivalent to an identical key set across both repo-config.yml files"
)]
fn then_identical_key_set_equivalence(_w: &mut RepoConfigValidateWorld) {
    // Equivalence: value-only difference (identical key set) passes; a key-set
    // difference (unknown key) fails. So "all three pass against the byte-identical
    // schema" iff their key sets are identical.
    let value_variant = canonical_repo_config().replacen(
        "specs/apps/rhino/behavior/rhino-cli/**",
        "specs/apps/rhino/behavior/rhino-cli/gherkin/**",
        1,
    );
    let key_variant = format!("{}\nbogus-unknown-section: true\n", canonical_repo_config());
    assert!(
        validate_config(&value_variant).status.success(),
        "identical key set (values differ) must validate"
    );
    assert!(
        !validate_config(&key_variant).status.success(),
        "divergent key set (unknown key) must fail"
    );
}

#[tokio::main]
async fn main() {
    RepoConfigValidateWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/repo-config-validate")
        .canonicalize()
        .expect("feature dir resolvable")
}
