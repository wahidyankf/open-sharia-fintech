@vendored-skill-preservation
Feature: The emitter owns only what it generates

  @unit
  Scenario: Vendored subdirectories are declared, not inferred
    Given .agents/skills/ holds 24 tracked files across 8 vendored plugin directories with no .claude/skills/ source and no way to regenerate them
    When the harness registry declares those 8 directories as vendored
    Then rhino-cli repo-config validate exits 0
    And an undeclared directory appearing under .agents/skills/ with no .claude/skills/ counterpart makes rhino-cli harness bindings validate exit non-zero, where an ownership heuristic would have silently deleted it instead

  @unit
  Scenario: Stale-mirror cleanup never reaches a vendored directory
    Given a skill directory is renamed under .claude/skills/ so its old mirror becomes stale
    When rhino-cli harness bindings generate runs
    Then the stale mirrored directory is removed and the new one created
    And all 8 vendored directories are still present, proving cleanup is scoped to emitter-owned paths
