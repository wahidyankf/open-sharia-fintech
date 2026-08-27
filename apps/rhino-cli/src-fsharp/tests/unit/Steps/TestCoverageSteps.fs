/// TickSpec step definitions binding `test-coverage-diff.feature`'s 4
/// scenarios and `test-coverage-merge.feature`'s 3 scenarios to
/// `RhinoCli.Application.TestCoverage`'s diff-coverage and merge-coverage
/// ports [Repo-grounded —
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/test-coverage/test-coverage-diff.feature`,
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/test-coverage/test-coverage-merge.feature`,
/// `apps/rhino-cli/src/application/testcoverage/diff.rs`,
/// `apps/rhino-cli/src/application/testcoverage/merge.rs`,
/// `apps/rhino-cli/src/application/testcoverage/lcov.rs`].
///
/// Follows `EnvValidateSteps.fs`'s per-scenario slicing convention: each
/// xunit `[<Fact>]` below runs exactly one scenario, extracted from the
/// real, frozen feature file. Neither `test-coverage diff` nor
/// `test-coverage merge` has a Rust command wrapper under
/// `apps/rhino-cli/src/commands/` (only `test_coverage_validate.rs` is wired
/// to a CLI verb there) to bind argument shapes against, so — matching
/// `TestCoverage.fs`'s own module doc comment — every scenario below calls
/// `computeDiffCoverage`/`toCoverageMapLcov`/`mergeCoverageMaps`/`writeLcov`/
/// `resultFromCoverageMap` directly rather than shelling a real CLI verb.
/// The merge scenarios do write real temp LCOV files to disk (rather than
/// building `CoverageMap` fixtures in memory like the diff scenarios do)
/// because "the merged output file exists in LCOV format" is itself part of
/// what the first merge scenario asserts.
module RhinoCli.Tests.Unit.Steps.TestCoverageSteps

open System
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
    let mutable lcovFilePaths: string list = []
    let mutable mergedCoverageMap: CoverageMap = Map.empty
    let mutable outputFilePath: string = ""

    let runDiff () =
        result <- Some(computeDiffCoverage "coverage.info" coverageMap hunks excludePatterns threshold)

    let theResult () : CoverageResult =
        result
        |> Option.defaultWith (fun () -> failwith "no command has been run by a When step")

    let newTempDir () =
        let dir =
            Path.Combine(Path.GetTempPath(), "rhino-cli-test-coverage-merge-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory(dir) |> ignore
        dir

    let writeLcovFixture (dir: string) (fileName: string) (content: string) : string =
        let path = Path.Combine(dir, fileName)
        File.WriteAllText(path, content)
        path

    let runMerge () =
        mergedCoverageMap <- lcovFilePaths |> List.map toCoverageMapLcov |> mergeCoverageMaps

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

    [<Given>]
    member _.``two LCOV coverage files with different source files``() =
        let dir = newTempDir ()

        lcovFilePaths <-
            [ writeLcovFixture dir "a.info" "SF:src/a.fs\nDA:1,1\nDA:2,1\nend_of_record\n"
              writeLcovFixture dir "b.info" "SF:src/b.fs\nDA:1,1\nDA:2,0\nend_of_record\n" ]

    [<Given>]
    member _.``two LCOV coverage files with high coverage``() =
        let dir = newTempDir ()

        lcovFilePaths <-
            [ writeLcovFixture dir "a.info" "SF:src/a.fs\nDA:1,1\nDA:2,1\nend_of_record\n"
              writeLcovFixture dir "b.info" "SF:src/b.fs\nDA:1,1\nDA:2,1\nend_of_record\n" ]

    [<Given>]
    member _.``two LCOV coverage files with low coverage``() =
        let dir = newTempDir ()

        lcovFilePaths <-
            [ writeLcovFixture dir "a.info" "SF:src/a.fs\nDA:1,0\nDA:2,0\nend_of_record\n"
              writeLcovFixture dir "b.info" "SF:src/b.fs\nDA:1,0\nDA:2,1\nend_of_record\n" ]

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

    [<When>]
    member _.``the developer runs test-coverage merge with an output file``() =
        runMerge ()
        let dir = Path.GetDirectoryName(List.head lcovFilePaths)
        outputFilePath <- Path.Combine(dir, "merged.info")
        writeLcov outputFilePath mergedCoverageMap
        result <- Some(resultFromCoverageMap mergedCoverageMap 0.0)

    [<When>]
    member _.``the developer runs test-coverage merge with validation at 80% threshold``() =
        runMerge ()
        result <- Some(resultFromCoverageMap mergedCoverageMap 80.0)

    [<When>]
    member _.``the developer runs test-coverage merge with validation at 95% threshold``() =
        runMerge ()
        result <- Some(resultFromCoverageMap mergedCoverageMap 95.0)

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() = Assert.True((theResult ()).Passed)

    [<Then>]
    member _.``the output reports 100% coverage``() = Assert.Equal(100.0, (theResult ()).Pct)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.False((theResult ()).Passed)

    [<Then>]
    member _.``the merged output file exists in LCOV format``() =
        Assert.True(File.Exists(outputFilePath))
        let content = File.ReadAllText(outputFilePath)
        Assert.Contains("SF:", content)
        Assert.Contains("end_of_record", content)

    [<Then>]
    member _.``the excluded files do not affect the diff coverage result``() =
        let r = theResult ()
        Assert.DoesNotContain(r.Files, fun (f: FileResult) -> f.Path = "generated/skip.fs")
        Assert.Equal(100.0, r.Pct)
        Assert.Equal(2, r.Total)

/// Reads one named `Scenario:` block out of a real, frozen feature file
/// under this namespace's `test-coverage/` spec directory (leaving the file
/// itself untouched) and runs it through TickSpec bound only against
/// `TestCoverageSteps` — see `EnvSteps.fs`'s `FeatureRunner` for why this is
/// per-scenario rather than per-file. Parameterized over the feature-file
/// name (rather than the diff-only-hardcoded path this module started with)
/// so this one runner serves both `test-coverage-diff.feature` and
/// `test-coverage-merge.feature`, matching this file's own module doc
/// comment on why one Steps file spans multiple feature files here.
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
                "test-coverage"
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
    /// `featureFileName` (a file directly inside `test-coverage/`), bound
    /// against `TestCoverageSteps`.
    let run (featureFileName: string) (scenarioTitle: string) : unit =
        let featurePath = Path.Combine(featureDir, featureFileName)
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<TestCoverageSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``No changed lines reports 100% coverage`` () =
    FeatureRunner.run "test-coverage-diff.feature" "No changed lines reports 100% coverage"

[<Fact>]
let ``Changed lines with full coverage pass threshold`` () =
    FeatureRunner.run "test-coverage-diff.feature" "Changed lines with full coverage pass threshold"

[<Fact>]
let ``Changed lines with missing coverage fail threshold`` () =
    FeatureRunner.run "test-coverage-diff.feature" "Changed lines with missing coverage fail threshold"

[<Fact>]
let ``Excluded files are not counted in diff coverage`` () =
    FeatureRunner.run "test-coverage-diff.feature" "Excluded files are not counted in diff coverage"

[<Fact>]
let ``Merging two LCOV files produces correct combined coverage`` () =
    FeatureRunner.run "test-coverage-merge.feature" "Merging two LCOV files produces correct combined coverage"

[<Fact>]
let ``Merging with validation passes when coverage meets threshold`` () =
    FeatureRunner.run "test-coverage-merge.feature" "Merging with validation passes when coverage meets threshold"

[<Fact>]
let ``Merging with validation fails when coverage is below threshold`` () =
    FeatureRunner.run "test-coverage-merge.feature" "Merging with validation fails when coverage is below threshold"
