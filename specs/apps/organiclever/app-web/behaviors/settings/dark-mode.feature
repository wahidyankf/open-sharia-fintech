Feature: Dark Mode

  As an app user
  I want to toggle dark mode in settings
  So that I can use the app comfortably in low-light environments

  @unit @e2e
  Scenario: Toggle dark mode on
    Given the settings screen shows dark mode is off
    When the user toggles dark mode
    Then dark mode is enabled

  @unit @e2e
  Scenario: Toggle dark mode off
    Given dark mode is enabled
    When the user toggles dark mode
    Then dark mode is disabled
