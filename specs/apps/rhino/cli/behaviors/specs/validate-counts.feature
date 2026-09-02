@specs-validate-counts
Feature: specs validate-counts

  As a developer
  I want rhino-cli specs validate-counts to measure a spec folder against the logical owner-corpus rules
  So that an empty or half-built corpus is detected and reported

  Scenario: product directory whose owners are corpora passes validation
    Given a spec tree for "testapp" whose one owner corpus is complete
    When the developer runs "rhino-cli specs validate-counts specs/apps/testapp"
    Then the command exits successfully
    And the output contains "0 finding"

  Scenario: folder that is neither a corpus nor a product holding one reports a finding
    Given a spec tree for "testapp" holding only the retired five folders
    When the developer runs "rhino-cli specs validate-counts specs/apps/testapp"
    Then the command exits with a failure code
    And the output contains "is neither a logical owner corpus nor a product holding one"

  Scenario: folder path that does not exist reports an error
    Given no directory exists at "specs/apps/nosuchapp"
    When the developer runs "rhino-cli specs validate-counts specs/apps/nosuchapp"
    Then the command exits with a failure code
    And the output contains "does not exist"

  Scenario: a library corpus at the folder root is measured by the corpus rules
    Given a library corpus at "specs/libs/testlib" carrying architecture.md and a non-empty behaviors/
    When the developer runs "rhino-cli specs validate-counts specs/libs/testlib"
    Then the command exits successfully
    And the output contains "0 finding"

  Scenario: a library corpus missing its behaviors index reports a finding
    Given a library corpus at "specs/libs/testlib" whose behaviors/ folder has no README.md
    When the developer runs "rhino-cli specs validate-counts specs/libs/testlib"
    Then the command exits with a failure code
    And the output contains "missing required entry: behaviors/README.md"
