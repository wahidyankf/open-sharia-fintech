@governance-word-budget-rule
Feature: Governance of the word-budget rule

  As a repository maintainer
  I want the word-budget rule documented, checker-aware, and preflight-tracked
  So that the gate is discoverable, AI-checkable, and deterministically enforced

  Scenario: The rule is documented as a convention
    Given the plan is complete
    When I look under "repo-governance/conventions/structure/"
    Then "governance-word-budget.md" exists
    And the file lists the monitored file classes, configured threshold source, and enforcement points

  Scenario: repo-rules-checker validates the budget qualitatively
    Given the plan is complete
    When "repo-rules-checker" runs Step 6
    Then it reports qualitative bloat concerns across the whole instruction-file class
    And it annotates that the word ceiling is enforced by the deterministic "governance-word-budget" gate

  Scenario: The quality-gate workflow delegates the validator by exact gate ID
    Given the plan is complete
    When I read "repo-governance/workflows/rules/rules-quality-gate.md"
    Then "governance-word-budget" is skipped locally and delegated from Step 0.5

  Scenario: The preflight envelope carries the governance-word-budget category
    Given a repo with instruction files within the configured budgets
    When the developer runs "rhino-cli repo-governance audit" with JSON output
    Then the envelope schema is "rhino-cli/repo-governance-audit/v1"
    And "result.categories" contains a category named "governance-word-budget"

  Scenario: The AI checker defers to lifecycle-gate evidence
    Given lifecycle evidence contains a current "governance-word-budget" result
    When "repo-rules-checker" runs Step 0.5
    Then it consumes the exact delegated gate ID "governance-word-budget"
    And it does not re-derive word counts in Step 6
