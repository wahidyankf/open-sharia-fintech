Feature: Backend API routing

  @unit
  Scenario: Unknown API path returns JSON not SPA HTML
    Given the service has finished starting
    When I send a GET request to "/api/v1/does-not-exist"
    Then the response status is 404
    And the response body field "error" is a non-empty string
