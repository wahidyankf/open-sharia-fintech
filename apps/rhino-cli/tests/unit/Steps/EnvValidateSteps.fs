module RhinoCli.Tests.Unit.Steps.EnvValidateSteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/env/env-validate-app-drift.feature" ]

open TickSpec
open Xunit
open RhinoCli.Application.Env

type EnvValidateSteps() =
    let mutable surface: SurfaceConfig =
        { Root = "surface"
          Kind = App
          Lang = "rust"
          Allowlist = [] }

    let mutable declared: string list = []
    let mutable read: string list = []
    let mutable findings: Finding list = []

    [<Given>]
    member _.``an app surface whose .env.example declares a key the source code never reads``() =
        declared <- [ "UNREAD_KEY" ]
        read <- []

    [<Given>]
    member _.``an app surface whose source code reads a key absent from .env.example``() =
        declared <- []
        read <- [ "UNDECLARED_KEY" ]

    [<Given>]
    member _.``an F.*``() =
        surface <- { surface with Lang = "fsharp" }
        declared <- [ "WRAPPED_KEY" ]
        read <- [ "WRAPPED_KEY" ]

    [<When>]
    member _.``the developer runs env validate``() =
        findings <- validateAppKeys surface declared read

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.NotEmpty findings

    [<Then>]
    member _.``the command exits successfully``() = Assert.Empty findings

    [<Then>]
    member _.``the output names the key as declared-but-unread``() =
        Assert.Contains(findings, fun finding -> finding.Drift = DeclaredButUnread && finding.Key = "UNREAD_KEY")

    [<Then>]
    member _.``the output names the key as read-but-undeclared``() =
        Assert.Contains(findings, fun finding -> finding.Drift = ReadButUndeclared && finding.Key = "UNDECLARED_KEY")

[<Fact>]
let ``declared but unread key is rejected by pure drift policy`` () =
    let steps = EnvValidateSteps()
    steps.``an app surface whose .env.example declares a key the source code never reads`` ()
    steps.``the developer runs env validate`` ()
    steps.``the command exits with a failure code`` ()
    steps.``the output names the key as declared-but-unread`` ()

[<Fact>]
let ``read but undeclared key is rejected by pure drift policy`` () =
    let steps = EnvValidateSteps()
    steps.``an app surface whose source code reads a key absent from .env.example`` ()
    steps.``the developer runs env validate`` ()
    steps.``the command exits with a failure code`` ()
    steps.``the output names the key as read-but-undeclared`` ()

[<Fact>]
let ``matching wrapped F sharp key is accepted by pure drift policy`` () =
    let steps = EnvValidateSteps()
    steps.``an F.*`` ()
    steps.``the developer runs env validate`` ()
    steps.``the command exits successfully`` ()
