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
use rhino_cli::application::repo_config::{self, HarnessEntry, OwnershipClass, RepoConfig};
use tempfile::TempDir;

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct RepoConfigValidateWorld {
    /// Synthetic git repo carrying a copy of the canonical repo-config.yml.
    repo: TempDir,
    /// Result of validating the canonical (valid) config.
    valid_output: Option<Output>,
    /// The `codex` harness registry entry, sliced out of the canonical config.
    codex_entry: Option<String>,
    /// The canonical config text, captured when ownership is inspected.
    canonical: Option<String>,
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
            codex_entry: None,
            canonical: None,
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

/// The eight vendored `.agents/skills/` subdirectories: plugin payload shipped
/// with the repository, with no `.claude/skills/` counterpart to regenerate them
/// from. The mirror emitter must leave every one of them untouched (DD-7).
const VENDORED_SKILL_DIRS: &[&str] = &[
    ".agents/skills/cavecrew",
    ".agents/skills/caveman",
    ".agents/skills/caveman-commit",
    ".agents/skills/caveman-compress",
    ".agents/skills/caveman-help",
    ".agents/skills/caveman-review",
    ".agents/skills/caveman-stats",
    ".agents/skills/compress",
];

/// Slice the `- name: codex` list item out of the canonical `harness:` block.
///
/// Runs from the entry's own `- name: codex` line up to (but excluding) the next
/// line that starts at column 0, which is the next top-level section.
fn slice_codex_entry(config: &str) -> String {
    let start = config
        .find("  - name: codex")
        .expect("canonical config declares a codex harness entry");
    let rest = &config[start..];
    let end = rest
        .match_indices('\n')
        .map(|(i, _)| i + 1)
        .find(|&i| rest[i..].chars().next().is_some_and(|c| !c.is_whitespace()))
        .unwrap_or(rest.len());
    rest[..end].to_string()
}

#[given("the canonical repo-config.yml")]
fn given_canonical_config(w: &mut RepoConfigValidateWorld) {
    init_git_repo(w.repo.path());
    std::fs::write(
        w.repo.path().join("repo-config.yml"),
        canonical_repo_config(),
    )
    .unwrap();
}

#[when("the codex harness entry is inspected")]
fn when_codex_entry_inspected(w: &mut RepoConfigValidateWorld) {
    w.codex_entry = Some(slice_codex_entry(&canonical_repo_config()));
}

#[then("it declares \".agents/skills\" as a mirror of \".claude/skills\"")]
fn then_declares_skills_mirror(w: &mut RepoConfigValidateWorld) {
    let entry = w.codex_entry.as_ref().expect("codex entry sliced");
    assert!(
        entry.contains("skills-dir: .agents/skills"),
        "codex entry must declare the mirror target; entry was:\n{entry}"
    );
    assert!(
        entry.contains("skills-mirrors: .claude/skills"),
        "codex entry must declare WHICH source tree .agents/skills mirrors, so the \
         emitter reads its input from the registry rather than inferring it; entry was:\n{entry}"
    );
    // A declaration the schema does not know is a silent no-op, so prove the
    // strict deserializer actually accepts it rather than merely tolerating it.
    let out = validate_config(&canonical_repo_config());
    assert!(
        out.status.success(),
        "the canonical config carrying skills-mirrors must strict-deserialize; stdout={} stderr={}",
        String::from_utf8_lossy(&out.stdout),
        String::from_utf8_lossy(&out.stderr)
    );
}

#[then("it declares the eight vendored skill subdirectories")]
fn then_declares_vendored_dirs(w: &mut RepoConfigValidateWorld) {
    let entry = w.codex_entry.as_ref().expect("codex entry sliced");
    assert!(
        entry.contains("vendored:"),
        "codex entry must carry a vendored: block; entry was:\n{entry}"
    );
    let missing: Vec<&str> = VENDORED_SKILL_DIRS
        .iter()
        .copied()
        .filter(|dir| !entry.contains(dir))
        .collect();
    assert!(
        missing.is_empty(),
        "codex entry must declare every vendored directory; missing {missing:?}; entry was:\n{entry}"
    );
    assert_eq!(
        VENDORED_SKILL_DIRS.len(),
        8,
        "the vendored set is exactly the eight plugin directories recorded in the Phase 6a baseline"
    );
}

#[then("each vendored entry names the plugin it came from")]
fn then_vendored_entries_name_their_origin(w: &mut RepoConfigValidateWorld) {
    let entry = w.codex_entry.as_ref().expect("codex entry sliced");
    // A bare path list says WHICH directories are exempt but not WHY, so a later
    // reader cannot tell a genuine plugin payload from a mistake someone silenced.
    for dir in VENDORED_SKILL_DIRS {
        let line = entry
            .lines()
            .find(|l| l.trim_start().starts_with(&format!("- {dir}")))
            .unwrap_or_else(|| panic!("vendored entry {dir} must be on its own line"));
        let (path, comment) = line
            .split_once('#')
            .unwrap_or_else(|| panic!("vendored entry {dir} carries no inline origin comment"));
        assert!(
            path.trim().ends_with(dir),
            "vendored entry {dir} must be one path per line; got: {line}"
        );
        assert!(
            comment.contains("plugin"),
            "vendored entry {dir} must name its plugin origin; got comment: {comment}"
        );
    }
}

#[then("the schema rejects a typo'd key inside the vendored declaration")]
fn then_rejects_typod_vendored_key(_w: &mut RepoConfigValidateWorld) {
    // Falsifiable the other way: the same config without the typo must pass, so
    // the rejection is attributable to the typo and not to the block as a whole.
    let canonical = canonical_repo_config();
    assert!(
        validate_config(&canonical).status.success(),
        "baseline canonical config must validate before the typo is injected"
    );
    let typod = canonical.replacen("    vendored:", "    vendoredd:", 1);
    assert_ne!(
        typod, canonical,
        "the typo injection must actually change the config"
    );
    let out = validate_config(&typod);
    assert!(
        !out.status.success(),
        "deny_unknown_fields must reject a typo'd key in the vendored block; stdout={}",
        String::from_utf8_lossy(&out.stdout)
    );
}

// ---------------------------------------------------------------------------
// Ownership classification (US-8) — the schema half. The behavioural half lives
// in `harness/harness-ownership.feature`, driven by `tests/harness_ownership.rs`.
// ---------------------------------------------------------------------------

/// Paths a harness entry claims, and therefore must classify. Instruction
/// surfaces count: `AGENTS.md` is a file a harness reads, so leaving it
/// unclassified is exactly the residue this phase exists to eliminate.
fn claimed_paths(entry: &HarnessEntry) -> Vec<String> {
    let mut paths = Vec::new();
    for opt in [
        entry.agent_dir.as_ref(),
        entry.skills_dir.as_ref(),
        entry.rules_dir.as_ref(),
        entry.config.as_ref(),
    ]
    .into_iter()
    .flatten()
    {
        paths.push(opt.clone());
    }
    paths.extend(entry.vendored.iter().cloned());
    paths.extend(entry.instruction.iter().cloned());
    paths
}

/// Load the canonical config through the real loader, so the assertions below
/// exercise the deserializer the command uses rather than a parallel parser.
fn load_canonical() -> RepoConfig {
    let dir = TempDir::new().expect("temp repo");
    init_git_repo(dir.path());
    std::fs::write(dir.path().join("repo-config.yml"), canonical_repo_config()).unwrap();
    repo_config::load(dir.path()).expect("canonical config loads")
}

#[when("the harness ownership declarations are inspected")]
fn when_ownership_inspected(w: &mut RepoConfigValidateWorld) {
    w.canonical = Some(canonical_repo_config());
}

#[then(
    "every binding path a harness entry claims carries exactly one of the classes \"generated\", \"vendored\", or \"source\""
)]
fn then_every_claimed_path_is_classified(_w: &mut RepoConfigValidateWorld) {
    let config = load_canonical();
    let mut unclassified: Vec<String> = Vec::new();
    let mut duplicated: Vec<String> = Vec::new();
    for entry in &config.harness {
        for path in claimed_paths(entry) {
            let declarations = entry
                .ownership
                .iter()
                .filter(|o| o.path == path)
                .collect::<Vec<_>>();
            match declarations.len() {
                0 => unclassified.push(format!("{}: {path}", entry.name)),
                1 => {
                    // Exhaustive match: a fourth class cannot be added to the
                    // enum without this failing to compile.
                    match declarations[0].class {
                        OwnershipClass::Generated
                        | OwnershipClass::Vendored
                        | OwnershipClass::Source => {}
                    }
                }
                _ => duplicated.push(format!("{}: {path}", entry.name)),
            }
        }
    }
    assert!(
        unclassified.is_empty(),
        "every path a harness entry claims must carry a declared ownership class; \
         unclassified: {unclassified:?}"
    );
    assert!(
        duplicated.is_empty(),
        "a path must carry exactly one class, never two; duplicated: {duplicated:?}"
    );
}

#[then("a registry entry declaring a fourth class value fails to deserialize")]
fn then_fourth_class_rejected(_w: &mut RepoConfigValidateWorld) {
    let canonical = canonical_repo_config();
    assert!(
        validate_config(&canonical).status.success(),
        "baseline canonical config must validate before a fourth class is injected"
    );
    let mutated = canonical.replacen("class: source", "class: bespoke", 1);
    assert_ne!(
        mutated, canonical,
        "the fourth-class injection must actually change the config"
    );
    let out = validate_config(&mutated);
    assert!(
        !out.status.success(),
        "a class value outside generated/vendored/source must be a hard deserialization \
         error rather than a silently-ignored value; stdout={}",
        String::from_utf8_lossy(&out.stdout)
    );
}

#[then("a vendored declaration carrying an empty reason fails validation")]
fn then_vendored_without_reason_rejected(_w: &mut RepoConfigValidateWorld) {
    let canonical = canonical_repo_config();
    let line = canonical
        .lines()
        .find(|l| l.contains("class: vendored"))
        .expect("at least one vendored ownership declaration")
        .to_string();
    let (before_reason, _) = line
        .split_once("reason:")
        .expect("a vendored declaration carries a reason on the same line");
    let blanked = format!("{before_reason}reason: \"\" }}");
    let mutated = canonical.replacen(&line, &blanked, 1);
    assert_ne!(
        mutated, canonical,
        "the empty-reason injection must actually change the config"
    );
    let out = validate_config(&mutated);
    assert!(
        !out.status.success(),
        "a vendored declaration with an empty reason must fail; an exempt path whose \
         justification is blank is indistinguishable from one nobody justified; stdout={}",
        String::from_utf8_lossy(&out.stdout)
    );
}

#[then("the canonical config carrying a non-empty reason on every vendored declaration exits 0")]
fn then_canonical_vendored_reasons_pass(_w: &mut RepoConfigValidateWorld) {
    let config = load_canonical();
    let mut reasonless: Vec<String> = Vec::new();
    for entry in &config.harness {
        for owned in &entry.ownership {
            if owned.class == OwnershipClass::Vendored
                && owned.reason.as_ref().is_none_or(|r| r.trim().is_empty())
            {
                reasonless.push(format!("{}: {}", entry.name, owned.path));
            }
        }
    }
    assert!(
        reasonless.is_empty(),
        "every vendored declaration must carry a non-empty reason; missing: {reasonless:?}"
    );
    let out = validate_config(&canonical_repo_config());
    assert!(
        out.status.success(),
        "the canonical config must validate; stdout={} stderr={}",
        String::from_utf8_lossy(&out.stdout),
        String::from_utf8_lossy(&out.stderr)
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
