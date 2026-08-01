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
