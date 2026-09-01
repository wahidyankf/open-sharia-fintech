Feature: The course-paths rendering layer builds and validates green

  As the ayokoding-www maintainers
  I want the complete course-paths rendering layer to build, test, and validate cleanly
  So that shipping path-aware navigation never regresses the site's quality gates

  # Stays @wip — "the course-paths rendering layer is complete over a fixture manifest" is only
  # true once Phase 3/4 ship the remaining path-landing/category/arc surfaces. Authored here
  # verbatim from prd.md now, per evidence/phase-2-specs-coverage-delta.txt.
  @wip
  Scenario: The navigation feature builds and validates green
    Given the course-paths rendering layer is complete over a fixture manifest
    When the ayokoding-www build, the unit tier, the fixture e2e suite, and the link and heading validators run
    Then the build and every tier succeed
    And link, heading-hierarchy, and markdownlint validation report no errors
