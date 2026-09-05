/// Integration tests for `RhinoCli.Application.Parity` — the checksum
/// -manifest port of `apps/rhino-cli/src/application/parity.rs`. Each test
/// builds its own throwaway `git init` fixture rather than touching this
/// checkout's own repository, since `generateAtRoot`/`validateAtRoot` both
/// read and write real Git index/worktree state.
module RhinoCli.Tests.Integration.Steps.ParityResourceTests

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

// ---- edge cases reached through real Git state (no mocking) ----

/// Runs `git`, tolerating a non-zero exit — used only for the merge-conflict
/// fixture below, where the failing `merge` invocation is the point.
let private runGitIgnoringFailure (cwd: string) (args: string list) : unit =
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
    proc.StandardError.ReadToEnd() |> ignore
    proc.StandardOutput.ReadToEnd() |> ignore
    proc.WaitForExit()

[<Fact>]
let ``generateAtRoot fails when a boundary path's staged blob is missing from the object database`` () =
    let root = newGitFixture ()
    writeFile root "apps/rhino-cli/LICENSE" "MIT\n"
    runGit root [ "add"; "-A" ]

    runGit
        root
        [ "update-index"
          "--add"
          "--cacheinfo"
          "100644,1111111111111111111111111111111111111111,apps/rhino-cli/LICENSE" ]

    match generateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for a staged blob missing from the object database")
    | Error message -> Assert.Contains("git cat-file failed for", message)

[<Fact>]
let ``generateAtRoot fails when a merge leaves a boundary path with unresolved index stages`` () =
    let root = newGitFixture ()
    writeFile root "apps/rhino-cli/LICENSE" "base\n"
    runGit root [ "add"; "-A" ]
    runGit root [ "commit"; "-m"; "base" ]
    runGit root [ "checkout"; "-q"; "-b"; "feature" ]
    writeFile root "apps/rhino-cli/LICENSE" "feature change\n"
    runGit root [ "add"; "-A" ]
    runGit root [ "commit"; "-m"; "feature" ]
    runGit root [ "checkout"; "-q"; "main" ]
    writeFile root "apps/rhino-cli/LICENSE" "main change\n"
    runGit root [ "add"; "-A" ]
    runGit root [ "commit"; "-m"; "main" ]
    runGitIgnoringFailure root [ "merge"; "feature"; "--no-edit" ]

    match generateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for an unresolved merge conflict")
    | Error message -> Assert.Contains("has an unresolved Git index entry", message)

[<Fact>]
let ``generateAtRoot fails when a staged boundary file is missing from the worktree`` () =
    let root = newGitFixture ()
    writeFile root "apps/rhino-cli/LICENSE" "MIT\n"
    runGit root [ "add"; "-A" ]
    File.Delete(Path.Combine(root, "apps/rhino-cli/LICENSE"))

    match generateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for a staged file missing from the worktree")
    | Error message -> Assert.Contains("read staged parity boundary file", message)

[<Fact>]
let ``validateAtRoot fails when repoRoot is not a Git repository but a manifest file exists`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-cli-parity-non-git-validate-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(Path.Combine(root, "apps", "rhino-cli")) |> ignore
    File.WriteAllText(Path.Combine(root, ManifestPath), "")

    match validateAtRoot root with
    | Ok() -> Assert.Fail("expected Error outside any Git repository")
    | Error message -> Assert.Contains("git ls-files", message)

[<Fact>]
let ``validateAtRoot fails when the manifest file is not staged`` () =
    let root = newGitFixture ()
    File.WriteAllText(Path.Combine(root, ManifestPath), "")

    match validateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for an untracked manifest file")
    | Error message -> Assert.Contains("is not staged", message)

[<Fact>]
let ``validateAtRoot fails when the manifest declares a duplicate boundary path`` () =
    let root = newGitFixture ()
    writeFile root "apps/rhino-cli/LICENSE" "MIT\n"
    runGit root [ "add"; "-A" ]
    generateAtRoot root |> ignore
    let line = (readManifest root).Trim()
    File.WriteAllText(Path.Combine(root, ManifestPath), line + "\n" + line + "\n")
    runGit root [ "add"; "-A" ]

    match validateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for a duplicate manifest entry")
    | Error message -> Assert.Contains("duplicate boundary path", message)

[<Fact>]
let ``generateAtRoot fails when the manifest path collides with an existing directory`` () =
    let root = newGitFixture ()

    Directory.CreateDirectory(Path.Combine(root, "apps", "rhino-cli", "parity-manifest.sha256"))
    |> ignore

    match generateAtRoot root with
    | Ok() -> Assert.Fail("expected Error when the manifest path is a directory")
    | Error message -> Assert.Contains("atomically replace parity manifest", message)

[<Fact>]
let ``validateAtRoot fails when the staged manifest text is malformed`` () =
    let root = newGitFixture ()
    File.WriteAllText(Path.Combine(root, ManifestPath), "not a valid manifest line\n")
    runGit root [ "add"; "-A" ]

    match validateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for a malformed manifest line")
    | Error message -> Assert.Contains("expected '<sha256>", message)

[<Fact>]
let ``validateAtRoot fails when a boundary file drifts after the manifest itself is staged`` () =
    let root = newGitFixture ()
    writeFile root "apps/rhino-cli/LICENSE" "MIT\n"
    runGit root [ "add"; "-A" ]
    generateAtRoot root |> ignore
    runGit root [ "add"; "-A" ]
    writeFile root "apps/rhino-cli/LICENSE" "drifted after the manifest was staged\n"

    match validateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for a boundary file drifting after the manifest was staged")
    | Error message -> Assert.Contains("differs from the Git index", message)

[<Fact>]
let ``validateAtRoot fails when a boundary file's hash no longer matches the declared manifest entry`` () =
    let root = newGitFixture ()
    writeFile root "apps/rhino-cli/LICENSE" "v1\n"
    runGit root [ "add"; "-A" ]
    generateAtRoot root |> ignore
    runGit root [ "add"; "-A" ]
    runGit root [ "commit"; "-m"; "v1" ]
    writeFile root "apps/rhino-cli/LICENSE" "v2\n"
    runGit root [ "add"; "-A" ]

    match validateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for a hash drifted from the declared manifest entry")
    | Error message ->
        Assert.Contains("no longer matches", message)
        Assert.Contains("rhino-cli parity manifest generate", message)

[<Fact>]
let ``generateAtRoot and validateAtRoot round-trip a manifest with two boundary files`` () =
    // A single-entry manifest's `parseManifest` recursion only ever reaches
    // its `[] -> Ok acc` base case directly from the initial call — this
    // exercises the loop's second (successful-continuation) iteration too,
    // so the recursive `loop (lineNumber + 1) rest (Map.add path hash acc)`
    // call runs with a non-empty `rest`.
    let root = newGitFixture ()
    writeFile root "apps/rhino-cli/LICENSE" "MIT\n"
    writeFile root "apps/rhino-cli/project.json" "{}\n"
    runGit root [ "add"; "-A" ]

    match generateAtRoot root with
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    | Ok() ->
        Assert.Contains("apps/rhino-cli/LICENSE", readManifest root)
        Assert.Contains("apps/rhino-cli/project.json", readManifest root)
        runGit root [ "add"; "-A" ]

        match validateAtRoot root with
        | Ok() -> ()
        | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``validateAtRoot fails when a declared boundary path is missing from the current boundary`` () =
    let root = newGitFixture ()
    writeFile root "apps/rhino-cli/LICENSE" "v1\n"
    runGit root [ "add"; "-A" ]
    generateAtRoot root |> ignore
    runGit root [ "add"; "-A" ]
    runGit root [ "commit"; "-m"; "v1" ]
    runGit root [ "rm"; "-q"; "apps/rhino-cli/LICENSE" ]

    match validateAtRoot root with
    | Ok() -> Assert.Fail("expected Error for a boundary path missing from the current boundary")
    | Error message -> Assert.Contains("no longer matches", message)
