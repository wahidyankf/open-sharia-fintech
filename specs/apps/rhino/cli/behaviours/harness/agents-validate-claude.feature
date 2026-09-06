@agents-validate-claude
Feature: Claude Code Agent and Skill Configuration Validation

  As a repository maintainer
  I want to verify that all Claude Code agents and skills are correctly configured
  So that agents behave as expected when invoked

  Scenario: A directory with all agents and skills correctly configured passes validation
    Given a .claude/ directory where all agents and skills are valid
    When the developer runs agents validate-claude
    Then the command exits successfully
    And the output reports all checks as passing

  Scenario: An agent file missing a required frontmatter field fails validation
    Given a .claude/ directory where one agent is missing the required "description" field
    When the developer runs agents validate-claude
    Then the command exits with a failure code
    And the output identifies the agent and the missing field

  Scenario: An agent declaring the ultra-tier fable model alias passes validation
    Given a .claude/ directory where one agent declares the "fable" model alias
    When the developer runs agents validate-claude
    Then the command exits successfully

  Scenario: An agent declaring a model outside the tier vocabulary fails validation
    Given a .claude/ directory where one agent declares the "gpt-4" model alias
    When the developer runs agents validate-claude
    Then the command exits with a failure code
    And the output reports the rejected model value

  Scenario: An agent nested in a role subfolder is validated
    Given a .claude/ directory where the only agent sits in a role subfolder
    When the developer runs agents validate-claude
    Then the command exits with a failure code
    And the output identifies the nested agent

  Scenario: An agent declaring no model fails validation
    Given a .claude/ directory where one agent declares no model field
    When the developer runs agents validate-claude
    Then the command exits with a failure code
    And the output reports the rejected model value

  Scenario: Two agents with the same name fail validation
    Given a .claude/ directory containing two agent files declaring the same name
    When the developer runs agents validate-claude
    Then the command exits with a failure code
    And the output reports the duplicate agent name

  Scenario: --agents-only validates agents without checking skills
    Given a .claude/ directory where agents are valid but skills have issues
    When the developer runs agents validate-claude with the --agents-only flag
    Then the command exits successfully

  Scenario: --skills-only validates skills without checking agents
    Given a .claude/ directory where skills are valid but agents have issues
    When the developer runs agents validate-claude with the --skills-only flag
    Then the command exits successfully

  Scenario: An agent whose effort contradicts its grade fails validation
    Given a .claude/ directory where one agent declares an effort its grade does not
    When the developer runs agents validate-claude
    Then the command exits with a failure code
    And the output reports the effort the grade declares

  Scenario: A registry declaring no grade vocabulary fails closed
    Given a .claude/ directory whose repo-config.yml declares no model-map for claude-code
    When the developer runs agents validate-claude
    Then the command exits with a failure code
    And the output reports that no grade vocabulary is declared

  Scenario: An agent stating no model selection justification fails validation
    Given a .claude/ directory where one agent's body states no model selection justification
    When the developer runs agents validate-claude
    Then the command exits with a failure code
    And the output reports the missing justification block
