@governance-word-budget-agents-md
Feature: AGENTS.md word-budget audit

  As a repository maintainer
  I want to verify that AGENTS.md stays within word-size targets
  So that the canonical instruction surface remains short enough for coding agents to load efficiently

  Scenario: AGENTS.md within target size passes the audit
    Given a repository containing an AGENTS.md file of 350 words
    When the developer runs governance word-budget validate
    Then the command exits successfully
    And the output reports the AGENTS.md size as within target

  Scenario: AGENTS.md over the target size emits a warn finding
    Given a repository containing an AGENTS.md file of 450 words
    When the developer runs governance word-budget validate
    Then the command exits successfully
    And the output identifies AGENTS.md as over the target size

  Scenario: AGENTS.md over the hard limit fails the command
    Given a repository containing an AGENTS.md file of 600 words
    When the developer runs governance word-budget validate
    Then the command exits with a failure code
    And the output identifies AGENTS.md as over the hard limit
