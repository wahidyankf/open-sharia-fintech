Feature: Backend static routing

  @unit
  Scenario: Unknown static asset is not replaced by the SPA shell
    Given the service has finished starting
    When I send a GET request to "/assets/missing.js"
    Then the response status is 404
