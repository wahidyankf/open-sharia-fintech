@specs-validate-adoption
Feature: specs structure validate adoption rules

  As a developer
  I want rhino-cli specs structure validate to verify an app has adopted the logical owner corpus
  So that FR-10 adoption gaps are surfaced before they accumulate

  Scenario: app with an owner corpus and no retired ddd tree passes validation
    Given an app "testapp" with an owner corpus and no ddd tree at specs/apps/testapp/ddd
    When the developer runs "rhino-cli specs structure validate testapp"
    Then the command exits successfully
    And the output contains "0 finding"

  Scenario: app with no owner corpus reports a finding
    Given an app "testapp" holding only the retired five folders
    When the developer runs "rhino-cli specs structure validate testapp"
    Then the command exits with a failure code
    And the output contains "no logical owner corpus"

  Scenario: app with a surviving retired ddd tree reports a finding
    Given an app "testapp" with an owner corpus and a retired ddd tree at specs/apps/testapp/ddd
    When the developer runs "rhino-cli specs structure validate testapp"
    Then the command exits with a failure code
    And the output contains "retired ddd/ tree"

  Scenario: unknown app with no spec tree at all reports an adoption finding
    Given an app "unknownapp" with no spec tree at all
    When the developer runs "rhino-cli specs structure validate unknownapp"
    Then the command exits with a failure code
    And the output contains "no logical owner corpus"
