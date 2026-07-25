Feature: Category landing empty state

  As a reader opening a category or arc landing before any path is published there
  I want an explicit, stated empty message instead of a blank content area
  So that I never mistake "nothing published yet" for a broken page

  # Stays @wip — the shared EmptyPathListState component and its wiring into category/arc
  # landings is Phase 3's category-split work (R7/A3), not yet built. Authored here verbatim
  # from prd.md now, per evidence/phase-2-specs-coverage-delta.txt.
  @wip
  Scenario: A category landing with no populated manifest renders an explicit empty state
    Given a structural category index exists with zero published path manifests
    When a reader opens that category's landing page
    Then the page renders a stated "being written, check back soon" message with a fallback link
    And the page never renders a blank content area with no message
