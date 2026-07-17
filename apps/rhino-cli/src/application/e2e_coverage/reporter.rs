//! Text/JSON/Markdown formatters for [`super::types::GapReport`].

use std::fmt::Write as _;

use anyhow::Error;
use serde::Serialize;

use super::types::{BaselineEntry, GapReport};

/// JSON output schema identifier for `specs e2e-coverage validate`.
const SCHEMA: &str = "rhino-cli/e2e-coverage/v1";

/// A `{feature, scenario}` entry as it appears in JSON output.
#[derive(Serialize)]
struct EntryJson<'a> {
    /// Repo-relative path to the `.feature` file.
    feature: &'a str,
    /// Scenario title.
    scenario: &'a str,
}

impl<'a> From<&'a BaselineEntry> for EntryJson<'a> {
    fn from(e: &'a BaselineEntry) -> Self {
        EntryJson {
            feature: &e.feature,
            scenario: &e.scenario,
        }
    }
}

/// JSON envelope wrapping a [`GapReport`].
#[derive(Serialize)]
struct Envelope<'a> {
    /// Output schema identifier.
    schema: &'a str,
    /// `"passed"` or `"failed"`.
    status: &'a str,
    /// New unbound scenarios beyond the baseline.
    result: Vec<EntryJson<'a>>,
    /// Baseline entries no longer emitted as `test.fixme`.
    stale: Vec<EntryJson<'a>>,
}

/// Writes the header line (pass/fail summary) shared by [`format_text`] and
/// [`format_markdown`].
fn header_line(report: &GapReport, prefix: &str, pass_label: &str, fail_label: &str) -> String {
    if report.new_gaps.is_empty() {
        format!("{prefix}{pass_label}: 0 new unbound scenario(s) beyond baseline")
    } else {
        format!(
            "{prefix}{fail_label}: {} new unbound scenario(s) found (increase of {} over baseline)",
            report.new_gaps.len(),
            report.new_gaps.len()
        )
    }
}

/// Formats `report` as human-readable text.
pub fn format_text(report: &GapReport) -> String {
    let mut sb = String::new();
    let _ = writeln!(
        sb,
        "{}",
        header_line(report, "E2E COVERAGE GAP DETECTOR ", "PASSED", "FAILED")
    );
    for g in &report.new_gaps {
        let _ = writeln!(sb, "  {}\n    -> Scenario: \"{}\"", g.feature, g.scenario);
    }
    if !report.stale.is_empty() {
        let _ = writeln!(
            sb,
            "\n{} stale baseline entrie(s) can be pruned:",
            report.stale.len()
        );
        for s in &report.stale {
            let _ = writeln!(sb, "  {}\n    -> Scenario: \"{}\"", s.feature, s.scenario);
        }
    }
    sb
}

/// Serializes `report` as a JSON envelope string.
///
/// # Errors
///
/// Returns an error if JSON serialization fails.
pub fn format_json(report: &GapReport) -> std::result::Result<String, Error> {
    let status = if report.new_gaps.is_empty() {
        "passed"
    } else {
        "failed"
    };
    let env = Envelope {
        schema: SCHEMA,
        status,
        result: report.new_gaps.iter().map(EntryJson::from).collect(),
        stale: report.stale.iter().map(EntryJson::from).collect(),
    };
    let mut s = serde_json::to_string_pretty(&env)?;
    s.push('\n');
    Ok(s)
}

/// Formats `report` as a Markdown report.
pub fn format_markdown(report: &GapReport) -> String {
    let mut sb = String::new();
    let _ = writeln!(
        sb,
        "## E2E Coverage Gap Detector\n\n**{}**\n",
        header_line(report, "", "PASSED", "FAILED")
    );
    if !report.new_gaps.is_empty() {
        sb.push_str("| Feature | Scenario |\n|---------|----------|\n");
        for g in &report.new_gaps {
            let _ = writeln!(sb, "| {} | {} |", g.feature, g.scenario);
        }
    }
    if !report.stale.is_empty() {
        let _ = writeln!(
            sb,
            "\n### Stale baseline entries ({})\n",
            report.stale.len()
        );
        sb.push_str("| Feature | Scenario |\n|---------|----------|\n");
        for s in &report.stale {
            let _ = writeln!(sb, "| {} | {} |", s.feature, s.scenario);
        }
    }
    sb
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::application::e2e_coverage::types::BaselineEntry;

    fn one_new_gap() -> GapReport {
        GapReport {
            new_gaps: vec![BaselineEntry {
                feature:
                    "specs/libs/web-ui/behavior/gherkin/resizable-panel/resizable-panel.feature"
                        .to_string(),
                scenario: "Resize the sidebar by keyboard".to_string(),
            }],
            stale: Vec::new(),
            failed: true,
        }
    }

    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature:Output identifies each new gap by feature path and scenario title
    #[test]
    fn text_report_names_feature_and_scenario() {
        let text = format_text(&one_new_gap());

        assert!(text.contains("Resize the sidebar by keyboard"));
        assert!(text.contains("resizable-panel.feature"));
        assert!(text.contains("increase of 1"));
    }

    #[test]
    fn text_report_passes_when_no_new_gaps() {
        let text = format_text(&GapReport::default());
        assert!(text.contains("PASSED"));
    }

    #[test]
    fn json_report_status_failed_with_gaps() {
        let s = format_json(&one_new_gap()).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["status"], "failed");
        assert_eq!(v["schema"], SCHEMA);
        assert_eq!(v["result"][0]["scenario"], "Resize the sidebar by keyboard");
    }

    #[test]
    fn json_report_status_passed_when_empty() {
        let s = format_json(&GapReport::default()).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["status"], "passed");
    }

    #[test]
    fn markdown_report_lists_new_gap() {
        let md = format_markdown(&one_new_gap());
        assert!(md.contains("**FAILED"));
        assert!(md.contains("Resize the sidebar by keyboard"));
    }
}
