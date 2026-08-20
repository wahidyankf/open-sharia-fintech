@vendored-skill-preservation
Feature: The emitter owns only what it generates

  Which directories are vendored is repository-local — one sibling repository
  carries a plugin payload under .agents/skills/ and the other carries none — so
  the first scenario derives the vendored set from the registry instead of
  naming it. The second scenario runs entirely inside a temp fixture whose own
  vendored set it controls.

  @unit
  Scenario: Vendored subdirectories are declared, not inferred
    Given every .agents/skills/ directory without a .claude/skills/ source is one the emitter cannot regenerate
    When the harness registry declares each of those directories as vendored
    Then rhino-cli repo-config validate exits 0
    And an undeclared directory appearing under .agents/skills/ with no .claude/skills/ counterpart makes rhino-cli harness bindings validate exit non-zero, where an ownership heuristic would have silently deleted it instead

  @unit
  Scenario: Stale-mirror cleanup never reaches a vendored directory
    Given a skill directory is renamed under .claude/skills/ so its old mirror becomes stale
    When rhino-cli harness bindings generate runs
    Then the stale mirrored directory is removed and the new one created
    And every vendored directory is still present, proving cleanup is scoped to emitter-owned paths

  @unit
  Scenario: A vendored declaration that disagrees with its own ownership record is refused
    Given a harness declares .agents/skills/vendor-plugin as ownership class vendored but its vendored list names a different value for it
    When rhino-cli harness bindings generate runs against that mismatched registry
    Then the run fails loudly instead of deleting the directory the ownership record protects

  @unit
  Scenario: A vendored entry naming no real directory is refused even when no ownership record contradicts it
    Given a harness's vendored list names a typo'd path with no ownership record for the real directory it was meant to protect
    When rhino-cli harness bindings generate runs against that under-declared registry
    Then the run fails loudly instead of deleting the real directory the typo'd entry was meant to protect
