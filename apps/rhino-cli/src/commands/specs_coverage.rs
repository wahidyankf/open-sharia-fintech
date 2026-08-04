//! `specs coverage` — checks that Gherkin spec steps are covered by test implementations.
//!
//! Port of `apps/rhino-cli/cmd/spec_coverage_validate.go`.
//! Same args (positional specs-dirs + final app-dir), same flags, same exit
//! codes, same byte-for-byte output.

use std::path::{Path, PathBuf};

use anyhow::{Context, Error, anyhow};
use clap::Args;

use crate::application::behavior_coverage::extract::{
    extract_covers_markers, extract_scenario_specs,
};
use crate::application::behavior_coverage::types::{
    BehaviorCoverageViolation, ProjectEnvelope, RuntimeCoverageViolation, TestLevel,
};
use crate::application::behavior_coverage::validator;
use crate::domain::cliout::OutputFormat;
use crate::internal::git;
use crate::internal::speccoverage::{checker, reporter, runtime_check, types::ScanOptions};

/// CLI arguments for `spec-coverage validate`.
#[derive(Args, Debug)]
pub struct ValidateArgs {
    /// Last positional arg is the app-dir; preceding args are specs-dirs.
    /// Must supply ≥2 positional args.
    #[arg(required = true, num_args = 2..)]
    pub paths: Vec<String>,
    /// Skip file matching; validate steps across ALL source files.
    #[arg(long = "shared-steps")]
    pub shared_steps: bool,
    /// Spec directory names to exclude from the `.feature`-file walk (repeatable).
    #[arg(long = "exclude-dir", value_name = "DIR")]
    pub exclude_dir: Vec<String>,
    /// App-dir directory names to exclude from the step-implementation source
    /// walk (repeatable). Separate from `--exclude-dir`: a name can be a
    /// legitimate spec-organization folder in the spec tree while also being
    /// a legitimate app-source folder name (e.g. a Next.js content-layer
    /// `content/` directory holding step-decorator-shaped teaching examples).
    #[arg(long = "exclude-source-dir", value_name = "DIR")]
    pub exclude_source_dir: Vec<String>,
    /// Directory containing unit test implementations (three-level mode).
    #[arg(long = "unit-dir", value_name = "DIR")]
    pub unit_dir: Option<String>,
    /// Directory containing integration test implementations (three-level mode).
    #[arg(long = "integration-dir", value_name = "DIR")]
    pub integration_dir: Option<String>,
    /// Directory containing e2e test implementations (three-level mode).
    #[arg(long = "e2e-dir", value_name = "DIR")]
    pub e2e_dir: Option<String>,
    /// Machine-readable run-report JSON for the unit tier's `@covers` scenarios
    /// (three-level mode only; runtime cross-check is skipped for a tier with
    /// no report supplied).
    #[arg(long = "unit-report", value_name = "PATH")]
    pub unit_report: Option<String>,
    /// Machine-readable run-report JSON for the integration tier's `@covers`
    /// scenarios (three-level mode only; see `--unit-report`).
    #[arg(long = "integration-report", value_name = "PATH")]
    pub integration_report: Option<String>,
    /// Machine-readable run-report JSON for the e2e tier's `@covers` scenarios
    /// (three-level mode only; see `--unit-report`).
    #[arg(long = "e2e-report", value_name = "PATH")]
    pub e2e_report: Option<String>,
}

/// Level name paired with its absolute directory path.
struct LevelDir {
    /// Short name used in diagnostic output (e.g. `"unit"`, `"integration"`, `"e2e"`).
    name: &'static str,
    /// The [`TestLevel`] this level dir represents, for the `@covers`
    /// runtime cross-check.
    test_level: TestLevel,
    /// Absolute path to the directory that contains the level's test implementations.
    dir: PathBuf,
    /// Absolute path to this level's machine-readable run-report JSON, if supplied.
    report: Option<PathBuf>,
}

/// Determine whether all three level dirs are provided, none, or a partial set.
///
/// Returns `Some(vec)` when all three are present, `None` when none are present,
/// and an `Err` when only some are provided.
fn resolve_level_dirs(
    args: &ValidateArgs,
    repo_root: &Path,
) -> std::result::Result<Option<Vec<LevelDir>>, Error> {
    let count = [&args.unit_dir, &args.integration_dir, &args.e2e_dir]
        .iter()
        .filter(|o| o.is_some())
        .count();

    match count {
        0 => Ok(None),
        3 => Ok(Some(vec![
            LevelDir {
                name: "unit",
                test_level: TestLevel::Unit,
                dir: repo_root.join(
                    args.unit_dir
                        .as_deref()
                        .expect("unit_dir is Some in count==3 arm"),
                ),
                report: args.unit_report.as_deref().map(|p| repo_root.join(p)),
            },
            LevelDir {
                name: "integration",
                test_level: TestLevel::Integration,
                dir: repo_root.join(
                    args.integration_dir
                        .as_deref()
                        .expect("integration_dir is Some in count==3 arm"),
                ),
                report: args
                    .integration_report
                    .as_deref()
                    .map(|p| repo_root.join(p)),
            },
            LevelDir {
                name: "e2e",
                test_level: TestLevel::E2e,
                dir: repo_root.join(
                    args.e2e_dir
                        .as_deref()
                        .expect("e2e_dir is Some in count==3 arm"),
                ),
                report: args.e2e_report.as_deref().map(|p| repo_root.join(p)),
            },
        ])),
        _ => Err(anyhow!(
            "must provide all three or none of --unit-dir, --integration-dir, --e2e-dir"
        )),
    }
}

/// Check coverage for a single level; print prefixed output and return whether gaps exist.
fn run_level_check(
    level: &LevelDir,
    specs_dirs: &[PathBuf],
    repo_root: &Path,
    args: &ValidateArgs,
    output_format: OutputFormat,
) -> std::result::Result<bool, Error> {
    println!("=== {} level ===", capitalize(level.name));

    let opts = ScanOptions {
        repo_root: repo_root.to_path_buf(),
        specs_dir: specs_dirs[0].clone(),
        specs_dirs: specs_dirs.to_vec(),
        app_dir: level.dir.clone(),
        verbose: false,
        quiet: false,
        shared_steps: args.shared_steps,
        exclude_dirs: args.exclude_dir.clone(),
        exclude_source_dirs: args.exclude_source_dir.clone(),
    };

    let result = checker::check_all(&opts)
        .with_context(|| format!("spec coverage check failed for {} level", level.name))?;

    let output = match output_format {
        OutputFormat::Text => reporter::format_text(&result, false, false),
        OutputFormat::Json => reporter::format_json(&result)?,
        OutputFormat::Markdown => reporter::format_markdown(&result),
    };
    print!("{output}");

    let has_gaps = !result.gaps.is_empty()
        || !result.scenario_gaps.is_empty()
        || !result.step_gaps.is_empty()
        || !result.orphan_step_impls.is_empty();

    if has_gaps && matches!(output_format, OutputFormat::Text) {
        eprintln!(
            "\nERROR: [{}] spec coverage gaps found: {} file gap(s), {} scenario gap(s), {} step gap(s), {} orphan step impl(s)",
            level.name,
            result.gaps.len(),
            result.scenario_gaps.len(),
            result.step_gaps.len(),
            result.orphan_step_impls.len()
        );
    }

    Ok(has_gaps)
}

/// Capitalize the first character of `s`, leaving the rest unchanged.
fn capitalize(s: &str) -> String {
    let mut chars = s.chars();
    match chars.next() {
        None => String::new(),
        Some(first) => first.to_uppercase().collect::<String>() + chars.as_str(),
    }
}

/// Run three-level mode: one pass per level dir, fail if any level has gaps.
///
/// After the per-level step-text traceability pass, also runs the `@covers`
/// marker-existence + level-envelope check
/// ([`crate::application::behavior_coverage::validator::validate`]) and the
/// runtime execution cross-check
/// ([`crate::application::speccoverage::runtime_check::check_runtime`]) —
/// the only mode where a per-scenario "level" has a concrete meaning (one
/// directory per level), so these checks are scoped to three-level mode and
/// leave every existing single-dir/shared-steps invocation unaffected.
fn run_three_level(
    levels: &[LevelDir],
    specs_dirs: &[PathBuf],
    repo_root: &Path,
    args: &ValidateArgs,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let mut failing_levels: Vec<&'static str> = Vec::new();

    for level in levels {
        let has_gaps = run_level_check(level, specs_dirs, repo_root, args, output_format)?;
        if has_gaps {
            failing_levels.push(level.name);
        }
    }

    // The `@covers` marker-existence and runtime-execution checks are opt-in:
    // they activate only when at least one `--<level>-report` is supplied.
    // Without that gate, every pre-existing three-level-mode caller (none of
    // which tag scenarios with `@unit`/`@integration`/`@e2e` today) would
    // start failing on `UntaggedScenario` violations it never opted into.
    let covers_enabled = levels.iter().any(|level| level.report.is_some());
    let (marker_violations, runtime_violations) = if covers_enabled {
        (
            check_covers_markers(levels, specs_dirs, repo_root)?,
            check_runtime_cross_check(levels, repo_root)?,
        )
    } else {
        (Vec::new(), Vec::new())
    };

    if matches!(output_format, OutputFormat::Text) {
        print_marker_violations(&marker_violations);
        print_runtime_violations(&runtime_violations);
    }

    if failing_levels.is_empty() && marker_violations.is_empty() && runtime_violations.is_empty() {
        return Ok(());
    }

    let mut parts = Vec::new();
    if !failing_levels.is_empty() {
        parts.push(format!("level(s) {}", failing_levels.join(", ")));
    }
    if !marker_violations.is_empty() {
        parts.push(format!(
            "{} @covers marker violation(s)",
            marker_violations.len()
        ));
    }
    if !runtime_violations.is_empty() {
        parts.push(format!(
            "{} runtime cross-check violation(s)",
            runtime_violations.len()
        ));
    }
    Err(anyhow!("spec coverage gaps found: {}", parts.join("; ")))
}

/// Extracts every scenario in `specs_dirs` and every `@covers` marker across
/// `levels`, then runs the marker-existence + level-envelope check.
///
/// The project envelope in three-level mode is exactly the three declared
/// levels (`--unit-dir`/`--integration-dir`/`--e2e-dir` are required
/// together, per [`resolve_level_dirs`]).
///
/// # Errors
///
/// Returns an error if a `.feature` file cannot be read or a level directory
/// cannot be walked.
fn check_covers_markers(
    levels: &[LevelDir],
    specs_dirs: &[PathBuf],
    repo_root: &Path,
) -> std::result::Result<Vec<BehaviorCoverageViolation>, Error> {
    let mut scenarios = Vec::new();
    for specs_dir in specs_dirs {
        for feature_file in checker::walk_feature_files(specs_dir, &[])? {
            let feature_path = feature_file.strip_prefix(repo_root).map_or_else(
                |_| feature_file.to_string_lossy().to_string(),
                |p| p.to_string_lossy().to_string(),
            );
            scenarios.extend(extract_scenario_specs(&feature_file, &feature_path)?);
        }
    }

    let mut markers = Vec::new();
    for level in levels {
        markers.extend(extract_covers_markers(
            &level.dir,
            level.test_level,
            repo_root,
        )?);
    }

    let envelope = ProjectEnvelope {
        levels: [TestLevel::Unit, TestLevel::Integration, TestLevel::E2e]
            .into_iter()
            .collect(),
    };

    Ok(validator::validate(&scenarios, &markers, &envelope))
}

/// Builds one [`runtime_check::TierInput`] per level and runs the runtime
/// execution cross-check.
///
/// # Errors
///
/// Returns an error if a level directory cannot be walked or a supplied
/// run-report cannot be read/parsed.
fn check_runtime_cross_check(
    levels: &[LevelDir],
    repo_root: &Path,
) -> std::result::Result<Vec<RuntimeCoverageViolation>, Error> {
    let tiers: Vec<runtime_check::TierInput<'_>> = levels
        .iter()
        .map(|level| runtime_check::TierInput {
            level: level.test_level,
            source_dir: level.dir.as_path(),
            run_report: level.report.as_deref(),
            repo_root,
        })
        .collect();
    runtime_check::check_runtime(&tiers)
}

/// Prints every `@covers` marker-existence violation to stdout, in the same
/// detailed-listing style as [`crate::application::speccoverage::reporter::format_text`]'s
/// gap sections (`print_marker_violations`) — the terse pass/fail summary
/// still surfaces separately via the command's returned `Err` message.
fn print_marker_violations(violations: &[BehaviorCoverageViolation]) {
    use BehaviorCoverageViolation as V;
    if violations.is_empty() {
        return;
    }
    println!("\n@covers marker violations ({}):", violations.len());
    for v in violations {
        match v {
            V::UntaggedScenario {
                feature_path,
                title,
            } => println!(
                "  - {feature_path}\n    → Scenario: \"{title}\" has no @unit/@integration/@e2e level tag"
            ),
            V::LevelOutsideEnvelope {
                feature_path,
                title,
                required_level,
            } => println!(
                "  - {feature_path}\n    → Scenario: \"{title}\" requires level [{required_level}], which is outside the project envelope"
            ),
            V::MissingCoverage {
                feature_path,
                title,
                missing_level,
            } => println!(
                "  - {feature_path}\n    → Scenario: \"{title}\" has no @covers marker at the [{missing_level}] level"
            ),
            V::CoverageAtUndeclaredLevel {
                source_file,
                feature_path,
                title,
                extra_level,
            } => println!(
                "  - {source_file}\n    → marks \"{title}\" ({feature_path}) covered at [{extra_level}], a level not declared on that scenario"
            ),
            V::OrphanMarker {
                source_file,
                feature_path,
                scenario_title,
            } => println!(
                "  - {source_file}\n    → marks \"{scenario_title}\" ({feature_path}), which no feature file contains (orphan marker)"
            ),
        }
    }
}

/// Prints every runtime cross-check violation to stdout, in the same
/// detailed-listing style as [`print_marker_violations`].
fn print_runtime_violations(violations: &[RuntimeCoverageViolation]) {
    if violations.is_empty() {
        return;
    }
    println!("\nRuntime cross-check violations ({}):", violations.len());
    for v in violations {
        match v {
            RuntimeCoverageViolation::NotExecuted {
                source_file,
                feature_path,
                scenario_title,
                level,
            } => println!(
                "  - {feature_path}\n    → Scenario: \"{scenario_title}\" [{level}] marked-but-not-executed (marker: {source_file})"
            ),
            RuntimeCoverageViolation::Failed {
                source_file,
                feature_path,
                scenario_title,
                level,
            } => println!(
                "  - {feature_path}\n    → Scenario: \"{scenario_title}\" [{level}] marked-but-failed (marker: {source_file})"
            ),
        }
    }
}

/// Run the `spec-coverage validate` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, fewer than 2 paths are
/// supplied, the coverage check fails, or spec coverage gaps are found.
pub fn run(args: &ValidateArgs, output_format: OutputFormat) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;

    if args.paths.len() < 2 {
        return Err(anyhow!(
            "spec-coverage validate requires at least 2 positional args (specs-dir... app-dir)"
        ));
    }

    let specs_dirs: Vec<PathBuf> = args.paths[..args.paths.len() - 1]
        .iter()
        .map(|sd| repo_root.join(sd))
        .collect();

    // Resolve three-level mode vs. single-dir mode.
    let level_dirs = resolve_level_dirs(args, &repo_root)?;

    if let Some(levels) = level_dirs {
        return run_three_level(&levels, &specs_dirs, &repo_root, args, output_format);
    }

    // Single-dir (backward-compatible) mode.
    let app_dir: PathBuf = repo_root.join(&args.paths[args.paths.len() - 1]);

    let opts = ScanOptions {
        repo_root: repo_root.clone(),
        specs_dir: specs_dirs[0].clone(), // primary for backward compat
        specs_dirs: specs_dirs.clone(),
        app_dir,
        verbose: false,
        quiet: false,
        shared_steps: args.shared_steps,
        exclude_dirs: args.exclude_dir.clone(),
        exclude_source_dirs: args.exclude_source_dir.clone(),
    };

    let result = checker::check_all(&opts).context("spec coverage check failed")?;

    let output = match output_format {
        OutputFormat::Text => reporter::format_text(&result, false, false),
        OutputFormat::Json => reporter::format_json(&result)?,
        OutputFormat::Markdown => reporter::format_markdown(&result),
    };
    print!("{output}");

    let has_gaps = !result.gaps.is_empty()
        || !result.scenario_gaps.is_empty()
        || !result.step_gaps.is_empty()
        || !result.orphan_step_impls.is_empty();

    if has_gaps {
        if matches!(output_format, OutputFormat::Text) {
            if !result.gaps.is_empty() {
                eprintln!(
                    "\nERROR: Found {} spec(s) without matching test files",
                    result.gaps.len()
                );
            }
            if !result.scenario_gaps.is_empty() {
                eprintln!(
                    "ERROR: Found {} scenario(s) without matching test implementations",
                    result.scenario_gaps.len()
                );
            }
            if !result.step_gaps.is_empty() {
                eprintln!(
                    "ERROR: Found {} step(s) without matching step definitions",
                    result.step_gaps.len()
                );
            }
            if !result.orphan_step_impls.is_empty() {
                eprintln!(
                    "ERROR: Found {} orphan step implementation(s) (no Gherkin step matches them)",
                    result.orphan_step_impls.len()
                );
            }
        }
        return Err(anyhow!(
            "spec coverage gaps found: {} file gap(s), {} scenario gap(s), {} step gap(s), {} orphan step impl(s)",
            result.gaps.len(),
            result.scenario_gaps.len(),
            result.step_gaps.len(),
            result.orphan_step_impls.len()
        ));
    }
    Ok(())
}

/// Run the `specs domain-coverage validate` command.
///
/// Gates the scan on `repo-config.yml`'s `specs.domain-areas` allowlist via
/// [`crate::application::domain_coverage::is_eligible`]: a project absent from
/// that list is skipped (exit 0) rather than silently duplicating
/// `specs behavior-coverage validate`'s full scan. An eligible project still
/// runs the same underlying scan as behavior-coverage today — no `domain/`
/// subfolder split exists yet in any repo's spec tree to further scope the
/// scan via [`crate::application::domain_coverage::filter_domain_scenarios`];
/// that path-based filter has nothing to act on until such content is
/// physically split out, which is a content-authoring decision tracked as a
/// separate follow-up, not a mechanical wiring change.
///
/// # Errors
///
/// Returns an error under the same conditions as [`run`], for eligible projects.
pub fn run_domain(
    args: &ValidateArgs,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;

    let project_name = args
        .paths
        .last()
        .map(Path::new)
        .and_then(|p| p.file_name())
        .and_then(|n| n.to_str())
        .ok_or_else(|| anyhow!("could not derive project name from the final app-dir path"))?;

    let config = crate::application::repo_config::load_or_default(&repo_root);
    if !crate::application::domain_coverage::is_eligible(project_name, &config.specs.domain_areas) {
        let message = format!(
            "specs domain-coverage validate: skipped — \"{project_name}\" is not listed in repo-config.yml's specs.domain-areas"
        );
        match output_format {
            OutputFormat::Text => println!("{message}"),
            OutputFormat::Json => println!(
                "{{\"skipped\":true,\"project\":\"{project_name}\",\"reason\":\"not in specs.domain-areas\"}}"
            ),
            OutputFormat::Markdown => println!("- {message}"),
        }
        return Ok(());
    }

    run(args, output_format)
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::test_support::CwdLock;
    use std::process::Command;
    use tempfile::TempDir;

    /// Initializes a bare-minimum git repo at `root` (no commit required —
    /// `git rev-parse --show-toplevel` only needs a `.git` directory).
    fn init_git_repo(root: &Path) {
        let status = Command::new("git")
            .args(["init"])
            .current_dir(root)
            .status()
            .expect("git init");
        assert!(status.success(), "git init must succeed");
    }

    /// Writes a spec dir with one scenario ("a real step") and an app dir
    /// containing both a matching step implementation (`src/real_steps.rs`)
    /// and an orphan step implementation under a directory named `content`
    /// (`content/legacy_steps.py`, matching no Gherkin step) — the same
    /// content-vs-spec-tree name collision the `--exclude-source-dir` flag
    /// exists to resolve.
    ///
    /// Returns `(specs_dir_rel, app_dir_rel)`, the two path args callers pass
    /// as [`ValidateArgs::paths`] (relative to `root`, which becomes the repo
    /// root once `init_git_repo` + `set_current_dir` have run).
    fn write_exclude_source_dir_fixture(root: &Path) -> (String, String) {
        let specs_dir = root.join("specs");
        std::fs::create_dir_all(&specs_dir).unwrap();
        std::fs::write(
            specs_dir.join("example.feature"),
            "Feature: Example\n  Scenario: A scenario\n    Given a real step\n",
        )
        .unwrap();

        let app_dir = root.join("app");
        std::fs::create_dir_all(app_dir.join("content")).unwrap();
        std::fs::write(
            app_dir.join("content/legacy_steps.py"),
            "@given(\"a taught condition\")\ndef given_taught():\n    pass\n",
        )
        .unwrap();
        std::fs::create_dir_all(app_dir.join("src")).unwrap();
        std::fs::write(
            app_dir.join("src/real_steps.rs"),
            "#[given(\"a real step\")]\nfn given_real() {}\n",
        )
        .unwrap();

        ("specs".to_string(), "app".to_string())
    }

    #[test]
    fn run_honors_exclude_source_dir_end_to_end() {
        let _cwd = CwdLock::acquire();
        let repo = TempDir::new().unwrap();
        let root = repo.path();
        init_git_repo(root);
        let (specs_dir, app_dir) = write_exclude_source_dir_fixture(root);
        std::env::set_current_dir(root).expect("chdir to temp repo root");

        let mut args = base_args(vec![specs_dir, app_dir]);
        args.shared_steps = true;

        // Without --exclude-source-dir, the app-tree walk picks up the Python
        // step decorator under `content/`. It matches no Gherkin step, so it
        // surfaces as an orphan step impl and run() fails.
        let err = run(&args, OutputFormat::Text).unwrap_err();
        assert!(
            err.to_string().contains("1 orphan step impl"),
            "expected an orphan-step-impl gap from the unexcluded content/ dir, got: {err}"
        );

        // With --exclude-source-dir content, args.exclude_source_dir must be
        // threaded into opts.exclude_source_dirs (specs_coverage.rs's run()),
        // excluding content/ from the app-tree walk so only the matching
        // `real_steps.rs` step implementation remains.
        args.exclude_source_dir = vec!["content".to_string()];
        assert!(
            run(&args, OutputFormat::Text).is_ok(),
            "expected --exclude-source-dir content to exclude the app-tree content/ dir end-to-end"
        );
    }

    #[test]
    fn run_level_check_honors_exclude_source_dir_end_to_end() {
        let _cwd = CwdLock::acquire();
        let repo = TempDir::new().unwrap();
        let root = repo.path();
        init_git_repo(root);
        let (specs_dir, level_dir) = write_exclude_source_dir_fixture(root);
        std::env::set_current_dir(root).expect("chdir to temp repo root");

        let mut args = ValidateArgs {
            paths: vec![specs_dir, level_dir.clone()],
            shared_steps: true,
            exclude_dir: vec![],
            exclude_source_dir: vec![],
            unit_dir: Some(level_dir.clone()),
            integration_dir: Some(level_dir.clone()),
            e2e_dir: Some(level_dir),
            unit_report: None,
            integration_report: None,
            e2e_report: None,
        };

        // Without --exclude-source-dir, every level's scan sees the same
        // orphan step impl under content/, so run_level_check (invoked once
        // per level by run_three_level) reports every level as failing.
        let err = run(&args, OutputFormat::Text).unwrap_err();
        assert!(
            err.to_string().contains("level(s)"),
            "expected all three levels to fail from the unexcluded content/ dir, got: {err}"
        );

        // With --exclude-source-dir content, args.exclude_source_dir must be
        // threaded into opts.exclude_source_dirs inside run_level_check too,
        // so every level's scan excludes content/ and passes.
        args.exclude_source_dir = vec!["content".to_string()];
        assert!(
            run(&args, OutputFormat::Text).is_ok(),
            "expected --exclude-source-dir content to exclude the app-tree content/ dir in three-level mode"
        );
    }

    fn base_args(paths: Vec<String>) -> ValidateArgs {
        ValidateArgs {
            paths,
            shared_steps: false,
            exclude_dir: vec![],
            exclude_source_dir: vec![],
            unit_dir: None,
            integration_dir: None,
            e2e_dir: None,
            unit_report: None,
            integration_report: None,
            e2e_report: None,
        }
    }

    #[test]
    fn validate_args_requires_two_paths_min() {
        let args = base_args(vec!["only-one".to_string()]);
        assert!(args.paths.len() < 2);
    }

    #[test]
    fn run_returns_err_on_too_few_paths() {
        let _cwd = CwdLock::acquire();
        let args = base_args(vec!["x".to_string()]);
        let err = run(&args, OutputFormat::Text).unwrap_err();
        assert!(err.to_string().contains("requires at least 2"));
    }

    #[test]
    fn run_returns_err_with_gaps_when_specs_missing_test_files() {
        let _cwd = CwdLock::acquire();
        let mut args = base_args(vec![
            "specs/apps/rhino/behavior/rhino-cli/gherkin".to_string(),
            "apps/rhino-cli/scripts".to_string(), // wrong dir → 0 step matchers → step gaps
        ]);
        args.shared_steps = true;
        let err = run(&args, OutputFormat::Text).unwrap_err();
        assert!(err.to_string().contains("spec coverage gaps found"));
    }

    #[test]
    fn run_returns_err_with_json_output_format() {
        let _cwd = CwdLock::acquire();
        let mut args = base_args(vec![
            "specs/apps/rhino/behavior/rhino-cli/gherkin".to_string(),
            "apps/rhino-cli/scripts".to_string(),
        ]);
        args.shared_steps = true;
        let err = run(&args, OutputFormat::Json).unwrap_err();
        assert!(err.to_string().contains("spec coverage gaps found"));
    }

    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/domain-coverage.feature:A project not in the domain-areas allowlist is skipped
    #[test]
    fn run_domain_skips_project_not_in_domain_areas() {
        let _cwd = CwdLock::acquire();
        // "rhino-cli" is not listed in repo-config.yml's specs.domain-areas.
        let args = base_args(vec![
            "specs/apps/rhino/behavior/rhino-cli/gherkin".to_string(),
            "apps/rhino-cli".to_string(),
        ]);
        let result = run_domain(&args, OutputFormat::Text);
        assert!(
            result.is_ok(),
            "expected Ok (skipped) for a non-domain-area project, got {result:?}"
        );
    }

    #[test]
    fn run_domain_runs_full_scan_for_eligible_project() {
        let _cwd = CwdLock::acquire();
        // "ose-be" IS listed in repo-config.yml's specs.domain-areas — falls through to run().
        let mut args = base_args(vec![
            "specs/apps/ose/behavior/be/gherkin".to_string(),
            "apps/ose-be".to_string(),
        ]);
        args.shared_steps = true;
        args.exclude_dir = vec!["messaging".to_string()];
        let result = run_domain(&args, OutputFormat::Text);
        assert!(
            result.is_ok(),
            "expected the real scan to pass for ose-be (matches its existing Nx target), got {result:?}"
        );
    }

    #[test]
    fn three_level_fails_when_integration_and_e2e_missing() {
        let _cwd = CwdLock::acquire();
        let args = ValidateArgs {
            paths: vec![
                "apps/rhino-cli/tests/fixtures/three-level".to_string(),
                "apps/rhino-cli/tests/fixtures/three-level/unit".to_string(),
            ],
            shared_steps: true,
            exclude_dir: vec![],
            exclude_source_dir: vec![],
            unit_dir: Some("apps/rhino-cli/tests/fixtures/three-level/unit".to_string()),
            integration_dir: Some(
                "apps/rhino-cli/tests/fixtures/three-level/integration".to_string(),
            ),
            e2e_dir: Some("apps/rhino-cli/tests/fixtures/three-level/e2e".to_string()),
            unit_report: None,
            integration_report: None,
            e2e_report: None,
        };
        let result = run(&args, OutputFormat::Text);
        assert!(
            result.is_err(),
            "three-level check should fail when integration/e2e dirs are empty"
        );
        let msg = result.unwrap_err().to_string();
        assert!(
            msg.contains("integration") || msg.contains("e2e"),
            "error should mention missing level, got: {msg}"
        );
    }

    #[test]
    fn three_level_passes_when_all_levels_covered() {
        let _cwd = CwdLock::acquire();
        let args = ValidateArgs {
            paths: vec![
                "apps/rhino-cli/tests/fixtures/three-level".to_string(),
                "apps/rhino-cli/tests/fixtures/three-level/unit".to_string(),
            ],
            shared_steps: true,
            exclude_dir: vec![],
            exclude_source_dir: vec![],
            unit_dir: Some("apps/rhino-cli/tests/fixtures/three-level/unit".to_string()),
            integration_dir: Some("apps/rhino-cli/tests/fixtures/three-level/unit".to_string()),
            e2e_dir: Some("apps/rhino-cli/tests/fixtures/three-level/unit".to_string()),
            unit_report: None,
            integration_report: None,
            e2e_report: None,
        };
        assert!(
            run(&args, OutputFormat::Text).is_ok(),
            "three-level check should pass when all levels have step implementations"
        );
    }

    #[test]
    fn partial_level_dirs_returns_err() {
        let _cwd = CwdLock::acquire();
        let args = ValidateArgs {
            paths: vec![
                "apps/rhino-cli/tests/fixtures/three-level".to_string(),
                "apps/rhino-cli/tests/fixtures/three-level/unit".to_string(),
            ],
            shared_steps: true,
            exclude_dir: vec![],
            exclude_source_dir: vec![],
            unit_dir: Some("apps/rhino-cli/tests/fixtures/three-level/unit".to_string()),
            integration_dir: None,
            e2e_dir: None,
            unit_report: None,
            integration_report: None,
            e2e_report: None,
        };
        let err = run(&args, OutputFormat::Text).unwrap_err();
        assert!(
            err.to_string().contains("must provide all three or none"),
            "partial flags should return error, got: {err}"
        );
    }

    #[test]
    #[ignore = "Real-corpus Gherkin coverage is blocked on the deferred Rust cucumber harness. \
                This test previously passed only because it aggregated the archived/rhino-cli Go step \
                defs, which have now been removed; apps/rhino-cli alone does not yet implement the \
                step definitions. Re-enable once the Rust cucumber harness lands."]
    fn run_returns_ok_on_real_rhino_cli_gherkin() {
        // Runs against the actual repo state. The Rust port's cucumber step definitions are not yet
        // implemented (tracked as deferred work), so the real Gherkin corpus is not fully covered by
        // apps/rhino-cli alone. Ignored until the harness is implemented.
        let _cwd = CwdLock::acquire();
        let args = ValidateArgs {
            paths: vec![
                "specs/apps/rhino/behavior/rhino-cli/gherkin".to_string(),
                "apps/rhino-cli".to_string(),
            ],
            shared_steps: true,
            exclude_dir: vec![],
            exclude_source_dir: vec![],
            unit_dir: None,
            integration_dir: None,
            e2e_dir: None,
            unit_report: None,
            integration_report: None,
            e2e_report: None,
        };
        assert!(run(&args, OutputFormat::Text).is_ok());
    }
}
