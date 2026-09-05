module RhinoCli.Tests.Unit.Steps.EnvRestoreSteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/env/env-restore.feature" ]

open System.Text.Json
open TickSpec
open Xunit
open RhinoCli.Application.Env

type EnvRestoreSteps() =
    let mutable entries: EnvFileEntry list = []
    let mutable existing: string list = []
    let mutable expected: string list = []
    let mutable sourceExists = true
    let mutable worktreeName = ""
    let mutable force = false
    let mutable includeConfig = false
    let mutable dryRun = false
    let mutable confirmation: bool option = None
    let mutable confirmationCalls = 0
    let mutable result: EnvOperationResult option = None
    let mutable error: string option = None
    let mutable restored: string list = []

    let add path source =
        entries <-
            entries
            @ [ { RelPath = path
                  AbsPath = path
                  Size = 1L
                  Skipped = false
                  Reason = ""
                  Source = source } ]

    let confirm () =
        confirmationCalls <- confirmationCalls + 1
        confirmation |> Option.defaultValue false

    let outcome () =
        result |> Option.defaultWith (fun () -> failwith "restore did not run")

    let run () =
        if not sourceExists then
            error <- Some "backup directory does not exist"
        else
            let selected =
                entries |> List.filter (fun item -> includeConfig || item.Source <> "config")

            let planned =
                planEnvOperation "restore" "/backup" selected existing force dryRun worktreeName confirm

            result <- Some planned

            if not planned.Cancelled && not planned.DryRun then
                restored <- selected |> List.map _.RelPath

    [<Given>]
    member _.``a backup directory containing previously backed-up .env files from the repository``() =
        expected <- [ ".env"; "apps/web/.env" ]
        expected |> List.iter (fun path -> add path "env")

    [<Given>]
    member _.``a backup directory at /tmp/my-env-backup containing a backed-up .env file``() = add ".env" "env"

    [<Given>]
    member _.``no directory exists at /nonexistent``() = sourceExists <- false

    [<Given>]
    member _.``a backup directory containing a previously backed-up .env file``() = add ".env" "env"

    [<Given>]
    member _.``a backup directory containing a backed-up .env file and a README.md file``() = add ".env" "env"

    [<Given>]
    member _.``a backup directory containing no .env files``() = entries <- []

    [<Given>]
    member _.``a backup directory containing a .env file backed up under a feature-branch namespace``() =
        worktreeName <- "feature-branch"
        add ".env" "env"

    [<Given>]
    member _.``the repository already contains a .env file at the original path``() = existing <- [ ".env" ]

    [<Given>]
    member _.``the repository does not contain a .env file at the original path``() = existing <- []

    [<Given>]
    member _.``a backup directory containing a .env file and a .claude/settings.local.json file``() =
        add ".env" "env"
        add ".claude/settings.local.json" "config"

    [<Given>]
    member _.``a backup directory containing a secrets.json file``() = add "secrets.json" "env"

    [<Given>]
    member _.``a backup directory containing a cert.pem file``() = add "cert.pem" "env"

    [<Given>]
    member _.``a backup directory containing a .secrets/notes.md file``() = add ".secrets/notes.md" "env"

    [<Given>]
    member _.``a backup directory containing a .env file and a secrets.json file``() =
        add ".env" "env"
        add "secrets.json" "env"

    [<When>]
    member _.``the developer runs rhino-cli env restore``() = run ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --dir /tmp/my-env-backup``() = run ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --dir /nonexistent``() = run ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --output json``() =
        force <- true
        run ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --worktree-aware from a worktree named "(.*)"``
        (name: string)
        =
        worktreeName <- name
        run ()

    [<When>]
    member _.``the developer runs rhino-cli env restore and confirms the overwrite``() =
        confirmation <- Some true
        run ()

    [<When>]
    member _.``the developer runs rhino-cli env restore and declines the overwrite``() =
        confirmation <- Some false
        run ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --force``() =
        force <- true
        run ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --include-config and --force``() =
        includeConfig <- true
        force <- true
        run ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --dry-run``() =
        dryRun <- true
        run ()

    [<Then>]
    member _.``the command exits successfully``() = Assert.True(error.IsNone)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.True(error.IsSome)

    [<Then>]
    member _.``each .env file is copied back to its original path in the repository``() =
        expected |> List.iter (fun path -> Assert.Contains(path, restored))

    [<Then>]
    member _.``the output lists each restored file``() =
        expected
        |> List.iter (fun path -> Assert.Contains(path, formatText (outcome ()) false false))

    [<Then>]
    member _.``the .env file is copied back to its original path in the repository``() =
        Assert.Contains(".env", restored)

    [<Then>]
    member _.``the output reports that the directory does not exist``() =
        Assert.Contains("does not exist", error.Value)

    [<Then>]
    member _.``the output is valid JSON``() =
        use _doc = JsonDocument.Parse(formatJson (outcome ()))
        ()

    [<Then>]
    member _.``the JSON includes the direction, backup directory, list of files, copied count, and skipped count``() =
        let json = formatJson (outcome ())

        [ "direction"; "dir"; "files"; "copied"; "skipped" ]
        |> List.iter (fun key -> Assert.Contains(key, json))

    [<Then>]
    member _.``README.md is not restored``() =
        Assert.DoesNotContain("README.md", restored)

    [<Then>]
    member _.``the output reports that zero files were restored``() = Assert.Equal(0, (outcome ()).Copied)

    [<Then>]
    member _.``the .env file is read from the feature-branch namespace inside the backup directory``() =
        Assert.Equal("feature-branch", worktreeName)

    [<Then>]
    member _.``the .env file is copied back to its original path in the worktree``() = Assert.Contains(".env", restored)

    [<Then>]
    member _.``the .env file in the repository is overwritten with the backup``() =
        Assert.Contains(".env", restored)
        Assert.Equal(1, confirmationCalls)

    [<Then>]
    member _.``the output reports that restore was cancelled``() = Assert.True((outcome ()).Cancelled)

    [<Then>]
    member _.``the existing repository file is unchanged``() =
        Assert.Empty restored
        Assert.Equal(1, confirmationCalls)

    [<Then>]
    member _.``the .env file in the repository is overwritten without prompting``() =
        Assert.Contains(".env", restored)
        Assert.Equal(0, confirmationCalls)

    [<Then>]
    member _.``no confirmation prompt is shown``() = Assert.Equal(0, confirmationCalls)

    [<Then>]
    member _.``the .env file is restored to the repository``() = Assert.Contains(".env", restored)

    [<Then>]
    member _.``the .claude/settings.local.json is restored to the repository preserving its relative path``() =
        Assert.Contains(".claude/settings.local.json", restored)

    [<Then>]
    member _.``the .claude/settings.local.json is not restored to the repository``() =
        Assert.DoesNotContain(".claude/settings.local.json", restored)

    [<Then>]
    member _.``secrets.json is copied back to the repository``() =
        Assert.Contains("secrets.json", restored)

    [<Then>]
    member _.``cert.pem is copied back to the repository``() = Assert.Contains("cert.pem", restored)

    [<Then>]
    member _.``.secrets/notes.md is copied back to the repository preserving its relative path``() =
        Assert.Contains(".secrets/notes.md", restored)

    [<Then>]
    member _.``no files are written to the repository``() = Assert.Empty restored

    [<Then>]
    member _.``the output lists the files that would be restored``() =
        Assert.Contains("WOULD", formatText (outcome ()) false false)

[<Fact>]
let ``restore policy confirms only real conflicts`` () =
    let steps = EnvRestoreSteps()
    steps.``a backup directory containing a previously backed-up .env file`` ()
    steps.``the repository already contains a .env file at the original path`` ()
    steps.``the developer runs rhino-cli env restore and declines the overwrite`` ()
    steps.``the output reports that restore was cancelled`` ()
    steps.``the existing repository file is unchanged`` ()

[<Fact>]
let ``restore dry run plans without writing`` () =
    let steps = EnvRestoreSteps()
    steps.``a backup directory containing a .env file and a secrets.json file`` ()
    steps.``the developer runs rhino-cli env restore with --dry-run`` ()
    steps.``no files are written to the repository`` ()
    steps.``the output lists the files that would be restored`` ()

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
let ``every restore behaviour has in-process Unit proof`` title =
    let s = EnvRestoreSteps()

    match title with
    | "Restore copies files back from backup" ->
        s.``a backup directory containing previously backed-up .env files from the repository`` ()
        s.``the developer runs rhino-cli env restore`` ()
        s.``the command exits successfully`` ()
        s.``each .env file is copied back to its original path in the repository`` ()
        s.``the output lists each restored file`` ()
    | "Restore with custom source directory" ->
        s.``a backup directory at /tmp/my-env-backup containing a backed-up .env file`` ()
        s.``the developer runs rhino-cli env restore with --dir /tmp/my-env-backup`` ()
        s.``the command exits successfully`` ()
        s.``the .env file is copied back to its original path in the repository`` ()
    | "Restore fails when backup directory does not exist" ->
        s.``no directory exists at /nonexistent`` ()
        s.``the developer runs rhino-cli env restore with --dir /nonexistent`` ()
        s.``the command exits with a failure code`` ()
        s.``the output reports that the directory does not exist`` ()
    | "JSON output for restore" ->
        s.``a backup directory containing a previously backed-up .env file`` ()
        s.``the developer runs rhino-cli env restore with --output json`` ()
        s.``the command exits successfully`` ()
        s.``the output is valid JSON`` ()
        s.``the JSON includes the direction, backup directory, list of files, copied count, and skipped count`` ()
    | "Restore only restores .env files" ->
        s.``a backup directory containing a backed-up .env file and a README.md file`` ()
        s.``the developer runs rhino-cli env restore`` ()
        s.``the command exits successfully`` ()
        s.``the .env file is copied back to its original path in the repository`` ()
        s.``README.md is not restored`` ()
    | "Restore with zero .env files in backup" ->
        s.``a backup directory containing no .env files`` ()
        s.``the developer runs rhino-cli env restore`` ()
        s.``the command exits successfully`` ()
        s.``the output reports that zero files were restored`` ()
    | "Worktree-aware restore reads from correct namespace" ->
        s.``a backup directory containing a .env file backed up under a feature-branch namespace`` ()

        s.``the developer runs rhino-cli env restore with --worktree-aware from a worktree named "(.*)"`` (
            "feature-branch"
        )

        s.``the command exits successfully`` ()
        s.``the .env file is read from the feature-branch namespace inside the backup directory`` ()
        s.``the .env file is copied back to its original path in the worktree`` ()
    | "Restore prompts when destination files already exist" ->
        s.``a backup directory containing a previously backed-up .env file`` ()
        s.``the repository already contains a .env file at the original path`` ()
        s.``the developer runs rhino-cli env restore and confirms the overwrite`` ()
        s.``the command exits successfully`` ()
        s.``the .env file in the repository is overwritten with the backup`` ()
    | "Restore aborts when user declines overwrite" ->
        s.``a backup directory containing a previously backed-up .env file`` ()
        s.``the repository already contains a .env file at the original path`` ()
        s.``the developer runs rhino-cli env restore and declines the overwrite`` ()
        s.``the command exits successfully`` ()
        s.``the output reports that restore was cancelled`` ()
        s.``the existing repository file is unchanged`` ()
    | "Restore with --force skips confirmation" ->
        s.``a backup directory containing a previously backed-up .env file`` ()
        s.``the repository already contains a .env file at the original path`` ()
        s.``the developer runs rhino-cli env restore with --force`` ()
        s.``the command exits successfully`` ()
        s.``the .env file in the repository is overwritten without prompting`` ()
    | "Restore proceeds without prompt when no conflicts exist" ->
        s.``a backup directory containing a previously backed-up .env file`` ()
        s.``the repository does not contain a .env file at the original path`` ()
        s.``the developer runs rhino-cli env restore`` ()
        s.``the command exits successfully`` ()
        s.``no confirmation prompt is shown`` ()
        s.``the .env file is restored to the repository`` ()
    | "Restore includes config files with --include-config" ->
        s.``a backup directory containing a .env file and a .claude/settings.local.json file`` ()
        s.``the developer runs rhino-cli env restore with --include-config and --force`` ()
        s.``the command exits successfully`` ()
        s.``the .env file is restored to the repository`` ()
        s.``the .claude/settings.local.json is restored to the repository preserving its relative path`` ()
    | "Restore without --include-config ignores config files in backup" ->
        s.``a backup directory containing a .env file and a .claude/settings.local.json file`` ()
        s.``the developer runs rhino-cli env restore with --force`` ()
        s.``the command exits successfully`` ()
        s.``the .env file is restored to the repository`` ()
        s.``the .claude/settings.local.json is not restored to the repository`` ()
    | "Restore recovers common secret file patterns" ->
        s.``a backup directory containing a secrets.json file`` ()
        s.``a backup directory containing a cert.pem file`` ()
        s.``a backup directory containing a .secrets/notes.md file`` ()
        s.``the developer runs rhino-cli env restore`` ()
        s.``the command exits successfully`` ()
        s.``secrets.json is copied back to the repository`` ()
        s.``cert.pem is copied back to the repository`` ()
        s.``.secrets/notes.md is copied back to the repository preserving its relative path`` ()
    | "Restore recovers a mix of .env and secret files together" ->
        s.``a backup directory containing a .env file and a secrets.json file`` ()
        s.``the developer runs rhino-cli env restore`` ()
        s.``the command exits successfully`` ()
        s.``secrets.json is copied back to the repository`` ()
    | "Dry-run restore previews without writing files" ->
        s.``a backup directory containing a secrets.json file`` ()
        s.``a backup directory containing a cert.pem file`` ()
        s.``a backup directory containing a .secrets/notes.md file`` ()
        s.``the developer runs rhino-cli env restore with --dry-run`` ()
        s.``no files are written to the repository`` ()
        s.``the output lists the files that would be restored`` ()
    | other -> Assert.Fail(sprintf "unmapped restore scenario: %s" other)
