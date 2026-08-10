Feature: Backend SPA fallback routing

  @unit
  Scenario: Unknown client route receives the SPA shell
    Given the service has finished starting
    When I send a GET request to "/future-client-route"
    Then the response status is 200
