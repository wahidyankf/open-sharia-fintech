//! `repo-config.yml` loader — unified repository configuration.
//!
//! Parses the top-level sections relevant to rhino-cli's spec coverage and
//! structure validators. The file lives at the repo root and its section schema
//! is byte-identical across both parity repos (ose-public, ose-private); only the
//! per-repo values differ.

use std::collections::BTreeMap;
use std::fs;
use std::path::{Component, Path, PathBuf};

use anyhow::{Context, Error};
use serde::Deserialize;

use crate::application::env::injection::Manifest as EnvInjectionManifest;
use crate::application::env::validate::Contract as EnvContract;
use crate::application::governance::word_budget::BudgetConfig;

/// A project entry in the `coverage.projects` list.
#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct CoverageProject {
    /// Nx project name (e.g. `"rhino-cli"`).
    pub name: String,
    /// Test levels this project runs at (`"unit"`, `"integration"`, `"e2e"`).
    pub levels: Vec<String>,
    /// Feature-file glob this project owns (surface-precise for apps; per-project for libs).
    pub specs: String,
}

/// The `coverage:` section of `repo-config.yml`.
#[derive(Debug, Clone, Deserialize, Default)]
#[serde(deny_unknown_fields)]
pub struct CoverageConfig {
    /// Explicit per-project test-level registry.
    pub projects: Vec<CoverageProject>,
}

/// The `specs:` section of `repo-config.yml`.
#[derive(Debug, Clone, Deserialize, Default)]
#[serde(deny_unknown_fields)]
pub struct SpecsConfig {
    /// Spec areas that must carry a `ddd/` folder. This is the single source of
    /// truth for DDD areas — validators read it here instead of a source-hard-coded
    /// per-repo allowlist. An area absent from this list must NOT carry `ddd/`.
    #[serde(rename = "ddd-areas", default)]
    pub ddd_areas: Vec<String>,
    /// Projects eligible for `specs:domain:coverage`. Distinct from `ddd-areas` —
    /// a project can be in one without being in the other.
    #[serde(rename = "domain-areas", default)]
    pub domain_areas: Vec<String>,
}

/// One harness entry in the `harness:` section of `repo-config.yml`.
#[derive(Debug, Clone, Deserialize, Default)]
#[serde(deny_unknown_fields)]
pub struct HarnessEntry {
    /// Harness identifier (e.g. `"claude-code"`, `"opencode"`, `"amazonq"`).
    pub name: String,
    /// Binding tier: `"source"`, `"generated"`, `"source-config"`, or `"native"`.
    pub tier: String,
    /// Directory of per-agent files (present for `source` and `generated` tiers).
    #[serde(rename = "agent-dir", default)]
    pub agent_dir: Option<String>,
    /// Directory of skill files (present for `source` tier only).
    #[serde(rename = "skills-dir", default)]
    pub skills_dir: Option<String>,
    /// Directory of injected rules files (generated tier only).
    #[serde(rename = "rules-dir", default)]
    pub rules_dir: Option<String>,
    /// Generated default-agent name (present for generated harnesses that
    /// materialize a named agent definition).
    #[serde(rename = "agent-name", default)]
    pub agent_name: Option<String>,
    /// Source agent-dir this entry must mirror (generated tier).
    #[serde(default)]
    pub mirrors: Option<String>,
    /// Source skills-dir that `skills-dir` must mirror (generated tier).
    ///
    /// Declared rather than inferred: the emitter reads its input tree from the
    /// registry, so a harness whose skills live somewhere other than
    /// `.claude/skills` is a config change, not a source edit (DD-2).
    #[serde(rename = "skills-mirrors", default)]
    pub skills_mirrors: Option<String>,
    /// Directories inside this entry's mirrored trees that the emitter must never
    /// write, delete, or regenerate.
    ///
    /// These are third-party plugin payloads committed to the repository with no
    /// counterpart in the source tree. Ownership is DECLARED here rather than
    /// inferred from "has no counterpart", because an inference would silently
    /// delete any genuinely stale mirror directory it could not explain (DD-7).
    #[serde(default)]
    pub vendored: Vec<String>,
    /// Config file path (source-config tier).
    #[serde(default)]
    pub config: Option<String>,
    /// Directory that must NOT exist (source-config tier).
    #[serde(rename = "forbid-dir", default)]
    pub forbid_dir: Option<String>,
    /// Thin-pointer file to check for no-shadowing (native tier).
    #[serde(default)]
    pub shadow: Option<String>,
    /// Instruction surfaces this harness reads (for instruction-size budgeting).
    #[serde(default)]
    pub instruction: Vec<String>,
}

impl HarnessEntry {
    /// `true` when this is a source tier entry with an agent directory.
    pub fn is_source_with_agents(&self) -> bool {
        self.tier == "source" && self.agent_dir.is_some()
    }

    /// `true` when this is a generated tier entry with an agent directory.
    pub fn is_generated_with_agents(&self) -> bool {
        self.tier == "generated" && self.agent_dir.is_some()
    }

    /// `true` when this entry is the harness the caller named.
    ///
    /// The single place a `--harness <name>` argument is matched against the
    /// registry, so the accepted set is always exactly what `repo-config.yml`
    /// declares rather than a source-hard-coded literal list.
    pub fn matches_name(&self, name: &str) -> bool {
        self.name == name
    }
}

/// Whether a gate validates or mutates repository content.
#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "kebab-case")]
pub enum GateType {
    /// A non-mutating validation gate.
    Check,
    /// A gate that changes repository content.
    Mutation,
}

/// Command runner for a gate.
#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "kebab-case")]
pub enum GateKind {
    /// A command implemented by rhino-cli.
    RhinoCli,
    /// A command available on `PATH`.
    External,
    /// An Nx target.
    Nx,
}

/// Execution wiring for a check gate.
#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "kebab-case")]
pub enum GateWiring {
    /// Emit one CI job for this gate.
    Matrix,
    /// A workflow declares this gate directly.
    HandWired,
}

/// A composition-rule exemption for a gate.
#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "kebab-case")]
pub enum GateCarveOut {
    /// The check reads the Git index and therefore has no CI counterpart.
    StagedOnly,
}

/// A gate execution surface.
#[derive(Debug, Clone, Deserialize, PartialEq, Eq, PartialOrd, Ord)]
#[serde(rename_all = "kebab-case")]
pub enum GateSurface {
    /// The commit-message hook.
    CommitMsg,
    /// The pre-commit hook.
    PreCommit,
    /// The pre-push hook.
    PrePush,
    /// Continuous integration.
    Ci,
}

/// The scope that determines a gate's inputs on a surface.
#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
#[serde(rename_all = "kebab-case")]
pub enum ScopeKind {
    /// Files of a matching type in the change.
    AffectedFileType,
    /// All files of a matching type in the repository.
    AllFileType,
    /// Projects affected by the change.
    AffectedProjects,
    /// Every project in the repository.
    AllProjects,
    /// Gate-specific input handling.
    Other,
    /// A check activated only by matching paths.
    PathGated,
}

/// Every tool identifier that Doctor can select from the registry.
///
/// This Rust-side inventory is the authoritative validation source for
/// per-gate `doctor-tools` metadata. Workflow configuration consumes declared
/// metadata and must not duplicate this list.
pub const DOCTOR_TOOL_INVENTORY: &[&str] = &[
    "git",
    "volta",
    "node",
    "npm",
    "rust",
    "cargo-llvm-cov",
    "dotnet",
    "docker",
    "jq",
    "shellcheck",
    "hadolint",
    "actionlint",
    "playwright",
    "shfmt",
    "tofu",
    "clang-format",
];

/// One entry in the `gates:` registry of `repo-config.yml`.
#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct GateEntry {
    /// Stable, unique gate identifier.
    pub id: String,
    /// Whether the entry checks or mutates repository content.
    #[serde(rename = "type")]
    pub gate_type: GateType,
    /// Leaf command run for this gate.
    pub command: String,
    /// Command runner (`rhino-cli`, `external`, or `nx`).
    pub kind: GateKind,
    /// Ordered Doctor tool identifiers needed before this gate can run.
    #[serde(rename = "doctor-tools", default)]
    pub doctor_tools: Vec<String>,
    /// Optional execution-wiring override for checks.
    #[serde(default)]
    pub wiring: Option<GateWiring>,
    /// Whether a mutation must re-stage its generated output.
    #[serde(default)]
    pub restages: bool,
    /// Command-specific arguments, such as exclusion lists.
    #[serde(default)]
    pub args: BTreeMap<String, Vec<String>>,
    /// Per-surface execution scopes.
    pub surfaces: BTreeMap<GateSurface, SurfaceScope>,
    /// Exemption from the cross-surface composition rule.
    #[serde(rename = "carve-out", default)]
    pub carve_out: Option<GateCarveOut>,
    /// Mutation gate verified by this check.
    #[serde(default)]
    pub verifies: Option<String>,
    /// Mutation category, such as `formatter`.
    #[serde(default)]
    pub category: Option<String>,
    /// CI job group this gate belongs to. Required for every gate whose
    /// `surfaces` includes `ci` (enforced by `gate validate`, not by this
    /// schema, since the requirement is conditional on the declared surface
    /// set); groups gates onto shared CI matrix jobs (DD-3).
    #[serde(rename = "ci-group", default)]
    pub ci_group: Option<String>,
}

/// Return registry arguments that are forwarded to the declared gate command.
///
/// Every key becomes a repeatable long option, preserving the configuration's
/// deterministic key and value ordering. `exclude` also shapes candidate-path
/// selection, but remains a fixed argument for commands that enforce their own
/// exclusion semantics.
#[must_use]
pub fn fixed_arguments(gate: &GateEntry) -> Vec<String> {
    gate.args
        .iter()
        .flat_map(|(key, values)| {
            values
                .iter()
                .flat_map(move |value| [format!("--{key}"), value.clone()])
        })
        .collect()
}

/// A gate's scope on one execution surface.
#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct SurfaceScope {
    /// Scope descriptor for the surface.
    pub scope: ScopeKind,
    /// Single file glob for an affected-file-type scope.
    #[serde(default)]
    pub glob: Option<String>,
    /// Multiple file globs for an affected-file-type scope.
    #[serde(default)]
    pub globs: Vec<String>,
    /// Optional shell command emitted instead of the default lint-staged command.
    ///
    /// The value is meaningful only for the pre-commit affected-file-type
    /// surface. When present, emitters use it verbatim, or substitute its one
    /// optional `{{command}}` marker with the rendered registry command.
    #[serde(rename = "lint-staged-shell", default)]
    pub lint_staged_shell: Option<String>,
    /// Paths that activate a path-gated scope.
    #[serde(default)]
    pub trigger: Vec<String>,
}

/// The `doctor:` section of `repo-config.yml`.
#[derive(Debug, Clone, Deserialize, Default)]
#[serde(deny_unknown_fields)]
pub struct DoctorConfig {
    /// Repository-relative `global.json` supplying the required .NET SDK
    /// version. When absent, Doctor uses the conventional root `global.json`.
    #[serde(rename = "dotnet-global-json", default)]
    pub dotnet_global_json: Option<String>,
    /// Tool names (from `doctor::tools::build_tool_defs`'s full roster) that
    /// this repo's dev workflow does not need — e.g. a formatter binary this
    /// repo's `lint-staged` config never invokes. Excluded from `doctor`'s
    /// check so a plain `doctor` run stays dormant for tools genuinely
    /// inapplicable to this repo instead of hard-failing on them. Mirrors the
    /// `specs.domain-areas` allowlist pattern: the check logic is
    /// byte-identical Rust; only this list's *values* differ per repo.
    #[serde(rename = "skip-tools", default)]
    pub skip_tools: Vec<String>,
}

/// Validate a configured repository-relative file path before it is joined to
/// a repository root. This is intentionally lexical so schema validation can
/// report unsafe configuration even when the configured file does not exist.
///
/// # Errors
///
/// Returns an error when the path is empty, absolute, or contains a parent
/// directory component.
pub fn validate_repo_relative_path(value: &str) -> Result<(), String> {
    let path = Path::new(value);
    if value.is_empty() || path.is_absolute() {
        return Err("must be a non-empty repository-relative path".to_string());
    }
    if path.components().any(|component| {
        matches!(
            component,
            Component::ParentDir | Component::RootDir | Component::Prefix(_)
        )
    }) {
        return Err("must not contain an absolute or parent-directory component".to_string());
    }
    Ok(())
}

/// Resolve a configured repository-relative path while proving that existing
/// path components do not escape `repo_root` through symlinks.
///
/// Missing final components are allowed: the caller may use the returned path
/// to report an absent optional configuration file. The nearest existing
/// ancestor is still canonicalized, which catches a symlinked intermediate
/// directory that points outside the repository.
///
/// # Errors
///
/// Returns an error when the configured path is lexically unsafe, the root or
/// nearest existing ancestor cannot be canonicalized, or that ancestor lies
/// outside the repository root.
pub fn confined_repo_path(repo_root: &Path, value: &str) -> Result<PathBuf, Error> {
    validate_repo_relative_path(value).map_err(Error::msg)?;
    let canonical_root = repo_root
        .canonicalize()
        .with_context(|| format!("canonicalize repository root {}", repo_root.display()))?;
    let candidate = repo_root.join(value);
    let existing_ancestor = candidate
        .ancestors()
        .find(|path| path.exists())
        .ok_or_else(|| Error::msg("configured path has no existing repository ancestor"))?;
    let canonical_ancestor = existing_ancestor.canonicalize().with_context(|| {
        format!(
            "canonicalize configured path ancestor {}",
            existing_ancestor.display()
        )
    })?;
    if !canonical_ancestor.starts_with(&canonical_root) {
        return Err(Error::msg(format!(
            "configured path {value:?} escapes the repository root through a symlink"
        )));
    }
    Ok(candidate)
}

/// Parsed `repo-config.yml` — the canonical schema, byte-identical across all
/// three repos. Every top-level section is modeled here, and both this struct
/// and its nested structs use `#[serde(deny_unknown_fields)]`: an unknown or
/// misspelled key fails the parse. This makes the struct itself the schema-parity
/// oracle — each repo validating its own `repo-config.yml` against its own copy of
/// this (byte-identical) struct is equivalent to an identical key set across all
/// three files. See `rhino-cli repo-config validate`.
#[derive(Debug, Clone, Deserialize, Default)]
#[serde(deny_unknown_fields)]
pub struct RepoConfig {
    /// All-harness binding registry (§3.2); every `harness` command reads this list.
    #[serde(default)]
    pub harness: Vec<HarnessEntry>,
    /// Gate registry declaring checks and mutations on every execution surface.
    #[serde(default)]
    pub gates: Vec<GateEntry>,
    /// Per-project test-level registry for the spec coverage validators.
    #[serde(default)]
    pub coverage: CoverageConfig,
    /// Spec-tree structure configuration for `specs:structure-validation`.
    #[serde(default)]
    pub specs: SpecsConfig,
    /// Per-surface instruction-file word budgets (was `instruction-size:`).
    #[serde(rename = "governance-word-budget", default)]
    pub governance_word_budget: Option<BudgetConfig>,
    /// Surface registry for `env validate` (code↔config drift detection).
    #[serde(rename = "env-contract", default)]
    pub env_contract: Option<EnvContract>,
    /// Value-less injection manifest for `env validate` (manifest-consistency pass).
    #[serde(rename = "env-injection", default)]
    pub env_injection: Option<EnvInjectionManifest>,
    /// Tools the `doctor` check should skip as inapplicable to this repo.
    #[serde(default)]
    pub doctor: DoctorConfig,
}

/// Load and parse `repo-config.yml` at `repo_root`.
///
/// # Errors
///
/// Returns an error when the file cannot be read or is not valid YAML.
pub fn load(repo_root: &Path) -> Result<RepoConfig, Error> {
    let path = repo_root.join("repo-config.yml");
    let data = fs::read_to_string(&path)
        .with_context(|| format!("cannot read repo-config.yml at {}", path.display()))?;
    serde_norway::from_str(&data)
        .map_err(|error| {
            let parse_error = error.to_string();
            if let Some(gate_id) = gate_id_from_parse_error(&data, &parse_error) {
                Error::msg(format!("{parse_error} (gate id {gate_id:?})"))
            } else {
                Error::msg(parse_error)
            }
        })
        .with_context(|| format!("failed to parse repo-config.yml at {}", path.display()))
}

/// Finds a gate identifier for a Serde error scoped to a `gates[index]` path.
fn gate_id_from_parse_error(data: &str, parse_error: &str) -> Option<String> {
    let index = parse_error
        .split_once("gates[")?
        .1
        .split_once(']')?
        .0
        .parse::<usize>()
        .ok()?;
    data.lines()
        .filter_map(|line| line.trim_start().strip_prefix("- id: "))
        .map(|id| id.trim().trim_matches(['\'', '"']).to_owned())
        .nth(index)
}

/// Load `repo-config.yml` at `repo_root`, returning an empty default if the file is absent or
/// cannot be parsed. Callers that need registry-driven behavior without hard failure use this.
#[must_use]
pub fn load_or_default(repo_root: &Path) -> RepoConfig {
    load(repo_root).unwrap_or_default()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::commands::repo_config_validate::gate_semantic_findings;
    use crate::internal::git;
    use crate::test_support::CwdLock;

    fn parse_gate_config(doctor_tools: Option<&str>) -> RepoConfig {
        let metadata = doctor_tools
            .map(|tools| format!("    doctor-tools: {tools}\n"))
            .unwrap_or_default();
        serde_norway::from_str(&format!(
            "gates:\n  - id: doctor-bootstrap\n    type: check\n    command: doctor\n    kind: rhino-cli\n    surfaces:\n      ci: {{ scope: other }}\n{metadata}"
        ))
        .expect("doctor-tools fixture must deserialize")
    }

    #[test]
    fn doctor_tools_metadata_is_optional_and_defaults_empty() {
        let config = parse_gate_config(None);

        assert!(config.gates[0].doctor_tools.is_empty());
        assert!(gate_semantic_findings(&config).is_empty());
    }

    #[test]
    fn doctor_tools_metadata_accepts_known_inventory_in_order() {
        let config = parse_gate_config(Some("[git, node]"));

        assert_eq!(config.gates[0].doctor_tools, ["git", "node"]);
        assert!(gate_semantic_findings(&config).is_empty());
    }

    #[test]
    fn doctor_tools_metadata_rejects_duplicates() {
        let config = parse_gate_config(Some("[git, git]"));
        let findings = gate_semantic_findings(&config);

        assert!(
            findings.iter().any(|finding| {
                finding.contains("doctor-tools")
                    && finding.contains("duplicate")
                    && finding.contains("git")
            }),
            "duplicate Doctor tools must be rejected; got: {findings:?}"
        );
    }

    #[test]
    fn doctor_tools_metadata_rejects_unknown_inventory_entries() {
        let config = parse_gate_config(Some("[not-a-doctor-tool]"));
        let findings = gate_semantic_findings(&config);

        assert!(
            findings.iter().any(|finding| {
                finding.contains("doctor-tools") && finding.contains("not-a-doctor-tool")
            }),
            "unknown Doctor tools must be rejected; got: {findings:?}"
        );
    }

    // Regression: this test used to hard-assert repo-specific domain literals
    // ("organiclever", "ose-be", ...), which only hold in ose-public's own
    // repo-config.yml — it failed immediately once rhino-cli's byte-identical
    // source ran against a sibling repo's own repo-config.yml data. `ddd-areas`
    // and `domain-areas` are legitimately empty in some repos (e.g. a scaffold
    // repo whose demo backends aren't DDD-structured), so only assert the one
    // structural property every repo's config must satisfy: at least one
    // project under test-level coverage (rhino-cli itself, at minimum).
    #[test]
    fn loads_repo_config_from_repo_root() {
        let _cwd = CwdLock::acquire();
        let repo_root = git::root::find_root().expect("must be in a git repo");
        let config = load(&repo_root).expect("repo-config.yml must be loadable");
        assert!(
            !config.coverage.projects.is_empty(),
            "coverage.projects must not be empty"
        );
    }

    #[test]
    fn coverage_project_has_correct_fields() {
        let _cwd = CwdLock::acquire();
        let repo_root = git::root::find_root().expect("must be in a git repo");
        let config = load(&repo_root).expect("repo-config.yml must be loadable");
        let rhino = config
            .coverage
            .projects
            .iter()
            .find(|p| p.name == "rhino-cli")
            .expect("rhino-cli must be in coverage.projects");
        assert!(
            rhino.levels.contains(&"unit".to_string()),
            "rhino-cli must declare unit level"
        );
        assert!(
            rhino.levels.contains(&"integration".to_string()),
            "rhino-cli must declare integration level"
        );
        assert!(
            rhino.specs.starts_with("specs/apps/rhino"),
            "rhino-cli specs glob must point to specs/apps/rhino"
        );
    }

    #[test]
    fn configured_repository_path_rejects_absolute_and_parent_components() {
        for path in [
            "/tmp/global.json",
            "../global.json",
            "tooling/../../global.json",
        ] {
            assert!(
                validate_repo_relative_path(path).is_err(),
                "unsafe configured path {path:?} must be rejected"
            );
        }
        assert!(validate_repo_relative_path("tooling/sdk/global.json").is_ok());
    }

    #[cfg(unix)]
    #[test]
    fn confined_repository_path_rejects_a_symlink_escape() {
        use std::os::unix::fs::symlink;

        let root = tempfile::tempdir().expect("create repository root");
        let outside = tempfile::tempdir().expect("create outside directory");
        symlink(outside.path(), root.path().join("tooling")).expect("create symlink escape");

        let error = confined_repo_path(root.path(), "tooling/sdk/global.json")
            .expect_err("symlinked configured path must fail");
        assert!(format!("{error:#}").contains("escapes the repository root"));
    }
}
