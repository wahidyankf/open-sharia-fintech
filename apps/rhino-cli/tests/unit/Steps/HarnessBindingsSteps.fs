module RhinoCli.Tests.Unit.Steps.HarnessBindingsSteps

open RhinoCli.Application
open RhinoCli.Application.Harness
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/harness/agents-bindings.feature" ]

let private harnessEntry name : RepoConfig.HarnessEntry =
    { Name = name
      Tier = RepoConfig.Tier.Generated
      AgentDir = Some("." + name + "/agents")
      Mirrors = Some ".claude/agents"
      ForbidDir = None
      SkillsDir = None
      SkillsMirrors = None
      Vendored = []
      ModelMap = Map.empty
      Catalog = None
      Ownership = [] }

type HarnessBindingsSteps() =
    let mutable config = RepoConfig.empty
    let mutable requested = ""
    let mutable presentDirectory = ".codex"
    let mutable directoryExists = true
    let mutable catalog = Ok "- `.codex`"

    let mutable binding =
        { RelPath = ".codex/agents/demo.toml"
          Content = "generated" }

    let mutable bindingActual: Result<string option, string> = Ok(Some "generated")
    let mutable codexFiles: Result<string list, unit> = Ok []
    let mutable mirrorNames: Result<string list, string> = Ok [ "demo.md" ]
    let mutable sourceNames: string list = [ "demo" ]
    let mutable checks: ValidationCheck list = []
    let mutable nameResult: Result<unit, string> = Ok()

    [<Given>]
    member _.``the repo-config\.yml harness registry declares codex``() =
        config <-
            { RepoConfig.empty with
                Harness = [ harnessEntry "codex" ] }

    [<Given>]
    member _.``the repo-config\.yml harness registry does not declare cursor``() =
        config <-
            { RepoConfig.empty with
                Harness = [ harnessEntry "codex" ] }

    [<Given>]
    member _.``a repository whose generated binding files match the generated content``() =
        bindingActual <- Ok(Some binding.Content)

    [<Given>]
    member _.``the platform-bindings catalog references every present binding directory``() =
        presentDirectory <- ".codex"
        directoryExists <- true
        catalog <- Ok "| Codex | `.codex` |"

    [<Given>]
    member _.``a repository with a known binding directory that the platform-bindings catalog does not reference``() =
        presentDirectory <- ".codex"
        directoryExists <- true
        catalog <- Ok "| Claude | `.claude` |"

    [<Given>]
    member _.``a repository where some known binding directories do not exist on disk``() =
        presentDirectory <- ".amazonq"
        directoryExists <- false
        catalog <- Ok ""

    [<Given>]
    member _.``a repository whose \.codex/agents directory holds a standalone \.toml agent file``() =
        codexFiles <- Ok [ "demo.toml" ]

    [<Given>]
    member _.``a repository whose \.codex/agents directory holds a \.md agent file``() = codexFiles <- Ok [ "demo.md" ]

    [<Given>]
    member _.``a repository whose generated agent directory holds a mirror with no source agent``() =
        mirrorNames <- Ok [ "README.md"; "rules-maker.md"; "repo-rules-maker.md" ]
        sourceNames <- [ "rules-maker" ]

    [<Given>]
    member _.``a repository whose generated agent mirrors each have a source agent``() =
        mirrorNames <- Ok [ "README.md"; "rules-maker.md" ]
        sourceNames <- [ "rules-maker" ]

    [<When>]
    member _.``the developer runs harness bindings generate for codex``() =
        requested <- "codex"
        nameResult <- validateHarnessName config requested

    [<When>]
    member _.``the developer runs harness bindings generate for cursor``() =
        requested <- "cursor"
        nameResult <- validateHarnessName config requested

    [<When>]
    member _.``the developer runs harness bindings validate``() =
        checks <-
            [ validateBindingContent binding bindingActual "regenerate the binding"
              validateCatalogCoverageState presentDirectory directoryExists catalog
              validateCodexAgentFilenames true codexFiles
              validateMirrorOrphanState ".opencode/agents" mirrorNames sourceNames ]

    [<Then>]
    member _.``the harness name is not rejected as unknown``() =
        Assert.Equal<Result<unit, string>>(Ok(), nameResult)

    [<Then>]
    member _.``the command exits successfully``() =
        Assert.True(Result.isOk nameResult)
        Assert.DoesNotContain(checks, fun check -> check.Status = "failed")

    [<Then>]
    member _.``the command exits with a failure code``() =
        Assert.True(
            Result.isError nameResult
            || (checks |> List.exists (fun check -> check.Status = "failed"))
        )

    [<Then>]
    member _.``the error names the registry-derived accepted set``() =
        match nameResult with
        | Error error -> Assert.Contains("expected one of 'codex'", error)
        | Ok() -> failwith "the absent harness was unexpectedly accepted"

    [<Then>]
    member _.``the output reports all binding checks as passing``() =
        Assert.All(checks, fun check -> Assert.Equal("passed", check.Status))

    [<Then>]
    member _.``the output identifies the binding directory missing a catalog row``() =
        Assert.Contains(checks, fun check -> check.Message.Contains(".codex exists but is not referenced"))

    [<Then>]
    member _.``no catalog row is required for the absent binding directories``() =
        Assert.Contains(checks, fun check -> check.Message.Contains("absent on disk; no catalog row required"))

    [<Then>]
    member _.``the output names \.toml as the officially-correct extension``() =
        Assert.Contains(checks, fun check -> check.Message.Contains("must be <name>.toml"))

    [<Then>]
    member _.``the output names the orphaned mirror and the source that no longer exists``() =
        let check =
            checks
            |> List.find (fun check -> check.Name = "Mirror Orphans: .opencode/agents")

        Assert.Equal("failed", check.Status)
        Assert.Equal("orphaned mirror(s): repo-rules-maker.md", check.Actual)
        Assert.Contains("no .claude/agents/ source explains it", check.Message)
        Assert.DoesNotContain("README.md", check.Actual)

module private HarnessBindingScenarios =
    let acceptedName () =
        let steps = HarnessBindingsSteps()
        steps.``the repo-config\.yml harness registry declares codex`` ()
        steps.``the developer runs harness bindings generate for codex`` ()
        steps.``the harness name is not rejected as unknown`` ()

    let rejectedName () =
        let steps = HarnessBindingsSteps()
        steps.``the repo-config\.yml harness registry does not declare cursor`` ()
        steps.``the developer runs harness bindings generate for cursor`` ()
        steps.``the command exits with a failure code`` ()
        steps.``the error names the registry-derived accepted set`` ()

    let matchingRepository () =
        let steps = HarnessBindingsSteps()
        steps.``a repository whose generated binding files match the generated content`` ()
        steps.``the platform-bindings catalog references every present binding directory`` ()
        steps.``the developer runs harness bindings validate`` ()
        steps.``the command exits successfully`` ()
        steps.``the output reports all binding checks as passing`` ()

    let missingCatalogRow () =
        let steps = HarnessBindingsSteps()
        steps.``a repository with a known binding directory that the platform-bindings catalog does not reference`` ()
        steps.``the developer runs harness bindings validate`` ()
        steps.``the command exits with a failure code`` ()
        steps.``the output identifies the binding directory missing a catalog row`` ()

    let absentDirectory () =
        let steps = HarnessBindingsSteps()
        steps.``a repository where some known binding directories do not exist on disk`` ()
        steps.``the developer runs harness bindings validate`` ()
        steps.``the command exits successfully`` ()
        steps.``no catalog row is required for the absent binding directories`` ()

    let tomlAgent () =
        let steps = HarnessBindingsSteps()
        steps.``a repository whose \.codex/agents directory holds a standalone \.toml agent file`` ()
        steps.``the developer runs harness bindings validate`` ()
        steps.``the command exits successfully`` ()

    let orphanedMirror () =
        let steps = HarnessBindingsSteps()
        steps.``a repository whose generated agent directory holds a mirror with no source agent`` ()
        steps.``the developer runs harness bindings validate`` ()
        steps.``the command exits with a failure code`` ()
        steps.``the output names the orphaned mirror and the source that no longer exists`` ()

    let sourcedMirrors () =
        let steps = HarnessBindingsSteps()
        steps.``a repository whose generated agent mirrors each have a source agent`` ()
        steps.``the developer runs harness bindings validate`` ()
        steps.``the command exits successfully`` ()

    let markdownAgent () =
        let steps = HarnessBindingsSteps()
        steps.``a repository whose \.codex/agents directory holds a \.md agent file`` ()
        steps.``the developer runs harness bindings validate`` ()
        steps.``the command exits with a failure code`` ()
        steps.``the output names \.toml as the officially-correct extension`` ()

[<Fact>]
let ``registry accepts declared harness`` () = HarnessBindingScenarios.acceptedName ()

[<Fact>]
let ``registry rejects absent harness`` () = HarnessBindingScenarios.rejectedName ()

[<Fact>]
let ``matching generated repository passes`` () =
    HarnessBindingScenarios.matchingRepository ()

[<Fact>]
let ``missing catalog row fails`` () =
    HarnessBindingScenarios.missingCatalogRow ()

[<Fact>]
let ``absent binding directory needs no row`` () =
    HarnessBindingScenarios.absentDirectory ()

[<Fact>]
let ``toml Codex agent passes`` () = HarnessBindingScenarios.tomlAgent ()

[<Fact>]
let ``markdown Codex agent fails`` () =
    HarnessBindingScenarios.markdownAgent ()

[<Fact>]
let ``orphaned generated mirror fails`` () =
    HarnessBindingScenarios.orphanedMirror ()

[<Fact>]
let ``generated mirrors with sources pass`` () =
    HarnessBindingScenarios.sourcedMirrors ()
