//! `specs e2e-coverage validate` — detects Gherkin scenarios that
//! playwright-bdd's `missingSteps: "skip-scenario"` setting silently
//! converts to `test.fixme(...)` in generated `.spec.js` output, checked
//! against a per-project baseline manifest so only *new* unbound scenarios
//! fail the gate.
//!
//! Command wrapper (imperative shell) around the pure core in
//! `crate::application::e2e_coverage`. Models after the sibling
//! `commands/specs_coverage.rs`.

use std::collections::HashSet;
use std::fs;
use std::path::{Path, PathBuf};

use anyhow::{Context, Error, anyhow};
use clap::Args;
use walkdir::WalkDir;

use crate::application::e2e_coverage::types::{self, BaselineEntry, BaselineManifest};
use crate::application::e2e_coverage::{diff, parser, reporter};
use crate::domain::cliout::OutputFormat;

/// CLI arguments for `specs e2e-coverage validate`.
#[derive(Args, Debug)]
pub struct ValidateArgs {
    /// Project directory that `--features-gen` and `--baseline` are resolved
    /// relative to (defaults to the current working directory).
    #[arg(default_value = ".")]
    pub project_dir: String,
    /// Glob(s) of `.feature` files this project consumes, resolved relative
    /// to `project_dir` (repeatable).
    #[arg(long = "features", value_name = "GLOB")]
    pub features: Vec<String>,
    /// Directory containing playwright-bdd's generated `.spec.js` output
    /// (e.g. `.features-gen`, produced by `npx bddgen`), resolved relative
    /// to `project_dir`.
    #[arg(long = "features-gen", value_name = "DIR")]
    pub features_gen: String,
    /// Path to the checked-in baseline manifest, resolved relative to
    /// `project_dir`.
    #[arg(long = "baseline", value_name = "PATH")]
    pub baseline: String,
    /// Project name recorded on the baseline manifest when generated via
    /// `--update-baseline`.
    #[arg(long = "project", value_name = "NAME")]
    pub project: String,
    /// Snapshot the current unbound set to `--baseline` instead of
    /// validating against it.
    #[arg(long = "update-baseline")]
    pub update_baseline: bool,
}

/// Run the `specs e2e-coverage validate` command.
///
/// # Errors
///
/// Returns an error if the generated output directory is missing, a
/// `.feature` file cannot be read, the baseline manifest cannot be
/// read/parsed, or new unbound scenarios beyond the baseline are found.
pub fn run(args: &ValidateArgs, output_format: OutputFormat) -> std::result::Result<(), Error> {
    let project_dir = PathBuf::from(&args.project_dir);
    let features_gen_dir = project_dir.join(&args.features_gen);
    let baseline_path = project_dir.join(&args.baseline);

    let declared = collect_declared(&project_dir, &args.features)?;
    let fixme_titles = scan_fixme_dir(&features_gen_dir)?;

    // The scan only yields scenario *titles* (test.fixme carries no feature
    // path); reconstruct {feature, scenario} pairs by matching declared
    // scenarios whose title playwright-bdd marked fixme.
    let fixme: Vec<BaselineEntry> = declared
        .iter()
        .filter(|e| fixme_titles.contains(&e.scenario))
        .cloned()
        .collect();

    if args.update_baseline {
        let manifest = BaselineManifest {
            project: args.project.clone(),
            allowed_unbound: fixme,
        };
        types::save_baseline(&baseline_path, &manifest)?;
        println!("Wrote baseline manifest to {}", baseline_path.display());
        return Ok(());
    }

    let manifest = types::load_baseline(&baseline_path)?;
    let report = diff::diff(&declared, &fixme, &manifest.allowed_unbound);

    let output = match output_format {
        OutputFormat::Text => reporter::format_text(&report),
        OutputFormat::Json => reporter::format_json(&report)?,
        OutputFormat::Markdown => reporter::format_markdown(&report),
    };
    print!("{output}");

    if report.failed {
        return Err(anyhow!(
            "{} new unbound scenario(s) found beyond baseline",
            report.new_gaps.len()
        ));
    }
    Ok(())
}

/// Extracts the declared `@e2e` scenario set across every `--features` glob,
/// resolved relative to `project_dir`.
///
/// # Errors
///
/// Returns an error if a glob pattern is invalid or a matched `.feature`
/// file cannot be read.
fn collect_declared(
    project_dir: &Path,
    features: &[String],
) -> std::result::Result<Vec<BaselineEntry>, Error> {
    let mut declared = Vec::new();
    for pattern in features {
        let abs_pattern = project_dir.join(pattern);
        let pattern_str = abs_pattern
            .to_str()
            .ok_or_else(|| anyhow!("non-utf8 features glob {pattern:?}"))?;
        for entry in glob::glob(pattern_str)
            .with_context(|| format!("invalid --features glob pattern {pattern:?}"))?
        {
            let path =
                entry.with_context(|| format!("failed to read glob match for {pattern:?}"))?;
            let feature_path = path.to_string_lossy().to_string();
            declared.extend(parser::extract_declared(&path, &feature_path)?);
        }
    }
    Ok(declared)
}

/// Recursively scans `dir` for `test.fixme(...)` titles across every
/// generated `.spec.js` file (and any other file playwright-bdd wrote —
/// non-UTF-8 files are silently skipped).
///
/// # Errors
///
/// Returns an error if `dir` does not exist or a directory walk encounters
/// an I/O error.
fn scan_fixme_dir(dir: &Path) -> std::result::Result<HashSet<String>, Error> {
    if !dir.exists() {
        return Err(anyhow!(
            "generated output directory {} not found — run `npx bddgen` first to produce it",
            dir.display()
        ));
    }
    let mut titles = HashSet::new();
    for entry in WalkDir::new(dir) {
        let entry = entry?;
        if !entry.file_type().is_file() {
            continue;
        }
        let Ok(content) = fs::read_to_string(entry.path()) else {
            continue; // binary/non-UTF-8 files carry no test.fixme markers
        };
        titles.extend(parser::scan_fixme_titles(&content));
    }
    Ok(titles)
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::TempDir;

    /// Writes a project fixture: one `.feature` file with two `@e2e`
    /// scenarios ("A", "B"), and a `.features-gen` dir whose generated
    /// `.spec.js` marks both as `test.fixme`. Returns `(project_dir,
    /// baseline_path)`.
    fn write_fixture(root: &std::path::Path) -> (String, String) {
        let features_dir = root.join("features");
        fs::create_dir_all(&features_dir).unwrap();
        fs::write(
            features_dir.join("example.feature"),
            "@e2e\nScenario: A\n  Given a\n\n@e2e\nScenario: B\n  Given b\n",
        )
        .unwrap();

        let gen_dir = root.join(".features-gen");
        fs::create_dir_all(&gen_dir).unwrap();
        fs::write(
            gen_dir.join("example.spec.js"),
            "test.fixme(\"A\", async ({ page }) => {});\ntest.fixme(\"B\", async ({ page }) => {});\n",
        )
        .unwrap();

        (
            root.to_string_lossy().to_string(),
            "e2e-coverage-baseline.json".to_string(),
        )
    }

    fn base_args(project_dir: String, baseline: String) -> ValidateArgs {
        ValidateArgs {
            project_dir,
            features: vec!["features/*.feature".to_string()],
            features_gen: ".features-gen".to_string(),
            baseline,
            project: "test-project".to_string(),
            update_baseline: false,
        }
    }

    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature:First-time baseline generation snapshots current unbound scenarios
    #[test]
    fn update_baseline_writes_current_fixme_set() {
        let tmp = TempDir::new().unwrap();
        let (project_dir, baseline) = write_fixture(tmp.path());

        let mut args = base_args(project_dir.clone(), baseline.clone());
        args.update_baseline = true;
        run(&args, OutputFormat::Text).unwrap();

        let baseline_path = tmp.path().join(&baseline);
        assert!(baseline_path.exists(), "baseline manifest was not written");
        let content = fs::read_to_string(&baseline_path).unwrap();
        assert!(content.contains("\"A\""));
        assert!(content.contains("\"B\""));

        // A follow-up validate run (no --update-baseline) must now pass,
        // since the just-written baseline exactly matches the current
        // fixme set.
        let validate_args = base_args(project_dir, baseline);
        assert!(
            run(&validate_args, OutputFormat::Text).is_ok(),
            "follow-up validate should pass against the freshly written baseline"
        );
    }

    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature:The generated output directory is absent
    #[test]
    fn missing_features_gen_errors() {
        let tmp = TempDir::new().unwrap();
        let features_dir = tmp.path().join("features");
        fs::create_dir_all(&features_dir).unwrap();
        fs::write(
            features_dir.join("example.feature"),
            "@e2e\nScenario: A\n  Given a\n",
        )
        .unwrap();
        // Deliberately do NOT create `.features-gen` — this is the
        // "bddgen was never run" case.

        let args = base_args(
            tmp.path().to_string_lossy().to_string(),
            "e2e-coverage-baseline.json".to_string(),
        );

        let err = run(&args, OutputFormat::Text).unwrap_err();
        let msg = err.to_string();
        assert!(
            msg.contains(".features-gen"),
            "expected the missing directory to be named in the error, got: {msg}"
        );
        assert!(
            msg.contains("bddgen"),
            "expected the error to instruct running bddgen first, got: {msg}"
        );
    }
}
