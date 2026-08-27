/// TickSpec step definitions binding `test-coverage-diff.feature`'s 4
/// scenarios, `test-coverage-merge.feature`'s 3 scenarios, and
/// `test-coverage-validate.feature`'s 10 scenarios to
/// `RhinoCli.Application.TestCoverage`'s diff-coverage, merge-coverage, and
/// validate ports [Repo-grounded —
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/test-coverage/test-coverage-diff.feature`,
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/test-coverage/test-coverage-merge.feature`,
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/test-coverage/test-coverage-validate.feature`,
/// `apps/rhino-cli/src/application/testcoverage/diff.rs`,
/// `apps/rhino-cli/src/application/testcoverage/merge.rs`,
/// `apps/rhino-cli/src/application/testcoverage/lcov.rs`,
/// `apps/rhino-cli/src/application/testcoverage/go_coverage.rs`,
/// `apps/rhino-cli/src/application/testcoverage/cobertura.rs`,
/// `apps/rhino-cli/src/application/testcoverage/reporter.rs`,
/// `apps/rhino-cli/src/commands/test_coverage_validate.rs`].
///
/// Follows `EnvValidateSteps.fs`'s per-scenario slicing convention: each
/// xunit `[<Fact>]` below runs exactly one scenario, extracted from the
/// real, frozen feature file. Neither `test-coverage diff` nor
/// `test-coverage merge` has a Rust command wrapper under
/// `apps/rhino-cli/src/commands/` (only `test_coverage_validate.rs` is wired
/// to a CLI verb there) to bind argument shapes against, so — matching
/// `TestCoverage.fs`'s own module doc comment — every diff/merge scenario
/// below calls `computeDiffCoverage`/`toCoverageMapLcov`/
/// `mergeCoverageMaps`/`writeLcov`/`resultFromCoverageMap` directly rather
/// than shelling a real CLI verb. The merge scenarios do write real temp
/// LCOV files to disk (rather than building `CoverageMap` fixtures in memory
/// like the diff scenarios do) because "the merged output file exists in
/// LCOV format" is itself part of what the first merge scenario asserts.
///
/// `test-coverage validate` DOES have a real, wired Rust command
/// (`test_coverage_validate.rs`), but `test-coverage` is not yet in
/// `FSHARP_NAMESPACES` (that flip is later, separate Wave C integration
/// work), so there is still no F# CLI dispatch arm to bind argument shapes
/// against here either — every validate scenario below calls
/// `RhinoCli.Application.TestCoverage.validate` directly with a
/// `ValidateOptions` record built by hand, matching this file's own
/// established precedent rather than parsing an argv string.
module RhinoCli.Tests.Unit.Steps.TestCoverageSteps

open System
open System.IO
open System.Text
open System.Text.Json
open TickSpec
open Xunit
open RhinoCli.Application.TestCoverage

/// One executable line's fixture coverage, used to build the
/// [`CoverageMap`] fixtures below.
let private lineCovered: LineCoverage = { HitCount = 1L; Branches = [] }

let private lineMissed: LineCoverage = { HitCount = 0L; Branches = [] }

let private coverageMapOf (files: (string * (int64 * LineCoverage) list) list) : CoverageMap =
    files |> List.map (fun (path, lines) -> path, Map.ofList lines) |> Map.ofList

/// Builds a Go `cover.out` file body recording `coveredCount` covered lines
/// out of `totalCount` total, one line per `DA`-equivalent block — used by
/// `test-coverage-validate.feature`'s Go-format scenarios. No `go.mod`/source
/// file accompanies it, so [`RhinoCli.Application.TestCoverage.computeGoResult`]'s
/// non-code-line skip never triggers, keeping the arithmetic exact.
let private goCoverOutContent (coveredCount: int) (totalCount: int) : string =
    let sb = StringBuilder()
    sb.Append("mode: set\n") |> ignore

    for i in 1..totalCount do
        let count = if i <= coveredCount then 1 else 0

        sb.Append(sprintf "example.com/proj/foo.go:%d.1,%d.2 1 %d\n" i i count)
        |> ignore

    sb.ToString()

/// Builds one `SF:`/`DA:`/`end_of_record` LCOV section recording
/// `coveredCount` covered lines out of `totalCount` total for `path` — used
/// by `test-coverage-validate.feature`'s LCOV-format scenarios.
let private lcovSectionFor (path: string) (coveredCount: int) (totalCount: int) : string =
    let sb = StringBuilder()
    sb.Append(sprintf "SF:%s\n" path) |> ignore

    for i in 1..totalCount do
        let count = if i <= coveredCount then 1 else 0
        sb.Append(sprintf "DA:%d,%d\n" i count) |> ignore

    sb.Append("end_of_record\n") |> ignore
    sb.ToString()

/// Builds a Cobertura XML report body recording `coveredCount` non-branch
/// covered lines out of `totalCount` total, all in one `<class>` — used by
/// `test-coverage-validate.feature`'s Cobertura-format scenarios.
let private coberturaContent (coveredCount: int) (totalCount: int) : string =
    let lines =
        [ for i in 1..totalCount ->
              let hits = if i <= coveredCount then 1 else 0
              sprintf "<line number=\"%d\" hits=\"%d\" branch=\"false\"/>" i hits ]
        |> String.concat "\n"

    sprintf
        "<?xml version=\"1.0\"?>\n<coverage>\n<packages>\n<package name=\"pkg\">\n<classes>\n<class filename=\"src/foo.py\">\n<lines>\n%s\n</lines>\n</class>\n</classes>\n</package>\n</packages>\n</coverage>\n"
        lines

/// A Cobertura XML report body with a single branch-covered line whose
/// `condition-coverage` reports one of two branches taken — classifies as
/// partial, used by the "partial branches" scenario.
let private coberturaPartialContent: string =
    "<?xml version=\"1.0\"?>\n<coverage>\n<packages>\n<package name=\"pkg\">\n<classes>\n<class filename=\"src/foo.py\">\n<lines>\n<line number=\"10\" hits=\"5\" branch=\"true\" condition-coverage=\"50% (1/2)\"/>\n</lines>\n</class>\n</classes>\n</package>\n</packages>\n</coverage>\n"

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

    // ---- `test-coverage validate` state — see `ValidateOptions`/
    // `ValidateOutcome` in `RhinoCli.Application.TestCoverage` for what each
    // field feeds. ----
    let mutable validateCoverageFile: string = ""
    let mutable validateThreshold: float = 0.0
    let mutable validatePerFile: bool = false
    let mutable validateBelowThreshold: float = 0.0
    let mutable validateExclude: string list = []
    let mutable validateJson: bool = false
    let mutable validateExcludedFileName: string = ""
    let mutable validateOutcome: Result<ValidateOutcome, string> option = None

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

    let runValidate () =
        validateOutcome <-
            Some(
                validate
                    { CoverageFile = validateCoverageFile
                      Threshold = validateThreshold
                      PerFile = validatePerFile
                      BelowThreshold = validateBelowThreshold
                      Exclude = validateExclude
                      Json = validateJson }
            )

    let theValidateOutcome () : Result<ValidateOutcome, string> =
        validateOutcome
        |> Option.defaultWith (fun () -> failwith "no command has been run by a When step")

    let theValidateOutput () : string =
        match theValidateOutcome () with
        | Ok outcome -> outcome.Output
        | Error message -> failwith (sprintf "expected a successful validate outcome, got error: %s" message)

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

    // ---- Given (`test-coverage-validate.feature`) ----

    [<Given>]
    member _.``a Go coverage file recording 90% line coverage``() =
        let dir = newTempDir ()
        validateCoverageFile <- writeLcovFixture dir "cover.out" (goCoverOutContent 9 10)

    [<Given>]
    member _.``a Go coverage file recording 70% line coverage``() =
        let dir = newTempDir ()
        validateCoverageFile <- writeLcovFixture dir "cover.out" (goCoverOutContent 7 10)

    [<Given>]
    member _.``an LCOV coverage file recording 90% line coverage``() =
        let dir = newTempDir ()
        validateCoverageFile <- writeLcovFixture dir "coverage.info" (lcovSectionFor "src/foo.fs" 9 10)

    [<Given>]
    member _.``a Go coverage file recording 85% line coverage``() =
        let dir = newTempDir ()
        validateCoverageFile <- writeLcovFixture dir "cover.out" (goCoverOutContent 17 20)

    [<Given>]
    member _.``an LCOV coverage file with multiple source files``() =
        let dir = newTempDir ()
        let content = lcovSectionFor "src/a.fs" 10 10 + lcovSectionFor "src/b.fs" 8 10
        validateCoverageFile <- writeLcovFixture dir "coverage.info" content
        validateExcludedFileName <- "src/b.fs"

    [<Given>]
    member _.``a Cobertura XML coverage file recording 90% line coverage``() =
        let dir = newTempDir ()
        validateCoverageFile <- writeLcovFixture dir "cobertura.xml" (coberturaContent 9 10)

    [<Given>]
    member _.``a Cobertura XML coverage file with partial branch coverage``() =
        let dir = newTempDir ()
        validateCoverageFile <- writeLcovFixture dir "cobertura.xml" coberturaPartialContent

    [<Given>]
    member _.``no coverage file exists at the specified path``() =
        let dir = newTempDir ()
        validateCoverageFile <- Path.Combine(dir, "missing-coverage.info")

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

    // ---- When (`test-coverage-validate.feature`) ----

    [<When>]
    member _.``the developer runs test-coverage validate with an 85% threshold``() =
        validateThreshold <- 85.0
        validatePerFile <- false
        validateBelowThreshold <- 0.0
        validateExclude <- []
        validateJson <- false
        runValidate ()

    [<When>]
    member _.``the developer runs test-coverage validate with an 85% threshold requesting JSON output``() =
        validateThreshold <- 85.0
        validatePerFile <- false
        validateBelowThreshold <- 0.0
        validateExclude <- []
        validateJson <- true
        runValidate ()

    [<When>]
    member _.``the developer runs test-coverage validate with an 85% threshold and per-file flag``() =
        validateThreshold <- 85.0
        validatePerFile <- true
        validateBelowThreshold <- 0.0
        validateExclude <- []
        validateJson <- false
        runValidate ()

    [<When>]
    member _.``the developer runs test-coverage validate with exclusion of a source file``() =
        validateThreshold <- 0.0
        validatePerFile <- true
        validateBelowThreshold <- 0.0
        validateExclude <- [ validateExcludedFileName ]
        validateJson <- false
        runValidate ()

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() =
        match validateOutcome with
        | Some(Ok outcome) -> Assert.True(outcome.Passed)
        | Some(Error message) -> failwith (sprintf "expected test-coverage validate to succeed, got error: %s" message)
        | None -> Assert.True((theResult ()).Passed)

    [<Then>]
    member _.``the output reports 100% coverage``() = Assert.Equal(100.0, (theResult ()).Pct)

    [<Then>]
    member _.``the command exits with a failure code``() =
        match validateOutcome with
        | Some(Ok outcome) -> Assert.False(outcome.Passed)
        | Some(Error _) -> ()
        | None -> Assert.False((theResult ()).Passed)

    [<Then>]
    member _.``the output reports the measured coverage percentage``() =
        let output = theValidateOutput ()
        Assert.Contains("Line coverage:", output)

    [<Then>]
    member _.``the output indicates the coverage passes the threshold``() =
        Assert.Contains("PASS", theValidateOutput ())

    [<Then>]
    member _.``the output indicates the coverage fails the threshold``() =
        Assert.Contains("FAIL", theValidateOutput ())

    [<Then>]
    member _.``the output is valid JSON``() =
        use _doc = JsonDocument.Parse(theValidateOutput ())
        ()

    [<Then>]
    member _.``the JSON includes the coverage percentage and pass/fail status``() =
        use doc = JsonDocument.Parse(theValidateOutput ())
        let root = doc.RootElement
        let mutable pctElement = Unchecked.defaultof<JsonElement>
        let mutable passedElement = Unchecked.defaultof<JsonElement>
        Assert.True(root.TryGetProperty("pct", &pctElement))
        Assert.True(root.TryGetProperty("passed", &passedElement))

    [<Then>]
    member _.``the output contains per-file coverage breakdown``() =
        Assert.Contains("Per-file coverage", theValidateOutput ())

    [<Then>]
    member _.``the output does not contain the excluded file``() =
        Assert.DoesNotContain(validateExcludedFileName, theValidateOutput ())

    [<Then>]
    member _.``the output describes the missing file``() =
        match theValidateOutcome () with
        | Error message -> Assert.Contains("not found", message)
        | Ok _ -> failwith "expected test-coverage validate to fail for a missing coverage file"

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
/// so this one runner serves `test-coverage-diff.feature`,
/// `test-coverage-merge.feature`, and `test-coverage-validate.feature` alike,
/// matching this file's own module doc comment on why one Steps file spans
/// multiple feature files here.
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

[<Fact>]
let ``A Go coverage file above the threshold reports success`` () =
    FeatureRunner.run "test-coverage-validate.feature" "A Go coverage file above the threshold reports success"

[<Fact>]
let ``A Go coverage file below the threshold reports failure`` () =
    FeatureRunner.run "test-coverage-validate.feature" "A Go coverage file below the threshold reports failure"

[<Fact>]
let ``An LCOV file above the threshold reports success`` () =
    FeatureRunner.run "test-coverage-validate.feature" "An LCOV file above the threshold reports success"

[<Fact>]
let ``Coverage at exactly the threshold passes`` () =
    FeatureRunner.run "test-coverage-validate.feature" "Coverage at exactly the threshold passes"

[<Fact>]
let ``JSON output includes structured coverage metrics`` () =
    FeatureRunner.run "test-coverage-validate.feature" "JSON output includes structured coverage metrics"

[<Fact>]
let ``Per-file flag shows individual file coverage`` () =
    FeatureRunner.run "test-coverage-validate.feature" "Per-file flag shows individual file coverage"

[<Fact>]
let ``A Cobertura XML file above the threshold reports success`` () =
    FeatureRunner.run "test-coverage-validate.feature" "A Cobertura XML file above the threshold reports success"

[<Fact>]
let ``A Cobertura XML file with partial branches classifies correctly`` () =
    FeatureRunner.run "test-coverage-validate.feature" "A Cobertura XML file with partial branches classifies correctly"

[<Fact>]
let ``Exclude flag removes files from coverage calculation`` () =
    FeatureRunner.run "test-coverage-validate.feature" "Exclude flag removes files from coverage calculation"

[<Fact>]
let ``A non-existent coverage file reports an error`` () =
    FeatureRunner.run "test-coverage-validate.feature" "A non-existent coverage file reports an error"
