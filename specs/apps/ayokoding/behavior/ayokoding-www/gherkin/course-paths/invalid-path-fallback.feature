Feature: Invalid path context fallback

  As a reader
  I want an unrecognized or stale path context to fall back silently to the canonical view
  So that a broken or outdated path link never surfaces an error

  # Cycle 3.4 (aggregate binder) added real e2e coverage alongside the pre-existing Phase 2 unit
  # binding — course-paths.steps.ts.
  @unit @e2e
  Scenario: An invalid path context falls back to the canonical view
    Given a reader opens a course URL with a path context that names no known path
    When the course page renders
    Then the course renders the canonical standalone view
    And no error is shown
