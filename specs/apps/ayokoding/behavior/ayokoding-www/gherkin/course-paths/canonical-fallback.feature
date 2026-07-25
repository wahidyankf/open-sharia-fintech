Feature: Canonical fallback rendering

  As a reader
  I want a course to render its full canonical view whenever no path context applies
  So that graceful fallback is the default rendering, not an error path bolted on afterward

  # Cycle 3.4 (aggregate binder) added real e2e coverage alongside the pre-existing Phase 2 unit
  # binding — course-paths.steps.ts.
  @unit @e2e
  Scenario: A course deep-linked without path context renders the canonical view
    Given a reader opens a course URL /en/learn/courses/<course-id> with no path context query parameter
    When the course page renders
    Then the course body renders in full with the content-tree breadcrumb and its prerequisite list
    And a "this course is part of" affordance lists every path that includes the course

  # Cycle 3.4 (aggregate binder) added real e2e coverage alongside the pre-existing Phase 2 unit
  # binding — course-paths.steps.ts.
  @unit @e2e
  Scenario: A course opened without path context renders the generic sidebar unchanged
    Given a reader opens a canonical course URL with no path context query parameter
    When the page renders
    Then the left sidebar shows the generic content tree exactly as it does elsewhere in the site
    And no path rail, path readout, or path breadcrumb segment appears
