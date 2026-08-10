Feature: Broken migration
  Scenario: Broken migration prevents partial startup
    Given the migration set contains an intentionally invalid SQL script in an isolated test fixture
    When the BeaverNest application starts against a disposable database
    Then startup exits non-zero before publishing the HTTP endpoint
    And the migration failure is logged without exposing sensitive configuration
