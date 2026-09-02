@specs-validate-logical-corpus
Feature: specs validate-tree for a logical owner corpus

  As a developer
  I want rhino-cli specs validate-tree to measure a migrated product against the logical owner-corpus shape
  So that a product moving to one README, one as-built architecture.md, and a recursive behaviors/ tree is proved rather than assumed

  Scenario: a product whose single owner corpus is complete passes validation
    Given a logical owner corpus for "testapp" at "cli" with its README, architecture, and a behaviors feature
    When the developer runs "rhino-cli specs validate-tree testapp"
    Then the command exits successfully
    And the output contains "0 finding"

  Scenario: an owner corpus missing its README reports a finding
    Given a logical owner corpus for "testapp" at "cli" whose README.md is absent
    When the developer runs "rhino-cli specs validate-tree testapp"
    Then the command exits with a failure code
    And the output contains "missing required entry: README.md"

  Scenario: an owner corpus with no behaviors directory reports a finding
    Given a logical owner corpus for "testapp" at "cli" whose behaviors directory is absent
    When the developer runs "rhino-cli specs validate-tree testapp"
    Then the command exits with a failure code
    And the output contains "missing required entry: behaviors"

  Scenario: an owner corpus whose behaviors tree holds no feature file reports a finding
    Given a logical owner corpus for "testapp" at "cli" whose behaviors directory holds no feature file
    When the developer runs "rhino-cli specs validate-tree testapp"
    Then the command exits with a failure code
    And the output contains "no feature files"

  Scenario: an owner corpus whose behaviors tree has no index reports a finding
    Given a logical owner corpus for "testapp" at "cli" whose behaviors directory has no README.md
    When the developer runs "rhino-cli specs validate-tree testapp"
    Then the command exits with a failure code
    And the output contains "missing required entry: behaviors/README.md"

  Scenario: legacy five-folder scaffolding surviving beside a corpus reports a finding
    Given a logical owner corpus for "testapp" at "cli" beside a surviving "product" folder
    When the developer runs "rhino-cli specs validate-tree testapp"
    Then the command exits with a failure code
    And the output contains "legacy folder product survives beside a logical owner corpus"
