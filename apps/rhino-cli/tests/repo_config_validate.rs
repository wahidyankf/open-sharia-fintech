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

/// This crate is byte-identical across sibling repositories whose plugin payload
/// differs, so the vendored set is *derived* rather than listed. A hard-coded
/// list would encode one repository's tree into an assertion the other cannot
/// satisfy — and a repository that ships no plugin skills at all is a legitimate
/// state, not a failure.
fn real_repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..")
}

/// Every `.agents/skills/<dir>` with no `.claude/skills/<dir>` counterpart:
/// plugin payload shipped with the repository, with no canonical source to
/// regenerate it from. The mirror emitter must leave every one untouched (DD-7).
/// Returns repo-relative paths, sorted; empty when the repository vendors none.
fn vendored_skill_dirs() -> Vec<String> {
    let root = real_repo_root();
    let mirror = root.join(".agents/skills");
    let Ok(entries) = std::fs::read_dir(&mirror) else {
        return Vec::new();
    };
    let mut out: Vec<String> = entries
        .filter_map(Result::ok)
        .filter(|e| e.path().is_dir())
        .map(|e| e.file_name().to_string_lossy().into_owned())
        .filter(|name| !root.join(".claude/skills").join(name).is_dir())
        .map(|name| format!(".agents/skills/{name}"))
        .collect();
    out.sort();
    out
}

/// The paths declared inside the codex entry's `vendored:` block, in declaration
/// order. Empty when the entry carries no such block.
fn declared_vendored_paths(entry: &str) -> Vec<String> {
    let Some(start) = entry.find("\n    vendored:") else {
        return Vec::new();
    };
    entry[start + 1..]
        .lines()
        .skip(1)
        .take_while(|l| l.starts_with("      - "))
        .map(|l| {
            l.trim_start()
                .trim_start_matches("- ")
                .split('#')
                .next()
                .unwrap_or_default()
                .trim()
                .to_string()
        })
        .collect()
}

/// The canonical config with a `vendored:` block guaranteed present on the codex
/// entry: returned unchanged when one is already declared, and otherwise given a
/// single-entry block inserted after `skills-mirrors:`. Lets a schema assertion
/// about that key run in a repository that vendors nothing.
///
/// The injected path is declared in BOTH hand-maintained lists, because the
/// validator cross-checks them — injecting only the `vendored:` half would make
/// this helper fail for a reason that has nothing to do with the key it is
/// probing.
fn with_vendored_block(config: &str) -> String {
    /// Path used only by the injected probe block; never touches the real tree.
    const PROBE: &str = ".agents/skills/probe";

    if config.contains("\n    vendored:") {
        return config.to_string();
    }
    let anchor = "    skills-mirrors: .claude/skills\n";
    let at = config
        .find(anchor)
        .expect("codex entry declares skills-mirrors")
        + anchor.len();
    let mut out = String::with_capacity(config.len() + 192);
    out.push_str(&config[..at]);
    out.push_str("    vendored:\n      - ");
    out.push_str(PROBE);
    out.push_str(" # plugin payload, no source\n");
    let rest = &config[at..];
    let ownership = "    ownership:\n";
    let own_at = rest
        .find(ownership)
        .expect("codex entry declares ownership")
        + ownership.len();
    out.push_str(&rest[..own_at]);
    out.push_str("      - { path: ");
    out.push_str(PROBE);
    out.push_str(", class: vendored, reason: injected probe }\n");
    out.push_str(&rest[own_at..]);
    out
}

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

#[then("it declares every vendored skill subdirectory")]
fn then_declares_vendored_dirs(w: &mut RepoConfigValidateWorld) {
    let entry = w.codex_entry.as_ref().expect("codex entry sliced");
    let expected = vendored_skill_dirs();
    let declared = declared_vendored_paths(entry);
    // Both directions. Missing catches a plugin the emitter would delete;
    // extra catches a declaration protecting a directory that no longer exists,
    // which is how a stale exemption outlives the thing it exempted.
    let missing: Vec<&String> = expected.iter().filter(|d| !declared.contains(d)).collect();
    assert!(
        missing.is_empty(),
        "every .agents/skills directory without a .claude/skills counterpart must be declared \
         vendored; missing {missing:?}; entry was:\n{entry}"
    );
    let extra: Vec<&String> = declared.iter().filter(|d| !expected.contains(d)).collect();
    assert!(
        extra.is_empty(),
        "a vendored declaration must name a directory that exists and has no canonical source; \
         stale {extra:?}; entry was:\n{entry}"
    );
    // A repository vendoring nothing is legitimate — but then the block must be
    // absent rather than present-and-empty, so the two states cannot be confused.
    if expected.is_empty() {
        assert!(
            !entry.contains("\n    vendored:"),
            "this repository vendors no plugin skills, so the codex entry must carry no \
             vendored: block at all; entry was:\n{entry}"
        );
    }
}

#[then("each vendored entry names the plugin it came from")]
fn then_vendored_entries_name_their_origin(w: &mut RepoConfigValidateWorld) {
    let entry = w.codex_entry.as_ref().expect("codex entry sliced");
    // A bare path list says WHICH directories are exempt but not WHY, so a later
    // reader cannot tell a genuine plugin payload from a mistake someone silenced.
    for dir in vendored_skill_dirs() {
        let line = entry
            .lines()
            .find(|l| l.trim_start().starts_with(&format!("- {dir}")))
            .unwrap_or_else(|| panic!("vendored entry {dir} must be on its own line"));
        let (path, comment) = line
            .split_once('#')
            .unwrap_or_else(|| panic!("vendored entry {dir} carries no inline origin comment"));
        assert!(
            path.trim().ends_with(&dir),
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
    // A repository that vendors nothing carries no block to typo, so one is
    // injected first — which also proves the schema accepts the key rather than
    // merely tolerating its absence.
    let canonical = with_vendored_block(&canonical_repo_config());
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
