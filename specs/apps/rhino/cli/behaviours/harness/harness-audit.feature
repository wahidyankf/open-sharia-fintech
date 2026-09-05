@harness-audit
Feature: `harness audit` aggregates every harness validator into one pass/fail report

  As a maintainer running the full agent-harness gate in one command
  I want `harness audit` to run every harness validator in sequence and report
  a single result
  So that missing platform-binding directories are caught even when naming
  and duplication checks pass

  Scenario: Missing agent directories fail the aggregate harness audit
    Given a repository with no .claude or .opencode agent directories
    When the developer runs "rhino-cli harness audit"
    Then the command exits with a failure code
    And the output names the failing "validate-claude" harness validator
