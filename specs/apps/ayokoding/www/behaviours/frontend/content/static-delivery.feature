Feature: Statically delivered content pages

  As a reader visiting AyoKoding
  I want content pages to remain cacheable with the correct document language
  So that courses load quickly in my selected locale

  Background:
    Given the app is running

  # Exemption(e2e): a browser or HTTP response cannot expose the internal build manifest that records prerendered routes; alternative-proof: ayokoding-www:test:integration / A content page is prerendered at build time
  @e2e-exempt
  Scenario: A content page is prerendered at build time
    Given the ayokoding-www site is built and deployed
    When the build output manifest is inspected
    Then the prerendered route count is at least two thousand
    And the inspected content route is present in the static route manifest

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A repeat request to a content page remains cacheable
  @integration-exempt
  Scenario: A repeat request to a content page remains cacheable
    Given a visitor has already requested a course lesson URL
    When the same URL is requested again
    Then the response does not carry a no-store cache directive

  Scenario: Runtime tRPC endpoints retain their filesystem assets
    Given the ayokoding-www standalone package is running
    When navigation search and course-path data are requested through tRPC
    Then every runtime data endpoint responds successfully

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The document language reflects the localized page locale
  @integration-exempt
  Scenario Outline: The document language reflects the localized page locale
    Given a visitor opens a localized page in the "<locale>" locale
    When the localized page renders
    Then the html element declares the "<language_code>" language code

    Examples:
      | locale | language_code |
      | en     | en            |
      | id     | id            |
