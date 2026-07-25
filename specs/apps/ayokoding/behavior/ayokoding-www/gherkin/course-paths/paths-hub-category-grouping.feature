Feature: Paths hub category grouping

  As a reader browsing every learning path
  I want the paths hub to group paths by category (careers vs. skills)
  So that I can tell at a glance which kind of path I'm looking at, not scan a flat, undifferentiated grid

  # Stays @wip — the paths hub renderer is Phase 3's category-split work (R6/R7), not yet built.
  # Authored here verbatim from prd.md now, per evidence/phase-2-specs-coverage-delta.txt.
  @wip
  Scenario: The paths hub groups paths by category, not a flat grid
    Given a fixture manifest set covers both a careers-shaped and a skills-shaped fixture
    When a reader opens the paths hub at /en/learn/paths
    Then the hub renders a Careers section grouped by arc and a separate Skills section
    And no path card from either category is rendered outside its category's section
