@harness-registry-driven
Feature: harness commands are registry-driven

  As a developer
  I want harness naming validate and harness duplication validate to derive their target sets from repo-config.yml
  So that adding a new harness requires only a config change, not a code change

  @unit
  Scenario: Every harness command is registry-driven, not hard-coded
    Given the repo-config.yml harness section lists an agent-bearing tier (Amazon Q) and a native instruction surface
    When harness naming validate and harness duplication validate run
    Then each derives its target set from the registry, not a hard-coded .claude/.opencode pair
    And harness naming validate checks the Amazon Q agent dir and the N-way mirror
    And a config-only addition of a new agent-bearing tier is covered with no source edit
