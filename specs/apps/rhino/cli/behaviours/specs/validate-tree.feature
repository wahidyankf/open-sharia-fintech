@specs-validate-tree
Feature: specs structure validate tree rules

  As a developer
  I want rhino-cli specs structure validate to verify a product's spec tree is a logical owner corpus
  So that a product that has not adopted the shape is reported rather than assumed to be fine

  Scenario: product whose owner corpus is complete passes validation
    Given a spec tree for "testapp" whose one owner corpus is complete
    When the developer runs "rhino-cli specs structure validate testapp"
    Then the command exits successfully
    And the output contains "0 finding"

  Scenario: product with no owner corpus at all reports a finding
    Given no spec tree exists for "unknownapp"
    When the developer runs "rhino-cli specs structure validate unknownapp"
    Then the command exits with a failure code
    And the output contains "no logical owner corpus"

  Scenario: product directory holding only retired folders reports a finding
    Given a spec tree for "testapp" holding only the retired five folders
    When the developer runs "rhino-cli specs structure validate testapp"
    Then the command exits with a failure code
    And the output contains "no logical owner corpus"
