@specs-gherkin-cardinality
Feature: `specs gherkin-cardinality validate` enforces Given/When/Then keyword cardinality

  As a maintainer enforcing the Gherkin step-keyword cardinality HARD rule
  (see repo-governance/development/infra/acceptance-criteria.md)
  I want `specs gherkin-cardinality validate` to flag any scenario that uses a
  primary Given/When/Then keyword more than once
  So that malformed multi-When/multi-Then scenarios are caught before merge

  Scenario: A scenario with two primary When keywords fails the audit
    Given a feature file containing a scenario with two primary "When" keywords
    When the developer runs specs gherkin-cardinality validate on the file
    Then the command exits with a failure code
    And the output names the offending file and scenario
