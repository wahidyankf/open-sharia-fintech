/// TickSpec step definitions binding `env-restore.feature`'s 16 scenarios to
/// `RhinoCli.Application.Env`'s `restore` port [Repo-grounded —
/// `specs/apps/rhino/cli/behaviors/env/env-restore.feature`,
/// `apps/rhino-cli/src/application/env/backup.rs`,
/// `apps/rhino-cli/src/commands/env_restore.rs`].
///
/// Follows `EnvSteps.fs`'s per-scenario slicing convention: each xunit
/// `[<Fact>]` below runs exactly one scenario, extracted from the real,
/// frozen feature file rather than a duplicated/rewritten copy of its
/// wording. Kept as its own file (rather than added to `EnvSteps.fs`) since
/// `env-restore.feature` is its own PR-sized slice of the `env` namespace,
/// same as `env-init.feature` was.
///
/// Two scenarios in the feature file spell a literal absolute path
/// (`/tmp/my-env-backup`, `/nonexistent`) in their Given/When wording. Rather
/// than actually touching those host paths (non-hermetic, and unsafe under
/// parallel test runs), the step bodies below satisfy the same natural-
/// language meaning using this file's own managed temp-directory fixtures —
/// the literal step text still matches the frozen feature file verbatim.
module RhinoCli.Tests.Unit.Steps.EnvRestoreSteps

open System
open System.IO
open System.Text.Json
open TickSpec
open Xunit
open RhinoCli.Application.Env

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type EnvRestoreSteps() =
    let mutable repoRoot: string option = None
    let mutable backupDir: string option = None
    let mutable expectedEnvRelPaths: string list = []
    let mutable worktreeAware = false
    let mutable worktreeName: string option = None
    let mutable forceFlag = false
    let mutable includeConfigFlag = false
    let mutable dryRunFlag = false
    let mutable confirmChoice: bool option = None
    let mutable confirmCallCount = 0
    let mutable opResult: Result<EnvOperationResult, string> option = None
    let mutable ownedDirs: string list = []

    let newTempDir (prefix: string) : string =
        let dir =
            Path.Combine(Path.GetTempPath(), "rhino-cli-env-restore-" + prefix + "-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory(dir) |> ignore
        ownedDirs <- dir :: ownedDirs
        dir

    let writeFile (root: string) (relativePath: string) (content: string) =
        let full = Path.Combine(root, relativePath)
        Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
        File.WriteAllText(full, content)

    let root () : string =
        match repoRoot with
        | Some dir -> dir
        | None -> failwith "no repository root has been prepared by a Given step"

    /// Reuses the repository root when a prior `Given`/`When` already created
    /// one, otherwise lazily creates a fresh one — unlike `backup`'s
    /// `EnvSteps.fs`, most `restore` scenarios never mention the destination
    /// repository explicitly at all, so it is only ever established lazily.
    let ensureRoot () : string =
        match repoRoot with
        | Some dir -> dir
        | None ->
            let dir = newTempDir "repo"
            repoRoot <- Some dir
            dir

    let ensureBackupDir () : string =
        match backupDir with
        | Some dir -> dir
        | None ->
            let dir = newTempDir "backup"
            backupDir <- Some dir
            dir

    let outcome () : EnvOperationResult =
        match opResult with
        | Some(Ok r) -> r
        | Some(Error message) -> failwith (sprintf "expected a successful restore, got error: %s" message)
        | None -> failwith "no command has been run by a When step"

    let confirm () : bool =
        confirmCallCount <- confirmCallCount + 1

        match confirmChoice with
        | Some v -> v
        | None -> failwith "confirm callback invoked but no confirm/decline choice was set by a When step"

    let runRestore () =
        let repo = ensureRoot ()
        let dest = ensureBackupDir ()

        let opts: EnvOptions =
            { RepoRoot = repo
              BackupDir = dest
              SkipDirs = []
              MaxSize = DefaultMaxSize
              WorktreeAware = worktreeAware
              WorktreeName = worktreeName |> Option.defaultValue ""
              Force = forceFlag
              IncludeConfig = includeConfigFlag
              DryRun = dryRunFlag }

        opResult <- Some(restore opts confirm)

    // ---- Given ----

    [<Given>]
    member _.``a backup directory containing previously backed-up .env files from the repository``() =
        let dir = ensureBackupDir ()
        writeFile dir ".env" "root=1"
        writeFile dir "apps/web/.env" "web=1"
        writeFile dir "apps/api/.env" "api=1"
        expectedEnvRelPaths <- [ ".env"; "apps/web/.env"; "apps/api/.env" ]

    [<Given>]
    member _.``a backup directory at /tmp/my-env-backup containing a backed-up .env file``() =
        let dir = ensureBackupDir ()
        writeFile dir ".env" "k=v"

    [<Given>]
    member _.``no directory exists at /nonexistent``() =
        let parent = newTempDir "missing-parent"
        backupDir <- Some(Path.Combine(parent, "nonexistent"))

    [<Given>]
    member _.``a backup directory containing a previously backed-up .env file``() =
        let dir = ensureBackupDir ()
        writeFile dir ".env" "k=v"

    [<Given>]
    member _.``a backup directory containing a backed-up .env file and a README.md file``() =
        let dir = ensureBackupDir ()
        writeFile dir ".env" "k=v"
        writeFile dir "README.md" "not a secret"

    [<Given>]
    member _.``a backup directory containing no .env files``() = ensureBackupDir () |> ignore

    [<Given>]
    member _.``a backup directory containing a .env file backed up under a feature-branch namespace``() =
        let dir = ensureBackupDir ()
        writeFile dir "feature-branch/.env" "k=v"

    [<Given>]
    member _.``the repository already contains a .env file at the original path``() =
        let dir = ensureRoot ()
        writeFile dir ".env" "existing=1"

    [<Given>]
    member _.``the repository does not contain a .env file at the original path``() = ensureRoot () |> ignore

    [<Given>]
    member _.``a backup directory containing a .env file and a .claude/settings.local.json file``() =
        let dir = ensureBackupDir ()
        writeFile dir ".env" "k=v"
        writeFile dir ".claude/settings.local.json" "{}"

    [<Given>]
    member _.``a backup directory containing a secrets.json file``() =
        let dir = ensureBackupDir ()
        writeFile dir "secrets.json" "{\"key\":\"val\"}"

    [<Given>]
    member _.``a backup directory containing a cert.pem file``() =
        let dir = ensureBackupDir ()
        writeFile dir "cert.pem" "-----BEGIN CERTIFICATE-----"

    [<Given>]
    member _.``a backup directory containing a .secrets/notes.md file``() =
        let dir = ensureBackupDir ()
        writeFile dir ".secrets/notes.md" "secret notes"

    [<Given>]
    member _.``a backup directory containing a .env file and a secrets.json file``() =
        let dir = ensureBackupDir ()
        writeFile dir ".env" "k=v"
        writeFile dir "secrets.json" "{\"key\":\"val\"}"

    // ---- When ----

    [<When>]
    member _.``the developer runs rhino-cli env restore``() = runRestore ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --dir /tmp/my-env-backup``() = runRestore ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --dir /nonexistent``() = runRestore ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --output json``() = runRestore ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --worktree-aware from a worktree named "(.*)"``
        (name: string)
        =
        worktreeAware <- true
        worktreeName <- Some name
        runRestore ()

    [<When>]
    member _.``the developer runs rhino-cli env restore and confirms the overwrite``() =
        confirmChoice <- Some true
        runRestore ()

    [<When>]
    member _.``the developer runs rhino-cli env restore and declines the overwrite``() =
        confirmChoice <- Some false
        runRestore ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --force``() =
        forceFlag <- true
        runRestore ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --include-config and --force``() =
        forceFlag <- true
        includeConfigFlag <- true
        runRestore ()

    [<When>]
    member _.``the developer runs rhino-cli env restore with --dry-run``() =
        dryRunFlag <- true
        runRestore ()

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() =
        match opResult with
        | Some(Ok _) -> ()
        | Some(Error message) -> Assert.Fail(sprintf "expected success, got error: %s" message)
        | None -> Assert.Fail("no command has been run by a When step")

    [<Then>]
    member _.``the command exits with a failure code``() =
        match opResult with
        | Some(Error _) -> ()
        | Some(Ok _) -> Assert.Fail("expected a failure code, got success")
        | None -> Assert.Fail("no command has been run by a When step")

    [<Then>]
    member _.``each .env file is copied back to its original path in the repository``() =
        for relPath in expectedEnvRelPaths do
            Assert.True(File.Exists(Path.Combine(root (), relPath)), sprintf "expected %s to be restored" relPath)

    [<Then>]
    member _.``the output lists each restored file``() =
        let text = formatText (outcome ()) false false

        for relPath in expectedEnvRelPaths do
            Assert.Contains(relPath, text)

    [<Then>]
    member _.``the .env file is copied back to its original path in the repository``() =
        Assert.True(File.Exists(Path.Combine(root (), ".env")))

    [<Then>]
    member _.``the output reports that the directory does not exist``() =
        match opResult with
        | Some(Error message) -> Assert.Contains("does not exist", message)
        | other -> Assert.Fail(sprintf "expected an error, got %A" other)

    [<Then>]
    member _.``the output is valid JSON``() =
        use _doc = JsonDocument.Parse(formatJson (outcome ()))
        ()

    [<Then>]
    member _.``the JSON includes the direction, backup directory, list of files, copied count, and skipped count``() =
        use doc = JsonDocument.Parse(formatJson (outcome ()))
        let rootElement = doc.RootElement
        Assert.True(rootElement.TryGetProperty("direction") |> fst)
        Assert.True(rootElement.TryGetProperty("dir") |> fst)
        Assert.True(rootElement.TryGetProperty("files") |> fst)
        Assert.True(rootElement.TryGetProperty("copied") |> fst)
        Assert.True(rootElement.TryGetProperty("skipped") |> fst)

    [<Then>]
    member _.``README.md is not restored``() =
        Assert.False(File.Exists(Path.Combine(root (), "README.md")))

    [<Then>]
    member _.``the output reports that zero files were restored``() =
        let r = outcome ()
        Assert.Equal(0, r.Copied)
        Assert.Contains("0 file(s)", formatText r false false)

    [<Then>]
    member _.``the .env file is read from the feature-branch namespace inside the backup directory``() =
        Assert.Contains(outcome().Files, fun (f: EnvFileEntry) -> f.RelPath = ".env")

    [<Then>]
    member _.``the .env file is copied back to its original path in the worktree``() =
        Assert.True(File.Exists(Path.Combine(root (), ".env")))

    [<Then>]
    member _.``the .env file in the repository is overwritten with the backup``() =
        Assert.Equal(1, confirmCallCount)
        Assert.Equal("k=v", File.ReadAllText(Path.Combine(root (), ".env")))

    [<Then>]
    member _.``the output reports that restore was cancelled``() =
        Assert.Contains("cancelled", formatText (outcome ()) false false)

    [<Then>]
    member _.``the existing repository file is unchanged``() =
        Assert.Equal(1, confirmCallCount)
        Assert.Equal("existing=1", File.ReadAllText(Path.Combine(root (), ".env")))

    [<Then>]
    member _.``the .env file in the repository is overwritten without prompting``() =
        Assert.Equal(0, confirmCallCount)
        Assert.Equal("k=v", File.ReadAllText(Path.Combine(root (), ".env")))

    [<Then>]
    member _.``no confirmation prompt is shown``() = Assert.Equal(0, confirmCallCount)

    [<Then>]
    member _.``the .env file is restored to the repository``() =
        Assert.True(File.Exists(Path.Combine(root (), ".env")))
        Assert.Equal("k=v", File.ReadAllText(Path.Combine(root (), ".env")))

    [<Then>]
    member _.``the .claude/settings.local.json is restored to the repository preserving its relative path``() =
        Assert.True(File.Exists(Path.Combine(root (), ".claude", "settings.local.json")))

    [<Then>]
    member _.``the .claude/settings.local.json is not restored to the repository``() =
        Assert.False(File.Exists(Path.Combine(root (), ".claude", "settings.local.json")))

    [<Then>]
    member _.``secrets.json is copied back to the repository``() =
        Assert.True(File.Exists(Path.Combine(root (), "secrets.json")))

    [<Then>]
    member _.``cert.pem is copied back to the repository``() =
        Assert.True(File.Exists(Path.Combine(root (), "cert.pem")))

    [<Then>]
    member _.``.secrets/notes.md is copied back to the repository preserving its relative path``() =
        Assert.True(File.Exists(Path.Combine(root (), ".secrets", "notes.md")))

    [<Then>]
    member _.``no files are written to the repository``() =
        Assert.Empty(Directory.EnumerateFileSystemEntries(ensureRoot ()))

    [<Then>]
    member _.``the output lists the files that would be restored``() =
        let text = formatText (outcome ()) false false
        Assert.Contains("secrets.json", text)
        Assert.Contains("cert.pem", text)
        Assert.Contains(".secrets/notes.md", text)
        Assert.Contains("WOULD", text)

    [<AfterScenario>]
    member _.Cleanup() =
        for dir in ownedDirs do
            if Directory.Exists dir then
                Directory.Delete(dir, true)

/// Reads one named `Scenario:` block out of the real, frozen
/// `env-restore.feature` file (leaving the file itself untouched) and runs it
/// through TickSpec bound only against `EnvRestoreSteps` — see `EnvSteps.fs`'s
/// `FeatureRunner` for why this is per-scenario rather than per-file.
module private FeatureRunner =

    let private featurePath: string =
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
                "behaviors",
                "env",
                "env-restore.feature"
            )
        )

    let private extractScenario (featureLines: string[]) (scenarioTitle: string) : string[] =
        let featureLine =
            featureLines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let scenarioHeader = sprintf "Scenario: %s" scenarioTitle

        let startIdx = featureLines |> Array.findIndex (fun l -> l.Trim() = scenarioHeader)

        let endIdx =
            featureLines
            |> Array.skip (startIdx + 1)
            |> Array.tryFindIndex (fun l ->
                let trimmed = l.Trim()

                trimmed.StartsWith("Scenario:", StringComparison.Ordinal)
                || trimmed.StartsWith("Scenario Outline:", StringComparison.Ordinal)
                // env-restore.feature tags every scenario with a leading
                // `@tag` line, same as env-backup.feature/env-init.feature —
                // the next scenario's tag line must also end the slice, or it
                // gets pulled in as a dangling trailing line with no scenario
                // body to attach to.
                || trimmed.StartsWith("@", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    /// Runs the single scenario named `scenarioTitle` from
    /// `env-restore.feature`, bound against `EnvRestoreSteps`.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<EnvRestoreSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``Restore copies files back from backup`` () =
    FeatureRunner.run "Restore copies files back from backup"

[<Fact>]
let ``Restore with custom source directory`` () =
    FeatureRunner.run "Restore with custom source directory"

[<Fact>]
let ``Restore fails when backup directory does not exist`` () =
    FeatureRunner.run "Restore fails when backup directory does not exist"

[<Fact>]
let ``JSON output for restore`` () =
    FeatureRunner.run "JSON output for restore"

[<Fact>]
let ``Restore only restores .env files`` () =
    FeatureRunner.run "Restore only restores .env files"

[<Fact>]
let ``Restore with zero .env files in backup`` () =
    FeatureRunner.run "Restore with zero .env files in backup"

[<Fact>]
let ``Worktree-aware restore reads from correct namespace`` () =
    FeatureRunner.run "Worktree-aware restore reads from correct namespace"

[<Fact>]
let ``Restore prompts when destination files already exist`` () =
    FeatureRunner.run "Restore prompts when destination files already exist"

[<Fact>]
let ``Restore aborts when user declines overwrite`` () =
    FeatureRunner.run "Restore aborts when user declines overwrite"

[<Fact>]
let ``Restore with --force skips confirmation`` () =
    FeatureRunner.run "Restore with --force skips confirmation"

[<Fact>]
let ``Restore proceeds without prompt when no conflicts exist`` () =
    FeatureRunner.run "Restore proceeds without prompt when no conflicts exist"

[<Fact>]
let ``Restore includes config files with --include-config`` () =
    FeatureRunner.run "Restore includes config files with --include-config"

[<Fact>]
let ``Restore without --include-config ignores config files in backup`` () =
    FeatureRunner.run "Restore without --include-config ignores config files in backup"

[<Fact>]
let ``Restore recovers common secret file patterns`` () =
    FeatureRunner.run "Restore recovers common secret file patterns"

[<Fact>]
let ``Restore recovers a mix of .env and secret files together`` () =
    FeatureRunner.run "Restore recovers a mix of .env and secret files together"

[<Fact>]
let ``Dry-run restore previews without writing files`` () =
    FeatureRunner.run "Dry-run restore previews without writing files"
