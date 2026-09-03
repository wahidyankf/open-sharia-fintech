Feature: App Shell Navigation

  As an app user
  I want consistent bottom-tab navigation across all screens
  So that I can move between sections of the app without losing my place

  @unit @e2e
  Scenario: Default tab is Home on first load
    When the app is freshly loaded
    Then the Home tab is active
    And the app shell is visible

  @unit @e2e
  Scenario: Navigate to History tab
    Given the app shell is visible
    When the user taps the History tab
    Then the History tab is active

  @unit @e2e
  Scenario: Navigate to Progress tab
    Given the app shell is visible
    When the user taps the Progress tab
    Then the Progress tab is active

  @unit @e2e
  Scenario: Navigate to Settings tab
    Given the app shell is visible
    When the user taps the Settings tab
    Then the Settings tab is active

  @unit @e2e
  Scenario: Open and close Add Entry sheet
    Given the app shell is visible
    When the user taps the FAB button
    Then the Add Entry sheet is open
    And the user closes the Add Entry sheet
    And the Add Entry sheet is closed

  @unit @e2e
  Scenario Outline: URL persists across page refresh on each tab
    Given the user is on "<path>"
    When the user refreshes the page
    Then the URL is still "<path>"
    And the "<screen>" screen is visible

    Examples:
      | path           | screen   |
      | /app/home      | Home     |
      | /app/history   | History  |
      | /app/progress  | Progress |
      | /app/settings  | Settings |
