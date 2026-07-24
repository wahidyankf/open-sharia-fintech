//! Gherkin feature-file parser.
//!
//! Byte-for-byte port of `apps/rhino-cli/internal/speccoverage/parser.go`.
//! Implements the same rules as the Go original:
//!
//! - `Background:` steps are collected and inserted as a synthetic
//!   `"(Background)"` scenario at position 0.
//! - `Scenario Outline:` steps have their `<placeholder>` tokens expanded
//!   for each row in the associated `Examples:` table and stored in
//!   [`ParsedStep::variants`].
//! - Plain `Scenario:` steps have an empty `variants` vector.

use std::fs::File;
use std::io::{BufRead, BufReader};
use std::path::Path;

use anyhow::Error;

/// A single parsed Gherkin step.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ParsedStep {
    /// Gherkin keyword without trailing whitespace (e.g. `"Given"`, `"When"`, `"Then"`).
    pub keyword: String,
    /// Step text after the keyword, with `<placeholder>` tokens left verbatim.
    pub text: String,
    /// Expanded step texts produced by substituting each `Examples` row into
    /// the `<placeholder>` tokens.  Empty for plain (non-outline) steps.
    pub variants: Vec<String>,
}

/// A single parsed Gherkin scenario (or the synthetic `Background` scenario).
#[derive(Debug, Clone, PartialEq, Eq, Default)]
pub struct ParsedScenario {
    /// Scenario title as it appears after `Scenario:` or `Scenario Outline:`.
    /// The synthetic background uses the title `"(Background)"`.
    pub title: String,
    /// Ordered list of steps belonging to this scenario.
    pub steps: Vec<ParsedStep>,
    /// `true` if a `@wip` tag line immediately precedes this scenario (allowing
    /// intervening blank lines and `#`-comments, matching the Gherkin tag-attachment rule
    /// `behavior_coverage::extract` already applies for the marker-existence checker).
    /// Step-coverage checkers in this module use this to exempt the scenario from step-gap
    /// (and, in one-to-one mode, scenario-gap) reporting — the same "`@wip` scenarios are
    /// fully exempt" rule `behavior_coverage::validator` documents for its own coverage check.
    pub is_wip: bool,
}

/// Gherkin step keywords recognised by the parser (each includes a trailing space).
const STEP_KEYWORDS: [&str; 5] = ["Given ", "When ", "Then ", "And ", "But "];

/// Parses a `.feature` file and returns all scenarios, including a synthetic
/// `(Background)` scenario prepended when a `Background:` block is present.
///
/// # Errors
///
/// Returns an error if the file cannot be opened or if a line cannot be read.
pub fn parse_feature_file(path: &Path) -> std::result::Result<Vec<ParsedScenario>, Error> {
    let (scenarios, _, ()) = parse_feature_file_inner(path)?;
    Ok(scenarios)
}

/// Returns all expanded step texts produced by `Scenario Outline` + `Examples`
/// substitution in the given feature file.
///
/// Useful for collecting the full set of concrete step strings when checking
/// whether step definitions cover parametrised scenarios.
///
/// # Errors
///
/// Returns an error if the file cannot be opened or if a line cannot be read.
pub fn expanded_outline_step_texts(path: &Path) -> std::result::Result<Vec<String>, Error> {
    let (_, expanded, ()) = parse_feature_file_inner(path)?;
    Ok(expanded)
}

/// Internal parser implementation shared by [`parse_feature_file`] and
/// [`expanded_outline_step_texts`].
///
/// Returns a triple of `(scenarios, expanded_steps, ())`.
///
/// # Errors
///
/// Returns an error if the file cannot be opened or if a line cannot be read.
fn parse_feature_file_inner(
    path: &Path,
) -> std::result::Result<(Vec<ParsedScenario>, Vec<String>, ()), Error> {
    let file = File::open(path)?;
    let mut scenarios: Vec<ParsedScenario> = Vec::new();
    let mut expanded_steps: Vec<String> = Vec::new();
    let mut bg_steps: Vec<ParsedStep> = Vec::new();
    let mut in_background = false;

    // Index of current scenario in `scenarios` (None when not inside one).
    let mut current_idx: Option<usize> = None;

    // Outline tracking — indices of outline steps within current.steps so we can
    // populate their variants when Examples rows arrive.
    let mut pending_outline_indices: Option<Vec<usize>> = None;

    let mut in_examples = false;
    let mut ex_headers: Option<Vec<String>> = None;

    // `true` once a `@wip` tag line has been seen and not yet consumed by (or discarded before)
    // the next `Scenario:`/`Scenario Outline:` line — mirrors the tag-attachment rule
    // `behavior_coverage::extract::extract_scenario_specs` already applies: a tag line attaches
    // to the next scenario line, surviving intervening blank lines, but is discarded by any other
    // non-blank content line (e.g. a `Feature:`-level tag must never leak onto the first scenario).
    let mut pending_wip = false;

    for raw in BufReader::new(file).lines() {
        let Ok(line_owned) = raw else { continue };
        let line = line_owned.trim();

        if line.is_empty() {
            continue;
        }

        if line.starts_with('@') {
            if line.split_whitespace().any(|tag| tag == "@wip") {
                pending_wip = true;
            }
            continue;
        }

        // A `#`-comment line is invisible to real Gherkin's tag-to-scenario association (see
        // `behavior_coverage::extract::extract_scenario_specs`'s identical branch) — skip it
        // without touching `pending_wip` so a comment between `@wip` and the scenario line it
        // tags does not silently discard the exemption.
        if line.starts_with('#') {
            continue;
        }

        if line.starts_with("Background:") {
            in_examples = false;
            ex_headers = None;
            pending_outline_indices = None;
            in_background = true;
            current_idx = None;
            pending_wip = false;
            continue;
        }

        if let Some(rest) = line.strip_prefix("Scenario Outline:") {
            in_examples = false;
            ex_headers = None;
            in_background = false;
            scenarios.push(ParsedScenario {
                title: rest.trim().to_string(),
                steps: Vec::new(),
                is_wip: pending_wip,
            });
            current_idx = Some(scenarios.len() - 1);
            pending_outline_indices = Some(Vec::new());
            pending_wip = false;
            continue;
        }
        if let Some(rest) = line.strip_prefix("Scenario:") {
            in_examples = false;
            ex_headers = None;
            in_background = false;
            scenarios.push(ParsedScenario {
                title: rest.trim().to_string(),
                steps: Vec::new(),
                is_wip: pending_wip,
            });
            current_idx = Some(scenarios.len() - 1);
            pending_outline_indices = None;
            pending_wip = false;
            continue;
        }

        if line.starts_with("Examples:") {
            in_examples = true;
            ex_headers = None;
            continue;
        }

        if in_examples && line.starts_with('|') {
            handle_examples_row(
                line,
                &mut ex_headers,
                pending_outline_indices.as_ref(),
                current_idx,
                &mut scenarios,
                &mut expanded_steps,
            );
            continue;
        }

        if try_push_step_line(
            line,
            in_background,
            current_idx,
            &mut pending_outline_indices,
            &mut scenarios,
            &mut bg_steps,
        ) {
            continue;
        }

        // A stray non-keyword content line — discard any tag that never attached to a scenario
        // (e.g. a `Feature:`-level tag), mirroring `extract::extract_scenario_specs`.
        pending_wip = false;
    }

    if !bg_steps.is_empty() {
        let bg = ParsedScenario {
            title: "(Background)".to_string(),
            steps: bg_steps,
            is_wip: false,
        };
        scenarios.insert(0, bg);
    }

    Ok((scenarios, expanded_steps, ()))
}

/// Handles a single `Examples:` table row line: the first row seen is captured as the header row
/// into `ex_headers`; every later row expands pending `Scenario Outline:` step placeholders via
/// [`expand_step`], pushing each expansion onto the matching step's `variants` and onto
/// `expanded_steps`.
///
/// Extracted out of [`parse_feature_file_inner`] purely to keep that function's line count within
/// the repo's clippy `too_many_lines` budget; behavior is unchanged from the original inline block.
fn handle_examples_row(
    line: &str,
    ex_headers: &mut Option<Vec<String>>,
    pending_outline_indices: Option<&Vec<usize>>,
    current_idx: Option<usize>,
    scenarios: &mut [ParsedScenario],
    expanded_steps: &mut Vec<String>,
) {
    let row = parse_row(line);
    if ex_headers.is_none() {
        *ex_headers = Some(row);
        return;
    }
    let (Some(idxs), Some(idx)) = (pending_outline_indices, current_idx) else {
        return;
    };
    let headers = ex_headers
        .as_ref()
        .expect("ex_headers is Some — is_none() branch above returns");
    for &step_idx in idxs {
        let text = scenarios[idx].steps[step_idx].text.clone();
        let exp = expand_step(&text, headers, &row);
        scenarios[idx].steps[step_idx].variants.push(exp.clone());
        expanded_steps.push(exp);
    }
}

/// Attempts to match `line` against a Gherkin step keyword (see [`STEP_KEYWORDS`]) and, on a
/// match, appends the parsed step to `bg_steps` (inside a `Background:` block) or to the current
/// scenario's step list (indexed by `current_idx`), recording its index in
/// `pending_outline_indices` when inside a `Scenario Outline:` block.
///
/// Returns `true` if a step keyword matched, `false` otherwise — extracted out of
/// [`parse_feature_file_inner`] purely to keep that function's line count within the repo's
/// clippy `too_many_lines` budget; behavior is unchanged from the original inline loop.
fn try_push_step_line(
    line: &str,
    in_background: bool,
    current_idx: Option<usize>,
    pending_outline_indices: &mut Option<Vec<usize>>,
    scenarios: &mut [ParsedScenario],
    bg_steps: &mut Vec<ParsedStep>,
) -> bool {
    for kw in STEP_KEYWORDS {
        if let Some(rest) = line.strip_prefix(kw) {
            let step = ParsedStep {
                keyword: kw.trim().to_string(),
                text: rest.trim().to_string(),
                variants: Vec::new(),
            };
            if in_background {
                bg_steps.push(step);
            } else if let Some(idx) = current_idx {
                scenarios[idx].steps.push(step);
                if let Some(idxs) = pending_outline_indices.as_mut() {
                    idxs.push(scenarios[idx].steps.len() - 1);
                }
            }
            return true;
        }
    }
    false
}

/// Splits a Gherkin table row into its cell values, trimming whitespace.
///
/// Leading and trailing pipe characters are removed before splitting.
fn parse_row(line: &str) -> Vec<String> {
    let s = line.trim().trim_matches('|');
    s.split('|').map(|p| p.trim().to_string()).collect()
}

/// Substitutes `<header>` tokens in `text` with the corresponding values from
/// `row`, paired by index into `headers`.
///
/// If `row` is shorter than `headers`, the excess headers are left unexpanded.
fn expand_step(text: &str, headers: &[String], row: &[String]) -> String {
    let mut out = text.to_string();
    for (i, h) in headers.iter().enumerate() {
        if i >= row.len() {
            break;
        }
        out = out.replace(&format!("<{h}>"), &row[i]);
    }
    out
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::TempDir;

    fn write_feature(content: &str) -> (TempDir, std::path::PathBuf) {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.feature");
        fs::write(&p, content).unwrap();
        (tmp, p)
    }

    #[test]
    fn parses_simple_scenario_with_three_steps() {
        let (_tmp, p) = write_feature(
            "Feature: foo\n\nScenario: bar\n  Given a precondition\n  When an action\n  Then an outcome\n",
        );
        let scenarios = parse_feature_file(&p).unwrap();
        assert_eq!(scenarios.len(), 1);
        assert_eq!(scenarios[0].title, "bar");
        assert_eq!(scenarios[0].steps.len(), 3);
        assert_eq!(scenarios[0].steps[0].keyword, "Given");
        assert_eq!(scenarios[0].steps[0].text, "a precondition");
        assert_eq!(scenarios[0].steps[2].keyword, "Then");
    }

    #[test]
    fn background_steps_yield_synthetic_first_scenario() {
        let (_tmp, p) = write_feature(
            "Feature: foo\n\nBackground:\n  Given baseline\n\nScenario: bar\n  Then result\n",
        );
        let scenarios = parse_feature_file(&p).unwrap();
        assert_eq!(scenarios.len(), 2);
        assert_eq!(scenarios[0].title, "(Background)");
        assert_eq!(scenarios[0].steps[0].text, "baseline");
        assert_eq!(scenarios[1].title, "bar");
    }

    #[test]
    fn outline_steps_get_variants_per_examples_row() {
        let (_tmp, p) = write_feature(
            "Feature: foo\n\nScenario Outline: bar\n  Given <state>\n  Then <result>\n\nExamples:\n  | state | result |\n  | A     | X      |\n  | B     | Y      |\n",
        );
        let scenarios = parse_feature_file(&p).unwrap();
        assert_eq!(scenarios.len(), 1);
        assert_eq!(scenarios[0].steps[0].text, "<state>");
        assert_eq!(scenarios[0].steps[0].variants, vec!["A", "B"]);
        assert_eq!(scenarios[0].steps[1].variants, vec!["X", "Y"]);
    }

    #[test]
    fn expanded_outline_step_texts_returns_all_variants() {
        let (_tmp, p) = write_feature(
            "Scenario Outline: x\n  Given <s>\n\nExamples:\n  | s |\n  | A |\n  | B |\n",
        );
        let exp = expanded_outline_step_texts(&p).unwrap();
        assert_eq!(exp, vec!["A", "B"]);
    }

    #[test]
    fn missing_file_returns_error() {
        let err = parse_feature_file(Path::new("/nonexistent/foo.feature")).unwrap_err();
        assert!(!err.to_string().is_empty());
    }

    // RED: `ParsedScenario` did not track the `@wip` tag at all — every scenario parsed as
    // `is_wip: false` regardless of its tag line, so a step-coverage checker built on this parser
    // (checker.rs's `check_shared_steps`/`check_one_to_one`) had no way to exempt a `@wip` scenario
    // from step-gap reporting, even though `behavior_coverage::validator` documents "`@wip` scenarios
    // are fully exempt" as the repo-wide rule. This test is falsifiable both ways: a parser that
    // ignores tags entirely fails the first assertion (untagged scenario) trivially (both would read
    // `false`) but fails the second (tagged scenario) because it can never read `true`.
    #[test]
    fn wip_tagged_scenario_is_flagged_is_wip() {
        let (_tmp, p) = write_feature(
            "Feature: foo\n\nScenario: untagged\n  Given a precondition\n\n@wip\nScenario: tagged\n  Given another precondition\n",
        );
        let scenarios = parse_feature_file(&p).unwrap();
        assert_eq!(scenarios.len(), 2);
        assert_eq!(scenarios[0].title, "untagged");
        assert!(
            !scenarios[0].is_wip,
            "untagged scenario must not be flagged wip"
        );
        assert_eq!(scenarios[1].title, "tagged");
        assert!(
            scenarios[1].is_wip,
            "@wip-tagged scenario must be flagged wip"
        );
    }

    // RED: a tag line stacked above `Scenario Outline:` must also flag `is_wip` — the exemption
    // must not silently apply only to plain `Scenario:` blocks.
    #[test]
    fn wip_tag_applies_to_scenario_outline_too() {
        let (_tmp, p) = write_feature(
            "Feature: foo\n\n@wip\nScenario Outline: bar\n  Given <state>\n\nExamples:\n  | state |\n  | A     |\n",
        );
        let scenarios = parse_feature_file(&p).unwrap();
        assert_eq!(scenarios.len(), 1);
        assert!(scenarios[0].is_wip);
    }

    // RED: a `Feature:`-level tag (or any other stray tag line not immediately followed by a
    // scenario line) must never leak onto the next real scenario it happens to precede.
    #[test]
    fn wip_tag_does_not_leak_across_an_intervening_content_line() {
        let (_tmp, p) =
            write_feature("@wip\nFeature: foo\n\nScenario: untagged\n  Given a precondition\n");
        let scenarios = parse_feature_file(&p).unwrap();
        assert_eq!(scenarios.len(), 1);
        assert!(
            !scenarios[0].is_wip,
            "a Feature-level tag must not leak onto the first scenario"
        );
    }

    // RED: before the fix, a `#`-comment line between `@wip` and its `Scenario:` line fell
    // through to the stray-content-line branch and reset `pending_wip = false`, silently
    // dropping the exemption — mirroring
    // `extract::extract_scenario_specs_tag_survives_a_comment_line_before_the_scenario`, which
    // this doc comment on `is_wip` claims to match.
    #[test]
    fn wip_tag_survives_a_comment_line_before_the_scenario() {
        let (_tmp, p) =
            write_feature("@wip\n# some comment\nScenario: tagged\n  Given a precondition\n");
        let scenarios = parse_feature_file(&p).unwrap();
        assert_eq!(scenarios.len(), 1);
        assert!(
            scenarios[0].is_wip,
            "@wip must survive an intervening `#`-comment line before the Scenario: line"
        );
    }
}
