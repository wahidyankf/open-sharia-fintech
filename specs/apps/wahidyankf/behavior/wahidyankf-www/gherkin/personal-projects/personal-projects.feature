Feature: Personal projects page

  As a visitor to wahidyankf-web
  I want to browse a list of personal projects
  So that I can learn what I have built outside of employed work

  Background:
    Given the app is running

  @unit @e2e
  Scenario: Personal projects page renders the heading
    When a visitor opens the personal projects page
    Then the H1 shows "Independent Projects"

  @unit @e2e
  Scenario: Personal projects page renders a search input
    When a visitor opens the personal projects page
    Then a search input with placeholder "Search projects..." is visible

  @unit @e2e
  Scenario: Personal projects page lists at least one project card
    When a visitor opens the personal projects page
    Then at least one project card is visible

  @unit @e2e
  Scenario: Each project card exposes external links where applicable
    When a visitor opens the personal projects page
    Then every project card exposes a Repository, Website, or YouTube link where the project has that resource

  @unit @e2e
  Scenario: Each project card shows how long the project has been running
    When a visitor opens the personal projects page
    Then every project card shows a duration next to its start date

  @unit @e2e
  Scenario: Each project card exposes clickable skill tags
    When a visitor opens the personal projects page
    Then every project card exposes at least one clickable skill tag

  @unit @e2e
  Scenario: Clicking a skill tag filters the project list
    When a visitor opens the personal projects page and clicks the "TypeScript" skill tag
    Then the URL becomes /personal-projects?search=TypeScript
