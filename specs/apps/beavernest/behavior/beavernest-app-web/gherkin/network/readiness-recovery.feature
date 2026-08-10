Feature: Workspace readiness recovery

  Scenario: Workspace recovers from readiness failure
    Given the readiness endpoint returns an unavailable response
    When I navigate to "/" and activate "Refresh status" after service recovery
    Then the readiness request is retried without a full page navigation
    And the region changes from Unavailable to Ready using a polite live announcement
