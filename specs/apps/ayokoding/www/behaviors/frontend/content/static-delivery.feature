Feature: Statically delivered content pages

  As a reader visiting AyoKoding
  I want content pages to be delivered from the CDN with the correct document language
  So that courses load quickly in my selected locale

  Background:
    Given the app is running

  @e2e
  Scenario: A content page is prerendered at build time
    Given the ayokoding-www site is built and deployed
    When the build output manifest is inspected
    Then the prerendered route count is at least two thousand
    And the content catch-all route is not marked as dynamically rendered

  @e2e
  Scenario: A repeat request to a content page remains cacheable
    Given a visitor has already requested a course lesson URL
    When the same URL is requested again
    Then the response does not carry a no-store cache directive

  @e2e @deployment
  Scenario: A repeat request to a deployed content page is served from the CDN
    Given a Vercel preview or production deployment is selected for CDN verification
    When the same deployed course lesson URL is requested again
    Then the deployed response is served from the CDN cache

  @unit @e2e
  Scenario: Runtime tRPC endpoints retain their filesystem assets
    Given the ayokoding-www standalone package is running
    When navigation search and course-path data are requested through tRPC
    Then every runtime data endpoint responds successfully

  @e2e
  Scenario Outline: The document language reflects the localized page locale
    Given a visitor opens a localized page in the "<locale>" locale
    When the localized page renders
    Then the html element declares the "<language_code>" language code

    Examples:
      | locale | language_code |
      | en     | en            |
      | id     | id            |
