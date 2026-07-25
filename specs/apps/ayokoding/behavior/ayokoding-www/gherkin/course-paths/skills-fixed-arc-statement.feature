Feature: Skills category landing fixed-arc statement

  As a reader exploring skills paths
  I want the skills category landing to state its one ramp promise plainly, with no chooser
  So that I'm not asked to pick among arcs that don't exist for this category

  # Stays @wip — category-landing.tsx (skills instance) is Phase 3's category-split work
  # (R6/R7/R8), not yet built. Authored here verbatim from prd.md now, per
  # evidence/phase-2-specs-coverage-delta.txt.
  @wip
  Scenario: The skills category landing states its fixed arc once, with no chooser
    Given a fixture skills manifest set is loaded
    When a reader opens the skills category landing at /en/learn/paths/skills/
    Then the page renders the ramp promise once as a statement, not a question
    And no arc-selection control is present anywhere on the page
