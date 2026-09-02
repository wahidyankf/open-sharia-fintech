Feature: organiclever-be NATS connection

  As an operations engineer
  I want organiclever-be to connect to NATS on startup
  So that messaging infrastructure is available before the API accepts requests

  @e2e
  Scenario: organiclever-be connects to its NATS server at startup
    Given ORGANICLEVER_BE_NATS_URL points to a running NATS server with JetStream enabled
    When organiclever-be starts up
    Then the NATS connection is established
    And the backend reports healthy after connecting
