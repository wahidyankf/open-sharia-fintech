@specs-audit
Feature: `specs audit` aggregates every specs validator into one pass/fail report

  As a maintainer running the full spec-tree quality gate in one command
  I want `specs audit` to run the structure, link, and gherkin-cardinality
  validators in sequence and report a single result
  So that a clean spec tree is confirmed compliant without invoking each
  validator by hand

  Scenario: Every specs validator passes on a repository with no spec violations
    Given a repository with no spec-tree violations
    When the developer runs rhino-cli specs audit
    Then the command exits successfully
    And the output contains "SPECS AUDIT PASSED"
