Feature: Home Screen

  As an app user
  I want to see my recent journal entries on the home screen
  So that I can review and manage what I have logged

  Scenario: Home screen shows entry list
    When the home screen is loaded with entries
    Then the entry list is visible

  Scenario: Filter entries by kind
    Given the home screen is loaded with workout and reading entries
    When the user selects the Workout filter
    Then only workout entries are shown

  Scenario: Open entry detail sheet
    Given the home screen shows an entry
    When the user taps the entry
    Then the entry detail sheet opens
    And the user closes the sheet
    And the entry detail sheet is closed
