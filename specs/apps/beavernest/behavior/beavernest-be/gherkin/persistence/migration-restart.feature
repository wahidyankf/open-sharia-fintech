Feature: Restart migrations
  Scenario: Restart does not reapply completed migrations
    Given the database contains a completed DbUp migration journal
    When the BeaverNest application restarts against the same mounted directory
    Then every completed migration remains recorded exactly once
    And readiness reports schema "current"
