Feature: Category landing empty state

  As a reader opening a category or arc landing before any path is published there
  I want an explicit, stated empty message instead of a blank content area
  So that I never mistake "nothing published yet" for a broken page

  # Bound Phase 3, Cycle 3.1a — unit-only by design (empty-path-list-state.test.tsx,
  # category-landing.test.tsx, arc-landing.test.tsx); delivery.md's Cycle 3.1a carries no e2e
  # command for this scenario.
  @unit
  Scenario: A category landing with no populated manifest renders an explicit empty state
    Given a structural category index exists with zero published path manifests
    When a reader opens that category's landing page
    Then the page renders a stated "being written, check back soon" message with a fallback link
    And the page never renders a blank content area with no message
