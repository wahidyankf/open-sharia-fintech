//! Doctor use case — checks and optionally installs required development tools.
//!
//! Moved from `crate::internal::doctor`. Public API unchanged;
//! `crate::internal::doctor` re-exports everything from here.

mod checker;
mod fixer;
mod reporter;
mod target_share;
mod tools;

use std::time::Duration;

pub use checker::{check_all, real_runner};
pub use fixer::{FixOptions, FixResult, fix_all, format_fix_summary};
pub use reporter::{format_json, format_markdown, format_text};
pub use target_share::{
    FixOutcome, PruneOutcome, SweepOutcome, TargetShareStatus, cache_root_ambient,
    cargo_sweep_present, check_target_shares, fix_target_shares, is_ci_ambient, prune_orphans,
    repo_name, sweep_stale,
};

/// Health status of a tool check.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ToolStatus {
    /// The tool is present and its version satisfies the requirement.
    Ok,
    /// The tool is present but its version does not match the requirement.
    Warning,
    /// The tool binary was not found in `PATH`.
    Missing,
}

impl ToolStatus {
    /// Returns the stable string code for this status (`"ok"`, `"warning"`, or `"missing"`).
    pub fn code(self) -> &'static str {
        match self {
            ToolStatus::Ok => "ok",
            ToolStatus::Warning => "warning",
            ToolStatus::Missing => "missing",
        }
    }
}

/// Controls which tools the doctor checks.
///
/// `Full` checks every known tool.  `Minimal` restricts to the core set
/// required in almost every environment: `git`, `volta`, `node`, `npm`,
/// `docker`, and `jq`.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Scope {
    /// Check every tool in the full tool list.
    Full,
    /// Check only the minimal core tool set.
    Minimal,
}

impl Scope {
    /// Returns the stable string code for this scope (`"full"` or `"minimal"`).
    pub fn code(self) -> &'static str {
        match self {
            Scope::Full => "full",
            Scope::Minimal => "minimal",
        }
    }

    /// Parses a scope string.
    ///
    /// `""` or `"full"` returns `Some(Full)`.  `"minimal"` returns
    /// `Some(Minimal)`.  Any other value returns `None`.
    pub fn parse(s: &str) -> Option<Scope> {
        match s {
            "" | "full" => Some(Scope::Full),
            "minimal" => Some(Scope::Minimal),
            _ => None,
        }
    }
}

/// Returns `true` when `name` belongs to the minimal tool set.
///
/// The minimal set is: `git`, `volta`, `node`, `npm`, `docker`, `jq`.
pub fn is_minimal_tool(name: &str) -> bool {
    matches!(name, "git" | "volta" | "node" | "npm" | "docker" | "jq")
}

/// Result of checking a single tool against its version requirement.
#[derive(Debug, Clone)]
pub struct ToolCheck {
    /// Human-readable tool name (e.g. `"node"`, `"golang"`).
    pub name: String,
    /// Name of the executable that is invoked (e.g. `"node"`, `"go"`).
    pub binary: String,
    /// Whether the tool is present and at the right version.
    pub status: ToolStatus,
    /// Version string reported by the installed binary, or empty when missing.
    pub installed_version: String,
    /// Version string required by the project config, or empty when unconstrained.
    pub required_version: String,
    /// Config file that provides the required version (e.g. `"package.json → volta.node"`).
    pub source: String,
    /// Human-readable explanation of the status (e.g. `"required: 24.11.1, version mismatch"`).
    pub note: String,
}

/// Aggregated results from a full doctor run.
#[derive(Debug, Clone)]
pub struct DoctorResult {
    /// Individual check results, one per tool.
    pub checks: Vec<ToolCheck>,
    /// Number of tools with status [`ToolStatus::Ok`].
    pub ok_count: usize,
    /// Number of tools with status [`ToolStatus::Warning`].
    pub warn_count: usize,
    /// Number of tools with status [`ToolStatus::Missing`].
    pub missing_count: usize,
    /// Wall-clock time taken by [`check_all`].
    pub duration: Duration,
    /// Scope that was used for the run.
    pub scope: Scope,
}

/// Output of a command invocation: `(stdout, stderr, exit_code)`.
///
/// `Err` indicates the binary was not found in `PATH` (no process was started).
pub type CommandOutput = Result<(String, String, i32), String>;

/// Injectable command runner used for testing.
///
/// Signature: `fn(binary, args) -> CommandOutput`.
pub type CommandRunner<'a> = &'a dyn Fn(&str, &[&str]) -> CommandOutput;

/// Configuration passed to [`check_all`] and [`fix_all`].
pub struct CheckOptions<'a> {
    /// Absolute path to the repository root.
    pub repo_root: std::path::PathBuf,
    /// Optional command runner override; defaults to [`real_runner`] when `None`.
    pub runner: Option<CommandRunner<'a>>,
    /// Which tool set to check.
    pub scope: Scope,
}
