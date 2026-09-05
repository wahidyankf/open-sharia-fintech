Feature: Theme
  As a site visitor
  I want to switch between light and dark mode
  So that I can read comfortably in my preferred visual environment

  Background:
    Given the app is running

  # Exemption(integration): the local-resource boundary cannot observe browser theme state without crossing the public browser boundary; alternative-proof: ose-www-fe-e2e:test:e2e / Default theme is light mode
  @integration-exempt
  Scenario: Default theme is light mode
    When the site loads without a stored theme preference
    Then the theme is set to light mode

  # Exemption(integration): the local-resource boundary cannot observe browser theme interaction without crossing the public browser boundary; alternative-proof: ose-www-fe-e2e:test:e2e / Theme toggle switches between modes
  @integration-exempt
  Scenario: Theme toggle switches between modes
    Given the site is in light mode
    When the user clicks the theme toggle and selects dark mode
    Then the site switches to dark mode
