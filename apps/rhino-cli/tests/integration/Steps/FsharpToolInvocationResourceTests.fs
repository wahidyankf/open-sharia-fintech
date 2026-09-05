/// Plain xunit tests for `RhinoCli.Application.Doctor`'s F# lint-target
/// Fantomas tool-invocation check — behaviour with no dedicated Gherkin
/// scenario, or exercised only indirectly there (mirrors the rationale
/// `DoctorToolCheckUnitTests.fs`'s module doc comment states for its own
/// split from `DoctorToolCheckSteps.fs`). No Rust source underlies this
/// feature, so unlike most `*UnitTests.fs` files in this directory there is
/// no `#[cfg(test)] mod tests` counterpart to port from.
module RhinoCli.Tests.Integration.Steps.FsharpToolInvocationResourceTests

open System
open System.IO
open Xunit
open RhinoCli.Application.Doctor
open RhinoCli.Domain.Types

let private makeRepo () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-fsharp-tool-invocation-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private writeProjectJson (path: string) (commandsJson: string) : unit =
    Directory.CreateDirectory(Path.GetDirectoryName(path: string)) |> ignore

    File.WriteAllText(path, sprintf """{ "targets": { "lint": { "options": { "commands": [%s] } } } }""" commandsJson)

// ---- discoverFsharpLintTargets ----

[<Fact>]
let ``discoverFsharpLintTargets finds a compliant target nested under an app directory`` () =
    let repoRoot = makeRepo ()

    try
        writeProjectJson
            (Path.Combine(repoRoot, "apps", "rhino-cli", "src-fsharp", "project.json"))
            "\"dotnet tool restore\", \"dotnet tool run fantomas --check apps/rhino-cli/src-fsharp\""

        let targets = discoverFsharpLintTargets repoRoot

        Assert.Equal(1, targets.Length)
        Assert.Equal("apps/rhino-cli/src-fsharp/project.json", targets.[0].ProjectJsonPath)
        Assert.Equal(2, targets.[0].Commands.Length)
    finally
        Directory.Delete(repoRoot, true)

[<Fact>]
let ``discoverFsharpLintTargets ignores a lint target that never mentions fantomas`` () =
    let repoRoot = makeRepo ()

    try
        writeProjectJson
            (Path.Combine(repoRoot, "apps", "rhino-cli", "project.json"))
            "\"cargo fmt --check\", \"cargo clippy\""

        Assert.Empty(discoverFsharpLintTargets repoRoot)
    finally
        Directory.Delete(repoRoot, true)

[<Fact>]
let ``discoverFsharpLintTargets ignores project.json under node_modules`` () =
    let repoRoot = makeRepo ()

    try
        writeProjectJson
            (Path.Combine(repoRoot, "apps", "some-app", "node_modules", "pkg", "project.json"))
            "\"dotnet tool restore\", \"dotnet tool run fantomas --check .\""

        Assert.Empty(discoverFsharpLintTargets repoRoot)
    finally
        Directory.Delete(repoRoot, true)

[<Fact>]
let ``discoverFsharpLintTargets returns empty when apps and libs are absent`` () =
    let repoRoot = makeRepo ()

    try
        Assert.Empty(discoverFsharpLintTargets repoRoot)
    finally
        Directory.Delete(repoRoot, true)

[<Fact>]
let ``discoverFsharpLintTargets tolerates a malformed project.json`` () =
    let repoRoot = makeRepo ()

    try
        let path = Path.Combine(repoRoot, "libs", "some-lib", "project.json")
        Directory.CreateDirectory(Path.GetDirectoryName(path: string)) |> ignore
        File.WriteAllText(path, "{ not valid json")

        Assert.Empty(discoverFsharpLintTargets repoRoot)
    finally
        Directory.Delete(repoRoot, true)

[<Fact>]
let ``discoverFsharpLintTargets tolerates a project.json with no lint target`` () =
    let repoRoot = makeRepo ()

    try
        let path = Path.Combine(repoRoot, "libs", "some-lib", "project.json")
        Directory.CreateDirectory(Path.GetDirectoryName(path: string)) |> ignore
        File.WriteAllText(path, """{ "targets": { "build": {} } }""")

        Assert.Empty(discoverFsharpLintTargets repoRoot)
    finally
        Directory.Delete(repoRoot, true)

[<Fact>]
let ``discoverFsharpLintTargets sorts results by repo-relative path`` () =
    let repoRoot = makeRepo ()

    try
        writeProjectJson
            (Path.Combine(repoRoot, "libs", "zeta-lib", "project.json"))
            "\"dotnet tool restore\", \"dotnet tool run fantomas --check .\""

        writeProjectJson
            (Path.Combine(repoRoot, "apps", "alpha-app", "project.json"))
            "\"dotnet tool restore\", \"dotnet tool run fantomas --check .\""

        let targets =
            discoverFsharpLintTargets repoRoot |> List.map (fun t -> t.ProjectJsonPath)

        Assert.Equal<string list>([ "apps/alpha-app/project.json"; "libs/zeta-lib/project.json" ], targets)
    finally
        Directory.Delete(repoRoot, true)

// ---- evaluateFsharpToolInvocation ----

let private target (commands: string list) : FsharpLintTarget =
    { ProjectJsonPath = "apps/fixture/project.json"
      Commands = commands }

[<Fact>]
let ``evaluateFsharpToolInvocation reports no findings for a compliant target`` () =
    let checks =
        evaluateFsharpToolInvocation [ target [ "dotnet tool restore"; "dotnet tool run fantomas --check ." ] ]

    Assert.Equal(1, checks.Length)
    Assert.Empty(checks.[0].Findings)

[<Fact>]
let ``evaluateFsharpToolInvocation flags a target missing dotnet tool restore entirely`` () =
    let checks =
        evaluateFsharpToolInvocation [ target [ "dotnet tool run fantomas --check ." ] ]

    Assert.Contains(
        checks.[0].Findings,
        fun (f: Finding) -> f.Message.Contains("does not restore the local .NET tool manifest")
    )

[<Fact>]
let ``evaluateFsharpToolInvocation flags a target that restores after invoking Fantomas`` () =
    let checks =
        evaluateFsharpToolInvocation [ target [ "dotnet tool run fantomas --check ."; "dotnet tool restore" ] ]

    Assert.Contains(
        checks.[0].Findings,
        fun (f: Finding) -> f.Message.Contains("does not restore the local .NET tool manifest")
    )

[<Fact>]
let ``evaluateFsharpToolInvocation flags a bare global fantomas invocation`` () =
    let checks =
        evaluateFsharpToolInvocation [ target [ "dotnet tool restore"; "fantomas --check ." ] ]

    Assert.Contains(
        checks.[0].Findings,
        fun (f: Finding) -> f.Message.Contains("invokes the global Fantomas app host directly")
    )

[<Fact>]
let ``evaluateFsharpToolInvocation accepts the dotnet fantomas driver form`` () =
    let checks =
        evaluateFsharpToolInvocation [ target [ "dotnet tool restore"; "dotnet fantomas --check ." ] ]

    Assert.Empty(checks.[0].Findings)

[<Fact>]
let ``evaluateFsharpToolInvocation marks every Finding as Blocking severity`` () =
    let checks = evaluateFsharpToolInvocation [ target [ "fantomas --check ." ] ]

    for f in checks.[0].Findings do
        Assert.Equal(Severity.Blocking, f.Severity)
        Assert.Equal(Some "apps/fixture/project.json", f.Path)

[<Fact>]
let ``evaluateFsharpToolInvocation evaluates every target regardless of compliance`` () =
    let checks =
        evaluateFsharpToolInvocation
            [ target [ "dotnet tool restore"; "dotnet tool run fantomas --check ." ]
              target [ "fantomas --check ." ] ]

    Assert.Equal(2, checks.Length)

[<Fact>]
let ``evaluateFsharpToolInvocation returns an empty list for an empty target list`` () =
    Assert.Empty(evaluateFsharpToolInvocation [])

// ---- checkUnformattedSample ----

[<Fact>]
let ``checkUnformattedSample never invokes the probe when no F# lint targets exist`` () =
    let mutable probed = false

    let probe: UnformattedSampleProbe =
        fun _ ->
            probed <- true
            Ok true

    let result = checkUnformattedSample [] "sample.fs" probe

    Assert.False(probed)
    Assert.True(Option.isNone result)

[<Fact>]
let ``checkUnformattedSample invokes the probe when at least one F# lint target exists`` () =
    let mutable receivedPath = ""

    let probe: UnformattedSampleProbe =
        fun path ->
            receivedPath <- path
            Ok false

    let result =
        checkUnformattedSample
            [ target [ "dotnet tool restore"; "dotnet tool run fantomas --check ." ] ]
            "sample.fs"
            probe

    Assert.Equal("sample.fs", receivedPath)
    Assert.Equal(Some(Ok false), result)

[<Fact>]
let ``checkUnformattedSample propagates a probe error`` () =
    let probe: UnformattedSampleProbe = fun _ -> Error "fantomas not found"

    let result =
        checkUnformattedSample
            [ target [ "dotnet tool restore"; "dotnet tool run fantomas --check ." ] ]
            "sample.fs"
            probe

    Assert.Equal(Some(Error "fantomas not found"), result)

[<Fact>]
let ``discoverFsharpLintTargets tolerates a project.json with no targets key at all`` () =
    let repoRoot = makeRepo ()

    try
        let path = Path.Combine(repoRoot, "apps", "no-targets-key", "project.json")
        Directory.CreateDirectory(Path.GetDirectoryName(path: string)) |> ignore
        File.WriteAllText(path, """{ "foo": "bar" }""")

        Assert.Empty(discoverFsharpLintTargets repoRoot)
    finally
        Directory.Delete(repoRoot, true)

[<Fact>]
let ``discoverFsharpLintTargets tolerates a lint target with no options key`` () =
    let repoRoot = makeRepo ()

    try
        let path = Path.Combine(repoRoot, "apps", "no-options-key", "project.json")
        Directory.CreateDirectory(Path.GetDirectoryName(path: string)) |> ignore
        File.WriteAllText(path, """{ "targets": { "lint": {} } }""")

        Assert.Empty(discoverFsharpLintTargets repoRoot)
    finally
        Directory.Delete(repoRoot, true)
