module RhinoCli.Tests.Unit.Steps.FsharpToolInvocationSteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/system/fsharp-tool-invocation.feature" ]

open TickSpec
open Xunit
open RhinoCli.Application.Doctor
open RhinoCli.Domain.Types

type FsharpToolInvocationSteps() =
    let mutable targets: FsharpLintTarget list = []
    let mutable checks: FsharpToolInvocationCheck list = []
    let mutable probeCalls = 0
    let mutable probeResult: Result<bool, string> option = None

    [<Given>]
    member _.``the local F.*``() =
        targets <-
            [ { ProjectJsonPath = "apps/example/project.json"
                Commands = [ "dotnet tool restore"; "dotnet tool run fantomas --check apps/example" ] } ]

    [<When>]
    member _.``every locally discovered F.*``() =
        checks <- evaluateFsharpToolInvocation targets

    [<Then>]
    member _.``every discovered F.*``() =
        Assert.Equal(targets.Length, checks.Length)
        Assert.NotEmpty(checks)

    [<Then>]
    member _.``each target restores its local .NET tool manifest before running Fantomas``() =
        checks
        |> List.collect _.Findings
        |> List.iter (fun finding ->
            Assert.DoesNotContain("does not restore the local .NET tool manifest", finding.Message))

    [<Then>]
    member _.``no target invokes the global Fantomas app host directly``() =
        checks
        |> List.collect _.Findings
        |> List.iter (fun finding -> Assert.DoesNotContain("invokes the global Fantomas app host", finding.Message))

    [<Then>]
    member _.``an unformatted source file is checked only when F.*``() =
        let probe: UnformattedSampleProbe =
            fun _ ->
                probeCalls <- probeCalls + 1
                Ok false

        probeResult <- checkUnformattedSample targets "sample.fs" probe
        Assert.Equal(1, probeCalls)
        Assert.Equal(Some(Ok false), probeResult)

[<Fact>]
let ``Every locally discovered F# lint target uses the pinned local Fantomas tool`` () =
    let steps = FsharpToolInvocationSteps()
    steps.``the local F.*`` ()
    steps.``every locally discovered F.*`` ()
    steps.``every discovered F.*`` ()
    steps.``each target restores its local .NET tool manifest before running Fantomas`` ()
    steps.``no target invokes the global Fantomas app host directly`` ()
    steps.``an unformatted source file is checked only when F.*`` ()
