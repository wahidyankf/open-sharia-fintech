Feature: Workspace readiness failure
  Scenario: Unready workspace returns a safe response
    Given SQLite cannot complete the readiness query
    When I send a GET request to "/api/v1/readiness"
    Then the response status is 503
    And the JSON response reports status "not-ready"
    And the response reveals no database path, SQL text or exception detail
    And the response sends "Cache-Control: no-store" without a cache validator
