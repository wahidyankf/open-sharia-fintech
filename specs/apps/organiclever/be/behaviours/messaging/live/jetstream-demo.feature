Feature: organiclever-be JetStream durable demo

  As an operations engineer
  I want organiclever-be to publish and durably consume messages via JetStream
  So that at-least-once delivery is verified end-to-end before the service handles real traffic

  # Exemption(integration): JetStream is reached over a network boundary forbidden to Integration; alternative-proof: organiclever-be-e2e:test:e2e / organiclever-be publishes and durably consumes its demo subject with ack
  @integration-exempt
  Scenario: organiclever-be publishes and durably consumes its demo subject with ack
    Given NATS JetStream is running and organiclever-be is stopped
    When organiclever-be publishes a demo message to that subject
    Then the durable consumer receives the message
    And the message is acknowledged
    And the messaging status surface reports the demo delivered and acked
