@harness-bindings
Feature: harness bindings validate

  As a developer
  I want rhino-cli harness bindings validate to check all 11 supported harnesses
  So that no harness is left unaccounted for in the binding validation gate

  @unit
  Scenario: All 11 harnesses are accounted for at their tier
    Given the harness binding commands and the repo-config.yml harness section
    When the harness coverage is inspected
    Then all 11 supported harnesses are listed (Claude Code, OpenCode, Amazon Q, Codex, Copilot, Cursor, Windsurf, Junie, Antigravity, Pi, Aider)
    And the generated tier (OpenCode, Amazon Q, Cursor) is regenerated and byte-parity-validated
    And the native tier (Copilot, Windsurf, Junie, Antigravity, Pi, Aider) is validated by the no-shadowing rule plus the AGENTS.md word budget
    And the harness set is data in repo-config.yml, identical across both parity repos, not a hard-coded directory list
