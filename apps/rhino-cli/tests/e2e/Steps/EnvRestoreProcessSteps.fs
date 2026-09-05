module RhinoCli.Tests.E2E.Steps.EnvRestoreProcessSteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/env/env-restore.feature" ]

open System
open System.Diagnostics
open System.IO
open System.Text.Json
open TickSpec
open Xunit

let private repositoryRoot =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "..", ".."))

let private executable =
    Path.Combine(repositoryRoot, "apps", "rhino-cli", "src", "dist", "rhino-cli-fsharp")

type EnvRestoreProcessSteps() =
    let fixture =
        Path.Combine(Path.GetTempPath(), "rhino-cli-env-restore-e2e-" + Guid.NewGuid().ToString("N"))

    let mutable root = Path.Combine(fixture, "repository")
    let backup = Path.Combine(fixture, "backup")
    let mutable source = backup
    let mutable expected: string list = []
    let mutable output = ""
    let mutable exitCode = 0
    let mutable answer: string option = None

    let initRoot name =
        root <- Path.Combine(fixture, name)
        Directory.CreateDirectory root |> ignore

        let info =
            ProcessStartInfo(FileName = "git", WorkingDirectory = root, UseShellExecute = false)

        info.ArgumentList.Add("init")
        info.ArgumentList.Add("-q")
        use proc = Process.Start info
        proc.WaitForExit()
        Assert.Equal(0, proc.ExitCode)

    do initRoot "repository"

    let write (baseDir: string) (relative: string) (content: string) =
        let path = Path.Combine(baseDir, relative)
        Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
        File.WriteAllText(path, content)

    let invoke commandArgs =
        let info =
            ProcessStartInfo(
                FileName = executable,
                WorkingDirectory = root,
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                RedirectStandardInput = true
            )

        [ "env"; "restore"; "--dir"; source ] @ commandArgs
        |> List.iter info.ArgumentList.Add

        use proc = Process.Start info

        answer
        |> Option.iter (fun value ->
            proc.StandardInput.WriteLine(value)
            proc.StandardInput.Close())

        output <- proc.StandardOutput.ReadToEnd() + proc.StandardError.ReadToEnd()
        proc.WaitForExit()
        exitCode <- proc.ExitCode

    let restored relative =
        File.Exists(Path.Combine(root, relative))

    [<Given>]
    member _.``a backup directory containing previously backed-up .env files from the repository``() =
        expected <- [ ".env"; "apps/web/.env"; "apps/api/.env" ]
        expected |> List.iter (fun path -> write backup path "backup=1")

    [<Given>]
    member _.``a backup directory at /tmp/my-env-backup containing a backed-up .env file``() =
        write backup ".env" "backup=1"

    [<Given>]
    member _.``no directory exists at /nonexistent``() =
        source <- Path.Combine(fixture, "nonexistent")

    [<Given>]
    member _.``a backup directory containing a previously backed-up .env file``() = write backup ".env" "backup=1"

    [<Given>]
    member _.``a backup directory containing a backed-up .env file and a README.md file``() =
        write backup ".env" "backup=1"
        write backup "README.md" "ignore"

    [<Given>]
    member _.``a backup directory containing no .env files``() =
        Directory.CreateDirectory backup |> ignore

    [<Given>]
    member _.``a backup directory containing a .env file backed up under a feature-branch namespace``() =
        write backup "feature-branch/.env" "backup=1"

    [<Given>]
    member _.``the repository already contains a .env file at the original path``() = write root ".env" "existing=1"

    [<Given>]
    member _.``the repository does not contain a .env file at the original path``() =
        Assert.False(File.Exists(Path.Combine(root, ".env")))

    [<Given>]
    member _.``a backup directory containing a .env file and a .claude/settings.local.json file``() =
        write backup ".env" "backup=1"
        write backup ".claude/settings.local.json" "{}"

    [<Given>]
    member _.``a backup directory containing a secrets.json file``() = write backup "secrets.json" "{}"

    [<Given>]
    member _.``a backup directory containing a cert.pem file``() = write backup "cert.pem" "certificate"

    [<Given>]
    member _.``a backup directory containing a .secrets/notes.md file``() =
        write backup ".secrets/notes.md" "notes"

    [<Given>]
    member _.``a backup directory containing a .env file and a secrets.json file``() =
        write backup ".env" "backup=1"
        write backup "secrets.json" "{}"

    [<When>]
    member _.``the developer runs rhino-cli env restore``() = invoke []

    [<When>]
    member _.``the developer runs rhino-cli env restore with --dir /tmp/my-env-backup``() = invoke []

    [<When>]
    member _.``the developer runs rhino-cli env restore with --dir /nonexistent``() = invoke []

    [<When>]
    member _.``the developer runs rhino-cli env restore with --output json``() = invoke [ "-o"; "json" ]

    [<When>]
    member _.``the developer runs rhino-cli env restore with --worktree-aware from a worktree named "(.*)"``
        (name: string)
        =
        initRoot name
        invoke [ "--worktree-aware" ]

    [<When>]
    member _.``the developer runs rhino-cli env restore and confirms the overwrite``() =
        answer <- Some "y"
        invoke []

    [<When>]
    member _.``the developer runs rhino-cli env restore and declines the overwrite``() =
        answer <- Some "n"
        invoke []

    [<When>]
    member _.``the developer runs rhino-cli env restore with --force``() = invoke [ "--force" ]

    [<When>]
    member _.``the developer runs rhino-cli env restore with --include-config and --force``() =
        invoke [ "--include-config"; "--force" ]

    [<When>]
    member _.``the developer runs rhino-cli env restore with --dry-run``() = invoke [ "--dry-run" ]

    [<Then>]
    member _.``the command exits successfully``() = Assert.Equal(0, exitCode)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.NotEqual(0, exitCode)

    [<Then>]
    member _.``each .env file is copied back to its original path in the repository``() =
        expected |> List.iter (fun path -> Assert.True(restored path, path))

    [<Then>]
    member _.``the output lists each restored file``() =
        expected |> List.iter (fun path -> Assert.Contains(path, output))

    [<Then>]
    member _.``the .env file is copied back to its original path in the repository``() = Assert.True(restored ".env")

    [<Then>]
    member _.``the output reports that the directory does not exist``() =
        Assert.Contains("does not exist", output)

    [<Then>]
    member _.``the output is valid JSON``() =
        use _doc = JsonDocument.Parse(output)
        ()

    [<Then>]
    member _.``the JSON includes the direction, backup directory, list of files, copied count, and skipped count``() =
        [ "direction"; "dir"; "files"; "copied"; "skipped" ]
        |> List.iter (fun key -> Assert.Contains(key, output))

    [<Then>]
    member _.``README.md is not restored``() = Assert.False(restored "README.md")

    [<Then>]
    member _.``the output reports that zero files were restored``() = Assert.Contains("0 file(s)", output)

    [<Then>]
    member _.``the .env file is read from the feature-branch namespace inside the backup directory``() =
        Assert.Contains("feature-branch", output)

    [<Then>]
    member _.``the .env file is copied back to its original path in the worktree``() = Assert.True(restored ".env")

    [<Then>]
    member _.``the .env file in the repository is overwritten with the backup``() =
        Assert.Equal("backup=1", File.ReadAllText(Path.Combine(root, ".env")))

    [<Then>]
    member _.``the output reports that restore was cancelled``() =
        Assert.Contains("cancelled", output, StringComparison.OrdinalIgnoreCase)

    [<Then>]
    member _.``the existing repository file is unchanged``() =
        Assert.Equal("existing=1", File.ReadAllText(Path.Combine(root, ".env")))

    [<Then>]
    member _.``the .env file in the repository is overwritten without prompting``() =
        Assert.Equal("backup=1", File.ReadAllText(Path.Combine(root, ".env")))
        Assert.DoesNotContain("Overwrite?", output)

    [<Then>]
    member _.``no confirmation prompt is shown``() =
        Assert.DoesNotContain("Overwrite?", output)

    [<Then>]
    member _.``the .env file is restored to the repository``() = Assert.True(restored ".env")

    [<Then>]
    member _.``the .claude/settings.local.json is restored to the repository preserving its relative path``() =
        Assert.True(restored ".claude/settings.local.json")

    [<Then>]
    member _.``the .claude/settings.local.json is not restored to the repository``() =
        Assert.False(restored ".claude/settings.local.json")

    [<Then>]
    member _.``secrets.json is copied back to the repository``() = Assert.True(restored "secrets.json")

    [<Then>]
    member _.``cert.pem is copied back to the repository``() = Assert.True(restored "cert.pem")

    [<Then>]
    member _.``.secrets/notes.md is copied back to the repository preserving its relative path``() =
        Assert.True(restored ".secrets/notes.md")

    [<Then>]
    member _.``no files are written to the repository``() =
        [ "secrets.json"; "cert.pem"; ".secrets/notes.md" ]
        |> List.iter (fun path -> Assert.False(restored path))

    [<Then>]
    member _.``the output lists the files that would be restored``() =
        Assert.Contains("WOULD", output)
        Assert.Contains("secrets.json", output)

    [<AfterScenario>]
    member _.Cleanup() =
        if Directory.Exists fixture then
            Directory.Delete(fixture, true)

module private FeatureRunner =
    let run title =
        let path =
            Path.Combine(repositoryRoot, "specs/apps/rhino/cli/behaviours/env/env-restore.feature")

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

        let definitions = StepDefinitions([| typeof<EnvRestoreProcessSteps> |])

        let feature =
            definitions.GenerateFeature(path, Array.append [| featureLine; "" |] lines.[startIndex .. endIndex - 1])

        (Seq.exactlyOne feature.Scenarios).Action.Invoke()

[<Theory>]
[<InlineData("Restore copies files back from backup")>]
[<InlineData("Restore with custom source directory")>]
[<InlineData("Restore fails when backup directory does not exist")>]
[<InlineData("JSON output for restore")>]
[<InlineData("Restore only restores .env files")>]
[<InlineData("Restore with zero .env files in backup")>]
[<InlineData("Worktree-aware restore reads from correct namespace")>]
[<InlineData("Restore prompts when destination files already exist")>]
[<InlineData("Restore aborts when user declines overwrite")>]
[<InlineData("Restore with --force skips confirmation")>]
[<InlineData("Restore proceeds without prompt when no conflicts exist")>]
[<InlineData("Restore includes config files with --include-config")>]
[<InlineData("Restore without --include-config ignores config files in backup")>]
[<InlineData("Restore recovers common secret file patterns")>]
[<InlineData("Restore recovers a mix of .env and secret files together")>]
[<InlineData("Dry-run restore previews without writing files")>]
let ``restore crosses the published CLI boundary`` title = FeatureRunner.run title
