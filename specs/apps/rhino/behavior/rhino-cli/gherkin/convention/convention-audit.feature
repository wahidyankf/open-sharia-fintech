@convention-audit
Feature: `convention audit` aggregates every convention validator into one pass/fail report

  As a maintainer running the full repository-convention gate in one command
  I want `convention audit` to run every convention validator in sequence and
  report a single result
  So that a single failing member is caught even when the other members pass

  Scenario: A missing LICENSE fails the aggregate convention audit
    Given a repository where one app directory is missing its LICENSE file
    When the developer runs "rhino-cli convention audit"
    Then the command exits with a failure code
    And the output names the failing "license" validator
