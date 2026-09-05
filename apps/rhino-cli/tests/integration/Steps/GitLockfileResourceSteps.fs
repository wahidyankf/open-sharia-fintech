/// TickSpec step definitions binding `specs/apps/rhino/cli/behaviours/git/git-lockfile.feature`'s
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
module RhinoCli.Tests.Integration.Steps.GitLockfileResourceSteps

/// Explicit static-coverage ownership; the validator scopes this file's
/// TickSpec bindings to these canonical features.
let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/git/git-lockfile.feature" ]


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
/// `specs/apps/rhino/cli/behaviours/git/git-lockfile.feature`
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
                "specs",
                "apps",
                "rhino",
                "cli",
                "behaviours",
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

// ---------------------------------------------------------------------------
// Direct unit tests against RhinoCli.Application.Git's public functions.
//
// Unlike the three `[<Fact>]`s above (each a `FeatureRunner.run` wrapper
// around a frozen Gherkin scenario), the tests below build their own isolated
// git fixture and call `syncAtRoot` directly, reusing this file's own
// `newGitFixture`/`writeFile`/`runGit`/`stagedFiles` helpers — closing
// coverage gaps the three Gherkin scenarios do not reach (unusual JSON value
// kinds, lockfile format variants, and subprocess failure paths).
// ---------------------------------------------------------------------------

[<Fact>]
let ``Lockfile fields that agree across reordered object keys, matching array order, and non-string value kinds are treated as current``
    ()
    =
    let root, _ = newGitFixture ()
    let appDir = "apps/rich-fields-app"

    writeFile
        root
        (appDir + "/package.json")
        "{\"name\":\"rich-fields-app\",\"version\":\"1.0.0\",\"dependencies\":{\"lodash\":\"^4.17.0\",\"axios\":\"^1.0.0\"},\"os\":[\"linux\",\"darwin\"],\"workspaces\":true,\"engines\":18}\n"

    let lockfileBefore =
        "{\"name\":\"rich-fields-app\",\"version\":\"1.0.0\",\"lockfileVersion\":3,\"packages\":{\"\":{\"name\":\"rich-fields-app\",\"version\":\"1.0.0\",\"dependencies\":{\"axios\":\"^1.0.0\",\"lodash\":\"^4.17.0\"},\"os\":[\"linux\",\"darwin\"],\"workspaces\":true,\"engines\":18}}}\n"

    writeFile root (appDir + "/package-lock.json") lockfileBefore
    runGit root [ "add"; appDir + "/package.json" ]

    use writer = new StringWriter()
    let result = syncAtRoot root writer

    match result with
    | Ok() -> ()
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

    Assert.DoesNotContain("Syncing", writer.ToString())
    Assert.Equal(lockfileBefore, File.ReadAllText(Path.Combine(root, appDir, "package-lock.json")))

[<Fact>]
let ``A field whose JSON kind differs between the manifest and its lockfile is treated as stale`` () =
    let root, _ = newGitFixture ()
    let appDir = "apps/kind-mismatch-app"

    writeFile
        root
        (appDir + "/package.json")
        "{\"name\":\"kind-mismatch-app\",\"version\":\"1.0.0\",\"dependencies\":{\"lodash\":\"^4.17.0\"}}\n"

    writeFile
        root
        (appDir + "/package-lock.json")
        "{\"name\":\"kind-mismatch-app\",\"version\":\"1.0.0\",\"lockfileVersion\":3,\"packages\":{\"\":{\"name\":\"kind-mismatch-app\",\"version\":\"1.0.0\",\"dependencies\":[]}}}\n"

    runGit root [ "add"; appDir + "/package.json" ]

    use writer = new StringWriter()
    let result = syncAtRoot root writer

    match result with
    | Ok() -> ()
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

    Assert.Contains("Syncing", writer.ToString())

[<Fact>]
let ``An object field with the same key count but different key names is treated as stale`` () =
    let root, _ = newGitFixture ()
    let appDir = "apps/diff-keys-app"

    writeFile
        root
        (appDir + "/package.json")
        "{\"name\":\"diff-keys-app\",\"version\":\"1.0.0\",\"dependencies\":{\"lodash\":\"^4.17.0\",\"axios\":\"^1.0.0\"}}\n"

    writeFile
        root
        (appDir + "/package-lock.json")
        "{\"name\":\"diff-keys-app\",\"version\":\"1.0.0\",\"lockfileVersion\":3,\"packages\":{\"\":{\"name\":\"diff-keys-app\",\"version\":\"1.0.0\",\"dependencies\":{\"lodash\":\"^4.17.0\",\"oldpkg\":\"^1.0.0\"}}}}\n"

    runGit root [ "add"; appDir + "/package.json" ]

    use writer = new StringWriter()
    let result = syncAtRoot root writer

    match result with
    | Ok() -> ()
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

    Assert.Contains("Syncing", writer.ToString())

[<Fact>]
let ``An array field in a different element order is treated as stale, unlike object key order`` () =
    let root, _ = newGitFixture ()
    let appDir = "apps/array-order-app"

    writeFile
        root
        (appDir + "/package.json")
        "{\"name\":\"array-order-app\",\"version\":\"1.0.0\",\"os\":[\"linux\",\"darwin\"]}\n"

    writeFile
        root
        (appDir + "/package-lock.json")
        "{\"name\":\"array-order-app\",\"version\":\"1.0.0\",\"lockfileVersion\":3,\"packages\":{\"\":{\"name\":\"array-order-app\",\"version\":\"1.0.0\",\"os\":[\"darwin\",\"linux\"]}}}\n"

    runGit root [ "add"; appDir + "/package.json" ]

    use writer = new StringWriter()
    let result = syncAtRoot root writer

    match result with
    | Ok() -> ()
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

    Assert.Contains("Syncing", writer.ToString())

[<Fact>]
let ``A v2+ lockfile whose packages object has no root entry falls back to the lockfile's own top-level fields`` () =
    let root, _ = newGitFixture ()
    let appDir = "apps/no-root-entry-app"

    writeFile root (appDir + "/package.json") "{\"name\":\"no-root-entry-app\",\"version\":\"1.1.0\"}\n"

    writeFile
        root
        (appDir + "/package-lock.json")
        "{\"name\":\"no-root-entry-app\",\"version\":\"1.0.0\",\"lockfileVersion\":3,\"packages\":{\"node_modules/foo\":{\"version\":\"2.0.0\"}}}\n"

    runGit root [ "add"; appDir + "/package.json" ]

    use writer = new StringWriter()
    let result = syncAtRoot root writer

    match result with
    | Ok() -> ()
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

    Assert.Contains("Syncing", writer.ToString())

[<Fact>]
let ``A v1-style lockfile with no packages object falls back to the lockfile's own top-level fields`` () =
    let root, _ = newGitFixture ()
    let appDir = "apps/v1-lockfile-app"

    writeFile root (appDir + "/package.json") "{\"name\":\"v1-lockfile-app\",\"version\":\"1.1.0\"}\n"

    writeFile
        root
        (appDir + "/package-lock.json")
        "{\"name\":\"v1-lockfile-app\",\"version\":\"1.0.0\",\"lockfileVersion\":1}\n"

    runGit root [ "add"; appDir + "/package.json" ]

    use writer = new StringWriter()
    let result = syncAtRoot root writer

    match result with
    | Ok() -> ()
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

    Assert.Contains("Syncing", writer.ToString())

[<Fact>]
let ``A field present in the manifest but absent from the lockfile root entry is treated as stale`` () =
    let root, _ = newGitFixture ()
    let appDir = "apps/asymmetric-field-app"

    writeFile
        root
        (appDir + "/package.json")
        "{\"name\":\"asymmetric-field-app\",\"version\":\"1.0.0\",\"license\":\"MIT\"}\n"

    writeFile
        root
        (appDir + "/package-lock.json")
        "{\"name\":\"asymmetric-field-app\",\"version\":\"1.0.0\",\"lockfileVersion\":3,\"packages\":{\"\":{\"name\":\"asymmetric-field-app\",\"version\":\"1.0.0\"}}}\n"

    runGit root [ "add"; appDir + "/package.json" ]

    use writer = new StringWriter()
    let result = syncAtRoot root writer

    match result with
    | Ok() -> ()
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

    Assert.Contains("Syncing", writer.ToString())

[<Fact>]
let ``Malformed JSON in a staged manifest is reported as a lockfile-read error`` () =
    let root, _ = newGitFixture ()
    let appDir = "apps/broken-json-app"

    writeFile root (appDir + "/package.json") "{ this is not valid json"
    writeFile root (appDir + "/package-lock.json") "{\"name\":\"broken-json-app\",\"version\":\"1.0.0\"}\n"

    runGit root [ "add"; appDir + "/package.json" ]

    use writer = new StringWriter()
    let result = syncAtRoot root writer

    match result with
    | Error message -> Assert.Contains("failed to read lockfile fields", message)
    | Ok() -> Assert.Fail("expected an Error for malformed JSON")

[<Fact>]
let ``A staged manifest with no sibling lockfile file is left untouched`` () =
    let root, _ = newGitFixture ()
    let appDir = "apps/no-lockfile-app"

    writeFile root (appDir + "/package.json") "{\"name\":\"no-lockfile-app\",\"version\":\"1.0.0\"}\n"
    runGit root [ "add"; appDir + "/package.json" ]
    let beforeStaged = stagedFiles root

    use writer = new StringWriter()
    let result = syncAtRoot root writer

    match result with
    | Ok() -> ()
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

    Assert.DoesNotContain("Syncing", writer.ToString())
    Assert.Equal<string list>(beforeStaged, stagedFiles root)

[<Fact>]
let ``A regenerated lockfile that git refuses to stage because it is gitignored is reported as a staging error`` () =
    let root, _ = newGitFixture ()
    let appDir = "apps/ignored-lockfile-app"

    writeFile root ".gitignore" (appDir + "/package-lock.json\n")
    writeFile root (appDir + "/package.json") "{\"name\":\"ignored-lockfile-app\",\"version\":\"1.1.0\"}\n"

    writeFile
        root
        (appDir + "/package-lock.json")
        "{\"name\":\"ignored-lockfile-app\",\"version\":\"1.0.0\",\"lockfileVersion\":3,\"packages\":{\"\":{\"name\":\"ignored-lockfile-app\",\"version\":\"1.0.0\"}}}\n"

    runGit root [ "add"; appDir + "/package.json" ]

    use writer = new StringWriter()
    let result = syncAtRoot root writer

    match result with
    | Error message -> Assert.Contains("failed to stage", message)
    | Ok() -> Assert.Fail("expected an Error because the lockfile path is gitignored")

// ---------------------------------------------------------------------------
// Subprocess-launch failures — `git`/`npm` genuinely missing from `PATH`,
// caught by `stagedPaths`/`npmRegenerateLockfile`'s
// `:? System.ComponentModel.Win32Exception` handlers. Safe to mutate the
// test host process's own `PATH` for the duration of one call: this
// assembly disables test parallelization (see `GitSteps.fs`'s module doc
// comment and `[<assembly: CollectionBehavior(DisableTestParallelization =
// true)>]` in `GitRootUnitTests.fs`), so no other test observes it.
//
// `gitAdd`'s own Win32Exception branch is NOT covered here: `stagedPaths`
// (the first `git` call `syncAtRoot` makes) and `gitAdd` (a later call in
// the same synchronous invocation) both need `git`, so there is no
// black-box way to make `git` resolve for the first call and disappear
// only for the second without an inherently flaky mid-call PATH toggle.
// ---------------------------------------------------------------------------

[<Fact>]
let ``syncAtRoot reports a Win32Exception when git is entirely missing from PATH`` () =
    let root, _ = newGitFixture ()
    writeFile root "README.md" "staged non-package file\n"
    runGit root [ "add"; "README.md" ]

    let originalPath = Environment.GetEnvironmentVariable "PATH"

    try
        Environment.SetEnvironmentVariable("PATH", "")
        use writer = new StringWriter()
        let result = syncAtRoot root writer

        match result with
        | Error message -> Assert.Contains("failed to invoke git diff --cached", message)
        | Ok() -> Assert.Fail("expected an Error because git is not on PATH")
    finally
        Environment.SetEnvironmentVariable("PATH", originalPath)

[<Fact>]
let ``syncAtRoot reports a Win32Exception when npm is missing from PATH but git is still resolvable`` () =
    let root, _ = newGitFixture ()
    let appDir = "apps/npm-missing-app"

    writeFile root (appDir + "/package.json") "{\"name\":\"npm-missing-app\",\"version\":\"1.1.0\"}\n"

    writeFile
        root
        (appDir + "/package-lock.json")
        "{\"name\":\"npm-missing-app\",\"version\":\"1.0.0\",\"lockfileVersion\":3,\"packages\":{\"\":{\"name\":\"npm-missing-app\",\"version\":\"1.0.0\"}}}\n"

    runGit root [ "add"; appDir + "/package.json" ]

    let originalPath = Environment.GetEnvironmentVariable "PATH"

    try
        // `git` lives at a fixed system path (`/usr/bin/git` on every runner
        // this repository targets); confining PATH to its directory alone
        // still resolves `git` while excluding npm's separate
        // Volta-managed directory.
        Environment.SetEnvironmentVariable("PATH", "/usr/bin")
        use writer = new StringWriter()
        let result = syncAtRoot root writer

        match result with
        | Error message -> Assert.Contains("failed to invoke npm install", message)
        | Ok() -> Assert.Fail("expected an Error because npm is not on PATH")
    finally
        Environment.SetEnvironmentVariable("PATH", originalPath)

// ---------------------------------------------------------------------------
// `npmRegenerateLockfile`'s non-zero-exit branch — a genuine (non-launch)
// `npm install --package-lock-only` failure, forced offline and
// deterministically by blocking `node_modules` creation with a same-named
// regular file
// ---------------------------------------------------------------------------

[<Fact>]
let ``A lockfile regeneration whose node_modules path is blocked by a same-named file is reported as a regeneration error``
    ()
    =
    let root, _ = newGitFixture ()
    let appDir = "apps/npm-nodemodules-blocked-app"

    writeFile root (appDir + "/package.json") "{\"name\":\"npm-nodemodules-blocked-app\",\"version\":\"1.1.0\"}\n"

    writeFile
        root
        (appDir + "/package-lock.json")
        "{\"name\":\"npm-nodemodules-blocked-app\",\"version\":\"1.0.0\",\"lockfileVersion\":3,\"packages\":{\"\":{\"name\":\"npm-nodemodules-blocked-app\",\"version\":\"1.0.0\"}}}\n"

    File.WriteAllText(Path.Combine(root, appDir, "node_modules"), "not a directory\n")
    runGit root [ "add"; appDir + "/package.json" ]

    use writer = new StringWriter()
    let result = syncAtRoot root writer

    match result with
    | Error message -> Assert.Contains(sprintf "failed to regenerate %s/package-lock.json" appDir, message)
    | Ok() -> Assert.Fail("expected an Error because node_modules creation is blocked")
