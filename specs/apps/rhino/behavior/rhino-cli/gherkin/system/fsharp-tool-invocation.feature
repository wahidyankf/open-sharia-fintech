@quality
Feature: Manifest-backed F# formatting checks

  Scenario: An F# lint target uses the pinned local Fantomas tool
    Given the F# lint targets are configured
    When the configured F# lint targets are inspected
    Then each target restores the local .NET tool manifest before running Fantomas
    And no target invokes the global Fantomas app host directly
    And an unformatted source file still makes the lint target fail
