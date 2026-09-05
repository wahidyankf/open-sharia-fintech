Feature: Service Health and Metadata
  As an operations engineer
  I want to monitor the health of the ayokoding-www backend and discover available locales
  So that I can detect service outages and configure locale-aware clients

  Background:
    Given the API is running

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / meta.health returns status ok
  @integration-exempt
  Scenario: meta.health returns status ok
    When the client calls meta.health
    Then the response should contain "status" equal to "ok"

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / meta.languages returns the list of available locales
  @integration-exempt
  Scenario: meta.languages returns the list of available locales
    When the client calls meta.languages
    Then the response should contain a non-null "languages" array
    And the "languages" array should include "en"
    And the "languages" array should include "id"
