Feature: Browser shortcut guidance
  The browser guidance is accessible and does not promise offline behaviour.

  Scenario: Browser Help keeps focus predictable
  Given I am using the workspace in a browser
    When I select Help
    Then I am told Browser Help is online only and browser availability varies
    And Escape closes the guidance and returns focus to Help
