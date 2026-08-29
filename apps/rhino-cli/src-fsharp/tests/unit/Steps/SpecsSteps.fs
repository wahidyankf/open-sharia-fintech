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

open System
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

    // ---- e2e-coverage.feature state ----

    /// Repo-relative feature path every synthetic e2e-coverage entry below
    /// shares — paired with `E2eMirrorKey` so `isUnboundOrAbsent` resolves the
    /// fixture's single generated `.spec.js` file to it.
    let e2eFeaturePath = "specs/apps/example/e2e.feature"
    let e2eMirrorKey = "e2e.feature"
    let mutable e2eScenarioRoot: string option = None
    let mutable e2eDeclared: BaselineEntry list = []
    let mutable e2eFixme: BaselineEntry list = []
    let mutable e2eBaseline: BaselineEntry list = []
    let mutable e2eGenDir: string option = None
    let mutable e2eGeneratedJs: string option = None
    let mutable e2eReport: GapReport option = None
    let mutable e2eError: string option = None
    let mutable e2eText: string = ""
    let mutable e2eBaselinePath: string option = None
    let mutable e2eSaveOutcome: Result<unit, string> option = None
    let mutable e2eLoaded: BaselineManifest option = None

    let e2eRoot () : string =
        match e2eScenarioRoot with
        | Some dir -> dir
        | None ->
            let dir =
                Path.Combine(Path.GetTempPath(), "rhino-cli-e2e-coverage-" + Guid.NewGuid().ToString("N"))

            Directory.CreateDirectory dir |> ignore
            e2eScenarioRoot <- Some dir
            dir

    /// Builds a `{feature, scenario}` entry against the shared fixture path.
    let e2eEntry (title: string) : BaselineEntry =
        { Feature = e2eFeaturePath
          Scenario = title }

    /// Writes `js` as the single generated `.spec.js` file playwright-bdd
    /// would emit for `e2eFeaturePath`, inside a fresh `.features-gen`
    /// directory, and points the validate step at it.
    let e2eWriteGenerated (js: string) : unit =
        let dir = Path.Combine(e2eRoot (), ".features-gen")
        Directory.CreateDirectory dir |> ignore
        File.WriteAllText(Path.Combine(dir, e2eMirrorKey + ".spec.js"), js)
        e2eGenDir <- Some dir
        e2eGeneratedJs <- Some js

    /// The `GapReport` the validate step produced, or a failure if the step
    /// errored before diffing.
    let e2eRequireReport () : GapReport =
        match e2eReport with
        | Some report -> report
        | None -> failwith "validate did not produce a gap report"

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

    // ---- Given (`e2e-coverage.feature`) ----

    [<Given>]
    member _.``a playwright-bdd project whose generated output marks scenarios "A" and "B" as test.fixme``() =
        e2eDeclared <- [ e2eEntry "A"; e2eEntry "B" ]
        e2eFixme <- [ e2eEntry "A"; e2eEntry "B" ]

    [<Given>]
    member _.``a baseline manifest that lists exactly scenarios "A" and "B" as allowed unbound``() =
        e2eBaseline <- [ e2eEntry "A"; e2eEntry "B" ]

    [<Given>]
    member _.``a baseline manifest that lists exactly scenario "A" as allowed unbound``() =
        e2eBaseline <- [ e2eEntry "A" ]

    [<Given>]
    member _.``generated output that marks scenarios "A" and "C" as test.fixme``() =
        e2eDeclared <- [ e2eEntry "A"; e2eEntry "C" ]
        e2eFixme <- [ e2eEntry "A"; e2eEntry "C" ]

    [<Given>]
    member _.``a baseline manifest that lists scenarios "A" and "B" as allowed unbound``() =
        e2eBaseline <- [ e2eEntry "A"; e2eEntry "B" ]

    [<Given>]
    member _.``generated output that marks only scenario "A" as test.fixme``() =
        e2eDeclared <- [ e2eEntry "A"; e2eEntry "B" ]
        e2eFixme <- [ e2eEntry "A" ]

    [<Given>]
    member _.``a scenario tagged \x40unit only that appears as test.fixme in the generated output``() =
        let scenarios =
            [ { FeaturePath = e2eFeaturePath
                Title = "Unit-only scenario"
                LevelTags = Set.ofList [ Unit ]
                IsWip = false } ]

        e2eDeclared <- declaredE2eEntries scenarios

        e2eWriteGenerated (
            String.Join(
                "\n",
                [ "test.describe('Feature: Example', () => {"
                  ""
                  "  test.fixme('Unit-only scenario', () => {});"
                  ""
                  "});"
                  "" ]
            )
        )

    [<Given>]
    member _.``a baseline manifest that lists no allowed unbound scenarios``() = e2eBaseline <- []

    [<Given>]
    member _.``an \x40e2e Scenario Outline whose generated Examples-row tests include one test.fixme``() =
        e2eDeclared <- [ e2eEntry "Resize the sidebar" ]

        e2eWriteGenerated (
            String.Join(
                "\n",
                [ "test.describe('Feature: Example', () => {"
                  ""
                  "  test.describe('Resize the sidebar', () => {"
                  ""
                  "    test('Example #1', () => {});"
                  ""
                  "    test.fixme('Example #2', () => {});"
                  ""
                  "  });"
                  ""
                  "});"
                  "" ]
            )
        )

    [<Given>]
    member _.``an \x40e2e Scenario Outline whose Examples table has zero data rows``() =
        e2eDeclared <- [ e2eEntry "Resize the sidebar" ]

        // A zero-row Examples table makes playwright-bdd render NOTHING for
        // the outline — only the file's other, unrelated content appears.
        e2eWriteGenerated (
            String.Join(
                "\n",
                [ "test.describe('Feature: Example', () => {"
                  ""
                  "  test('An unrelated bound scenario', () => {});"
                  ""
                  "});"
                  "" ]
            )
        )

    [<Given>]
    member _.``a .feature file with a "Rule:" block tagged "\x40skip"``() =
        e2eWriteGenerated (
            String.Join(
                "\n",
                [ "test.describe('Feature: Example', () => {"
                  ""
                  "  test.describe.skip('Rule: gated behaviour', () => {"
                  ""
                  "    test('Nested scenario', () => {});"
                  ""
                  "  });"
                  ""
                  "  test('Other scenario', () => {});"
                  ""
                  "});"
                  "" ]
            )
        )

    [<Given>]
    member _.``the Rule contains at least one Scenario``() =
        e2eDeclared <- e2eDeclared @ [ e2eEntry "Nested scenario" ]

    [<Given>]
    member _.``the file also has other, non-skipped content so it still generates``() =
        e2eDeclared <- e2eDeclared @ [ e2eEntry "Other scenario" ]

    [<Given>]
    member _.``a .feature file whose top-level "Feature:" is tagged "\x40fixme"``() =
        e2eDeclared <- [ e2eEntry "First scenario"; e2eEntry "Second scenario" ]

        e2eWriteGenerated (
            String.Join(
                "\n",
                [ "test.describe.fixme('Feature: Gated feature', () => {"
                  ""
                  "  test('First scenario', () => {});"
                  ""
                  "  test('Second scenario', () => {});"
                  ""
                  "});"
                  "" ]
            )
        )

    [<Given>]
    member _.``an \x40e2e scenario titled with an apostrophe that appears as test.fixme using playwright-bdd's escaped single-quote convention``
        ()
        =
        e2eDeclared <- [ e2eEntry "User's dashboard loads" ]

        e2eWriteGenerated (
            String.Join(
                "\n",
                [ "test.describe('Feature: Example', () => {"
                  ""
                  @"  test.fixme('User\'s dashboard loads', () => {});"
                  ""
                  "});"
                  "" ]
            )
        )

    [<Given>]
    member _.``a new unbound scenario "Resize the sidebar by keyboard" in "resizable-panel.feature"``() =
        let gap =
            { Feature = "specs/libs/web-ui/behavior/gherkin/resizable-panel/resizable-panel.feature"
              Scenario = "Resize the sidebar by keyboard" }

        e2eReport <-
            Some
                { NewGaps = [ gap ]
                  Stale = []
                  Failed = true }

    [<Given>]
    member _.``a project with no baseline manifest yet``() =
        let path = Path.Combine(e2eRoot (), "e2e-coverage-baseline.json")
        Assert.False(File.Exists path, "fixture must start with no baseline manifest")
        e2eBaselinePath <- Some path

    [<Given>]
    member _.``generated output that marks scenarios "A" and "B" as test.fixme``() =
        e2eDeclared <- [ e2eEntry "A"; e2eEntry "B" ]
        e2eFixme <- [ e2eEntry "A"; e2eEntry "B" ]

    [<Given>]
    member _.``a project whose .features-gen directory does not exist``() =
        let dir = Path.Combine(e2eRoot (), ".features-gen")
        Assert.False(Directory.Exists dir, "fixture must start with no generated-output directory")
        e2eGenDir <- Some dir

    // ---- When (`e2e-coverage.feature`) ----

    [<When>]
    member _.``rhino-cli specs e2e-coverage validate runs for that project``() =
        match e2eGenDir with
        | Some dir ->
            match scanFixmeDir dir with
            | Error message -> e2eError <- Some message
            | Ok byFile ->
                let fixme =
                    e2eDeclared
                    |> List.filter (fun entry -> isUnboundOrAbsent entry.Feature entry.Scenario byFile)

                e2eReport <- Some(diffGaps e2eDeclared fixme e2eBaseline)
        | None -> e2eReport <- Some(diffGaps e2eDeclared e2eFixme e2eBaseline)

    [<When>]
    member _.``rhino-cli specs e2e-coverage validate runs and detects it as a new gap``() =
        e2eText <- formatGapText (e2eRequireReport ())

    [<When>]
    member _.``rhino-cli specs e2e-coverage validate runs with the --update-baseline flag``() =
        let path =
            match e2eBaselinePath with
            | Some p -> p
            | None -> failwith "no baseline path established"

        e2eSaveOutcome <-
            Some(
                saveBaseline
                    path
                    { Project = "example-e2e"
                      AllowedUnbound = e2eFixme }
            )

    // ---- Then (`e2e-coverage.feature`) ----

    [<Then>]
    member _.``it passes with exit code 0``() =
        Assert.True(e2eError.IsNone, "validate must not error")
        Assert.False((e2eRequireReport ()).Failed, "validate must pass")

    [<Then>]
    member _.``it reports 2 declared-but-unbound scenarios all covered by the baseline``() =
        let report = e2eRequireReport ()
        let unbound = e2eDeclared |> List.filter (fun entry -> List.contains entry e2eFixme)
        Assert.Equal(2, List.length unbound)
        Assert.Empty(report.NewGaps)

    [<Then>]
    member _.``it fails with a non-zero exit code``() =
        match e2eError with
        | Some message -> Assert.False(String.IsNullOrWhiteSpace message, "error message must be populated")
        | None -> Assert.True((e2eRequireReport ()).Failed, "validate must fail")

    [<Then>]
    member _.``it names scenario "C" and its containing .feature file as a new unbound gap``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "C" ], report.NewGaps)

    [<Then>]
    member _.``it does not report scenario "A" as a new gap``() =
        let report = e2eRequireReport ()
        Assert.DoesNotContain(e2eEntry "A", report.NewGaps)

    [<Then>]
    member _.``it reports scenario "B" as newly bound relative to the baseline``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "B" ], report.Stale)

    [<Then>]
    member _.``it reports scenario "B" as a stale baseline entry that can be pruned``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "B" ], report.Stale)

    [<Then>]
    member _.``it does not report the \x40unit-only scenario as an unbound gap``() =
        let report = e2eRequireReport ()
        Assert.Empty(report.NewGaps)

        // Two-way check: the title IS emitted as test.fixme, so the pass above
        // comes from the @e2e declared-set filter, not from an empty fixture.
        let js =
            match e2eGeneratedJs with
            | Some content -> content
            | None -> failwith "no generated output written"

        Assert.Contains("Unit-only scenario", scanFixmeTitles js)

    [<Then>]
    member _.``it reports exactly one new unbound scenario for the outline``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "Resize the sidebar" ], report.NewGaps)

    [<Then>]
    member _.``it reports exactly one new unbound scenario for the zero-row outline``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "Resize the sidebar" ], report.NewGaps)

    [<Then>]
    member _.``every scenario nested under the skipped Rule is reported as unbound``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "Nested scenario" ], report.NewGaps)

    [<Then>]
    member _.``every scenario in the file is reported as unbound``() =
        let report = e2eRequireReport ()

        Assert.Equal<BaselineEntry list>([ e2eEntry "First scenario"; e2eEntry "Second scenario" ], report.NewGaps)

    [<Then>]
    member _.``it reports exactly one new unbound scenario for the apostrophe-bearing title``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "User's dashboard loads" ], report.NewGaps)

    [<Then>]
    member _.``the failure output contains the scenario title "Resize the sidebar by keyboard"``() =
        Assert.Contains("Resize the sidebar by keyboard", e2eText, StringComparison.Ordinal)

    [<Then>]
    member _.``the failure output contains the feature file path ending in "resizable-panel.feature"``() =
        Assert.Contains("resizable-panel.feature", e2eText, StringComparison.Ordinal)

    [<Then>]
    member _.``the failure output states the delta is an increase of 1 over baseline``() =
        Assert.Contains("increase of 1 over baseline", e2eText, StringComparison.Ordinal)

    [<Then>]
    member _.``it writes a baseline manifest listing scenarios "A" and "B" as allowed unbound``() =
        Assert.Equal<Result<unit, string> option>(Some(Ok()), e2eSaveOutcome)

        let path =
            match e2eBaselinePath with
            | Some p -> p
            | None -> failwith "no baseline path established"

        match loadBaseline path with
        | Error message -> failwith message
        | Ok manifest ->
            e2eLoaded <- Some manifest
            Assert.Equal<BaselineEntry list>([ e2eEntry "A"; e2eEntry "B" ], manifest.AllowedUnbound)

    [<Then>]
    member _.``a subsequent validate run for that project passes with exit code 0``() =
        let manifest =
            match e2eLoaded with
            | Some m -> m
            | None -> failwith "baseline manifest was not reloaded"

        let report = diffGaps e2eDeclared e2eFixme manifest.AllowedUnbound
        Assert.False(report.Failed, "a validate run against the freshly written baseline must pass")

    [<Then>]
    member _.``it reports that bddgen output was not found and must be generated first``() =
        let message =
            match e2eError with
            | Some m -> m
            | None -> failwith "validate did not report an error"

        Assert.Contains("not found", message, StringComparison.Ordinal)
        Assert.Contains("npx bddgen", message, StringComparison.Ordinal)

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

[<Fact>]
let ``A project's current unbound gaps exactly match its checked-in baseline`` () =
    FeatureRunner.run "e2e-coverage.feature" "A project's current unbound gaps exactly match its checked-in baseline"

[<Fact(DisplayName = "A newly added @e2e scenario ships without a step definition")>]
let ``A newly added e2e scenario ships without a step definition`` () =
    FeatureRunner.run "e2e-coverage.feature" "A newly added @e2e scenario ships without a step definition"

[<Fact>]
let ``A previously-unbound scenario is now bound`` () =
    FeatureRunner.run "e2e-coverage.feature" "A previously-unbound scenario is now bound"

[<Fact>]
let ``The baseline lists a scenario that is no longer unbound`` () =
    FeatureRunner.run "e2e-coverage.feature" "The baseline lists a scenario that is no longer unbound"

[<Fact(DisplayName = "A test.fixme scenario that is not @e2e-tagged is ignored")>]
let ``A test fixme scenario that is not e2e-tagged is ignored`` () =
    FeatureRunner.run "e2e-coverage.feature" "A test.fixme scenario that is not @e2e-tagged is ignored"

[<Fact>]
let ``A Scenario Outline ships an unbound Examples-row test`` () =
    FeatureRunner.run "e2e-coverage.feature" "A Scenario Outline ships an unbound Examples-row test"

[<Fact>]
let ``A Scenario Outline has zero Examples data rows`` () =
    FeatureRunner.run "e2e-coverage.feature" "A Scenario Outline has zero Examples data rows"

[<Fact(DisplayName = "A Rule-level @skip tag is detected as unbound")>]
let ``A Rule-level skip tag is detected as unbound`` () =
    FeatureRunner.run "e2e-coverage.feature" "A Rule-level @skip tag is detected as unbound"

[<Fact(DisplayName = "A Feature-level @fixme tag is detected as unbound")>]
let ``A Feature-level fixme tag is detected as unbound`` () =
    FeatureRunner.run "e2e-coverage.feature" "A Feature-level @fixme tag is detected as unbound"

[<Fact>]
let ``A test fixme title contains an escaped apostrophe`` () =
    FeatureRunner.run "e2e-coverage.feature" "A test.fixme title contains an escaped apostrophe"

[<Fact>]
let ``Output identifies each new gap by feature path and scenario title`` () =
    FeatureRunner.run "e2e-coverage.feature" "Output identifies each new gap by feature path and scenario title"

[<Fact>]
let ``First-time baseline generation snapshots current unbound scenarios`` () =
    FeatureRunner.run "e2e-coverage.feature" "First-time baseline generation snapshots current unbound scenarios"

[<Fact>]
let ``The generated output directory is absent`` () =
    FeatureRunner.run "e2e-coverage.feature" "The generated output directory is absent"
