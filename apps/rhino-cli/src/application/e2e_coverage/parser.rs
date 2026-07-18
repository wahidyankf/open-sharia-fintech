//! Declared-scenario extraction and generated-output scanning for the e2e
//! scenario coverage gap detector.

use std::path::Path;
use std::sync::OnceLock;

use anyhow::Error;
use regex::Regex;

use crate::application::behavior_coverage::extract::extract_scenario_specs;
use crate::application::behavior_coverage::types::TestLevel;

use super::types::BaselineEntry;

/// Extracts the declared `@e2e` scenario set from a `.feature` file.
///
/// Delegates to [`extract_scenario_specs`] (shared with the behavior-coverage
/// engine) and filters to scenarios tagged `@e2e` — untagged and
/// `@unit`/`@integration`-only scenarios are not part of this gate's declared
/// set (AC-5).
///
/// # Errors
///
/// Returns an error if `path` cannot be read.
pub fn extract_declared(path: &Path, feature_path: &str) -> Result<Vec<BaselineEntry>, Error> {
    let specs = extract_scenario_specs(path, feature_path)?;
    Ok(specs
        .into_iter()
        .filter(|s| s.level_tags.contains(&TestLevel::E2e))
        .map(|s| BaselineEntry {
            feature: s.feature_path,
            scenario: s.title,
        })
        .collect())
}

/// Scans playwright-bdd generated `.spec.js` source for `test.fixme(...)`
/// call titles — the literal signal playwright-bdd emits for a scenario its
/// `missingSteps: "skip-scenario"` config silently skipped for lacking a step
/// definition (see the `e2e-scenario-coverage-gap-detector` plan's
/// `tech-docs.md` DD-2).
///
/// Only sees a plain `Scenario:`'s own title this way — a `Scenario
/// Outline`'s Examples-row tests are titled per playwright-bdd's own
/// convention (`Example #<N>` by default), never the outline's declared
/// title, so an unbound Outline is invisible here; see
/// [`scan_unbound_describe_titles`] for that case.
pub fn scan_fixme_titles(spec_js: &str) -> Vec<String> {
    fixme_title_re()
        .captures_iter(spec_js)
        .map(|caps| captured_title(&caps))
        .collect()
}

/// Scans playwright-bdd generated `.spec.js` source for `test.describe(...)`
/// blocks that contain at least one nested `test.fixme(...)` call, returning
/// each such block's own (unescaped) title.
///
/// playwright-bdd wraps every `Scenario Outline`'s Examples-row-derived tests
/// in one `test.describe` block titled with the outline's own raw Gherkin
/// title (`node_modules/playwright-bdd/dist/generate/file.js`'s
/// `renderScenarioOutline` → `formatter.describe`) — the individual tests
/// inside are titled per playwright-bdd's own Examples-row convention
/// (`Example #<N>` by default; see `examplesTitleBuilder.js`'s
/// `getDefaultTitle`), which never exact-matches the outline's own declared
/// title. So [`scan_fixme_titles`] alone can never see an unbound Outline —
/// the generated title it captures per unbound row is `Example #<N>`, not
/// the outline's title. This function closes that gap by matching on the
/// wrapping `describe` block's title instead: an outline is treated as
/// unbound if ANY of its Examples-row tests is `test.fixme` (see the
/// `e2e-scenario-coverage-gap-detector` plan's `tech-docs.md` DD-6).
///
/// A block's extent is found by matching leading-whitespace width between
/// its `test.describe(...)` open line and its own closing `});` line —
/// playwright-bdd's generator always indents a block's open and close lines
/// identically (both are emitted as un-indented siblings of the same
/// returned array, then uniformly re-indented together by whichever parent
/// block wraps them; see `formatter.js`'s `describe()`/`indent()`), so this
/// never requires full JS parsing or brace-balancing. This also means an
/// enclosing `Feature`/`Rule`-level `describe` (which wraps everything below
/// it) is itself matched and, if the feature has ANY unbound scenario
/// anywhere, reported too — harmless, since a Feature/Rule name never
/// collides with a declared scenario title.
pub fn scan_unbound_describe_titles(spec_js: &str) -> Vec<String> {
    let lines: Vec<&str> = spec_js.lines().collect();
    let mut result = Vec::new();
    for (i, line) in lines.iter().enumerate() {
        let Some(caps) = describe_re().captures(line) else {
            continue;
        };
        // playwright-bdd collapses a describe with zero children onto a
        // single line (`test.describe('title', () => {});`) — its body is
        // trivially empty, so it can never contain a nested test.fixme.
        if line.trim_end().ends_with("{});") {
            continue;
        }
        let indent = leading_whitespace_len(line);
        let contains_fixme = lines[i + 1..]
            .iter()
            .take_while(|candidate| {
                !(candidate.trim() == "});" && leading_whitespace_len(candidate) == indent)
            })
            .any(|candidate| candidate.contains("test.fixme("));
        if contains_fixme {
            result.push(captured_title(&caps));
        }
    }
    result
}

/// Matches either a single-quoted or double-quoted JS string literal,
/// respecting backslash-escaped characters (including an escaped instance of
/// the literal's own delimiter) so a match never terminates early at an
/// escaped quote. Shared between [`fixme_title_re`] and [`describe_re`] —
/// both extract a JS string literal argument from a generated `.spec.js`
/// call, and playwright-bdd's `jsStringWrap` always uses this same
/// backslash-escaping convention regardless of which call emits the string
/// (see [`unescape_js_string`]). Capture group 1 holds a single-quoted body,
/// group 2 a double-quoted body — exactly one is `Some` per match. Rust's
/// `regex` crate has no backreferences/lookaround, so the two quote styles
/// are matched via separate alternatives rather than one delimiter-agnostic
/// pattern.
const QUOTED_JS_STRING: &str = r#"(?:'((?:\\.|[^'\\])*)'|"((?:\\.|[^"\\])*)")"#;

/// Matches a `test.fixme("<title>", ...)` call's title argument.
///
/// Deliberately matches only `test.fixme(` (not bare `test(`) — playwright-bdd
/// emits `test.fixme` exclusively for scenarios `missingSteps:
/// "skip-scenario"` silently skipped for lacking a step definition.
fn fixme_title_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(&format!(r"test\.fixme\(\s*{QUOTED_JS_STRING}")).expect("valid regex")
    })
}

/// Matches a `test.describe("<title>", ...)` (or `test.describe.only(...)`,
/// `.skip(...)`, etc.) block's title argument — never an anonymous
/// `test.describe(() => {{ ... }})` (playwright-bdd's retry-wrapper for a
/// single `Scenario`), since that has no quoted string in the title
/// position at all.
fn describe_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(&format!(r"test\.describe(?:\.\w+)?\(\s*{QUOTED_JS_STRING}"))
            .expect("valid regex")
    })
}

/// Extracts and unescapes a [`QUOTED_JS_STRING`] match's captured body —
/// whichever of the two alternative capture groups matched (single- or
/// double-quoted).
fn captured_title(caps: &regex::Captures<'_>) -> String {
    let raw = caps
        .get(1)
        .or_else(|| caps.get(2))
        .map(|m| m.as_str())
        .unwrap_or_default();
    unescape_js_string(raw)
}

/// Reverses playwright-bdd's `jsStringWrap` escaping
/// (`node_modules/playwright-bdd/dist/utils/jsStringWrap.js`): it
/// backslash-escapes only the wrapping quote character and `\` itself, and
/// turns line-terminator characters into `\n`, `\r`, or a `\uNNNN` escape
/// (for the U+2028/U+2029 line/paragraph separators). Any other
/// backslash-escaped character is passed through literally (the backslash
/// is dropped) — matching ordinary JS semantics for an unrecognized
/// escape, and safely a no-op for text that was never escaped in the first
/// place.
fn unescape_js_string(raw: &str) -> String {
    let mut out = String::with_capacity(raw.len());
    let mut chars = raw.chars();
    while let Some(c) = chars.next() {
        if c != '\\' {
            out.push(c);
            continue;
        }
        match chars.next() {
            Some('n') => out.push('\n'),
            Some('r') => out.push('\r'),
            Some('t') => out.push('\t'),
            Some('u') => {
                let hex: String = chars.by_ref().take(4).collect();
                if let Some(decoded) = u32::from_str_radix(&hex, 16).ok().and_then(char::from_u32) {
                    out.push(decoded);
                } else {
                    // Malformed/short \u escape — preserve the raw text
                    // rather than silently losing data.
                    out.push('\\');
                    out.push('u');
                    out.push_str(&hex);
                }
            }
            Some(other) => out.push(other),
            // Trailing backslash with nothing after it — preserve as-is.
            None => out.push('\\'),
        }
    }
    out
}

/// Returns the number of leading whitespace characters (bytes, since
/// playwright-bdd's generator indents with plain ASCII spaces only) on
/// `line`.
fn leading_whitespace_len(line: &str) -> usize {
    line.len() - line.trim_start().len()
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature:A test.fixme scenario that is not @e2e-tagged is ignored
    #[test]
    fn declared_set_is_e2e_only() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.feature");
        std::fs::write(
            &p,
            "@unit\nScenario: A\n  Given a\n\n@e2e\nScenario: B\n  Given b\n",
        )
        .unwrap();

        let declared = extract_declared(&p, "specs/x.feature").unwrap();

        assert_eq!(declared.len(), 1);
        assert_eq!(declared[0].scenario, "B");
        assert_eq!(declared[0].feature, "specs/x.feature");
    }

    #[test]
    fn scan_finds_test_fixme_titles() {
        let spec_js = r#"
            test.fixme("Title A", async ({ page }) => {
                // unbound
            });
            test("Title B", async ({ page }) => {
                // bound
            });
        "#;

        let titles = scan_fixme_titles(spec_js);

        assert_eq!(titles, vec!["Title A".to_string()]);
    }

    /// Regression test for the apostrophe-truncation bug: a naive `[^"']+`
    /// capture group stops at an escaped apostrophe's quote character
    /// (mistaking it for the string's real closing quote), silently
    /// truncating the captured title. Reproduces playwright-bdd's default
    /// single-quote `jsStringWrap` escaping (`\'`) for a title containing a
    /// possessive.
    #[test]
    fn scan_fixme_titles_unescapes_single_quoted_apostrophe() {
        let spec_js = r"test.fixme('A user\'s profile renders correctly', async ({ page }) => {});";

        let titles = scan_fixme_titles(spec_js);

        assert_eq!(
            titles,
            vec!["A user's profile renders correctly".to_string()]
        );
    }

    /// A title containing trailing content AFTER the escaped apostrophe must
    /// not be silently dropped — the old `[^"']+` capture stopped so early
    /// that everything past the escaped quote (including the rest of the
    /// title) fell outside the match entirely.
    #[test]
    fn scan_fixme_titles_does_not_truncate_title_after_escaped_apostrophe() {
        let spec_js = r"test.fixme('It\'s working now', async ({ page }) => {});";

        let titles = scan_fixme_titles(spec_js);

        assert_eq!(titles, vec!["It's working now".to_string()]);
    }

    /// Double-quoted titles use playwright-bdd's `quotes: "double"` config
    /// convention, escaping `\"` instead of `\'`.
    #[test]
    fn scan_fixme_titles_unescapes_double_quoted_double_quote() {
        let spec_js = r#"test.fixme("Say \"hi\" now", async ({ page }) => {});"#;

        let titles = scan_fixme_titles(spec_js);

        assert_eq!(titles, vec!["Say \"hi\" now".to_string()]);
    }

    /// A literal backslash character in a title is escaped to `\\` by
    /// `jsStringWrap` regardless of quote style.
    #[test]
    fn scan_fixme_titles_unescapes_backslash() {
        let spec_js = r"test.fixme('back\\slash', async ({ page }) => {});";

        let titles = scan_fixme_titles(spec_js);

        assert_eq!(titles, vec!["back\\slash".to_string()]);
    }

    /// `jsStringWrap` only escapes the wrapping quote character and `\` —
    /// a double quote embedded in a single-quoted title passes through
    /// completely unescaped and must not be mistaken for the string's
    /// delimiter.
    #[test]
    fn scan_fixme_titles_preserves_unescaped_double_quote_inside_single_quoted_title() {
        let spec_js = r#"test.fixme('He said "hi"', async ({ page }) => {});"#;

        let titles = scan_fixme_titles(spec_js);

        assert_eq!(titles, vec!["He said \"hi\"".to_string()]);
    }

    /// Regression test for the Scenario-Outline blind spot: `scan_fixme_titles`
    /// alone never sees an unbound outline (its Examples-row tests are titled
    /// `Example #<N>`, never the outline's own title) — `scan_unbound_describe_titles`
    /// closes that gap by matching on the wrapping `describe` block instead.
    #[test]
    fn scan_unbound_describe_titles_detects_outline_with_unbound_example() {
        let spec_js = "\
test.describe('Outline title', () => {
  test.fixme('Example #1', async ({ page }) => {
  });
  test('Example #2', async ({ page }) => {
  });
});
";

        let titles = scan_unbound_describe_titles(spec_js);

        assert_eq!(titles, vec!["Outline title".to_string()]);
    }

    /// Negative counterpart: an outline whose Examples table is fully bound
    /// (zero `test.fixme` rows) must not be reported — guards against the
    /// fix itself over-matching every `describe` block regardless of its
    /// nested tests' state.
    #[test]
    fn scan_unbound_describe_titles_ignores_fully_bound_outline() {
        let spec_js = "\
test.describe('Outline title', () => {
  test('Example #1', async ({ page }) => {
  });
  test('Example #2', async ({ page }) => {
  });
});
";

        let titles = scan_unbound_describe_titles(spec_js);

        assert!(titles.is_empty());
    }

    /// A `describe` block with zero children collapses onto a single line
    /// (`test.describe('title', () => {});`) — its body is trivially empty
    /// and can never contain a nested `test.fixme`.
    #[test]
    fn scan_unbound_describe_titles_ignores_describe_with_zero_children() {
        let spec_js = "test.describe('Empty outline', () => {});\n";

        let titles = scan_unbound_describe_titles(spec_js);

        assert!(titles.is_empty());
    }

    /// Proves the indentation-based block-boundary matching correctly
    /// disambiguates SIBLING `describe` blocks nested under a common
    /// Feature-level `describe` — a naive "first `});` found anywhere after
    /// the open line" implementation would incorrectly extend a fully-bound
    /// outline's span into its unbound sibling's body (or vice versa).
    #[test]
    fn scan_unbound_describe_titles_disambiguates_sibling_outlines_under_a_feature_describe() {
        let spec_js = "\
test.describe('Feature', () => {
  test.describe('Bound outline', () => {
    test('Example #1', async ({ page }) => {
    });
  });
  test.describe('Unbound outline', () => {
    test.fixme('Example #1', async ({ page }) => {
    });
    test('Example #2', async ({ page }) => {
    });
  });
});
";

        let titles = scan_unbound_describe_titles(spec_js);

        assert!(
            titles.contains(&"Unbound outline".to_string()),
            "expected the outline with a test.fixme example to be detected, got: {titles:?}"
        );
        assert!(
            !titles.contains(&"Bound outline".to_string()),
            "a fully-bound outline (no nested test.fixme) must not be reported, got: {titles:?}"
        );
    }
}
