/// TickSpec step definitions binding `specs/apps/rhino/behavior/rhino-cli/gherkin/git/git-lockfile.feature`'s
/// 3 scenarios to `RhinoCli.Application.Git.syncAtRoot`
/// [Repo-grounded — `apps/rhino-cli/src/commands/git/lockfile.rs`].
///
/// Every scenario below builds its own throwaway `git init` fixture rather
/// than touching this checkout's own repository, since `syncAtRoot` reads
/// and writes real Git index state (`git diff --cached`, `git add`). Each
/// fixture write is preceded by the Git Fixture Isolation Convention's six
/// layers: capped discovery (`GIT_CEILING_DIRECTORIES`), explicit `GIT_DIR`
/// (never relying on process CWD for repository selection), blanked
/// identity/config (`GIT_CONFIG_GLOBAL`/`GIT_CONFIG_SYSTEM`), a pre-write
/// escape guard comparing `git rev-parse --show-toplevel` against the
/// fixture's own canonicalized root, and an exit-status check on every
/// subprocess — see
/// `repo-governance/development/quality/git-fixture-isolation.md`.
module RhinoCli.Tests.Unit.Steps.GitSteps

open System
open System.Diagnostics
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Git

// ---------------------------------------------------------------------------
// Isolated git fixture helpers
// ---------------------------------------------------------------------------

let private isolate (root: string) (psi: ProcessStartInfo) =
    psi.EnvironmentVariables.["GIT_DIR"] <- Path.Combine(root, ".git")
    psi.EnvironmentVariables.["GIT_CEILING_DIRECTORIES"] <- root
    psi.EnvironmentVariables.["GIT_CONFIG_GLOBAL"] <- "/dev/null"
    psi.EnvironmentVariables.["GIT_CONFIG_SYSTEM"] <- "/dev/null"

/// Runs a `git` subcommand against `root`, isolated per the convention's
/// Standards 1-3, failing loud on a non-zero exit (Standard 5).
let private runGit (root: string) (args: string list) : unit =
    use proc = new Process()
    proc.StartInfo.FileName <- "git"
    args |> List.iter proc.StartInfo.ArgumentList.Add
    proc.StartInfo.WorkingDirectory <- root
    proc.StartInfo.RedirectStandardOutput <- true
    proc.StartInfo.RedirectStandardError <- true
    proc.StartInfo.UseShellExecute <- false
    isolate root proc.StartInfo
    proc.Start() |> ignore
    let stderr = proc.StandardError.ReadToEnd()
    proc.WaitForExit()

    if proc.ExitCode <> 0 then
        failwithf "git %s failed in %s: %s" (String.concat " " args) root stderr

/// Runs `git rev-parse --show-toplevel` against `cwd` with **no** isolation
/// env vars, relying on ordinary discovery from a directory already known
/// to contain `.git` immediately — used once, right after `git init`, to
/// learn the fixture's own canonicalized root (macOS's temp root is itself
/// a symlink, so the raw path and git's resolved path can differ).
let private canonicalToplevel (cwd: string) : string =
    use proc = new Process()
    proc.StartInfo.FileName <- "git"
    proc.StartInfo.ArgumentList.Add("rev-parse")
    proc.StartInfo.ArgumentList.Add("--show-toplevel")
    proc.StartInfo.WorkingDirectory <- cwd
    proc.StartInfo.RedirectStandardOutput <- true
    proc.StartInfo.RedirectStandardError <- true
    proc.StartInfo.UseShellExecute <- false
    proc.Start() |> ignore
    let stdout = proc.StandardOutput.ReadToEnd()
    proc.StandardError.ReadToEnd() |> ignore
    proc.WaitForExit()
    stdout.Trim()

/// Standard 4 escape guard — asserts `git rev-parse --show-toplevel` still
/// resolves to `canonicalRoot` immediately before a write, so a fixture bug
/// can never mutate a repository other than its own throwaway one.
let private assertRepoRootIs (canonicalRoot: string) (root: string) : unit =
    use proc = new Process()
    proc.StartInfo.FileName <- "git"
    proc.StartInfo.ArgumentList.Add("rev-parse")
    proc.StartInfo.ArgumentList.Add("--show-toplevel")
    proc.StartInfo.WorkingDirectory <- root
    proc.StartInfo.RedirectStandardOutput <- true
    proc.StartInfo.RedirectStandardError <- true
    proc.StartInfo.UseShellExecute <- false
    isolate root proc.StartInfo
    proc.Start() |> ignore
    let stdout = proc.StandardOutput.ReadToEnd()
    proc.StandardError.ReadToEnd() |> ignore
    proc.WaitForExit()
    let resolved = stdout.Trim()

    if resolved <> canonicalRoot then
        failwithf "git fixture escape guard tripped: expected %s, git resolved %s" canonicalRoot resolved

/// A fresh `git init` repository with a committable identity configured
/// locally (never global), returning the fixture's raw and canonicalized
/// root — see `canonicalToplevel`'s doc comment for why both are kept.
let private newGitFixture () : string * string =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-cli-git-lockfile-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(root) |> ignore
    runGit root [ "init"; "-q"; "-b"; "main" ]
    let canonicalRoot = canonicalToplevel root
    assertRepoRootIs canonicalRoot root
    runGit root [ "config"; "user.name"; "Rhino CLI Test" ]
    assertRepoRootIs canonicalRoot root
    runGit root [ "config"; "user.email"; "rhino-cli-test@example.invalid" ]
    root, canonicalRoot

let private writeFile (root: string) (relativePath: string) (content: string) : unit =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName(full: string)) |> ignore
    File.WriteAllText(full, content)

/// Thin isolated `git` `Process` builder for the read-only assertions this
/// file makes after `syncAtRoot` runs (`stagedFiles`) — mirrors `runGit`'s
/// isolation without its exit-status-checked `Start`/`WaitForExit` sequence,
/// since callers here need the live `Process` to read stdout from.
let private gitProcessForTest (root: string) (args: string list) : Process =
    let proc = new Process()
    proc.StartInfo.FileName <- "git"
    args |> List.iter proc.StartInfo.ArgumentList.Add
    proc.StartInfo.WorkingDirectory <- root
    proc.StartInfo.RedirectStandardOutput <- true
    proc.StartInfo.RedirectStandardError <- true
    proc.StartInfo.UseShellExecute <- false
    isolate root proc.StartInfo
    proc

let private stagedFiles (root: string) : string list =
    use proc = gitProcessForTest root [ "diff"; "--cached"; "--name-only" ]
    proc.Start() |> ignore
    let stdout = proc.StandardOutput.ReadToEnd()
    proc.StandardError.ReadToEnd() |> ignore
    proc.WaitForExit()
    stdout.Split('\n') |> Array.filter (fun l -> l <> "") |> List.ofArray

// ---------------------------------------------------------------------------
// Step definitions
// ---------------------------------------------------------------------------

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type GitSteps() =
    let mutable root: string = ""
    let mutable appDir: string = ""
    let mutable lockfilePath: string = ""
    let mutable lockfileBefore: string = ""
    let mutable stagedBefore: string list = []
    let mutable output: string = ""
    let mutable result: Result<unit, string> option = None

    let run () =
        stagedBefore <- stagedFiles root
        use writer = new StringWriter()
        result <- Some(syncAtRoot root writer)
        output <- writer.ToString()

    // ---- Given ----

    [<Given>]
    member _.``a staged app package.json whose version disagrees with its package-lock.json``() =
        let r, _ = newGitFixture ()
        root <- r
        appDir <- "apps/sample-app"
        lockfilePath <- appDir + "/package-lock.json"
        writeFile root (appDir + "/package.json") "{\"name\":\"sample-app\",\"version\":\"1.1.0\"}\n"

        lockfileBefore <-
            "{\n  \"name\": \"sample-app\",\n  \"version\": \"1.0.0\",\n  \"lockfileVersion\": 3,\n  \"packages\": {\n    \"\": { \"name\": \"sample-app\", \"version\": \"1.0.0\" }\n  }\n}\n"

        writeFile root lockfilePath lockfileBefore
        runGit root [ "add"; appDir + "/package.json" ]

    [<Given>]
    member _.``a staged app package.json whose fields already agree with its package-lock.json``() =
        let r, _ = newGitFixture ()
        root <- r
        appDir <- "apps/current-app"
        lockfilePath <- appDir + "/package-lock.json"
        writeFile root (appDir + "/package.json") "{\"name\":\"current-app\",\"version\":\"1.1.0\"}\n"

        lockfileBefore <-
            "{\n  \"name\": \"current-app\",\n  \"version\": \"1.1.0\",\n  \"lockfileVersion\": 3,\n  \"packages\": {\n    \"\": { \"name\": \"current-app\", \"version\": \"1.1.0\" }\n  }\n}\n"

        writeFile root lockfilePath lockfileBefore
        runGit root [ "add"; appDir + "/package.json" ]

    [<Given>]
    member _.``no app package.json file is staged``() =
        let r, _ = newGitFixture ()
        root <- r
        writeFile root "README.md" "staged non-package file\n"
        runGit root [ "add"; "README.md" ]

    // ---- When ----

    [<When>]
    member _.``the developer runs "git lockfile sync"``() = run ()

    // ---- Then ----

    [<Then>]
    member _.``the command regenerates the app's package-lock.json to match the manifest``() =
        match result with
        | Some(Ok()) ->
            let after = File.ReadAllText(Path.Combine(root, lockfilePath))
            Assert.Contains("\"version\": \"1.1.0\"", after)
            Assert.NotEqual<string>(lockfileBefore, after)
        | Some(Error message) -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
        | None -> Assert.Fail("no When step ran")

    [<Then>]
    member _.``the regenerated package-lock.json is staged``() =
        Assert.Contains(lockfilePath, stagedFiles root)

    [<Then>]
    member _.``the command exits successfully``() =
        match result with
        | Some(Ok()) -> ()
        | Some(Error message) -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
        | None -> Assert.Fail("no When step ran")

    [<Then>]
    member _.``the output reports no lockfile was synced``() =
        Assert.DoesNotContain("Syncing", output)

    [<Then>]
    member _.``the package-lock.json file is not modified``() =
        Assert.Equal(lockfileBefore, File.ReadAllText(Path.Combine(root, lockfilePath)))

    [<Then>]
    member _.``the output is empty``() = Assert.Equal("", output)

    [<Then>]
    member _.``the staged file set is unchanged``() =
        Assert.Equal<string list>(stagedBefore, stagedFiles root)

/// Reads one named `Scenario:` block out of the real, frozen
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/git/git-lockfile.feature`
/// file (leaving the file itself untouched) and runs it through TickSpec
/// bound only against `GitSteps` — see `EnvSteps.fs`'s `FeatureRunner` for
/// why this is per-scenario rather than per-file.
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
                "..",
                "specs",
                "apps",
                "rhino",
                "behavior",
                "rhino-cli",
                "gherkin",
                "git",
                "git-lockfile.feature"
            )
        )

    let private extractScenario (featureLines: string[]) (scenarioTitle: string) : string[] =
        let featureLine =
            featureLines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let startIdx =
            featureLines
            |> Array.findIndex (fun l -> l.Trim() = sprintf "Scenario: %s" scenarioTitle)

        let endIdx =
            featureLines
            |> Array.skip (startIdx + 1)
            |> Array.tryFindIndex (fun l ->
                let trimmed = l.Trim()
                trimmed.StartsWith("Scenario:", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    /// Runs `scenarioTitle` from `git-lockfile.feature`, bound against
    /// `GitSteps`.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<GitSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)

        for scenario in feature.Scenarios do
            scenario.Action.Invoke()

[<Fact>]
let ``A staged package manifest with a stale lockfile is regenerated and staged`` () =
    FeatureRunner.run "A staged package manifest with a stale lockfile is regenerated and staged"

[<Fact>]
let ``A staged package manifest whose lockfile is already current is left untouched`` () =
    FeatureRunner.run "A staged package manifest whose lockfile is already current is left untouched"

[<Fact>]
let ``No staged app package.json means no lockfile work`` () =
    FeatureRunner.run "No staged app package.json means no lockfile work"
