//! CLI entry point: argument parsing, subcommand dispatch, and help output.

use clap::{Parser, Subcommand};

use crate::commands::{
    convention_audit, convention_validate_emoji, convention_validate_license, doctor, env_backup,
    env_init, env_restore, env_staged_guard, env_validate, gate, git, governance_audit,
    governance_generate_readme_index, governance_layer_coherence,
    governance_rewrite_readme_index_paths, governance_traceability_audit,
    governance_validate_readme_index, governance_validate_word_budget, governance_vendor_audit,
    harness_audit, harness_catalog, harness_generate_bindings, harness_sync_promote,
    harness_sync_triage, harness_validate_bindings, harness_validate_claude,
    harness_validate_duplication, harness_validate_ownership, harness_validate_sync, md_audit,
    md_validate_frontmatter, md_validate_frontmatter_dates, md_validate_heading_hierarchy,
    md_validate_links, md_validate_mermaid, md_validate_naming, parity, repo_config_validate,
    specs_audit, specs_coverage, specs_e2e_coverage, specs_gherkin_cardinality,
    specs_scaffold_dart, specs_structure_validate, specs_validate_counts, test_coverage_validate,
};
use crate::domain::cliout::OutputFormat;

#[derive(Parser, Debug)]
#[command(
    name = "rhino-cli",
    version = "0.16.1",
    about = "CLI tools for repository management",
    long_about = "Command-line tools for repository management and automation.",
    disable_help_flag = true
)]
/// Root CLI arguments shared across all subcommands.
pub struct Cli {
    /// Enable verbose output with timestamps.
    #[arg(
        long,
        short = 'v',
        global = true,
        help = "verbose output with timestamps"
    )]
    pub verbose: bool,

    /// Suppress all output except errors.
    #[arg(long, short = 'q', global = true, help = "quiet mode (errors only)")]
    pub quiet: bool,

    /// Output format: `text`, `json`, or `markdown`.
    #[arg(
        long,
        short = 'o',
        global = true,
        default_value = "text",
        help = "output format: text, json, markdown"
    )]
    pub output: String,

    /// Disable ANSI color codes in output.
    #[arg(long = "no-color", global = true, help = "disable colored output")]
    pub no_color: bool,

    /// Echo a literal message to stdout and exit.
    #[arg(
        long,
        global = true,
        default_value = "",
        help = "echo a message to stdout"
    )]
    pub say: String,

    /// Print help and exit.
    #[arg(long, short = 'h', global = true, help = "Print help")]
    pub help: bool,

    /// Subcommand to execute.
    #[command(subcommand)]
    pub command: Option<Commands>,
}

/// Top-level CLI subcommands dispatched by the root `Cli` parser.
#[derive(Subcommand, Debug)]
pub enum Commands {
    /// Test coverage commands (validate).
    #[command(name = "test-coverage", subcommand)]
    TestCoverage(TestCoverageCommands),
    /// Repository governance audits and validators.
    #[command(name = "repo-governance", subcommand)]
    RepoGovernance(RepoGovernanceCommands),
    /// Markdown validators (links, mermaid, heading-hierarchy, naming, frontmatter, etc.).
    #[command(name = "md", subcommand)]
    Md(MdCommands),
    /// Convention validators (emoji, license).
    #[command(name = "convention", subcommand)]
    Convention(ConventionCommands),
    /// Harness (agent binding) validators and generators.
    #[command(name = "harness", subcommand)]
    Harness(HarnessCommands),
    /// Cross-cutting governance gates (word budget, README index/completeness).
    #[command(name = "governance", subcommand)]
    Governance(GovernanceCommands),
    /// Spec tree validators and contract codegen helpers.
    #[command(name = "specs", subcommand)]
    Specs(SpecsCommands),
    /// Repository configuration (`repo-config.yml`) schema-parity validator.
    #[command(name = "repo-config", subcommand)]
    RepoConfig(RepoConfigCommands),
    /// Environment file helpers (init, backup, restore, validate, staged-guard).
    #[command(name = "env", subcommand)]
    Env(EnvCommands),
    /// Gate-registry commands.
    #[command(name = "gate", subcommand)]
    Gate(GateCommands),
    /// Git workflow helpers.
    #[command(name = "git", subcommand)]
    Git(GitCommands),
    /// Rhino CLI byte-identity boundary helpers.
    #[command(name = "parity", subcommand)]
    Parity(ParityCommands),
    /// Check required tool versions are installed and correct.
    #[command(name = "doctor")]
    Doctor(doctor::DoctorArgs),
}

// ---------------------------------------------------------------------------
// test-coverage (union command surface — the live coverage-gate validator,
// depended on by per-project coverage targets; diff/merge logic lives in
// `application::testcoverage` but is not exposed as a command, matching the
// live surface in the sibling repos)
// ---------------------------------------------------------------------------

/// Test coverage subcommands (`validate`).
#[derive(Subcommand, Debug)]
pub enum TestCoverageCommands {
    /// Check test coverage against a threshold (standard line-based algorithm).
    Validate(test_coverage_validate::ValidateArgs),
}

// ---------------------------------------------------------------------------
// repo-config (verb-last: repo-config validate) — the schema-parity gate
// ---------------------------------------------------------------------------

/// Repository configuration subcommands (`validate`).
#[derive(Subcommand, Debug)]
pub enum RepoConfigCommands {
    /// Strict-deserialize `repo-config.yml` against the canonical schema (key-set + enum parity).
    Validate(repo_config_validate::ValidateArgs),
}

/// Gate-registry subcommands.
#[derive(Subcommand, Debug)]
pub enum GateCommands {
    /// List declared gates for an execution surface.
    List(gate::list::ListArgs),
    /// Emit the generated artifact for a gate surface.
    Emit(gate::emit::EmitArgs),
    /// Run declared gates for an execution surface.
    Run(gate::run::RunArgs),
    /// Validate gate-registry composition rules.
    Validate(gate::validate::ValidateArgs),
}

/// Git workflow helper subcommands.
#[derive(Subcommand, Debug)]
pub enum GitCommands {
    /// Lockfile synchronization commands.
    #[command(subcommand)]
    Lockfile(GitLockfileCommands),
}

/// Lockfile synchronization subcommands.
#[derive(Subcommand, Debug)]
pub enum GitLockfileCommands {
    /// Regenerate and stage lockfiles for staged app manifests.
    Sync(git::lockfile::SyncArgs),
}

/// Byte-identity parity subcommands.
#[derive(Subcommand, Debug)]
pub enum ParityCommands {
    /// Checksum-manifest operations.
    #[command(name = "manifest", subcommand)]
    Manifest(ParityManifestCommands),
}

/// `parity manifest` subcommands.
#[derive(Subcommand, Debug)]
pub enum ParityManifestCommands {
    /// Deliberately regenerate the committed parity manifest.
    Generate(parity::GenerateArgs),
    /// Verify the committed parity manifest without regenerating it.
    Validate(parity::ValidateArgs),
}

// ---------------------------------------------------------------------------
// env (unchanged — all already verb-last or single-word noun)
// ---------------------------------------------------------------------------

/// Environment file subcommands (`init`, `backup`, `restore`, `validate`, `staged-guard`).
#[derive(Subcommand, Debug)]
pub enum EnvCommands {
    /// Create .env files from .env.example templates.
    #[command(name = "init")]
    Init(env_init::EnvInitArgs),
    /// Back up .env files from the repository.
    #[command(name = "backup")]
    Backup(env_backup::EnvBackupArgs),
    /// Restore .env files from a backup.
    #[command(name = "restore")]
    Restore(env_restore::EnvRestoreArgs),
    /// Check code↔config drift for all surfaces in env-contract.yaml.
    #[command(name = "validate")]
    Validate(env_validate::EnvValidateArgs),
    /// Guard against committing real .env files.
    #[command(name = "staged-guard", subcommand)]
    StagedGuard(EnvStagedGuardCommands),
}

/// Subcommands for `env staged-guard`.
#[derive(Subcommand, Debug)]
pub enum EnvStagedGuardCommands {
    /// Reject any staged .env* file except .env.example (policy: guard-env-file-access).
    #[command(name = "validate")]
    Validate(env_staged_guard::EnvStagedGuardValidateArgs),
}

// ---------------------------------------------------------------------------
// repo-governance (verb-last: repo-governance {noun} validate)
// ---------------------------------------------------------------------------

/// Repository governance subcommands.
#[derive(Subcommand, Debug)]
pub enum RepoGovernanceCommands {
    /// Scan governance markdown for forbidden vendor-specific terms.
    #[command(name = "vendor", subcommand)]
    Vendor(RepoGovernanceVendorCommands),
    /// Audit governance docs for layer numbering/naming coherence.
    #[command(name = "layer-coherence", subcommand)]
    LayerCoherence(RepoGovernanceLayerCoherenceCommands),
    /// Audit governance documents for required traceability sections.
    #[command(name = "traceability", subcommand)]
    Traceability(RepoGovernanceTraceabilityCommands),
    /// Run all deterministic governance audits and emit a JSON envelope.
    #[command(name = "audit")]
    Audit(governance_audit::AuditArgs),
}

/// `repo-governance vendor` subcommands.
#[derive(Subcommand, Debug)]
pub enum RepoGovernanceVendorCommands {
    /// Scan governance markdown for forbidden vendor-specific terms.
    #[command(name = "validate")]
    Validate(governance_vendor_audit::VendorAuditArgs),
}

/// `repo-governance layer-coherence` subcommands.
#[derive(Subcommand, Debug)]
pub enum RepoGovernanceLayerCoherenceCommands {
    /// Audit governance docs for layer numbering/naming coherence.
    #[command(name = "validate")]
    Validate(governance_layer_coherence::LayerCoherenceArgs),
}

/// `repo-governance traceability` subcommands.
#[derive(Subcommand, Debug)]
pub enum RepoGovernanceTraceabilityCommands {
    /// Audit governance documents for required traceability sections.
    #[command(name = "validate")]
    Validate(governance_traceability_audit::TraceabilityAuditArgs),
}

// ---------------------------------------------------------------------------
// md (verb-last: md {noun} validate)
// ---------------------------------------------------------------------------

/// Markdown validator subcommands.
#[derive(Subcommand, Debug)]
pub enum MdCommands {
    /// Validate markdown links (relative paths exist on disk).
    #[command(name = "links", subcommand)]
    Links(MdLinksCommands),
    /// Validate Mermaid flowchart diagrams (label length, span, single-diagram).
    #[command(name = "mermaid", subcommand)]
    Mermaid(MdMermaidCommands),
    /// Validate markdown heading hierarchy (one H1, no skipped levels).
    #[command(name = "heading-hierarchy", subcommand)]
    HeadingHierarchy(MdHeadingHierarchyCommands),
    /// Validate markdown filenames against the lowercase-kebab-case rule.
    #[command(name = "naming", subcommand)]
    Naming(MdNamingCommands),
    /// Validate documentation YAML frontmatter against area-specific schemas.
    #[command(name = "frontmatter", subcommand)]
    Frontmatter(MdFrontmatterCommands),
    /// Audit markdown files for forbidden manual date metadata.
    #[command(name = "frontmatter-dates", subcommand)]
    FrontmatterDates(MdFrontmatterDatesCommands),
    /// Run all md validators in sequence and aggregate findings.
    #[command(name = "audit")]
    Audit(md_audit::AuditArgs),
}

/// `md links` subcommands.
#[derive(Subcommand, Debug)]
pub enum MdLinksCommands {
    /// Validate markdown links (relative paths exist on disk).
    #[command(name = "validate")]
    Validate(md_validate_links::ValidateLinksArgs),
}

/// `md mermaid` subcommands.
#[derive(Subcommand, Debug)]
pub enum MdMermaidCommands {
    /// Validate Mermaid flowchart diagrams (label length, span, single-diagram).
    #[command(name = "validate")]
    Validate(md_validate_mermaid::ValidateMermaidArgs),
}

/// `md heading-hierarchy` subcommands.
#[derive(Subcommand, Debug)]
pub enum MdHeadingHierarchyCommands {
    /// Validate markdown heading hierarchy (one H1, no skipped levels).
    #[command(name = "validate")]
    Validate(md_validate_heading_hierarchy::ValidateHeadingHierarchyArgs),
}

/// `md naming` subcommands.
#[derive(Subcommand, Debug)]
pub enum MdNamingCommands {
    /// Validate markdown filenames against the lowercase-kebab-case rule.
    #[command(name = "validate")]
    Validate(md_validate_naming::ValidateNamingArgs),
}

/// `md frontmatter` subcommands.
#[derive(Subcommand, Debug)]
pub enum MdFrontmatterCommands {
    /// Validate documentation YAML frontmatter against area-specific schemas.
    #[command(name = "validate")]
    Validate(md_validate_frontmatter::ValidateFrontmatterArgs),
}

/// `md frontmatter-dates` subcommands.
#[derive(Subcommand, Debug)]
pub enum MdFrontmatterDatesCommands {
    /// Audit markdown files for forbidden manual date metadata.
    #[command(name = "validate")]
    Validate(md_validate_frontmatter_dates::FrontmatterAuditArgs),
}

// ---------------------------------------------------------------------------
// governance (verb-last: governance {noun} validate)
// Word budget (instruction-file word budget, cross-domain moved from harness
// in this plan) and README index/completeness (cross-domain moved from md).
// ---------------------------------------------------------------------------

/// Governance gate subcommands.
#[derive(Subcommand, Debug)]
pub enum GovernanceCommands {
    /// Check per-surface and resolved-tree word budgets for instruction files.
    #[command(name = "word-budget", subcommand)]
    WordBudget(GovernanceWordBudgetCommands),
    /// Audit directory README.md indexes against sibling markdown files.
    #[command(name = "readme-index", subcommand)]
    ReadmeIndex(GovernanceReadmeIndexCommands),
}

/// `governance word-budget` subcommands.
#[derive(Subcommand, Debug)]
pub enum GovernanceWordBudgetCommands {
    /// Check per-surface and resolved-tree word budgets for instruction files.
    #[command(name = "validate")]
    Validate(governance_validate_word_budget::ValidateWordBudgetArgs),
}

/// `governance readme-index` subcommands.
#[derive(Subcommand, Debug)]
pub enum GovernanceReadmeIndexCommands {
    /// Audit directory README.md indexes against sibling markdown files.
    #[command(name = "validate")]
    Validate(governance_validate_readme_index::ReadmeIndexAuditArgs),
    /// Write conforming README.md (or split-directory sibling `<name>.md`)
    /// indexes for every covered directory that needs one (FR-3.12).
    #[command(name = "generate")]
    Generate(governance_generate_readme_index::ReadmeIndexGenerateArgs),
    /// Repoint markdown link targets across the corpus from a TSV rename map,
    /// leaving entry order, annotations, and prose untouched.
    #[command(name = "rewrite-paths")]
    RewritePaths(governance_rewrite_readme_index_paths::ReadmeIndexRewritePathsArgs),
}

// ---------------------------------------------------------------------------
// convention (verb-last: convention {noun} validate)
// Note: AGENTS.md size is owned by `governance word-budget validate`; the byte-based
// validator that once lived here is gone, and instruction-size moved to the harness domain.
// ---------------------------------------------------------------------------

/// Convention validator subcommands.
#[derive(Subcommand, Debug)]
pub enum ConventionCommands {
    /// Audit forbidden file types for emoji codepoints.
    #[command(name = "emoji", subcommand)]
    Emoji(ConventionEmojiCommands),
    /// Verify per-directory LICENSE files match the licensing convention.
    #[command(name = "license", subcommand)]
    License(ConventionLicenseCommands),
    /// Run all convention validators in sequence and aggregate findings.
    #[command(name = "audit")]
    Audit(convention_audit::AuditArgs),
}

/// `convention emoji` subcommands.
#[derive(Subcommand, Debug)]
pub enum ConventionEmojiCommands {
    /// Audit forbidden file types for emoji codepoints.
    #[command(name = "validate")]
    Validate(convention_validate_emoji::EmojiAuditArgs),
}

/// `convention license` subcommands.
#[derive(Subcommand, Debug)]
pub enum ConventionLicenseCommands {
    /// Verify per-directory LICENSE files match the licensing convention.
    #[command(name = "validate")]
    Validate(convention_validate_license::LicenseAuditArgs),
}

// ---------------------------------------------------------------------------
// harness (verb-last: harness {noun} validate / harness {noun} generate)
// Note: harness sync opencode is merged into harness bindings generate
//       (use --harness opencode).
//       convention validate instruction-size is cross-domain moved here.
// ---------------------------------------------------------------------------

/// Harness (agent binding) subcommands.
#[derive(Subcommand, Debug)]
pub enum HarnessCommands {
    /// Detect verbatim duplication across agent and skill files.
    #[command(name = "duplication", subcommand)]
    Duplication(HarnessDuplicationCommands),
    /// Validate Claude Code agent and skill format in .claude/ directory.
    #[command(name = "claude", subcommand)]
    Claude(HarnessClaudeCommands),
    /// Validate that .claude/ and .opencode/ are in sync.
    #[command(name = "sync", subcommand)]
    Sync(HarnessSyncCommands),
    /// Validate binding artifacts and generate platform bindings.
    #[command(name = "bindings", subcommand)]
    Bindings(HarnessBindingsCommands),
    /// Validate that every tracked binding file carries one declared owner.
    #[command(name = "ownership", subcommand)]
    Ownership(HarnessOwnershipCommands),
    /// Generate and guard the platform-binding catalog table.
    #[command(name = "catalog", subcommand)]
    Catalog(HarnessCatalogCommands),
    /// Run all harness validators in sequence and aggregate findings.
    #[command(name = "audit")]
    Audit(harness_audit::AuditArgs),
}

/// `harness catalog` subcommands.
#[derive(Subcommand, Debug)]
pub enum HarnessCatalogCommands {
    /// Render the catalog table from the harness registry into its
    /// generated region, leaving surrounding prose untouched.
    #[command(name = "generate")]
    Generate(harness_catalog::CatalogGenerateArgs),
    /// Fail when the generated region diverges from the harness registry.
    #[command(name = "validate")]
    Validate(harness_catalog::CatalogValidateArgs),
}

/// `harness duplication` subcommands.
#[derive(Subcommand, Debug)]
pub enum HarnessDuplicationCommands {
    /// Detect verbatim duplication across agent and skill files.
    #[command(name = "validate")]
    Validate(harness_validate_duplication::DetectDuplicationArgs),
}

/// `harness claude` subcommands.
#[derive(Subcommand, Debug)]
pub enum HarnessClaudeCommands {
    /// Validate Claude Code agent and skill format in .claude/ directory.
    #[command(name = "validate")]
    Validate(harness_validate_claude::ValidateClaudeArgs),
}

/// `harness sync` subcommands.
#[derive(Subcommand, Debug)]
pub enum HarnessSyncCommands {
    /// Validate that .claude/ and .opencode/ are in sync.
    #[command(name = "validate")]
    Validate(harness_validate_sync::ValidateSyncArgs),
    /// Report every generated mirror that diverges from canonical source, by
    /// content, and say which side moved.
    #[command(name = "triage")]
    Triage(harness_sync_triage::SyncTriageArgs),
    /// Propose a mirror edit as a patch against canonical source. Writes nothing.
    #[command(name = "promote")]
    Promote(harness_sync_promote::SyncPromoteArgs),
}

/// `harness ownership` subcommands.
#[derive(Subcommand, Debug)]
pub enum HarnessOwnershipCommands {
    /// Validate that every tracked binding file carries one declared owner.
    #[command(name = "validate")]
    Validate(harness_validate_ownership::ValidateOwnershipArgs),
}

/// `harness bindings` subcommands.
#[derive(Subcommand, Debug)]
pub enum HarnessBindingsCommands {
    /// Validate the generated binding files and catalog coverage.
    #[command(name = "validate")]
    Validate(harness_validate_bindings::ValidateBindingsArgs),
    /// Generate every generated-tier platform binding.
    /// Use --harness <NAME> to regenerate one binding only; accepted names are
    /// the `harness:` registry entries in `repo-config.yml`.
    #[command(name = "generate")]
    Generate(harness_generate_bindings::GenerateBindingsArgs),
}

// ---------------------------------------------------------------------------
// specs (verb-last: specs {noun} validate)
// Note: specs validate gherkin-cardinality → specs gherkin-cardinality validate
// ---------------------------------------------------------------------------

/// Spec tree subcommands.
#[derive(Subcommand, Debug)]
pub enum SpecsCommands {
    /// Audit `.feature` scenarios for repeated primary Given/When/Then keywords.
    #[command(name = "gherkin-cardinality", subcommand)]
    GherkinCardinality(SpecsGherkinCardinalityCommands),
    /// Run all structural validators (adoption + tree + counts) in one pass.
    #[command(name = "structure", subcommand)]
    Structure(SpecsStructureCommands),
    /// Validate each required spec subfolder contains at least one spec file. Kept as a
    /// standalone leaf for spec trees outside `specs/apps/` (e.g. `specs/libs/*`) that
    /// `specs structure validate` cannot reach.
    #[command(name = "counts", subcommand)]
    Counts(SpecsCountsCommands),
    /// Run per-level @covers behavior coverage validation.
    #[command(name = "behavior-coverage", subcommand)]
    BehaviorCoverage(SpecsBehaviorCoverageCommands),
    /// Detect Gherkin scenarios playwright-bdd silently skipped via
    /// `test.fixme`, checked against a per-project baseline manifest.
    #[command(name = "e2e-coverage", subcommand)]
    E2eCoverage(SpecsE2eCoverageCommands),
    /// Run per-level @covers coverage validation scoped to domain/** feature files.
    #[command(name = "domain-coverage", subcommand)]
    DomainCoverage(SpecsDomainCoverageCommands),
    /// Scaffold generated contract package structure (e.g. Dart pubspec).
    #[command(name = "scaffold", subcommand)]
    Scaffold(SpecsScaffoldCommands),
    /// Run all specs validators in sequence and aggregate findings.
    #[command(name = "audit")]
    Audit(specs_audit::AuditArgs),
}

/// `specs gherkin-cardinality` subcommands.
#[derive(Subcommand, Debug)]
pub enum SpecsGherkinCardinalityCommands {
    /// Audit `.feature` scenarios for repeated primary Given/When/Then keywords.
    #[command(name = "validate")]
    Validate(specs_gherkin_cardinality::GherkinKeywordCardinalityArgs),
}

/// `specs behavior-coverage` subcommands.
#[derive(Subcommand, Debug)]
pub enum SpecsBehaviorCoverageCommands {
    /// Validate that all BDD spec files have matching test implementations at the required levels.
    #[command(name = "validate")]
    Validate(specs_coverage::ValidateArgs),
}

/// `specs e2e-coverage` subcommands.
#[derive(Subcommand, Debug)]
pub enum SpecsE2eCoverageCommands {
    /// Validate that generated playwright-bdd output has no new unbound
    /// `@e2e` scenarios beyond the checked-in baseline manifest.
    #[command(name = "validate")]
    Validate(specs_e2e_coverage::ValidateArgs),
}

/// `specs domain-coverage` subcommands.
#[derive(Subcommand, Debug)]
pub enum SpecsDomainCoverageCommands {
    /// Validate per-level @covers coverage for domain/** feature files using the domain-areas allowlist.
    #[command(name = "validate")]
    Validate(specs_coverage::ValidateArgs),
}

/// `specs structure` subcommands.
#[derive(Subcommand, Debug)]
pub enum SpecsStructureCommands {
    /// Run adoption + tree + counts structural validators in sequence with per-layer labels.
    #[command(name = "validate")]
    Validate(specs_structure_validate::ValidateStructureArgs),
}

/// `specs counts` subcommands.
#[derive(Subcommand, Debug)]
pub enum SpecsCountsCommands {
    /// Validate each required spec subfolder contains at least one spec file.
    #[command(name = "validate")]
    Validate(specs_validate_counts::ValidateCountsArgs),
}

/// Specs scaffold subcommands.
#[derive(Subcommand, Debug)]
pub enum SpecsScaffoldCommands {
    /// Generate Dart package scaffolding around generated contract types (dormant in ose-public).
    #[command(name = "dart")]
    Dart(specs_scaffold_dart::ScaffoldDartArgs),
}

// ---------------------------------------------------------------------------
// dispatch
// ---------------------------------------------------------------------------

/// Parse CLI arguments and dispatch to the appropriate subcommand.
///
/// Returns the process exit code: `0` on success, `1` on command error, `2` on
/// argument parse error.
///
/// # Errors
///
/// Returns a non-zero exit code when the selected subcommand reports an error.
pub fn run() -> i32 {
    let cli = match Cli::try_parse() {
        Ok(c) => c,
        Err(e) => {
            e.print().ok();
            return 2;
        }
    };

    let output_format = match OutputFormat::parse(&cli.output) {
        Ok(f) => f,
        Err(err) => {
            eprintln!("Error: {err}");
            return 1;
        }
    };

    if cli.help {
        return print_help_and_exit();
    }

    if let Some(cmd) = &cli.command {
        return dispatch(cmd, output_format, cli.verbose, cli.quiet);
    }

    if !cli.say.is_empty() {
        println!("{}", cli.say);
        return 0;
    }

    print_help_and_exit()
}

/// Route a top-level [`Commands`] variant to its subcommand handler.
///
/// Returns `0` on success or `1` on error.
fn dispatch(cmd: &Commands, output_format: OutputFormat, verbose: bool, quiet: bool) -> i32 {
    let result = match cmd {
        Commands::TestCoverage(tc) => match tc {
            TestCoverageCommands::Validate(args) => {
                test_coverage_validate::run(args, output_format)
            }
        },
        Commands::RepoGovernance(rg) => dispatch_repo_governance(rg, output_format),
        Commands::Md(mc) => dispatch_md(mc, output_format, verbose, quiet),
        Commands::Convention(cc) => dispatch_convention(cc, output_format),
        Commands::Harness(hc) => dispatch_harness(hc, output_format),
        Commands::Governance(gc) => dispatch_governance(gc, output_format),
        Commands::Specs(sc) => dispatch_specs(sc, output_format),
        Commands::RepoConfig(rc) => match rc {
            RepoConfigCommands::Validate(args) => repo_config_validate::run(args, output_format),
        },
        Commands::Gate(gc) => match gc {
            GateCommands::List(args) => gate::list::run(args, output_format),
            GateCommands::Emit(args) => gate::emit::run(args, output_format),
            GateCommands::Run(args) => gate::run::run(args, output_format),
            GateCommands::Validate(args) => gate::validate::run(args, output_format),
        },
        Commands::Git(gc) => match gc {
            GitCommands::Lockfile(lc) => match lc {
                GitLockfileCommands::Sync(args) => git::lockfile::run(args, output_format),
            },
        },
        Commands::Parity(pc) => match pc {
            ParityCommands::Manifest(mc) => match mc {
                ParityManifestCommands::Generate(args) => parity::generate(args, output_format),
                ParityManifestCommands::Validate(args) => parity::validate(args, output_format),
            },
        },
        Commands::Env(ec) => match ec {
            EnvCommands::Init(args) => env_init::run(args, output_format),
            EnvCommands::Backup(args) => env_backup::run(args, output_format),
            EnvCommands::Restore(args) => env_restore::run(args, output_format),
            EnvCommands::Validate(args) => env_validate::run(args, output_format),
            EnvCommands::StagedGuard(sc) => match sc {
                EnvStagedGuardCommands::Validate(args) => {
                    env_staged_guard::run(args, output_format)
                }
            },
        },
        Commands::Doctor(args) => doctor::run(args, output_format),
    };
    match result {
        Ok(()) => 0,
        Err(e) => {
            eprintln!("Error: {e}");
            1
        }
    }
}

/// Route a [`RepoGovernanceCommands`] variant to its handler.
///
/// # Errors
///
/// Propagates any error returned by the selected repo-governance subcommand.
fn dispatch_repo_governance(
    rg: &RepoGovernanceCommands,
    output_format: OutputFormat,
) -> std::result::Result<(), anyhow::Error> {
    match rg {
        RepoGovernanceCommands::Vendor(vc) => match vc {
            RepoGovernanceVendorCommands::Validate(args) => {
                governance_vendor_audit::run(args, output_format)
            }
        },
        RepoGovernanceCommands::LayerCoherence(lcc) => match lcc {
            RepoGovernanceLayerCoherenceCommands::Validate(args) => {
                governance_layer_coherence::run(args, output_format)
            }
        },
        RepoGovernanceCommands::Traceability(tc) => match tc {
            RepoGovernanceTraceabilityCommands::Validate(args) => {
                governance_traceability_audit::run(args, output_format)
            }
        },
        RepoGovernanceCommands::Audit(args) => governance_audit::run(args, output_format),
    }
}

/// Route a [`MdCommands`] variant to its handler.
///
/// # Errors
///
/// Propagates any error returned by the selected md subcommand.
fn dispatch_md(
    mc: &MdCommands,
    output_format: OutputFormat,
    verbose: bool,
    quiet: bool,
) -> std::result::Result<(), anyhow::Error> {
    match mc {
        MdCommands::Links(lc) => match lc {
            MdLinksCommands::Validate(args) => md_validate_links::run(args, output_format),
        },
        MdCommands::Mermaid(mc) => match mc {
            MdMermaidCommands::Validate(args) => {
                md_validate_mermaid::run(args, output_format, verbose, quiet)
            }
        },
        MdCommands::HeadingHierarchy(hc) => match hc {
            MdHeadingHierarchyCommands::Validate(args) => {
                md_validate_heading_hierarchy::run(args, output_format)
            }
        },
        MdCommands::Naming(nc) => match nc {
            MdNamingCommands::Validate(args) => md_validate_naming::run(args, output_format),
        },
        MdCommands::Frontmatter(fc) => match fc {
            MdFrontmatterCommands::Validate(args) => {
                md_validate_frontmatter::run(args, output_format)
            }
        },
        MdCommands::FrontmatterDates(fdc) => match fdc {
            MdFrontmatterDatesCommands::Validate(args) => {
                md_validate_frontmatter_dates::run(args, output_format)
            }
        },
        MdCommands::Audit(args) => md_audit::run(args, output_format),
    }
}

/// Route a [`GovernanceCommands`] variant to its handler.
///
/// # Errors
///
/// Propagates any error returned by the selected governance subcommand.
fn dispatch_governance(
    gc: &GovernanceCommands,
    output_format: OutputFormat,
) -> std::result::Result<(), anyhow::Error> {
    match gc {
        GovernanceCommands::WordBudget(wc) => match wc {
            GovernanceWordBudgetCommands::Validate(args) => {
                governance_validate_word_budget::run(args, output_format)
            }
        },
        GovernanceCommands::ReadmeIndex(ric) => match ric {
            GovernanceReadmeIndexCommands::Validate(args) => {
                governance_validate_readme_index::run(args, output_format)
            }
            GovernanceReadmeIndexCommands::Generate(args) => {
                governance_generate_readme_index::run(args, output_format)
            }
            GovernanceReadmeIndexCommands::RewritePaths(args) => {
                governance_rewrite_readme_index_paths::run(args, output_format)
            }
        },
    }
}

/// Route a [`ConventionCommands`] variant to its handler.
///
/// # Errors
///
/// Propagates any error returned by the selected convention subcommand.
fn dispatch_convention(
    cc: &ConventionCommands,
    output_format: OutputFormat,
) -> std::result::Result<(), anyhow::Error> {
    match cc {
        ConventionCommands::Emoji(ec) => match ec {
            ConventionEmojiCommands::Validate(args) => {
                convention_validate_emoji::run(args, output_format)
            }
        },
        ConventionCommands::License(lc) => match lc {
            ConventionLicenseCommands::Validate(args) => {
                convention_validate_license::run(args, output_format)
            }
        },
        ConventionCommands::Audit(args) => convention_audit::run(args, output_format),
    }
}

/// Route a [`HarnessCommands`] variant to its handler.
///
/// # Errors
///
/// Propagates any error returned by the selected harness subcommand.
fn dispatch_harness(
    hc: &HarnessCommands,
    output_format: OutputFormat,
) -> std::result::Result<(), anyhow::Error> {
    match hc {
        HarnessCommands::Duplication(dc) => match dc {
            HarnessDuplicationCommands::Validate(args) => {
                harness_validate_duplication::run(args, output_format)
            }
        },
        HarnessCommands::Claude(cc) => match cc {
            HarnessClaudeCommands::Validate(args) => {
                harness_validate_claude::run(args, output_format)
            }
        },
        HarnessCommands::Sync(sc) => match sc {
            HarnessSyncCommands::Validate(args) => harness_validate_sync::run(args, output_format),
            HarnessSyncCommands::Triage(args) => harness_sync_triage::run(args),
            HarnessSyncCommands::Promote(args) => harness_sync_promote::run(args),
        },
        HarnessCommands::Catalog(cc) => match cc {
            HarnessCatalogCommands::Generate(args) => {
                harness_catalog::run_generate(args, output_format)
            }
            HarnessCatalogCommands::Validate(args) => {
                harness_catalog::run_validate(args, output_format)
            }
        },
        HarnessCommands::Ownership(oc) => match oc {
            HarnessOwnershipCommands::Validate(args) => {
                harness_validate_ownership::run(args, output_format)
            }
        },
        HarnessCommands::Bindings(bc) => match bc {
            HarnessBindingsCommands::Validate(args) => {
                harness_validate_bindings::run(args, output_format)
            }
            HarnessBindingsCommands::Generate(args) => {
                harness_generate_bindings::run(args, output_format)
            }
        },
        HarnessCommands::Audit(args) => harness_audit::run(args, output_format),
    }
}

/// Route a [`SpecsCommands`] variant to its handler.
///
/// # Errors
///
/// Propagates any error returned by the selected specs subcommand.
fn dispatch_specs(
    sc: &SpecsCommands,
    output_format: OutputFormat,
) -> std::result::Result<(), anyhow::Error> {
    match sc {
        SpecsCommands::GherkinCardinality(gc) => match gc {
            SpecsGherkinCardinalityCommands::Validate(args) => {
                specs_gherkin_cardinality::run(args, output_format)
            }
        },
        SpecsCommands::Structure(sc) => match sc {
            SpecsStructureCommands::Validate(args) => {
                specs_structure_validate::run(args, output_format)
            }
        },
        SpecsCommands::Counts(cc) => match cc {
            SpecsCountsCommands::Validate(args) => specs_validate_counts::run(args, output_format),
        },
        SpecsCommands::BehaviorCoverage(bc) => match bc {
            SpecsBehaviorCoverageCommands::Validate(args) => {
                specs_coverage::run(args, output_format)
            }
        },
        SpecsCommands::E2eCoverage(ec) => match ec {
            SpecsE2eCoverageCommands::Validate(args) => {
                specs_e2e_coverage::run(args, output_format)
            }
        },
        SpecsCommands::DomainCoverage(dc) => match dc {
            SpecsDomainCoverageCommands::Validate(args) => {
                specs_coverage::run_domain(args, output_format)
            }
        },
        SpecsCommands::Scaffold(sc) => match sc {
            SpecsScaffoldCommands::Dart(args) => specs_scaffold_dart::run(args, output_format),
        },
        SpecsCommands::Audit(args) => specs_audit::run(args, output_format),
    }
}

/// Print the top-level help message to stdout and return exit code `0`.
fn print_help_and_exit() -> i32 {
    let mut cmd = <Cli as clap::CommandFactory>::command();
    cmd.print_help().ok();
    println!();
    0
}

#[cfg(test)]
mod cli_uniform_grammar_tests {
    use super::Cli;
    use clap::Parser;

    // --- OLD dash-form tests: must FAIL (dash-separated old form removed in P9b) ---

    #[test]
    fn old_md_validate_mermaid_fails() {
        let result = Cli::try_parse_from(["rhino-cli", "md", "validate-mermaid"]);
        assert!(
            result.is_err(),
            "md validate-mermaid should no longer parse"
        );
    }

    #[test]
    fn old_harness_detect_duplication_fails() {
        let result = Cli::try_parse_from(["rhino-cli", "harness", "detect-duplication"]);
        assert!(
            result.is_err(),
            "harness detect-duplication should no longer parse"
        );
    }

    #[test]
    fn old_repo_governance_vendor_audit_fails() {
        let result = Cli::try_parse_from(["rhino-cli", "repo-governance", "vendor-audit"]);
        assert!(
            result.is_err(),
            "repo-governance vendor-audit should no longer parse"
        );
    }

    #[test]
    fn old_specs_coverage_fails() {
        let result = Cli::try_parse_from(["rhino-cli", "specs", "coverage"]);
        assert!(result.is_err(), "specs coverage should no longer parse");
    }

    // --- P9b verb-middle forms: must FAIL after §2a-names verb-last rename ---

    #[test]
    fn new_md_validate_mermaid_passes() {
        // After §2a-names: md validate mermaid (verb-middle) is removed; md mermaid validate is
        // the new form.
        let result = Cli::try_parse_from(["rhino-cli", "md", "validate", "mermaid"]);
        assert!(
            result.is_err(),
            "md validate mermaid must no longer parse after verb-last rename (use: md mermaid validate)"
        );
    }

    #[test]
    fn new_harness_sync_opencode_passes() {
        // After §2a-names: harness sync opencode is removed (merged into harness bindings generate).
        let result = Cli::try_parse_from(["rhino-cli", "harness", "sync", "opencode"]);
        assert!(
            result.is_err(),
            "harness sync opencode must no longer parse (use: harness bindings generate --harness opencode)"
        );
    }

    #[test]
    fn new_repo_governance_validate_vendor_passes() {
        // After §2a-names: repo-governance validate vendor (verb-middle) is removed.
        let result = Cli::try_parse_from(["rhino-cli", "repo-governance", "validate", "vendor"]);
        assert!(
            result.is_err(),
            "repo-governance validate vendor must no longer parse after verb-last rename (use: repo-governance vendor validate)"
        );
    }

    // --- P9b new uniform forms: must PASS (already verb-last) ---

    #[test]
    fn new_specs_behavior_coverage_validate_passes() {
        // behavior-coverage validate requires ≥2 positional args; supply dummy paths.
        let result = Cli::try_parse_from([
            "rhino-cli",
            "specs",
            "behavior-coverage",
            "validate",
            "specs/",
            "apps/",
        ]);
        assert!(
            result.is_ok(),
            "specs behavior-coverage validate must parse: {:?}",
            result.err()
        );
    }

    // --- P1-1b rename: new form must PASS, old form must FAIL after rename ---

    #[test]
    fn specs_behavior_coverage_validate_passes_after_rename() {
        // coverage requires ≥2 positional args; supply dummy paths so parse succeeds.
        let result = Cli::try_parse_from([
            "rhino-cli",
            "specs",
            "behavior-coverage",
            "validate",
            "specs/",
            "apps/",
        ]);
        assert!(
            result.is_ok(),
            "specs behavior-coverage validate must parse after rename: {:?}",
            result.err()
        );
    }

    #[test]
    fn specs_validate_coverage_no_longer_parses_after_rename() {
        let result = Cli::try_parse_from([
            "rhino-cli",
            "specs",
            "validate",
            "coverage",
            "specs/",
            "apps/",
        ]);
        assert!(
            result.is_err(),
            "specs validate coverage must no longer parse after rename to behavior-coverage"
        );
    }

    // --- P1-1b-RED2: specs domain-coverage validate must parse after implementation ---

    #[test]
    fn specs_domain_coverage_validate_parses() {
        // domain-coverage validate requires ≥2 positional args; supply dummy paths.
        let result = Cli::try_parse_from([
            "rhino-cli",
            "specs",
            "domain-coverage",
            "validate",
            "specs/",
            "apps/",
        ]);
        assert!(
            result.is_ok(),
            "specs domain-coverage validate must parse after implementation: {:?}",
            result.err()
        );
    }

    // --- P1-1b-RED3: specs structure validate merged command + old leaves removed ---

    #[test]
    fn specs_structure_validate_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "specs", "structure", "validate"]);
        assert!(
            result.is_ok(),
            "specs structure validate must parse after merge: {:?}",
            result.err()
        );
    }

    #[test]
    fn specs_validate_adoption_no_longer_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "specs", "validate", "adoption"]);
        assert!(
            result.is_err(),
            "specs validate adoption must no longer parse after merge into specs structure validate"
        );
    }

    #[test]
    fn specs_validate_tree_no_longer_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "specs", "validate", "tree"]);
        assert!(
            result.is_err(),
            "specs validate tree must no longer parse after merge into specs structure validate"
        );
    }

    #[test]
    fn specs_validate_counts_no_longer_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "specs", "validate", "counts"]);
        assert!(
            result.is_err(),
            "specs validate counts must no longer parse after merge into specs structure validate"
        );
    }

    // --- P1-1b-RED5: specs validate bc / specs validate ul removed from CLI ---

    // --- P1-1b-RED6: specs validate links removed from CLI ---

    #[test]
    fn specs_validate_links_no_longer_parses() {
        // RED: specs validate links must not parse after the command is deleted in GREEN6.
        let result =
            Cli::try_parse_from(["rhino-cli", "specs", "validate", "links", "specs/apps/x"]);
        assert!(
            result.is_err(),
            "specs validate links must no longer parse after command removed in GREEN6"
        );
    }

    #[test]
    fn specs_validate_bc_no_longer_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "specs", "validate", "bc", "my-app"]);
        assert!(
            result.is_err(),
            "specs validate bc must no longer parse after bc check merged into specs structure validate"
        );
    }

    // --- P1-1b-RED7: env staged-guard validate not yet wired ---

    #[test]
    fn env_staged_guard_validate_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "env", "staged-guard", "validate"]);
        assert!(
            result.is_ok(),
            "env staged-guard validate must parse after wired in GREEN7; got error"
        );
    }

    #[test]
    fn specs_validate_ul_no_longer_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "specs", "validate", "ul", "my-app"]);
        assert!(
            result.is_err(),
            "specs validate ul must no longer parse after ul check merged into specs structure validate"
        );
    }

    // --- test-coverage validate is live in the union command surface ---

    #[test]
    fn test_coverage_validate_still_parses() {
        let result =
            Cli::try_parse_from(["rhino-cli", "test-coverage", "validate", "cover.xml", "90"]);
        assert!(
            result.is_ok(),
            "test-coverage validate must parse (union command surface): {:?}",
            result.err()
        );
    }

    // --- §2a-names GREEN: verb-last new forms must PASS ---

    #[test]
    fn verb_last_convention_emoji_validate_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "convention", "emoji", "validate", "."]);
        assert!(
            result.is_ok(),
            "convention emoji validate must parse after verb-last rename: {:?}",
            result.err()
        );
    }

    #[test]
    fn verb_last_harness_bindings_validate_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "harness", "bindings", "validate"]);
        assert!(
            result.is_ok(),
            "harness bindings validate must parse after verb-last rename: {:?}",
            result.err()
        );
    }

    #[test]
    fn verb_last_governance_word_budget_validate_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "governance", "word-budget", "validate"]);
        assert!(
            result.is_ok(),
            "governance word-budget validate must parse after cross-domain move: {:?}",
            result.err()
        );
    }

    #[test]
    fn old_harness_instruction_size_validate_no_longer_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "harness", "instruction-size", "validate"]);
        assert!(
            result.is_err(),
            "harness instruction-size validate must no longer parse after the cross-domain \
             move to governance word-budget validate"
        );
    }

    #[test]
    fn verb_last_governance_readme_index_validate_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "governance", "readme-index", "validate"]);
        assert!(
            result.is_ok(),
            "governance readme-index validate must parse after cross-domain move: {:?}",
            result.err()
        );
    }

    #[test]
    fn governance_readme_index_generate_parses() {
        // FR-3.12: `governance readme-index generate` is a new subcommand
        // alongside `validate`, following the same `harness bindings
        // generate`/`validate` pairing pattern.
        let result = Cli::try_parse_from(["rhino-cli", "governance", "readme-index", "generate"]);
        assert!(
            result.is_ok(),
            "governance readme-index generate must parse: {:?}",
            result.err()
        );
    }

    #[test]
    fn governance_readme_index_generate_accepts_paths_and_exclude_flags() {
        let result = Cli::try_parse_from([
            "rhino-cli",
            "governance",
            "readme-index",
            "generate",
            "--paths",
            "repo-governance/",
            "--exclude",
            "plans/",
        ]);
        assert!(
            result.is_ok(),
            "governance readme-index generate must accept --paths/--exclude: {:?}",
            result.err()
        );
    }

    #[test]
    fn old_md_readme_index_validate_no_longer_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "md", "readme-index", "validate"]);
        assert!(
            result.is_err(),
            "md readme-index validate must no longer parse after the cross-domain move to \
             governance readme-index validate"
        );
    }

    #[test]
    fn verb_last_harness_bindings_generate_with_harness_flag_parses() {
        let result = Cli::try_parse_from([
            "rhino-cli",
            "harness",
            "bindings",
            "generate",
            "--harness",
            "opencode",
        ]);
        assert!(
            result.is_ok(),
            "harness bindings generate --harness opencode must parse: {:?}",
            result.err()
        );
    }

    // --- §2a-names GREEN: old verb-middle forms must FAIL ---

    #[test]
    fn verb_middle_convention_validate_emoji_no_longer_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "convention", "validate", "emoji", "."]);
        assert!(
            result.is_err(),
            "convention validate emoji must no longer parse after verb-last rename"
        );
    }

    #[test]
    fn verb_middle_harness_validate_bindings_no_longer_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "harness", "validate", "bindings"]);
        assert!(
            result.is_err(),
            "harness validate bindings must no longer parse after verb-last rename"
        );
    }

    #[test]
    fn verb_middle_convention_validate_instruction_size_no_longer_parses() {
        let result =
            Cli::try_parse_from(["rhino-cli", "convention", "validate", "instruction-size"]);
        assert!(
            result.is_err(),
            "convention validate instruction-size must no longer parse (cross-domain moved to \
             governance word-budget validate)"
        );
    }

    #[test]
    fn verb_middle_harness_validate_instruction_size_no_longer_parses() {
        let result = Cli::try_parse_from(["rhino-cli", "harness", "validate", "instruction-size"]);
        assert!(
            result.is_err(),
            "harness validate instruction-size must no longer parse (cross-domain moved to \
             governance word-budget validate)"
        );
    }

    #[test]
    fn git_lockfile_sync_accepts_a_positional_path() {
        // Regression test for the clap parsing layer: `git lockfile sync <path>` previously
        // failed with an unexpected-argument error because SyncArgs declared no positional
        // field. This parses through the real `Cli` type (not `sync_at_root` directly) so it
        // actually exercises the layer that broke.
        use super::{Commands, GitCommands, GitLockfileCommands};

        let result = Cli::try_parse_from([
            "rhino-cli",
            "git",
            "lockfile",
            "sync",
            "apps/example/package.json",
        ]);
        let cli = result.expect("git lockfile sync must accept a positional path argument");
        assert!(
            matches!(
                cli.command,
                Some(Commands::Git(GitCommands::Lockfile(
                    GitLockfileCommands::Sync(_)
                )))
            ),
            "expected `git lockfile sync` to parse into its own args, got {:?}",
            cli.command
        );
        if let Some(Commands::Git(GitCommands::Lockfile(GitLockfileCommands::Sync(args)))) =
            cli.command
        {
            assert_eq!(
                args.positional,
                vec!["apps/example/package.json".to_string()]
            );
        }
    }
}
