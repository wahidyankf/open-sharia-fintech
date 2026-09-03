Feature: ose-be JetStream durable demo

  As an operations engineer
  I want ose-be to publish and durably consume messages via JetStream
  So that at-least-once delivery is verified end-to-end before the service handles real traffic

  @e2e
  Scenario: ose-be publishes and durably consumes its demo subject with ack
    Given ose-be has a JetStream durable stream and consumer for its demo subject
    When ose-be publishes a demo message to that subject
    Then the durable consumer receives the message
    And the message is acknowledged
    And the messaging status surface reports the demo delivered and acked
