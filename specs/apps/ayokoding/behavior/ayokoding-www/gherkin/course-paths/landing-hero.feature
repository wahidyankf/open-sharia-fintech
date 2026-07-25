Feature: Landing hero surfaces goal paths

  As a first-time visitor
  I want the site landing page's hero to show the goal-labeled paths directly
  So that I can pick a learning path without hunting through a generic menu first

  # Stays @wip — Screen 0's hero (apps/ayokoding-www/src/features/app-shell/shell/hero.tsx
  # extension) is this plan's Phase 3/4 work, not yet built. Authored here verbatim from
  # prd.md now, per evidence/phase-2-specs-coverage-delta.txt.
  @wip
  Scenario: The landing hero surfaces the four goal paths directly
    Given a first-time visitor opens the site landing page at /en
    When the hero section renders
    Then the hero shows a goal-labeled path card for each published path
    And a "Compare all paths" link to /en/learn/paths is visible below the cards
