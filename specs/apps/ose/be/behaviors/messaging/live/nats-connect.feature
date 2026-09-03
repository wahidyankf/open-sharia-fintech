Feature: ose-be NATS connection

  As an operations engineer
  I want ose-be to connect to NATS on startup
  So that messaging infrastructure is available before the API accepts requests

  @e2e
  Scenario: ose-be connects to its NATS server at startup
    Given OSE_BE_NATS_URL points to a running NATS server with JetStream enabled
    When ose-be starts up
    Then the NATS connection is established
    And the backend reports healthy after connecting
