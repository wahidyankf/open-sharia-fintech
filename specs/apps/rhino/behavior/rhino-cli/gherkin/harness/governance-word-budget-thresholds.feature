@governance-word-budget-thresholds
Feature: Governance word-budget gate

  As a repository maintainer
  I want all auto-loaded instruction surfaces to stay within configured word thresholds
  So that coding-agent harnesses load instruction files completely without silent truncation

  Background:
    Given a committed "governance-word-budget.yaml" mapping instruction-file globs to target, warn, and fail word thresholds

  Scenario: A file within target passes silently
    Given "AGENTS.md" is 400 words
    And its target is 400 and its fail ceiling is 500
    When the developer runs governance word-budget validate
    Then the command exits successfully
    And the file is reported with severity "ok"

  Scenario: A file over target but under the ceiling warns without failing
    Given "AGENTS.md" is 450 words
    And its target is 400 and its fail ceiling is 500
    When the developer runs governance word-budget validate
    Then the command exits successfully
    And the file is reported with severity "warn"

  Scenario: A file over its hard ceiling fails the command
    Given "AGENTS.md" is 600 words
    And its fail ceiling is 500
    When the developer runs governance word-budget validate
    Then the command exits with a failure code
    And the file is reported with severity "fail"

  Scenario: A configured glob matching no file is a no-op
    Given no file exists at ".codex/agents/example.md"
    When the developer runs governance word-budget validate
    Then no finding is emitted for ".codex/agents/example.md"

  Scenario: The resolved tree is checked against the fail ceiling
    Given "CLAUDE.md" imports "AGENTS.md" via "@AGENTS.md"
    And the sum of "CLAUDE.md" plus the imported files exceeds the 1500-word tree ceiling
    When the developer runs governance word-budget validate
    Then a finding with key "resolved-tree" is reported with severity "fail"

  Scenario: The legacy registry-merge alias no longer exists
    When the developer runs harness instruction-size validate
    Then the command exits with a usage error
    And the output reports an unknown subcommand
