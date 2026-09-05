Feature: ose-be JetStream durable demo

  As an operations engineer
  I want ose-be to publish and durably consume messages via JetStream
  So that at-least-once delivery is verified end-to-end before the service handles real traffic

  # Exemption(integration): JetStream is reached over a network boundary forbidden to Integration; alternative-proof: ose-be-e2e:test:e2e / ose-be publishes and durably consumes its demo subject with ack
  @integration-exempt
  Scenario: ose-be publishes and durably consumes its demo subject with ack
    Given NATS JetStream is running and ose-be is stopped
    When ose-be publishes a demo message to that subject
    Then the durable consumer receives the message
    And the message is acknowledged
    And the messaging status surface reports the demo delivered and acked
