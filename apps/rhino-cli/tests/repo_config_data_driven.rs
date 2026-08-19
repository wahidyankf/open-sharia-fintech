//! Cucumber-rs suite asserting rhino-cli reads its repo-specific behaviour
//! (env globs, domain-areas, ddd-areas) from `repo-config.yml` rather than from
//! source-hard-coded per-repo literals.
//!
//! Wires `specs/apps/rhino/behavior/rhino-cli/gherkin/repo-config/` to step
//! definitions that build a synthetic repo whose `repo-config.yml` declares a
//! custom ddd-area, then drive `specs counts validate` and assert the custom
//! area (not a hard-coded default) drives the scan.

#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::unwrap_used, clippy::panic)]

use std::path::{Path, PathBuf};

use cucumber::{World as _, given, then, when};
use rhino_cli::application::doctor::build_tool_defs;
use rhino_cli::application::repo_config::{self, HarnessEntry};
use rhino_cli::application::repo_governance::frontmatter_audit::audit_frontmatter;
use rhino_cli::application::specs::required_spec_folders;
use rhino_cli::commands::repo_config_validate;
use rhino_cli::commands::specs_validate_counts::{ValidateCountsArgs, run_at_root};
use rhino_cli::infrastructure::fs::real::RealFs;
use rhino_cli::infrastructure::git::root::find_root_from;
use tempfile::TempDir;

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct RepoConfigDataWorld {
    /// Synthetic repo whose repo-config.yml declares a custom ddd-area.
    repo: TempDir,
    /// Result of running `specs counts validate` with no explicit app list.
    ran_ok: bool,
    /// Captured stdout of the run.
    output: String,
    /// Codex harness entry loaded from the real repository config.
    codex_entry: Option<HarnessEntry>,
    /// Every harness entry loaded from the real repository config.
    all_entries: Vec<HarnessEntry>,
    /// Whether a configured website exclusion was honoured by the audit.
    website_exclusions_respected: bool,
    /// Whether the configured .NET SDK path drove Doctor's version reader.
    dotnet_global_json_respected: bool,
}

impl std::fmt::Debug for RepoConfigDataWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("RepoConfigDataWorld")
            .finish_non_exhaustive()
    }
}

impl RepoConfigDataWorld {
    fn new() -> Self {
        Self {
            repo: TempDir::new().expect("temp repo"),
            ran_ok: false,
            output: String::new(),
            codex_entry: None,
            all_entries: Vec::new(),
            website_exclusions_respected: false,
            dotnet_global_json_respected: false,
        }
    }
}

fn write(root: &Path, rel: &str, content: &str) {
    let p = root.join(rel);
    std::fs::create_dir_all(p.parent().unwrap()).unwrap();
    std::fs::write(p, content).unwrap();
}

/// Regression for P1B-WEBSITE: repository-specific website exclusions belong
/// to the frontmatter gate's configuration, rather than shared Rust source.
fn website_prefix_exclusions_are_runtime_config() {
    let repo = TempDir::new().expect("temp repo");
    let root = repo.path();
    write(
        root,
        "repo-config.yml",
        concat!(
            "harness: []\n",
            "coverage:\n  projects: []\n",
            "gates:\n",
            "  - id: md-frontmatter-dates\n",
            "    type: check\n",
            "    command: md frontmatter-dates\n",
            "    kind: rhino-cli\n",
            "    args:\n",
            "      exclude:\n",
            "        - apps/custom-site/\n",
            "    surfaces:\n",
            "      ci: { scope: all-file-type }\n",
        ),
    );
    write(
        root,
        "apps/custom-site/content/post.md",
        "---\nupdated: 2026-01-01\n---\n",
    );

    let config = repo_config::load(root).expect("custom repo config must load");
    let exclusions = config
        .gates
        .iter()
        .find(|gate| gate.id == "md-frontmatter-dates")
        .and_then(|gate| gate.args.get("exclude"))
        .expect("frontmatter gate must declare exclusions");
    let findings = audit_frontmatter(&RealFs, &[root.to_string_lossy().to_string()], exclusions)
        .expect("audit must run");
    assert!(
        findings.is_empty(),
        "a configured website path must be skipped; findings: {findings:#?}"
    );
}

/// Regression for P1B-DOC-COMMENT: Doctor's .NET SDK source path is
/// repository data, rather than a shared-source application literal.
fn dotnet_global_json_is_runtime_config() {
    let repo = TempDir::new().expect("temp repo");
    let root = repo.path();
    write(
        root,
        "repo-config.yml",
        "doctor:\n  dotnet-global-json: tooling/sdk/global.json\n",
    );
    write(
        root,
        "tooling/sdk/global.json",
        r#"{"sdk":{"version":"9.0.100"}}"#,
    );

    let dotnet = build_tool_defs(root)
        .into_iter()
        .find(|tool| tool.name == "dotnet")
        .expect("dotnet tool definition");
    assert_eq!(dotnet.source, "doctor.dotnet-global-json → sdk.version");
    assert_eq!(
        (dotnet.read_req)(),
        "9.0.100",
        "Doctor must read the configured .NET SDK path"
    );
}

/// Regression for the harness-registry contraction: the repository supports
/// exactly three coding-agent harnesses, and the registry is the single place
/// that says so. Fixture-backed against the real `repo-config.yml` rather than
/// a synthetic one, because the point is what THIS repository declares.
fn harness_registry_declares_exactly_three_harnesses() {
    let root = find_root_from(None).expect("repo root");
    let config = repo_config::load(&root).expect("load repo-config.yml");

    let mut names: Vec<&str> = config.harness.iter().map(|h| h.name.as_str()).collect();
    names.sort_unstable();

    assert_eq!(
        names,
        vec!["claude-code", "codex", "opencode"],
        "{} harness entries found, 3 expected",
        names.len()
    );
}

/// Runs the named regression selected by Cargo's test-filter argument.
///
/// This Cucumber target uses `harness = false`, so Cargo forwards a filter to
/// this binary rather than discovering `#[test]` functions. Recognising the
/// two P1B extraction names preserves the plan's focused RED/GREEN commands
/// without weakening the normal no-filter Cucumber run.
fn run_selected_extraction_regression() -> bool {
    match std::env::args().nth(1).as_deref() {
        Some("website_prefix_exclusions_are_runtime_config") => {
            website_prefix_exclusions_are_runtime_config();
            true
        }
        Some("dotnet_global_json_is_runtime_config") => {
            dotnet_global_json_is_runtime_config();
            true
        }
        Some("harness_registry_declares_exactly_three_harnesses") => {
            harness_registry_declares_exactly_three_harnesses();
            true
        }
        _ => false,
    }
}

#[given("rhino-cli's repo-specific behaviour (env globs, domain/ddd areas)")]
fn given_repo_config_declares_custom_ddd_area(w: &mut RepoConfigDataWorld) {
    let root = w.repo.path();
    // repo-config.yml declares a custom ddd-area that is NOT one of the historical
    // hard-coded defaults (organiclever / ose).
    write(
        root,
        "repo-config.yml",
        concat!(
            "harness: []\n",
            "coverage:\n  projects: []\n",
            "specs:\n  ddd-areas:\n    - widget-app\n  domain-areas: []\n",
        ),
    );
    // Give widget-app a complete, clean spec tree so a data-driven scan passes.
    for sub in required_spec_folders() {
        write(root, &format!("specs/apps/widget-app/{sub}/a.md"), "x\n");
    }
}

#[when("rhino-cli runs")]
fn when_specs_counts_runs(w: &mut RepoConfigDataWorld) {
    let args = ValidateCountsArgs {
        folder: None,
        apps: vec![],
    };
    let mut buf: Vec<u8> = Vec::new();
    let result = run_at_root(w.repo.path(), &args, &mut buf);
    w.ran_ok = result.is_ok();
    w.output = String::from_utf8_lossy(&buf).into_owned();
}

#[then("it reads that behaviour from repo-config.yml, not from source hard-coded per repo")]
fn then_reads_from_repo_config(w: &mut RepoConfigDataWorld) {
    assert!(
        w.output.contains("widget-app"),
        "default scan must target the repo-config.yml ddd-area 'widget-app' (data-driven), \
         not source-hard-coded defaults; got output: {}",
        w.output
    );
    assert!(
        w.ran_ok,
        "the config-declared widget-app tree is clean, so the run must succeed; got output: {}",
        w.output
    );
}

#[given("the harness registry section of repo-config.yml")]
fn given_harness_registry_section(w: &mut RepoConfigDataWorld) {
    let root = find_root_from(None).expect("repo root");
    let config = repo_config::load(&root).expect("load repo-config.yml");
    w.codex_entry = config.harness.iter().find(|h| h.name == "codex").cloned();
    w.all_entries = config.harness;
}

#[when("the codex entry is read")]
fn when_codex_entry_is_read(w: &mut RepoConfigDataWorld) {
    assert!(
        w.codex_entry.is_some(),
        "codex harness entry must exist in repo-config.yml"
    );
}

#[when("the full registry is read")]
fn when_full_registry_is_read(w: &mut RepoConfigDataWorld) {
    assert!(
        !w.all_entries.is_empty(),
        "the harness registry must not be empty"
    );
}

#[then("the entry declares the generated tier")]
fn then_codex_entry_generated_tier(w: &mut RepoConfigDataWorld) {
    let entry = w.codex_entry.as_ref().expect("codex entry loaded");
    assert_eq!(entry.tier, "generated");
}

#[then("the entry declares .codex/agents as its agent directory")]
fn then_codex_entry_agent_dir(w: &mut RepoConfigDataWorld) {
    let entry = w.codex_entry.as_ref().expect("codex entry loaded");
    assert_eq!(entry.agent_dir.as_deref(), Some(".codex/agents"));
}

#[then("the entry declares .claude/agents as the source it mirrors")]
fn then_codex_entry_mirror_source(w: &mut RepoConfigDataWorld) {
    let entry = w.codex_entry.as_ref().expect("codex entry loaded");
    assert_eq!(entry.mirrors.as_deref(), Some(".claude/agents"));
}

#[then("the entry declares no forbidden directory")]
fn then_codex_entry_no_forbid_dir(w: &mut RepoConfigDataWorld) {
    // `.codex/agents/*.toml` IS the official Codex subagent surface, so a
    // `forbid-dir` here would block the correct layout outright.
    let entry = w.codex_entry.as_ref().expect("codex entry loaded");
    assert_eq!(
        entry.forbid_dir, None,
        "codex must not forbid its own official subagent directory"
    );
}

#[then("it names exactly claude-code, opencode, and codex")]
fn then_registry_names_exactly_three(w: &mut RepoConfigDataWorld) {
    let mut names: Vec<&str> = w.all_entries.iter().map(|h| h.name.as_str()).collect();
    names.sort_unstable();
    assert_eq!(names, vec!["claude-code", "codex", "opencode"]);
}

#[given("the frontmatter-date gate declares website exclusions")]
fn given_frontmatter_date_gate_declares_website_exclusions(_w: &mut RepoConfigDataWorld) {}

#[when("the configured frontmatter-date audit runs")]
fn when_configured_frontmatter_date_audit_runs(w: &mut RepoConfigDataWorld) {
    website_prefix_exclusions_are_runtime_config();
    w.website_exclusions_respected = true;
}

#[then("configured excluded website content is skipped")]
fn then_configured_excluded_website_content_is_skipped(w: &mut RepoConfigDataWorld) {
    assert!(w.website_exclusions_respected);
}

#[given("the Doctor configuration declares a .NET SDK path")]
fn given_doctor_config_declares_dotnet_global_json(_w: &mut RepoConfigDataWorld) {}

#[when("Doctor resolves its required .NET SDK version")]
fn when_doctor_resolves_dotnet_version(w: &mut RepoConfigDataWorld) {
    dotnet_global_json_is_runtime_config();
    w.dotnet_global_json_respected = true;
}

#[then("the configured global.json supplies that version")]
fn then_configured_dotnet_global_json_supplies_version(w: &mut RepoConfigDataWorld) {
    assert!(w.dotnet_global_json_respected);
}

fn gates_section_deserializes_gate_entries() {
    let repo = TempDir::new().expect("temp repo");
    write(
        repo.path(),
        "repo-config.yml",
        concat!(
            "gates:\n",
            "  - id: repo-config-validate\n",
            "    type: check\n",
            "    command: repo-config validate\n",
            "    kind: rhino-cli\n",
            "    surfaces:\n",
            "      pre-push: { scope: all-file-type }\n",
        ),
    );

    repo_config::load(repo.path()).expect(
        "a gates section must deserialize as gate entries with id, type, command, kind, and surfaces",
    );
}

fn gate_parse_error(gate: &str) -> String {
    let repo = TempDir::new().expect("temp repo");
    write(repo.path(), "repo-config.yml", &format!("gates:\n{gate}"));
    let error = repo_config::load(repo.path()).expect_err("invalid gate value must be rejected");
    format!("{error:#}")
}

fn invalid_gate_enum_values_are_rejected() {
    let scope_error = gate_parse_error(concat!(
        "  - id: invalid-scope\n",
        "    type: check\n",
        "    command: repo-config validate\n",
        "    kind: rhino-cli\n",
        "    surfaces:\n",
        "      pre-push: { scope: sometimes }\n",
    ));
    assert!(
        scope_error.contains("invalid-scope"),
        "an invalid gate scope must name the nearest gate id; got: {scope_error}"
    );
    assert!(scope_error.contains("unknown variant `sometimes`"));
    assert!(scope_error.contains("affected-file-type"));
    assert!(scope_error.contains("all-file-type"));
    assert!(scope_error.contains("affected-projects"));
    assert!(scope_error.contains("all-projects"));
    assert!(scope_error.contains("other"));
    assert!(scope_error.contains("path-gated"));

    let type_error = gate_parse_error(concat!(
        "  - id: invalid-type\n",
        "    type: cleanup\n",
        "    command: repo-config validate\n",
        "    kind: rhino-cli\n",
        "    surfaces:\n",
        "      pre-push: { scope: all-file-type }\n",
    ));
    assert!(type_error.contains("unknown variant `cleanup`"));
    assert!(type_error.contains("check"));
    assert!(type_error.contains("mutation"));
}

fn mutation_gate_wiring_is_rejected() {
    let repo = TempDir::new().expect("temp repo");
    write(
        repo.path(),
        "repo-config.yml",
        concat!(
            "harness:\n",
            "  - name: claude-code\n",
            "    tier: source\n",
            "coverage:\n",
            "  projects:\n",
            "    - name: rhino-cli\n",
            "      levels: [unit]\n",
            "      specs: specs/apps/rhino/behavior/rhino-cli/**\n",
            "gates:\n",
            "  - id: invalid-mutation-wiring\n",
            "    type: mutation\n",
            "    command: harness bindings generate\n",
            "    kind: rhino-cli\n",
            "    wiring: matrix\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
        ),
    );

    let mut output = Vec::new();
    let result = repo_config_validate::run_at_root(repo.path(), &mut output);
    let output = String::from_utf8_lossy(&output);
    assert!(
        result.is_err(),
        "a type: mutation gate declaring wiring: matrix must be rejected by repo-config validate; output: {output}"
    );
    assert!(
        output.contains("gates[0] (gate id \"invalid-mutation-wiring\").wiring"),
        "the wiring finding must identify its gate; output: {output}"
    );
    assert!(output.contains("type \"check\""));
    assert!(output.contains("type \"mutation\""));
}

fn check_gate_wiring_is_accepted() {
    let repo = TempDir::new().expect("temp repo");
    write(
        repo.path(),
        "repo-config.yml",
        concat!(
            "harness:\n",
            "  - name: claude-code\n",
            "    tier: source\n",
            "coverage:\n",
            "  projects:\n",
            "    - name: rhino-cli\n",
            "      levels: [unit]\n",
            "      specs: specs/apps/rhino/behavior/rhino-cli/**\n",
            "gates:\n",
            "  - id: valid-check-wiring\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    wiring: matrix\n",
            "    surfaces:\n",
            "      pre-push: { scope: affected-projects }\n",
        ),
    );

    let mut output = Vec::new();
    let result = repo_config_validate::run_at_root(repo.path(), &mut output);
    assert!(
        result.is_ok(),
        "a type: check gate declaring wiring: matrix must pass repo-config validate; output: {}",
        String::from_utf8_lossy(&output)
    );
}

fn restages_and_carve_out_require_their_applicable_gate_types() {
    let restages_repo = TempDir::new().expect("temp repo");
    write(
        restages_repo.path(),
        "repo-config.yml",
        concat!(
            "harness:\n",
            "  - name: claude-code\n",
            "    tier: source\n",
            "coverage:\n",
            "  projects:\n",
            "    - name: rhino-cli\n",
            "      levels: [unit]\n",
            "      specs: specs/apps/rhino/behavior/rhino-cli/**\n",
            "gates:\n",
            "  - id: invalid-check-restages\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    restages: true\n",
            "    surfaces:\n",
            "      pre-push: { scope: affected-projects }\n",
        ),
    );
    let mut restages_output = Vec::new();
    let restages_result =
        repo_config_validate::run_at_root(restages_repo.path(), &mut restages_output);

    let carve_out_repo = TempDir::new().expect("temp repo");
    write(
        carve_out_repo.path(),
        "repo-config.yml",
        concat!(
            "harness:\n",
            "  - name: claude-code\n",
            "    tier: source\n",
            "coverage:\n",
            "  projects:\n",
            "    - name: rhino-cli\n",
            "      levels: [unit]\n",
            "      specs: specs/apps/rhino/behavior/rhino-cli/**\n",
            "gates:\n",
            "  - id: invalid-mutation-carve-out\n",
            "    type: mutation\n",
            "    command: harness bindings generate\n",
            "    kind: rhino-cli\n",
            "    carve-out: staged-only\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
        ),
    );
    let mut carve_out_output = Vec::new();
    let carve_out_result =
        repo_config_validate::run_at_root(carve_out_repo.path(), &mut carve_out_output);

    assert!(
        restages_result.is_err() && carve_out_result.is_err(),
        "type: check with restages: true and type: mutation with carve-out: staged-only must both be rejected by repo-config validate; restages output: {}; carve-out output: {}",
        String::from_utf8_lossy(&restages_output),
        String::from_utf8_lossy(&carve_out_output)
    );
    assert!(
        String::from_utf8_lossy(&restages_output)
            .contains("gates[0] (gate id \"invalid-check-restages\").restages")
    );
    assert!(String::from_utf8_lossy(&restages_output).contains("type \"mutation\""));
    assert!(String::from_utf8_lossy(&restages_output).contains("type \"check\""));
    assert!(
        String::from_utf8_lossy(&carve_out_output)
            .contains("gates[0] (gate id \"invalid-mutation-carve-out\").carve-out")
    );
    assert!(String::from_utf8_lossy(&carve_out_output).contains("type \"check\""));
    assert!(String::from_utf8_lossy(&carve_out_output).contains("type \"mutation\""));
}

fn restages_and_carve_out_are_accepted_for_their_applicable_gate_types() {
    let restages_repo = TempDir::new().expect("temp repo");
    write(
        restages_repo.path(),
        "repo-config.yml",
        concat!(
            "harness:\n",
            "  - name: claude-code\n",
            "    tier: source\n",
            "coverage:\n",
            "  projects:\n",
            "    - name: rhino-cli\n",
            "      levels: [unit]\n",
            "      specs: specs/apps/rhino/behavior/rhino-cli/**\n",
            "gates:\n",
            "  - id: valid-mutation-restages\n",
            "    type: mutation\n",
            "    command: harness bindings generate\n",
            "    kind: rhino-cli\n",
            "    restages: true\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
        ),
    );
    let mut restages_output = Vec::new();
    let restages_result =
        repo_config_validate::run_at_root(restages_repo.path(), &mut restages_output);

    let carve_out_repo = TempDir::new().expect("temp repo");
    write(
        carve_out_repo.path(),
        "repo-config.yml",
        concat!(
            "harness:\n",
            "  - name: claude-code\n",
            "    tier: source\n",
            "coverage:\n",
            "  projects:\n",
            "    - name: rhino-cli\n",
            "      levels: [unit]\n",
            "      specs: specs/apps/rhino/behavior/rhino-cli/**\n",
            "gates:\n",
            "  - id: valid-check-carve-out\n",
            "    type: check\n",
            "    command: env staged-guard validate\n",
            "    kind: rhino-cli\n",
            "    carve-out: staged-only\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
        ),
    );
    let mut carve_out_output = Vec::new();
    let carve_out_result =
        repo_config_validate::run_at_root(carve_out_repo.path(), &mut carve_out_output);

    assert!(
        restages_result.is_ok() && carve_out_result.is_ok(),
        "mutation restages and check carve-out must pass repo-config validate; restages output: {}; carve-out output: {}",
        String::from_utf8_lossy(&restages_output),
        String::from_utf8_lossy(&carve_out_output)
    );
}

fn duplicate_gate_ids_are_rejected() {
    let repo = TempDir::new().expect("temp repo");
    write(
        repo.path(),
        "repo-config.yml",
        concat!(
            "harness:\n",
            "  - name: claude-code\n",
            "    tier: source\n",
            "coverage:\n",
            "  projects:\n",
            "    - name: rhino-cli\n",
            "      levels: [unit]\n",
            "      specs: specs/apps/rhino/behavior/rhino-cli/**\n",
            "gates:\n",
            "  - id: duplicate-gate\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      pre-push: { scope: affected-projects }\n",
            "  - id: duplicate-gate\n",
            "    type: check\n",
            "    command: test:unit\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      ci: { scope: affected-projects }\n",
        ),
    );

    let mut output = Vec::new();
    let result = repo_config_validate::run_at_root(repo.path(), &mut output);
    assert!(
        result.is_err(),
        "duplicate gate ids must be rejected by repo-config validate; output: {}",
        String::from_utf8_lossy(&output)
    );
    assert!(String::from_utf8_lossy(&output).contains("gates[1].id"));
    assert!(String::from_utf8_lossy(&output).contains("duplicate-gate"));
}

fn unique_gate_ids_are_accepted() {
    let repo = TempDir::new().expect("temp repo");
    write(
        repo.path(),
        "repo-config.yml",
        concat!(
            "harness:\n",
            "  - name: claude-code\n",
            "    tier: source\n",
            "coverage:\n",
            "  projects:\n",
            "    - name: rhino-cli\n",
            "      levels: [unit]\n",
            "      specs: specs/apps/rhino/behavior/rhino-cli/**\n",
            "gates:\n",
            "  - id: test-quick\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      pre-push: { scope: affected-projects }\n",
            "  - id: test-unit\n",
            "    type: check\n",
            "    command: test:unit\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      ci: { scope: affected-projects }\n",
        ),
    );

    let mut output = Vec::new();
    let result = repo_config_validate::run_at_root(repo.path(), &mut output);
    assert!(
        result.is_ok(),
        "unique gate ids must pass repo-config validate; output: {}",
        String::from_utf8_lossy(&output)
    );
}

fn gates_require_at_least_one_surface() {
    let repo = TempDir::new().expect("temp repo");
    write(
        repo.path(),
        "repo-config.yml",
        concat!(
            "harness:\n",
            "  - name: claude-code\n",
            "    tier: source\n",
            "coverage:\n",
            "  projects:\n",
            "    - name: rhino-cli\n",
            "      levels: [unit]\n",
            "      specs: specs/apps/rhino/behavior/rhino-cli/**\n",
            "gates:\n",
            "  - id: no-surfaces\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces: {}\n",
        ),
    );

    let mut output = Vec::new();
    let result = repo_config_validate::run_at_root(repo.path(), &mut output);
    assert!(
        result.is_err(),
        "a gate with surfaces: {{}} must be rejected by repo-config validate; output: {}",
        String::from_utf8_lossy(&output)
    );
    assert!(String::from_utf8_lossy(&output).contains("no-surfaces"));
    assert!(String::from_utf8_lossy(&output).contains("at least one surface is required"));
}

fn non_empty_surfaces_are_accepted() {
    let repo = TempDir::new().expect("temp repo");
    write(
        repo.path(),
        "repo-config.yml",
        concat!(
            "harness:\n",
            "  - name: claude-code\n",
            "    tier: source\n",
            "coverage:\n",
            "  projects:\n",
            "    - name: rhino-cli\n",
            "      levels: [unit]\n",
            "      specs: specs/apps/rhino/behavior/rhino-cli/**\n",
            "gates:\n",
            "  - id: one-surface\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      pre-push: { scope: affected-projects }\n",
        ),
    );

    let mut output = Vec::new();
    let result = repo_config_validate::run_at_root(repo.path(), &mut output);
    assert!(
        result.is_ok(),
        "a gate with one surface must pass repo-config validate; output: {}",
        String::from_utf8_lossy(&output)
    );
}

#[tokio::main]
async fn main() {
    if run_selected_extraction_regression() {
        return;
    }
    website_prefix_exclusions_are_runtime_config();
    gates_section_deserializes_gate_entries();
    invalid_gate_enum_values_are_rejected();
    mutation_gate_wiring_is_rejected();
    check_gate_wiring_is_accepted();
    restages_and_carve_out_require_their_applicable_gate_types();
    restages_and_carve_out_are_accepted_for_their_applicable_gate_types();
    duplicate_gate_ids_are_rejected();
    unique_gate_ids_are_accepted();
    gates_require_at_least_one_surface();
    non_empty_surfaces_are_accepted();
    RepoConfigDataWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/repo-config")
        .canonicalize()
        .expect("feature dir resolvable")
}
