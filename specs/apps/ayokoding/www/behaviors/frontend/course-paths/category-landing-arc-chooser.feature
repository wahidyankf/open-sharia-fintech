Feature: Careers category landing arc chooser

  As a reader exploring careers paths
  I want the careers category landing to offer an arc chooser
  So that I can pick the career arc that matches my situation before picking a specific role

  # Bound Phase 3, Cycle 3.1b-i — unit (category-landing.test.tsx) and e2e (course-paths.steps.ts).
  @unit @e2e
  Scenario: The careers category landing offers an arc chooser
    Given a fixture careers manifest set with three arcs is loaded
    When a reader opens the careers category landing at /en/learn/paths/careers/
    Then the page renders one arc card per arc with its member role(s) previewed
    And the immediately-effective arc card previews exactly two member roles
