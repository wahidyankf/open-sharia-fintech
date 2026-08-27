/// Plain xunit tests for `RhinoCli.Application.Doctor`'s pure/testable
/// cargo target-share helpers — behaviour with no dedicated Gherkin scenario,
/// or exercised only indirectly there (mirrors the rationale
/// `EnvStagedGuardUnitTests.fs`'s module doc comment states for its own split
/// from `DoctorSteps.fs`). Ported from
/// `apps/rhino-cli/src/application/doctor/target_share.rs`'s
/// `#[cfg(test)] mod tests`.
///
/// `sweep_scope_is_repo_namespaced` is not ported: `sweepScope` is a private
/// helper (not part of `Doctor`'s public surface, unlike Rust's
/// `pub(crate)`-equivalent test-only visibility), and the property it guards
/// — the sweep never touching a sibling repo's cache namespace — is already
/// exercised end-to-end by every `pruneOrphans`/`sweepStale` test below,
/// which all pass a repo-scoped `cacheRoot/repoName` path.
module RhinoCli.Tests.Unit.Steps.DoctorUnitTests

open System
open System.Diagnostics
open System.IO
open Xunit
open RhinoCli.Application.Doctor

// ---- isCi ----

[<Fact>]
let ``isCi is true when either signal is set`` () =
    Assert.True(isCi true false, "CI set alone must report true")
    Assert.True(isCi false true, "GITHUB_ACTIONS set alone must report true")
    Assert.True(isCi true true, "both set must report true")
    Assert.False(isCi false false, "neither set must report false")

// ---- discoverCrates ----

let private writeCargoToml (dir: string) =
    Directory.CreateDirectory(dir) |> ignore
    File.WriteAllText(Path.Combine(dir, "Cargo.toml"), "[package]\nname = \"x\"\n")

[<Fact>]
let ``discoverCrates walks apps and libs`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-discover-" + Guid.NewGuid().ToString("N"))

    try
        writeCargoToml (Path.Combine(root, "apps", "a"))
        writeCargoToml (Path.Combine(root, "apps", "b"))
        writeCargoToml (Path.Combine(root, "libs", "c"))
        // A non-crate directory (no Cargo.toml) must NOT be discovered.
        Directory.CreateDirectory(Path.Combine(root, "apps", "not-a-crate")) |> ignore

        let found = discoverCrates root |> List.sort

        let expected =
            [ Path.Combine(root, "apps", "a")
              Path.Combine(root, "apps", "b")
              Path.Combine(root, "libs", "c") ]
            |> List.sort

        Assert.Equal<string list>(expected, found)
    finally
        Directory.Delete(root, true)

// ---- cacheRootFrom / repoName / sharedTargetPath ----

[<Fact>]
let ``cacheRootFrom honors an explicit override`` () =
    Assert.Equal("/override/dir", cacheRootFrom (Some "/override/dir") None)

[<Fact>]
let ``cacheRootFrom falls back to home cache dir when no override is given`` () =
    Assert.Equal(Path.Combine("/home/dev", ".cache", "ose-cargo-target"), cacheRootFrom None (Some "/home/dev"))

[<Fact>]
let ``repoName returns the basename of the common dir's parent`` () =
    Assert.Equal("my-repo", repoName (Path.Combine("/some/path/my-repo", ".git")))

[<Fact>]
let ``sharedTargetPath composes cache root, repo name, and crate leaf`` () =
    Assert.Equal(
        Path.Combine("/cache", "my-repo", "rhino-cli"),
        sharedTargetPath "/cache" "my-repo" (Path.Combine("/some/path/my-repo", "apps", "rhino-cli"))
    )

// ---- git fixture helpers (mirrors ParityUnitTests.fs's own self-contained fixture) ----

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

/// A fresh `git init` repository with a committable identity configured
/// locally (never touches global/user git config).
let private newGitFixture (prefix: string) : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-" + prefix + "-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    runGit dir [ "init"; "-q"; "-b"; "main" ]
    runGit dir [ "config"; "user.name"; "Rhino CLI Test" ]
    runGit dir [ "config"; "user.email"; "rhino-cli-test@example.invalid" ]
    File.WriteAllText(Path.Combine(dir, "README.md"), "throwaway fixture")
    runGit dir [ "add"; "." ]
    runGit dir [ "commit"; "-m"; "init" ]
    dir

let private addWorktree (repoDir: string) (worktreeDir: string) : unit =
    runGit repoDir [ "worktree"; "add"; "--detach"; worktreeDir ]

let private makeCrate (repoRoot: string) (name: string) : string =
    let crateDir = Path.Combine(repoRoot, "apps", name)
    writeCargoToml crateDir
    crateDir

// ---- checkTargetShares ----

[<Fact>]
let ``checkTargetShares reports unshared target without mutating it`` () =
    let repoRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-check-" + Guid.NewGuid().ToString("N"))

    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-cache-" + Guid.NewGuid().ToString("N"))

    try
        let crateDir = makeCrate repoRoot "foo"
        let targetDir = Path.Combine(crateDir, "target")
        Directory.CreateDirectory(targetDir) |> ignore
        File.WriteAllText(Path.Combine(targetDir, "marker.txt"), "stale")

        let report = checkTargetShares repoRoot cacheRoot "myrepo" false
        Assert.Equal(1, List.length report)
        Assert.Equal(crateDir, report.[0].CrateDir)
        Assert.Equal(Path.Combine(cacheRoot, "myrepo", "foo"), report.[0].SharedPath)

        // No mutation: the plain directory and its stale marker file survive.
        Assert.True(Directory.Exists(targetDir))
        Assert.True(File.Exists(Path.Combine(targetDir, "marker.txt")))

        let ciReport = checkTargetShares repoRoot cacheRoot "myrepo" true
        Assert.Empty(ciReport)
    finally
        Directory.Delete(repoRoot, true)

        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

// ---- fixTargetShares ----

[<Fact>]
let ``fixTargetShares creates a symlink into the shared cache`` () =
    let repoRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-fix-" + Guid.NewGuid().ToString("N"))

    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-cache-" + Guid.NewGuid().ToString("N"))

    try
        let crateDir = makeCrate repoRoot "foo"

        let outcome = fixTargetShares repoRoot cacheRoot "myrepo" false
        Assert.Equal(1, outcome.Created)

        let target = Path.Combine(crateDir, "target")
        let expectedShared = Path.Combine(cacheRoot, "myrepo", "foo")
        Assert.NotNull(DirectoryInfo(target).LinkTarget)
        Assert.Equal(expectedShared, DirectoryInfo(target).LinkTarget)
    finally
        Directory.Delete(repoRoot, true)

        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

[<Fact>]
let ``fixTargetShares is idempotent on a second run`` () =
    let repoRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-fix2-" + Guid.NewGuid().ToString("N"))

    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-cache-" + Guid.NewGuid().ToString("N"))

    try
        let crateDir = makeCrate repoRoot "foo"

        let first = fixTargetShares repoRoot cacheRoot "myrepo" false
        Assert.Equal(1, first.Created)

        let target = Path.Combine(crateDir, "target")
        let linkBefore = DirectoryInfo(target).LinkTarget

        let second = fixTargetShares repoRoot cacheRoot "myrepo" false
        Assert.Equal(1, second.AlreadyCorrect)
        Assert.Equal(0, second.Created)

        Assert.Equal(linkBefore, DirectoryInfo(target).LinkTarget)
    finally
        Directory.Delete(repoRoot, true)

        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

[<Fact>]
let ``fixTargetShares replaces a plain target directory with a symlink`` () =
    let repoRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-fix3-" + Guid.NewGuid().ToString("N"))

    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-cache-" + Guid.NewGuid().ToString("N"))

    try
        let crateDir = makeCrate repoRoot "foo"
        let target = Path.Combine(crateDir, "target")
        Directory.CreateDirectory(target) |> ignore
        File.WriteAllText(Path.Combine(target, "stale.txt"), "stale artifact")

        let outcome = fixTargetShares repoRoot cacheRoot "myrepo" false
        Assert.Equal(1, outcome.ReplacedPlainDir)
        Assert.NotNull(DirectoryInfo(target).LinkTarget)

        let sharedPath = Path.Combine(cacheRoot, "myrepo", "foo")
        Assert.False(File.Exists(Path.Combine(sharedPath, "stale.txt")))
    finally
        Directory.Delete(repoRoot, true)

        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

[<Fact>]
let ``fixTargetShares no-ops under CI`` () =
    let repoRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-fixci-" + Guid.NewGuid().ToString("N"))

    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-cache-" + Guid.NewGuid().ToString("N"))

    try
        let crateDir = makeCrate repoRoot "foo"
        let target = Path.Combine(crateDir, "target")
        Directory.CreateDirectory(target) |> ignore

        let outcome = fixTargetShares repoRoot cacheRoot "myrepo" true
        Assert.True(outcome.SkippedCi)
        Assert.Equal(0, outcome.Created)
        Assert.Equal(0, outcome.ReplacedPlainDir)
        Assert.True(Directory.Exists(target))
        Assert.Null(DirectoryInfo(target).LinkTarget)
    finally
        Directory.Delete(repoRoot, true)

        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

[<Fact>]
let ``fixTargetShares run from the main checkout also shares a linked worktree's crate`` () =
    let repo = newGitFixture "fix-linked"

    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-cache-" + Guid.NewGuid().ToString("N"))

    let linked =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-linked-" + Guid.NewGuid().ToString("N"))

    try
        makeCrate repo "foo" |> ignore
        addWorktree repo linked
        let linkedCrate = makeCrate linked "foo"
        let linkedTarget = Path.Combine(linkedCrate, "target")
        Directory.CreateDirectory(linkedTarget) |> ignore

        let outcome = fixTargetShares repo cacheRoot "myrepo" false
        Assert.Equal(2, outcome.Created)

        let shared = Path.Combine(cacheRoot, "myrepo", "foo")
        Assert.Equal(shared, DirectoryInfo(linkedTarget).LinkTarget)
        Assert.Equal(shared, DirectoryInfo(Path.Combine(repo, "apps", "foo", "target")).LinkTarget)
    finally
        (try
            runGit repo [ "worktree"; "remove"; "--force"; linked ]
         with _ ->
             ())

        Directory.Delete(repo, true)

        if Directory.Exists(linked) then
            Directory.Delete(linked, true)

        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

// ---- pruneOrphans ----

[<Fact>]
let ``pruneOrphans removes an orphaned shared-cache entry`` () =
    let repo = newGitFixture "prune-orphan"

    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-cache-" + Guid.NewGuid().ToString("N"))

    try
        let orphanDir = Path.Combine(cacheRoot, "myrepo", "orphan-crate")
        Directory.CreateDirectory(orphanDir) |> ignore
        File.WriteAllText(Path.Combine(orphanDir, "marker.txt"), "stale")

        let outcome = pruneOrphans repo cacheRoot "myrepo" false false
        Assert.Equal<string list>([ orphanDir ], outcome.Deleted)
        Assert.False(Directory.Exists(orphanDir))
    finally
        Directory.Delete(repo, true)

        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

[<Fact>]
let ``pruneOrphans fails closed when worktree enumeration fails`` () =
    let nonRepo =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-nonrepo-" + Guid.NewGuid().ToString("N"))

    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-cache-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(nonRepo) |> ignore

    try
        let entryDir = Path.Combine(cacheRoot, "myrepo", "some-crate")
        Directory.CreateDirectory(entryDir) |> ignore
        File.WriteAllText(Path.Combine(entryDir, "marker.txt"), "keep")

        let outcome = pruneOrphans nonRepo cacheRoot "myrepo" false false
        Assert.True(outcome.EnumerationFailed)
        Assert.Empty(outcome.Deleted)
        Assert.True(Directory.Exists(entryDir))
    finally
        Directory.Delete(nonRepo, true)

        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

[<Fact>]
let ``pruneOrphans preserves an entry referenced by a live worktree`` () =
    let repo = newGitFixture "prune-live"

    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-cache-" + Guid.NewGuid().ToString("N"))

    try
        let liveDir = Path.Combine(cacheRoot, "myrepo", "foo")
        Directory.CreateDirectory(liveDir) |> ignore

        let crateDir = makeCrate repo "foo"

        Directory.CreateSymbolicLink(Path.Combine(crateDir, "target"), liveDir)
        |> ignore

        let outcome = pruneOrphans repo cacheRoot "myrepo" false false
        Assert.Empty(outcome.Deleted)
        Assert.True(Directory.Exists(liveDir))
    finally
        Directory.Delete(repo, true)

        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

[<Fact>]
let ``pruneOrphans no-ops under CI`` () =
    let repoRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-pruneci-" + Guid.NewGuid().ToString("N"))

    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-cache-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(repoRoot) |> ignore

    try
        let orphanDir = Path.Combine(cacheRoot, "myrepo", "orphan-crate")
        Directory.CreateDirectory(orphanDir) |> ignore

        let outcome = pruneOrphans repoRoot cacheRoot "myrepo" false true
        Assert.True(outcome.SkippedCi)
        Assert.Empty(outcome.Deleted)
        Assert.True(Directory.Exists(orphanDir))
    finally
        Directory.Delete(repoRoot, true)

        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

[<Fact>]
let ``pruneOrphans dry-run reports without deleting`` () =
    let repo = newGitFixture "prune-dry"

    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-cache-" + Guid.NewGuid().ToString("N"))

    try
        let orphanDir = Path.Combine(cacheRoot, "myrepo", "orphan-crate")
        Directory.CreateDirectory(orphanDir) |> ignore

        let outcome = pruneOrphans repo cacheRoot "myrepo" true false
        Assert.Equal<string list>([ orphanDir ], outcome.Candidates)
        Assert.Empty(outcome.Deleted)
        Assert.True(Directory.Exists(orphanDir))
    finally
        Directory.Delete(repo, true)

        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

// ---- sweepStale ----

[<Fact>]
let ``sweepStale reports Skipped when cargo-sweep is absent`` () =
    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-sweep-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(cacheRoot) |> ignore

    try
        let outcome = sweepStale cacheRoot "myrepo" false false false
        Assert.True(outcome.Skipped)
        Assert.False(outcome.Ran)
    finally
        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

[<Fact>]
let ``sweepStale is CI-guarded even when cargo-sweep is present`` () =
    let cacheRoot =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-sweep2-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(cacheRoot) |> ignore

    try
        let outcome = sweepStale cacheRoot "myrepo" false true true
        Assert.True(outcome.SkippedCi)
        Assert.False(outcome.Ran)
        Assert.False(outcome.Skipped)
    finally
        if Directory.Exists(cacheRoot) then
            Directory.Delete(cacheRoot, true)

// ---- format* ----

[<Fact>]
let ``formatCheckReport reports CI skip`` () =
    Assert.Contains("CI detected", formatCheckReport [] true)

[<Fact>]
let ``formatCheckReport reports crates needing sharing`` () =
    let text =
        formatCheckReport
            [ { CrateDir = "apps/foo"
                SharedPath = "/cache/myrepo/foo" } ]
            false

    Assert.Contains("1 crate(s) need sharing", text)
    Assert.Contains("apps/foo", text)

[<Fact>]
let ``formatFixReport reports the created/already-correct/replaced counts`` () =
    let text =
        formatFixReport
            { Created = 1
              AlreadyCorrect = 2
              ReplacedPlainDir = 1
              SkippedCi = false }

    Assert.Contains("1 created", text)
    Assert.Contains("2 already correct", text)
    Assert.Contains("1 plain dir(s) replaced", text)

[<Fact>]
let ``formatPruneReport reports candidates under dry-run`` () =
    let text =
        formatPruneReport
            { Deleted = []
              Preserved = []
              Candidates = [ "/cache/myrepo/orphan" ]
              SkippedCi = false
              EnumerationFailed = false }
            true

    Assert.Contains("candidate", text)
    Assert.Contains("/cache/myrepo/orphan", text)

[<Fact>]
let ``formatSweepReport is empty when the sweep ran`` () =
    Assert.Equal(
        "",
        formatSweepReport
            { Skipped = false
              SkippedCi = false
              Ran = true }
    )
