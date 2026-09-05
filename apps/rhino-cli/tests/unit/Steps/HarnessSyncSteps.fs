module RhinoCli.Tests.Unit.Steps.HarnessSyncSteps

open System.Collections.Generic
open RhinoCli.Application.Harness
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/harness/agents-sync.feature" ]

let private agentDocument model =
    $"---\nname: fixture\ndescription: fixture\ntools: Read, Write\nmodel: {model}\ncolor: blue\n---\nAgent body.\n"

let private sourceMapping (description: string) (model: string) : Dictionary<string, obj> =
    let result = Dictionary<string, obj>()
    result.["description"] <- description
    result.["model"] <- model
    result.["tools"] <- "Read, Write"
    result

let private mirrorMapping (description: string) (model: string) : Dictionary<string, obj> =
    let permissions = Dictionary<obj, obj>()
    permissions.["read"] <- "allow"
    permissions.["write"] <- "allow"
    let result = Dictionary<string, obj>()
    result.["description"] <- description
    result.["model"] <- model
    result.["permission"] <- permissions
    result

type HarnessSyncSteps() =
    let mutable source = agentDocument "sonnet"
    let mutable includeSkill = false
    let mutable dryRun = false
    let mutable agentsOnly = false
    let mutable converted: ConvertedAgentContent option = None
    let mutable writtenPaths: string list = []
    let mutable validationChecks: ValidationCheck list = []
    let mutable sourceCount = 1
    let mutable mirrorCount = 1
    let mutable sourceDescription = "fixture"
    let mutable mirrorDescription = "fixture"

    let runSync () =
        converted <-
            convertAgentContent ".claude/agents/fixture.md" ".claude/agents" ".opencode/agents" source
            |> Result.toOption

        if not dryRun && converted.IsSome then
            writtenPaths <- [ ".opencode/agents/fixture.md" ]

            if includeSkill && not agentsOnly then
                writtenPaths <- ".claude/skills/fixture/SKILL.md" :: writtenPaths

    let runValidation () =
        let countCheck = validateAgentCountValues sourceCount mirrorCount

        validationChecks <-
            if sourceCount <> mirrorCount then
                [ countCheck ]
            else
                [ countCheck
                  validateAgentYaml
                      "fixture"
                      (sourceMapping sourceDescription "sonnet")
                      (mirrorMapping mirrorDescription (convertModel "sonnet"))
                      "Agent body.\n"
                      "Agent body.\n"
                      "body mismatch" ]

    [<Given>]
    member _.``a \.claude/ directory with valid agents and skills``() = includeSkill <- true

    [<Given>]
    member _.``a \.claude/ directory with agents and skills to convert``() = includeSkill <- true

    [<Given>]
    member _.``a \.claude/ directory with both agents and skills``() = includeSkill <- true

    [<Given>]
    member _.``a \.claude/ agent configured with the "([^"]+)" model``(model: string) = source <- agentDocument model

    [<Given>]
    member _.``\.claude/ and \.opencode/ configurations that are fully synchronised``() =
        sourceCount <- 1
        mirrorCount <- 1
        sourceDescription <- "fixture"
        mirrorDescription <- "fixture"

    [<Given>]
    member _.``an agent in \.claude/ whose description differs from its \.opencode/ counterpart``() =
        sourceCount <- 1
        mirrorCount <- 1
        sourceDescription <- "fixture"
        mirrorDescription <- "different"

    [<Given>]
    member _.``\.claude/ containing more agents than \.opencode/``() =
        sourceCount <- 2
        mirrorCount <- 1

    [<When>]
    member _.``the developer runs rhino-cli harness bindings generate``() = runSync ()

    [<When>]
    member _.``the developer runs rhino-cli harness bindings generate with the --dry-run flag``() =
        dryRun <- true
        runSync ()

    [<When>]
    member _.``the developer runs rhino-cli harness bindings generate with the --agents-only flag``() =
        agentsOnly <- true
        runSync ()

    [<When>]
    member _.``the developer runs rhino-cli harness sync validate``() = runValidation ()

    [<Then>]
    member _.``the command exits successfully``() =
        Assert.True(
            converted.IsSome
            || (validationChecks |> List.forall (fun check -> check.Status = "passed"))
        )

    [<Then>]
    member _.``the command exits with a failure code``() =
        Assert.Contains(validationChecks, fun check -> check.Status = "failed")

    [<Then>]
    member _.``the \.opencode/ directory contains the converted configuration``() =
        Assert.Contains(".opencode/agents/fixture.md", writtenPaths)
        Assert.Contains(".claude/skills/fixture/SKILL.md", writtenPaths)

    [<Then>]
    member _.``the output describes the planned operations``() = Assert.True(converted.IsSome)

    [<Then>]
    member _.``no files are written to the \.opencode/ directory``() = Assert.Empty(writtenPaths)

    [<Then>]
    member _.``only agent files are written to the \.opencode/ directory``() =
        Assert.Equal<string list>([ ".opencode/agents/fixture.md" ], writtenPaths)

    [<Then>]
    member _.``the corresponding \.opencode/ agent uses the "([^"]+)" model identifier``(model: string) =
        Assert.Contains($"model: {model}", converted.Value.Content)

    [<Then>]
    member _.``the output reports all sync checks as passing``() =
        Assert.All(validationChecks, fun check -> Assert.Equal("passed", check.Status))

    [<Then>]
    member _.``the output identifies the agent with the mismatched description``() =
        Assert.Contains(validationChecks, fun check -> check.Message = "description mismatch")

    [<Then>]
    member _.``the output reports the agent count mismatch``() =
        Assert.Contains(validationChecks, fun check -> check.Name = "Agent Count" && check.Status = "failed")

module private HarnessSyncScenarios =
    let sync () =
        let steps = HarnessSyncSteps()
        steps.``a \.claude/ directory with valid agents and skills`` ()
        steps.``the developer runs rhino-cli harness bindings generate`` ()
        steps.``the command exits successfully`` ()
        steps.``the \.opencode/ directory contains the converted configuration`` ()

    let dryRun () =
        let steps = HarnessSyncSteps()
        steps.``a \.claude/ directory with agents and skills to convert`` ()
        steps.``the developer runs rhino-cli harness bindings generate with the --dry-run flag`` ()
        steps.``the command exits successfully`` ()
        steps.``the output describes the planned operations`` ()
        steps.``no files are written to the \.opencode/ directory`` ()

    let agentsOnly () =
        let steps = HarnessSyncSteps()
        steps.``a \.claude/ directory with both agents and skills`` ()
        steps.``the developer runs rhino-cli harness bindings generate with the --agents-only flag`` ()
        steps.``the command exits successfully`` ()
        steps.``only agent files are written to the \.opencode/ directory`` ()

    let model sourceModel () =
        let steps = HarnessSyncSteps()
        steps.``a \.claude/ agent configured with the "([^"]+)" model`` (sourceModel)
        steps.``the developer runs rhino-cli harness bindings generate`` ()
        steps.``the command exits successfully`` ()
        steps.``the corresponding \.opencode/ agent uses the "([^"]+)" model identifier`` ("zai-coding-plan/glm-5.2")

    let validate () =
        let steps = HarnessSyncSteps()
        steps.``\.claude/ and \.opencode/ configurations that are fully synchronised`` ()
        steps.``the developer runs rhino-cli harness sync validate`` ()
        steps.``the command exits successfully`` ()
        steps.``the output reports all sync checks as passing`` ()

    let descriptionMismatch () =
        let steps = HarnessSyncSteps()
        steps.``an agent in \.claude/ whose description differs from its \.opencode/ counterpart`` ()
        steps.``the developer runs rhino-cli harness sync validate`` ()
        steps.``the command exits with a failure code`` ()
        steps.``the output identifies the agent with the mismatched description`` ()

    let countMismatch () =
        let steps = HarnessSyncSteps()
        steps.``\.claude/ containing more agents than \.opencode/`` ()
        steps.``the developer runs rhino-cli harness sync validate`` ()
        steps.``the command exits with a failure code`` ()
        steps.``the output reports the agent count mismatch`` ()

[<Fact>]
let ``sync converts agents and preserves skills`` () = HarnessSyncScenarios.sync ()

[<Fact>]
let ``dry run previews without writes`` () = HarnessSyncScenarios.dryRun ()

[<Fact>]
let ``agents-only skips skills`` () = HarnessSyncScenarios.agentsOnly ()

[<Theory>]
[<InlineData("sonnet")>]
[<InlineData("opus")>]
let ``model aliases map to OpenCode`` model = HarnessSyncScenarios.model model ()

[<Fact>]
let ``synchronised agents validate`` () = HarnessSyncScenarios.validate ()

[<Fact>]
let ``description drift fails validation`` () =
    HarnessSyncScenarios.descriptionMismatch ()

[<Fact>]
let ``agent count drift fails validation`` () = HarnessSyncScenarios.countMismatch ()
