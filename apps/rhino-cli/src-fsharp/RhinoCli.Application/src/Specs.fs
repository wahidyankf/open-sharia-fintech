/// Port of the per-level `@covers` behavior coverage engine
/// [Repo-grounded — `apps/rhino-cli/src/application/behavior_coverage/types.rs`,
/// `apps/rhino-cli/src/application/behavior_coverage/validator.rs`] for
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/specs/behavior-coverage.feature`'s
/// 6 scenarios, plus the `domain/**`-scoped allowlist gate
/// [Repo-grounded — `apps/rhino-cli/src/application/domain_coverage/mod.rs`]
/// for `domain-coverage.feature`'s 2 scenarios, which reuses [`validate`]
/// rather than duplicating it.
///
/// Scope: this first PR against the `specs` subsystem ports only what
/// [`validate`] itself needs — [`TestLevel`], [`ScenarioSpec`],
/// [`CoversMarker`], [`ProjectEnvelope`], and [`BehaviorCoverageViolation`].
/// No Rust command wrapper for `specs behavior-coverage validate` is wired
/// through this file — the live CLI verb (`commands::specs_coverage::run`)
/// calls the same engine as one leg of a larger three-level check that this
/// plan's later `spec-coverage-validate.feature` PR ports — so, matching
/// `TestCoverage.fs`'s own established precedent for a feature with no
/// F# CLI dispatch arm yet, every scenario calls [`validate`] directly.
module RhinoCli.Application.Specs

/// Test level: unit, integration, or e2e.
type TestLevel =
    | Unit
    | Integration
    | E2e

/// A Gherkin scenario extracted from a feature file.
type ScenarioSpec =
    {
        FeaturePath: string
        Title: string
        /// Level tags declared on this scenario (@unit, @integration, @e2e).
        /// Empty means untagged (a lint error).
        LevelTags: Set<TestLevel>
        /// True if the scenario is tagged @wip (exempt from coverage).
        IsWip: bool
    }

/// An `@covers` marker found in a test source file.
type CoversMarker =
    {
        SourceFile: string
        /// Test level derived from the owning test target (unit/integration/e2e).
        Level: TestLevel
        FeaturePath: string
        ScenarioTitle: string
    }

/// The set of test levels a project supports (its level envelope P).
type ProjectEnvelope = { Levels: Set<TestLevel> }

/// A violation found by the behavior coverage engine.
type BehaviorCoverageViolation =
    /// A scenario has no @unit/@integration/@e2e level tags.
    | UntaggedScenario of FeaturePath: string * Title: string
    /// A scenario's tag names a level not in the project envelope P.
    | LevelOutsideEnvelope of FeaturePath: string * Title: string * RequiredLevel: TestLevel
    /// A scenario requires a level (from S) but has no @covers marker at that level.
    | MissingCoverage of FeaturePath: string * Title: string * MissingLevel: TestLevel
    /// A @covers marker targets a level not in the scenario's own tags S (over-coverage).
    | CoverageAtUndeclaredLevel of SourceFile: string * FeaturePath: string * Title: string * ExtraLevel: TestLevel
    /// A @covers marker references a scenario title that no feature file contains.
    | OrphanMarker of SourceFile: string * FeaturePath: string * ScenarioTitle: string

/// Validates `@covers` coverage for the given scenarios and markers.
///
/// Rules enforced:
/// - Untagged non-wip scenario → `UntaggedScenario`
/// - Scenario tag outside project envelope P → `LevelOutsideEnvelope`
/// - Missing marker at a required level → `MissingCoverage`
/// - Marker at a level not in the scenario's own tags S → `CoverageAtUndeclaredLevel`
/// - Marker referencing an unknown scenario → `OrphanMarker`
/// - `@wip` scenarios are fully exempt.
let validate
    (scenarios: ScenarioSpec list)
    (markers: CoversMarker list)
    (envelope: ProjectEnvelope)
    : BehaviorCoverageViolation list =
    let scenarioLookup =
        scenarios |> List.map (fun s -> (s.FeaturePath, s.Title), s) |> Map.ofList

    let scenarioViolations =
        scenarios
        |> List.collect (fun scenario ->
            if scenario.IsWip then
                []
            elif Set.isEmpty scenario.LevelTags then
                [ UntaggedScenario(scenario.FeaturePath, scenario.Title) ]
            else
                scenario.LevelTags
                |> Set.toList
                |> List.collect (fun level ->
                    let envelopeViolation =
                        if Set.contains level envelope.Levels then
                            []
                        else
                            [ LevelOutsideEnvelope(scenario.FeaturePath, scenario.Title, level) ]

                    let covered =
                        markers
                        |> List.exists (fun m ->
                            m.FeaturePath = scenario.FeaturePath
                            && m.ScenarioTitle = scenario.Title
                            && m.Level = level)

                    let coverageViolation =
                        if covered then
                            []
                        else
                            [ MissingCoverage(scenario.FeaturePath, scenario.Title, level) ]

                    envelopeViolation @ coverageViolation))

    let markerViolations =
        markers
        |> List.collect (fun marker ->
            match Map.tryFind (marker.FeaturePath, marker.ScenarioTitle) scenarioLookup with
            | None -> [ OrphanMarker(marker.SourceFile, marker.FeaturePath, marker.ScenarioTitle) ]
            | Some scenario ->
                if not scenario.IsWip && not (Set.contains marker.Level scenario.LevelTags) then
                    [ CoverageAtUndeclaredLevel(marker.SourceFile, marker.FeaturePath, scenario.Title, marker.Level) ]
                else
                    [])

    scenarioViolations @ markerViolations

/// `true` iff `projectName` is listed in `domainAreas`.
///
/// A project absent from the allowlist is skipped even if it has `domain/**`
/// feature files.
let isEligible (projectName: string) (domainAreas: string list) : bool =
    domainAreas |> List.contains projectName

/// Returns only those scenarios whose `FeaturePath` contains a `domain`
/// path component.
let filterDomainScenarios (scenarios: ScenarioSpec list) : ScenarioSpec list =
    scenarios
    |> List.filter (fun s -> s.FeaturePath.Split('/') |> Array.contains "domain")
