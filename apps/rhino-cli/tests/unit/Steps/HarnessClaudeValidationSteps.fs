module RhinoCli.Tests.Unit.Steps.HarnessClaudeValidationSteps

open System.IO
open RhinoCli.Application.Harness
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/harness/agents-validate-claude.feature" ]

/// The grade translation the validator reads from `repo-config.yml` at
/// runtime, declared here so a unit test exercises the vocabulary without
/// depending on the repository's own registry.
let private testGradeMaps: GradeMaps =
    { GradeOfAlias = Map.ofList [ "fable", "ultra"; "opus", "planning"; "sonnet", "execution"; "haiku", "fast" ]
      EffortOfGrade = Map.ofList [ "ultra", "high"; "planning", "high"; "execution", "xhigh"; "fast", "xhigh" ]
      ModelOfGrade = Map.empty }

/// Fixtures carry the effort their grade declares, because effort is a
/// property of the grade rather than of the agent: `sonnet` is the execution
/// grade, which sits at `xhigh`.
let private validAgent name =
    $"---\nname: {name}\ndescription: fixture agent\ntools: Read, Write\nmodel: sonnet\neffort: xhigh\ncolor: blue\n---\nBody.\n"

let private agentWithModelAndEffort name model effort =
    $"---\nname: {name}\ndescription: fixture agent\ntools: Read, Write\nmodel: {model}\neffort: {effort}\ncolor: blue\n---\nBody.\n"

let private agentWithModel name model =
    $"---\nname: {name}\ndescription: fixture agent\ntools: Read, Write\nmodel: {model}\ncolor: blue\n---\nBody.\n"

let private agentWithoutModel name =
    $"---\nname: {name}\ndescription: fixture agent\ntools: Read, Write\ncolor: blue\n---\nBody.\n"

let private passedSkill = ValidationCheck.passed "Skill: fixture" "valid"
let private failedSkill = ValidationCheck.failedMsg "Skill: fixture" "invalid"

type HarnessClaudeValidationSteps() =
    let mutable agents: (string * string) list = []
    let mutable declaredModel = ""
    let mutable declaredAgent = ""
    let mutable skillChecks: ValidationCheck list = [ passedSkill ]
    let mutable maps = testGradeMaps
    let mutable agentsOnly = false
    let mutable skillsOnly = false
    let mutable result = ValidationResult.empty

    let agentChecks () =
        agents
        |> List.fold
            (fun (checks, names) (path, content) ->
                let filename = Path.GetFileName path
                let current, next = validateAgentDocument maps path filename content names Set.empty
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
              "---\nname: missing-description\ntools: Read, Write\nmodel: sonnet\neffort: xhigh\ncolor: blue\n---\nBody.\n" ]

    [<Given>]
    member _.``a \.claude/ directory where one agent declares the "fable" model alias``() =
        agents <- [ "ultra-agent.md", agentWithModelAndEffort "ultra-agent" "fable" "high" ]

    [<Given>]
    member _.``a \.claude/ directory where one agent declares the "gpt-4" model alias``() =
        declaredAgent <- "foreign-model-agent"
        declaredModel <- "gpt-4"
        agents <- [ "foreign-model-agent.md", agentWithModel "foreign-model-agent" "gpt-4" ]

    [<Given>]
    member _.``a \.claude/ directory where the only agent sits in a role subfolder``() =
        declaredAgent <- "nested-agent"
        declaredModel <- "gpt-4"
        agents <- [ "swe/nested-agent.md", agentWithModel "nested-agent" "gpt-4" ]

    [<Given>]
    member _.``a \.claude/ directory where one agent declares no model field``() =
        declaredAgent <- "no-model-agent"
        declaredModel <- ""
        agents <- [ "no-model-agent.md", agentWithoutModel "no-model-agent" ]

    [<Given>]
    member _.``a \.claude/ directory where one agent declares an effort its grade does not``() =
        // `sonnet` is the execution grade, whose declared effort is `xhigh`.
        agents <- [ "wrong-effort-agent.md", agentWithModelAndEffort "wrong-effort-agent" "sonnet" "low" ]

    /// An unreadable or model-map-less registry deserializes to an empty
    /// vocabulary, which is the state the validator must refuse rather than
    /// wave through.
    [<Given>]
    member _.``a \.claude/ directory whose repo-config\.yml declares no model-map for claude-code``() =
        maps <-
            { emptyGradeMaps with
                EffortOfGrade = testGradeMaps.EffortOfGrade }

        agents <- [ "valid-agent.md", validAgent "valid-agent" ]

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
    member _.``the output reports the rejected model value``() =
        // The accepted vocabulary is compared as a set: it is assembled from
        // the registry, so its rendering order is an implementation detail.
        let expectedVocabulary =
            Set.ofList [ "fable"; "opus"; "sonnet"; "haiku"; "inherit"; "claude-*" ]

        Assert.Contains(
            result.Checks,
            fun check ->
                check.Name.Contains(declaredAgent)
                && check.Actual = $"Model: {declaredModel}"
                && Set.ofArray (check.Expected.Split('|')) = expectedVocabulary
        )

    [<Then>]
    member _.``the output identifies the nested agent``() =
        Assert.Contains(result.Checks, fun check -> check.Name.Contains("nested-agent"))

    [<Then>]
    member _.``the output reports the effort the grade declares``() =
        Assert.Contains(
            result.Checks,
            fun check ->
                check.Name.Contains("wrong-effort-agent")
                && check.Expected = "effort: xhigh (the execution grade)"
                && check.Actual = "effort: low"
        )

    [<Then>]
    member _.``the output reports that no grade vocabulary is declared``() =
        Assert.Contains(
            result.Checks,
            fun check -> check.Status = "failed" && check.Actual = "no grade vocabulary declared"
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
let ``ultra-tier fable alias passes`` () =
    HarnessClaudeScenarios.run
        (fun s -> s.``a \.claude/ directory where one agent declares the "fable" model alias`` ())
        (fun s -> s.``the developer runs agents validate-claude`` ())
        (fun s -> s.``the command exits successfully`` ())

[<Fact>]
let ``model outside the tier vocabulary fails`` () =
    HarnessClaudeScenarios.run
        (fun s -> s.``a \.claude/ directory where one agent declares the "gpt-4" model alias`` ())
        (fun s -> s.``the developer runs agents validate-claude`` ())
        (fun s ->
            s.``the command exits with a failure code`` ()
            s.``the output reports the rejected model value`` ())

[<Fact>]
let ``agent nested in a role subfolder is validated`` () =
    HarnessClaudeScenarios.run
        (fun s -> s.``a \.claude/ directory where the only agent sits in a role subfolder`` ())
        (fun s -> s.``the developer runs agents validate-claude`` ())
        (fun s ->
            s.``the command exits with a failure code`` ()
            s.``the output identifies the nested agent`` ())

[<Fact>]
let ``agent declaring no model fails`` () =
    HarnessClaudeScenarios.run
        (fun s -> s.``a \.claude/ directory where one agent declares no model field`` ())
        (fun s -> s.``the developer runs agents validate-claude`` ())
        (fun s ->
            s.``the command exits with a failure code`` ()
            s.``the output reports the rejected model value`` ())

[<Fact>]
let ``effort contradicting the grade fails`` () =
    HarnessClaudeScenarios.run
        (fun s -> s.``a \.claude/ directory where one agent declares an effort its grade does not`` ())
        (fun s -> s.``the developer runs agents validate-claude`` ())
        (fun s ->
            s.``the command exits with a failure code`` ()
            s.``the output reports the effort the grade declares`` ())

[<Fact>]
let ``a registry with no grade vocabulary fails closed`` () =
    HarnessClaudeScenarios.run
        (fun s -> s.``a \.claude/ directory whose repo-config\.yml declares no model-map for claude-code`` ())
        (fun s -> s.``the developer runs agents validate-claude`` ())
        (fun s ->
            s.``the command exits with a failure code`` ()
            s.``the output reports that no grade vocabulary is declared`` ())

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
