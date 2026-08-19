@codex-binding
Feature: Codex agent definitions are generated from .claude/agents/

  Scenario: A Claude agent under a role subfolder gets a flat Codex TOML counterpart
    Given a repository whose .claude/agents/ directory holds one agent under a role subfolder
    When the developer runs harness bindings generate
    Then the command exits successfully
    And .codex/agents/ holds exactly one TOML file named for that agent
    And the emitted Codex agent declares name, description, and developer_instructions
    And the emitted Codex agent declares no model field

  Scenario: Agent identity comes from the name frontmatter, not the source subfolder
    Given a repository whose .claude/agents/ holds two agents in different role subfolders whose name frontmatter differs from their filename
    When the developer runs harness bindings generate
    Then the command exits successfully
    And .codex/agents/ holds one flat TOML file per agent keyed on the name frontmatter
    And no emitted filename repeats a role subfolder name

  Scenario: Regenerating rewrites only the delimited region of .codex/config.toml
    Given a repository whose .codex/config.toml carries hand-maintained mcp_servers, features, and ci-monitor-subagent tables
    When the developer runs harness bindings generate twice
    Then the command exits successfully
    And .codex/config.toml declares a generated agents table for the fixture agent
    And the hand-maintained mcp_servers, features, and ci-monitor-subagent tables are unchanged
    And the second run left .codex/config.toml byte-identical to the first
