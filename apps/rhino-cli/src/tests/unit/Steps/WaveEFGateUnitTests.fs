/// Plain xunit tests for `RhinoCli.Cli.Dispatch.route`'s `gate run`/`gate
/// list` leaves, driven **in-process** against a disposable Git fixture.
/// `GateExecutionSteps.fs`'s 30 scenarios spawn the real, prebuilt CLI as a
/// subprocess (`gate run`'s `rhino-cli`-kind leaf spawns the current
/// executable, so an in-process call would resolve to the test host) — that
/// makes them invisible to coverlet's line-coverage instrumentation, which is
/// why `Gate.fs`'s internals (`runGit`, `stagedPaths`, `changedPaths`,
/// `candidatePaths`, `globRegex`, the `gate run` loop) sat at 57% line
/// coverage despite extensive scenario coverage — see `learnings.md`,
/// 2026-08-30. This file exercises the same fixture shapes through `route`
/// directly so coverlet can see them.
module RhinoCli.Tests.Unit.Steps.WaveEFGateUnitTests

open System
open System.Diagnostics
open System.IO
open Xunit
open RhinoCli.Cli.Dispatch

let private runCaptured (getRepoRoot: unit -> Result<string, string>) (argv: string[]) : int * string * string =
    let originalOut = Console.Out
    let originalErr = Console.Error
    use outWriter = new StringWriter()
    use errWriter = new StringWriter()

    try
        Console.SetOut(outWriter)
        Console.SetError(errWriter)
        let exitCode = route getRepoRoot argv
        exitCode, outWriter.ToString(), errWriter.ToString()
    finally
        Console.SetOut(originalOut)
        Console.SetError(originalErr)

let private okRoot (root: string) () = Ok root

/// Mirrors `GateExecutionSteps.fs`'s `gate`/`config` fixture helpers.
let private gate (id: string) (gateType: string) (command: string) (kind: string) (surfaces: string) : string =
    sprintf
        "  - id: %s\n    type: %s\n    command: %s\n    kind: %s\n    surfaces:\n%s"
        id
        gateType
        command
        kind
        surfaces

let private config (gates: string) : string = "gates:\n" + gates

type private RunResult =
    { ExitCode: int
      Stdout: string
      Stderr: string }

let private runProcess (exe: string) (args: string list) (cwd: string) (env: (string * string) list) : RunResult =
    let psi =
        ProcessStartInfo(
            FileName = exe,
            UseShellExecute = false,
            WorkingDirectory = cwd,
            RedirectStandardOutput = true,
            RedirectStandardError = true
        )

    for a in args do
        psi.ArgumentList.Add a

    for k, v in env do
        psi.Environment.[k] <- v

    use p = Process.Start psi
    let out = p.StandardOutput.ReadToEnd()
    let err = p.StandardError.ReadToEnd()
    p.WaitForExit()

    { ExitCode = p.ExitCode
      Stdout = out
      Stderr = err }

/// A fresh temp dir with an initialized Git repository, ready for
/// `write`/`stage`/`commit`. Only the fixture's OWN `git` subprocess calls
/// get `GIT_DIR`/`GIT_WORK_TREE` overrides — the test host process's own
/// environment is never touched, so `Gate.fs`'s in-process `runGit`/
/// `stagedPaths` calls (which use `WorkingDirectory = repoRoot`) resolve
/// this fixture correctly via cwd-based discovery.
type private GitFixture() =
    let root =
        let dir =
            Path.Combine(Path.GetTempPath(), "rhino-cli-waveef-gate-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory dir |> ignore
        dir

    let fixtureGitEnv =
        [ "GIT_DIR", Path.Combine(root, ".git")
          "GIT_CEILING_DIRECTORIES", root
          "GIT_CONFIG_GLOBAL", "/dev/null"
          "GIT_CONFIG_SYSTEM", "/dev/null" ]

    let runGit (args: string list) : RunResult =
        runProcess "git" args root fixtureGitEnv

    member _.Root = root

    member _.Write(relative: string, contents: string) =
        let path = Path.Combine(root, relative)
        Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
        File.WriteAllText(path, contents)

    member _.Init() = runGit [ "init"; "--quiet" ] |> ignore

    member _.Stage(paths: string list) = runGit ("add" :: paths) |> ignore

    member _.Commit(message: string) =
        let result =
            runProcess
                "git"
                [ "commit"; "--quiet"; "-m"; message ]
                root
                (fixtureGitEnv
                 @ [ "GIT_AUTHOR_NAME", "waveef-gate-fixture"
                     "GIT_AUTHOR_EMAIL", "waveef-gate-fixture@example.invalid"
                     "GIT_COMMITTER_NAME", "waveef-gate-fixture"
                     "GIT_COMMITTER_EMAIL", "waveef-gate-fixture@example.invalid" ])

        Assert.Equal(0, result.ExitCode)

/// An always-runs `external`-kind gate declared on `pre-push`.
let private alwaysRunsConfig =
    config (gate "always-runs" "check" "sh -c 'exit 0'" "external" "      pre-push: { scope: other }\n")

[<Fact>]
let ``route runs an unconditional gate on pre-push`` () =
    let fx = GitFixture()
    fx.Init()
    fx.Write("repo-config.yml", alwaysRunsConfig)
    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, out, _ =
        runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=pre-push" |]

    Assert.Equal(0, code)
    Assert.Contains("Running gate always-runs", out)

[<Fact>]
let ``route runs a named gate via --only`` () =
    let fx = GitFixture()
    fx.Init()
    fx.Write("repo-config.yml", alwaysRunsConfig)
    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, out, _ =
        runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=pre-push"; "--only=always-runs" |]

    Assert.Equal(0, code)
    Assert.Contains("Running gate always-runs", out)

[<Fact>]
let ``route surfaces a failing gate's error on pre-push`` () =
    let fx = GitFixture()
    fx.Init()

    fx.Write(
        "repo-config.yml",
        config (gate "always-fails" "check" "sh -c 'exit 1'" "external" "      pre-push: { scope: other }\n")
    )

    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, _, err =
        runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=pre-push" |]

    Assert.Equal(1, code)
    Assert.Contains("gate always-fails failed", err)

[<Fact>]
let ``route runs a path-gated gate on pre-push when the trigger path is staged`` () =
    let fx = GitFixture()
    fx.Init()

    fx.Write(
        "repo-config.yml",
        config (
            gate
                "path-gated-check"
                "check"
                "sh -c 'exit 0'"
                "external"
                "      pre-push:\n        scope: path-gated\n        trigger:\n          - docs/\n"
        )
    )

    fx.Write("docs/a.md", "# A\n")
    fx.Stage [ "repo-config.yml"; "docs/a.md" ]
    fx.Commit "initial"

    fx.Write("docs/a.md", "# A changed\n")
    fx.Stage [ "docs/a.md" ]

    let code, out, _ =
        runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=pre-push" |]

    Assert.Equal(0, code)
    Assert.Contains("Running gate path-gated-check", out)

[<Fact>]
let ``route skips a path-gated gate on pre-push when no changed path matches the trigger`` () =
    let fx = GitFixture()
    fx.Init()

    fx.Write(
        "repo-config.yml",
        config (
            gate
                "path-gated-check"
                "check"
                "sh -c 'exit 0'"
                "external"
                "      pre-push:\n        scope: path-gated\n        trigger:\n          - docs/\n"
        )
    )

    fx.Write("src/a.txt", "one\n")
    fx.Stage [ "repo-config.yml"; "src/a.txt" ]
    fx.Commit "initial"

    fx.Write("src/a.txt", "two\n")
    fx.Stage [ "src/a.txt" ]

    let code, out, _ =
        runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=pre-push" |]

    Assert.Equal(0, code)
    Assert.DoesNotContain("Running gate path-gated-check", out)

[<Fact>]
let ``route reports missing --surface on gate run`` () =
    let fx = GitFixture()
    fx.Init()
    fx.Write("repo-config.yml", alwaysRunsConfig)
    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, _, err = runCaptured (okRoot fx.Root) [| "gate"; "run" |]
    Assert.Equal(2, code)
    Assert.Contains("--surface <SURFACE>", err)

[<Fact>]
let ``route reports missing --surface on gate run with --help`` () =
    let fx = GitFixture()
    fx.Init()
    fx.Write("repo-config.yml", alwaysRunsConfig)
    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, _, err = runCaptured (okRoot fx.Root) [| "gate"; "run"; "--help" |]
    Assert.Equal(2, code)
    Assert.Contains("--help", err)

[<Fact>]
let ``route threads a commit-message file through gate run on commit-msg`` () =
    // A commit-message file is only valid on the `commit-msg` surface — see
    // `runAtRootWithOnlyAndMessageFile`'s guard in Gate.fs.
    let fx = GitFixture()
    fx.Init()

    fx.Write(
        "repo-config.yml",
        config (gate "msg-check" "check" "sh -c 'exit 0'" "external" "      commit-msg: { scope: other }\n")
    )

    fx.Write("msg.txt", "a commit message\n")
    fx.Stage [ "repo-config.yml"; "msg.txt" ]
    fx.Commit "initial"

    let code, out, _ =
        runCaptured
            (okRoot fx.Root)
            [| "gate"
               "run"
               "--surface=commit-msg"
               "--"
               Path.Combine(fx.Root, "msg.txt") |]

    Assert.Equal(0, code)
    Assert.Contains("Running gate msg-check", out)

[<Fact>]
let ``route rejects a commit-message file on a non-commit-msg surface`` () =
    let fx = GitFixture()
    fx.Init()
    fx.Write("repo-config.yml", alwaysRunsConfig)
    fx.Write("msg.txt", "a commit message\n")
    fx.Stage [ "repo-config.yml"; "msg.txt" ]
    fx.Commit "initial"

    let code, _, err =
        runCaptured
            (okRoot fx.Root)
            [| "gate"
               "run"
               "--surface=pre-push"
               "--"
               Path.Combine(fx.Root, "msg.txt") |]

    Assert.Equal(1, code)
    Assert.Contains("commit-message file is only valid for the commit-msg surface", err)

[<Fact>]
let ``route reports missing --surface on gate list`` () =
    let fx = GitFixture()
    fx.Init()
    fx.Write("repo-config.yml", alwaysRunsConfig)
    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, _, err = runCaptured (okRoot fx.Root) [| "gate"; "list" |]
    Assert.Equal(2, code)
    Assert.Contains("--surface <SURFACE>", err)

[<Fact>]
let ``route lists gates declared on a surface`` () =
    let fx = GitFixture()
    fx.Init()
    fx.Write("repo-config.yml", alwaysRunsConfig)
    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, out, _ =
        runCaptured (okRoot fx.Root) [| "gate"; "list"; "--surface=pre-push" |]

    Assert.Equal(0, code)
    Assert.Contains("always-runs", out)

[<Fact>]
let ``route lists gates declared on a surface as JSON`` () =
    let fx = GitFixture()
    fx.Init()
    fx.Write("repo-config.yml", alwaysRunsConfig)
    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, out, _ =
        runCaptured (okRoot fx.Root) [| "gate"; "list"; "--surface=pre-push"; "--format=json" |]

    Assert.Equal(0, code)
    Assert.Contains("always-runs", out)

[<Fact>]
let ``route reports a gate missing ci_group when listing --by-group`` () =
    let fx = GitFixture()
    fx.Init()
    fx.Write("repo-config.yml", alwaysRunsConfig)
    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, _, err =
        runCaptured (okRoot fx.Root) [| "gate"; "list"; "--surface=pre-push"; "--by-group" |]

    Assert.Equal(1, code)
    Assert.Contains("missing ci_group required for grouped output", err)

// ---------------------------------------------------------------------------
// AffectedFileType / AllFileType candidate scopes — matchingFiles,
// filterCandidates, globRegex, isExcluded, reportEmptyScopeSkip
// ---------------------------------------------------------------------------

[<Fact>]
let ``route skips a file-scoped gate on pre-commit when no staged file matches its glob`` () =
    let fx = GitFixture()
    fx.Init()

    fx.Write(
        "repo-config.yml",
        config (
            gate
                "md-only-check"
                "check"
                "sh -c 'exit 0'"
                "external"
                "      pre-commit: { scope: affected-file-type, glob: \"*.md\" }\n"
        )
    )

    fx.Write("src/a.txt", "one\n")
    fx.Stage [ "repo-config.yml"; "src/a.txt" ]
    fx.Commit "initial"

    fx.Write("src/a.txt", "two\n")
    fx.Stage [ "src/a.txt" ]

    let code, out, _ =
        runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=pre-commit" |]

    Assert.Equal(0, code)
    Assert.Contains("Skipping gate md-only-check", out)

[<Fact>]
let ``route runs an all-file-type-scoped gate on pre-push when a tracked file matches its glob`` () =
    let fx = GitFixture()
    fx.Init()

    fx.Write(
        "repo-config.yml",
        config (
            gate
                "md-tree-check"
                "check"
                "sh -c 'exit 0'"
                "external"
                "      pre-push: { scope: all-file-type, glob: \"**/*.md\", exclude: [\"vendor\"] }\n"
        )
    )

    fx.Write("docs/a.md", "# A\n")
    fx.Write("vendor/skip.md", "# skip\n")
    fx.Stage [ "repo-config.yml"; "docs/a.md"; "vendor/skip.md" ]
    fx.Commit "initial"

    let code, out, _ =
        runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=pre-push" |]

    Assert.Equal(0, code)
    Assert.Contains("Running gate md-tree-check", out)

// ---------------------------------------------------------------------------
// `ci` surface — the `GATE_CHANGED_BASE` explicit-base branch of `changedPaths`
// ---------------------------------------------------------------------------

[<Fact>]
let ``route falls back to the merge base on ci when GATE_CHANGED_BASE is unset`` () =
    let fx = GitFixture()
    fx.Init()

    fx.Write(
        "repo-config.yml",
        config (
            gate
                "ci-path-gated"
                "check"
                "sh -c 'exit 0'"
                "external"
                "      ci:\n        scope: path-gated\n        trigger:\n          - docs/\n"
        )
    )

    fx.Write("docs/a.md", "# A\n")
    fx.Stage [ "repo-config.yml"; "docs/a.md" ]
    fx.Commit "initial"

    fx.Write("docs/a.md", "# A changed\n")
    fx.Stage [ "docs/a.md" ]

    let code, out, _ = runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=ci" |]
    Assert.Equal(0, code)
    Assert.Contains("Running gate ci-path-gated", out)

[<Fact>]
let ``route honors an explicit GATE_CHANGED_BASE on ci`` () =
    let fx = GitFixture()
    fx.Init()

    fx.Write(
        "repo-config.yml",
        config (
            gate
                "ci-path-gated"
                "check"
                "sh -c 'exit 0'"
                "external"
                "      ci:\n        scope: path-gated\n        trigger:\n          - docs/\n"
        )
    )

    fx.Write("docs/a.md", "# A\n")
    fx.Stage [ "repo-config.yml"; "docs/a.md" ]
    fx.Commit "first"

    fx.Write("docs/a.md", "# A changed\n")
    fx.Stage [ "docs/a.md" ]
    fx.Commit "second"

    let firstSha =
        let result =
            runProcess "git" [ "rev-parse"; "HEAD~1" ] fx.Root [ "GIT_DIR", Path.Combine(fx.Root, ".git") ]

        result.Stdout.Trim()

    let previous = Environment.GetEnvironmentVariable "GATE_CHANGED_BASE"

    try
        Environment.SetEnvironmentVariable("GATE_CHANGED_BASE", firstSha)
        let code, out, _ = runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=ci" |]
        Assert.Equal(0, code)
        Assert.Contains("Running gate ci-path-gated", out)
    finally
        Environment.SetEnvironmentVariable("GATE_CHANGED_BASE", previous)

// ---------------------------------------------------------------------------
// `--group` — resolveGroupGates, reportGroupSummary
// ---------------------------------------------------------------------------

let private groupedConfig (secondCommand: string) =
    config (
        "  - id: group-a\n    type: check\n    command: sh -c 'exit 0'\n    kind: external\n    ci-group: my-group\n    surfaces:\n      pre-push: { scope: other }\n"
        + sprintf
            "  - id: group-b\n    type: check\n    command: %s\n    kind: external\n    ci-group: my-group\n    surfaces:\n      pre-push: { scope: other }\n"
            secondCommand
    )

[<Fact>]
let ``route runs every gate in a passing --group`` () =
    let fx = GitFixture()
    fx.Init()
    fx.Write("repo-config.yml", groupedConfig "sh -c 'exit 0'")
    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, out, _ =
        runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=pre-push"; "--group=my-group" |]

    Assert.Equal(0, code)
    Assert.Contains("group-a\tPASS", out)
    Assert.Contains("group-b\tPASS", out)

[<Fact>]
let ``route reports a failing member of a --group`` () =
    let fx = GitFixture()
    fx.Init()
    fx.Write("repo-config.yml", groupedConfig "sh -c 'exit 1'")
    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, out, err =
        runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=pre-push"; "--group=my-group" |]

    Assert.Equal(1, code)
    Assert.Contains("group-b\tFAIL", out)
    Assert.Contains("gate group my-group failed", err)

[<Fact>]
let ``route reports an unmatched --group id`` () =
    let fx = GitFixture()
    fx.Init()
    fx.Write("repo-config.yml", alwaysRunsConfig)
    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, _, err =
        runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=pre-push"; "--group=no-such-group" |]

    Assert.Equal(1, code)
    Assert.Contains("matched no gates on surface", err)

// ---------------------------------------------------------------------------
// `restages: true` — restagingBeforeSnapshot, restageMutationOutputs,
// worktreeChangedPaths, mutationOutputDelta
// ---------------------------------------------------------------------------

[<Fact>]
let ``route restages a mutation gate's new output file`` () =
    let fx = GitFixture()
    fx.Init()

    fx.Write(
        "repo-config.yml",
        config (
            "  - id: mutating-check\n    type: mutation\n    command: touch generated.txt\n    kind: external\n    restages: true\n    surfaces:\n      pre-push: { scope: other }\n"
        )
    )

    fx.Stage [ "repo-config.yml" ]
    fx.Commit "initial"

    let code, out, _ =
        runCaptured (okRoot fx.Root) [| "gate"; "run"; "--surface=pre-push" |]

    Assert.Equal(0, code)
    Assert.Contains("Running gate mutating-check", out)
    Assert.True(File.Exists(Path.Combine(fx.Root, "generated.txt")))

    let staged =
        (runProcess "git" [ "diff"; "--cached"; "--name-only" ] fx.Root [ "GIT_DIR", Path.Combine(fx.Root, ".git") ])
            .Stdout

    Assert.Contains("generated.txt", staged)
