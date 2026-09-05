module RhinoCli.Tests.E2E.Steps.ContractsProcessSteps

open System
open System.Diagnostics
open System.IO
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/contracts/contracts-dart-scaffold.feature" ]

let private repoRoot =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "..", ".."))

let private executable =
    Path.Combine(repoRoot, "apps", "rhino-cli", "src", "dist", "rhino-cli-fsharp")

type ContractsProcessSteps() =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-contracts-e2e-" + Guid.NewGuid().ToString("N"))

    let mutable exitCode = -1
    let mutable standardOutput = ""
    let mutable standardError = ""

    let write (relative: string) (contents: string) =
        let path = Path.Combine(root, relative)
        Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
        File.WriteAllText(path, contents)

    let read (relative: string) =
        File.ReadAllText(Path.Combine(root, relative))

    let initialiseRepository () =
        let info =
            ProcessStartInfo(
                FileName = "git",
                WorkingDirectory = root,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            )

        [ "init"; "-q"; "-b"; "main" ] |> List.iter info.ArgumentList.Add
        info.Environment.["GIT_CONFIG_GLOBAL"] <- "/dev/null"
        info.Environment.["GIT_CONFIG_SYSTEM"] <- "/dev/null"
        use proc = Process.Start info
        proc.StandardOutput.ReadToEnd() |> ignore
        let error = proc.StandardError.ReadToEnd()
        proc.WaitForExit()

        if proc.ExitCode <> 0 then
            failwithf "git init failed: %s" error

    do
        Directory.CreateDirectory root |> ignore
        initialiseRepository ()

    [<Given>]
    member _.``a generated-contracts directory with model Dart files``() =
        write "lib/model/user.dart" "// user"
        write "lib/model/account.dart" "// account"

    [<Given>]
    member _.``a generated-contracts directory with no model files``() =
        let models = Path.Combine(root, "lib", "model")
        Directory.CreateDirectory(models) |> ignore
        Assert.Empty(Directory.GetFiles(models, "*.dart"))

    [<Given>]
    member _.``an existing generated-contracts directory with old scaffold files``() =
        write "pubspec.yaml" "stale"
        write "lib/crud_contracts.dart" "stale"

    [<When>]
    member _.``the developer runs specs scaffold dart on the directory``() =
        let info =
            ProcessStartInfo(
                FileName = executable,
                WorkingDirectory = root,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            )

        [ "specs"; "scaffold"; "dart"; "--dir"; root ]
        |> List.iter info.ArgumentList.Add

        use proc = Process.Start info
        standardOutput <- proc.StandardOutput.ReadToEnd()
        standardError <- proc.StandardError.ReadToEnd()
        proc.WaitForExit()
        exitCode <- proc.ExitCode

    [<Then>]
    member _.``the command exits successfully``() =
        Assert.True((exitCode = 0), $"exit {exitCode}\nstdout:\n{standardOutput}\nstderr:\n{standardError}")

    [<Then>]
    member _.``pubspec.yaml is created with correct content``() =
        Assert.Contains("name: crud_contracts", read "pubspec.yaml")

    [<Then>]
    member _.``pubspec.yaml is created``() =
        Assert.True(File.Exists(Path.Combine(root, "pubspec.yaml")))

    [<Then>]
    member _.``the barrel library is created with part directives for each model``() =
        let body = read "lib/crud_contracts.dart" in
        Assert.Contains("part 'model/account.dart';", body)
        Assert.Contains("part 'model/user.dart';", body)

    [<Then>]
    member _.``the barrel library is created without part directives``() =
        Assert.DoesNotContain("part 'model/", read "lib/crud_contracts.dart")

    [<Then>]
    member _.``the existing files are overwritten with fresh scaffold``() =
        Assert.Contains("name: crud_contracts", read "pubspec.yaml")
        Assert.Contains("library openapi.api", read "lib/crud_contracts.dart")

    [<AfterScenario>]
    member _.Cleanup() =
        if Directory.Exists root then
            Directory.Delete(root, true)

module private FeatureRunner =
    let path =
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
                "contracts",
                "contracts-dart-scaffold.feature"
            )
        )

    let run title =
        let lines = File.ReadAllLines path

        let featureLine =
            lines |> Array.find (fun line -> line.TrimStart().StartsWith("Feature:"))

        let start =
            lines |> Array.findIndex (fun line -> line.Trim() = "Scenario: " + title)

        let finish =
            lines
            |> Array.skip (start + 1)
            |> Array.tryFindIndex (fun line -> line.TrimStart().StartsWith("Scenario:"))
            |> Option.map (fun offset -> start + 1 + offset)
            |> Option.defaultValue lines.Length

        let feature =
            StepDefinitions([| typeof<ContractsProcessSteps> |])
                .GenerateFeature(path, Array.append [| featureLine; "" |] lines.[start .. finish - 1])

        (Seq.exactlyOne feature.Scenarios).Action.Invoke()

[<Theory>]
[<InlineData("Normal scaffold with model files")>]
[<InlineData("Scaffold with no model files")>]
[<InlineData("Scaffold overwrites existing files")>]
let ``Dart scaffold crosses the published process`` title = FeatureRunner.run title
