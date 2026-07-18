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
    /// to `project_dir` (repeatable). Required — `clap` rejects an omitted
    /// flag, but cannot detect a *provided* glob that matches zero files
    /// (e.g. after a directory rename); [`run`] guards against that case
    /// explicitly.
    #[arg(long = "features", value_name = "GLOB", required = true)]
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
/// Returns an error if `--features` matches zero `.feature` files (e.g. a
/// misconfigured glob), the generated output directory is missing, a
/// `.feature` file cannot be read, the baseline manifest cannot be
/// read/parsed, or new unbound scenarios beyond the baseline are found.
pub fn run(args: &ValidateArgs, output_format: OutputFormat) -> std::result::Result<(), Error> {
    let project_dir = PathBuf::from(&args.project_dir);
    let features_gen_dir = project_dir.join(&args.features_gen);
    let baseline_path = project_dir.join(&args.baseline);

    let (declared_with_paths, any_feature_file_matched) =
        collect_declared(&project_dir, &args.features)?;
    // `scan_fixme_dir` runs (and may error on a missing `.features-gen`)
    // BEFORE the empty-glob guard below — a missing generated-output
    // directory is a more specific, more actionable diagnostic than an
    // empty `--features` match, and both conditions can hold at once (e.g.
    // `bddgen` was simply never run against a freshly scaffolded project).
    let fixme_by_file = scan_fixme_dir(&features_gen_dir)?;
    if !any_feature_file_matched {
        return Err(anyhow!(
            "--features matched no .feature files across glob(s) {:?} — \
             check for a path typo or directory rename (an empty declared set \
             would otherwise make this gate always silently pass)",
            args.features
        ));
    }

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
/// Also returns whether ANY `.feature` file matched at least one glob —
/// distinct from whether any `@e2e`-tagged scenario was declared. A project
/// whose matched `.feature` files genuinely contain zero `@e2e` scenarios
/// (all `@unit`/`@integration`) is a legitimate empty-declared-set state that
/// must still pass the gate; only a glob matching NO FILES AT ALL (an
/// omitted flag already caught by `clap`, or a misconfigured/renamed path)
/// is the misconfiguration `run` guards against — see the caller.
///
/// # Errors
///
/// Returns an error if a glob pattern is invalid, a matched `.feature` file
/// cannot be read, or its canonical path cannot be resolved.
fn collect_declared(
    project_dir: &Path,
    features: &[String],
) -> std::result::Result<(Vec<(PathBuf, BaselineEntry)>, bool), Error> {
    let mut declared = Vec::new();
    let mut any_feature_file_matched = false;
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
            any_feature_file_matched = true;
            let canonical = path.canonicalize().with_context(|| {
                format!("failed to resolve canonical path for {}", path.display())
            })?;
            let feature_path = path.to_string_lossy().to_string();
            for scenario in parser::extract_declared(&path, &feature_path)? {
                declared.push((canonical.clone(), scenario));
            }
        }
    }
    Ok((declared, any_feature_file_matched))
}

/// Recursively scans `dir` for unbound scenario titles, keyed by EVERY
/// generated `.spec.js` file's path relative to `dir` with the trailing
/// `.spec.js` suffix stripped — including files with an empty title set
/// (fully bound, no unbound scenarios at all). A file's title set is the
/// union of its plain `test.fixme(...)` call titles (a bare `Scenario:`) and
/// its `test.describe(...)` block titles that wrap at least one nested
/// `test.fixme` (a `Scenario Outline:` — see
/// [`parser::scan_unbound_describe_titles`]). Any other file playwright-bdd
/// wrote that isn't itself named `*.spec.js` is omitted; a `.spec.js` file
/// that happens to be non-UTF-8 is recorded with an empty title set rather
/// than omitted entirely (see [`is_fixme`] for why recording bound files
/// matters).
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
        let Ok(rel) = entry.path().strip_prefix(dir) else {
            continue;
        };
        let Some(mirror_key) = rel
            .to_string_lossy()
            .strip_suffix(".spec.js")
            .map(str::to_string)
        else {
            continue; // not a generated .spec.js file
        };
        let titles: HashSet<String> = match fs::read_to_string(entry.path()) {
            // Union of two independent unbound-title sources: plain
            // `test.fixme(...)` call titles (covers a bare `Scenario:`), and
            // `test.describe(...)` block titles that wrap at least one
            // nested `test.fixme` (covers a `Scenario Outline:` — see
            // `scan_unbound_describe_titles`'s doc comment for why a plain
            // title-only scan can never see an unbound Outline).
            Ok(content) => parser::scan_fixme_titles(&content)
                .into_iter()
                .chain(parser::scan_unbound_describe_titles(&content))
                .collect(),
            // binary/non-UTF-8 .spec.js carries no readable test.fixme
            // markers, but the file itself must still be recorded (with an
            // empty title set) so it can out-compete a shorter, unrelated
            // suffix match in `is_fixme`.
            Err(_) => HashSet::new(),
        };
        by_file.insert(mirror_key, titles);
    }
    Ok(by_file)
}

/// Returns `true` when `scenario` is an unbound title (a plain `test.fixme`
/// call title, or a `Scenario Outline`'s wrapping `describe` title — see
/// [`scan_fixme_dir`]) in the SINGLE generated file playwright-bdd actually
/// produced for this exact `.feature` file — resolved as the LONGEST (most
/// specific) mirror key among all generated files whose mirrored relative
/// path is a component-wise suffix of `feature_abs`.
///
/// Two different `.feature` files can share a tail directory/basename
/// sequence at different nesting depths (e.g. `features/a/foo.feature` and
/// `features/b/a/foo.feature` both have a mirror key `a/foo.feature`, which
/// is a *suffix* of `features/b/a/foo.feature`'s canonical path); accepting
/// ANY suffix match (rather than the longest one) would let the shallower,
/// unrelated file's fixme titles falsely bind to the deeper file's scenario.
/// Preferring the longest match disambiguates this — combined with
/// [`scan_fixme_dir`] now recording EVERY generated file (bound or unbound),
/// a fully-bound file at a deeper nesting depth is never invisible to this
/// resolution, so it always wins over a shorter, unrelated suffix match. This
/// is the per-file pairing this function exists for — see the `fixme`
/// construction note in [`run`].
fn is_fixme(
    feature_abs: &Path,
    scenario: &str,
    fixme_by_file: &HashMap<String, HashSet<String>>,
) -> bool {
    fixme_by_file
        .keys()
        .filter(|mirror_key| path_ends_with(feature_abs, mirror_key))
        .max_by_key(|mirror_key| Path::new(mirror_key).components().count())
        .is_some_and(|mirror_key| fixme_by_file[mirror_key].contains(scenario))
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

    /// Writes a project fixture reproducing the directory-nesting variant of
    /// the title-collision bug: two `.feature` files — `features/a/foo.feature`
    /// and `features/b/a/foo.feature` — share a tail directory/basename
    /// sequence (`a/foo.feature`) at different nesting depths, and both
    /// declare an identically-titled `@e2e` scenario ("Same title"). Only
    /// the shallower file (`a/foo.feature`) is genuinely `test.fixme`'d;
    /// the deeper one (`b/a/foo.feature`) is a normal, fully-implemented
    /// `test(...)`. A naive "any component-wise suffix match" would treat
    /// `a/foo.feature`'s mirror key as a match for BOTH files (since it's a
    /// trailing-path suffix of `b/a/foo.feature` too), falsely reporting the
    /// fully-implemented deeper scenario as unbound. Returns
    /// `(project_dir, baseline_path)`.
    fn write_nested_directory_collision_fixture(root: &std::path::Path) -> (String, String) {
        let features_dir = root.join("features");
        fs::create_dir_all(features_dir.join("a")).unwrap();
        fs::create_dir_all(features_dir.join("b/a")).unwrap();
        fs::write(
            features_dir.join("a/foo.feature"),
            "@e2e\nScenario: Same title\n  Given a\n",
        )
        .unwrap();
        fs::write(
            features_dir.join("b/a/foo.feature"),
            "@e2e\nScenario: Same title\n  Given a\n",
        )
        .unwrap();

        let gen_dir = root.join(".features-gen");
        fs::create_dir_all(gen_dir.join("a")).unwrap();
        fs::create_dir_all(gen_dir.join("b/a")).unwrap();
        fs::write(
            gen_dir.join("a/foo.feature.spec.js"),
            "test.fixme(\"Same title\", async ({ page }) => {});\n",
        )
        .unwrap();
        fs::write(
            gen_dir.join("b/a/foo.feature.spec.js"),
            "test(\"Same title\", async ({ page }) => {});\n",
        )
        .unwrap();

        (
            root.to_string_lossy().to_string(),
            "e2e-coverage-baseline.json".to_string(),
        )
    }

    /// Writes a project fixture reproducing the Scenario-Outline blind-spot
    /// bug: one `.feature` file with an `@e2e Scenario Outline` whose
    /// Examples table has 2 rows, and a `.features-gen` dir whose generated
    /// `.spec.js` wraps the two Examples-row tests — titled `Example #1`/
    /// `Example #2` per playwright-bdd's default Examples-title convention,
    /// never the outline's own title — in a `test.describe` block titled
    /// with the outline's raw title. ONE of the two rows is `test.fixme`.
    /// Returns `(project_dir, baseline_path)`.
    fn write_outline_fixture(root: &std::path::Path) -> (String, String) {
        let features_dir = root.join("features");
        fs::create_dir_all(&features_dir).unwrap();
        fs::write(
            features_dir.join("example.feature"),
            "@e2e\nScenario Outline: Renders the field correctly\n  Given a field\n\n  Examples:\n    | field |\n    | name  |\n    | email |\n",
        )
        .unwrap();

        let gen_dir = root.join(".features-gen");
        fs::create_dir_all(&gen_dir).unwrap();
        fs::write(
            gen_dir.join("example.feature.spec.js"),
            "test.describe('Renders the field correctly', () => {\n  test.fixme('Example #1', async ({ page }) => {\n  });\n  test('Example #2', async ({ page }) => {\n  });\n});\n",
        )
        .unwrap();

        (
            root.to_string_lossy().to_string(),
            "e2e-coverage-baseline.json".to_string(),
        )
    }

    /// Negative counterpart of [`write_outline_fixture`]: the SAME outline,
    /// but BOTH Examples rows are ordinary, fully-implemented `test(...)`
    /// calls — zero `test.fixme` anywhere. Returns `(project_dir,
    /// baseline_path)`.
    fn write_fully_bound_outline_fixture(root: &std::path::Path) -> (String, String) {
        let features_dir = root.join("features");
        fs::create_dir_all(&features_dir).unwrap();
        fs::write(
            features_dir.join("example.feature"),
            "@e2e\nScenario Outline: Renders the field correctly\n  Given a field\n\n  Examples:\n    | field |\n    | name  |\n    | email |\n",
        )
        .unwrap();

        let gen_dir = root.join(".features-gen");
        fs::create_dir_all(&gen_dir).unwrap();
        fs::write(
            gen_dir.join("example.feature.spec.js"),
            "test.describe('Renders the field correctly', () => {\n  test('Example #1', async ({ page }) => {\n  });\n  test('Example #2', async ({ page }) => {\n  });\n});\n",
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

    /// Regression test for the directory-nesting variant of the
    /// title-collision bug (distinct from
    /// `fixme_reconstruction_does_not_collide_across_feature_files_with_same_scenario_title`,
    /// which only covers same-depth files). `features/a/foo.feature` and
    /// `features/b/a/foo.feature` share a tail path (`a/foo.feature`) at
    /// different nesting depths and declare an identically-titled `@e2e`
    /// scenario; only the shallower file is genuinely `test.fixme`'d. Before
    /// the fix, `is_fixme` accepted ANY component-wise suffix match, so
    /// `b/a/foo.feature`'s scenario spuriously resolved to `a/foo.feature`'s
    /// mirror key (a fully-bound generated file for `b/a/foo.feature` was
    /// never even recorded, since `scan_fixme_dir` skipped files with no
    /// `test.fixme` calls) — reporting 2 false gaps. After the fix
    /// (longest-match resolution over a `fixme_by_file` map that records
    /// every generated file, bound or unbound), only `a/foo.feature`'s
    /// genuinely-unbound scenario is a new gap (1 gap).
    #[test]
    fn fixme_reconstruction_does_not_collide_across_nested_directories_with_same_tail_path() {
        let tmp = TempDir::new().unwrap();
        let (project_dir, baseline) = write_nested_directory_collision_fixture(tmp.path());
        let mut args = base_args(project_dir, baseline);
        args.features = vec!["features/**/*.feature".to_string()];

        let err = run(&args, OutputFormat::Text).unwrap_err();
        let msg = err.to_string();

        assert!(
            msg.contains("1 new unbound scenario"),
            "expected exactly 1 new gap (features/a/foo.feature's genuinely-unbound \
             scenario only) — features/b/a/foo.feature's identically-titled but \
             fully-implemented scenario must not be falsely reported due to a \
             directory-nesting suffix-match collision, got: {msg}"
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

    /// Regression test for the omitted-`--features`-flag case: `clap` must
    /// reject a missing `--features` occurrence at parse time rather than
    /// silently defaulting to an empty glob list (which would make the gate
    /// always report 0 gaps regardless of what `.features-gen` contains).
    #[test]
    fn features_flag_is_required_by_clap() {
        use clap::Parser;

        #[derive(Parser, Debug)]
        struct Wrapper {
            #[command(flatten)]
            args: ValidateArgs,
        }

        let result = Wrapper::try_parse_from([
            "rhino-cli",
            ".",
            "--features-gen",
            ".features-gen",
            "--baseline",
            "e2e-coverage-baseline.json",
            "--project",
            "test-project",
        ]);

        assert!(
            result.is_err(),
            "expected clap to reject an omitted --features flag as a required \
             argument, got: {result:?}"
        );
    }

    /// Regression test for the zero-match-`--features`-glob case: a
    /// *provided* `--features` glob that matches zero `.feature` files (e.g.
    /// after a path typo or directory rename) must error explicitly rather
    /// than silently reporting "0 new unbound scenario(s)" — indistinguishable,
    /// from the gate's own output, from "everything is correctly covered".
    /// `clap`'s `required = true` cannot catch this case since the flag IS
    /// present; only `run`'s explicit `any_feature_file_matched` guard can.
    #[test]
    fn empty_features_glob_match_errors_instead_of_silently_passing() {
        let tmp = TempDir::new().unwrap();
        // `.features-gen` genuinely contains a test.fixme call, but no
        // `features/` directory exists at all — the glob matches nothing.
        let gen_dir = tmp.path().join(".features-gen");
        fs::create_dir_all(&gen_dir).unwrap();
        fs::write(
            gen_dir.join("example.feature.spec.js"),
            "test.fixme(\"A\", async ({ page }) => {});\n",
        )
        .unwrap();
        fs::write(
            tmp.path().join("e2e-coverage-baseline.json"),
            "{\"project\": \"test-project\", \"allowedUnbound\": []}\n",
        )
        .unwrap();

        let args = base_args(
            tmp.path().to_string_lossy().to_string(),
            "e2e-coverage-baseline.json".to_string(),
        );

        let err = run(&args, OutputFormat::Text).unwrap_err();
        let msg = err.to_string();
        assert!(
            msg.contains("--features"),
            "expected an explicit error naming --features when the glob \
             matched nothing, got: {msg}"
        );
    }

    /// Locks in the distinction the previous two tests rely on: a `--features`
    /// glob that DOES match a real `.feature` file, but that file genuinely
    /// declares zero `@e2e`-tagged scenarios (e.g. every scenario is
    /// `@unit`-only), is a legitimate empty-declared-set state — it must
    /// still pass with 0 gaps, never be conflated with the "glob matched
    /// nothing" misconfiguration guarded above.
    #[test]
    fn feature_file_with_zero_e2e_scenarios_passes_without_error() {
        let tmp = TempDir::new().unwrap();
        let features_dir = tmp.path().join("features");
        fs::create_dir_all(&features_dir).unwrap();
        fs::write(
            features_dir.join("example.feature"),
            "@unit\nScenario: Unit only\n  Given a\n",
        )
        .unwrap();

        let gen_dir = tmp.path().join(".features-gen");
        fs::create_dir_all(&gen_dir).unwrap();
        fs::write(
            gen_dir.join("example.feature.spec.js"),
            "test.fixme(\"Unit only\", async ({ page }) => {});\n",
        )
        .unwrap();
        fs::write(
            tmp.path().join("e2e-coverage-baseline.json"),
            "{\"project\": \"test-project\", \"allowedUnbound\": []}\n",
        )
        .unwrap();

        let args = base_args(
            tmp.path().to_string_lossy().to_string(),
            "e2e-coverage-baseline.json".to_string(),
        );

        assert!(
            run(&args, OutputFormat::Text).is_ok(),
            "a matched .feature file with zero @e2e scenarios must pass, \
             not be mistaken for an empty --features glob match"
        );
    }

    /// Regression test for the Scenario-Outline blind-spot bug: `is_fixme`'s
    /// exact-match `HashSet::contains` check can never equal an Outline's
    /// raw declared title against playwright-bdd's real Examples-row-derived
    /// test titles (`Example #<N>` by default — never the outline's own
    /// title). Reproduces the reviewer's real `bddgen` finding: an outline
    /// whose Examples table has one unbound row must be reported as a new
    /// gap, not silently pass as "0 new unbound scenario(s)".
    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature:A Scenario Outline ships an unbound Examples-row test
    #[test]
    fn outline_scenario_with_unbound_example_row_is_reported_as_new_gap() {
        let tmp = TempDir::new().unwrap();
        let (project_dir, baseline) = write_outline_fixture(tmp.path());
        let args = base_args(project_dir, baseline);

        let err = run(&args, OutputFormat::Text).unwrap_err();
        let msg = err.to_string();

        assert!(
            msg.contains("1 new unbound scenario"),
            "expected the outline (one unbound Examples row) to be reported \
             as exactly 1 new gap, got: {msg}"
        );
    }

    /// Negative counterpart: an outline whose Examples table is fully bound
    /// (no `test.fixme` rows at all) must not be reported as a gap — guards
    /// against the fix itself over-matching (e.g. treating every outline as
    /// unbound regardless of its Examples-row tests' actual state).
    #[test]
    fn outline_scenario_fully_bound_is_not_reported_as_gap() {
        let tmp = TempDir::new().unwrap();
        let (project_dir, baseline) = write_fully_bound_outline_fixture(tmp.path());
        let args = base_args(project_dir, baseline);

        assert!(
            run(&args, OutputFormat::Text).is_ok(),
            "a fully-bound outline (zero test.fixme Examples rows) must pass"
        );
    }

    /// Regression test for the apostrophe-truncation bug: `fixme_title_re`'s
    /// naive `[^"']+` capture truncated at an escaped apostrophe, so a
    /// scenario titled with a possessive/contraction was silently invisible
    /// to gap detection. Reproduces the reviewer's exact repro: a scenario
    /// that is 100% unbound, validated against a COMPLETELY EMPTY baseline,
    /// must be reported as a new gap rather than silently passing.
    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature:A test.fixme title contains an escaped apostrophe
    #[test]
    fn apostrophe_titled_scenario_is_reported_as_new_gap() {
        let tmp = TempDir::new().unwrap();
        let features_dir = tmp.path().join("features");
        fs::create_dir_all(&features_dir).unwrap();
        fs::write(
            features_dir.join("example.feature"),
            "@e2e\nScenario: A user's profile renders correctly\n  Given a step\n",
        )
        .unwrap();

        let gen_dir = tmp.path().join(".features-gen");
        fs::create_dir_all(&gen_dir).unwrap();
        fs::write(
            gen_dir.join("example.feature.spec.js"),
            "test.fixme('A user\\'s profile renders correctly', async ({ page }) => {\n});\n",
        )
        .unwrap();
        fs::write(
            tmp.path().join("e2e-coverage-baseline.json"),
            "{\"project\": \"test-project\", \"allowedUnbound\": []}\n",
        )
        .unwrap();

        let args = base_args(
            tmp.path().to_string_lossy().to_string(),
            "e2e-coverage-baseline.json".to_string(),
        );

        let err = run(&args, OutputFormat::Text).unwrap_err();
        let msg = err.to_string();
        assert!(
            msg.contains("1 new unbound scenario"),
            "expected the apostrophe-titled scenario to be reported as a \
             new gap against an empty baseline, got: {msg}"
        );
    }

    /// Adjacent edge case to the apostrophe repro: playwright-bdd's default
    /// single-quote wrapping leaves an embedded double quote completely
    /// unescaped/literal (`jsStringWrap` only escapes the wrapping quote
    /// character itself and `\`) — this must not be mistaken for the
    /// string's own delimiter.
    #[test]
    fn double_quote_titled_scenario_is_reported_as_new_gap() {
        let tmp = TempDir::new().unwrap();
        let features_dir = tmp.path().join("features");
        fs::create_dir_all(&features_dir).unwrap();
        fs::write(
            features_dir.join("example.feature"),
            "@e2e\nScenario: The banner says \"Welcome\"\n  Given a step\n",
        )
        .unwrap();

        let gen_dir = tmp.path().join(".features-gen");
        fs::create_dir_all(&gen_dir).unwrap();
        fs::write(
            gen_dir.join("example.feature.spec.js"),
            "test.fixme('The banner says \"Welcome\"', async ({ page }) => {\n});\n",
        )
        .unwrap();
        fs::write(
            tmp.path().join("e2e-coverage-baseline.json"),
            "{\"project\": \"test-project\", \"allowedUnbound\": []}\n",
        )
        .unwrap();

        let args = base_args(
            tmp.path().to_string_lossy().to_string(),
            "e2e-coverage-baseline.json".to_string(),
        );

        let err = run(&args, OutputFormat::Text).unwrap_err();
        let msg = err.to_string();
        assert!(
            msg.contains("1 new unbound scenario"),
            "expected the double-quote-bearing scenario to be reported as a \
             new gap, got: {msg}"
        );
    }

    /// Adjacent edge case: a literal backslash character in a title (e.g. a
    /// Windows-style path fragment) is escaped to `\\` by `jsStringWrap`.
    #[test]
    fn backslash_titled_scenario_is_reported_as_new_gap() {
        let tmp = TempDir::new().unwrap();
        let features_dir = tmp.path().join("features");
        fs::create_dir_all(&features_dir).unwrap();
        fs::write(
            features_dir.join("example.feature"),
            "@e2e\nScenario: Loads config from C:\\temp\n  Given a step\n",
        )
        .unwrap();

        let gen_dir = tmp.path().join(".features-gen");
        fs::create_dir_all(&gen_dir).unwrap();
        fs::write(
            gen_dir.join("example.feature.spec.js"),
            "test.fixme('Loads config from C:\\\\temp', async ({ page }) => {\n});\n",
        )
        .unwrap();
        fs::write(
            tmp.path().join("e2e-coverage-baseline.json"),
            "{\"project\": \"test-project\", \"allowedUnbound\": []}\n",
        )
        .unwrap();

        let args = base_args(
            tmp.path().to_string_lossy().to_string(),
            "e2e-coverage-baseline.json".to_string(),
        );

        let err = run(&args, OutputFormat::Text).unwrap_err();
        let msg = err.to_string();
        assert!(
            msg.contains("1 new unbound scenario"),
            "expected the backslash-bearing scenario to be reported as a \
             new gap, got: {msg}"
        );
    }
}
