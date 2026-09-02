Feature: Structural design token exports
  As a frontend developer
  I want web-ui-token to export the structural design tokens
  So that every app can consume a consistent color, spacing, radius, and typography scale

  Scenario: The package exports every structural token module
    Given the web-ui-token package
    When I import from "@open-sharia-enterprise/web-ui-token"
    Then "colorTokens" should be exported
    And "radius" should be exported
    And "spacing" should be exported
    And "typography" should be exported
