Feature: Workspace readiness loading

  Scenario: Workspace shows readiness loading state
    Given the readiness response is intentionally delayed
    When I navigate to "/"
    Then the readiness region reports that status is being checked
    And the region does not falsely report the database as ready
