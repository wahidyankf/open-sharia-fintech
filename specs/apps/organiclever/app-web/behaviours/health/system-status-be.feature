Feature: BE Status Page

  As an app user
  I want the app to show the backend connectivity status
  So that I can diagnose whether the backend service is reachable

  Scenario: BE status page shows Not Configured when env unset
    Given ORGANICLEVER_BE_URL is unset
    When a visitor requests GET /system/status/be
    Then the response status is 200
    And the body contains "Not configured"

  Scenario: Backend health-check page is excluded from search indexes
    When a crawler requests GET /system/status/be
    Then the response declares the page non-indexable

  @local-fullstack
  # Exemption(e2e): the shared browser server has one immutable process-level backend URL and cannot select a different server-side upstream per scenario; alternative-proof: organiclever-app-web:test:unit / BE status page shows UP when backend healthy
  @e2e-exempt
  Scenario: BE status page shows UP when backend healthy
    Given ORGANICLEVER_BE_URL is "http://be.example.test"
    And the backend health endpoint returns 200 with body {"status":"UP"}
    When a visitor requests GET /system/status/be
    Then the response status is 200
    And the body contains "UP"
    And the body contains the backend URL

  @local-fullstack
  # Exemption(e2e): Playwright cannot replace the Next.js server process's outbound backend connection with a refused socket for one scenario; alternative-proof: organiclever-app-web:test:unit / BE status page shows DOWN when backend unreachable
  @e2e-exempt
  Scenario: BE status page shows DOWN when backend unreachable
    Given ORGANICLEVER_BE_URL is "http://be.example.test"
    And the backend health endpoint fails with connection refused
    When a visitor requests GET /system/status/be
    Then the response status is 200
    And the body contains "DOWN"
    And the body contains the failure reason
    And no uncaught exception reaches the Next.js error boundary

  @local-fullstack
  # Exemption(e2e): Playwright cannot hold the Next.js server process's outbound backend request open for one scenario without replacing its process-level upstream; alternative-proof: organiclever-app-web:test:unit / BE status page shows DOWN when backend times out
  @e2e-exempt
  Scenario: BE status page shows DOWN when backend times out
    Given ORGANICLEVER_BE_URL is "http://be.example.test"
    And the backend health endpoint does not respond within 3 seconds
    When a visitor requests GET /system/status/be
    Then the response status is 200
    And the body contains "DOWN"
    And the body contains "timeout"
