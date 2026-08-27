/// Plain xunit tests for `RhinoCli.Infrastructure.GitRoot.findRoot`.
/// Exercises the real `git` binary against the current process's working
/// directory rather than mocking the process boundary — this repo's own
/// checkout (a git worktree) and a non-repository temp directory are the
/// two real-world states the function distinguishes.
///
/// One test below mutates `Environment.CurrentDirectory`, process-global
/// state that would otherwise race every other file's tests if xunit ran
/// its default one-collection-per-module parallelism — hence the assembly
/// -wide opt-out declared here, which also protects `ParityUnitTests`'s own
/// git-fixture tests elsewhere in this run.
module RhinoCli.Tests.Unit.Steps.GitRootUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Infrastructure.GitRoot

[<assembly: CollectionBehavior(DisableTestParallelization = true)>]
do ()

[<Fact>]
let ``findRoot succeeds when the working directory is inside a git checkout`` () =
    // The test host's own working directory is somewhere under this repo's
    // worktree, which is itself a git checkout.
    match findRoot () with
    | Ok root -> Assert.True(Directory.Exists(root))
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

/// Writes an executable named `git` into a fresh temp directory that always
/// exits with `exitCode` and prints `stdout` to standard out, returning
/// that directory — used to drive `findRoot`'s two branches a real `git`
/// binary cannot deterministically produce (a "successful" empty-path
/// result) or that are awkward to provoke otherwise (the binary missing
/// entirely).
let private newFakeGitDir (exitCode: int) (stdout: string) : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-fake-git-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    let scriptPath = Path.Combine(dir, "git")
    File.WriteAllText(scriptPath, sprintf "#!/bin/sh\nprintf '%%s' \"%s\"\nexit %d\n" stdout exitCode)
    File.SetUnixFileMode(scriptPath, UnixFileMode.UserRead ||| UnixFileMode.UserWrite ||| UnixFileMode.UserExecute)
    dir

let private withPath (dir: string) (body: unit -> unit) =
    let original = Environment.GetEnvironmentVariable("PATH")

    try
        Environment.SetEnvironmentVariable("PATH", dir + ":" + original)
        body ()
    finally
        Environment.SetEnvironmentVariable("PATH", original)

[<Fact>]
let ``findRoot fails when git rev-parse exits successfully with empty output`` () =
    let fakeGitDir = newFakeGitDir 0 ""

    withPath fakeGitDir (fun () ->
        match findRoot () with
        | Error message -> Assert.Equal("git rev-parse returned empty path", message)
        | Ok root -> Assert.Fail(sprintf "expected Error, got Ok %s" root))

[<Fact>]
let ``findRoot fails when the git binary cannot be invoked at all`` () =
    let original = Environment.GetEnvironmentVariable("PATH")

    try
        Environment.SetEnvironmentVariable("PATH", "")

        match findRoot () with
        | Error message -> Assert.Contains("failed to invoke git rev-parse", message)
        | Ok root -> Assert.Fail(sprintf "expected Error, got Ok %s" root)
    finally
        Environment.SetEnvironmentVariable("PATH", original)

// ---- getStagedFiles ----

let private runGit (cwd: string) (args: string list) : unit =
    use proc = new Diagnostics.Process()
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
/// locally (never touches global/user git config) — same shape as
/// `ParityUnitTests.newGitFixture`, duplicated here rather than shared
/// since each file's fixture helper is deliberately self-contained.
let private newGitFixture () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-gitroot-staged-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    runGit dir [ "init"; "-q"; "-b"; "main" ]
    runGit dir [ "config"; "user.name"; "Rhino CLI Test" ]
    runGit dir [ "config"; "user.email"; "rhino-cli-test@example.invalid" ]
    dir

[<Fact>]
let ``getStagedFiles returns an empty list when nothing is staged`` () =
    let root = newGitFixture ()

    match getStagedFiles root with
    | Ok files -> Assert.Empty(files)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``getStagedFiles lists a real staged file`` () =
    let root = newGitFixture ()
    File.WriteAllText(Path.Combine(root, ".env"), "SECRET=1\n")
    runGit root [ "add"; ".env" ]

    match getStagedFiles root with
    | Ok files -> Assert.Contains(".env", files)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``getStagedFiles lists multiple staged files without blank entries`` () =
    let root = newGitFixture ()
    File.WriteAllText(Path.Combine(root, "a.txt"), "a\n")
    File.WriteAllText(Path.Combine(root, "b.txt"), "b\n")
    runGit root [ "add"; "a.txt"; "b.txt" ]

    match getStagedFiles root with
    | Ok files ->
        Assert.Equal(2, List.length files)
        Assert.Contains("a.txt", files)
        Assert.Contains("b.txt", files)
        Assert.DoesNotContain("", files)
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

[<Fact>]
let ``getStagedFiles fails when repoRoot is not a git repository`` () =
    let outsideRepo =
        Path.Combine(Path.GetTempPath(), "rhino-cli-gitroot-staged-outside-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(outsideRepo) |> ignore

    try
        match getStagedFiles outsideRepo with
        | Error message -> Assert.Contains("git diff --cached failed", message)
        | Ok files -> Assert.Fail(sprintf "expected Error, got Ok %A" files)
    finally
        Directory.Delete(outsideRepo, true)

[<Fact>]
let ``getStagedFiles fails when the git binary cannot be invoked at all`` () =
    let original = Environment.GetEnvironmentVariable("PATH")
    let root = newGitFixture ()

    try
        Environment.SetEnvironmentVariable("PATH", "")

        match getStagedFiles root with
        | Error message -> Assert.Contains("failed to run git diff --cached", message)
        | Ok files -> Assert.Fail(sprintf "expected Error, got Ok %A" files)
    finally
        Environment.SetEnvironmentVariable("PATH", original)

[<Fact>]
let ``findRoot fails when the working directory is outside any git repository`` () =
    let original = Environment.CurrentDirectory

    let outsideRepo =
        Path.Combine(Path.GetTempPath(), "rhino-cli-gitroot-unit-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(outsideRepo) |> ignore

    try
        Environment.CurrentDirectory <- outsideRepo

        match findRoot () with
        | Error message -> Assert.Contains("git rev-parse failed", message)
        | Ok root -> Assert.Fail(sprintf "expected Error, got Ok %s" root)
    finally
        Environment.CurrentDirectory <- original
        Directory.Delete(outsideRepo, true)
