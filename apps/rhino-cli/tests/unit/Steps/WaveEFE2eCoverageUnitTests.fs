/// Plain xunit tests for `RhinoCli.Cli.Dispatch.route`'s `specs e2e-coverage
/// validate` leaf. `SpecsSteps.fs`'s e2e-coverage scenarios exercise the
/// underlying `Specs` module functions directly and, for the CLI shape, spawn
/// a subprocess — both invisible to coverlet, which is why this leaf sat at
/// 0% line coverage despite the underlying logic being well-tested. This file
/// drives `route` in-process against a minimal synthetic fixture instead of
/// the real checkout, since `--update-baseline` writes a file and must never
/// touch this repo's own baseline — see `learnings.md`, 2026-08-30.
module RhinoCli.Tests.Unit.Steps.WaveEFE2eCoverageUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Cli.Dispatch

let private newTempDir () =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-waveef-e2e-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private writeFile (root: string) (relativePath: string) (content: string) =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
    File.WriteAllText(full, content)

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

let private featureWithOneE2eScenario =
    "Feature: Example\n\n  @e2e\n  Scenario: does the thing\n    Given x\n"

/// A fixture with one declared `@e2e` scenario, rendered (bound) by the
/// generated spec.js — the coverage-clean arm.
let private newBoundFixture () =
    let root = newTempDir ()
    writeFile root "specs/apps/example/e2e.feature" featureWithOneE2eScenario
    writeFile root ".features-gen/specs/apps/example/e2e.feature.spec.js" "test('does the thing', () => {});"
    root

/// A fixture with one declared `@e2e` scenario left unbound (the generated
/// spec.js exists but never renders it) — the findings-present arm.
let private newUnboundFixture () =
    let root = newTempDir ()
    writeFile root "specs/apps/example/e2e.feature" featureWithOneE2eScenario
    writeFile root ".features-gen/specs/apps/example/e2e.feature.spec.js" "// nothing rendered here\n"
    root

let private e2eArgs (root: string) (extra: string list) : string[] =
    [ "specs"
      "e2e-coverage"
      "validate"
      "--features"
      "specs/apps/example/e2e.feature"
      "--features-gen"
      ".features-gen"
      "--baseline"
      "e2e-baseline.json"
      "--project"
      "example" ]
    @ extra
    @ [ root ]
    |> List.toArray

[<Fact>]
let ``route reports every missing required flag on specs e2e-coverage validate`` () =
    let root = newTempDir ()

    let code, _, err =
        runCaptured (okRoot root) [| "specs"; "e2e-coverage"; "validate" |]

    Assert.Equal(2, code)
    Assert.Contains("--features <GLOB>", err)
    Assert.Contains("--features-gen <DIR>", err)
    Assert.Contains("--baseline <PATH>", err)
    Assert.Contains("--project <NAME>", err)

[<Fact>]
let ``route reports missing required flags on specs e2e-coverage validate with --help`` () =
    let root = newTempDir ()

    let code, _, err =
        runCaptured (okRoot root) [| "specs"; "e2e-coverage"; "validate"; "--help" |]

    Assert.Equal(2, code)
    Assert.Contains("--help", err)

[<Fact>]
let ``route reports an empty glob match on specs e2e-coverage validate`` () =
    let root = newTempDir ()
    writeFile root ".features-gen/placeholder" ""

    let code, _, err = runCaptured (okRoot root) (e2eArgs root [])
    Assert.Equal(1, code)
    Assert.Contains("matched no .feature files", err)

[<Fact>]
let ``route reports a missing features-gen directory on specs e2e-coverage validate`` () =
    let root = newTempDir ()
    writeFile root "specs/apps/example/e2e.feature" featureWithOneE2eScenario

    let code, _, err = runCaptured (okRoot root) (e2eArgs root [])
    Assert.Equal(1, code)
    Assert.Contains("run `npx bddgen` first", err)

[<Fact>]
let ``route passes specs e2e-coverage validate when every declared scenario is bound`` () =
    let root = newBoundFixture ()
    let code, out, _ = runCaptured (okRoot root) (e2eArgs root [])
    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders a clean specs e2e-coverage validate pass as JSON`` () =
    let root = newBoundFixture ()
    let code, out, _ = runCaptured (okRoot root) (e2eArgs root [ "-o"; "json" ])
    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders a clean specs e2e-coverage validate pass as markdown`` () =
    let root = newBoundFixture ()
    let code, out, _ = runCaptured (okRoot root) (e2eArgs root [ "-o"; "markdown" ])
    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route reports a new unbound scenario beyond baseline on specs e2e-coverage validate`` () =
    let root = newUnboundFixture ()
    let code, _, err = runCaptured (okRoot root) (e2eArgs root [])
    Assert.Equal(1, code)
    Assert.Contains("new unbound scenario(s) found beyond baseline", err)

[<Fact>]
let ``route writes a baseline manifest with --update-baseline`` () =
    let root = newUnboundFixture ()
    let code, out, _ = runCaptured (okRoot root) (e2eArgs root [ "--update-baseline" ])
    Assert.Equal(0, code)
    Assert.Contains("Wrote baseline manifest to", out)
    Assert.True(File.Exists(Path.Combine(root, "e2e-baseline.json")))

[<Fact>]
let ``route reports an unreadable baseline manifest on specs e2e-coverage validate`` () =
    let root = newBoundFixture ()
    writeFile root "e2e-baseline.json" "not json"
    let code, _, err = runCaptured (okRoot root) (e2eArgs root [])
    Assert.Equal(1, code)
    Assert.NotEmpty err
