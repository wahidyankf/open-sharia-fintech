@quality
Feature: Manifest-backed F# formatting checks

  Scenario: Every locally discovered F# lint target uses the pinned local Fantomas tool
    Given the local F# lint targets are discovered
    When every locally discovered F# lint target is evaluated
    Then every discovered F# lint target is evaluated
    And each target restores its local .NET tool manifest before running Fantomas
    And no target invokes the global Fantomas app host directly
    And an unformatted source file is checked only when F# lint targets exist
