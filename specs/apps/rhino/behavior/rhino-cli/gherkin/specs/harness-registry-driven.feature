@harness-registry-driven
Feature: harness commands are registry-driven

  As a developer
  I want harness duplication validate to derive its target set from repo-config.yml
  So that adding a new harness requires only a config change, not a code change

  @unit
  Scenario: The duplication validator is registry-driven, not hard-coded
    Given the repo-config.yml harness section lists an agent-bearing tier (Amazon Q) and a native instruction surface
    When harness duplication validate runs
    Then it derives its target set from the registry, not a hard-coded .claude/.opencode pair
    And a config-only addition of a new agent-bearing tier is covered with no source edit

  @unit
  Scenario: The bindings generator derives its accepted harness names from the registry
    Given a repo-config.yml whose harness registry names a harness the source code never mentions
    When harness bindings generate is asked for that registry-declared name
    Then the name is not rejected as unknown
    And asking for a name the registry omits is rejected, listing the registry-derived set
