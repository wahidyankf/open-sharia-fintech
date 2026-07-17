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
pub fn scan_fixme_titles(spec_js: &str) -> Vec<String> {
    fixme_title_re()
        .captures_iter(spec_js)
        .map(|caps| caps[1].to_string())
        .collect()
}

/// Matches a `test.fixme("<title>", ...)` call's title argument.
///
/// Deliberately matches only `test.fixme(` (not bare `test(`) — playwright-bdd
/// emits `test.fixme` exclusively for scenarios `missingSteps:
/// "skip-scenario"` silently skipped for lacking a step definition.
fn fixme_title_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r#"test\.fixme\(\s*["']([^"']+)["']"#).expect("valid regex"))
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
}
