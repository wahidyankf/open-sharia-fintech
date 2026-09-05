module RhinoCli.Tests.E2E.Steps.TestCoverageProcessSteps

open System
open System.Diagnostics
open System.IO
open System.Text
open System.Text.Json
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/test-coverage/test-coverage-validate.feature" ]

let private repositoryRoot =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "..", ".."))

let private executable =
    Path.Combine(repositoryRoot, "apps", "rhino-cli", "src", "dist", "rhino-cli-fsharp")

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

type TestCoverageProcessSteps() =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-test-coverage-e2e-" + Guid.NewGuid().ToString("N"))

    let mutable coverageFile = ""
    let mutable excludedFileName = ""
    let mutable exitCode = -1
    let mutable output = ""

    let write (name: string) (content: string) =
        let path = Path.Combine(root, name)
        File.WriteAllText(path, content)
        coverageFile <- path

    let run extraArguments =
        let startInfo =
            ProcessStartInfo(
                FileName = executable,
                WorkingDirectory = repositoryRoot,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            )

        [ "test-coverage"; "validate"; coverageFile; "85" ] @ extraArguments
        |> List.iter startInfo.ArgumentList.Add

        use commandProcess = Process.Start(startInfo)
        let standardOutput = commandProcess.StandardOutput.ReadToEnd()
        let standardError = commandProcess.StandardError.ReadToEnd()
        commandProcess.WaitForExit()
        exitCode <- commandProcess.ExitCode
        output <- standardOutput + "\n" + standardError

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
    member _.``the developer runs test-coverage validate with an 85% threshold``() = run []

    [<When>]
    member _.``the developer runs test-coverage validate with an 85% threshold requesting JSON output``() =
        run [ "--output"; "json" ]

    [<When>]
    member _.``the developer runs test-coverage validate with an 85% threshold and per-file flag``() =
        run [ "--per-file" ]

    [<When>]
    member _.``the developer runs test-coverage validate with exclusion of a source file``() =
        run [ "--per-file"; "--exclude"; excludedFileName ]

    [<Then>]
    member _.``the command exits successfully``() = Assert.Equal(0, exitCode)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.NotEqual(0, exitCode)

    [<Then>]
    member _.``the output reports the measured coverage percentage``() = Assert.Contains("90.00%", output)

    [<Then>]
    member _.``the output indicates the coverage passes the threshold``() = Assert.Contains("PASS", output)

    [<Then>]
    member _.``the output indicates the coverage fails the threshold``() = Assert.Contains("FAIL", output)

    [<Then>]
    member _.``the output is valid JSON``() =
        use _document = JsonDocument.Parse(output.Trim())
        ()

    [<Then>]
    member _.``the JSON includes the coverage percentage and pass/fail status``() =
        use document = JsonDocument.Parse(output.Trim())
        Assert.Equal(90.0, document.RootElement.GetProperty("pct").GetDouble())
        Assert.True(document.RootElement.GetProperty("passed").GetBoolean())

    [<Then>]
    member _.``the output contains per-file coverage breakdown``() =
        Assert.Contains("Per-file coverage (2 files)", output)

    [<Then>]
    member _.``the output does not contain the excluded file``() =
        Assert.DoesNotContain(excludedFileName, output)

    [<Then>]
    member _.``the output describes the missing file``() = Assert.Contains("not found", output)

    [<AfterScenario>]
    member _.Cleanup() =
        if Directory.Exists(root) then
            Directory.Delete(root, true)

module private FeatureRunner =

    let private featurePath =
        Path.Combine(
            repositoryRoot,
            "specs",
            "apps",
            "rhino",
            "cli",
            "behaviours",
            "test-coverage",
            "test-coverage-validate.feature"
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
            StepDefinitions([| typeof<TestCoverageProcessSteps> |]).GenerateFeature(featurePath, snippet)

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
let ``coverage validation crosses the published process`` title = FeatureRunner.run title
