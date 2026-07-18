//! `specs e2e-coverage validate` — detects Gherkin scenarios that
//! playwright-bdd's `missingSteps: "skip-scenario"` setting silently
//! converts to `test.fixme(...)` in generated `.spec.js` output, checked
//! against a per-project baseline manifest so only *new* unbound scenarios
//! fail the gate.
//!
//! Command wrapper (imperative shell) around the pure core in
//! `crate::application::e2e_coverage`. Models after the sibling
//! `commands/specs_coverage.rs`.

use std::collections::{HashMap, HashSet};
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

    let declared_with_paths = collect_declared(&project_dir, &args.features)?;
    let fixme_by_file = scan_fixme_dir(&features_gen_dir)?;

    // The scan only yields scenario *titles* per generated file (test.fixme
    // carries no feature path of its own); reconstruct {feature, scenario}
    // pairs by matching each declared scenario against ONLY its own
    // originating generated file's fixme titles — never a flat, cross-file
    // title union. Scenario titles can legitimately repeat across different
    // `.feature` files (see `BaselineEntry`'s pairing invariant in
    // `types.rs`), and matching by title alone would falsely credit a
    // fully-implemented scenario as unbound whenever a same-titled scenario
    // elsewhere happens to be genuinely fixme'd. See `is_fixme` for the
    // per-file pairing logic.
    let fixme: Vec<BaselineEntry> = declared_with_paths
        .iter()
        .filter(|(feature_abs, entry)| is_fixme(feature_abs, &entry.scenario, &fixme_by_file))
        .map(|(_, entry)| entry.clone())
        .collect();
    let declared: Vec<BaselineEntry> = declared_with_paths.into_iter().map(|(_, e)| e).collect();

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
/// resolved relative to `project_dir`. Each entry is paired with the
/// canonical (symlink- and `..`-resolved) absolute path of its originating
/// `.feature` file — used only by [`is_fixme`] to pair the entry against the
/// correct generated `.spec.js` file's fixme titles; never persisted on
/// `BaselineEntry` itself, so baseline manifest compatibility is unaffected.
///
/// # Errors
///
/// Returns an error if a glob pattern is invalid, a matched `.feature` file
/// cannot be read, or its canonical path cannot be resolved.
fn collect_declared(
    project_dir: &Path,
    features: &[String],
) -> std::result::Result<Vec<(PathBuf, BaselineEntry)>, Error> {
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
            let canonical = path.canonicalize().with_context(|| {
                format!("failed to resolve canonical path for {}", path.display())
            })?;
            let feature_path = path.to_string_lossy().to_string();
            for scenario in parser::extract_declared(&path, &feature_path)? {
                declared.push((canonical.clone(), scenario));
            }
        }
    }
    Ok(declared)
}

/// Recursively scans `dir` for `test.fixme(...)` titles, keyed by each
/// generated `.spec.js` file's path relative to `dir` with the trailing
/// `.spec.js` suffix stripped (any other file playwright-bdd wrote —
/// non-UTF-8 files, or files with no `test.fixme` calls — is omitted).
///
/// playwright-bdd generates exactly one `.spec.js` per `.feature` file,
/// mirroring the directory structure below its `featuresRoot`; stripping the
/// `.spec.js` suffix therefore reconstructs that `.feature` file's path
/// relative to `featuresRoot`, which [`is_fixme`] matches as a
/// component-wise suffix of each declared entry's canonical absolute path.
///
/// # Errors
///
/// Returns an error if `dir` does not exist or a directory walk encounters
/// an I/O error.
fn scan_fixme_dir(dir: &Path) -> std::result::Result<HashMap<String, HashSet<String>>, Error> {
    if !dir.exists() {
        return Err(anyhow!(
            "generated output directory {} not found — run `npx bddgen` first to produce it",
            dir.display()
        ));
    }
    let mut by_file = HashMap::new();
    for entry in WalkDir::new(dir) {
        let entry = entry?;
        if !entry.file_type().is_file() {
            continue;
        }
        let Ok(content) = fs::read_to_string(entry.path()) else {
            continue; // binary/non-UTF-8 files carry no test.fixme markers
        };
        let titles: HashSet<String> = parser::scan_fixme_titles(&content).into_iter().collect();
        if titles.is_empty() {
            continue;
        }
        let Ok(rel) = entry.path().strip_prefix(dir) else {
            continue;
        };
        if let Some(mirror_key) = rel.to_string_lossy().strip_suffix(".spec.js") {
            by_file.insert(mirror_key.to_string(), titles);
        }
    }
    Ok(by_file)
}

/// Returns `true` when `scenario` is a `test.fixme` title in the ONE
/// generated file whose mirrored relative path matches `feature_abs`'s
/// trailing path segments — i.e. the specific generated file playwright-bdd
/// produced for this exact `.feature` file, never a different file that
/// happens to declare a same-titled scenario elsewhere (the bug this
/// per-file pairing fixes — see the `fixme` construction note in [`run`]).
fn is_fixme(
    feature_abs: &Path,
    scenario: &str,
    fixme_by_file: &HashMap<String, HashSet<String>>,
) -> bool {
    fixme_by_file.iter().any(|(mirror_key, titles)| {
        path_ends_with(feature_abs, mirror_key) && titles.contains(scenario)
    })
}

/// Returns `true` when `mirror_key`'s path components are an exact,
/// component-wise suffix of `path`'s components (e.g. `path`
/// `/repo/specs/x/foo.feature` matches `mirror_key` `specs/x/foo.feature` or
/// `x/foo.feature`, but never a partial path segment like `o/foo.feature`).
fn path_ends_with(path: &Path, mirror_key: &str) -> bool {
    let path_segments: Vec<_> = path.components().collect();
    let key_segments: Vec<_> = Path::new(mirror_key).components().collect();
    !key_segments.is_empty() && path_segments.ends_with(&key_segments)
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::TempDir;

    /// Writes a project fixture: one `.feature` file with two `@e2e`
    /// scenarios ("A", "B"), and a `.features-gen` dir whose generated
    /// `.spec.js` marks both as `test.fixme`. The generated file is named
    /// `example.feature.spec.js` (not `example.spec.js`) to match
    /// playwright-bdd's real naming convention — it keeps the `.feature`
    /// extension and appends `.spec.js` — which [`is_fixme`]'s file-pairing
    /// logic relies on. Returns `(project_dir, baseline_path)`.
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
            gen_dir.join("example.feature.spec.js"),
            "test.fixme(\"A\", async ({ page }) => {});\ntest.fixme(\"B\", async ({ page }) => {});\n",
        )
        .unwrap();

        (
            root.to_string_lossy().to_string(),
            "e2e-coverage-baseline.json".to_string(),
        )
    }

    /// Writes a project fixture reproducing the title-collision-across-files
    /// bug: two `.feature` files — `file1.feature`, `file2.feature` — each
    /// declaring an identically-titled `@e2e` scenario ("Same title"), but
    /// only `file1`'s generated output actually marks it `test.fixme`;
    /// `file2`'s is a normal, fully-implemented `test(...)`. A title-only
    /// match would (incorrectly) treat `file2`'s scenario as unbound too,
    /// since its title collides with `file1`'s genuinely-unbound one.
    /// Returns `(project_dir, baseline_path)`.
    fn write_collision_fixture(root: &std::path::Path) -> (String, String) {
        let features_dir = root.join("features");
        fs::create_dir_all(&features_dir).unwrap();
        fs::write(
            features_dir.join("file1.feature"),
            "@e2e\nScenario: Same title\n  Given a\n",
        )
        .unwrap();
        fs::write(
            features_dir.join("file2.feature"),
            "@e2e\nScenario: Same title\n  Given a\n",
        )
        .unwrap();

        let gen_dir = root.join(".features-gen");
        fs::create_dir_all(&gen_dir).unwrap();
        fs::write(
            gen_dir.join("file1.feature.spec.js"),
            "test.fixme(\"Same title\", async ({ page }) => {});\n",
        )
        .unwrap();
        fs::write(
            gen_dir.join("file2.feature.spec.js"),
            "test(\"Same title\", async ({ page }) => {});\n",
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

    /// Regression test for the title-collision-across-files bug: two
    /// `.feature` files declare an identically-titled `@e2e` scenario, but
    /// only ONE is genuinely `test.fixme`'d. Before the fix, `fixme` was
    /// reconstructed by matching declared entries against a flat,
    /// cross-file `HashSet<String>` of fixme titles — so `file2`'s
    /// fully-implemented "Same title" scenario was falsely reported as a
    /// new gap (2 gaps) purely because `file1` happens to declare a
    /// same-titled, genuinely-unbound scenario. After the fix, only
    /// `file1`'s scenario is a new gap (1 gap).
    #[test]
    fn fixme_reconstruction_does_not_collide_across_feature_files_with_same_scenario_title() {
        let tmp = TempDir::new().unwrap();
        let (project_dir, baseline) = write_collision_fixture(tmp.path());
        let args = base_args(project_dir, baseline);

        let err = run(&args, OutputFormat::Text).unwrap_err();
        let msg = err.to_string();

        assert!(
            msg.contains("1 new unbound scenario"),
            "expected exactly 1 new gap (file1's genuinely-unbound scenario only) — \
             file2's identically-titled but fully-implemented scenario must not be \
             falsely reported, got: {msg}"
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
