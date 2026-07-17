//! Spec-coverage scanner — walks `.feature` trees and source trees, matches
//! step definitions to Gherkin scenarios, and returns gaps plus orphan step
//! implementations.
//!
//! Port of `apps/rhino-cli/internal/speccoverage/checker.go`.

use std::collections::HashSet;
use std::fs;
use std::path::{Path, PathBuf};
use std::sync::OnceLock;
use std::time::Instant;

use anyhow::Error;
use regex::Regex;
use walkdir::WalkDir;

use super::extractors;
use super::matcher::{MatcherKind, StepMatcher, add_step_to_matcher_with_origin};
use super::parser::{ParsedStep, parse_feature_file};
use super::types::{CheckResult, CoverageGap, OrphanStepImpl, ScanOptions, ScenarioGap, StepGap};
use super::util::{first_non_empty, normalize_ws, unescape_string};

// ============================================================
// TS/JS extraction regexes (live inline in Go checker.go).
// ============================================================

/// Matches a TypeScript/JavaScript `Scenario("title", …)` call. The `(?s)`
/// flag is functionally inert here (the pattern has no `.` metacharacter)
/// but kept for symmetry with `step_def_re()`, signaling that callers scan
/// the whole file content rather than a single line.
fn scenario_def_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(r#"(?s)Scenario\s*\(\s*(?:"((?:[^"\\]|\\.)*)"|'((?:[^'\\]|\\.)*)')\s*,"#)
            .expect("valid regex")
    })
}

/// Matches a TypeScript/JavaScript `Given("…", …)` / `When(…)` / etc. step call.
fn step_def_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(r#"(?s)(?:Given|When|Then|And|But)\s*\(\s*(?:"((?:[^"\\]|\\.)*)"|'((?:[^'\\]|\\.)*)')\s*,"#).expect("valid regex")
    })
}

/// Matches a TypeScript/JavaScript `Given(/^regex$/, …)` regex step call.
fn ts_regex_step_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(r"(?s)(?:Given|When|Then|And|But)\s*\(\s*/\^?(.*?)\$?\s*/\s*,")
            .expect("valid regex")
    })
}

/// Matches a Go godog sc.Step call (godog step registration pattern).
fn go_step_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"\.Step\(`([^`]+)`").expect("valid regex"))
}

/// Matches a Go `// Scenario: Title` comment used to declare scenario coverage.
fn go_scenario_comment_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"//\s*Scenario:\s*(.+?)\s*$").expect("valid regex"))
}

// ============================================================
// Constants
// ============================================================

/// Returns the set of directory names that the walker skips unconditionally.
///
/// These directories are generated output, dependency caches, or synthetic
/// test-fixture scaffolding that should never be scanned for step
/// definitions. `fixtures` in particular holds throwaway step-def-shaped
/// content authored purely to exercise the coverage-checker's own unit tests
/// (e.g. `apps/rhino-cli/tests/fixtures/three-level/`) — no Gherkin scenario
/// in a real spec tree ever references it, so leaving it unskipped produces
/// false "orphan step implementation" findings when a project's own source
/// tree is scanned as `app_dir`.
fn skip_dirs() -> &'static HashSet<&'static str> {
    static SET: OnceLock<HashSet<&'static str>> = OnceLock::new();
    SET.get_or_init(|| {
        let arr = [
            "node_modules",
            ".next",
            "build",
            "dist",
            "storybook-static",
            "coverage",
            ".git",
            "target",
            "_build",
            "deps",
            "bin",
            "obj",
            "__pycache__",
            ".pytest_cache",
            ".venv",
            "generated-contracts",
            "generated_contracts",
            ".dart_tool",
            ".features-gen",
            "fixtures",
        ];
        arr.into_iter().collect()
    })
}

/// Returns `true` if `name` should be skipped when walking an `app_dir`
/// source tree: either a universal skip-dir (see [`skip_dirs`]) or one of
/// the caller-supplied `exclude_source_dirs` (fed from
/// `ScanOptions::exclude_source_dirs`, i.e. the `--exclude-source-dir` CLI
/// flag).
///
/// Deliberately a *separate* exclusion list from `--exclude-dir` (which only
/// filters the `.feature`-file walk, see [`walk_feature_files`]): a directory
/// name can be a legitimate spec-organization folder in the spec tree while
/// also being a legitimate app-source folder name in the app tree (e.g. a
/// Next.js content-layer `content/` directory holding step-decorator-shaped
/// teaching examples, coexisting with a Gherkin `content/` folder grouping
/// content-API scenarios). Sharing one exclusion list between both walks
/// would let excluding one tree silently exclude the other. This lets a
/// project declare the app-tree exclusion explicitly in its own Nx target
/// rather than rhino-cli hardcoding that project's directory-naming
/// convention for every repo that links this binary.
fn is_excluded_source_dir(name: &str, exclude_source_dirs: &[String]) -> bool {
    skip_dirs().contains(name) || exclude_source_dirs.iter().any(|d| d == name)
}

// ============================================================
// Public entry point
// ============================================================

/// Runs the spec-coverage scan described by `opts` and returns a
/// [`CheckResult`].
///
/// If `opts.specs_dirs` is empty and `opts.specs_dir` is set, the single
/// directory is used instead.  Selects either shared-step or 1-to-1 mode
/// based on `opts.shared_steps`.
///
/// # Errors
///
/// Returns an error if any file I/O or directory walk fails.
pub fn check_all(opts: &ScanOptions) -> std::result::Result<CheckResult, Error> {
    let mut effective = opts.clone();
    if effective.specs_dirs.is_empty() && !effective.specs_dir.as_os_str().is_empty() {
        effective.specs_dirs = vec![effective.specs_dir.clone()];
    }
    if effective.shared_steps {
        check_shared_steps(&effective)
    } else {
        check_one_to_one(&effective)
    }
}

/// Collects all `.feature` files from the spec directories specified in `opts`.
///
/// Falls back to `opts.specs_dir` when `opts.specs_dirs` is empty.
///
/// # Errors
///
/// Returns an error if any directory walk fails.
fn collect_feature_files(opts: &ScanOptions) -> std::result::Result<Vec<PathBuf>, Error> {
    let dirs: Vec<PathBuf> = if !opts.specs_dirs.is_empty() {
        opts.specs_dirs.clone()
    } else if !opts.specs_dir.as_os_str().is_empty() {
        vec![opts.specs_dir.clone()]
    } else {
        Vec::new()
    };
    let mut all = Vec::new();
    for dir in &dirs {
        all.extend(walk_feature_files(dir, &opts.exclude_dirs)?);
    }
    Ok(all)
}

/// Runs the scan in shared-step mode: all step definitions are matched against
/// all Gherkin steps without requiring a file-name correspondence.
///
/// # Errors
///
/// Returns an error if any file I/O or directory walk fails.
fn check_shared_steps(opts: &ScanOptions) -> std::result::Result<CheckResult, Error> {
    let start = Instant::now();
    let spec_files = collect_feature_files(opts)?;
    let all_step_texts = extract_all_step_texts(&opts.app_dir, &opts.exclude_source_dirs)?;
    let mut step_gaps: Vec<StepGap> = Vec::new();
    let mut all_gherkin_steps: Vec<String> = Vec::new();
    let mut total_scenarios = 0usize;
    let mut total_steps = 0usize;

    for spec_file in &spec_files {
        let rel_spec = rel_to(&opts.repo_root, spec_file);
        let scenarios = parse_feature_file(spec_file)?;
        for sc in &scenarios {
            total_scenarios += 1;
            for step in &sc.steps {
                total_steps += 1;
                all_gherkin_steps.push(step.text.clone());
                all_gherkin_steps.extend(step.variants.iter().cloned());
                if !step_covered(&all_step_texts, step) {
                    step_gaps.push(StepGap {
                        spec_file: rel_spec.clone(),
                        scenario_title: sc.title.clone(),
                        step_keyword: step.keyword.clone(),
                        step_text: step.text.clone(),
                    });
                }
            }
        }
    }

    let orphans = check_orphan_step_impls(&all_step_texts, &all_gherkin_steps, &opts.repo_root);

    Ok(CheckResult {
        total_specs: spec_files.len(),
        total_scenarios,
        total_steps,
        gaps: Vec::new(),
        scenario_gaps: Vec::new(),
        step_gaps,
        orphan_step_impls: orphans,
        duration: start.elapsed(),
    })
}

/// Runs the scan in 1-to-1 mode: each `.feature` file must have a
/// corresponding test file whose stem matches the feature file's stem.
///
/// # Errors
///
/// Returns an error if any file I/O or directory walk fails.
fn check_one_to_one(opts: &ScanOptions) -> std::result::Result<CheckResult, Error> {
    let start = Instant::now();
    let spec_files = collect_feature_files(opts)?;
    let all_step_texts = extract_all_step_texts(&opts.app_dir, &opts.exclude_source_dirs)?;
    let mut gaps: Vec<CoverageGap> = Vec::new();
    let mut scenario_gaps: Vec<ScenarioGap> = Vec::new();
    let mut step_gaps: Vec<StepGap> = Vec::new();
    let mut all_gherkin_steps: Vec<String> = Vec::new();
    let mut total_scenarios = 0usize;
    let mut total_steps = 0usize;

    for spec_file in &spec_files {
        let stem = spec_file
            .file_stem()
            .and_then(|s| s.to_str())
            .map(|s| s.trim_end_matches(".feature").to_string())
            .unwrap_or_default();

        let test_file_paths =
            find_all_matching_test_files(&opts.app_dir, &stem, &opts.exclude_source_dirs)?;

        if test_file_paths.is_empty() {
            let rel_path = rel_to(&opts.repo_root, spec_file);
            gaps.push(CoverageGap {
                spec_file: rel_path,
                stem: stem.clone(),
            });
            // Still collect Gherkin step texts from this file for orphan check.
            let scenarios = parse_feature_file(spec_file)?;
            for sc in &scenarios {
                for step in &sc.steps {
                    all_gherkin_steps.push(step.text.clone());
                }
            }
            continue;
        }

        let rel_spec = rel_to(&opts.repo_root, spec_file);
        let scenarios = parse_feature_file(spec_file)?;

        let mut scenario_titles: HashSet<String> = HashSet::new();
        for test_file in &test_file_paths {
            let titles = extract_scenario_titles(test_file)?;
            scenario_titles.extend(titles);
        }

        for sc in &scenarios {
            total_scenarios += 1;
            let normalized = normalize_ws(&sc.title);
            if !scenario_titles.contains(&normalized) {
                scenario_gaps.push(ScenarioGap {
                    spec_file: rel_spec.clone(),
                    scenario_title: sc.title.clone(),
                });
            }

            for step in &sc.steps {
                total_steps += 1;
                all_gherkin_steps.push(step.text.clone());
                all_gherkin_steps.extend(step.variants.iter().cloned());
                if !step_covered(&all_step_texts, step) {
                    step_gaps.push(StepGap {
                        spec_file: rel_spec.clone(),
                        scenario_title: sc.title.clone(),
                        step_keyword: step.keyword.clone(),
                        step_text: step.text.clone(),
                    });
                }
            }
        }
    }

    let orphans = check_orphan_step_impls(&all_step_texts, &all_gherkin_steps, &opts.repo_root);

    Ok(CheckResult {
        total_specs: spec_files.len(),
        total_scenarios,
        total_steps,
        gaps,
        scenario_gaps,
        step_gaps,
        orphan_step_impls: orphans,
        duration: start.elapsed(),
    })
}

// ============================================================
// Coverage helpers
// ============================================================

/// Returns `true` if `step` has at least one matching entry in `sm`.
///
/// For steps with no variants the primary `text` is checked directly.
/// For steps with variants all variant texts must match.
fn step_covered(sm: &StepMatcher, step: &ParsedStep) -> bool {
    if sm.matches(&step.text) {
        return true;
    }
    if step.variants.is_empty() {
        return false;
    }
    step.variants.iter().all(|v| sm.matches(v))
}

/// Identifies step-definition entries in `sm` that match no step in
/// `all_gherkin_steps` and returns them as [`OrphanStepImpl`] values.
///
/// `repo_root` is used to strip the absolute path prefix from the reported
/// file paths.
fn check_orphan_step_impls(
    sm: &StepMatcher,
    all_gherkin_steps: &[String],
    repo_root: &Path,
) -> Vec<OrphanStepImpl> {
    if sm.entries.is_empty() {
        return Vec::new();
    }
    let normalized: Vec<String> = all_gherkin_steps
        .iter()
        .map(|gs| normalize_ws(gs))
        .collect();

    let mut orphans = Vec::new();
    for (i, e) in sm.entries.iter().enumerate() {
        let matched = match e.kind {
            MatcherKind::Exact => normalized.iter().any(|gs| gs == &e.exact_text),
            MatcherKind::Pattern => {
                // entries[i] corresponds to patterns[?]; we tracked pattern compilation
                // via sm.patterns. Walk that list against pattern_text for identity.
                sm.patterns
                    .iter()
                    .filter(|re| re.as_str() == e.pattern_text)
                    .any(|re| normalized.iter().any(|gs| re.is_match(gs)))
                    || sm
                        .patterns
                        .get(pattern_index_for_entry(sm, i))
                        .is_some_and(|re| normalized.iter().any(|gs| re.is_match(gs)))
            }
        };
        if matched {
            continue;
        }
        let text = if matches!(e.kind, MatcherKind::Pattern) {
            e.pattern_text.clone()
        } else {
            e.exact_text.clone()
        };
        let file_path = if repo_root.as_os_str().is_empty() {
            e.file.clone()
        } else {
            Path::new(&e.file)
                .strip_prefix(repo_root)
                .map_or_else(|_| e.file.clone(), |p| p.to_string_lossy().to_string())
        };
        orphans.push(OrphanStepImpl {
            file: file_path,
            matcher_kind: match e.kind {
                MatcherKind::Exact => "exact".to_string(),
                MatcherKind::Pattern => "pattern".to_string(),
            },
            matcher_text: text,
        });
    }
    orphans
}

/// Computes the index into `sm.patterns` that corresponds to the pattern entry
/// at position `i` in `sm.entries`.
///
/// Counts the number of `Pattern` entries that precede `i` in `entries`.
/// This is safe because [`StepMatcher::add_pattern_with_origin`] appends to
/// both `entries` and `patterns` in lockstep, so the count equals the index
/// into `patterns`.
fn pattern_index_for_entry(sm: &StepMatcher, i: usize) -> usize {
    sm.entries
        .iter()
        .take(i)
        .filter(|e| matches!(e.kind, MatcherKind::Pattern))
        .count()
}

// ============================================================
// Walking
// ============================================================

/// Recursively walks `dir` and returns all `.feature` files, skipping any
/// directory whose name is in `exclude_dirs`.
///
/// Returns an empty `Vec` if `dir` does not exist.
///
/// `pub(crate)` so [`crate::commands::specs_coverage`]'s `@covers`
/// runtime-cross-check wiring can reuse the same feature-file walk rather
/// than duplicating it.
///
/// # Errors
///
/// Returns an error if the directory walk encounters an I/O error.
pub(crate) fn walk_feature_files(
    dir: &Path,
    exclude_dirs: &[String],
) -> std::result::Result<Vec<PathBuf>, Error> {
    if !dir.exists() {
        return Ok(Vec::new());
    }
    let excl: HashSet<&str> = exclude_dirs.iter().map(String::as_str).collect();
    let mut files = Vec::new();
    let walker = WalkDir::new(dir).into_iter().filter_entry(|e| {
        if e.file_type().is_dir() {
            let name = e.file_name().to_string_lossy();
            !excl.contains(name.as_ref())
        } else {
            true
        }
    });
    for entry in walker {
        let entry = entry?;
        if entry.file_type().is_file() && entry.path().to_string_lossy().ends_with(".feature") {
            files.push(entry.path().to_path_buf());
        }
    }
    Ok(files)
}

/// Converts a kebab-case stem to `PascalCase`.
///
/// Each hyphen-separated segment has its first character uppercased.
/// Empty segments (e.g. from leading or consecutive hyphens) are skipped.
fn to_pascal_case(stem: &str) -> String {
    let mut b = String::new();
    for p in stem.split('-') {
        if p.is_empty() {
            continue;
        }
        let mut chars = p.chars();
        if let Some(c) = chars.next() {
            for u in c.to_uppercase() {
                b.push(u);
            }
            b.push_str(chars.as_str());
        }
    }
    b
}

/// Returns `true` if the file base name `base` is a plausible test file for
/// the feature stem `stem`.
///
/// Checks multiple naming conventions: kebab-case, `snake_case`, `PascalCase`,
/// and `test_<snake>` prefix.
fn matches_stem(base: &str, stem: &str) -> bool {
    let snake = stem.replace('-', "_");
    let pascal = to_pascal_case(stem);
    let test_snake = format!("test_{snake}");

    let prefixes = [
        format!("{stem}."),
        format!("{stem}_"),
        format!("{snake}."),
        format!("{snake}_"),
        pascal.clone(),
        format!("{test_snake}."),
        format!("{test_snake}_"),
    ];
    for prefix in &prefixes {
        if base.starts_with(prefix) {
            return true;
        }
    }
    base == stem || base == snake
}

/// Returns `true` if `path` is a test/step file based on its extension and
/// language-specific naming conventions.
fn is_test_file(path: &Path) -> bool {
    let base = path.file_name().and_then(|s| s.to_str()).unwrap_or("");
    let ext = path.extension().and_then(|s| s.to_str()).unwrap_or("");
    match ext {
        "" => true, // exact stem match w/o extension
        "go" => base.ends_with("_test.go"),
        "ts" | "tsx" | "js" | "jsx" => {
            base.contains(".test.")
                || base.contains(".spec.")
                || base.contains(".steps.")
                || base.contains(".integration.")
                || base.contains("_test.")
        }
        "java" | "kt" => is_in_test_dir(path),
        "py" => base.starts_with("test_") || base.ends_with("_test.py") || is_in_test_dir(path),
        "exs" => base.ends_with("_test.exs") || base.ends_with("_steps.exs"),
        "rs" => base.ends_with("_test.rs") || is_in_test_dir(path),
        "fs" | "cs" => {
            is_in_test_dir(path)
                || base.ends_with("Steps.cs")
                || base.ends_with("Tests.cs")
                || base.ends_with("Steps.fs")
                || base.ends_with("Tests.fs")
        }
        "clj" => base.ends_with("_test.clj") || base.ends_with("_steps.clj"),
        "dart" => base.ends_with("_test.dart") || is_in_test_dir(path),
        _ => false,
    }
}

/// Returns `true` if any path component of `path` is named `test`, `tests`,
/// or `Tests`.
fn is_in_test_dir(path: &Path) -> bool {
    path.components()
        .any(|comp| matches!(comp.as_os_str().to_str(), Some("test" | "tests" | "Tests")))
}

/// Recursively walks `app_dir` and returns all test/step files whose base name
/// matches `stem`, skipping directories per [`is_excluded_source_dir`].
///
/// Returns an empty `Vec` if `app_dir` does not exist.
///
/// # Errors
///
/// Returns an error if the directory walk encounters an I/O error.
fn find_all_matching_test_files(
    app_dir: &Path,
    stem: &str,
    exclude_source_dirs: &[String],
) -> std::result::Result<Vec<PathBuf>, Error> {
    if !app_dir.exists() {
        return Ok(Vec::new());
    }
    let mut matches = Vec::new();
    let walker = WalkDir::new(app_dir).into_iter().filter_entry(|e| {
        if e.file_type().is_dir() {
            let name = e.file_name().to_string_lossy();
            !is_excluded_source_dir(name.as_ref(), exclude_source_dirs)
        } else {
            true
        }
    });
    for entry in walker {
        let entry = entry?;
        if !entry.file_type().is_file() {
            continue;
        }
        let base = entry.file_name().to_string_lossy();
        if matches_stem(&base, stem) && is_test_file(entry.path()) {
            matches.push(entry.path().to_path_buf());
        }
    }
    Ok(matches)
}

// ============================================================
// Scenario title extraction (dispatch by ext)
// ============================================================

/// Dispatches to the appropriate scenario-title extractor based on the file
/// extension of `test_file_path`.
///
/// Auto-bind frameworks (Elixir, F#, Clojure) return an empty set because
/// their scenario matching is implicit.
///
/// # Errors
///
/// Returns an error if the file cannot be read.
fn extract_scenario_titles(test_file_path: &Path) -> std::result::Result<HashSet<String>, Error> {
    let ext = test_file_path
        .extension()
        .and_then(|s| s.to_str())
        .unwrap_or("");
    match ext {
        "go" | "java" | "kt" | "cs" | "rs" | "dart" => extract_go_scenario_titles(test_file_path),
        "py" => extractors::extract_python_scenario_titles(test_file_path),
        "exs" | "fs" | "clj" => Ok(HashSet::new()), // auto-bind frameworks
        _ => extract_ts_scenario_titles(test_file_path),
    }
}

/// Extracts scenario titles from a TypeScript/JavaScript test file by scanning
/// the whole file content for `Scenario("…", …)` and `Scenario('…', …)` call
/// patterns — not line-by-line, so a title that wraps onto the physical line
/// after `Scenario(` is still recognized.
///
/// # Errors
///
/// Returns an error if the file cannot be read.
fn extract_ts_scenario_titles(p: &Path) -> std::result::Result<HashSet<String>, Error> {
    let content = fs::read_to_string(p)?;
    let mut titles = HashSet::new();
    for caps in scenario_def_re().captures_iter(&content) {
        let dq = caps.get(1).map_or("", |m| m.as_str());
        let sq = caps.get(2).map_or("", |m| m.as_str());
        let title = unescape_string(first_non_empty(dq, sq));
        titles.insert(normalize_ws(&title));
    }
    Ok(titles)
}

/// Extracts scenario titles from a Go (or other language) test file by
/// scanning for `// Scenario: Title` comment markers.
///
/// # Errors
///
/// Returns an error if the file cannot be read.
fn extract_go_scenario_titles(p: &Path) -> std::result::Result<HashSet<String>, Error> {
    let content = fs::read_to_string(p)?;
    let mut titles = HashSet::new();
    for line in content.lines() {
        if let Some(caps) = go_scenario_comment_re().captures(line) {
            titles.insert(normalize_ws(
                caps.get(1)
                    .expect("capture group 1 always present")
                    .as_str(),
            ));
        }
    }
    Ok(titles)
}

// ============================================================
// Whole-app step extraction (walks + per-ext dispatch)
// ============================================================

/// Walks `app_dir` recursively and extracts all step definitions from every
/// recognised source file, aggregating them into a single [`StepMatcher`].
///
/// Skips directories per [`is_excluded_source_dir`] — the universal
/// `skip_dirs` set plus any caller-supplied `exclude_source_dirs`. Returns an
/// empty matcher if `app_dir` does not exist.
///
/// # Errors
///
/// Returns an error if the directory walk encounters an I/O error.
pub fn extract_all_step_texts(
    app_dir: &Path,
    exclude_source_dirs: &[String],
) -> std::result::Result<StepMatcher, Error> {
    let mut sm = StepMatcher::new();
    if !app_dir.exists() {
        return Ok(sm);
    }

    let walker = WalkDir::new(app_dir).into_iter().filter_entry(|e| {
        if e.file_type().is_dir() {
            let name = e.file_name().to_string_lossy();
            !is_excluded_source_dir(name.as_ref(), exclude_source_dirs)
        } else {
            true
        }
    });

    for entry in walker {
        let entry = entry?;
        if !entry.file_type().is_file() {
            continue;
        }
        let path = entry.path();
        let ext = path.extension().and_then(|s| s.to_str()).unwrap_or("");
        let _ = match ext {
            "ts" | "tsx" | "js" | "jsx" => extract_ts_step_texts(path, &mut sm),
            "go" => extract_go_step_texts(path, &mut sm),
            "java" | "kt" => extractors::extract_jvm_step_texts(path, &mut sm),
            "py" => extractors::extract_python_step_texts(path, &mut sm),
            "ex" | "exs" => extractors::extract_elixir_step_texts(path, &mut sm),
            "rs" => extractors::extract_rust_step_texts(path, &mut sm),
            "cs" => extractors::extract_csharp_step_texts(path, &mut sm),
            "fs" => extractors::extract_fsharp_step_texts(path, &mut sm),
            "clj" => extractors::extract_clojure_step_texts(path, &mut sm),
            "dart" => extractors::extract_dart_step_texts(path, &mut sm),
            _ => Ok(()),
        };
    }
    Ok(sm)
}

/// Extracts step definitions from a TypeScript/JavaScript source file.
///
/// Strips JS/TS comments first, then recognises both string-literal step
/// calls and `/regex/` step calls.
///
/// # Errors
///
/// Returns an error if the file cannot be read.
fn extract_ts_step_texts(path: &Path, sm: &mut StepMatcher) -> std::result::Result<(), Error> {
    let content = fs::read_to_string(path)?;
    let src = strip_js_comments(&content);
    let path_s = path.to_string_lossy();

    for caps in step_def_re().captures_iter(&src) {
        let dq = caps.get(1).map_or("", |m| m.as_str());
        let sq = caps.get(2).map_or("", |m| m.as_str());
        let text = unescape_string(first_non_empty(dq, sq));
        add_step_to_matcher_with_origin(sm, &text, &path_s);
    }
    for caps in ts_regex_step_re().captures_iter(&src) {
        let pattern = caps
            .get(1)
            .expect("capture group 1 always present")
            .as_str();
        if let Ok(re) = Regex::new(pattern) {
            sm.add_pattern_with_origin(re, pattern, &path_s);
        }
    }
    Ok(())
}

/// Extracts step definitions from a Go godog source file by scanning for godog step registration calls.
///
/// # Errors
///
/// Returns an error if the file cannot be read.
fn extract_go_step_texts(path: &Path, sm: &mut StepMatcher) -> std::result::Result<(), Error> {
    let content = fs::read_to_string(path)?;
    let path_s = path.to_string_lossy();
    for line in content.lines() {
        for caps in go_step_re().captures_iter(line) {
            let pattern = caps
                .get(1)
                .expect("capture group 1 always present")
                .as_str();
            if let Ok(re) = Regex::new(pattern) {
                sm.add_pattern_with_origin(re, pattern, &path_s);
            }
        }
    }
    Ok(())
}

/// Strips JS/TS comments from `src`, returning the comment-free source.
///
/// Rules (UTF-8 safe — walks by `char`, not byte):
///
/// - `/* … */` block comments are removed (preserving embedded newlines as
///   bare `\n` so line numbers stay consistent).
/// - `// …` line comments are removed **only** when they start at the
///   beginning of a line (i.e. after optional leading whitespace).  Inline
///   `// …` after real code is preserved.
/// - String and template literals (`"…"`, `'…'`, `` `…` ``) are passed
///   through verbatim so comment-like text inside strings is not stripped.
fn strip_js_comments(src: &str) -> String {
    let chars: Vec<char> = src.chars().collect();
    let n = chars.len();
    let mut out = String::with_capacity(src.len());
    let mut i = 0usize;
    let mut at_line_start = true;
    while i < n {
        let c = chars[i];
        if c == '\n' {
            out.push('\n');
            i += 1;
            at_line_start = true;
            continue;
        }
        if c == '/' && i + 1 < n && chars[i + 1] == '*' {
            let mut j = i + 2;
            while j + 1 < n && !(chars[j] == '*' && chars[j + 1] == '/') {
                if chars[j] == '\n' {
                    out.push('\n');
                }
                j += 1;
            }
            i = j + 2;
            continue;
        }
        if at_line_start && c == '/' && i + 1 < n && chars[i + 1] == '/' {
            let mut j = i + 2;
            while j < n && chars[j] != '\n' {
                j += 1;
            }
            i = j;
            continue;
        }
        if c == '"' || c == '\'' || c == '`' {
            let quote = c;
            out.push(c);
            i += 1;
            while i < n {
                if chars[i] == '\\' && i + 1 < n {
                    out.push(chars[i]);
                    out.push(chars[i + 1]);
                    i += 2;
                    continue;
                }
                out.push(chars[i]);
                if chars[i] == quote {
                    i += 1;
                    break;
                }
                i += 1;
            }
            at_line_start = false;
            continue;
        }
        out.push(c);
        if c != ' ' && c != '\t' {
            at_line_start = false;
        }
        i += 1;
    }
    out
}

// ============================================================
// Path helpers
// ============================================================

/// Returns `p` relative to `root`.
///
/// If `root` is empty or `p` does not start with `root`, returns the
/// string representation of `p` unchanged.
fn rel_to(root: &Path, p: &Path) -> String {
    if root.as_os_str().is_empty() {
        return p.to_string_lossy().to_string();
    }
    p.strip_prefix(root).map_or_else(
        |_| p.to_string_lossy().to_string(),
        |r| r.to_string_lossy().to_string(),
    )
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[test]
    fn to_pascal_case_handles_kebab() {
        assert_eq!(to_pascal_case("health-check"), "HealthCheck");
        assert_eq!(to_pascal_case("user"), "User");
        assert_eq!(to_pascal_case("a-b-c"), "ABC");
    }

    #[test]
    fn matches_stem_kebab_snake_pascal_test_prefix() {
        assert!(matches_stem("user-login.test.ts", "user-login"));
        assert!(matches_stem("user_login.test.ts", "user-login"));
        assert!(matches_stem("UserLogin", "user-login"));
        assert!(matches_stem("test_user_login.py", "user-login"));
        assert!(matches_stem("user-login", "user-login"));
        assert!(!matches_stem("other.ts", "user-login"));
    }

    #[test]
    fn is_test_file_typescript() {
        assert!(is_test_file(Path::new("x.test.ts")));
        assert!(is_test_file(Path::new("x.spec.ts")));
        assert!(is_test_file(Path::new("x.steps.ts")));
        assert!(!is_test_file(Path::new("x.ts")));
    }

    #[test]
    fn is_test_file_go() {
        assert!(is_test_file(Path::new("foo_test.go")));
        assert!(!is_test_file(Path::new("foo.go")));
    }

    #[test]
    fn is_test_file_python() {
        assert!(is_test_file(Path::new("test_foo.py")));
        assert!(is_test_file(Path::new("foo_test.py")));
        assert!(is_test_file(Path::new("tests/foo.py")));
    }

    #[test]
    fn is_in_test_dir_detects_test_segments() {
        assert!(is_in_test_dir(Path::new("a/tests/b.rs")));
        assert!(is_in_test_dir(Path::new("a/test/b.rs")));
        assert!(is_in_test_dir(Path::new("a/Tests/b.cs")));
        assert!(!is_in_test_dir(Path::new("a/b/c.rs")));
    }

    #[test]
    fn strip_js_comments_removes_block_and_line_at_line_start() {
        let s = "/* drop */ keep\n// drop\n  // drop\nreal_code(); // keep\n";
        let out = strip_js_comments(s);
        assert!(!out.contains("drop"));
        assert!(out.contains("real_code()"));
        assert!(out.contains("// keep")); // not at line start → preserved
    }

    #[test]
    fn strip_js_comments_preserves_strings() {
        let s = r#"const x = "// not a comment"; foo();"#;
        let out = strip_js_comments(s);
        assert!(out.contains("// not a comment"));
    }

    #[test]
    fn walk_feature_files_returns_features_recursively() {
        let tmp = TempDir::new().unwrap();
        std::fs::create_dir_all(tmp.path().join("a/b")).unwrap();
        std::fs::write(tmp.path().join("x.feature"), "Feature: x").unwrap();
        std::fs::write(tmp.path().join("a/y.feature"), "Feature: y").unwrap();
        std::fs::write(tmp.path().join("a/b/z.feature"), "Feature: z").unwrap();
        std::fs::write(tmp.path().join("not.txt"), "no").unwrap();
        let files = walk_feature_files(tmp.path(), &[]).unwrap();
        assert_eq!(files.len(), 3);
    }

    #[test]
    fn walk_feature_files_skips_excluded_dirs() {
        let tmp = TempDir::new().unwrap();
        std::fs::create_dir_all(tmp.path().join("skip-me")).unwrap();
        std::fs::write(tmp.path().join("x.feature"), "Feature: x").unwrap();
        std::fs::write(tmp.path().join("skip-me/y.feature"), "Feature: y").unwrap();
        let files = walk_feature_files(tmp.path(), &["skip-me".to_string()]).unwrap();
        assert_eq!(files.len(), 1);
    }

    #[test]
    fn extract_all_step_texts_aggregates_across_languages() {
        let tmp = TempDir::new().unwrap();
        std::fs::write(
            tmp.path().join("steps.go"),
            "func step(sc *godog.ScenarioContext) {\n  sc.Step(`^user logs in$`, login)\n}\n",
        )
        .unwrap();
        std::fs::write(
            tmp.path().join("Steps.java"),
            "@Given(\"a user\")\nvoid step() {}\n",
        )
        .unwrap();
        let sm = extract_all_step_texts(tmp.path(), &[]).unwrap();
        assert!(sm.matches("user logs in"));
        assert!(sm.matches("a user"));
    }

    #[test]
    fn extract_all_step_texts_honors_exclude_dirs_in_source_walk() {
        // `--exclude-dir` was originally wired only into the `.feature`-file walk
        // (see `walk_feature_files_skips_excluded_dirs` above); it must also apply to the
        // app_dir *source* walk so a project with a directory-naming convention `skip_dirs`
        // doesn't know about (e.g. a content-layer directory holding step-decorator-shaped
        // teaching examples) can declare the exclusion explicitly via its own Nx target
        // rather than rhino-cli hardcoding that project's convention for every repo.
        let tmp = TempDir::new().unwrap();
        std::fs::create_dir_all(tmp.path().join("content/learning/code")).unwrap();
        std::fs::write(
            tmp.path().join("content/learning/code/test_bdd_example.py"),
            "@given(\"a taught condition\")\ndef given_taught():\n    pass\n",
        )
        .unwrap();
        std::fs::create_dir_all(tmp.path().join("src")).unwrap();
        std::fs::write(
            tmp.path().join("src/real_steps.rs"),
            "#[given(\"a real step\")]\nfn given_real() {}\n",
        )
        .unwrap();

        let unfiltered = extract_all_step_texts(tmp.path(), &[]).unwrap();
        assert!(unfiltered.matches("a taught condition"));

        let filtered = extract_all_step_texts(tmp.path(), &["content".to_string()]).unwrap();
        assert!(filtered.matches("a real step"));
        assert!(!filtered.matches("a taught condition"));
    }

    #[test]
    fn extract_all_step_texts_skips_fixtures_dir() {
        // `apps/rhino-cli/tests/fixtures/three-level/unit/feature_steps.rs` is a synthetic
        // fixture used only by `specs_coverage.rs`'s own three-level-mode unit tests (passed
        // explicitly as `app_dir`/`unit_dir`/etc. there, so the "fixtures" ancestor component
        // is never itself walked in that call). When the real `apps/rhino-cli` tree is scanned
        // as `app_dir` (the real `specs behavior-coverage validate --shared-steps` invocation),
        // a step-def-shaped fixture file left under a directory literally named `fixtures`
        // should not surface as a false "orphan step implementation" — no Gherkin scenario in
        // the real spec tree will ever reference throwaway fixture step text.
        let tmp = TempDir::new().unwrap();
        std::fs::create_dir_all(tmp.path().join("fixtures/three-level/unit")).unwrap();
        std::fs::write(
            tmp.path()
                .join("fixtures/three-level/unit/feature_steps.rs"),
            "#[given(\"a condition\")]\nfn given_a_condition() {}\n",
        )
        .unwrap();
        std::fs::create_dir_all(tmp.path().join("src")).unwrap();
        std::fs::write(
            tmp.path().join("src/real_steps.rs"),
            "#[given(\"a real step\")]\nfn given_real() {}\n",
        )
        .unwrap();
        let sm = extract_all_step_texts(tmp.path(), &[]).unwrap();
        assert!(sm.matches("a real step"));
        assert!(!sm.matches("a condition"));
    }

    #[test]
    fn check_all_one_to_one_reports_file_gap() {
        let tmp = TempDir::new().unwrap();
        let specs = tmp.path().join("specs");
        let app = tmp.path().join("app");
        std::fs::create_dir_all(&specs).unwrap();
        std::fs::create_dir_all(&app).unwrap();
        std::fs::write(
            specs.join("user-login.feature"),
            "Feature: x\nScenario: T\n  Given x\n",
        )
        .unwrap();
        // No test file in app.
        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            specs_dir: specs.clone(),
            specs_dirs: vec![],
            app_dir: app.clone(),
            verbose: false,
            quiet: false,
            shared_steps: false,
            exclude_dirs: vec![],
            exclude_source_dirs: vec![],
        };
        let r = check_all(&opts).unwrap();
        assert_eq!(r.gaps.len(), 1);
        assert_eq!(r.gaps[0].stem, "user-login");
    }

    #[test]
    fn exclude_dirs_and_exclude_source_dirs_are_independent() {
        // A directory name can be legitimate in BOTH trees at once for different
        // reasons — e.g. `content/` grouping content-API Gherkin scenarios in the
        // spec tree while also being a Next.js content-layer directory in the app
        // tree. Excluding it from one walk must never silently exclude it from the
        // other: `exclude_dirs` (feature-file walk) and `exclude_source_dirs`
        // (app_dir source walk) are deliberately separate CLI flags/fields for
        // exactly this reason.
        let tmp = TempDir::new().unwrap();
        let specs = tmp.path().join("specs");
        let app = tmp.path().join("app");
        std::fs::create_dir_all(specs.join("content")).unwrap();
        std::fs::create_dir_all(app.join("content")).unwrap();
        std::fs::write(
            specs.join("content/content-api.feature"),
            "Feature: x\nScenario: T\n  Given a taught condition\n",
        )
        .unwrap();
        std::fs::write(
            app.join("content/steps.py"),
            "@given(\"a taught condition\")\ndef given_taught():\n    pass\n",
        )
        .unwrap();

        // Excluding "content" only via exclude_source_dirs must still pick up the
        // real spec scenario in specs/content/ — no false step gap.
        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            specs_dir: specs.clone(),
            specs_dirs: vec![],
            app_dir: app.clone(),
            verbose: false,
            quiet: false,
            shared_steps: true,
            exclude_dirs: vec![],
            exclude_source_dirs: vec!["content".to_string()],
        };
        let r = check_all(&opts).unwrap();
        assert_eq!(
            r.total_scenarios, 1,
            "spec scenario must still be collected"
        );
        assert_eq!(
            r.step_gaps.len(),
            1,
            "step impl was excluded from the source walk, so the step is uncovered"
        );
    }

    #[test]
    fn check_orphan_step_impls_flags_uncovered_exact_entries() {
        let mut sm = StepMatcher::new();
        sm.add_exact_with_origin("user logs in", "/repo/x.rs");
        sm.add_exact_with_origin("orphaned step", "/repo/y.rs");
        let gherkin = vec!["user logs in".to_string()];
        let orphans = check_orphan_step_impls(&sm, &gherkin, Path::new("/repo"));
        assert_eq!(orphans.len(), 1);
        assert_eq!(orphans[0].matcher_text, "orphaned step");
        assert_eq!(orphans[0].matcher_kind, "exact");
        // Path becomes repo-relative.
        assert_eq!(orphans[0].file, "y.rs");
    }

    #[test]
    fn check_orphan_step_impls_handles_pattern_entries() {
        let mut sm = StepMatcher::new();
        let re = Regex::new(r"^count is \d+$").expect("valid hardcoded regex");
        sm.add_pattern_with_origin(re, r"^count is \d+$", "/repo/x.rs");
        let orphans_no_match =
            check_orphan_step_impls(&sm, &["different step".to_string()], Path::new("/repo"));
        assert_eq!(orphans_no_match.len(), 1);
        assert_eq!(orphans_no_match[0].matcher_kind, "pattern");

        // Now with a matching Gherkin step.
        let orphans_match =
            check_orphan_step_impls(&sm, &["count is 42".to_string()], Path::new("/repo"));
        assert_eq!(orphans_match.len(), 0);
    }

    #[test]
    fn check_orphan_step_impls_empty_matcher_returns_empty() {
        let sm = StepMatcher::new();
        let orphans = check_orphan_step_impls(&sm, &["a".to_string()], Path::new("/repo"));
        assert!(orphans.is_empty());
    }

    #[test]
    fn step_covered_with_variants_requires_all_to_match() {
        let mut sm = StepMatcher::new();
        sm.add_exact_with_origin("user enters A", "x.rs");
        sm.add_exact_with_origin("user enters B", "x.rs");
        let step = ParsedStep {
            keyword: "Given".to_string(),
            text: "user enters <state>".to_string(),
            variants: vec!["user enters A".to_string(), "user enters B".to_string()],
        };
        assert!(step_covered(&sm, &step));

        let step_partial = ParsedStep {
            keyword: "Given".to_string(),
            text: "user enters <state>".to_string(),
            variants: vec!["user enters A".to_string(), "user enters C".to_string()],
        };
        assert!(!step_covered(&sm, &step_partial));
    }

    #[test]
    fn extract_ts_scenario_titles_picks_up_double_quoted_title() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.test.ts");
        std::fs::write(
            &p,
            "Scenario(\"User logs in\", () => {});\nScenario('Another title', () => {});\n",
        )
        .unwrap();
        let titles = extract_ts_scenario_titles(&p).unwrap();
        assert!(titles.contains("User logs in"));
        assert!(titles.contains("Another title"));
    }

    #[test]
    fn extract_ts_scenario_titles_picks_up_cross_line_double_quoted_title() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.test.ts");
        std::fs::write(&p, "Scenario(\n  \"Wrapped double title\",\n  () => {});\n").unwrap();
        let titles = extract_ts_scenario_titles(&p).unwrap();
        assert!(titles.contains("Wrapped double title"));
    }

    #[test]
    fn extract_ts_scenario_titles_picks_up_cross_line_single_quoted_title() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.test.ts");
        std::fs::write(&p, "Scenario(\n  'Wrapped single title',\n  () => {});\n").unwrap();
        let titles = extract_ts_scenario_titles(&p).unwrap();
        assert!(titles.contains("Wrapped single title"));
    }

    #[test]
    fn extract_ts_scenario_titles_preserves_same_line_titles() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.test.ts");
        std::fs::write(
            &p,
            "Scenario(\"User logs in\", () => {});\nScenario('Another title', () => {});\n",
        )
        .unwrap();
        let titles = extract_ts_scenario_titles(&p).unwrap();
        assert!(titles.contains("User logs in"));
        assert!(titles.contains("Another title"));
    }

    #[test]
    fn extract_go_scenario_titles_picks_up_comment() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x_test.go");
        std::fs::write(&p, "// Scenario: Foo bar baz\nfunc Test() {}\n").unwrap();
        let titles = extract_go_scenario_titles(&p).unwrap();
        assert!(titles.contains("Foo bar baz"));
    }

    #[test]
    fn extract_scenario_titles_dispatches_by_extension() {
        let tmp = TempDir::new().unwrap();
        let go = tmp.path().join("x_test.go");
        std::fs::write(&go, "// Scenario: Go T\n").unwrap();
        assert!(extract_scenario_titles(&go).unwrap().contains("Go T"));

        let ts = tmp.path().join("x.test.ts");
        std::fs::write(&ts, "Scenario(\"TS T\", () => {});\n").unwrap();
        assert!(extract_scenario_titles(&ts).unwrap().contains("TS T"));

        // Auto-bind frameworks return empty.
        let fs = tmp.path().join("x.fs");
        std::fs::write(&fs, "// nothing\n").unwrap();
        assert!(extract_scenario_titles(&fs).unwrap().is_empty());
    }

    #[test]
    fn find_all_matching_test_files_respects_skip_dirs() {
        let tmp = TempDir::new().unwrap();
        std::fs::create_dir_all(tmp.path().join("node_modules")).unwrap();
        std::fs::create_dir_all(tmp.path().join("src")).unwrap();
        std::fs::write(tmp.path().join("node_modules/x.test.ts"), "").unwrap();
        std::fs::write(tmp.path().join("src/x.test.ts"), "").unwrap();
        let matches = find_all_matching_test_files(tmp.path(), "x", &[]).unwrap();
        assert_eq!(matches.len(), 1);
        assert!(matches[0].to_string_lossy().contains("src"));
    }

    #[test]
    fn find_all_matching_test_files_returns_empty_for_missing_dir() {
        let matches = find_all_matching_test_files(Path::new("/nonexistent"), "x", &[]).unwrap();
        assert!(matches.is_empty());
    }

    #[test]
    fn collect_feature_files_falls_back_to_specs_dir_when_dirs_empty() {
        let tmp = TempDir::new().unwrap();
        let specs = tmp.path().join("specs");
        std::fs::create_dir_all(&specs).unwrap();
        std::fs::write(specs.join("x.feature"), "Feature: x").unwrap();
        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            specs_dir: specs.clone(),
            specs_dirs: vec![],
            app_dir: PathBuf::new(),
            verbose: false,
            quiet: false,
            shared_steps: false,
            exclude_dirs: vec![],
            exclude_source_dirs: vec![],
        };
        let files = collect_feature_files(&opts).unwrap();
        assert_eq!(files.len(), 1);
    }

    #[test]
    fn check_all_shared_steps_skips_file_matching() {
        let tmp = TempDir::new().unwrap();
        let specs = tmp.path().join("specs");
        let app = tmp.path().join("app");
        std::fs::create_dir_all(&specs).unwrap();
        std::fs::create_dir_all(&app).unwrap();
        std::fs::write(
            specs.join("foo.feature"),
            "Feature: x\nScenario: T\n  Given user logs in\n",
        )
        .unwrap();
        std::fs::write(
            app.join("steps.go"),
            "// stub\nfunc x(sc *godog.ScenarioContext) {\n  sc.Step(`^user logs in$`, fn)\n}\n",
        )
        .unwrap();
        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            specs_dir: specs.clone(),
            specs_dirs: vec![],
            app_dir: app.clone(),
            verbose: false,
            quiet: false,
            shared_steps: true,
            exclude_dirs: vec![],
            exclude_source_dirs: vec![],
        };
        let r = check_all(&opts).unwrap();
        assert_eq!(r.gaps.len(), 0); // shared_steps skips file matching
        assert_eq!(r.step_gaps.len(), 0); // step is covered
        assert_eq!(r.total_scenarios, 1);
    }
}
