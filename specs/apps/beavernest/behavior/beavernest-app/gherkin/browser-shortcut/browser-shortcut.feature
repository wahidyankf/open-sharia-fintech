Feature: Browser shortcut guidance
  The browser guidance is accessible and does not promise offline behaviour.

  Scenario: Browser guidance keeps focus predictable
    Given I am using the workspace in a browser
    When I select Browser shortcut
    Then I am told that the workspace is online only
    And Escape closes the guidance and returns focus to Browser shortcut
