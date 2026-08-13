Feature: Unavailable workspace diagnostics
  Scenario: Unavailable workspace withholds diagnostic causes
    Given diagnostics observes unavailable readiness
    When I send a GET request to "/api/v1/diagnostics"
    Then the response status is 503
    And the JSON response reports status "unavailable" with only unavailable readiness components
    And the diagnostics response reveals no cause, version, uptime or server time
    And the response sends "Cache-Control: no-store" without a cache validator
