/// Plain xunit tests proving the DDD namespace is absent from Rhino's
/// application layer, CLI route table, and `repo-config.yml` parser. These are
/// reflection- and route-level assertions rather than direct references, so
/// they fail with a focused message while the retired surface still exists
/// instead of failing to compile.
module RhinoCli.Tests.Unit.Steps.DddRetirementUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Cli.Dispatch
open RhinoCli.Application

let private applicationAssembly = typeof<RepoConfig.GateEntry>.Assembly

/// Runs `route`, capturing stdout/stderr around the call and restoring the
/// prior writers afterwards even if `route` throws.
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

let private applicationTypeNamesContaining (fragment: string) =
    applicationAssembly.GetTypes()
    |> Array.choose (fun t -> if isNull t.FullName then None else Some t.FullName)
    |> Array.filter (fun name -> name.Contains fragment)
    |> Array.sort

[<Fact>]
let ``the application layer exposes no bounded-context registry module`` () =
    Assert.Equal<string[]>([||], applicationTypeNamesContaining "Ddd")

[<Fact>]
let ``the application layer exposes no ubiquitous-language glossary module`` () =
    Assert.Equal<string[]>([||], applicationTypeNamesContaining "Glossary")

[<Fact>]
let ``the repo-config parser carries no DDD-only specs section`` () =
    let retired =
        typeof<RepoConfig.RepoConfig>.GetProperties()
        |> Array.map (fun p -> p.Name)
        |> Array.filter (fun name -> name = "Specs")

    Assert.Equal<string[]>([||], retired)

[<Fact>]
let ``specs domain-coverage validate is not a route`` () =
    let root = "/synthetic/repo"

    let exitCode, stdout, stderr =
        runCaptured (fun () -> Ok root) [| "specs"; "domain-coverage"; "validate"; "widget-app" |]

    Assert.Equal(2, exitCode)
    Assert.Contains("unrecognized or not-yet-routed invocation", stdout + stderr)
