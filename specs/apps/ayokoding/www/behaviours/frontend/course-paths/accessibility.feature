Feature: Course-paths accessibility contract

  As a reader using a keyboard or a screen reader
  I want every path-aware navigation surface to be a labelled, operable landmark
  So that following a learning path never depends on being able to see or use a mouse

  # Bound Phase 3, Cycle 3.3 — unit (path-rail.test.tsx, prerequisite-list.test.tsx and other
  # per-component Phase 2 tests already cover each landmark's individual attributes) and e2e,
  # asserted together across the full rendered surface for the first time here
  # (course-paths-a11y.steps.ts).
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / The navigation feature meets accessibility requirements
  @integration-exempt
  Scenario: The navigation feature meets accessibility requirements
    Given a reader uses a keyboard and a screen reader on a course in path context
    When they navigate the path rail, banner, breadcrumb, prerequisite list, and prev/next
    Then each is a labelled landmark reachable and operable by keyboard with visible focus
    And the document language attribute matches the active locale
