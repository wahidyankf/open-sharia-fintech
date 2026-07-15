//! Shared data types for the spec-coverage subsystem.
//!
//! Byte-for-byte port of `apps/rhino-cli/internal/speccoverage/types.go`.
//! All public types are `Clone` so callers can freely move results around
//! without holding references into the scanner internals.

use std::path::PathBuf;
use std::time::Duration;

/// Configuration options passed to the spec-coverage scanner.
///
/// Construct with [`Default`] and fill in the relevant fields before calling
/// [`super::checker::check_all`].
#[derive(Debug, Clone, Default)]
pub struct ScanOptions {
    /// Absolute path to the repository root, used to compute repo-relative paths
    /// in reported findings.
    pub repo_root: PathBuf,
    /// Legacy single-spec-tree input.
    ///
    /// When `specs_dirs` is non-empty it takes precedence over this field.
    pub specs_dir: PathBuf,
    /// Absolute paths to one or more spec trees walked together.
    ///
    /// When non-empty, overrides `specs_dir`.
    pub specs_dirs: Vec<PathBuf>,
    /// Absolute path to the application source directory walked for test/step files.
    pub app_dir: PathBuf,
    /// Emit verbose output when set to `true`.
    pub verbose: bool,
    /// Suppress all output when set to `true`.
    pub quiet: bool,
    /// When `true`, treat all step definitions as shared across all feature files
    /// instead of requiring a 1-to-1 filename mapping.
    pub shared_steps: bool,
    /// Directory names to skip during the feature-file walk.
    pub exclude_dirs: Vec<String>,
    /// Directory names to skip during the `app_dir` source walk (step-definition
    /// extraction and 1-to-1 test-file matching), in addition to the built-in
    /// universal skip set.
    ///
    /// Kept separate from `exclude_dirs`: the two walks scan different trees
    /// (spec files vs. application source) and a directory name can be a
    /// legitimate spec-organization folder in one tree while also being a
    /// legitimate app-source folder name in the other (e.g. a Gherkin
    /// directory named `content/` grouping content-API scenarios coexisting
    /// with a Next.js `content/` content-layer directory) — collapsing them
    /// into one flag would make excluding one tree silently exclude the
    /// other.
    pub exclude_source_dirs: Vec<String>,
}

/// A feature file that has no corresponding test/step file in the app directory.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CoverageGap {
    /// Repo-relative path to the `.feature` file.
    pub spec_file: String,
    /// File stem derived from `spec_file` (e.g. `"user-login"` from `user-login.feature`).
    pub stem: String,
}

/// A Gherkin scenario that is absent from the corresponding test file.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ScenarioGap {
    /// Repo-relative path to the `.feature` file containing the missing scenario.
    pub spec_file: String,
    /// Title of the scenario that has no matching test.
    pub scenario_title: String,
}

/// A single Gherkin step that has no matching step-definition implementation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StepGap {
    /// Repo-relative path to the `.feature` file containing the unimplemented step.
    pub spec_file: String,
    /// Title of the scenario that owns this step.
    pub scenario_title: String,
    /// Gherkin keyword for the step (e.g. `"Given"`, `"When"`, `"Then"`).
    pub step_keyword: String,
    /// Step text without the leading keyword.
    pub step_text: String,
}

/// A step-definition entry that matches no Gherkin step in any scanned feature file.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct OrphanStepImpl {
    /// Repo-relative path to the file containing the orphan step definition.
    pub file: String,
    /// How the step was matched: `"exact"` or `"pattern"`.
    pub matcher_kind: String,
    /// The literal text or regex pattern of the orphan definition.
    pub matcher_text: String,
}

/// Aggregated result returned by [`super::checker::check_all`].
#[derive(Debug, Clone, Default)]
pub struct CheckResult {
    /// Total number of `.feature` files scanned.
    pub total_specs: usize,
    /// Total number of scenarios encountered across all feature files.
    pub total_scenarios: usize,
    /// Total number of steps encountered across all scenarios.
    pub total_steps: usize,
    /// Feature files with no matching test file (1-to-1 mode only).
    pub gaps: Vec<CoverageGap>,
    /// Scenarios present in feature files but absent from the test file.
    pub scenario_gaps: Vec<ScenarioGap>,
    /// Steps present in feature files but without a matching step definition.
    pub step_gaps: Vec<StepGap>,
    /// Step definitions that match no Gherkin step in the scanned feature files.
    pub orphan_step_impls: Vec<OrphanStepImpl>,
    /// Wall-clock time taken by the scan.
    pub duration: Duration,
}
