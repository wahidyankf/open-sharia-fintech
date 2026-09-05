module RhinoCli.Tests.Unit.Steps.FsharpToolInvocationUnitTests

open Xunit
open RhinoCli.Application.Doctor
open RhinoCli.Domain.Types

let private target (commands: string list) : FsharpLintTarget =
    { ProjectJsonPath = "apps/fixture/project.json"
      Commands = commands }

[<Theory>]
[<InlineData("dotnet tool run fantomas --check .")>]
[<InlineData("dotnet tool restore;fantomas --check .")>]
[<InlineData("dotnet tool run fantomas --check .;dotnet tool restore")>]
let ``invalid command sequences report blocking findings`` (commandText: string) =
    let commands = commandText.Split(';') |> Array.toList
    let result = evaluateFsharpToolInvocation [ target commands ] |> List.exactlyOne
    Assert.NotEmpty(result.Findings)

    result.Findings
    |> List.iter (fun finding ->
        Assert.Equal(Severity.Blocking, finding.Severity)
        Assert.Equal(Some "apps/fixture/project.json", finding.Path))

[<Theory>]
[<InlineData("dotnet tool run fantomas --check .")>]
[<InlineData("dotnet fantomas --check .")>]
let ``local Fantomas forms pass after tool restore`` invocation =
    let result =
        evaluateFsharpToolInvocation [ target [ "dotnet tool restore"; invocation ] ]
        |> List.exactlyOne

    Assert.Empty(result.Findings)

[<Fact>]
let ``evaluation preserves target cardinality`` () =
    let targets =
        [ target [ "dotnet tool restore"; "dotnet fantomas --check ." ]
          target [ "fantomas --check ." ] ]

    Assert.Equal(targets.Length, evaluateFsharpToolInvocation targets |> List.length)

[<Fact>]
let ``evaluation accepts an empty target set`` () =
    Assert.Empty(evaluateFsharpToolInvocation [])

[<Fact>]
let ``sample probe is skipped without lint targets`` () =
    let mutable calls = 0

    let probe _ =
        calls <- calls + 1
        Ok true

    Assert.Equal(None, checkUnformattedSample [] "sample.fs" probe)
    Assert.Equal(0, calls)

[<Theory>]
[<InlineData(true)>]
[<InlineData(false)>]
let ``sample probe result is preserved when targets exist`` formatted =
    let mutable received = ""

    let probe path =
        received <- path
        Ok formatted

    let result =
        checkUnformattedSample [ target [ "dotnet tool restore"; "dotnet fantomas --check ." ] ] "sample.fs" probe

    Assert.Equal("sample.fs", received)
    Assert.Equal(Some(Ok formatted), result)

[<Fact>]
let ``sample probe errors are preserved`` () =
    let probe _ = Error "fantomas unavailable"

    let result =
        checkUnformattedSample [ target [ "dotnet tool restore"; "dotnet fantomas --check ." ] ] "sample.fs" probe

    Assert.Equal(Some(Error "fantomas unavailable"), result)
