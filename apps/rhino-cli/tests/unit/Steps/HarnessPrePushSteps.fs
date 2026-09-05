module RhinoCli.Tests.Unit.Steps.HarnessPrePushSteps

open RhinoCli.Application.Harness
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/harness/governance-word-budget-pre-push.feature" ]

type HarnessPrePushSteps() =
    let mutable changedPaths: string list = []
    let mutable hasFail = false
    let mutable validatorCalls = 0
    let mutable outcome = { GateInvoked = false; ExitCode = -1 }

    [<Given>]
    member _.``my push range modifies "([^"]+)"``(path: string) = changedPaths <- [ path ]

    [<Given>]
    member _.``my push range modifies only "([^"]+)"``(path: string) = changedPaths <- [ path ]

    [<Given>]
    member _.``"AGENTS.md" exceeds its fail ceiling``() = hasFail <- true

    [<Given>]
    member _.``"AGENTS.md" is within its fail ceiling``() = hasFail <- false

    [<When>]
    member _.``the pre-push hook runs``() =
        outcome <-
            evaluatePrePushWordBudgetGate changedPaths (fun () ->
                validatorCalls <- validatorCalls + 1
                hasFail)

    [<Then>]
    member _.``the word-budget gate runs``() =
        Assert.True(outcome.GateInvoked)
        Assert.Equal(1, validatorCalls)

    [<Then>]
    member _.``the push is aborted with a non-zero exit``() = Assert.NotEqual(0, outcome.ExitCode)

    [<Then>]
    member _.``the word-budget validation target is not invoked``() =
        Assert.False(outcome.GateInvoked)
        Assert.Equal(0, validatorCalls)

    [<Then>]
    member _.``the word-budget validation target runs and exits 0``() =
        Assert.True(outcome.GateInvoked)
        Assert.Equal(1, validatorCalls)
        Assert.Equal(0, outcome.ExitCode)

    [<Then>]
    member _.``the push proceeds``() = Assert.Equal(0, outcome.ExitCode)

module private HarnessPrePushScenarios =
    let failing () =
        let steps = HarnessPrePushSteps()
        steps.``my push range modifies "([^"]+)"`` ("AGENTS.md")
        steps.``"AGENTS.md" exceeds its fail ceiling`` ()
        steps.``the pre-push hook runs`` ()
        steps.``the word-budget gate runs`` ()
        steps.``the push is aborted with a non-zero exit`` ()

    let skipped () =
        let steps = HarnessPrePushSteps()
        steps.``my push range modifies only "([^"]+)"`` ("apps/ose-www/src/page.tsx")
        steps.``the pre-push hook runs`` ()
        steps.``the word-budget validation target is not invoked`` ()

    let passing () =
        let steps = HarnessPrePushSteps()
        steps.``my push range modifies "([^"]+)"`` ("AGENTS.md")
        steps.``"AGENTS.md" is within its fail ceiling`` ()
        steps.``the pre-push hook runs`` ()
        steps.``the word-budget validation target runs and exits 0`` ()
        steps.``the push proceeds`` ()

    let rtk () =
        let steps = HarnessPrePushSteps()
        steps.``my push range modifies "([^"]+)"`` ("RTK.md")
        steps.``the pre-push hook runs`` ()
        steps.``the word-budget gate runs`` ()

[<Fact>]
let ``over-budget instruction changes block push`` () = HarnessPrePushScenarios.failing ()

[<Fact>]
let ``non-instruction changes skip word budget`` () = HarnessPrePushScenarios.skipped ()

[<Fact>]
let ``in-budget instruction changes pass`` () = HarnessPrePushScenarios.passing ()

[<Fact>]
let ``RTK changes invoke configured gate`` () = HarnessPrePushScenarios.rtk ()
