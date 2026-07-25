Feature: Course-paths accessibility contract

  As a reader using a keyboard or a screen reader
  I want every path-aware navigation surface to be a labelled, operable landmark
  So that following a learning path never depends on being able to see or use a mouse

  # Stays @wip — asserted across the full rendered surface (rail, banner, breadcrumb,
  # prerequisite list, prev/next) together, which is only complete once Phase 3/4 ship the
  # remaining path-landing/category/arc surfaces. Authored here verbatim from prd.md now,
  # per evidence/phase-2-specs-coverage-delta.txt.
  @wip
  Scenario: The navigation feature meets accessibility requirements
    Given a reader uses a keyboard and a screen reader on a course in path context
    When they navigate the path rail, banner, breadcrumb, prerequisite list, and prev/next
    Then each is a labelled landmark reachable and operable by keyboard with visible focus
    And the document language attribute matches the active locale
