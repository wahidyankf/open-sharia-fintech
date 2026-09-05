module RhinoCli.Tests.Unit.Steps.HarnessAuditSteps

open RhinoCli.Application.Harness
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/harness/harness-audit.feature" ]

type HarnessAuditSteps() =
    let mutable failingMembers: (string * int) list = []
    let mutable outcome = aggregateHarnessAudit []

    [<Given>]
    member _.``a repository with no \.claude or \.opencode agent directories``() =
        failingMembers <- [ "validate-claude", 2 ]

    [<When>]
    member _.``the developer runs "rhino-cli harness audit"``() =
        outcome <- aggregateHarnessAudit failingMembers

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.NotEqual(0, outcome.ExitCode)

    [<Then>]
    member _.``the output names the failing "validate-claude" harness validator``() =
        Assert.Contains("validate-claude: 2 check(s) failed", outcome.Output)

[<Fact>]
let ``aggregate audit reports its failing validator`` () =
    let steps = HarnessAuditSteps()
    steps.``a repository with no \.claude or \.opencode agent directories`` ()
    steps.``the developer runs "rhino-cli harness audit"`` ()
    steps.``the command exits with a failure code`` ()
    steps.``the output names the failing "validate-claude" harness validator`` ()
