Feature: Static filtered portfolio routes

  As a visitor sharing a portfolio search
  I want the filtered CV URL to retain its result state
  So that recipients can open relevant portfolio entries directly

  Background:
    Given the app is running

  @unit @e2e
  Scenario: Search-filtered portfolio routes are static yet still filterable
    When a visitor opens the shared CV search URL for "TypeScript"
    Then the CV search input is prefilled with "TypeScript"
    And the "Head of Engineering - Hijra Bank" entry is visible
    And the "Database Design Fundamentals for Software Engineers" entry is hidden

  @unit @e2e
  Scenario: Public portfolio routes are available from the production server
    When a visitor requests every public portfolio page
    Then each public portfolio page responds with a successful HTML document

  @e2e
  Scenario: Crawlers receive discovery directives for every public route
    When a crawler requests the robots and sitemap routes
    Then robots permits crawling and names the canonical sitemap
    And the sitemap lists every public portfolio route
