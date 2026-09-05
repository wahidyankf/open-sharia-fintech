module RhinoCli.Tests.Unit.Steps.TestCoverageSteps

open System
open System.IO
open System.Text
open System.Text.Json
open RhinoCli.Application.TestCoverage
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/test-coverage/test-coverage-validate.feature" ]

let private goCoverOutContent (coveredCount: int) (totalCount: int) : string =
    let text = StringBuilder("mode: set\n")

    for lineNumber in 1..totalCount do
        let hitCount = if lineNumber <= coveredCount then 1 else 0

        text.Append($"example.com/proj/foo.go:{lineNumber}.1,{lineNumber}.2 1 {hitCount}\n")
        |> ignore

    text.ToString()

let private lcovSectionFor (path: string) (coveredCount: int) (totalCount: int) : string =
    let text = StringBuilder($"SF:{path}\n")

    for lineNumber in 1..totalCount do
        let hitCount = if lineNumber <= coveredCount then 1 else 0
        text.Append($"DA:{lineNumber},{hitCount}\n") |> ignore

    text.Append("end_of_record\n") |> ignore
    text.ToString()

let private coberturaContent (coveredCount: int) (totalCount: int) : string =
    let lines =
        [ for lineNumber in 1..totalCount do
              let hitCount = if lineNumber <= coveredCount then 1 else 0
              $"<line number=\"{lineNumber}\" hits=\"{hitCount}\" branch=\"false\"/>" ]
        |> String.concat "\n"

    $"<?xml version=\"1.0\"?>\n<coverage><packages><package name=\"pkg\"><classes><class filename=\"src/foo.py\"><lines>{lines}</lines></class></classes></package></packages></coverage>"

let private coberturaPartialContent =
    "<?xml version=\"1.0\"?>\n<coverage><packages><package name=\"pkg\"><classes><class filename=\"src/foo.py\"><lines><line number=\"10\" hits=\"5\" branch=\"true\" condition-coverage=\"50% (1/2)\"/></lines></class></classes></package></packages></coverage>"

let private linesOf (content: string) : string array =
    content.Replace("\r\n", "\n", StringComparison.Ordinal).Replace('\r', '\n').Split('\n')

type TestCoverageSteps() =
    let mutable virtualFiles: Map<string, string> = Map.empty
    let mutable coverageFile = "/coverage/cover.out"
    let mutable excludedFileName = ""
    let mutable outcome: Result<ValidateOutcome, string> option = None

    let addFile path content =
        virtualFiles <- Map.add path content virtualFiles

    let fileAccess: FileAccess =
        { Exists = fun path -> Map.containsKey path virtualFiles
          ReadAllLines = fun path -> virtualFiles |> Map.find path |> linesOf }

    let run options =
        outcome <- Some(validateWith fileAccess options)

    let baseOptions threshold =
        { CoverageFile = coverageFile
          Threshold = threshold
          PerFile = false
          BelowThreshold = 0.0
          Exclude = []
          Json = false
          Markdown = false }

    let requiredOutcome () =
        outcome
        |> Option.defaultWith (fun () -> failwith "the When step did not invoke validation")

    let requiredOutput () =
        match requiredOutcome () with
        | Ok value -> value.Output
        | Error message -> failwith $"expected a coverage report, got: {message}"

    [<Given>]
    member _.``a Go coverage file recording 90% line coverage``() =
        coverageFile <- "/coverage/cover.out"
        addFile coverageFile (goCoverOutContent 9 10)

    [<Given>]
    member _.``a Go coverage file recording 70% line coverage``() =
        coverageFile <- "/coverage/cover.out"
        addFile coverageFile (goCoverOutContent 7 10)

    [<Given>]
    member _.``an LCOV coverage file recording 90% line coverage``() =
        coverageFile <- "/coverage/coverage.info"
        addFile coverageFile (lcovSectionFor "src/foo.fs" 9 10)

    [<Given>]
    member _.``a Go coverage file recording 85% line coverage``() =
        coverageFile <- "/coverage/cover.out"
        addFile coverageFile (goCoverOutContent 17 20)

    [<Given>]
    member _.``an LCOV coverage file with multiple source files``() =
        coverageFile <- "/coverage/coverage.info"
        excludedFileName <- "src/b.fs"
        addFile coverageFile (lcovSectionFor "src/a.fs" 10 10 + lcovSectionFor excludedFileName 8 10)

    [<Given>]
    member _.``a Cobertura XML coverage file recording 90% line coverage``() =
        coverageFile <- "/coverage/cobertura.xml"
        addFile coverageFile (coberturaContent 9 10)

    [<Given>]
    member _.``a Cobertura XML coverage file with partial branch coverage``() =
        coverageFile <- "/coverage/cobertura.xml"
        addFile coverageFile coberturaPartialContent

    [<Given>]
    member _.``no coverage file exists at the specified path``() =
        coverageFile <- "/coverage/missing-coverage.info"

    [<When>]
    member _.``the developer runs test-coverage validate with an 85% threshold``() = run (baseOptions 85.0)

    [<When>]
    member _.``the developer runs test-coverage validate with an 85% threshold requesting JSON output``() =
        run { baseOptions 85.0 with Json = true }

    [<When>]
    member _.``the developer runs test-coverage validate with an 85% threshold and per-file flag``() =
        run { baseOptions 85.0 with PerFile = true }

    [<When>]
    member _.``the developer runs test-coverage validate with exclusion of a source file``() =
        run
            { baseOptions 0.0 with
                PerFile = true
                Exclude = [ excludedFileName ] }

    [<Then>]
    member _.``the command exits successfully``() =
        match requiredOutcome () with
        | Ok value -> Assert.True(value.Passed)
        | Error message -> failwith $"expected successful validation, got: {message}"

    [<Then>]
    member _.``the command exits with a failure code``() =
        match requiredOutcome () with
        | Ok value -> Assert.False(value.Passed)
        | Error _ -> ()

    [<Then>]
    member _.``the output reports the measured coverage percentage``() =
        Assert.Contains("Line coverage: 90.00%", requiredOutput ())

    [<Then>]
    member _.``the output indicates the coverage passes the threshold``() =
        Assert.Contains("PASS", requiredOutput ())

    [<Then>]
    member _.``the output indicates the coverage fails the threshold``() =
        Assert.Contains("FAIL", requiredOutput ())

    [<Then>]
    member _.``the output is valid JSON``() =
        use _document = JsonDocument.Parse(requiredOutput ())
        ()

    [<Then>]
    member _.``the JSON includes the coverage percentage and pass/fail status``() =
        use document = JsonDocument.Parse(requiredOutput ())
        let root = document.RootElement
        let mutable percentage = Unchecked.defaultof<JsonElement>
        let mutable passed = Unchecked.defaultof<JsonElement>
        Assert.True(root.TryGetProperty("pct", &percentage))
        Assert.True(root.TryGetProperty("passed", &passed))
        Assert.Equal(90.0, percentage.GetDouble())
        Assert.True(passed.GetBoolean())

    [<Then>]
    member _.``the output contains per-file coverage breakdown``() =
        let output = requiredOutput ()
        Assert.Contains("Per-file coverage (2 files)", output)
        Assert.Contains("src/a.fs", output)
        Assert.Contains("src/b.fs", output)

    [<Then>]
    member _.``the output does not contain the excluded file``() =
        Assert.DoesNotContain(excludedFileName, requiredOutput ())

    [<Then>]
    member _.``the output describes the missing file``() =
        match requiredOutcome () with
        | Error message -> Assert.Contains("not found", message)
        | Ok _ -> failwith "expected missing coverage input to fail"

module private FeatureRunner =

    let private readFeature () =
        let assembly = typeof<TestCoverageSteps>.Assembly

        let resourceName =
            assembly.GetManifestResourceNames()
            |> Array.find (fun name -> name.EndsWith("test-coverage-validate.feature", StringComparison.Ordinal))

        use stream = assembly.GetManifestResourceStream(resourceName)
        use reader = new StreamReader(stream)
        reader.ReadToEnd().Replace("\r\n", "\n", StringComparison.Ordinal).Split('\n')

    let private extractScenario (featureLines: string array) (scenarioTitle: string) : string array =
        let featureLine =
            featureLines
            |> Array.find (fun line -> line.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let scenarioHeader = $"Scenario: {scenarioTitle}"

        let startIndex =
            featureLines |> Array.findIndex (fun line -> line.Trim() = scenarioHeader)

        let endIndex =
            featureLines
            |> Array.skip (startIndex + 1)
            |> Array.tryFindIndex (fun line ->
                let trimmed = line.Trim()

                trimmed.StartsWith("Scenario:", StringComparison.Ordinal)
                || trimmed.StartsWith("Scenario Outline:", StringComparison.Ordinal)
                || trimmed.StartsWith("@", StringComparison.Ordinal))
            |> Option.map (fun relativeIndex -> startIndex + relativeIndex + 1)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIndex .. endIndex - 1]

    let run scenarioTitle =
        let source = readFeature ()
        let snippet = extractScenario source scenarioTitle
        let definitions = StepDefinitions([| typeof<TestCoverageSteps> |])
        let feature = definitions.GenerateFeature("test-coverage-validate.feature", snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``A Go coverage file above the threshold reports success`` () =
    FeatureRunner.run "A Go coverage file above the threshold reports success"

[<Fact>]
let ``A Go coverage file below the threshold reports failure`` () =
    FeatureRunner.run "A Go coverage file below the threshold reports failure"

[<Fact>]
let ``An LCOV file above the threshold reports success`` () =
    FeatureRunner.run "An LCOV file above the threshold reports success"

[<Fact>]
let ``Coverage at exactly the threshold passes`` () =
    FeatureRunner.run "Coverage at exactly the threshold passes"

[<Fact>]
let ``JSON output includes structured coverage metrics`` () =
    FeatureRunner.run "JSON output includes structured coverage metrics"

[<Fact>]
let ``Per-file flag shows individual file coverage`` () =
    FeatureRunner.run "Per-file flag shows individual file coverage"

[<Fact>]
let ``A Cobertura XML file above the threshold reports success`` () =
    FeatureRunner.run "A Cobertura XML file above the threshold reports success"

[<Fact>]
let ``A Cobertura XML file with partial branches classifies correctly`` () =
    FeatureRunner.run "A Cobertura XML file with partial branches classifies correctly"

[<Fact>]
let ``Exclude flag removes files from coverage calculation`` () =
    FeatureRunner.run "Exclude flag removes files from coverage calculation"

[<Fact>]
let ``A non-existent coverage file reports an error`` () =
    FeatureRunner.run "A non-existent coverage file reports an error"
