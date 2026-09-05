Feature: BE health endpoint
  As a system operator
  I want the BE to advertise liveness
  So that orchestrators can route traffic only to healthy instances

  # Exemption(integration): HTTP is a network boundary forbidden to Integration and the in-process route is already Unit proof; alternative-proof: ose-be-e2e:test:e2e / Health endpoint returns 200
  @integration-exempt
  Scenario: Health endpoint returns 200
    Given the ose-be service is running
    When I send GET /api/v1/health
    Then the response status is 200
    And the response body has a "status" field equal to "healthy"
