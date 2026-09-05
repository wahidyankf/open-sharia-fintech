module RhinoCli.Tests.E2E.Steps.EnvInitProcessSteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/env/env-init.feature" ]

open System
open System.Diagnostics
open System.IO
open TickSpec
open Xunit

let private repositoryRoot =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "..", ".."))

let private executable =
    Path.Combine(repositoryRoot, "apps", "rhino-cli", "src", "dist", "rhino-cli-fsharp")

type EnvInitProcessSteps() =
    let fixture =
        Path.Combine(Path.GetTempPath(), "rhino-cli-env-init-e2e-" + Guid.NewGuid().ToString("N"))

    let root = Path.Combine(fixture, "repository")
    let mutable output = ""
    let mutable exitCode = 0

    do
        Directory.CreateDirectory root |> ignore

        let info =
            ProcessStartInfo(FileName = "git", WorkingDirectory = root, UseShellExecute = false)

        info.ArgumentList.Add("init")
        info.ArgumentList.Add("-q")
        use proc = Process.Start info
        proc.WaitForExit()
        Assert.Equal(0, proc.ExitCode)

    let write (relative: string) (content: string) =
        let path = Path.Combine(root, relative)
        Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
        File.WriteAllText(path, content)

    let invoke args =
        let info =
            ProcessStartInfo(
                FileName = executable,
                WorkingDirectory = root,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            )

        [ "env"; "init" ] @ args |> List.iter info.ArgumentList.Add
        use proc = Process.Start info
        output <- proc.StandardOutput.ReadToEnd() + proc.StandardError.ReadToEnd()
        proc.WaitForExit()
        exitCode <- proc.ExitCode

    let local (app: string) =
        Path.Combine(root, "infra", "dev", app, ".env.local")

    [<Given>]
    member _.``.env.example files exist in infra/dev but no .env.local files``() =
        write "infra/dev/api/.env.example" "api=1"
        write "infra/dev/web/.env.example" "web=1"

    [<Given>]
    member _.``.env.example files exist in infra/dev and some .env.local files already exist``() =
        write "infra/dev/api/.env.example" "api=1"
        write "infra/dev/web/.env.example" "web=1"
        write "infra/dev/api/.env.local" "existing=1"

    [<Given>]
    member _.``no .env.example files exist in infra/dev``() =
        Directory.CreateDirectory(Path.Combine(root, "infra", "dev")) |> ignore

    [<When>]
    member _.``the developer runs env init``() = invoke []

    [<When>]
    member _.``the developer runs env init with the force flag``() = invoke [ "--force" ]

    [<Then>]
    member _.``the command exits successfully``() = Assert.Equal(0, exitCode)

    [<Then>]
    member _.``.env.local files are created from each .env.example``() =
        Assert.True(File.Exists(local "api"))
        Assert.True(File.Exists(local "web"))

    [<Then>]
    member _.``no bare .env file is created``() =
        Assert.False(File.Exists(Path.Combine(root, "infra/dev/api/.env")))
        Assert.False(File.Exists(Path.Combine(root, "infra/dev/web/.env")))

    [<Then>]
    member _.``the output lists each created file``() =
        Assert.Contains("infra/dev/api/.env.local", output)
        Assert.Contains("infra/dev/web/.env.local", output)

    [<Then>]
    member _.``existing .env.local files are not overwritten``() =
        Assert.Equal("existing=1", File.ReadAllText(local "api"))

    [<Then>]
    member _.``the output shows skipped files``() = Assert.Contains("Skipped:", output)

    [<Then>]
    member _.``all .env.local files are created or overwritten``() =
        Assert.Equal("api=1", File.ReadAllText(local "api"))
        Assert.Equal("web=1", File.ReadAllText(local "web"))

    [<Then>]
    member _.``the output reports zero files created``() =
        Assert.Contains("Summary: 0 created", output)

    [<AfterScenario>]
    member _.Cleanup() =
        if Directory.Exists fixture then
            Directory.Delete(fixture, true)

module private FeatureRunner =
    let run title =
        let path =
            Path.Combine(repositoryRoot, "specs/apps/rhino/cli/behaviours/env/env-init.feature")

        let lines = File.ReadAllLines path

        let featureLine =
            lines |> Array.find (fun line -> line.TrimStart().StartsWith("Feature:"))

        let startIndex =
            lines |> Array.findIndex (fun line -> line.Trim() = "Scenario: " + title)

        let endIndex =
            lines
            |> Array.skip (startIndex + 1)
            |> Array.tryFindIndex (fun line ->
                line.TrimStart().StartsWith("Scenario:") || line.TrimStart().StartsWith("@"))
            |> Option.map (fun offset -> startIndex + 1 + offset)
            |> Option.defaultValue lines.Length

        let definitions = StepDefinitions([| typeof<EnvInitProcessSteps> |])

        let feature =
            definitions.GenerateFeature(path, Array.append [| featureLine; "" |] lines.[startIndex .. endIndex - 1])

        (Seq.exactlyOne feature.Scenarios).Action.Invoke()

[<Theory>]
[<InlineData("Bootstrap env files from examples")>]
[<InlineData("Skip existing env files")>]
[<InlineData("Force overwrite existing env files")>]
[<InlineData("No env.example files found")>]
let ``env init crosses the published CLI boundary`` title = FeatureRunner.run title
