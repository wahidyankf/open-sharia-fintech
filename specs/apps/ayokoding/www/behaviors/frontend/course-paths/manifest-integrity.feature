Feature: Manifest integrity

  As a path-manifest author
  I want every course reference in a manifest to resolve to a real, unique course
  So that a manifest never links a reader to a missing or ambiguous course

  @wip
  Scenario: Every manifest course reference resolves to a real course
    Given a path manifest lists a courseOrder of course IDs
    When the manifest-integrity check runs
    Then every listed course ID resolves to an existing course in the library
    And no course ID appears more than once in the manifest
