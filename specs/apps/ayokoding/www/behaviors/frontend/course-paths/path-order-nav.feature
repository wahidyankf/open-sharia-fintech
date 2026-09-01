Feature: Path-order navigation

  As a reader following a learning path
  I want prev/next and the path rail to follow the manifest's course order
  So that I always know where I am in the path and what comes next

  @unit
  Scenario: Prev and next follow the active path's order
    Given a reader is on a course with an active path context
    When the reader reads the prev/next navigation
    Then prev and next are the neighboring courses in that path's manifest
    And both links preserve the path context query parameter

  # Cycle 3.4 (aggregate binder) added real e2e coverage alongside the pre-existing Phase 2 unit
  # binding — course-paths.steps.ts.
  @unit @e2e
  Scenario: The path rail shows the whole ordered arc beside a course at desktop width
    Given a reader opens a course in path context on a desktop-width viewport
    When the page renders
    Then the left rail lists that path's courses in manifest order with the current course marked
    And the current course is distinguished by a marker and weight, not by colour alone
    And the rail offers a link back to the full path and to the whole course library

  # Cycle 3.4 (aggregate binder) added real e2e coverage alongside the pre-existing Phase 2 unit
  # binding — course-paths.steps.ts.
  @unit @e2e
  Scenario: The path rail collapses into the existing navigation drawer on a phone
    Given a reader opens a course in path context on a phone-width viewport
    When they activate the path readout's "open path course list" control
    Then the existing left navigation drawer opens showing that path's ordered courses
    And focus moves into the drawer and returns to the control when the drawer is dismissed
