Feature: Health Check
  As an operations engineer
  I want to monitor the health of the ose-web backend
  So that I can detect service outages quickly

  Background:
    Given the API is running

  # Exemption(integration): the status contract has no local resource boundary and is observable only through the public HTTP response; alternative-proof: ose-www-be-e2e:test:e2e / Health endpoint returns ok status
  @integration-exempt
  Scenario: Health endpoint returns ok status
    When the health endpoint is called
    Then the response contains status "ok"
