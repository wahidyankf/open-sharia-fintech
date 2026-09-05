Feature: Database migrations on boot

  As a platform operator
  I want the backend to automatically apply pending schema migrations on startup
  So that the database schema is always in sync without manual intervention

  # Exemption(integration): the PostgreSQL adapter uses a network protocol forbidden to Integration; alternative-proof: organiclever-be-e2e:test:e2e / Backend applies pending migrations on startup
  @integration-exempt
  Scenario: Backend applies pending migrations on startup
    Given a fresh test database has pending organiclever-be migrations
    When organiclever-be starts against that database
    Then organiclever-be reaches its public health endpoint after applying migrations
