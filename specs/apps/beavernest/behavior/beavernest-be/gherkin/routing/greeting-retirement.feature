Feature: Retired backend routes

  @unit
  Scenario: Greeting route is no longer part of the API
    Given the service has finished starting
    When I send a GET request to "/api/v1/hello"
    Then the response status is 404
