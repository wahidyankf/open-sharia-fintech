Feature: Paths hub category grouping

  As a reader browsing every learning path
  I want the paths hub to group paths by category (careers vs. skills)
  So that I can tell at a glance which kind of path I'm looking at, not scan a flat, undifferentiated grid

  # Bound Phase 3, Cycle 3.4 (aggregate binder) — unit (route-paths-hub.test.tsx, implemented as
  # part of Cycle 3.1's GREEN step) and e2e (course-paths.steps.ts), the latter for the first time
  # here.
  @unit @e2e
  Scenario: The paths hub groups paths by category, not a flat grid
    Given a fixture manifest set covers both a careers-shaped and a skills-shaped fixture
    When a reader opens the paths hub at /en/learn/paths
    Then the hub renders a Careers section grouped by arc and a separate Skills section
    And no path card from either category is rendered outside its category's section
