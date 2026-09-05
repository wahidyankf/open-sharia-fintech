module RhinoCli.Tests.Unit.Steps.HarnessClaudeValidationSteps

open RhinoCli.Application.Harness
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/harness/agents-validate-claude.feature" ]

let private validAgent name =
    $"---\nname: {name}\ndescription: fixture agent\ntools: Read, Write\nmodel: sonnet\ncolor: blue\n---\nBody.\n"

let private passedSkill = ValidationCheck.passed "Skill: fixture" "valid"
let private failedSkill = ValidationCheck.failedMsg "Skill: fixture" "invalid"

type HarnessClaudeValidationSteps() =
    let mutable agents: (string * string) list = []
    let mutable skillChecks: ValidationCheck list = [ passedSkill ]
    let mutable agentsOnly = false
    let mutable skillsOnly = false
    let mutable result = ValidationResult.empty

    let agentChecks () =
        agents
        |> List.fold
            (fun (checks, names) (filename, content) ->
                let current, next = validateAgentDocument filename filename content names Set.empty
                checks @ current, next)
            ([], Set.empty)
        |> fst

    [<Given>]
    member _.``a \.claude/ directory where all agents and skills are valid``() =
        agents <- [ "valid-agent.md", validAgent "valid-agent" ]

    [<Given>]
    member _.``a \.claude/ directory where one agent is missing the required "description" field``() =
        agents <-
            [ "missing-description.md",
              "---\nname: missing-description\ntools: Read, Write\nmodel: sonnet\ncolor: blue\n---\nBody.\n" ]

    [<Given>]
    member _.``a \.claude/ directory containing two agent files declaring the same name``() =
        agents <- [ "duplicate.md", validAgent "duplicate"; "other.md", validAgent "duplicate" ]

    [<Given>]
    member _.``a \.claude/ directory where agents are valid but skills have issues``() =
        agents <- [ "valid-agent.md", validAgent "valid-agent" ]
        skillChecks <- [ failedSkill ]

    [<Given>]
    member _.``a \.claude/ directory where skills are valid but agents have issues``() =
        agents <- [ "missing-description.md", "---\nname: missing-description\ntools: Read\n---\nBody.\n" ]
        skillChecks <- [ passedSkill ]

    [<When>]
    member _.``the developer runs agents validate-claude``() =
        result <- tallyClaudeValidation false false skillChecks (agentChecks ())

    [<When>]
    member _.``the developer runs agents validate-claude with the --agents-only flag``() =
        agentsOnly <- true
        result <- tallyClaudeValidation agentsOnly skillsOnly skillChecks (agentChecks ())

    [<When>]
    member _.``the developer runs agents validate-claude with the --skills-only flag``() =
        skillsOnly <- true
        result <- tallyClaudeValidation agentsOnly skillsOnly skillChecks (agentChecks ())

    [<Then>]
    member _.``the command exits successfully``() = Assert.Equal(0, result.FailedChecks)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.True(result.FailedChecks > 0)

    [<Then>]
    member _.``the output reports all checks as passing``() =
        Assert.All(result.Checks, fun check -> Assert.Equal("passed", check.Status))

    [<Then>]
    member _.``the output identifies the agent and the missing field``() =
        Assert.Contains(
            result.Checks,
            fun check ->
                check.Name.Contains("missing-description")
                && check.Actual.Contains("description")
        )

    [<Then>]
    member _.``the output reports the duplicate agent name``() =
        Assert.Contains(result.Checks, fun check -> check.Actual.Contains("Duplicate name: duplicate"))

module private HarnessClaudeScenarios =
    let run givenStep whenStep thenSteps =
        let steps = HarnessClaudeValidationSteps()
        givenStep steps
        whenStep steps
        thenSteps steps

[<Fact>]
let ``valid Claude binding passes`` () =
    HarnessClaudeScenarios.run
        (fun s -> s.``a \.claude/ directory where all agents and skills are valid`` ())
        (fun s -> s.``the developer runs agents validate-claude`` ())
        (fun s ->
            s.``the command exits successfully`` ()
            s.``the output reports all checks as passing`` ())

[<Fact>]
let ``missing description fails`` () =
    HarnessClaudeScenarios.run
        (fun s -> s.``a \.claude/ directory where one agent is missing the required "description" field`` ())
        (fun s -> s.``the developer runs agents validate-claude`` ())
        (fun s ->
            s.``the command exits with a failure code`` ()
            s.``the output identifies the agent and the missing field`` ())

[<Fact>]
let ``duplicate agent name fails`` () =
    HarnessClaudeScenarios.run
        (fun s -> s.``a \.claude/ directory containing two agent files declaring the same name`` ())
        (fun s -> s.``the developer runs agents validate-claude`` ())
        (fun s ->
            s.``the command exits with a failure code`` ()
            s.``the output reports the duplicate agent name`` ())

[<Fact>]
let ``agents-only ignores skill failures`` () =
    HarnessClaudeScenarios.run
        (fun s -> s.``a \.claude/ directory where agents are valid but skills have issues`` ())
        (fun s -> s.``the developer runs agents validate-claude with the --agents-only flag`` ())
        (fun s -> s.``the command exits successfully`` ())

[<Fact>]
let ``skills-only ignores agent failures`` () =
    HarnessClaudeScenarios.run
        (fun s -> s.``a \.claude/ directory where skills are valid but agents have issues`` ())
        (fun s -> s.``the developer runs agents validate-claude with the --skills-only flag`` ())
        (fun s -> s.``the command exits successfully`` ())
