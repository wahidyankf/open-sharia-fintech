Feature: Landing hero surfaces goal paths

  As a first-time visitor
  I want the site landing page's hero to show the goal-labeled paths directly
  So that I can pick a learning path without hunting through a generic menu first

  # Bound Phase 3, Cycle 3.2 — unit (landing.test.tsx) and e2e (course-paths.steps.ts).
  @unit @e2e
  Scenario: The landing hero surfaces the four goal paths directly
    Given a first-time visitor opens the site landing page at /en
    When the hero section renders
    Then the hero shows a goal-labeled path card for each published path
    And a "Compare all paths" link to /en/learn/paths is visible below the cards
