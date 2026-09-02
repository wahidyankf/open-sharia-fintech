Feature: Database migrations on boot

  As a platform operator
  I want the backend to automatically apply pending schema migrations on startup
  So that the database schema is always in sync without manual intervention

  @integration
  Scenario: Backend applies pending migrations on startup
    Given the database has no applied migrations
    When the backend runs its migration routine
    Then the migrations table records at least one applied migration
