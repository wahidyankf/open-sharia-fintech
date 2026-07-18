//! Extraction helpers for the per-level @covers behavior coverage engine.
//!
//! Parses Gherkin scenario level tags (`@unit`/`@integration`/`@e2e`/`@wip`)
//! from `.feature` files into [`ScenarioSpec`]s, and `// @covers
//! <spec-path>:<scenario-title>` markers from test source files into
//! [`CoversMarker`]s — the two inputs [`super::validator::validate`] and
//! [`crate::application::speccoverage::runtime_check::check_runtime`] need,
//! neither of which the legacy
//! [`crate::application::speccoverage`] engine extracts today (it only
//! matches raw step text, not scenario-level tags or `@covers` markers).

use std::collections::HashSet;
use std::fs;
use std::path::Path;
use std::sync::OnceLock;

use anyhow::Error;
use regex::Regex;
use walkdir::WalkDir;

use super::types::{CoversMarker, ScenarioSpec, TestLevel};

/// Directory names skipped while walking a level dir for `@covers` markers —
/// generated output and dependency caches never carry hand-authored markers.
fn skip_dirs() -> &'static HashSet<&'static str> {
    static SET: OnceLock<HashSet<&'static str>> = OnceLock::new();
    SET.get_or_init(|| {
        ["node_modules", ".git", "target", "dist", "build", ".next"]
            .into_iter()
            .collect()
    })
}

/// Matches a `@covers <spec-path>:<scenario-title>` marker.
///
/// Deliberately matches the marker text alone, not any particular
/// comment-prefix syntax (`//`, `#`, `--`, …) — every language's marker
/// shares the same `@covers <path>:<title>` payload regardless of which
/// comment style wraps it.
fn covers_marker_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"@covers\s+(\S+):(.+?)\s*$").expect("valid regex"))
}

/// Recursively scans `dir` for `@covers <spec-path>:<scenario-title>`
/// markers, tagging every marker found with `level` — the caller already
/// knows which level `dir` represents (e.g. a project's `--unit-dir`).
///
/// `source_file` on each returned marker is repo-relative when `repo_root` is
/// a prefix of the marker's file path, and the raw path otherwise.
///
/// Returns an empty `Vec` if `dir` does not exist.
///
/// # Errors
///
/// Returns an error if the directory walk encounters an I/O error.
pub fn extract_covers_markers(
    dir: &Path,
    level: TestLevel,
    repo_root: &Path,
) -> Result<Vec<CoversMarker>, Error> {
    let mut markers = Vec::new();
    if !dir.exists() {
        return Ok(markers);
    }

    let walker = WalkDir::new(dir).into_iter().filter_entry(|e| {
        if e.file_type().is_dir() {
            let name = e.file_name().to_string_lossy();
            !skip_dirs().contains(name.as_ref())
        } else {
            true
        }
    });

    for entry in walker {
        let entry = entry?;
        if !entry.file_type().is_file() {
            continue;
        }
        let Ok(content) = fs::read_to_string(entry.path()) else {
            continue; // binary/non-UTF-8 files carry no markers
        };
        let source_file = if repo_root.as_os_str().is_empty() {
            entry.path().to_string_lossy().to_string()
        } else {
            entry.path().strip_prefix(repo_root).map_or_else(
                |_| entry.path().to_string_lossy().to_string(),
                |p| p.to_string_lossy().to_string(),
            )
        };
        for line in content.lines() {
            if let Some(caps) = covers_marker_re().captures(line) {
                markers.push(CoversMarker {
                    source_file: source_file.clone(),
                    level,
                    feature_path: caps[1].to_string(),
                    scenario_title: caps[2].trim().to_string(),
                });
            }
        }
    }
    Ok(markers)
}

/// Parses `path`'s `Scenario:`/`Scenario Outline:` blocks into
/// [`ScenarioSpec`]s, reading the `@unit`/`@integration`/`@e2e` level tags and
/// the `@wip` exemption tag declared on the tag line(s) immediately above
/// each scenario line — the same layout used throughout
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/specs/behavior-coverage.feature`.
///
/// `feature_path` is stored verbatim on every returned [`ScenarioSpec`] (the
/// caller supplies the repo-relative path so this function stays I/O-free
/// beyond reading `path` itself).
///
/// # Errors
///
/// Returns an error if the file cannot be read.
pub fn extract_scenario_specs(path: &Path, feature_path: &str) -> Result<Vec<ScenarioSpec>, Error> {
    let content = fs::read_to_string(path)?;
    let mut specs = Vec::new();
    let mut pending_tags: Vec<String> = Vec::new();

    for raw in content.lines() {
        let line = raw.trim();
        if line.is_empty() {
            continue;
        }
        if line.starts_with('@') {
            pending_tags.extend(line.split_whitespace().map(str::to_string));
            continue;
        }
        // A `#`-comment line is invisible to real Gherkin's tag-to-scenario
        // association: `@cucumber/gherkin` (what playwright-bdd's own
        // `generateMessages` call uses under the hood) simply ignores a
        // comment wherever it appears — before a tag, between stacked tags,
        // or between a tag and the `Scenario:`/`Scenario Outline:` line it
        // applies to — the tag still attaches to the next real keyword line.
        // Skipping the comment here (without touching `pending_tags`)
        // preserves any tags already accumulated instead of dropping them,
        // matching that real-parser behavior exactly.
        if line.starts_with('#') {
            continue;
        }
        // `Scenario Template:` is an official Gherkin dialect alias for
        // `Scenario Outline:` (`@cucumber/gherkin`'s `gherkin-languages.json`,
        // `en.scenarioOutline: ["Scenario Outline", "Scenario Template"]`) —
        // playwright-bdd renders real test output for either spelling, so
        // both must be recognised here to keep the declared set complete.
        let title = line
            .strip_prefix("Scenario Outline:")
            .or_else(|| line.strip_prefix("Scenario Template:"))
            .or_else(|| line.strip_prefix("Scenario:"));
        if let Some(title) = title {
            let mut level_tags = HashSet::new();
            let mut is_wip = false;
            for tag in &pending_tags {
                match tag.as_str() {
                    "@unit" => {
                        level_tags.insert(TestLevel::Unit);
                    }
                    "@integration" => {
                        level_tags.insert(TestLevel::Integration);
                    }
                    "@e2e" => {
                        level_tags.insert(TestLevel::E2e);
                    }
                    "@wip" => is_wip = true,
                    _ => {}
                }
            }
            specs.push(ScenarioSpec {
                feature_path: feature_path.to_string(),
                title: title.trim().to_string(),
                level_tags,
                is_wip,
            });
            pending_tags.clear();
            continue;
        }
        // Any other content line (Feature:, Background:, Given/When/Then,
        // Examples:, table rows, …) is not a tag line — clear any pending
        // tags that never attached to a scenario (e.g. Feature-level tags).
        pending_tags.clear();
    }
    Ok(specs)
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[test]
    fn extract_covers_markers_finds_rust_comment_marker() {
        let tmp = TempDir::new().unwrap();
        std::fs::write(
            tmp.path().join("test.rs"),
            "// @covers specs/apps/example/foo.feature:Logs in\nfn x() {}\n",
        )
        .unwrap();
        let markers = extract_covers_markers(tmp.path(), TestLevel::Unit, Path::new("")).unwrap();
        assert_eq!(markers.len(), 1);
        assert_eq!(markers[0].feature_path, "specs/apps/example/foo.feature");
        assert_eq!(markers[0].scenario_title, "Logs in");
        assert_eq!(markers[0].level, TestLevel::Unit);
    }

    #[test]
    fn extract_covers_markers_works_across_comment_styles() {
        let tmp = TempDir::new().unwrap();
        std::fs::write(
            tmp.path().join("test.py"),
            "# @covers specs/apps/example/foo.feature:Logs in\n",
        )
        .unwrap();
        let markers =
            extract_covers_markers(tmp.path(), TestLevel::Integration, Path::new("")).unwrap();
        assert_eq!(markers.len(), 1);
        assert_eq!(markers[0].level, TestLevel::Integration);
    }

    #[test]
    fn extract_covers_markers_returns_repo_relative_source_file() {
        let tmp = TempDir::new().unwrap();
        std::fs::create_dir_all(tmp.path().join("apps/example/tests")).unwrap();
        std::fs::write(
            tmp.path().join("apps/example/tests/test.rs"),
            "// @covers specs/apps/example/foo.feature:Logs in\n",
        )
        .unwrap();
        let markers = extract_covers_markers(
            &tmp.path().join("apps/example/tests"),
            TestLevel::Unit,
            tmp.path(),
        )
        .unwrap();
        assert_eq!(markers[0].source_file, "apps/example/tests/test.rs");
    }

    #[test]
    fn extract_covers_markers_returns_empty_for_missing_dir() {
        let markers =
            extract_covers_markers(Path::new("/nonexistent"), TestLevel::Unit, Path::new(""))
                .unwrap();
        assert!(markers.is_empty());
    }

    #[test]
    fn extract_scenario_specs_reads_level_tags() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.feature");
        std::fs::write(
            &p,
            "@unit\nScenario: A\n  Given a\n\n@integration @e2e\nScenario: B\n  Given b\n",
        )
        .unwrap();
        let specs = extract_scenario_specs(&p, "specs/x.feature").unwrap();
        assert_eq!(specs.len(), 2);
        assert_eq!(specs[0].title, "A");
        assert!(specs[0].level_tags.contains(&TestLevel::Unit));
        assert!(!specs[0].is_wip);
        assert_eq!(specs[1].title, "B");
        assert!(specs[1].level_tags.contains(&TestLevel::Integration));
        assert!(specs[1].level_tags.contains(&TestLevel::E2e));
    }

    #[test]
    fn extract_scenario_specs_reads_wip_tag() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.feature");
        std::fs::write(&p, "@wip\nScenario: A\n  Given a\n").unwrap();
        let specs = extract_scenario_specs(&p, "specs/x.feature").unwrap();
        assert!(specs[0].is_wip);
        assert!(specs[0].level_tags.is_empty());
    }

    #[test]
    fn extract_scenario_specs_untagged_scenario_has_no_level_tags() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.feature");
        std::fs::write(&p, "Feature: x\n\nScenario: A\n  Given a\n").unwrap();
        let specs = extract_scenario_specs(&p, "specs/x.feature").unwrap();
        assert_eq!(specs.len(), 1);
        assert!(specs[0].level_tags.is_empty());
        assert!(!specs[0].is_wip);
    }

    #[test]
    fn extract_scenario_specs_scenario_outline_is_recognised() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.feature");
        std::fs::write(
            &p,
            "@unit\nScenario Outline: A\n  Given <x>\n\nExamples:\n  | x |\n  | 1 |\n",
        )
        .unwrap();
        let specs = extract_scenario_specs(&p, "specs/x.feature").unwrap();
        assert_eq!(specs.len(), 1);
        assert_eq!(specs[0].title, "A");
        assert!(specs[0].level_tags.contains(&TestLevel::Unit));
    }

    /// `Scenario Template:` is an official Gherkin dialect alias for
    /// `Scenario Outline:` (see `node_modules/@cucumber/gherkin`'s own
    /// `gherkin-languages.json`, `en.scenarioOutline: ["Scenario Outline",
    /// "Scenario Template"]`) — playwright-bdd genuinely renders a
    /// `test`/`test.fixme` for a scenario declared with this keyword, so it
    /// must be recognised here too, exactly like `Scenario Outline:`.
    #[test]
    fn extract_scenario_specs_recognises_scenario_template_alias() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.feature");
        std::fs::write(
            &p,
            "@e2e\nScenario Template: A\n  Given <x>\n\nExamples:\n  | x |\n  | 1 |\n",
        )
        .unwrap();
        let specs = extract_scenario_specs(&p, "specs/x.feature").unwrap();
        assert_eq!(specs.len(), 1);
        assert_eq!(specs[0].title, "A");
        assert!(specs[0].level_tags.contains(&TestLevel::E2e));
    }

    #[test]
    fn extract_scenario_specs_feature_level_tag_does_not_leak_into_first_scenario() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.feature");
        std::fs::write(&p, "@feature-tag\nFeature: x\n\nScenario: A\n  Given a\n").unwrap();
        let specs = extract_scenario_specs(&p, "specs/x.feature").unwrap();
        assert_eq!(specs.len(), 1);
        assert!(specs[0].level_tags.is_empty());
    }

    /// Regression test for a cycle-6 CRITICAL finding: real Gherkin (as
    /// parsed by `@cucumber/gherkin`, which playwright-bdd's own
    /// `generateMessages` call uses under the hood) does not break a tag's
    /// association with its scenario across an intervening `#`-comment line
    /// — the comment is simply ignored and the tag still applies. Before
    /// this fix, the tag-accumulation loop cleared `pending_tags` on ANY
    /// non-blank, non-tag, non-Scenario-keyword line, including a comment,
    /// so a tag separated from its scenario by a comment silently vanished
    /// from the declared set.
    #[test]
    fn extract_scenario_specs_tag_survives_a_comment_line_before_the_scenario() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.feature");
        std::fs::write(&p, "@e2e\n# some comment\nScenario: X\n  Given a\n").unwrap();
        let specs = extract_scenario_specs(&p, "specs/x.feature").unwrap();
        assert_eq!(specs.len(), 1);
        assert_eq!(specs[0].title, "X");
        assert!(
            specs[0].level_tags.contains(&TestLevel::E2e),
            "expected @e2e to survive the intervening comment line, got: {:?}",
            specs[0].level_tags
        );
    }

    /// Generalization check: a comment BETWEEN two stacked tag lines must
    /// not drop the earlier tag either — before the fix, the comment line
    /// cleared `pending_tags` outright, so only the tag(s) accumulated AFTER
    /// the comment survived to the scenario.
    #[test]
    fn extract_scenario_specs_tag_survives_a_comment_between_stacked_tags() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.feature");
        std::fs::write(&p, "@unit\n# some comment\n@e2e\nScenario: X\n  Given a\n").unwrap();
        let specs = extract_scenario_specs(&p, "specs/x.feature").unwrap();
        assert_eq!(specs.len(), 1);
        assert!(
            specs[0].level_tags.contains(&TestLevel::Unit),
            "expected @unit (accumulated before the comment) to survive, got: {:?}",
            specs[0].level_tags
        );
        assert!(
            specs[0].level_tags.contains(&TestLevel::E2e),
            "expected @e2e (accumulated after the comment) to be present too, got: {:?}",
            specs[0].level_tags
        );
    }

    /// Generalization check: a comment line BEFORE the first tag must not
    /// confuse the parser — `pending_tags` is empty at that point either
    /// way, so this mainly proves the comment-skip branch never panics or
    /// otherwise misbehaves when it has nothing pending to preserve.
    #[test]
    fn extract_scenario_specs_tolerates_a_comment_line_before_the_first_tag() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.feature");
        std::fs::write(&p, "# leading file comment\n@e2e\nScenario: X\n  Given a\n").unwrap();
        let specs = extract_scenario_specs(&p, "specs/x.feature").unwrap();
        assert_eq!(specs.len(), 1);
        assert!(specs[0].level_tags.contains(&TestLevel::E2e));
    }

    /// Generalization check: a comment line immediately before `Feature:`
    /// must not change the existing feature-level-tag-does-not-leak
    /// behavior — `Feature:` itself (a genuine content line, not a comment)
    /// still clears any pending feature-level tag, comment or no comment.
    #[test]
    fn extract_scenario_specs_comment_before_feature_line_does_not_change_leak_behavior() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("x.feature");
        std::fs::write(
            &p,
            "@feature-tag\n# comment\nFeature: x\n\nScenario: A\n  Given a\n",
        )
        .unwrap();
        let specs = extract_scenario_specs(&p, "specs/x.feature").unwrap();
        assert_eq!(specs.len(), 1);
        assert!(specs[0].level_tags.is_empty());
    }
}
