Feature: organiclever-be NATS connection

  As an operations engineer
  I want organiclever-be to connect to NATS on startup
  So that messaging infrastructure is available before the API accepts requests

  # Exemption(integration): NATS is reached over a network boundary forbidden to Integration; alternative-proof: organiclever-be-e2e:test:e2e / organiclever-be connects to its NATS server at startup
  @integration-exempt
  Scenario: organiclever-be connects to its NATS server at startup
    Given ORGANICLEVER_BE_NATS_URL points to a running NATS server with JetStream enabled
    When organiclever-be starts up
    Then the NATS connection is established
    And the backend reports healthy after connecting
