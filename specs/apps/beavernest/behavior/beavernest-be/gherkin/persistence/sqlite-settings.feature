Feature: SQLite safety settings
  Scenario: Database enables required safety settings
    Given a migrated BeaverNest database is open
    When the SQLite operating settings are inspected
    Then foreign key enforcement is enabled
    And journal mode is WAL
    And a finite busy timeout is configured
