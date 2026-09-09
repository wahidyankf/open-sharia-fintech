Feature: Roots BE health endpoint
  As a system operator
  I want the BE to advertise liveness
  So that orchestrators can route traffic only to healthy instances

  # Exemption(integration): HTTP is a network boundary forbidden to Integration and the in-process route is already Unit proof; alternative-proof: roots-be-e2e:test:e2e / Health endpoint returns 200
  @integration-exempt
  Scenario: Health endpoint returns 200
    Given the roots-be service is running
    When I send GET /api/v1/health
    Then the response status is 200
    And the response body has a "status" field equal to "healthy"

  # Exemption(integration): HTTP is a network boundary forbidden to Integration and the in-process route is already Unit proof; alternative-proof: roots-be-e2e:test:e2e / Health endpoint reports the JSON content type
  @integration-exempt
  Scenario: Health endpoint reports the JSON content type
    Given the roots-be service is running
    When I send GET /api/v1/health
    Then the response "Content-Type" header starts with "application/json"

  # Exemption(integration): HTTP is a network boundary forbidden to Integration and the in-process router already proves the fallback; alternative-proof: roots-be-e2e:test:e2e / An unknown route is rejected
  @integration-exempt
  Scenario: An unknown route is rejected
    Given the roots-be service is running
    When I send GET /api/v1/does-not-exist
    Then the response status is 404
