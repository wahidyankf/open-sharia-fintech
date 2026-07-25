Feature: Arc landing with two roles

  As a reader opening a career arc that offers two roles
  I want both role cards to render fully, side by side
  So that comparing the two roles never shows a placeholder standing in for real content

  # Stays @wip — arc-landing.tsx is Phase 3's category-split work (R6/R7/R8), not yet built.
  # Authored here verbatim from prd.md now, per evidence/phase-2-specs-coverage-delta.txt.
  @wip
  Scenario: An arc landing with two paths renders both role cards without a placeholder
    Given the fixture immediately-effective arc manifest lists two roles
    When a reader opens the arc landing at /en/learn/paths/careers/immediately-effective/
    Then both role cards render side by side with their own course counts
    And neither card is a placeholder or an empty grid cell
