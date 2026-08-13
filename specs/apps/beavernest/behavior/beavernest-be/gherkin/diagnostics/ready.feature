Feature: Ready workspace diagnostics
  Scenario: Ready workspace returns a safe live snapshot
    Given startup migrations completed and SQLite accepts queries
    And the diagnostics clock, version and uptime are deterministic
    When I send a GET request to "/api/v1/diagnostics"
    Then the response status is 200
    And the JSON response reports status "ready", safe version, whole-second uptime and UTC server time
    And the response reports the named database and schema readiness components
    And the response sends "Cache-Control: no-store" without a cache validator
