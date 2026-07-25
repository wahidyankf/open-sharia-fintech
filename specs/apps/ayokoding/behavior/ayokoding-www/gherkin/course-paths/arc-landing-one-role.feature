Feature: Arc landing with one role

  As a reader opening a career arc that offers a single role
  I want that role's card to render full detail
  So that I never see a sparse stub or an empty placeholder card next to it

  # Stays @wip — arc-landing.tsx is Phase 3's category-split work (R6/R7/R8), not yet built.
  # Authored here verbatim from prd.md now, per evidence/phase-2-specs-coverage-delta.txt.
  @wip
  Scenario: An arc landing with one path renders a full card, not a sparse stub
    Given a fixture arc manifest lists exactly one role
    When a reader opens that arc's landing page
    Then the single role card renders with an inline first-phase syllabus preview
    And the layout does not reserve or render a visibly empty second card
