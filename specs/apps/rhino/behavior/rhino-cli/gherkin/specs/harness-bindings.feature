@harness-bindings
Feature: harness bindings validate

  As a developer
  I want rhino-cli harness bindings validate to check all 3 supported harnesses
  So that no harness is left unaccounted for in the binding validation gate

  @unit
  Scenario: All 3 harnesses are accounted for at their tier
    Given the harness binding commands and the repo-config.yml harness section
    When the harness coverage is inspected
    Then all 3 supported harnesses are listed (Claude Code, OpenCode, Codex)
    And the source tier (Claude Code) is the single hand-authored origin every mirror derives from
    And the generated tier (OpenCode, Codex) is regenerated and byte-parity-validated
    And the harness set is data in repo-config.yml, identical across both parity repos, not a hard-coded directory list

  @unit
  Scenario: No retired tier survives the contraction
    Given the harness binding commands and the repo-config.yml harness section
    When the harness coverage is inspected
    Then no entry declares the retired source-config or native tier
