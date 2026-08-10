Feature: Development data isolation
  Scenario: Development uses a separate SQLite directory
    Given the local development command receives an explicit developer-owned data directory
    When it starts the backend on the local development port
    Then the database resolves only within that development directory
    And the command neither reads nor inherits the production host data-bind source
