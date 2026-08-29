/// TickSpec step definitions binding `gate-binary-resolution.feature`'s 4
/// scenarios against the real `apps/rhino-cli/scripts/rhino-bin.sh` resolver
/// shim [Repo-grounded — `tests/gate_specs.rs`'s binary-resolution bindings].
///
/// The subject here is the shim script, not an F# module: the shim is the
/// language-agnostic entry point every generated gate command goes through,
/// and it resolves the Rust binary for any first argument not listed in
/// `FSHARP_NAMESPACES`. These scenarios therefore exercise the same real
/// script the Rust suite does rather than a fixture stand-in — a stub shim
/// would prove only that the stub matches the assertions.
///
/// Every scenario that can reach the shim's build tier sandboxes it through a
/// scratch `CARGO_TARGET_DIR`, so the shared `apps/rhino-cli/target/gate/`
/// artifact this test run itself depends on is never rebuilt or removed.
module RhinoCli.Tests.Unit.Steps.GateSteps

open System
open System.Diagnostics
open System.IO
open TickSpec
open Xunit

/// `tests/unit/Steps` → `tests/unit` → `tests` → `src-fsharp` → `rhino-cli` →
/// `apps` → repo root.
let private repoRoot: string =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "..", "..", ".."))

let private shimPath: string =
    Path.Combine(repoRoot, "apps", "rhino-cli", "scripts", "rhino-bin.sh")

/// Deterministic, side-effect-free probe args: `--say <msg>` echoes `<msg>`
/// and exits 0. `--version` is deliberately not used — this CLI maps clap's
/// `DisplayVersion` pseudo-error to exit 2
/// [Repo-grounded — `gate_specs.rs::RESOLVER_SHIM_PROBE_ARGS`].
let private probeArgs = [ "--say"; "resolver-shim-probe" ]

type private RunResult =
    { ExitCode: int
      Stdout: string
      Stderr: string }

let private run (exe: string) (args: string list) (env: (string * string) list) : RunResult =
    let psi = ProcessStartInfo(exe)

    for a in args do
        psi.ArgumentList.Add a

    psi.RedirectStandardOutput <- true
    psi.RedirectStandardError <- true
    psi.UseShellExecute <- false
    psi.WorkingDirectory <- repoRoot

    for k, v in env do
        psi.Environment[k] <- v

    use p = Process.Start psi
    let out = p.StandardOutput.ReadToEnd()
    let err = p.StandardError.ReadToEnd()
    p.WaitForExit()

    { ExitCode = p.ExitCode
      Stdout = out
      Stderr = err }

let private scratchDir () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-gate-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory dir |> ignore
    dir

let private makeExecutable (path: string) : unit =
    File.SetUnixFileMode(
        path,
        UnixFileMode.UserRead
        ||| UnixFileMode.UserWrite
        ||| UnixFileMode.UserExecute
        ||| UnixFileMode.GroupRead
        ||| UnixFileMode.GroupExecute
        ||| UnixFileMode.OtherRead
        ||| UnixFileMode.OtherExecute
    )

/// `PATH` with the directory holding `cargo` removed, so an invocation that
/// reached the shim's `cargo build` tier would fail with "command not found"
/// rather than succeed. A successful exit is then conclusive proof no build
/// was attempted — stronger than any timing heuristic
/// [Repo-grounded — `gate_specs.rs::path_without_cargo_directory`].
let private pathWithoutCargo () : string =
    let existing = Environment.GetEnvironmentVariable "PATH"

    let cargoDir =
        existing.Split(Path.PathSeparator)
        |> Array.tryFind (fun d -> d <> "" && File.Exists(Path.Combine(d, "cargo")))

    existing.Split(Path.PathSeparator)
    |> Array.filter (fun d -> Some d <> cargoDir)
    |> String.concat (string Path.PathSeparator)

/// The gate-profile binary these scenarios compare the shim against, built on
/// first use. A fresh clone has never built it and the ambient sweeper deletes
/// `target/` at any time, so assuming its presence would make these scenarios
/// pass only on a machine that happened to have built it
/// [Repo-grounded — `gate_specs.rs::real_prebuilt_rhino_cli`].
let private prebuiltRhinoCli: Lazy<string> =
    lazy
        (let binary =
            Path.Combine(repoRoot, "apps", "rhino-cli", "target", "gate", "rhino-cli")

         if File.Exists binary then
             binary
         else
             let r =
                 run
                     "cargo"
                     [ "build"
                       "--profile"
                       "gate"
                       "--manifest-path"
                       Path.Combine(repoRoot, "apps", "rhino-cli", "Cargo.toml") ]
                     []

             Assert.True(
                 r.ExitCode = 0 && File.Exists binary,
                 sprintf "cargo build --profile gate must produce %s: %s" binary r.Stderr
             )

             binary)

type GateSteps() =
    let mutable targetDir: string option = None
    let mutable overrideBin: string option = None
    let mutable invalidOverride: string option = None
    let mutable stripCargoFromPath = false
    let mutable staleMtimeBefore: DateTime option = None
    let mutable firstRun: RunResult option = None

    let result () =
        match firstRun with
        | Some r -> r
        | None -> failwith "resolver shim invocation recorded"

    let sandbox () =
        match targetDir with
        | Some d -> d
        | None -> failwith "sandbox target dir configured"

    let sandboxBinary () =
        Path.Combine(sandbox (), "gate", "rhino-cli")

    // ---- Given ----

    [<Given>]
    member _.``the rhino-cli binary is absent because the ambient sweeper removed target/``() =
        targetDir <- Some(scratchDir ())

    [<Given>]
    member _.``the environment variable RHINO_CLI_BIN points at an executable rhino-cli binary``() =
        let dir = scratchDir ()
        let stub = Path.Combine(dir, "stub-rhino-cli")
        File.WriteAllText(stub, "#!/bin/sh\nprintf 'stub-rhino-cli-override-marker\\n'\nexit 0\n")
        makeExecutable stub
        overrideBin <- Some stub
        stripCargoFromPath <- true

    [<Given>]
    member _.``the prebuilt gate-profile binary in target/ is older than the source tree it was built from``() =
        let dir = scratchDir ()
        let gateDir = Path.Combine(dir, "gate")
        Directory.CreateDirectory gateDir |> ignore
        let placeholder = Path.Combine(gateDir, "rhino-cli")

        // Deliberately NOT the real binary: its marker output proves whether
        // the shim rebuilt it or silently kept serving it, which is the
        // regression this scenario guards against.
        File.WriteAllText(placeholder, "#!/bin/sh\nprintf 'stale-placeholder-marker\\n'\nexit 0\n")
        makeExecutable placeholder

        // Backdated far enough to predate every real file under
        // apps/rhino-cli/src, Cargo.toml, and Cargo.lock — the shim's
        // `find ... -newer` staleness check always compares against those
        // real paths, since SRC_DIR resolves relative to the shim's own
        // location rather than to CARGO_TARGET_DIR.
        let backdated = DateTime.UnixEpoch.AddHours 24.0
        File.SetLastWriteTimeUtc(placeholder, backdated)
        staleMtimeBefore <- Some backdated
        targetDir <- Some dir

    [<Given>]
    member _.``the environment variable RHINO_CLI_BIN points at a path that does not exist``() =
        // Sandboxed so the fallthrough deterministically reaches the build
        // tier regardless of what the real target/gate/rhino-cli holds.
        targetDir <- Some(scratchDir ())
        invalidOverride <- Some(Path.Combine(scratchDir (), "does-not-exist-rhino-cli"))

    // ---- When ----

    [<When>]
    member _.``a generated gate command runs through the resolver shim``() =
        let env =
            [ match targetDir with
              | Some d -> "CARGO_TARGET_DIR", d
              | None -> ()
              match overrideBin with
              | Some b -> "RHINO_CLI_BIN", b
              | None -> ()
              match invalidOverride with
              | Some b -> "RHINO_CLI_BIN", b
              | None -> ()
              if stripCargoFromPath then
                  "PATH", pathWithoutCargo () ]

        firstRun <- Some(run shimPath probeArgs env)

    // ---- Then ----

    [<Then>]
    member _.``the shim builds the binary and then executes the requested gate``() =
        let r = result ()
        Assert.True(r.ExitCode = 0, sprintf "shim must build then execute successfully: %s" r.Stderr)

        Assert.True(File.Exists(sandboxBinary ()), "shim must build the binary into the sandbox target directory")

    [<Then>]
    member _.``the gate reports the same result it would have reported with the binary present``() =
        let shim = result ()
        let direct = run prebuiltRhinoCli.Value probeArgs []
        Assert.Equal(direct.ExitCode, shim.ExitCode)
        Assert.Equal(direct.Stdout, shim.Stdout)

    [<Then>]
    member _.``a subsequent invocation reuses the built binary without rebuilding``() =
        let binary = sandboxBinary ()
        let before = File.GetLastWriteTimeUtc binary
        let second = run shimPath probeArgs [ "CARGO_TARGET_DIR", sandbox () ]

        Assert.True(second.ExitCode = 0, sprintf "second shim invocation must succeed: %s" second.Stderr)

        Assert.Equal(before, File.GetLastWriteTimeUtc binary)

    [<Then>]
    member _.``the shim rebuilds the binary before executing the requested gate``() =
        let r = result ()

        Assert.True(r.ExitCode = 0, sprintf "shim must rebuild a stale binary then execute successfully: %s" r.Stderr)

        let after = File.GetLastWriteTimeUtc(sandboxBinary ())
        let before = Option.get staleMtimeBefore

        Assert.True(after > before, sprintf "a stale binary must be rebuilt: before=%O after=%O" before after)

        Assert.DoesNotContain("stale-placeholder-marker", r.Stdout)

    [<Then>]
    member _.``the shim falls back to discovery instead of the invalid override``() =
        let r = result ()

        Assert.True(
            r.ExitCode = 0,
            sprintf "an invalid RHINO_CLI_BIN must fall back to discovery, not fail: %s" r.Stderr
        )

        Assert.True(
            File.Exists(sandboxBinary ()),
            "an invalid override must fall through to discovery, which builds into CARGO_TARGET_DIR"
        )

    [<Then>]
    member _.``the shim executes the binary at that path``() =
        let r = result ()
        Assert.True(r.ExitCode = 0, sprintf "shim must execute the RHINO_CLI_BIN override: %s" r.Stderr)
        Assert.Equal("stub-rhino-cli-override-marker", r.Stdout.Trim())

    [<Then>]
    member _.``it performs no cargo build``() =
        // The invocation's PATH excluded cargo's directory, so had the shim
        // fallen through to its build tier the shell would have reported
        // "command not found" and the shim would have exited non-zero. A
        // successful exit is conclusive.
        let r = result ()

        Assert.True(r.ExitCode = 0, sprintf "shim must not attempt cargo build when RHINO_CLI_BIN is set: %s" r.Stderr)

module private FeatureRunner =

    let private featurePath: string =
        Path.Combine(
            repoRoot,
            "specs",
            "apps",
            "rhino",
            "behavior",
            "rhino-cli",
            "gherkin",
            "gate",
            "gate-binary-resolution.feature"
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

                trimmed.StartsWith("Scenario:", StringComparison.Ordinal)
                || trimmed.StartsWith("@", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<GateSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``A swept target directory produces a slow run, not a failure`` () =
    FeatureRunner.run "A swept target directory produces a slow run, not a failure"

[<Fact>]
let ``RHINO_CLI_BIN takes precedence over discovery`` () =
    FeatureRunner.run "RHINO_CLI_BIN takes precedence over discovery"

[<Fact>]
let ``A stale prebuilt binary is rebuilt, not silently reused`` () =
    FeatureRunner.run "A stale prebuilt binary is rebuilt, not silently reused"

[<Fact>]
let ``An invalid RHINO_CLI_BIN override falls through to discovery`` () =
    FeatureRunner.run "An invalid RHINO_CLI_BIN override falls through to discovery"
