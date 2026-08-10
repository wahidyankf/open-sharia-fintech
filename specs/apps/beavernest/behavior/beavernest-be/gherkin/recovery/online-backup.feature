Feature: Online backup
  Scenario: Online backup produces a valid database
    Given BeaverNest is ready with WAL enabled
    When I run the manual backup command while the application remains online
    Then the backup completes through the SQLite backup API
    And integrity_check returns "ok" for the backup
    And foreign_key_check returns no rows for the backup
