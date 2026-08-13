Feature: Readiness recovery
  A user can refresh an unavailable workspace without reloading the page.

  Scenario: Refresh recovers an unavailable workspace
    Given the workspace is unavailable
    When I select Refresh status
    And the readiness endpoint becomes ready
    Then the workspace summary reports that the application is available
