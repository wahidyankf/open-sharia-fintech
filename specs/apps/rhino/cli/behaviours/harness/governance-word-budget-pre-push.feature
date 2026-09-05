@governance-word-budget-pre-push
Feature: Pre-push enforcement of the word-budget gate

  As a repository maintainer
  I want the pre-push hook to block pushes that put an instruction file over budget
  So that over-budget surfaces never land on the shared branch

  # Exemption(e2e): the subject is the private Git pre-push hook orchestration, not a public Rhino command; alternative-proof: rhino-cli:test:integration / Pushing an over-budget instruction file is blocked
  @e2e-exempt
  Scenario: Pushing an over-budget instruction file is blocked
    Given my push range modifies "AGENTS.md"
    And "AGENTS.md" exceeds its fail ceiling
    When the pre-push hook runs
    Then the word-budget gate runs
    And the push is aborted with a non-zero exit

  # Exemption(e2e): selective push-range routing is private hook state absent from the public Rhino process; alternative-proof: rhino-cli:test:integration / Pushing changes that do not touch instruction files skips the gate
  @e2e-exempt
  Scenario: Pushing changes that do not touch instruction files skips the gate
    Given my push range modifies only "apps/ose-www/src/page.tsx"
    When the pre-push hook runs
    Then the word-budget validation target is not invoked

  # Exemption(e2e): push continuation is owned by the private Git hook boundary rather than the published CLI; alternative-proof: rhino-cli:test:integration / Pushing an in-budget instruction-file edit passes
  @e2e-exempt
  Scenario: Pushing an in-budget instruction-file edit passes
    Given my push range modifies "AGENTS.md"
    And "AGENTS.md" is within its fail ceiling
    When the pre-push hook runs
    Then the word-budget validation target runs and exits 0
    And the push proceeds

  # Exemption(e2e): impacted-file routing for RTK.md is observable only inside the private pre-push hook; alternative-proof: rhino-cli:test:integration / Pushing an RTK-only change invokes its configured gate
  @e2e-exempt
  Scenario: Pushing an RTK-only change invokes its configured gate
    Given my push range modifies "RTK.md"
    When the pre-push hook runs
    Then the word-budget gate runs
