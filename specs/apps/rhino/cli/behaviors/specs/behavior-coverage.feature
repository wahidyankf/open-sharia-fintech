@specs-behavior-coverage
Feature: specs behavior-coverage validate

  As a developer
  I want rhino-cli specs behavior-coverage validate to enforce per-level @covers markers
  So that every Gherkin scenario is explicitly covered at the declared test levels

  @unit
  Scenario: An untagged scenario fails the gate
    Given a scenario with no @unit, @integration, or @e2e level tag
    When rhino-cli specs behavior-coverage validate runs
    Then it fails and names the untagged scenario

  @unit
  Scenario: A scenario requiring a level outside the project envelope fails
    Given a project whose coverage registry declares only the unit level
    And a scenario in that project tagged @integration
    When rhino-cli specs behavior-coverage validate runs
    Then it fails because the scenario requires a level not in the project envelope

  @unit
  Scenario: A scenario not covered at a required level fails
    Given a scenario tagged @unit and @e2e
    And a test marks it @covers at the unit level only
    When rhino-cli specs behavior-coverage validate runs
    Then it fails and names the missing e2e coverage

  @unit
  Scenario: An @covers at an undeclared level fails
    Given a scenario tagged @unit only
    And a test marks it @covers at the e2e level
    When rhino-cli specs behavior-coverage validate runs
    Then it fails because the e2e level is not declared for that scenario

  @unit
  Scenario: An orphan @covers marker fails the gate
    Given a test with an @covers marker referencing a scenario title that no feature file contains
    When rhino-cli specs behavior-coverage validate runs
    Then it fails and names the orphan marker

  @unit
  Scenario: A @wip scenario is exempt from coverage
    Given a scenario tagged @wip with no @covers markers
    When rhino-cli specs behavior-coverage validate runs
    Then it does not fail and reports the scenario in the exempt count
