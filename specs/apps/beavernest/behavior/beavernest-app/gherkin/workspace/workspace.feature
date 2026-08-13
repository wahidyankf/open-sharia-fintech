Feature: BeaverNest workspace readiness
  The workspace presents a clear, responsive availability summary.

  Scenario: A ready workspace presents every safe component state
    Given the BeaverNest readiness endpoint reports a ready workspace
    When I open the Flutter Web root route
    Then I can read the workspace availability, database and schema state
    And the summary remains usable on mobile, tablet and desktop widths
    And on desktop I can use the persistent status and diagnostics rail
