@repo-governance-test-boundary
Feature: Integration Test Network Boundary Audit

  As a repository maintainer
  I want every project's Integration tests to reach no network unless the repository allowlists it
  So that a loopback dependency can never enter a project silently

  Scenario: No project uses a network API in Integration tests passes
    Given a repository where no integration test source references a network API
    When the developer runs repo-governance test-boundary validate
    Then the command exits successfully
    And the test-boundary output reports zero findings

  Scenario: An unallowlisted project using a network API fails
    Given a repository where an integration test opens an HTTP client and the project is not allowlisted
    When the developer runs repo-governance test-boundary validate
    Then the command exits with a failure code
    And the test-boundary output names the offending project and source file

  Scenario: An allowlisted project using a network API passes
    Given a repository where an integration test opens an HTTP client and the project is allowlisted with a reason
    When the developer runs repo-governance test-boundary validate
    Then the command exits successfully
    And the test-boundary output reports zero findings

  Scenario: An allowlist entry whose project uses no network API warns
    Given a repository where a project is allowlisted but no integration test references a network API
    When the developer runs repo-governance test-boundary validate
    Then the command exits successfully
    And the test-boundary output reports the allowlist entry as stale

  Scenario: An allowlist entry naming a project without Integration tests fails
    Given a repository where an allowlist entry names a project that declares no test:integration target
    When the developer runs repo-governance test-boundary validate
    Then the command exits with a failure code
    And the test-boundary output identifies the unknown allowlisted project

  Scenario: An allowlist entry with no reason fails
    Given a repository where an allowlist entry omits its reason
    When the developer runs repo-governance test-boundary validate
    Then the command exits with a failure code
    And the test-boundary output identifies the allowlist entry with no reason

  Scenario: A module specifier inside a fixture string is not a network API use
    Given a repository where an integration test embeds a package name inside a JSON fixture string
    When the developer runs repo-governance test-boundary validate
    Then the command exits successfully
    And the test-boundary output reports zero findings
