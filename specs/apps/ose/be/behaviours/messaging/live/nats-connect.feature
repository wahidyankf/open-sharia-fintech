Feature: ose-be NATS connection

  As an operations engineer
  I want ose-be to connect to NATS on startup
  So that messaging infrastructure is available before the API accepts requests

  # Exemption(integration): NATS is reached over a network boundary forbidden to Integration; alternative-proof: ose-be-e2e:test:e2e / ose-be connects to its NATS server at startup
  @integration-exempt
  Scenario: ose-be connects to its NATS server at startup
    Given OSE_BE_NATS_URL points to a running NATS server with JetStream enabled
    When ose-be starts up
    Then the NATS connection is established
    And the backend reports healthy after connecting
