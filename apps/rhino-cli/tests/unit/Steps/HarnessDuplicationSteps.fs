module RhinoCli.Tests.Unit.Steps.HarnessDuplicationSteps

open TickSpec
open Xunit
open RhinoCli.Application.Harness

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/harness/agents-detect-duplication.feature" ]

let private prose prefix count =
    [ 1..count ]
    |> List.map (fun n -> $"{prefix} substantive line {n}")
    |> String.concat "\n"

type HarnessDuplicationSteps() =
    let mutable files: (string * string) list = []
    let mutable findings: DuplicationFinding list = []

    [<Given>]
    member _.``a repository with agent and skill files whose bodies share no 10-line verbatim windows``() =
        files <- [ "a.md", prose "alpha" 12; "SKILL.md", prose "beta" 12 ]

    [<Given>]
    member _.``a repository with two agent files that share 12 consecutive lines verbatim``() =
        let shared = prose "shared" 12 in files <- [ "a.md", shared; "b.md", shared ]

    [<Given>]
    member _.``a repository with an agent file whose body matches 11 consecutive lines of a SKILL.md``() =
        let shared = prose "shared" 11 in files <- [ "agent.md", shared; "skills/demo/SKILL.md", shared ]

    [<Given>]
    member _.``a repository where two agent files share a 10-line window composed only of headings or blank lines``() =
        let shared = [ 1..10 ] |> List.map (fun n -> $"# Heading {n}") |> String.concat "\n" in
        files <- [ "a.md", shared; "b.md", shared ]

    [<When>]
    member _.``the developer runs agents detect-duplication``() =
        findings <- detectDuplicationFromContents files

    [<Then>]
    member _.``the command exits successfully``() = Assert.Empty(findings)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.NotEmpty(findings)

    [<Then>]
    member _.``the output reports zero duplication clusters``() = Assert.Empty(findings)

    [<Then>]
    member _.``the output identifies the duplicated cluster across both agents``() =
        Assert.Equal<string list>([ "a.md"; "b.md" ], findings.Head.Files)

    [<Then>]
    member _.``the output identifies the duplicated cluster across the agent and the skill``() =
        Assert.Contains("agent.md", findings.Head.Files)
        Assert.Contains("skills/demo/SKILL.md", findings.Head.Files)

[<Fact>]
let ``distinct bodies pass`` () =
    let w = HarnessDuplicationSteps() in
    w.``a repository with agent and skill files whose bodies share no 10-line verbatim windows`` ()
    w.``the developer runs agents detect-duplication`` ()
    w.``the command exits successfully`` ()
    w.``the output reports zero duplication clusters`` ()

[<Fact>]
let ``agent duplicate fails`` () =
    let w = HarnessDuplicationSteps() in
    w.``a repository with two agent files that share 12 consecutive lines verbatim`` ()
    w.``the developer runs agents detect-duplication`` ()
    w.``the command exits with a failure code`` ()
    w.``the output identifies the duplicated cluster across both agents`` ()

[<Fact>]
let ``agent skill duplicate fails`` () =
    let w = HarnessDuplicationSteps() in
    w.``a repository with an agent file whose body matches 11 consecutive lines of a SKILL.md`` ()
    w.``the developer runs agents detect-duplication`` ()
    w.``the command exits with a failure code`` ()
    w.``the output identifies the duplicated cluster across the agent and the skill`` ()

[<Fact>]
let ``heading window is excluded`` () =
    let w = HarnessDuplicationSteps() in
    w.``a repository where two agent files share a 10-line window composed only of headings or blank lines`` ()
    w.``the developer runs agents detect-duplication`` ()
    w.``the command exits successfully`` ()
    w.``the output reports zero duplication clusters`` ()
