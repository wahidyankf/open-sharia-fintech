Feature: Internationalisation and Language Switching

  As a reader visiting AyoKoding
  I want to switch between available languages
  So that I can read content in my preferred language

  Background:
    Given the app is running

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Language switcher displays the current locale
  @integration-exempt
  Scenario: Language switcher displays the current locale
    When a visitor is on a page under the /en locale
    Then the language switcher should display "English" as the current language

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Switching language redirects to the locale-specific URL
  @integration-exempt
  Scenario: Switching language redirects to the locale-specific URL
    Given a visitor is on the English AI benchmark page at /en/tools/ai-benchmark
    When the visitor selects Indonesian from the language switcher
    Then the visitor should be redirected to the Indonesian AI benchmark page at /id/tools/ai-benchmark

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / UI labels change to the selected language
  @integration-exempt
  Scenario: UI labels change to the selected language
    When a visitor is on the Indonesian version of a page
    Then navigation labels and UI text should be displayed in Indonesian
    And the page title and headings should reflect the Indonesian locale content

  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / Root URL redirects to the default locale
  @integration-exempt
  Scenario: Root URL redirects to the default locale
    When a visitor opens the root URL /
    Then they should be redirected to /en
    And the English version of the home page should be displayed
