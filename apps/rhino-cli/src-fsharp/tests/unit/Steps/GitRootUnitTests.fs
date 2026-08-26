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
