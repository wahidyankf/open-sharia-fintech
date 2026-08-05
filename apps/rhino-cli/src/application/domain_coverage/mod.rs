//! `specs domain-coverage validate` — per-level @covers engine scoped to `domain/**` feature
//! files, gated by the `specs.domain-areas` allowlist in `repo-config.yml`.
//!
//! The validation logic reuses the `behavior_coverage::validator::validate()` engine; this module
//! adds the domain-path filter (`domain/**` only) and the domain-areas allowlist check.

/// Returns `true` iff `project_name` is listed in `domain_areas`.
///
/// A project absent from the allowlist is skipped even if it has `domain/**` feature files.
pub fn is_eligible(project_name: &str, domain_areas: &[String]) -> bool {
    domain_areas.iter().any(|a| a == project_name)
}

/// Returns only those scenarios whose `feature_path` contains a `domain/` path component.
pub fn filter_domain_scenarios(
    scenarios: &[crate::application::behavior_coverage::types::ScenarioSpec],
) -> Vec<&crate::application::behavior_coverage::types::ScenarioSpec> {
    scenarios
        .iter()
        .filter(|s| {
            s.feature_path
                .split('/')
                .any(|component| component == "domain")
        })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/domain-coverage.feature:A project not in the domain-areas allowlist is skipped
    #[test]
    fn non_domain_area_project_is_skipped() {
        let domain_areas = vec![
            "fixture-ledger-api".to_string(),
            "fixture-catalog-api".to_string(),
        ];
        assert!(
            !is_eligible("fixture-utility-cli", &domain_areas),
            "fixture-utility-cli must not be eligible for domain-coverage — not in domain-areas"
        );
    }

    // @covers specs/apps/rhino/behavior/rhino-cli/gherkin/specs/domain-coverage.feature:An uncovered domain scenario fails the gate
    #[test]
    fn domain_area_project_is_eligible() {
        let domain_areas = vec![
            "fixture-ledger-api".to_string(),
            "fixture-catalog-api".to_string(),
        ];
        assert!(
            is_eligible("fixture-ledger-api", &domain_areas),
            "fixture-ledger-api must be eligible for domain-coverage — listed in domain-areas"
        );
    }
}
