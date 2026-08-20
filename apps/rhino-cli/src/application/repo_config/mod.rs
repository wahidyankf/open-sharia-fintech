//! `repo-config.yml` loader — unified repository configuration.
//!
//! Parses the top-level sections relevant to rhino-cli's spec coverage and
//! structure validators. The file lives at the repo root and its section schema
//! is byte-identical across both parity repos (ose-public, ose-private); only the
//! per-repo values differ.

use std::collections::BTreeMap;
use std::fs;
use std::io;
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
    /// Binding tier: `"source"` or `"generated"`.
    pub tier: Tier,
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
    /// Config file path this entry declares, e.g. `.codex/config.toml`.
    #[serde(default)]
    pub config: Option<String>,
    /// Directory that must NOT exist, for a harness whose absence is itself
    /// the invariant being validated.
    #[serde(rename = "forbid-dir", default)]
    pub forbid_dir: Option<String>,
    /// Thin-pointer file to check for no-shadowing.
    #[serde(default)]
    pub shadow: Option<String>,
    /// Instruction surfaces this harness reads (for instruction-size budgeting).
    #[serde(default)]
    pub instruction: Vec<String>,
    /// Catalog facts rendered into the generated region of the platform-binding
    /// catalog document.
    ///
    /// Optional so a registry entry can exist before its catalog row is written,
    /// but `harness catalog generate` fails on an entry that lacks one: a
    /// silently-skipped harness would produce a catalog that is complete-looking
    /// and wrong, which is the exact failure generation exists to prevent.
    #[serde(default)]
    pub catalog: Option<CatalogEntry>,
    /// Ownership class for every binding path this entry claims.
    ///
    /// A binding file that belongs to no declared class is the defect this field
    /// exists to make impossible: `.opencode/skills/` sat in a binding directory
    /// for months owned by nobody, generated by nothing, and excluded from the
    /// word budget by a comment. There are exactly three classes and no fourth.
    #[serde(default)]
    pub ownership: Vec<OwnershipEntry>,
}

/// The two — and only two — binding tiers a harness entry may declare.
///
/// Represented as an enum rather than a string — the same pattern
/// [`OwnershipClass`] already uses, and the more safety-critical of the two:
/// `guard_emitter_targets` treats any tier value that is not exactly
/// `Tier::Generated` as "no guard needed", so with a bare `String` field a
/// single-character typo (`"generatd"`) silently disabled the guard instead of
/// failing to parse. A fourth — well, third — value is now a hard
/// deserialization error at the schema boundary.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize, Default)]
#[serde(rename_all = "lowercase")]
pub enum Tier {
    /// Hand-authored canonical input; the emitter must never write to it.
    Source,
    /// Emitted by `harness bindings generate`; must reproduce byte-for-byte.
    ///
    /// The struct-level `Default` derive on [`HarnessEntry`] needs some
    /// variant to fall back to even though `tier` is a required YAML key with
    /// no `#[serde(default)]` of its own; `Generated` is picked because it is
    /// the guarded variant — a struct built via `Default::default()` in a test
    /// still trips `guard_emitter_targets` rather than silently bypassing it.
    #[default]
    Generated,
}

impl Tier {
    /// Registry spelling of this tier, for findings and reports.
    #[must_use]
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Source => "source",
            Self::Generated => "generated",
        }
    }
}

/// The three — and only three — ownership classes a binding path may carry.
///
/// Represented as an enum rather than a string so a fourth value is a hard
/// deserialization error at the schema boundary rather than a semantic check
/// someone can forget to call.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum OwnershipClass {
    /// Emitted by `harness bindings generate`; must reproduce byte-for-byte.
    Generated,
    /// Third-party payload with no in-repo source; must survive regeneration
    /// untouched. Requires a `reason`.
    Vendored,
    /// Hand-authored canonical input; the emitter must never write to it.
    Source,
}

impl OwnershipClass {
    /// Registry spelling of this class, for findings and reports.
    #[must_use]
    pub const fn as_str(self) -> &'static str {
        match self {
            Self::Generated => "generated",
            Self::Vendored => "vendored",
            Self::Source => "source",
        }
    }
}

/// One harness's row in the generated platform-binding catalog table.
///
/// Every field is a rendered markdown cell rather than a structured fact.
/// Cells carry inline code spans and footnote references (`[^mcp]`), so the
/// registry holds the exact text the table shows. Deriving the markup instead
/// would put a second formatter between the registry and the document, and the
/// two could disagree — the drift this generation exists to eliminate.
///
/// Footnote *definitions* stay in the hand-authored prose outside the generated
/// region. A cell references one; the emitter does not own its text.
#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct CatalogEntry {
    /// Display name in the first column (e.g. `"OpenAI Codex CLI"`).
    pub platform: String,
    /// Whether the harness reads root `AGENTS.md` natively.
    #[serde(rename = "reads-agents-md")]
    pub reads_agents_md: String,
    /// Tool-specific instruction surface.
    #[serde(rename = "instruction-surface")]
    pub instruction_surface: String,
    /// Project-scoped MCP configuration path.
    #[serde(rename = "mcp-config")]
    pub mcp_config: String,
    /// Custom-agent surface.
    #[serde(rename = "agent-surface")]
    pub agent_surface: String,
    /// Skills surface.
    #[serde(rename = "skills-surface")]
    pub skills_surface: String,
    /// Support status.
    pub status: String,
}

/// One binding path and the class that owns it.
#[derive(Debug, Clone, Deserialize)]
#[serde(deny_unknown_fields)]
pub struct OwnershipEntry {
    /// Repository-relative path (a file, or a directory prefix ending in `/`).
    pub path: String,
    /// Which of the three classes owns this path.
    pub class: OwnershipClass,
    /// Why this path carries its class. Required for `vendored`, where the
    /// class is an exemption from regeneration and an unexplained exemption is
    /// indistinguishable from an oversight someone silenced.
    #[serde(default)]
    pub reason: Option<String>,
}

impl HarnessEntry {
    /// `true` when this is a source tier entry with an agent directory.
    pub fn is_source_with_agents(&self) -> bool {
        self.tier == Tier::Source && self.agent_dir.is_some()
    }

    /// `true` when this is a generated tier entry with an agent directory.
    pub fn is_generated_with_agents(&self) -> bool {
        self.tier == Tier::Generated && self.agent_dir.is_some()
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
/// Also rejects a leading `Component::CurDir` (`./`). Not for lexical safety —
/// `./a/b` cannot escape the repository — but because `Path::starts_with`
/// disagrees with `Path::components()` equality on it: `Path::new("./a/b")`
/// and `Path::new("a/b")` denote the same location, yet
/// `Path::new("./a/b").starts_with("a")` and `Path::new("a/b").starts_with("./a")`
/// are both `false`. A `./`-prefixed registry value therefore silently defeats
/// every [`path_is_under`] cross-check that compares it against an
/// un-prefixed path, passing `repo-config validate` while disabling the
/// ownership cross-check it should have participated in. Rejecting is
/// preferable to normalizing: the registry is hand-authored, and this repo's
/// stated preference is explicit configuration over implicit convention.
///
/// # Errors
///
/// Returns an error when the path is empty, absolute, contains a parent
/// directory component, or contains a `./` current-directory component.
pub fn validate_repo_relative_path(value: &str) -> Result<(), String> {
    let path = Path::new(value);
    if value.is_empty() || path.is_absolute() {
        return Err("must be a non-empty repository-relative path".to_string());
    }
    if path.components().any(|component| {
        matches!(
            component,
            Component::ParentDir | Component::RootDir | Component::Prefix(_) | Component::CurDir
        )
    }) {
        return Err(
            "must not contain an absolute, parent-directory, or ./ current-directory component"
                .to_string(),
        );
    }
    Ok(())
}

/// `true` when `path` lies at or under `dir`, compared component-wise via
/// [`Path::starts_with`] rather than by string prefix.
///
/// A string-prefix test disagrees with this on a doubled separator: Rust's
/// `Path::components()` collapses `a//b` to the same components as `a/b`, but
/// `"a//b".starts_with("a/")` is `false`. Three call sites used to compute
/// this independently and could disagree on exactly that input, which let a
/// declared-vendored path silently escape a cross-check that is supposed to
/// keep it from being deleted (cycle-2 Finding 10): the C2 ownership
/// cross-check in `repo_config_validate.rs`, the skills-mirror emitter's
/// vendored-skip test in `skills_mirror.rs`, and `ownership.rs::claims()`
/// (a third, string-prefix implementation, unified onto this one in cycle 3).
/// This is now the crate's one shared implementation; `validate_repo_relative_path`
/// additionally rejects a `./`-prefixed registry value outright, because
/// normalizing it here would not help a caller that never routes through this
/// function.
#[must_use]
pub fn path_is_under<P: AsRef<Path>, D: AsRef<Path>>(path: P, dir: D) -> bool {
    path.as_ref().starts_with(dir.as_ref())
}

/// Resolve a configured repository-relative path while proving that existing
/// path components do not escape `repo_root` through symlinks.
///
/// Missing final components are allowed: the caller may use the returned path
/// to report an absent optional configuration file. The nearest existing
/// ancestor is still canonicalized, which catches a symlinked intermediate
/// directory that points outside the repository.
///
/// Returns the **canonicalized** destination — `canonical_ancestor` joined
/// with the unresolved (necessarily nonexistent, so nothing left to resolve)
/// remaining suffix — not the lexical `repo_root.join(value)`. A caller that
/// re-checks `result.starts_with(repo_root)` as defense in depth is checking
/// something real: the un-canonicalized `repo_root.join(value)` would always
/// start with `repo_root` by construction, which made an earlier version of
/// that re-check a tautology that could never fail, documented as a live
/// safety net it did not provide.
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
    // `existing_ancestor` came from `candidate.ancestors()`, so this can never
    // fail — but a fallible path is cheaper to keep correct than a documented
    // panic, and it needs no `# Panics` section.
    let remaining = candidate
        .strip_prefix(existing_ancestor)
        .map_err(|_| Error::msg("configured path ancestor is not a prefix of itself"))?;
    Ok(canonical_ancestor.join(remaining))
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
    /// Where the generated platform-binding catalog lands, and the date its
    /// claims were last verified against upstream.
    #[serde(rename = "harness-catalog", default)]
    pub harness_catalog: Option<HarnessCatalog>,
}

/// Document-level settings for the generated platform-binding catalog.
///
/// Separate from the per-harness `catalog:` blocks because these are facts about
/// the *document*, not about any one harness. Folding `verified` into the harness
/// entries would give one stamp three sources that could disagree.
#[derive(Debug, Clone, Deserialize, PartialEq, Eq)]
#[serde(deny_unknown_fields)]
pub struct HarnessCatalog {
    /// Repository-relative path of the catalog document.
    pub document: String,
    /// Date the catalog's upstream claims were last verified, rendered into the
    /// generated region as the verification stamp. Declared rather than stamped
    /// at generation time: a generated timestamp would change on every run and
    /// make the drift guard fire on its own output.
    pub verified: String,
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
    parse_repo_config(&data, &path)
}

/// Load `repo-config.yml` at `repo_root`, discriminating "no entry exists at
/// this path at all" from every other failure to stat, read, or parse it.
///
/// Returns `Ok(None)` **only** when [`fs::symlink_metadata`] itself reports
/// [`io::ErrorKind::NotFound`] — the one case that legitimately means "no
/// registry declared". Deliberately `symlink_metadata`, not `Path::exists()`
/// or a `read_to_string`-only check: both of those follow a symlink and
/// therefore report a **dangling** symlink identically to a genuinely absent
/// path (a `read_to_string` on a dangling symlink fails with the same
/// `NotFound` a missing path would). `symlink_metadata` stats the link entry
/// itself, so a dangling symlink is correctly seen as "something is declared
/// here" and its subsequent read failure propagates as `Err` instead of
/// silently taking the default branch. A permission-denied ancestor directory
/// and a present-but-unparseable file also return `Err`, for the same reason:
/// only a confirmed-absent path may fall back to `RepoConfig::default()`.
///
/// # Errors
///
/// Returns an error when an entry exists at the path but cannot be statted,
/// cannot be read, or is not valid YAML.
pub fn load_optional(repo_root: &Path) -> Result<Option<RepoConfig>, Error> {
    let path = repo_root.join("repo-config.yml");
    match fs::symlink_metadata(&path) {
        Ok(_) => {}
        Err(error) if error.kind() == io::ErrorKind::NotFound => return Ok(None),
        Err(error) => {
            return Err(Error::new(error)
                .context(format!("cannot stat repo-config.yml at {}", path.display())));
        }
    }
    let data = fs::read_to_string(&path)
        .with_context(|| format!("cannot read repo-config.yml at {}", path.display()))?;
    parse_repo_config(&data, &path).map(Some)
}

/// Parses `data` (the contents of `repo-config.yml` at `path`, used only for
/// error context) into a [`RepoConfig`], enriching a `gates[index]` schema
/// error with the offending gate's `id` when one can be recovered.
fn parse_repo_config(data: &str, path: &Path) -> Result<RepoConfig, Error> {
    serde_norway::from_str(data)
        .map_err(|error| {
            let parse_error = error.to_string();
            if let Some(gate_id) = gate_id_from_parse_error(data, &parse_error) {
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

    // Regression for the thread-12 fix: a `./`-prefixed registry value used to
    // pass validation and then silently defeat `path_is_under` (`Path::new("./a/b")
    // .starts_with("a")` is `false`), which let a declared-vendored path
    // silently escape the C2 ownership cross-check — the same failure mode as
    // cycle-2 Finding 10, reopened through normalization instead of doubled
    // separators.
    #[test]
    fn validate_repo_relative_path_rejects_a_current_dir_prefixed_value() {
        // `Path::components()` only ever preserves `CurDir` for a LEADING
        // `./` — an interior or trailing `.` (e.g. `agents/./skills`) is
        // silently normalized away by Rust's own parser before this function
        // ever sees a component to reject, so only the leading form is a real
        // input to guard against.
        for path in ["./agents/skills", "./a"] {
            assert!(
                validate_repo_relative_path(path).is_err(),
                "./-prefixed configured path {path:?} must be rejected, not silently accepted \
                 and left to defeat path_is_under downstream"
            );
        }
    }

    #[test]
    fn path_is_under_disagrees_with_a_naive_prefix_test_on_a_current_dir_component() {
        // Documents exactly why validate_repo_relative_path must reject `./`
        // outright rather than relying on path_is_under to handle it: the two
        // spellings of the identical location do not satisfy Path::starts_with
        // against each other in either direction.
        assert!(!path_is_under(Path::new("./a/b"), Path::new("a")));
        assert!(!path_is_under(Path::new("a/b"), Path::new("./a")));
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

    // Regression for the thread-11 fix: `confined_repo_path` used to prove the
    // destination was safe via `canonical_ancestor`, then discard that proof
    // and return the un-canonicalized lexical join instead. Every caller's
    // `result.starts_with(repo_root)` "defense in depth" re-check therefore
    // compared `repo_root.join(rel)` against `repo_root` — which can never be
    // false — a tautology presented as a live safety net. The returned path
    // must now be the canonicalized one actually proven safe.
    #[cfg(unix)]
    #[test]
    fn confined_repository_path_returns_the_canonicalized_destination_not_the_lexical_join() {
        use std::os::unix::fs::symlink;

        let outer = tempfile::tempdir().expect("create outer directory");
        std::fs::create_dir(outer.path().join("sub")).expect("create sub directory");
        let parent = tempfile::tempdir().expect("create symlink parent");
        let root_link = parent.path().join("root-link");
        symlink(outer.path(), &root_link).expect("create root symlink");

        let resolved = confined_repo_path(&root_link, "sub/missing-file.txt")
            .expect("a symlinked root resolving inside itself must succeed");

        let canonical_outer = outer.path().canonicalize().expect("canonicalize outer");
        assert_eq!(
            resolved,
            canonical_outer.join("sub/missing-file.txt"),
            "must return the canonicalized destination, not repo_root.join(value)"
        );
        assert!(
            !resolved.starts_with(&root_link),
            "the canonicalized result must not retain the symlinked root component, or a \
             caller's starts_with(repo_root) re-check against the raw root stays a tautology"
        );
    }
}
