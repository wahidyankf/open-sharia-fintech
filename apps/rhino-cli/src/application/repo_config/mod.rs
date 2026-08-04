//! `repo-config.yml` loader — unified repository configuration.
//!
//! Parses the top-level sections relevant to rhino-cli's spec coverage and
//! structure validators. The file lives at the repo root and its section schema
//! is byte-identical across all three repos (ose-public, ose-primer, ose-private);
//! only the per-repo values differ.

use std::collections::BTreeMap;
use std::fs;
use std::path::Path;

use anyhow::{Context, Error};
use serde::Deserialize;

use crate::application::env::injection::Manifest as EnvInjectionManifest;
use crate::application::env::validate::Contract as EnvContract;
use crate::application::repo_governance::instruction_size::BudgetConfig;

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
    /// Source agent-dir this entry must mirror (generated tier).
    #[serde(default)]
    pub mirrors: Option<String>,
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
    /// Paths that activate a path-gated scope.
    #[serde(default)]
    pub trigger: Vec<String>,
}

/// The `doctor:` section of `repo-config.yml`.
#[derive(Debug, Clone, Deserialize, Default)]
#[serde(deny_unknown_fields)]
pub struct DoctorConfig {
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
    /// Per-surface instruction-file size budgets (was `instruction-size-budget.yaml`).
    #[serde(rename = "instruction-size", default)]
    pub instruction_size: Option<BudgetConfig>,
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
    use crate::internal::git;
    use crate::test_support::CwdLock;

    // Regression: this test used to hard-assert repo-specific domain literals
    // ("organiclever", "ose-be", ...), which only hold in ose-public's own
    // repo-config.yml — it failed immediately once rhino-cli's byte-identical
    // source ran against ose-primer's own repo-config.yml data. `ddd-areas`
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
}
