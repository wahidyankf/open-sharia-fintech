/// TickSpec step definitions binding the 13 feature files under
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/specs/` to
/// `RhinoCli.Application.Specs`'s ports, mirroring the single monolithic
/// Rust `tests/specs_tree.rs` runner that owns all of them
/// [Repo-grounded — `apps/rhino-cli/tests/specs_tree.rs`].
///
/// This PR adds `domain-coverage.feature`'s 2 scenarios to the
/// `behavior-coverage.feature` wiring an earlier PR laid down. Follows
/// `TestCoverageSteps.fs`'s per-scenario slicing convention: each xunit
/// `[<Fact>]` below runs exactly one scenario, extracted from the real,
/// frozen feature file.
module RhinoCli.Tests.Unit.Steps.SpecsSteps

open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Specs

/// Repo-relative feature-file path shared by every synthetic `@covers`
/// scenario/marker built below — matches Rust's `BC_FEATURE_PATH` constant.
[<Literal>]
let private BcFeaturePath = "specs/apps/example/foo.feature"

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type SpecsSteps() =
    // ---- behavior-coverage.feature / domain-coverage.feature (pure engine) state ----
    let mutable bcScenarios: ScenarioSpec list = []
    let mutable bcMarkers: CoversMarker list = []
    let mutable bcEnvelope: ProjectEnvelope = { Levels = Set.empty }
    let mutable bcViolations: BehaviorCoverageViolation list = []
    let mutable bcExemptCount: int = 0
    let mutable dcProjectName: string = ""
    let mutable dcDomainAreas: string list = []
    let mutable dcEligible: bool = false

    // ---- Given (`behavior-coverage.feature`) ----

    [<Given>]
    member _.``a scenario with no \x40unit, \x40integration, or \x40e2e level tag``() =
        bcScenarios <-
            bcScenarios
            @ [ { FeaturePath = BcFeaturePath
                  Title = "Untagged scenario"
                  LevelTags = Set.empty
                  IsWip = false } ]

        bcEnvelope <- { Levels = Set.ofList [ Unit ] }

    [<Given>]
    member _.``a project whose coverage registry declares only the unit level``() =
        bcEnvelope <- { Levels = Set.ofList [ Unit ] }

    [<Given>]
    member _.``a scenario in that project tagged \x40integration``() =
        bcScenarios <-
            bcScenarios
            @ [ { FeaturePath = BcFeaturePath
                  Title = "Integration scenario"
                  LevelTags = Set.ofList [ Integration ]
                  IsWip = false } ]

    [<Given>]
    member _.``a scenario tagged \x40unit and \x40e2e``() =
        bcScenarios <-
            bcScenarios
            @ [ { FeaturePath = BcFeaturePath
                  Title = "Multi-level scenario"
                  LevelTags = Set.ofList [ Unit; E2e ]
                  IsWip = false } ]

        bcEnvelope <- { Levels = Set.ofList [ Unit; E2e ] }

    [<Given>]
    member _.``a test marks it \x40covers at the unit level only``() =
        let title = (List.last bcScenarios).Title

        bcMarkers <-
            bcMarkers
            @ [ { SourceFile = "apps/example/src/test.rs"
                  Level = Unit
                  FeaturePath = BcFeaturePath
                  ScenarioTitle = title } ]

    [<Given>]
    member _.``a scenario tagged \x40unit only``() =
        bcScenarios <-
            bcScenarios
            @ [ { FeaturePath = BcFeaturePath
                  Title = "Unit-only scenario"
                  LevelTags = Set.ofList [ Unit ]
                  IsWip = false } ]

        bcEnvelope <- { Levels = Set.ofList [ Unit; E2e ] }

    [<Given>]
    member _.``a test marks it \x40covers at the e2e level``() =
        let title = (List.last bcScenarios).Title

        bcMarkers <-
            bcMarkers
            @ [ { SourceFile = "apps/example-e2e/tests/test.spec.ts"
                  Level = E2e
                  FeaturePath = BcFeaturePath
                  ScenarioTitle = title } ]

    [<Given>]
    member _.``a test with an \x40covers marker referencing a scenario title that no feature file contains``() =
        bcMarkers <-
            bcMarkers
            @ [ { SourceFile = "apps/example/src/test.rs"
                  Level = Unit
                  FeaturePath = BcFeaturePath
                  ScenarioTitle = "Non-existent scenario" } ]

        bcEnvelope <- { Levels = Set.ofList [ Unit ] }

    [<Given>]
    member _.``a scenario tagged \x40wip with no \x40covers markers``() =
        bcScenarios <-
            bcScenarios
            @ [ { FeaturePath = BcFeaturePath
                  Title = "WIP scenario"
                  LevelTags = Set.empty
                  IsWip = true } ]

        bcEnvelope <- { Levels = Set.ofList [ Unit ] }

    // ---- When / Then (`behavior-coverage.feature`) ----

    [<When>]
    member _.``rhino-cli specs behavior-coverage validate runs``() =
        bcViolations <- validate bcScenarios bcMarkers bcEnvelope
        bcExemptCount <- bcScenarios |> List.filter (fun s -> s.IsWip) |> List.length

    [<Then>]
    member _.``it fails and names the untagged scenario``() =
        Assert.True(
            bcViolations
            |> List.exists (function
                | UntaggedScenario(_, title) -> title = "Untagged scenario"
                | _ -> false),
            sprintf "got: %A" bcViolations
        )

    [<Then>]
    member _.``it fails because the scenario requires a level not in the project envelope``() =
        Assert.True(
            bcViolations
            |> List.exists (function
                | LevelOutsideEnvelope _ -> true
                | _ -> false),
            sprintf "got: %A" bcViolations
        )

    [<Then>]
    member _.``it fails and names the missing e2e coverage``() =
        Assert.True(
            bcViolations
            |> List.exists (function
                | MissingCoverage(_, _, E2e) -> true
                | _ -> false),
            sprintf "got: %A" bcViolations
        )

    [<Then>]
    member _.``it fails because the e2e level is not declared for that scenario``() =
        Assert.True(
            bcViolations
            |> List.exists (function
                | CoverageAtUndeclaredLevel _ -> true
                | _ -> false),
            sprintf "got: %A" bcViolations
        )

    [<Then>]
    member _.``it fails and names the orphan marker``() =
        Assert.True(
            bcViolations
            |> List.exists (function
                | OrphanMarker(_, _, scenarioTitle) -> scenarioTitle = "Non-existent scenario"
                | _ -> false),
            sprintf "got: %A" bcViolations
        )

    [<Then>]
    member _.``it does not fail and reports the scenario in the exempt count``() =
        Assert.Empty(bcViolations: BehaviorCoverageViolation list)
        Assert.Equal(1, bcExemptCount)

    // ---- Given / When / Then (`domain-coverage.feature`) ----

    [<Given>]
    member _.``a project listed in the specs.domain-areas allowlist``() =
        dcDomainAreas <- [ "ose-be" ]
        dcProjectName <- "ose-be"

    [<Given>]
    member _.``a domain scenario not covered at its required level by any \x40covers marker``() =
        bcScenarios <-
            bcScenarios
            @ [ { FeaturePath = "specs/apps/ose/behavior/be/domain/foo.feature"
                  Title = "Uncovered domain scenario"
                  LevelTags = Set.ofList [ Unit ]
                  IsWip = false } ]

        bcEnvelope <- { Levels = Set.ofList [ Unit ] }

    [<Given>]
    member _.``a project not listed in the specs.domain-areas allowlist``() =
        dcDomainAreas <- [ "ose-be" ]
        dcProjectName <- "rhino-cli"

    [<Given>]
    member _.``that project has domain/\*\* feature files``() =
        bcScenarios <-
            bcScenarios
            @ [ { FeaturePath = "specs/apps/rhino/behavior/rhino-cli/domain/bar.feature"
                  Title = "Domain scenario for skipped project"
                  LevelTags = Set.ofList [ Unit ]
                  IsWip = false } ]

        bcEnvelope <- { Levels = Set.ofList [ Unit ] }

    [<When>]
    member _.``rhino-cli specs domain-coverage validate runs``() =
        dcEligible <- isEligible dcProjectName dcDomainAreas

        bcViolations <-
            if dcEligible then
                validate (filterDomainScenarios bcScenarios) bcMarkers bcEnvelope
            else
                []

    [<Then>]
    member _.``it fails and names the uncovered domain scenario``() =
        Assert.True(dcEligible, "project must be eligible for this scenario")

        Assert.True(
            bcViolations
            |> List.exists (function
                | MissingCoverage(_, title, _) -> title = "Uncovered domain scenario"
                | _ -> false),
            sprintf "got: %A" bcViolations
        )

    [<Then>]
    member _.``the project is skipped and no violation is reported``() =
        Assert.False(dcEligible, "project must be skipped (not in domain-areas allowlist)")
        Assert.Empty(bcViolations: BehaviorCoverageViolation list)

module private FeatureRunner =

    let private featureDir: string =
        Path.GetFullPath(
            Path.Combine(
                __SOURCE_DIRECTORY__,
                "..",
                "..",
                "..",
                "..",
                "..",
                "..",
                "specs",
                "apps",
                "rhino",
                "behavior",
                "rhino-cli",
                "gherkin",
                "specs"
            )
        )

    let private extractScenario (featureLines: string[]) (scenarioTitle: string) : string[] =
        let featureLine =
            featureLines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", System.StringComparison.Ordinal))

        let scenarioHeader = sprintf "Scenario: %s" scenarioTitle

        let startIdx = featureLines |> Array.findIndex (fun l -> l.Trim() = scenarioHeader)

        let endIdx =
            featureLines
            |> Array.skip (startIdx + 1)
            |> Array.tryFindIndex (fun l ->
                let trimmed = l.Trim()

                trimmed.StartsWith("Scenario:", System.StringComparison.Ordinal)
                || trimmed.StartsWith("Scenario Outline:", System.StringComparison.Ordinal)
                || trimmed.StartsWith("@", System.StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    /// Runs the single scenario named `scenarioTitle` from `featureFileName`
    /// (a file directly inside `gherkin/specs/`), bound against `SpecsSteps`.
    let run (featureFileName: string) (scenarioTitle: string) : unit =
        let featurePath = Path.Combine(featureDir, featureFileName)
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<SpecsSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``An untagged scenario fails the gate`` () =
    FeatureRunner.run "behavior-coverage.feature" "An untagged scenario fails the gate"

[<Fact>]
let ``A scenario requiring a level outside the project envelope fails`` () =
    FeatureRunner.run "behavior-coverage.feature" "A scenario requiring a level outside the project envelope fails"

[<Fact>]
let ``A scenario not covered at a required level fails`` () =
    FeatureRunner.run "behavior-coverage.feature" "A scenario not covered at a required level fails"

[<Fact(DisplayName = "An @covers at an undeclared level fails")>]
let ``An covers at an undeclared level fails`` () =
    FeatureRunner.run "behavior-coverage.feature" "An @covers at an undeclared level fails"

[<Fact(DisplayName = "An orphan @covers marker fails the gate")>]
let ``An orphan covers marker fails the gate`` () =
    FeatureRunner.run "behavior-coverage.feature" "An orphan @covers marker fails the gate"

[<Fact(DisplayName = "A @wip scenario is exempt from coverage")>]
let ``A wip scenario is exempt from coverage`` () =
    FeatureRunner.run "behavior-coverage.feature" "A @wip scenario is exempt from coverage"

[<Fact>]
let ``An uncovered domain scenario fails the gate`` () =
    FeatureRunner.run "domain-coverage.feature" "An uncovered domain scenario fails the gate"

[<Fact>]
let ``A project not in the domain-areas allowlist is skipped`` () =
    FeatureRunner.run "domain-coverage.feature" "A project not in the domain-areas allowlist is skipped"
