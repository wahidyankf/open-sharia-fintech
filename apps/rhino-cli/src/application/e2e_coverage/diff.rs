//! Pure diff core for the e2e scenario coverage gap detector.

use std::collections::HashSet;

use super::types::{BaselineEntry, GapReport};

/// Computes the coverage gap diff for a project.
///
/// - `declared`: scenarios eligible for gap detection (typically `@e2e`-tagged
///   scenarios extracted from the project's consumed `.feature` files — see
///   `super::parser`).
/// - `fixme`: scenarios playwright-bdd's generated output emits as
///   `test.fixme` — the ground-truth "currently unbound" set.
/// - `baseline`: the checked-in manifest of scenarios previously accepted as
///   unbound.
///
/// [`GapReport::new_gaps`] is `(declared ∩ fixme) \ baseline` — scenarios
/// unbound today that the baseline has not yet accepted. A non-empty
/// `new_gaps` set fails the gate. [`GapReport::stale`] is `baseline \ fixme`
/// — baseline entries no longer emitted as `test.fixme`; it never affects
/// `failed`.
pub fn diff(
    declared: &[BaselineEntry],
    fixme: &[BaselineEntry],
    baseline: &[BaselineEntry],
) -> GapReport {
    let fixme_set: HashSet<&BaselineEntry> = fixme.iter().collect();
    let baseline_set: HashSet<&BaselineEntry> = baseline.iter().collect();

    let mut new_gaps = new_gaps(declared, &fixme_set, &baseline_set);
    new_gaps.sort();
    let mut stale = stale(baseline, &fixme_set);
    stale.sort();

    GapReport {
        failed: !new_gaps.is_empty(),
        new_gaps,
        stale,
    }
}

/// Computes `(declared ∩ fixme) \ baseline` — scenarios currently unbound
/// that the baseline has not yet accepted.
fn new_gaps(
    declared: &[BaselineEntry],
    fixme_set: &HashSet<&BaselineEntry>,
    baseline_set: &HashSet<&BaselineEntry>,
) -> Vec<BaselineEntry> {
    declared
        .iter()
        .filter(|e| fixme_set.contains(e) && !baseline_set.contains(e))
        .cloned()
        .collect()
}

/// Computes `baseline \ fixme` — baseline entries no longer emitted as
/// `test.fixme`.
fn stale(baseline: &[BaselineEntry], fixme_set: &HashSet<&BaselineEntry>) -> Vec<BaselineEntry> {
    baseline
        .iter()
        .filter(|e| !fixme_set.contains(e))
        .cloned()
        .collect()
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    /// Feature path shared by every fixture entry below.
    const FEATURE: &str = "specs/apps/example/gherkin/example.feature";

    /// Builds a `{feature, scenario}` entry for test fixtures.
    fn entry(scenario: &str) -> BaselineEntry {
        BaselineEntry {
            feature: FEATURE.to_string(),
            scenario: scenario.to_string(),
        }
    }

    /// Builds a `Vec<BaselineEntry>` from scenario titles, all sharing
    /// [`FEATURE`].
    fn set(scenarios: &[&str]) -> Vec<BaselineEntry> {
        scenarios.iter().map(|s| entry(s)).collect()
    }

    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature:A project's current unbound gaps exactly match its checked-in baseline
    #[test]
    fn baseline_match_passes() {
        let declared = set(&["A", "B"]);
        let fixme = set(&["A", "B"]);
        let baseline = set(&["A", "B"]);
        let report = diff(&declared, &fixme, &baseline);
        assert!(report.new_gaps.is_empty());
        assert!(!report.failed);
    }

    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature:A newly added @e2e scenario ships without a step definition
    #[test]
    fn new_gap_fails_and_named() {
        let declared = set(&["A", "C"]);
        let fixme = set(&["A", "C"]);
        let baseline = set(&["A"]);
        let report = diff(&declared, &fixme, &baseline);
        assert!(report.failed);
        assert_eq!(report.new_gaps, vec![entry("C")]);
    }

    // AC-3 ("newly bound relative to baseline") and AC-8 ("stale baseline
    // entry that can be pruned") describe the identical Given/When/Then
    // fixture and the identical computed set — baseline \ fixme — from two
    // narrative angles. `GapReport::stale` is the single field backing both
    // readings (see its doc comment in `types.rs`).

    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature:A previously-unbound scenario is now bound
    #[test]
    fn shrinkage_passes_and_reports_newly_bound() {
        let declared = set(&["A", "B"]);
        let fixme = set(&["A"]);
        let baseline = set(&["A", "B"]);
        let report = diff(&declared, &fixme, &baseline);
        assert!(!report.failed);
        assert_eq!(report.stale, vec![entry("B")]);
    }

    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature:The baseline lists a scenario that is no longer unbound
    #[test]
    fn stale_baseline_entry_reported() {
        let declared = set(&["A", "B"]);
        let fixme = set(&["A"]);
        let baseline = set(&["A", "B"]);
        let report = diff(&declared, &fixme, &baseline);
        assert!(!report.failed);
        assert_eq!(report.stale, vec![entry("B")]);
    }
}
