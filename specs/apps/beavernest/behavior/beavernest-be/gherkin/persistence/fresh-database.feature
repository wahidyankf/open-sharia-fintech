Feature: Fresh durable database
  Scenario: Fresh database is migrated before serving
    Given the configured durable database directory is writable and contains no database
    When the BeaverNest application starts
    Then DbUp creates its migration journal before the HTTP endpoint begins listening
    And no product or domain table is created
