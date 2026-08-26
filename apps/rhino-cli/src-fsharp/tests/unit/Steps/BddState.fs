module RhinoCli.Tests.Unit.Steps.BddState

open System
open System.Collections.Concurrent
open System.IO

/// Shared mutable state for BDD scenario steps. All step modules read/write
/// through these so a When-step's outcome is visible to Then-steps
/// regardless of which module defines them — mirrors
/// `CraneCli.Tests.Unit.Steps.BddState`'s pattern for the same reason.
let mutable LastExitCode: int = -1
let mutable LastOutput: string = ""

/// Every temp directory created by a scenario's Given-step, deleted once at
/// process exit rather than per-scenario: `RhinoCli.Application.Convention`'s
/// functions here take a real repo-root path (no `Fs` port/mock exists in
/// this wave), so each fixture needs real on-disk files to scan.
let private tempDirs = ConcurrentBag<string>()

let private cleanupTempDirs () =
    for dir in tempDirs do
        try
            if Directory.Exists dir then
                Directory.Delete(dir, true)
        with _ ->
            ()

AppDomain.CurrentDomain.ProcessExit.Add(fun _ -> cleanupTempDirs ())

/// Creates a fresh, empty temp directory for one scenario's fixture and
/// registers it for cleanup at process exit.
let NewTempDir () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-fsharp-tests-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory dir |> ignore
    tempDirs.Add dir
    dir

/// Runs a When-step's action and records its `(exitCode, output)` result into
/// the shared state Then-steps assert against.
let RunWithWriter (f: unit -> int * string) =
    let code, output = f ()
    LastExitCode <- code
    LastOutput <- output
