@specs-validate-adoption
Feature: specs validate-adoption

  As a developer
  I want rhino-cli specs validate-adoption to verify an app has adopted BDD practices
  So that FR-10 adoption gaps are surfaced before they accumulate

  Scenario: app with BDD feature files and no retired ddd tree passes validation
    Given an app "testapp" that has at least one feature file under specs/apps/testapp/behavior/ and no ddd tree at specs/apps/testapp/ddd
    When the developer runs "rhino-cli specs validate-adoption testapp"
    Then the command exits successfully
    And the output contains "0 finding"

  Scenario: app missing behavior feature files reports a finding
    Given an app "testapp" that has no feature files under specs/apps/testapp/behavior/
    When the developer runs "rhino-cli specs validate-adoption testapp"
    Then the command exits with a failure code
    And the output contains "no feature files"

  Scenario: app with a surviving retired ddd tree reports a finding
    Given an app "testapp" that has feature files and a retired ddd tree at specs/apps/testapp/ddd
    When the developer runs "rhino-cli specs validate-adoption testapp"
    Then the command exits with a failure code
    And the output contains "retired ddd/ tree"

  Scenario: unknown app with no spec tree at all reports a behavior adoption finding
    Given an app "unknownapp" with no spec tree at all
    When the developer runs "rhino-cli specs validate-adoption unknownapp"
    Then the command exits with a failure code
    And the output contains "no feature files"
