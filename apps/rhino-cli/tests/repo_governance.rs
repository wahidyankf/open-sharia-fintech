//! Cucumber-rs behavior tests for the `repo-governance` governance-audit
//! validators: `repo-governance vendor validate`, `repo-governance
//! layer-coherence validate`, `repo-governance traceability validate`, and
//! `repo-governance audit`.
//!
//! Wires the behavior-contract feature files at
//! `specs/apps/rhino/behavior/rhino-cli/gherkin/repo-governance/` to step
//! definitions that build an in-memory fixture via `MockFs` and call the
//! Fs-injected validator functions directly (no process spawn), asserting on
//! their typed return values.

// Test step-definition scaffolding: private World state and step fns are
// self-documenting via their #[given]/#[when]/#[then] gherkin strings.
#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]

use std::fmt::Write as _;
use std::path::PathBuf;

use cucumber::{World as _, given, then, when};
use rhino_cli::application::fs::mock::MockFs;
use rhino_cli::application::repo_governance::audit_orchestrator::{
    AuditCategoryResult, AuditEnvelope, AuditOptions, run_audit as run_governance_audit,
};
use rhino_cli::application::repo_governance::layer_coherence::{
    KIND_CROSS_FILE_NAME_MISMATCH, KIND_NUMBERING_GAP, LayerCoherenceFinding, audit_layer_coherence,
};
use rhino_cli::application::repo_governance::traceability_audit::{
    KIND_MISSING_AGENT_REFERENCE, KIND_MISSING_CONVENTIONS_IMPLEMENTED,
    KIND_MISSING_PRINCIPLES_IMPLEMENTED, KIND_MISSING_VISION_SUPPORTED, TraceabilityFinding,
    audit_traceability,
};
use rhino_cli::application::repo_governance::vendor_audit::{Finding, walk as vendor_walk};

/// Fixed absolute repo root every scenario's `MockFs` fixture is rooted at.
/// Never touches the real filesystem — every read is served by `MockFs`.
fn repo_root() -> PathBuf {
    PathBuf::from("/repo")
}

/// Shared scenario state. Each `When` step populates exactly one of the
/// `*_findings`/`audit_env` fields with the typed result of calling a single
/// Fs-injected validator against `fs`.
#[derive(cucumber::World, Debug)]
#[world(init = Self::new)]
struct GovernanceWorld {
    fs: MockFs,
    /// Repo-root-relative scan path passed to the vendor-audit `walk()` call
    /// (a file or a directory).
    target: PathBuf,
    vendor_findings: Option<Vec<Finding>>,
    layer_findings: Option<Vec<LayerCoherenceFinding>>,
    traceability_findings: Option<Vec<TraceabilityFinding>>,
    audit_env: Option<AuditEnvelope>,
    /// Captured JSON serializations from each invocation of a
    /// repeated-invocation step (the byte-determinism scenario).
    captured_runs: Vec<String>,
}

impl GovernanceWorld {
    fn new() -> Self {
        Self {
            fs: MockFs::new(),
            target: PathBuf::from("repo-governance"),
            vendor_findings: None,
            layer_findings: None,
            traceability_findings: None,
            audit_env: None,
            captured_runs: Vec::new(),
        }
    }

    /// Adds (or overwrites) a file at repo-root-relative `rel` with `content`.
    fn write(&mut self, rel: &str, content: &str) {
        let path = repo_root().join(rel);
        self.fs = std::mem::take(&mut self.fs).with_file(path, content);
    }

    /// Writes identical layer declarations to both governance layer-coherence
    /// documents (`repository-governance-architecture.md` and `README.md`) so
    /// `repo-governance layer-coherence validate` reports zero findings for
    /// them, leaving only whatever other fixtures the calling step wrote.
    fn write_matching_layer_docs(&mut self, layers: &[(u32, &str)]) {
        let doc = layer_doc(layers);
        self.write(
            "repo-governance/repository-governance-architecture.md",
            &doc,
        );
        self.write("repo-governance/README.md", &doc);
    }

    /// Runs `vendor_audit::walk` against `self.target` (resolved relative to
    /// the fixed repo root) and stores the result.
    fn run_vendor_validate(&mut self) {
        let full = repo_root().join(&self.target);
        self.vendor_findings =
            Some(vendor_walk(&self.fs, &full).expect("vendor walk succeeds against MockFs"));
    }

    /// Runs `layer_coherence::audit_layer_coherence` against the fixed repo
    /// root and stores the result.
    fn run_layer_coherence(&mut self) {
        self.layer_findings = Some(
            audit_layer_coherence(&self.fs, &repo_root())
                .expect("layer-coherence audit succeeds against MockFs"),
        );
    }

    /// Runs `traceability_audit::audit_traceability` against the fixed repo
    /// root and stores the result.
    fn run_traceability(&mut self) {
        self.traceability_findings = Some(
            audit_traceability(&self.fs, &repo_root())
                .expect("traceability audit succeeds against MockFs"),
        );
    }

    /// Runs `audit_orchestrator::run_audit` with `opts` (whose `repo_root`
    /// field is overwritten with the fixed scenario repo root) and stores the
    /// resulting envelope.
    fn exec_audit(&mut self, mut opts: AuditOptions) {
        opts.repo_root = repo_root();
        self.audit_env = Some(
            run_governance_audit(&self.fs, &opts)
                .expect("governance audit succeeds against MockFs"),
        );
    }

    /// Returns `true` when the single validator that has run so far reported
    /// zero findings (mirrors the subprocess binary's exit-0 behavior).
    fn passed(&self) -> bool {
        self.vendor_findings
            .as_ref()
            .map(Vec::is_empty)
            .or_else(|| self.layer_findings.as_ref().map(Vec::is_empty))
            .or_else(|| self.traceability_findings.as_ref().map(Vec::is_empty))
            .or_else(|| {
                self.audit_env
                    .as_ref()
                    .map(|env| env.result.total_findings == 0)
            })
            .expect("a validator has run before this Then step")
    }

    fn vendor(&self) -> &[Finding] {
        self.vendor_findings
            .as_deref()
            .expect("vendor-audit validator has run")
    }

    fn layer(&self) -> &[LayerCoherenceFinding] {
        self.layer_findings
            .as_deref()
            .expect("layer-coherence validator has run")
    }

    fn traceability(&self) -> &[TraceabilityFinding] {
        self.traceability_findings
            .as_deref()
            .expect("traceability validator has run")
    }

    fn audit(&self) -> &AuditEnvelope {
        self.audit_env
            .as_ref()
            .expect("governance-audit orchestrator has run")
    }
}

/// Builds a Markdown fragment declaring each `(number, name)` pair using the
/// bold `**Layer N: Name**` syntax the layer-coherence audit recognizes.
fn layer_doc(layers: &[(u32, &str)]) -> String {
    let mut s = String::new();
    for (n, name) in layers {
        let _ = writeln!(s, "**Layer {n}: {name}**");
    }
    s
}

/// Returns the `vendor-audit` category result from a `repo-governance audit`
/// envelope.
fn vendor_audit_category(env: &AuditEnvelope) -> &AuditCategoryResult {
    env.result
        .categories
        .iter()
        .find(|c| c.name == "vendor-audit")
        .expect("vendor-audit category present in result")
}

/// Returns the `file` field of every finding in the `vendor-audit` category,
/// with backslashes normalized to forward slashes for cross-platform
/// comparison.
fn vendor_audit_files(env: &AuditEnvelope) -> Vec<String> {
    vendor_audit_category(env)
        .findings
        .iter()
        .map(|f| f.file.replace('\\', "/"))
        .collect()
}

// ===========================================================================
// Given steps — repo-governance vendor validate
// ===========================================================================

// Matches any quoted term/path in plain prose, including the Scenario Outline
// placeholders (`"<term>"`, `"<path>"`) and the substituted example values
// (e.g. `"Junie"`, `".junie/"`). The captured token is embedded verbatim in the
// fixture prose so the scanner has something to flag.
#[given(regex = r#"^a governance markdown file containing "([^"]+)" in plain prose$"#)]
#[allow(clippy::needless_pass_by_value)] // cucumber-rs binds the capture by value
fn given_term_in_prose(w: &mut GovernanceWorld, term: String) {
    w.target = PathBuf::from("repo-governance/doc.md");
    w.write(
        "repo-governance/doc.md",
        &format!("# Doc\n\nWe use {term} daily.\n"),
    );
}

#[given(r#"a governance markdown file containing "Claude Code" inside a code fence"#)]
fn given_brand_in_fence(w: &mut GovernanceWorld) {
    w.target = PathBuf::from("repo-governance/doc.md");
    w.write("repo-governance/doc.md", "# Doc\n\n```\nClaude Code\n```\n");
}

#[given(r#"a governance markdown file containing "Claude Code" inside a binding-example fence"#)]
fn given_brand_in_binding_example(w: &mut GovernanceWorld) {
    w.target = PathBuf::from("repo-governance/doc.md");
    w.write(
        "repo-governance/doc.md",
        "# Doc\n\n```binding-example\nClaude Code\n```\n",
    );
}

// Matches any quoted term under a "Platform Binding Examples" heading (the
// term is exempt there). Covers both `"Claude Code"` and the `"Junie"` outline
// example value.
#[given(
    regex = r#"^a governance markdown file containing "([^"]+)" under a "Platform Binding Examples" heading$"#
)]
#[allow(clippy::needless_pass_by_value)] // cucumber-rs binds the capture by value
fn given_term_under_pb_heading(w: &mut GovernanceWorld, term: String) {
    w.target = PathBuf::from("repo-governance/doc.md");
    w.write(
        "repo-governance/doc.md",
        &format!("# Doc\n\n## Platform Binding Examples\n\n{term} is fine here.\n"),
    );
}

#[given("a governance directory with no forbidden terms in prose")]
fn given_clean_directory(w: &mut GovernanceWorld) {
    w.target = PathBuf::from("repo-governance");
    w.write(
        "repo-governance/a.md",
        "# A\n\nVendor-neutral prose only.\n",
    );
    w.write(
        "repo-governance/b.md",
        "# B\n\nThe coding agent does the work.\n",
    );
}

#[given(r#"a governance markdown file containing "Skills" inside a code fence"#)]
fn given_skills_in_fence(w: &mut GovernanceWorld) {
    w.target = PathBuf::from("repo-governance/doc.md");
    w.write("repo-governance/doc.md", "# Doc\n\n```\nSkills\n```\n");
}

// ===========================================================================
// Given steps — repo-governance layer-coherence validate
// ===========================================================================

#[given("a repository where both governance docs list layers 0 through 5 with identical names")]
fn given_layers_identical(w: &mut GovernanceWorld) {
    w.write_matching_layer_docs(&[
        (0, "Vision"),
        (1, "Principles"),
        (2, "Conventions"),
        (3, "Development"),
        (4, "Agents"),
        (5, "Workflows"),
    ]);
}

#[given("a repository where the governance docs list layers 0, 1, and 3 with no layer 2")]
fn given_layers_gap(w: &mut GovernanceWorld) {
    w.write_matching_layer_docs(&[(0, "Vision"), (1, "Principles"), (3, "Development")]);
}

#[given(
    "a repository where the two governance docs assign different names to the same layer number"
)]
fn given_layers_name_mismatch(w: &mut GovernanceWorld) {
    w.write(
        "repo-governance/repository-governance-architecture.md",
        "**Layer 0: Vision**\n",
    );
    w.write("repo-governance/README.md", "**Layer 0: Mission**\n");
}

// ===========================================================================
// Given steps — repo-governance traceability validate
// ===========================================================================

#[given("a repository where every governance document carries the required traceability sections")]
fn given_traceability_clean(w: &mut GovernanceWorld) {
    w.write(
        "repo-governance/principles/p.md",
        "# P\n\n## Vision Supported\n\nBody.\n",
    );
    w.write(
        "repo-governance/conventions/c.md",
        "# C\n\n## Principles Implemented/Respected\n\nBody.\n",
    );
    w.write(
        "repo-governance/development/d.md",
        "# D\n\n## Principles Implemented/Respected\n\n## Conventions Implemented/Respected\n\nBody.\n",
    );
    w.write(
        "repo-governance/workflows/w.md",
        "# W\n\nSee `.claude/agents/foo-bar.md`.\n",
    );
}

#[given("a repository with a principle file that is missing the \"## Vision Supported\" heading")]
fn given_principle_missing_vision(w: &mut GovernanceWorld) {
    w.write(
        "repo-governance/principles/p.md",
        "# P\n\nNo heading here.\n",
    );
}

#[given(
    "a repository with a convention file that is missing the \"## Principles Implemented/Respected\" heading"
)]
fn given_convention_missing_principles(w: &mut GovernanceWorld) {
    w.write(
        "repo-governance/conventions/c.md",
        "# C\n\nNo heading here.\n",
    );
}

#[given(
    "a repository with a development file that is missing the \"## Conventions Implemented/Respected\" heading"
)]
fn given_development_missing_conventions(w: &mut GovernanceWorld) {
    w.write(
        "repo-governance/development/d.md",
        "# D\n\n## Principles Implemented/Respected\n\nBody.\n",
    );
}

#[given("a repository with a workflow file that contains no reference to any .claude/agents/ file")]
fn given_workflow_missing_agent_ref(w: &mut GovernanceWorld) {
    w.write("repo-governance/workflows/w.md", "# W\n\nno agent here.\n");
}

#[given(
    "a repository with a governance document split into a child directory whose children carry plain kebab-case names"
)]
fn given_split_child_plain_kebab_case(w: &mut GovernanceWorld) {
    // The parent keeps the traceability heading; its children, indexed by the
    // sibling README.md, are exempt by position — the Ordinal Filename Prefixes
    // Convention strips the `NN-` prefix these children once carried.
    w.write(
        "repo-governance/conventions/c.md",
        "# C\n\n## Principles Implemented/Respected\n\nBody.\n",
    );
    w.write(
        "repo-governance/conventions/c/README.md",
        "# C\n\n- [One](./one.md) — first shard.\n",
    );
    w.write(
        "repo-governance/conventions/c/one.md",
        "# One\n\nNo heading here.\n",
    );
}

#[given("a split convention whose indexed child carries the required traceability section")]
fn given_split_convention_with_child_traceability(w: &mut GovernanceWorld) {
    w.write(
        "repo-governance/conventions/c.md",
        "# C\n\nSee [Principles](./c/principles.md).\n",
    );
    w.write(
        "repo-governance/conventions/c/README.md",
        "# C\n\n- [Principles](./principles.md) — traceability.\n",
    );
    w.write(
        "repo-governance/conventions/c/principles.md",
        "# Principles Implemented/Respected\n\nBody.\n",
    );
}

#[given("a repository with an indexed category directory that has no same-named parent document")]
fn given_indexed_category_dir(w: &mut GovernanceWorld) {
    // A category directory carries a README.md index but no same-named sibling
    // `.md`, so its members are whole conventions, not split children.
    w.write(
        "repo-governance/conventions/formatting/README.md",
        "# Formatting\n\n- [Color](./color.md) — palette rules.\n",
    );
    w.write(
        "repo-governance/conventions/formatting/color.md",
        "# Color\n\nNo heading here.\n",
    );
}

// ===========================================================================
// Given steps — repo-governance audit
// ===========================================================================

#[given("a repository where every deterministic governance category reports zero findings")]
fn given_audit_all_clean(w: &mut GovernanceWorld) {
    w.write_matching_layer_docs(&[(0, "Vision")]);
}

#[given(
    "a repository with forbidden vendor terms in repo-governance prose and also in out-of-scope paths such as build caches, app source, and worktrees"
)]
fn given_audit_vendor_scope(w: &mut GovernanceWorld) {
    w.write(
        "repo-governance/conventions/foo.md",
        "We use Claude Code internally.\n",
    );
    w.write("AGENTS.md", "Edited with Cursor today.\n");
    w.write("CLAUDE.md", "Powered by Anthropic models.\n");
    w.write(".nx/cache/x.md", "Built on OpenCode.\n");
    w.write("apps/web/y.md", "Built on OpenCode.\n");
    w.write("worktrees/wt/z.md", "Built on OpenCode.\n");
}

#[given(
    "a repository where two deterministic governance categories report findings and the rest pass"
)]
fn given_audit_mixed(w: &mut GovernanceWorld) {
    // layer-coherence passes: matching single-layer docs.
    w.write_matching_layer_docs(&[(0, "Vision")]);
    // vendor-audit fails: one forbidden term.
    w.write("repo-governance/doc.md", "We use Claude Code daily.\n");
    // traceability-audit fails: a principle missing its required heading.
    w.write("repo-governance/principles/p.md", "# P\n\nNo heading.\n");
}

#[given("a repository where deterministic governance categories return a fixed finding set")]
fn given_audit_fixed_set(w: &mut GovernanceWorld) {
    w.write_matching_layer_docs(&[(0, "Vision")]);
    w.write("repo-governance/doc.md", "We use Claude Code daily.\n");
}

#[given("a repository where a finding key matches a known-false-positives entry")]
fn given_audit_false_positive(w: &mut GovernanceWorld) {
    w.write_matching_layer_docs(&[(0, "Vision")]);
    w.write("repo-governance/doc.md", "We use Claude Code daily.\n");

    // Prime a run to learn the finding's exact key, then register it as a
    // known false positive so the measured run in the `When` step suppresses
    // it instead of counting it toward total_findings.
    w.exec_audit(AuditOptions::default());
    let key = vendor_audit_category(w.audit()).findings[0].key.clone();
    w.write(
        "generated-reports/.known-false-positives.md",
        &format!("- `{key}`\n"),
    );
}

#[given("a repository where deterministic governance categories return any finding set")]
fn given_audit_any_set(w: &mut GovernanceWorld) {
    w.write("repo-governance/doc.md", "We use Claude Code daily.\n");
}

// ===========================================================================
// When steps
// ===========================================================================

#[when("the developer runs repo-governance vendor validate on the file")]
#[when("the developer runs repo-governance vendor validate on the directory")]
fn when_run_vendor_validate(w: &mut GovernanceWorld) {
    w.run_vendor_validate();
}

#[when("the developer runs repo-governance layer-coherence validate")]
fn when_run_layer_coherence(w: &mut GovernanceWorld) {
    w.run_layer_coherence();
}

#[when("the developer runs repo-governance traceability validate")]
fn when_run_traceability(w: &mut GovernanceWorld) {
    w.run_traceability();
}

#[when("the developer runs repo-governance audit")]
fn when_run_governance_audit(w: &mut GovernanceWorld) {
    w.exec_audit(AuditOptions::default());
}

#[when("the developer runs repo-governance audit ten consecutive times with a fixed clock")]
fn when_run_governance_audit_ten_times(w: &mut GovernanceWorld) {
    let opts = AuditOptions {
        repo_root: repo_root(),
        now: Some("2026-01-01T00:00:00Z".to_string()),
        ..Default::default()
    };
    let mut runs = Vec::with_capacity(10);
    for _ in 0..10 {
        let env =
            run_governance_audit(&w.fs, &opts).expect("governance audit succeeds against MockFs");
        runs.push(serde_json::to_string(&env).expect("envelope serializes to JSON"));
    }
    w.captured_runs = runs;
}

#[when("the developer runs repo-governance audit with include-category limited to one category")]
fn when_run_governance_audit_include_category(w: &mut GovernanceWorld) {
    w.exec_audit(AuditOptions {
        include_only: vec!["layer-coherence".to_string()],
        ..Default::default()
    });
}

// ===========================================================================
// Then steps — shared exit-code assertions
// ===========================================================================

#[then("the command exits with a failure code")]
fn then_exit_fail(w: &mut GovernanceWorld) {
    assert!(!w.passed(), "expected findings, got a clean result");
}

#[then("the command exits successfully")]
fn then_exit_ok(w: &mut GovernanceWorld) {
    assert!(w.passed(), "expected zero findings");
}

// ===========================================================================
// Then steps — repo-governance vendor validate
// ===========================================================================

#[then("the output identifies the forbidden term and its location")]
fn then_identifies_term(w: &mut GovernanceWorld) {
    let findings = w.vendor();
    assert!(!findings.is_empty(), "expected at least one finding");
    assert!(
        findings.iter().any(|f| f.path.ends_with("doc.md")),
        "got: {findings:?}"
    );
}

#[then("the output reports zero findings")]
fn then_zero_findings(w: &mut GovernanceWorld) {
    assert!(w.vendor().is_empty(), "got: {:?}", w.vendor());
}

// ===========================================================================
// Then steps — repo-governance layer-coherence validate
// ===========================================================================

#[then("the layer-coherence output reports zero findings")]
fn then_layer_zero_findings(w: &mut GovernanceWorld) {
    assert!(w.layer().is_empty(), "got: {:?}", w.layer());
}

#[then("the layer-coherence output identifies the numbering gap")]
fn then_layer_numbering_gap(w: &mut GovernanceWorld) {
    let findings = w.layer();
    assert!(
        findings
            .iter()
            .any(|f| f.kind == KIND_NUMBERING_GAP && f.message.contains("Layer 2")),
        "got: {findings:?}"
    );
}

#[then("the layer-coherence output identifies the layer name disagreement")]
fn then_layer_name_disagreement(w: &mut GovernanceWorld) {
    let findings = w.layer();
    assert!(
        findings
            .iter()
            .any(|f| f.kind == KIND_CROSS_FILE_NAME_MISMATCH
                && f.message.contains("Vision")
                && f.message.contains("Mission")),
        "got: {findings:?}"
    );
}

// ===========================================================================
// Then steps — repo-governance traceability validate
// ===========================================================================

#[then("the traceability output reports zero findings")]
fn then_traceability_zero(w: &mut GovernanceWorld) {
    assert!(w.traceability().is_empty(), "got: {:?}", w.traceability());
}

#[then("the traceability output identifies the missing Vision Supported section")]
fn then_traceability_missing_vision(w: &mut GovernanceWorld) {
    let findings = w.traceability();
    assert!(
        findings
            .iter()
            .any(|f| f.kind == KIND_MISSING_VISION_SUPPORTED),
        "got: {findings:?}"
    );
}

#[then("the traceability output identifies the missing Principles Implemented section")]
fn then_traceability_missing_principles(w: &mut GovernanceWorld) {
    let findings = w.traceability();
    assert!(
        findings
            .iter()
            .any(|f| f.kind == KIND_MISSING_PRINCIPLES_IMPLEMENTED),
        "got: {findings:?}"
    );
}

#[then("the traceability output identifies the missing Conventions Implemented section")]
fn then_traceability_missing_conventions(w: &mut GovernanceWorld) {
    let findings = w.traceability();
    assert!(
        findings
            .iter()
            .any(|f| f.kind == KIND_MISSING_CONVENTIONS_IMPLEMENTED),
        "got: {findings:?}"
    );
}

#[then("the traceability output identifies the missing agent reference")]
fn then_traceability_missing_agent_ref(w: &mut GovernanceWorld) {
    let findings = w.traceability();
    assert!(
        findings
            .iter()
            .any(|f| f.kind == KIND_MISSING_AGENT_REFERENCE),
        "got: {findings:?}"
    );
}

// ===========================================================================
// Then steps — repo-governance audit
// ===========================================================================

#[then("the output reports total_findings equal to zero across all categories")]
fn then_audit_zero_total(w: &mut GovernanceWorld) {
    let env = w.audit();
    assert_eq!(env.result.total_findings, 0, "got: {env:?}");
}

#[then(
    "the vendor-audit category reports findings only from repo-governance, AGENTS.md, and CLAUDE.md"
)]
fn then_audit_vendor_scope(w: &mut GovernanceWorld) {
    let env = w.audit();
    let files = vendor_audit_files(env);
    assert_eq!(files.len(), 3, "got: {files:?}");
    assert!(
        files
            .iter()
            .any(|f| f.ends_with("repo-governance/conventions/foo.md")),
        "got: {files:?}"
    );
    assert!(
        files.iter().any(|f| f.ends_with("/AGENTS.md")),
        "got: {files:?}"
    );
    assert!(
        files.iter().any(|f| f.ends_with("/CLAUDE.md")),
        "got: {files:?}"
    );
}

#[then(
    "forbidden vendor terms in build caches, app source, and worktrees do not appear in the result"
)]
fn then_audit_vendor_scope_excludes(w: &mut GovernanceWorld) {
    let env = w.audit();
    let files = vendor_audit_files(env);
    assert!(!files.iter().any(|f| f.contains("/.nx/")), "got: {files:?}");
    assert!(
        !files.iter().any(|f| f.contains("/apps/")),
        "got: {files:?}"
    );
    assert!(
        !files.iter().any(|f| f.contains("/worktrees/")),
        "got: {files:?}"
    );
}

#[then("the output reports total_findings equal to the sum of category findings")]
fn then_audit_sum_total(w: &mut GovernanceWorld) {
    let env = w.audit();
    let sum: usize = env.result.categories.iter().map(|c| c.findings.len()).sum();
    assert_eq!(env.result.total_findings, sum, "got: {env:?}");
    let failing = env.result.categories.iter().filter(|c| !c.passed).count();
    assert_eq!(
        failing, 2,
        "expected exactly two failing categories, got: {env:?}"
    );
}

#[then("every run produces byte-identical JSON output")]
fn then_audit_byte_identical(w: &mut GovernanceWorld) {
    assert_eq!(w.captured_runs.len(), 10, "expected 10 captured runs");
    let first = &w.captured_runs[0];
    for (i, run) in w.captured_runs.iter().enumerate() {
        assert_eq!(run, first, "run {i} diverged from run 0");
    }
}

#[then("the matching finding appears under skipped_false_positives")]
fn then_audit_skipped_false_positive(w: &mut GovernanceWorld) {
    let env = w.audit();
    assert_eq!(env.result.skipped_false_positives.len(), 1, "got: {env:?}");
}

#[then("the matching finding does not count toward total_findings")]
fn then_audit_false_positive_excluded_from_total(w: &mut GovernanceWorld) {
    let env = w.audit();
    assert_eq!(env.result.total_findings, 0, "got: {env:?}");
}

#[then("only the listed category appears in the result categories list")]
fn then_audit_include_category_filter(w: &mut GovernanceWorld) {
    let env = w.audit();
    assert_eq!(env.result.categories.len(), 1, "got: {env:?}");
    assert_eq!(
        env.result.categories[0].name, "layer-coherence",
        "got: {env:?}"
    );
}

#[tokio::main]
async fn main() {
    GovernanceWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/repo-governance")
        .canonicalize()
        .expect("feature dir resolvable")
}
