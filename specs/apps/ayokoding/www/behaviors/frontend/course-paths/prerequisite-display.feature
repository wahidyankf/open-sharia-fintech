Feature: Prerequisite display

  As a reader
  I want a course page to list its declared prerequisites regardless of path context
  So that I always know what to complete before this course, even outside a path

  @unit
  Scenario: A course page surfaces its declared prerequisites
    Given a course declares prerequisites in its canonical metadata
    When a reader opens the course page with or without a path context
    Then the page lists each prerequisite course with a link to its canonical URL
    And the prerequisite list renders even in the canonical no-path view
