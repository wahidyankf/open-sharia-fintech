/// Integration proof for the staged-env guard against a real local Git index.
module RhinoCli.Tests.Integration.Steps.EnvStagedGuardResourceSteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/specs/env-staged-guard.feature" ]

open System
open System.Diagnostics
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Env

type EnvStagedGuardResourceSteps() =
    let repoRoot =
        Path.Combine(Path.GetTempPath(), "rhino-env-index-" + Guid.NewGuid().ToString("N"))

    let mutable offending: string list option = None

    let git arguments =
        let startInfo =
            ProcessStartInfo(
                "git",
                WorkingDirectory = repoRoot,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            )

        arguments |> List.iter startInfo.ArgumentList.Add
        use childProcess = Process.Start startInfo
        let stdout = childProcess.StandardOutput.ReadToEnd()
        let stderr = childProcess.StandardError.ReadToEnd()
        childProcess.WaitForExit()
        Assert.True(childProcess.ExitCode = 0, sprintf "git %s failed: %s" (String.concat " " arguments) stderr)
        stdout

    let stage (path: string) =
        Directory.CreateDirectory repoRoot |> ignore
        git [ "init"; "--quiet" ] |> ignore

        let absolute =
            Path.Combine(repoRoot, path.Replace('/', Path.DirectorySeparatorChar))

        Directory.CreateDirectory(Path.GetDirectoryName absolute) |> ignore
        File.WriteAllText(absolute, "fixture=true\n")
        git [ "add"; "--"; path ] |> ignore

    let runGuard () =
        let staged =
            (git [ "diff"; "--cached"; "--name-only"; "--diff-filter=ACMR" ])
                .Split('\n', StringSplitOptions.RemoveEmptyEntries)
            |> List.ofArray

        offending <- Some(checkStagedFiles staged)

    let result () =
        offending |> Option.defaultWith (fun () -> failwith "staged guard did not run")

    [<Given>]
    member _.``a real \.env file is staged for commit``() = stage ".env"

    [<Given>]
    member _.``only \.env\.example is staged for commit``() = stage ".env.example"

    [<Given>]
    member _.``a git index with "(.*)" staged``(file: string) = stage file

    [<When>]
    member _.``the pre-commit hook runs rhino-cli env staged-guard validate``() = runGuard ()

    [<When>]
    member _.``"rhino-cli env staged-guard validate" runs``() = runGuard ()

    [<Then>]
    member _.``it exits non-zero and names the offending file``() = Assert.Contains(".env", result ())

    [<Then>]
    member _.``the commit is aborted``() = Assert.NotEmpty(result ())

    [<Then>]
    member _.``it exits zero and does not block the commit``() = Assert.Empty(result ())

    [<Then>]
    member _.``the command exits non-zero``() = Assert.NotEmpty(result ())

    [<Then>]
    member _.``the output names "(.*)" as offending``(file: string) = Assert.Contains(file, result ())

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
                "specs",
                "env-staged-guard.feature"
            )
        )

    let private extractScenario (lines: string[]) title =
        let featureLine =
            lines
            |> Array.find (fun line -> line.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let startIndex =
            lines
            |> Array.findIndex (fun line ->
                let trimmed = line.Trim()

                trimmed = sprintf "Scenario: %s" title
                || trimmed = sprintf "Scenario Outline: %s" title)

        let endIndex =
            lines
            |> Array.skip (startIndex + 1)
            |> Array.tryFindIndex (fun line ->
                let trimmed = line.Trim()

                trimmed.StartsWith("Scenario:", StringComparison.Ordinal)
                || trimmed.StartsWith("Scenario Outline:", StringComparison.Ordinal))
            |> Option.map (fun relative -> startIndex + 1 + relative)
            |> Option.defaultValue lines.Length

        Array.append [| featureLine; "" |] lines.[startIndex .. endIndex - 1]

    let run title =
        let definitions = StepDefinitions([| typeof<EnvStagedGuardResourceSteps> |])

        let feature =
            definitions.GenerateFeature(featurePath, extractScenario (File.ReadAllLines featurePath) title)

        feature.Scenarios |> Seq.iter (fun scenario -> scenario.Action.Invoke())

[<Theory>]
[<InlineData("Committing a real .env file is rejected")>]
[<InlineData("Staging .env.example is allowed")>]
[<InlineData("Staging any real env file is rejected at commit time")>]
let ``staged env guard reads a real isolated Git index`` title = FeatureRunner.run title
