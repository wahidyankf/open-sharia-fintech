Feature: Browser workspace readiness

  Scenario: Browser renders the workspace and obtains readiness
    Given BeaverNest is reachable through its configured VPN address
    When I navigate to "/" in a new browser session
    Then the application shell renders before the readiness request completes
    And the browser sends a same-origin GET request to "/api/v1/readiness"
    And the page reports Application Available, Database Ready and Schema Current
