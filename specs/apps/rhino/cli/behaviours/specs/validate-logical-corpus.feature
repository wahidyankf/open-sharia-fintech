@specs-validate-logical-corpus
Feature: specs structure validate for a logical owner corpus

  As a developer
  I want rhino-cli specs structure validate to measure a product against the logical owner-corpus shape
  So that a product moving to one README, one as-built architecture.md, and a recursive behaviours/ tree is proved rather than assumed

  Scenario: a product whose single owner corpus is complete passes validation
    Given a logical owner corpus for "testapp" at "cli" with its README, architecture, and a behaviours feature
    When the developer runs "rhino-cli specs structure validate testapp"
    Then the command exits successfully
    And the output contains "0 finding"

  Scenario: an owner corpus missing its README reports a finding
    Given a logical owner corpus for "testapp" at "cli" whose README.md is absent
    When the developer runs "rhino-cli specs structure validate testapp"
    Then the command exits with a failure code
    And the output contains "missing required entry: README.md"

  Scenario: an owner corpus with no behaviours directory reports a finding
    Given a logical owner corpus for "testapp" at "cli" whose behaviours directory is absent
    When the developer runs "rhino-cli specs structure validate testapp"
    Then the command exits with a failure code
    And the output contains "missing required entry: behaviours"

  Scenario: an owner corpus whose behaviours tree holds no feature file reports a finding
    Given a logical owner corpus for "testapp" at "cli" whose behaviours directory holds no feature file
    When the developer runs "rhino-cli specs structure validate testapp"
    Then the command exits with a failure code
    And the output contains "no feature files"

  Scenario: an owner corpus whose behaviours tree has no index reports a finding
    Given a logical owner corpus for "testapp" at "cli" whose behaviours directory has no README.md
    When the developer runs "rhino-cli specs structure validate testapp"
    Then the command exits with a failure code
    And the output contains "missing required entry: behaviours/README.md"

  Scenario: legacy five-folder scaffolding surviving beside a corpus reports a finding
    Given a logical owner corpus for "testapp" at "cli" beside a surviving "product" folder
    When the developer runs "rhino-cli specs structure validate testapp"
    Then the command exits with a failure code
    And the output contains "legacy folder product survives beside a logical owner corpus"
