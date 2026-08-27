/// TickSpec step definitions binding `test-coverage-diff.feature`'s 4
/// scenarios to `RhinoCli.Application.TestCoverage`'s diff-coverage port
/// [Repo-grounded —
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/test-coverage/test-coverage-diff.feature`,
/// `apps/rhino-cli/src/application/testcoverage/diff.rs`].
///
/// Follows `EnvValidateSteps.fs`'s per-scenario slicing convention: each
/// xunit `[<Fact>]` below runs exactly one scenario, extracted from the
/// real, frozen feature file. No Rust command wrapper exists for
/// `test-coverage diff` under `apps/rhino-cli/src/commands/` (only
/// `test_coverage_validate.rs` is wired to a CLI verb there) to bind
/// argument shapes against, so — matching `TestCoverage.fs`'s own module doc
/// comment — every scenario below calls `computeDiffCoverage` directly with
/// a `CoverageMap`/`DiffHunk list` fixture built in this file, rather than
/// shelling a real `git diff` or round-tripping through a coverage-report
/// file parser.
module RhinoCli.Tests.Unit.Steps.TestCoverageSteps

open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.TestCoverage

/// One executable line's fixture coverage, used to build the
/// [`CoverageMap`] fixtures below.
let private lineCovered: LineCoverage = { HitCount = 1L; Branches = [] }

let private lineMissed: LineCoverage = { HitCount = 0L; Branches = [] }

let private coverageMapOf (files: (string * (int64 * LineCoverage) list) list) : CoverageMap =
    files |> List.map (fun (path, lines) -> path, Map.ofList lines) |> Map.ofList

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type TestCoverageSteps() =
    let mutable coverageMap: CoverageMap = Map.empty
    let mutable hunks: DiffHunk list = []
    let mutable excludePatterns: string list = []
    let mutable threshold: float = 0.0
    let mutable result: CoverageResult option = None

    let runDiff () =
        result <- Some(computeDiffCoverage "coverage.info" coverageMap hunks excludePatterns threshold)

    let theResult () : CoverageResult =
        result
        |> Option.defaultWith (fun () -> failwith "no command has been run by a When step")

    // ---- Given ----

    [<Given>]
    member _.``a coverage file and no git changes``() =
        coverageMap <- coverageMapOf [ "src/foo.fs", [ 1L, lineCovered; 2L, lineMissed ] ]
        hunks <- []

    [<Given>]
    member _.``a coverage file where all changed lines are covered``() =
        coverageMap <- coverageMapOf [ "src/foo.fs", [ 1L, lineCovered; 2L, lineCovered ] ]

        hunks <-
            [ { FilePath = "src/foo.fs"
                ChangedLines = [ 1L; 2L ] } ]

    [<Given>]
    member _.``a coverage file where some changed lines are missed``() =
        coverageMap <- coverageMapOf [ "src/foo.fs", [ 1L, lineCovered; 2L, lineMissed; 3L, lineMissed ] ]

        hunks <-
            [ { FilePath = "src/foo.fs"
                ChangedLines = [ 1L; 2L; 3L ] } ]

    [<Given>]
    member _.``a coverage file and changes in excluded files``() =
        coverageMap <-
            coverageMapOf
                [ "src/kept.fs", [ 1L, lineCovered; 2L, lineCovered ]
                  "generated/skip.fs", [ 1L, lineMissed; 2L, lineMissed ] ]

        hunks <-
            [ { FilePath = "src/kept.fs"
                ChangedLines = [ 1L; 2L ] }
              { FilePath = "generated/skip.fs"
                ChangedLines = [ 1L; 2L ] } ]

    // ---- When ----

    [<When>]
    member _.``the developer runs test-coverage diff``() =
        threshold <- 0.0
        excludePatterns <- []
        runDiff ()

    [<When>]
    member _.``the developer runs test-coverage diff with a threshold``() =
        threshold <- 80.0
        excludePatterns <- []
        runDiff ()

    [<When>]
    member _.``the developer runs test-coverage diff with a high threshold``() =
        threshold <- 90.0
        excludePatterns <- []
        runDiff ()

    [<When>]
    member _.``the developer runs test-coverage diff with exclusion``() =
        threshold <- 0.0
        excludePatterns <- [ "generated/*" ]
        runDiff ()

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() = Assert.True((theResult ()).Passed)

    [<Then>]
    member _.``the output reports 100% coverage``() = Assert.Equal(100.0, (theResult ()).Pct)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.False((theResult ()).Passed)

    [<Then>]
    member _.``the excluded files do not affect the diff coverage result``() =
        let r = theResult ()
        Assert.DoesNotContain(r.Files, fun (f: FileResult) -> f.Path = "generated/skip.fs")
        Assert.Equal(100.0, r.Pct)
        Assert.Equal(2, r.Total)

/// Reads one named `Scenario:` block out of the real, frozen
/// `test-coverage-diff.feature` file (leaving the file itself untouched) and
/// runs it through TickSpec bound only against `TestCoverageSteps` — see
/// `EnvSteps.fs`'s `FeatureRunner` for why this is per-scenario rather than
/// per-file.
module private FeatureRunner =

    let private featurePath: string =
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
                "test-coverage",
                "test-coverage-diff.feature"
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

    /// Runs the single scenario named `scenarioTitle` from
    /// `test-coverage-diff.feature`, bound against `TestCoverageSteps`.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<TestCoverageSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``No changed lines reports 100% coverage`` () =
    FeatureRunner.run "No changed lines reports 100% coverage"

[<Fact>]
let ``Changed lines with full coverage pass threshold`` () =
    FeatureRunner.run "Changed lines with full coverage pass threshold"

[<Fact>]
let ``Changed lines with missing coverage fail threshold`` () =
    FeatureRunner.run "Changed lines with missing coverage fail threshold"

[<Fact>]
let ``Excluded files are not counted in diff coverage`` () =
    FeatureRunner.run "Excluded files are not counted in diff coverage"
