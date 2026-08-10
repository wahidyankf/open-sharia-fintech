Feature: Workspace readiness
  Scenario: Ready workspace reports database and schema state
    Given startup migrations completed and SQLite accepts queries
    When I send a GET request to "/api/v1/readiness"
    Then the response status is 200
    And the JSON response reports status "ready", database "ready" and schema "current"
    And the response sends "Cache-Control: no-store" without a cache validator
