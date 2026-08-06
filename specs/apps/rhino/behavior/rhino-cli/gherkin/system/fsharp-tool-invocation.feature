@quality
Feature: Manifest-backed F# formatting checks

  Scenario: Every locally discovered F# lint target uses the pinned local Fantomas tool
    Given the local F# lint targets are discovered
    When every locally discovered F# lint target is evaluated
    Then at least one local Fantomas lint target is found when F# linting applies
    And each target restores the local .NET tool manifest before running Fantomas
    And no target invokes the global Fantomas app host directly
    And an unformatted source file still makes the lint target fail
