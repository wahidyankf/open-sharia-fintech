Feature: Backend liveness
  Scenario: Live process reports liveness without database details
    Given the BeaverNest process is accepting HTTP requests
    When I send a GET request to "/api/v1/health"
    Then the response status is 200
    And the JSON response reports status "ok"
    And the response reveals no database path or migration detail
