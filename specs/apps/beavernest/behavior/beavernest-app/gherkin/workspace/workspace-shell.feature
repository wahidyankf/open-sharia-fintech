Feature: Foundation workspace shell
  The combined BeaverNest runtime exposes a small, same-origin status workspace.

  Scenario: Web opens the same-origin workspace
    Given the combined BeaverNest runtime is ready
    When I open the Flutter Web root route
    Then the Foundation status shell is visible before readiness resolves
    And the client requests the relative "/api/v1/readiness" route
    And the status reports Application Available, Database Ready and Schema Current
