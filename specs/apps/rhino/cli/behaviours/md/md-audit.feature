@md-audit
Feature: `md audit` aggregates every markdown validator into one pass/fail report

  As a maintainer running the full markdown-quality gate in one command
  I want `md audit` to run every md validator in sequence and report a single result
  So that a clean documentation tree is confirmed compliant without invoking each
  validator by hand

  Scenario: Every md validator passes on a repository with no markdown files
    Given a repository containing no markdown files
    When the developer runs "rhino-cli md audit"
    Then the command exits successfully
    And the output reports all md validators passed
