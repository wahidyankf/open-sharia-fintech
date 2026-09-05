Feature: Course omitted from a path

  As a path curator
  I want a course that a path's manifest doesn't include to render its normal canonical view
  So that a curated subset never breaks navigation for a course it leaves out

  # Cycle 3.4 (aggregate binder) added real e2e coverage alongside the pre-existing Phase 2 unit
  # binding — course-paths.steps.ts.
  # Exemption(integration): the scenario is observable at the public browser or HTTP boundary and has no separate local resource boundary; alternative-proof: ayokoding-www-fe-e2e:test:e2e / A course omitted from a path shows no path nav for that path
  @integration-exempt
  Scenario: A course omitted from a path shows no path nav for that path
    Given a course is not listed in a given path's manifest
    When a reader opens that course with that path's context
    Then the course renders the canonical standalone view
    And neither the path rail nor the path banner is shown for that path
