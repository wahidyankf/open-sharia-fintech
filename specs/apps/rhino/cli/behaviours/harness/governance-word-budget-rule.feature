@governance-word-budget-rule
Feature: Governance of the word-budget rule

  As a repository maintainer
  I want the word-budget rule documented, checker-aware, and preflight-tracked
  So that the gate is discoverable, AI-checkable, and deterministically enforced

  # Exemption(e2e): repository documentation presence has no published Rhino command boundary; alternative-proof: rhino-cli:test:integration / The rule is documented as a convention
  @e2e-exempt
  Scenario: The rule is documented as a convention
    Given the plan is complete
    When I look under "repo-governance/conventions/structure/"
    Then "governance-word-budget.md" exists
    And the file lists the monitored file classes, configured threshold source, and enforcement points

  # Exemption(e2e): this contract belongs to the private AI checker instruction surface, not executable CLI output; alternative-proof: rhino-cli:test:integration / rules-checker validates the budget qualitatively
  @e2e-exempt
  Scenario: rules-checker validates the budget qualitatively
    Given the plan is complete
    When "rules-checker" runs Step 6
    Then it reports qualitative bloat concerns across the whole instruction-file class
    And it annotates that the word ceiling is enforced by the deterministic "governance-word-budget" gate

  # Exemption(e2e): workflow delegation is repository governance content with no public Rhino process route; alternative-proof: rhino-cli:test:integration / The quality-gate workflow delegates the validator by exact gate ID
  @e2e-exempt
  Scenario: The quality-gate workflow delegates the validator by exact gate ID
    Given the plan is complete
    When I read "repo-governance/workflows/rules/rules-quality-gate.md"
    Then "governance-word-budget" is skipped locally and delegated from Step 0.5

  Scenario: The preflight envelope carries the governance-word-budget category
    Given a repo with instruction files within the configured budgets
    When the developer runs "rhino-cli repo-governance audit" with JSON output
    Then the envelope schema is "rhino-cli/repo-governance-audit/v1"
    And "result.categories" contains a category named "governance-word-budget"

  # Exemption(e2e): lifecycle-evidence consumption is private AI-checker collaboration state absent from public CLI output; alternative-proof: rhino-cli:test:integration / The AI checker defers to lifecycle-gate evidence
  @e2e-exempt
  Scenario: The AI checker defers to lifecycle-gate evidence
    Given lifecycle evidence contains a current "governance-word-budget" result
    When "rules-checker" runs Step 0.5
    Then it consumes the exact delegated gate ID "governance-word-budget"
    And it does not re-derive word counts in Step 6
