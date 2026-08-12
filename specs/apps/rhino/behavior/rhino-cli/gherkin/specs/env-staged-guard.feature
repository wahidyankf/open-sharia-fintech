@env-staged-guard
Feature: env staged-guard validate

  As a developer
  I want rhino-cli env staged-guard validate to block commits of real .env files
  So that secrets are never accidentally committed to the repository

  @unit
  Scenario: Committing a real .env file is rejected
    Given a real .env file is staged for commit
    When the pre-commit hook runs rhino-cli env staged-guard validate
    Then it exits non-zero and names the offending file
    And the commit is aborted

  @unit
  Scenario: Staging .env.example is allowed
    Given only .env.example is staged for commit
    When the pre-commit hook runs rhino-cli env staged-guard validate
    Then it exits zero and does not block the commit

  @unit
  Scenario Outline: Staging any real env file is rejected at commit time
    Given a git index with "<file>" staged
    When "rhino-cli env staged-guard validate" runs
    Then the command exits non-zero
    And the output names "<file>" as offending

    Examples:
      | file              |
      | .env              |
      | .env.local        |
      | .env.test         |
      | .env.prod         |
      | .env.stag         |
      | apps/x/.env.local |
