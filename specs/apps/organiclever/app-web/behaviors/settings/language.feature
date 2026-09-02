Feature: Language Setting

  As an app user
  I want to switch the app language between English and Bahasa Indonesia
  So that I can use the app in my preferred language

  @unit @e2e
  Scenario: Switch to Bahasa Indonesia
    Given the settings screen shows language is English
    When the user selects Indonesian language
    Then the language is set to Indonesian

  @unit @e2e
  Scenario: Switch back to English
    Given the settings screen shows language is Indonesian
    When the user selects English language
    Then the language is set to English
