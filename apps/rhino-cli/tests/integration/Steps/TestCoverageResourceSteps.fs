module RhinoCli.Tests.Integration.Steps.TestCoverageResourceSteps

open System
open System.IO
open System.Text
open System.Text.Json
open RhinoCli.Application.TestCoverage
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/test-coverage/test-coverage-validate.feature" ]

let private goContent covered total =
    let text = StringBuilder("mode: set\n")

    for lineNumber in 1..total do
        let hitCount = if lineNumber <= covered then 1 else 0

        text.Append($"example.com/proj/foo.go:{lineNumber}.1,{lineNumber}.2 1 {hitCount}\n")
        |> ignore

    text.ToString()

let private lcovSection path covered total =
    let text = StringBuilder($"SF:{path}\n")

    for lineNumber in 1..total do
        let hitCount = if lineNumber <= covered then 1 else 0
        text.Append($"DA:{lineNumber},{hitCount}\n") |> ignore

    text.Append("end_of_record\n") |> ignore
    text.ToString()

let private coberturaContent covered total =
    let lines =
        [ for lineNumber in 1..total do
              let hitCount = if lineNumber <= covered then 1 else 0
              $"<line number=\"{lineNumber}\" hits=\"{hitCount}\" branch=\"false\"/>" ]
        |> String.concat "\n"

    $"<?xml version=\"1.0\"?>\n<coverage><packages><package name=\"pkg\"><classes><class filename=\"src/foo.py\"><lines>{lines}</lines></class></classes></package></packages></coverage>"

let private partialCobertura =
    "<?xml version=\"1.0\"?>\n<coverage><packages><package name=\"pkg\"><classes><class filename=\"src/foo.py\"><lines><line number=\"10\" hits=\"5\" branch=\"true\" condition-coverage=\"50% (1/2)\"/></lines></class></classes></package></packages></coverage>"

type TestCoverageResourceSteps() =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-test-coverage-integration-" + Guid.NewGuid().ToString("N"))

    let mutable coverageFile = ""
    let mutable excludedFileName = ""
    let mutable outcome: Result<ValidateOutcome, string> option = None

    let write (name: string) (content: string) =
        let path = Path.Combine(root, name)
        File.WriteAllText(path, content)
        coverageFile <- path

    let options threshold =
        { CoverageFile = coverageFile
          Threshold = threshold
          PerFile = false
          BelowThreshold = 0.0
          Exclude = []
          Json = false
          Markdown = false }

    let run opts = outcome <- Some(validate opts)

    let requiredOutcome () =
        outcome
        |> Option.defaultWith (fun () -> failwith "the When step did not invoke validation")

    let requiredOutput () =
        match requiredOutcome () with
        | Ok value -> value.Output
        | Error message -> failwith $"expected a coverage report, got: {message}"

    do Directory.CreateDirectory(root) |> ignore

    [<Given>]
    member _.``a Go coverage file recording 90% line coverage``() = write "cover.out" (goContent 9 10)

    [<Given>]
    member _.``a Go coverage file recording 70% line coverage``() = write "cover.out" (goContent 7 10)

    [<Given>]
    member _.``an LCOV coverage file recording 90% line coverage``() =
        write "coverage.info" (lcovSection "src/foo.fs" 9 10)

    [<Given>]
    member _.``a Go coverage file recording 85% line coverage``() = write "cover.out" (goContent 17 20)

    [<Given>]
    member _.``an LCOV coverage file with multiple source files``() =
        excludedFileName <- "src/b.fs"
        write "coverage.info" (lcovSection "src/a.fs" 10 10 + lcovSection excludedFileName 8 10)

    [<Given>]
    member _.``a Cobertura XML coverage file recording 90% line coverage``() =
        write "cobertura.xml" (coberturaContent 9 10)

    [<Given>]
    member _.``a Cobertura XML coverage file with partial branch coverage``() = write "cobertura.xml" partialCobertura

    [<Given>]
    member _.``no coverage file exists at the specified path``() =
        coverageFile <- Path.Combine(root, "missing-coverage.info")

    [<When>]
    member _.``the developer runs test-coverage validate with an 85% threshold``() = run (options 85.0)

    [<When>]
    member _.``the developer runs test-coverage validate with an 85% threshold requesting JSON output``() =
        run { options 85.0 with Json = true }

    [<When>]
    member _.``the developer runs test-coverage validate with an 85% threshold and per-file flag``() =
        run { options 85.0 with PerFile = true }

    [<When>]
    member _.``the developer runs test-coverage validate with exclusion of a source file``() =
        run
            { options 0.0 with
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
        let rootElement = document.RootElement
        Assert.Equal(90.0, rootElement.GetProperty("pct").GetDouble())
        Assert.True(rootElement.GetProperty("passed").GetBoolean())

    [<Then>]
    member _.``the output contains per-file coverage breakdown``() =
        Assert.Contains("Per-file coverage (2 files)", requiredOutput ())

    [<Then>]
    member _.``the output does not contain the excluded file``() =
        Assert.DoesNotContain(excludedFileName, requiredOutput ())

    [<Then>]
    member _.``the output describes the missing file``() =
        match requiredOutcome () with
        | Error message -> Assert.Contains("not found", message)
        | Ok _ -> failwith "expected missing coverage input to fail"

    [<AfterScenario>]
    member _.Cleanup() =
        if Directory.Exists(root) then
            Directory.Delete(root, true)

module private FeatureRunner =

    let private featurePath =
        Path.GetFullPath(
            Path.Combine(
                __SOURCE_DIRECTORY__,
                "..",
                "..",
                "..",
                "..",
                "..",
                "specs",
                "apps",
                "rhino",
                "cli",
                "behaviours",
                "test-coverage",
                "test-coverage-validate.feature"
            )
        )

    let run title =
        let lines = File.ReadAllLines(featurePath)

        let featureLine =
            lines |> Array.find (fun line -> line.TrimStart().StartsWith("Feature:"))

        let startIndex =
            lines |> Array.findIndex (fun line -> line.Trim() = "Scenario: " + title)

        let endIndex =
            lines
            |> Array.skip (startIndex + 1)
            |> Array.tryFindIndex (fun line -> line.TrimStart().StartsWith("Scenario:"))
            |> Option.map (fun offset -> startIndex + offset + 1)
            |> Option.defaultValue lines.Length

        let snippet = Array.append [| featureLine; "" |] lines.[startIndex .. endIndex - 1]

        let feature =
            StepDefinitions([| typeof<TestCoverageResourceSteps> |]).GenerateFeature(featurePath, snippet)

        (Seq.exactlyOne feature.Scenarios).Action.Invoke()

[<Theory>]
[<InlineData("A Go coverage file above the threshold reports success")>]
[<InlineData("A Go coverage file below the threshold reports failure")>]
[<InlineData("An LCOV file above the threshold reports success")>]
[<InlineData("Coverage at exactly the threshold passes")>]
[<InlineData("JSON output includes structured coverage metrics")>]
[<InlineData("Per-file flag shows individual file coverage")>]
[<InlineData("A Cobertura XML file above the threshold reports success")>]
[<InlineData("A Cobertura XML file with partial branches classifies correctly")>]
[<InlineData("Exclude flag removes files from coverage calculation")>]
[<InlineData("A non-existent coverage file reports an error")>]
let ``coverage validation uses real local files`` title = FeatureRunner.run title
