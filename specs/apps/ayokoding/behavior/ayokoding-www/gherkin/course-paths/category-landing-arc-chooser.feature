Feature: Careers category landing arc chooser

  As a reader exploring careers paths
  I want the careers category landing to offer an arc chooser
  So that I can pick the career arc that matches my situation before picking a specific role

  # Stays @wip — category-landing.tsx (careers instance) is Phase 3's category-split work
  # (R6/R7/R8), not yet built. Authored here verbatim from prd.md now, per
  # evidence/phase-2-specs-coverage-delta.txt.
  @wip
  Scenario: The careers category landing offers an arc chooser
    Given a fixture careers manifest set with three arcs is loaded
    When a reader opens the careers category landing at /en/learn/paths/careers/
    Then the page renders one arc card per arc with its member role(s) previewed
    And the immediately-effective arc card previews exactly two member roles
