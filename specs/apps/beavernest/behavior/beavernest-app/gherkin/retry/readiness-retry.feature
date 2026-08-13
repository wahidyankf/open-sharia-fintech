Feature: Readiness recovery
  A user can refresh an unavailable workspace without reloading the page.

  Scenario: Refresh recovers an unavailable workspace
    Given the workspace is unavailable
    When I select Refresh status
    And the readiness endpoint becomes ready
    Then the workspace summary reports that the application is available

  Scenario: Refresh recovers a failed status request
    Given the workspace status request fails
    When I select Refresh status after a request failure
    Then the workspace status retry reports that the application is available
