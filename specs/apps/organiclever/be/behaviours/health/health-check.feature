Feature: Service Health Check

  As an operations engineer
  I want to monitor the health of the OrganicLever backend
  So that I can detect service outages quickly

  Background:
    Given the API is running

  # Exemption(integration): HTTP is a network boundary forbidden to Integration and the in-process route is already Unit proof; alternative-proof: organiclever-be-e2e:test:e2e / Health endpoint reports the service as UP
  @integration-exempt
  Scenario: Health endpoint reports the service as UP
    When an operations engineer sends GET /health
    Then the response status code should be 200
    And the health status should be "ok"

  # Exemption(integration): HTTP is a network boundary forbidden to Integration and the in-process route is already Unit proof; alternative-proof: organiclever-be-e2e:test:e2e / Anonymous health check does not expose component details
  @integration-exempt
  Scenario: Anonymous health check does not expose component details
    When an unauthenticated engineer sends GET /health
    Then the response status code should be 200
    And the health status should be "ok"
    And the response should not include detailed component health information
