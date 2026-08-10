Feature: Workspace neutral content

  Scenario: Workspace contains no promotional call to action
    Given I am viewing the rendered workspace home
    When I inspect the visible page content and accessible links
    Then no promotional product description is present
    And no external GitHub call to action is present
