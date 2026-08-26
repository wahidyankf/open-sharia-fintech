/// Plain xunit tests for `RhinoCli.Application.Parity` — the checksum
/// -manifest port of `apps/rhino-cli/src/application/parity.rs`. Each test
/// builds its own throwaway `git init` fixture rather than touching this
/// checkout's own repository, since `generateAtRoot`/`validateAtRoot` both
/// read and write real Git index/worktree state.
module RhinoCli.Tests.Unit.Steps.ParityUnitTests

open System
open System.Diagnostics
open System.IO
open Xunit
open RhinoCli.Application.Parity

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
let private newGitFixture () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-parity-unit-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    runGit dir [ "init"; "-q"; "-b"; "main" ]
    runGit dir [ "config"; "user.name"; "Rhino CLI Test" ]
    runGit dir [ "config"; "user.email"; "rhino-cli-test@example.invalid" ]
    // The real repo always has `apps/rhino-cli/` (the manifest's own parent
    // directory) present; a fixture with no boundary files at all would
    // otherwise fail to write the manifest for a reason unrelated to what
    // each test actually exercises.
    Directory.CreateDirectory(Path.Combine(dir, "apps", "rhino-cli")) |> ignore
    dir

let private writeFile (root: string) (relativePath: string) (content: string) =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
    File.WriteAllText(full, content)

let private readManifest (root: string) : string =
    File.ReadAllText(Path.Combine(root, ManifestPath))

// ---- generate / validate round trip ----

[<Fact>]
let ``generateAtRoot succeeds with an empty manifest when no boundary path matches`` () =
    let root = newGitFixture ()

    match generateAtRoot root with
    | Ok() -> Assert.Equal("", readManifest root)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateAtRoot succeeds immediately after generateAtRoot with no boundary files`` () =
    let root = newGitFixture ()
    generateAtRoot root |> ignore
    runGit root [ "add"; "-A" ]

    match validateAtRoot root with
    | Ok() -> ()
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``generateAtRoot and validateAtRoot round-trip a real staged boundary file`` () =
    let root = newGitFixture ()
    writeFile root "apps/rhino-cli/LICENSE" "MIT\n"
    runGit root [ "add"; "-A" ]

    match generateAtRoot root with
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    | Ok() ->
        Assert.Contains("apps/rhino-cli/LICENSE", readManifest root)
        runGit root [ "add"; "-A" ]

        match validateAtRoot root with
        | Ok() -> ()
        | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

// ---- worktree-vs-index drift ----

[<Fact>]
let ``generateAtRoot fails when a boundary file's worktree copy drifts from the Git index`` () =
    let root = newGitFixture ()
    writeFile root "apps/rhino-cli/LICENSE" "MIT\n"
    runGit root [ "add"; "-A" ]
    writeFile root "apps/rhino-cli/LICENSE" "changed after staging\n"

    match generateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for worktree/index drift")
    | Error message ->
        Assert.Contains("differs from the Git index", message)
        Assert.Contains("rhino-cli parity manifest generate", message)

// ---- symlink rejection ----

[<Fact>]
let ``generateAtRoot rejects a symlink inside the boundary`` () =
    let root = newGitFixture ()
    let targetPath = Path.Combine(root, "outside-target.txt")
    File.WriteAllText(targetPath, "target\n")
    let linkPath = Path.Combine(root, "apps", "rhino-cli", "LICENSE")
    Directory.CreateDirectory(Path.GetDirectoryName(linkPath)) |> ignore

    File.CreateSymbolicLink(linkPath, targetPath) |> ignore
    runGit root [ "add"; "-A" ]

    match generateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for a symlinked boundary path")
    | Error message -> Assert.Contains("is a symlink in the Git index", message)

// ---- manifest itself drifting from the Git index ----

[<Fact>]
let ``validateAtRoot fails when the manifest's worktree copy drifts from the Git index`` () =
    let root = newGitFixture ()
    generateAtRoot root |> ignore
    runGit root [ "add"; "-A" ]
    File.WriteAllText(Path.Combine(root, ManifestPath), "not what was staged\n")

    match validateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for a drifted manifest file")
    | Error message -> Assert.Contains("differs from the Git index", message)

// ---- non-canonical manifest text ----

[<Fact>]
let ``validateAtRoot fails when the staged manifest is not the canonical rendering`` () =
    let root = newGitFixture ()
    writeFile root "apps/rhino-cli/LICENSE" "MIT\n"
    runGit root [ "add"; "-A" ]
    generateAtRoot root |> ignore
    let canonical = readManifest root
    // A trailing blank line: `parseManifest` filters empty lines, so every
    // declared hash still parses and matches `actual` exactly — this
    // exercises the *final* "not the canonical sorted checksum manifest"
    // literal-text check specifically, not any earlier drift/missing-entry
    // branch.
    File.WriteAllText(Path.Combine(root, ManifestPath), canonical + "\n")
    runGit root [ "add"; "-A" ]

    match validateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for a non-canonical manifest")
    | Error message -> Assert.Contains("not the canonical sorted checksum manifest", message)

// ---- missing / unreadable manifest ----

[<Fact>]
let ``validateAtRoot fails when the manifest file does not exist`` () =
    let root = newGitFixture ()

    match validateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for a missing manifest file")
    | Error message -> Assert.Contains(ManifestPath, message)

// ---- non-git repoRoot ----

[<Fact>]
let ``generateAtRoot fails when repoRoot is not a Git repository`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-cli-parity-non-git-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(root) |> ignore

    match generateAtRoot root with
    | Ok() -> Assert.Fail("expected Error outside any Git repository")
    | Error message -> Assert.Contains("git ls-files", message)
