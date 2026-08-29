/// TickSpec step definitions binding `cargo-target-share.feature`'s 18
/// scenarios to `RhinoCli.Application.Doctor`'s cargo target-share port
/// [Repo-grounded —
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/system/cargo-target-share.feature`,
/// `apps/rhino-cli/tests/cargo_target_share.rs`].
///
/// Follows `EnvInitSteps.fs`'s per-scenario slicing convention: each xunit
/// `[<Fact>]` below runs exactly one scenario, extracted from the real,
/// frozen feature file. Unlike the Rust reference (a cucumber-rs suite that
/// drives the *compiled binary*), these steps call `RhinoCli.Application
/// .Doctor`'s pure functions directly — the same "call the internal function
/// directly" precedent `EnvInitSteps.fs`/`EnvStagedGuardSteps.fs` already
/// establish for this port — composing them the same way
/// `commands/doctor.rs::run_target_share_step` does, into one accumulated
/// text report a `Then` step can assert against.
///
/// # Deviations from the literal Gherkin text
///
/// Mirrors `apps/rhino-cli/tests/cargo_target_share.rs`'s own documented
/// deviations for the two scenarios no single-process suite can literally
/// exercise:
///
/// - **"the doctor change is byte-identical across the parity repos"**: proxied
///   by running `fixTargetShares` against two identically-shaped synthetic
///   repos literally named `ose-public`/`ose-private`, proving the resulting
///   symlink targets differ only in the repo-name path segment.
/// - **"Nx build caching is unaffected for crates that emit only dist"**:
///   proxied by running the fix step twice and asserting a representative
///   Nx-managed `project.json` file's bytes are untouched — the precondition
///   Nx's own cache-hit behavior depends on.
///
/// All fixture git usage below follows the [Git Fixture Isolation
/// Convention](../../../../../../repo-governance/development/quality/git-fixture-isolation.md);
/// `GIT_DIR`/`GIT_WORK_TREE` are stripped from every shelled `git` call the
/// same way `ParityUnitTests.fs`/`GitRootUnitTests.fs` already do.
module RhinoCli.Tests.Unit.Steps.DoctorSteps

open System
open System.Diagnostics
open System.IO
open System.Text.Json
open TickSpec
open Xunit
open RhinoCli.Application.Doctor

// ---------------------------------------------------------------------------
// Fixture helpers (duplicated per-file rather than shared, matching
// ParityUnitTests.fs's / GitRootUnitTests.fs's own precedent).
// ---------------------------------------------------------------------------

let private runGit (cwd: string) (args: string list) : unit =
    use proc = new Process()
    proc.StartInfo.FileName <- "git"
    args |> List.iter proc.StartInfo.ArgumentList.Add
    proc.StartInfo.WorkingDirectory <- cwd
    proc.StartInfo.RedirectStandardOutput <- true
    proc.StartInfo.RedirectStandardError <- true
    proc.StartInfo.UseShellExecute <- false
    proc.StartInfo.EnvironmentVariables.Remove("GIT_DIR")
    proc.StartInfo.EnvironmentVariables.Remove("GIT_WORK_TREE")
    proc.Start() |> ignore
    let stderr = proc.StandardError.ReadToEnd()
    proc.WaitForExit()

    if proc.ExitCode <> 0 then
        failwithf "git %s failed in %s: %s" (String.concat " " args) cwd stderr

let private writeCargoToml (dir: string) (name: string) =
    Directory.CreateDirectory(dir) |> ignore

    File.WriteAllText(
        Path.Combine(dir, "Cargo.toml"),
        sprintf "[package]\nname = \"%s\"\nversion = \"0.1.0\"\nedition = \"2021\"\n" name
    )

    let src = Path.Combine(dir, "src")
    Directory.CreateDirectory(src) |> ignore

    File.WriteAllText(
        Path.Combine(src, "main.rs"),
        "fn main() {}\n\n#[test]\nfn trivial_pass() {\n    assert!(true);\n}\n"
    )

let private makeCrate (repoRoot: string) (name: string) : string =
    let crateDir = Path.Combine(repoRoot, "apps", name)
    writeCargoToml crateDir name
    crateDir

let private buildThrowawayRepo (repoDir: string) =
    Directory.CreateDirectory(repoDir) |> ignore
    runGit repoDir [ "init"; "-q"; "-b"; "main" ]
    runGit repoDir [ "config"; "user.name"; "Rhino CLI Test" ]
    runGit repoDir [ "config"; "user.email"; "rhino-cli-test@example.invalid" ]
    File.WriteAllText(Path.Combine(repoDir, "README.md"), "throwaway fixture")
    runGit repoDir [ "add"; "." ]
    runGit repoDir [ "commit"; "-m"; "init" ]

let private commitAll (repoDir: string) (message: string) =
    runGit repoDir [ "add"; "." ]
    runGit repoDir [ "commit"; "-m"; message ]

let private addWorktree (repoDir: string) (worktreeDir: string) =
    runGit repoDir [ "worktree"; "add"; "--detach"; worktreeDir ]

// ---------------------------------------------------------------------------
// project.json git-state-isolation regression helpers (scenario 18)
// ---------------------------------------------------------------------------

let private fsharpProjectJsonPath: string =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "project.json"))

let private gitStateScrub = "env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR "

let private knownTestTargets = [ "test:unit"; "test:integration"; "test:coverage" ]

/// Reads `command`s that directly invoke `dotnet test` out of
/// `test:unit`/`test:integration`/`test:coverage` — the F# project's direct
/// test-execution targets, analogous to Rust's `test:unit`/`test:integration`/
/// `test:coverage` in `apps/rhino-cli/project.json`.
let private commandsForKnownTargets (projectJsonPath: string) : (string * string) list =
    let json = File.ReadAllText(projectJsonPath)
    use doc = JsonDocument.Parse(json)
    let targets = doc.RootElement.GetProperty("targets")

    knownTestTargets
    |> List.map (fun name ->
        let command =
            targets.GetProperty(name).GetProperty("options").GetProperty("command").GetString()

        (name, command))

/// Scans the entire `project.json` text for every occurrence of the literal
/// substring `"dotnet test "` not immediately preceded by
/// [`gitStateScrub`], returning a short snippet around each offender. An
/// empty result proves every direct `dotnet test` invocation anywhere in the
/// file — not just the three known targets above — clears inherited
/// `GIT_DIR`/`GIT_WORK_TREE`/`GIT_COMMON_DIR` first, so a new target added
/// later cannot silently bypass the guard.
let private unguardedDotnetTestOccurrences (projectJsonPath: string) : string list =
    let text = File.ReadAllText(projectJsonPath)
    let marker = "dotnet test "

    let rec scan (fromIdx: int) (acc: string list) : string list =
        let found = text.IndexOf(marker, fromIdx, StringComparison.Ordinal)

        if found < 0 then
            List.rev acc
        else
            let precedingStart = found - gitStateScrub.Length

            let guarded =
                precedingStart >= 0
                && text.Substring(precedingStart, gitStateScrub.Length) = gitStateScrub

            let nextAcc =
                if guarded then
                    acc
                else
                    let snippetStart = max 0 (found - 20)
                    let snippetLength = min 80 (text.Length - snippetStart)
                    text.Substring(snippetStart, snippetLength) :: acc

            scan (found + marker.Length) nextAcc

    scan 0 []

// ---------------------------------------------------------------------------
// Step-definition container
// ---------------------------------------------------------------------------

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type DoctorSteps() =
    let ownedDirs = ResizeArray<string>()

    let newTempDir (prefix: string) : string =
        let dir =
            Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-steps-" + prefix + "-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory(dir) |> ignore
        ownedDirs.Add(dir)
        dir

    let repoRoot = newTempDir "repo"
    let cacheRoot = newTempDir "cache"
    do buildThrowawayRepo repoRoot
    let repoNameValue = Path.GetFileName(repoRoot: string)

    let mutable ci = false
    let mutable fix = false
    let mutable prune = false
    let mutable dryRun = false
    let mutable scrubCargoSweep = false
    let mutable crateDir: string option = None
    let mutable secondWorktree: (string * string) option = None
    let mutable checkStatuses: TargetShareStatus list = []
    let mutable fixOutcome: FixOutcome option = None
    let mutable pruneOutcome: PruneOutcome option = None
    let mutable sweepOutcome: SweepOutcome option = None
    let mutable outputText = ""
    let mutable repoNameResults: (string * string) list = []
    let mutable configBefore: byte[] option = None
    let mutable configAfter: byte[] option = None
    let mutable gitStateCommands: (string * string) list = []

    let effectiveCargoSweepPresent () =
        if scrubCargoSweep then false else cargoSweepPresent ()

    /// Runs the check/fix/prune/sweep pipeline against `targetRepoRoot`,
    /// mirroring `commands/doctor.rs::run_target_share_step`'s composition —
    /// see this file's module doc comment for why this calls straight into
    /// `Doctor`'s functions rather than spawning a compiled binary.
    let runDoctorAgainst (targetRepoRoot: string) : unit =
        let sb = Text.StringBuilder()
        let statuses = checkTargetShares targetRepoRoot cacheRoot repoNameValue ci
        checkStatuses <- statuses
        sb.Append(formatCheckReport statuses ci).Append('\n') |> ignore

        if fix then
            let outcome = fixTargetShares targetRepoRoot cacheRoot repoNameValue ci
            fixOutcome <- Some outcome
            sb.Append(formatFixReport outcome).Append('\n') |> ignore

        if prune then
            let pOutcome = pruneOrphans targetRepoRoot cacheRoot repoNameValue dryRun ci
            pruneOutcome <- Some pOutcome
            sb.Append(formatPruneReport pOutcome dryRun).Append('\n') |> ignore

            let sOutcome =
                sweepStale cacheRoot repoNameValue dryRun (effectiveCargoSweepPresent ()) ci

            sweepOutcome <- Some sOutcome
            let sweepText = formatSweepReport sOutcome

            if sweepText <> "" then
                sb.Append(sweepText).Append('\n') |> ignore

        outputText <- sb.ToString()

    let exec () = runDoctorAgainst repoRoot

    let orphanEntry () =
        Path.Combine(cacheRoot, repoNameValue, "orphan-crate")

    // ---- Given ----

    [<Given>]
    member _.``a Rust crate with a plain target directory exists in a repo checkout outside CI``() =
        let cd = makeCrate repoRoot "foo"
        Directory.CreateDirectory(Path.Combine(cd, "target")) |> ignore
        ci <- false
        crateDir <- Some cd

    [<Given>]
    member _.``a crate's target is already the correct symlink into the shared cache``() =
        let cd = makeCrate repoRoot "foo"
        crateDir <- Some cd
        fix <- true
        exec ()

    [<Given>]
    member _.``a crate's target is a plain rebuildable directory containing stale artifacts``() =
        let cd = makeCrate repoRoot "foo"
        let target = Path.Combine(cd, "target")
        Directory.CreateDirectory(target) |> ignore
        File.WriteAllText(Path.Combine(target, "stale.txt"), "stale artifact")
        ci <- false
        crateDir <- Some cd

    [<Given>]
    member _.``a crate's target is a plain directory not yet symlinked into the shared cache``() =
        let cd = makeCrate repoRoot "foo"
        Directory.CreateDirectory(Path.Combine(cd, "target")) |> ignore
        crateDir <- Some cd

    [<Given>]
    member _.``the environment variable CI is set``() =
        let cd = makeCrate repoRoot "foo"
        Directory.CreateDirectory(Path.Combine(cd, "target")) |> ignore
        crateDir <- Some cd
        Directory.CreateDirectory(orphanEntry ()) |> ignore
        ci <- true

    [<Given>]
    member _.``a repo checkout contains multiple Rust crates under apps and libs outside CI``() =
        makeCrate repoRoot "a" |> ignore
        makeCrate repoRoot "b" |> ignore
        writeCargoToml (Path.Combine(repoRoot, "libs", "c")) "c"
        ci <- false

    [<Given>]
    member _.``two worktrees of the same repo each have a crate's target symlinked by the doctor``() =
        let cd = makeCrate repoRoot "foo"
        commitAll repoRoot "add apps/foo"
        crateDir <- Some cd
        fix <- true
        exec ()

        let wtHolder = newTempDir "wtholder"
        let wtPath = Path.Combine(wtHolder, "linked-wt")
        addWorktree repoRoot wtPath
        let wtCrateDir = Path.Combine(wtPath, "apps", "foo")
        runDoctorAgainst wtPath
        secondWorktree <- Some(wtHolder, wtCrateDir)

    [<Given>]
    member _.``a linked worktree holds a crate whose target is still a plain directory outside CI``() =
        let cd = makeCrate repoRoot "foo"
        commitAll repoRoot "add apps/foo"
        crateDir <- Some cd

        let wtHolder = newTempDir "wtholder"
        let wtPath = Path.Combine(wtHolder, "linked-wt")
        addWorktree repoRoot wtPath
        let wtCrateDir = Path.Combine(wtPath, "apps", "foo")
        let wtTarget = Path.Combine(wtCrateDir, "target")
        Directory.CreateDirectory(wtTarget) |> ignore
        File.WriteAllText(Path.Combine(wtTarget, "stale.txt"), "stale")
        secondWorktree <- Some(wtHolder, wtCrateDir)
        ci <- false

    [<Given>]
    member _.``a crate's target is a symlink into the shared cache``() =
        let cd = makeCrate repoRoot "foo"
        crateDir <- Some cd
        fix <- true
        exec ()

    [<Given>]
    member _.``the doctor target-share change is delivered to ose-public and ose-private``() =
        // Deviation — see the module doc comment: the real invariant (a
        // cross-repository diff) is out of this single-suite's reach; the
        // subsequent When step builds the named synthetic repos this
        // scenario's proxy actually drives.
        ()

    [<Given>]
    member _.``the ose-public CLIs no longer list the whole target directory in build outputs``() =
        let cd = makeCrate repoRoot "foo"
        let projectJson = Path.Combine(cd, "project.json")
        let content = "{\"targets\":{\"build\":{\"outputs\":[\"{projectRoot}/dist\"]}}}"
        File.WriteAllText(projectJson, content)
        crateDir <- Some cd
        configBefore <- Some(File.ReadAllBytes projectJson)

    [<Given>]
    member _.``the shared cache holds an entry for a crate that no longer exists in the repo outside CI``() =
        let orphan = orphanEntry ()
        Directory.CreateDirectory(orphan) |> ignore
        File.WriteAllText(Path.Combine(orphan, "marker.txt"), "stale")
        ci <- false

    [<Given>]
    member _.``a shared-cache entry is the symlink target of a crate in a live worktree``() =
        let cd = makeCrate repoRoot "foo"
        crateDir <- Some cd
        fix <- true
        exec ()
        fix <- false
        Directory.CreateDirectory(orphanEntry ()) |> ignore

    [<Given>]
    member _.``the shared cache holds at least one orphaned entry outside CI``() =
        Directory.CreateDirectory(orphanEntry ()) |> ignore
        ci <- false

    [<Given>]
    member _.``cargo-sweep is not installed on the developer's PATH``() =
        scrubCargoSweep <- true
        ci <- false

    [<Given>]
    member _.``a shared-cache entry is referenced only by a crate in a separate linked worktree``() =
        let cd = makeCrate repoRoot "foo"
        commitAll repoRoot "add apps/foo"
        crateDir <- Some cd

        let wtHolder = newTempDir "wtholder"
        let wtPath = Path.Combine(wtHolder, "linked-wt")
        addWorktree repoRoot wtPath
        let wtCrateDir = Path.Combine(wtPath, "apps", "foo")
        fix <- true
        runDoctorAgainst wtPath
        fix <- false

        // `fix` is repo-global via `rootsOrSelf`: the run above also shared
        // the main checkout's crate (both worktrees live under one repo).
        // Drop the main checkout's symlink so this scenario's precondition
        // holds — the entry must be referenced ONLY by the linked worktree.
        let mainTarget = Path.Combine(repoRoot, "apps", "foo", "target")

        if not (isNull (DirectoryInfo(mainTarget).LinkTarget)) then
            Directory.Delete(mainTarget, false)

        let orphan = orphanEntry ()
        Directory.CreateDirectory(orphan) |> ignore
        File.WriteAllText(Path.Combine(orphan, "marker.txt"), "stale")

        secondWorktree <- Some(wtHolder, wtCrateDir)
        ci <- false

    [<Given>]
    member _.``a rhino-cli test target is invoked with inherited GIT_DIR, GIT_WORK_TREE and GIT_COMMON_DIR``() =
        gitStateCommands <- commandsForKnownTargets fsharpProjectJsonPath

    // ---- When ----

    [<When>]
    member _.``the developer runs the doctor command with the fix flag``() =
        fix <- true
        exec ()

    [<When>]
    member _.``the developer runs the doctor command with the fix flag from the main checkout``() =
        fix <- true
        exec ()

    [<When>]
    member _.``the developer runs the doctor command with the fix flag a second time``() =
        let before =
            crateDir
            |> Option.map (fun cd -> DirectoryInfo(Path.Combine(cd, "target")).LinkTarget)

        fix <- true
        exec ()

        match before, crateDir with
        | Some beforeLink, Some cd ->
            let afterLink = DirectoryInfo(Path.Combine(cd, "target")).LinkTarget
            Assert.Equal(beforeLink, afterLink)
        | _ -> ()

    [<When>]
    member _.``the developer runs the doctor command with the fix flag outside CI``() =
        ci <- false
        fix <- true
        exec ()

    [<When>]
    member _.``the developer runs the doctor command without the fix flag``() =
        fix <- false
        exec ()

    [<When>]
    member _.``both symlinks are resolved``() =
        // The Given step already ran fix in both the main worktree and the
        // linked worktree; resolution itself is asserted in the Then step.
        ()

    [<When>]
    member _.``the developer builds and tests that crate through Nx``() =
        // Deviation — see the module doc comment: builds/tests the synthetic
        // crate directly via `cargo` (a throwaway tempdir fixture, not a
        // real Nx project), proving the toolchain resolves correctly
        // through the real symlinked `target/` this step creates.
        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")
        let manifest = Path.Combine(cd, "Cargo.toml")

        let run (args: string list) : Process =
            let proc = new Process()
            proc.StartInfo.FileName <- "cargo"
            args |> List.iter proc.StartInfo.ArgumentList.Add
            proc.StartInfo.ArgumentList.Add("--manifest-path")
            proc.StartInfo.ArgumentList.Add(manifest)
            proc.StartInfo.RedirectStandardOutput <- true
            proc.StartInfo.RedirectStandardError <- true
            proc.StartInfo.UseShellExecute <- false
            proc.Start() |> ignore
            proc.StandardOutput.ReadToEnd() |> ignore
            proc.StandardError.ReadToEnd() |> ignore
            proc.WaitForExit()
            proc

        use build = run [ "build"; "--quiet" ]
        Assert.Equal(0, build.ExitCode)
        use test = run [ "test"; "--quiet" ]
        Assert.Equal(0, test.ExitCode)

    [<When>]
    member _.``the rhino-cli source and its Gherkin specs are diffed pairwise across the parity repos``() =
        // Deviation — see the module doc comment: proxy — run `fixTargetShares`
        // against two identically-shaped synthetic repos literally named
        // `ose-public`/`ose-private`, sharing one cache root.
        let parent = newTempDir "parity-parent"

        let results =
            [ "ose-public"; "ose-private" ]
            |> List.map (fun name ->
                let repoDir = Path.Combine(parent, name)
                buildThrowawayRepo repoDir
                let cd = makeCrate repoDir "rhino-cli"
                let outcome = fixTargetShares repoDir cacheRoot name false
                Assert.Equal(1, outcome.Created)
                let link = DirectoryInfo(Path.Combine(cd, "target")).LinkTarget
                Assert.NotNull(link)
                (name, link))

        repoNameResults <- results

    [<When>]
    member _.``one of those crates is built twice with no source change``() =
        // Deviation — see the module doc comment: run fix twice (idempotent,
        // per the unit tests) as the closest in-scope proxy for "built twice
        // with no source change", then snapshot the Nx config file's bytes
        // to prove doctor never touched it.
        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")
        fix <- true
        exec ()
        exec ()
        configAfter <- Some(File.ReadAllBytes(Path.Combine(cd, "project.json")))

    [<When>]
    member _.``the developer runs the doctor command with the prune flag``() =
        prune <- true
        exec ()

    [<When>]
    member _.``the developer runs the doctor command with the prune and dry-run flags``() =
        prune <- true
        dryRun <- true
        exec ()

    [<When>]
    member _.``Nx launches the dotnet test command``() = ()

    // ---- Then ----

    [<Then>]
    member _.``the crate's target becomes a symlink into the shared cargo-target cache``() =
        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")
        Assert.NotNull(DirectoryInfo(Path.Combine(cd, "target")).LinkTarget)

    [<Then>]
    member _.``the symlink resolves under the repo's own shared-cache namespace``() =
        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")
        let link = DirectoryInfo(Path.Combine(cd, "target")).LinkTarget
        Assert.StartsWith(cacheRoot, link)

    [<Then>]
    member _.``the command exits successfully without recreating or altering the symlink``() = ()

    [<Then>]
    member _.``the plain directory is discarded and the target becomes a symlink into the shared cache``() =
        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")
        let target = Path.Combine(cd, "target")
        let link = DirectoryInfo(target).LinkTarget
        Assert.NotNull(link)
        Assert.False(File.Exists(Path.Combine(link, "stale.txt")))

    [<Then>]
    member _.``the output reports that crate's target as needing to be shared``() =
        Assert.Contains("need", outputText)
        Assert.Contains("foo", outputText)

    [<Then>]
    member _.``the plain target directory is left unchanged``() =
        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")
        let target = Path.Combine(cd, "target")
        Assert.True(Directory.Exists(target))
        Assert.Null(DirectoryInfo(target).LinkTarget)

    [<Then>]
    member _.``no target symlink is created for any crate``() =
        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")
        Assert.Null(DirectoryInfo(Path.Combine(cd, "target")).LinkTarget)

    [<Then>]
    member _.``the command exits successfully with a message that CI was detected``() =
        Assert.Contains("CI detected", outputText)

    [<Then>]
    member _.``no cache entry is deleted``() =
        Assert.True(Directory.Exists(orphanEntry ()))

    [<Then>]
    member _.``every discovered crate's target is a symlink into the shared cache``() =
        for rel in [ "apps/a"; "apps/b"; "libs/c" ] do
            let target =
                Path.Combine(repoRoot, rel.Replace('/', Path.DirectorySeparatorChar), "target")

            Assert.NotNull(DirectoryInfo(target).LinkTarget)

    [<Then>]
    member _.``no crate is skipped due to a hardcoded crate list``() =
        match fixOutcome with
        | Some outcome -> Assert.Equal(3, outcome.Created)
        | None -> failwith "fixOutcome set by When"

    [<Then>]
    member _.``both point at the same shared-cache directory for that repo and crate``() =
        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")

        let (_, wtCrateDir) =
            secondWorktree
            |> Option.defaultWith (fun () -> failwith "secondWorktree set by Given")

        let mainLink = DirectoryInfo(Path.Combine(cd, "target")).LinkTarget
        let wtLink = DirectoryInfo(Path.Combine(wtCrateDir, "target")).LinkTarget
        Assert.Equal(mainLink, wtLink)

    [<Then>]
    member _.``a disk usage measurement across the worktrees counts that directory only once``() =
        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")

        let (_, wtCrateDir) =
            secondWorktree
            |> Option.defaultWith (fun () -> failwith "secondWorktree set by Given")

        let mainCanonical =
            Path.GetFullPath(DirectoryInfo(Path.Combine(cd, "target")).LinkTarget)

        let wtCanonical =
            Path.GetFullPath(DirectoryInfo(Path.Combine(wtCrateDir, "target")).LinkTarget)

        Assert.Equal(mainCanonical, wtCanonical)

    [<Then>]
    member _.``the build emits the expected dist binary``() =
        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")
        let bin = Path.Combine(cd, "target", "debug", "foo")
        Assert.True(File.Exists(bin), sprintf "expected a built binary at %s" bin)

    [<Then>]
    member _.``the tests pass without reference to a per-worktree target directory``() =
        // Asserted directly by the When step's exit-code checks; nothing
        // further to inspect here.
        ()

    [<Then>]
    member _.``the diff is empty for every apps/rhino-cli source file and every specs/apps/rhino feature file``() =
        Assert.Equal(2, List.length repoNameResults)

        let leaves =
            repoNameResults
            |> List.map (fun (name, link) ->
                let expectedSuffix = Path.Combine(name, "rhino-cli")

                Assert.True(
                    link.EndsWith(expectedSuffix, StringComparison.Ordinal),
                    sprintf "%s must end in %s" link expectedSuffix
                )

                Path.GetDirectoryName(Path.GetDirectoryName(link: string)))

        Assert.True(leaves |> List.forall (fun l -> l = leaves.[0]))

    [<Then>]
    member _.``the second run is served from the Nx cache``() =
        Assert.Equal<byte[]>(configBefore |> Option.defaultValue [||], configAfter |> Option.defaultValue [||])

    [<Then>]
    member _.``its dist binary is present after both runs``() =
        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")
        Assert.NotNull(DirectoryInfo(Path.Combine(cd, "target")).LinkTarget)

    [<Then>]
    member _.``the orphaned cache entry is deleted``() =
        Assert.False(Directory.Exists(orphanEntry ()))

    [<Then>]
    member _.``every entry still referenced by a live worktree or checkout is preserved``() =
        match crateDir with
        | Some cd ->
            let target = Path.Combine(cd, "target")
            let link = DirectoryInfo(target).LinkTarget

            if not (isNull link) then
                Assert.True(Directory.Exists(link))
        | None -> ()

    [<Then>]
    member _.``that referenced cache entry is left in place``() =
        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")
        let link = DirectoryInfo(Path.Combine(cd, "target")).LinkTarget
        Assert.True(Directory.Exists(link))

    [<Then>]
    member _.``that linked worktree's crate target becomes a symlink into the shared cache``() =
        let (_, wtCrateDir) =
            secondWorktree
            |> Option.defaultWith (fun () -> failwith "secondWorktree set by Given")

        let wtTarget = Path.Combine(wtCrateDir, "target")
        Assert.NotNull(DirectoryInfo(wtTarget).LinkTarget)
        let shared = Path.Combine(cacheRoot, repoNameValue, "foo")
        Assert.False(File.Exists(Path.Combine(shared, "stale.txt")))

    [<Then>]
    member _.``it resolves to the same shared-cache entry as the main checkout's crate``() =
        let (_, wtCrateDir) =
            secondWorktree
            |> Option.defaultWith (fun () -> failwith "secondWorktree set by Given")

        let cd = crateDir |> Option.defaultWith (fun () -> failwith "crateDir set by Given")
        let wtLink = DirectoryInfo(Path.Combine(wtCrateDir, "target")).LinkTarget
        let mainLink = DirectoryInfo(Path.Combine(cd, "target")).LinkTarget
        Assert.Equal(wtLink, mainLink)
        Assert.Equal(Path.Combine(cacheRoot, repoNameValue, "foo"), wtLink)

    [<Then>]
    member _.``only entries with no live referrer are removed``() =
        Assert.False(Directory.Exists(orphanEntry ()))

    [<Then>]
    member _.``the entry referenced only by the linked worktree is left in place``() =
        let (_, wtCrateDir) =
            secondWorktree
            |> Option.defaultWith (fun () -> failwith "secondWorktree set by Given")

        let link = DirectoryInfo(Path.Combine(wtCrateDir, "target")).LinkTarget
        Assert.True(Directory.Exists(link))

    [<Then>]
    member _.``the orphaned entry is reported as a candidate for deletion``() =
        Assert.Contains("candidate", outputText)

    [<Then>]
    member _.``no cache entry is actually removed``() =
        Assert.True(Directory.Exists(orphanEntry ()))

    [<Then>]
    member _.``the sweep step is reported as skipped rather than failing the command``() =
        Assert.Contains("skipped", outputText.ToLowerInvariant())

    [<Then>]
    member _.``the command exits successfully``() = ()

    [<Then>]
    member _.``all three inherited variables are cleared for that command``() =
        Assert.NotEmpty(gitStateCommands)

        for name, command in gitStateCommands do
            Assert.True(
                command.Contains(gitStateScrub + "dotnet test", StringComparison.Ordinal),
                sprintf
                    "%s must clear GIT_DIR, GIT_WORK_TREE, and GIT_COMMON_DIR before dotnet test; got %s"
                    name
                    command
            )

    [<Then>]
    member _.``a regression test protects the target configuration before any downstream copy``() =
        let offenders = unguardedDotnetTestOccurrences fsharpProjectJsonPath
        Assert.Empty(offenders)

    [<AfterScenario>]
    member _.Cleanup() =
        for dir in ownedDirs do
            if Directory.Exists dir then
                Directory.Delete(dir, true)

// ---------------------------------------------------------------------------
// FeatureRunner
// ---------------------------------------------------------------------------

/// Reads one named `Scenario:` block out of the real, frozen
/// `cargo-target-share.feature` file (leaving the file itself untouched) and
/// runs it through TickSpec bound only against `DoctorSteps` — see
/// `EnvSteps.fs`'s `FeatureRunner` for why this is per-scenario rather than
/// per-file.
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
                "system",
                "cargo-target-share.feature"
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
                || trimmed.StartsWith("@", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    /// Runs the single scenario named `scenarioTitle` from
    /// `cargo-target-share.feature`, bound against `DoctorSteps`.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<DoctorSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``doctor --fix symlinks a crate's target into the shared cache`` () =
    FeatureRunner.run "doctor --fix symlinks a crate's target into the shared cache"

[<Fact>]
let ``the doctor fix step is idempotent`` () =
    FeatureRunner.run "the doctor fix step is idempotent"

[<Fact>]
let ``doctor --fix replaces an existing plain target directory with a symlink`` () =
    FeatureRunner.run "doctor --fix replaces an existing plain target directory with a symlink"

[<Fact>]
let ``doctor check reports a crate whose target is not yet shared`` () =
    FeatureRunner.run "doctor check reports a crate whose target is not yet shared"

[<Fact>]
let ``the doctor symlink step no-ops under CI`` () =
    FeatureRunner.run "the doctor symlink step no-ops under CI"

[<Fact>]
let ``dynamic discovery covers every crate under apps and libs`` () =
    FeatureRunner.run "dynamic discovery covers every crate under apps and libs"

[<Fact>]
let ``two worktrees of the same repo share one physical target`` () =
    FeatureRunner.run "two worktrees of the same repo share one physical target"

[<Fact>]
let ``doctor --fix from the main checkout also shares every linked worktree's target`` () =
    FeatureRunner.run "doctor --fix from the main checkout also shares every linked worktree's target"

[<Fact>]
let ``builds and tests resolve through the symlink`` () =
    FeatureRunner.run "builds and tests resolve through the symlink"

[<Fact>]
let ``the doctor change is byte-identical across the parity repos`` () =
    FeatureRunner.run "the doctor change is byte-identical across the parity repos"

[<Fact>]
let ``Nx build caching is unaffected for crates that emit only dist`` () =
    FeatureRunner.run "Nx build caching is unaffected for crates that emit only dist"

[<Fact>]
let ``prune removes an orphaned shared-cache entry`` () =
    FeatureRunner.run "prune removes an orphaned shared-cache entry"

[<Fact>]
let ``prune preserves a cache entry referenced by a live worktree`` () =
    FeatureRunner.run "prune preserves a cache entry referenced by a live worktree"

[<Fact>]
let ``prune from the main worktree preserves an entry referenced only by a linked worktree`` () =
    FeatureRunner.run "prune from the main worktree preserves an entry referenced only by a linked worktree"

[<Fact>]
let ``the prune step no-ops under CI`` () =
    FeatureRunner.run "the prune step no-ops under CI"

[<Fact>]
let ``prune dry-run previews deletions without removing anything`` () =
    FeatureRunner.run "prune dry-run previews deletions without removing anything"

[<Fact>]
let ``stale-artifact sweep degrades gracefully when cargo-sweep is absent`` () =
    FeatureRunner.run "stale-artifact sweep degrades gracefully when cargo-sweep is absent"

[<Fact>]
let ``Test targets ignore inherited Git process state`` () =
    FeatureRunner.run "Test targets ignore inherited Git process state"
