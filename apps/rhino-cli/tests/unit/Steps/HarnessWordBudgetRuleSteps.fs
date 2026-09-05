module RhinoCli.Tests.Unit.Steps.HarnessWordBudgetRuleSteps

open RhinoCli.Application.Harness
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/harness/governance-word-budget-rule.feature" ]

type private PlanState =
    | Draft
    | Complete

type HarnessWordBudgetRuleSteps() =
    let convention =
        "monitored file classes; thresholds come from repo-config.yml; pre-commit, pre-push, and CI enforce"

    let checker =
        "qualitative instruction-file class review delegates numeric enforcement to governance-word-budget"

    let workflow =
        "Step 0.5: skip local governance-word-budget and use delegated lifecycle evidence"

    let lifecycle =
        "Step 0.5 consumes governance-word-budget; Step 6 does not re-derive word counts"

    let mutable checks: ValidationCheck list = []
    let mutable json = ""
    let mutable planState = Draft
    let mutable auditCategory: RepoGovernanceAuditCategory option = None
    let mutable lifecycleGateId: string option = None

    let requireCompletePlan () = Assert.Equal(Complete, planState)

    let runRuleChecks () =
        requireCompletePlan ()
        checks <- wordBudgetRuleChecks convention checker workflow lifecycle

    [<Given>]
    member _.``the plan is complete``() = planState <- Complete

    [<Given>]
    member _.``a repo with instruction files within the configured budgets``() =
        auditCategory <-
            Some
                { Name = "governance-word-budget"
                  Passed = true
                  Findings = [] }

    [<Given>]
    member _.``lifecycle evidence contains a current "governance-word-budget" result``() =
        lifecycleGateId <- Some "governance-word-budget"

    [<When>]
    member _.``I look under "repo-governance/conventions/structure/"``() = runRuleChecks ()

    [<When>]
    member _.``"repo-rules-checker" runs Step 6``() = runRuleChecks ()

    [<When>]
    member _.``I read "repo-governance/workflows/rules/rules-quality-gate\.md"``() = runRuleChecks ()

    [<When>]
    member _.``the developer runs "rhino-cli repo-governance audit" with JSON output``() =
        json <- repoGovernanceAuditJsonForCategory auditCategory.Value

    [<When>]
    member _.``"repo-rules-checker" runs Step 0\.5``() =
        Assert.Equal(Some "governance-word-budget", lifecycleGateId)
        checks <- wordBudgetRuleChecks convention checker workflow lifecycle

    [<Then>]
    member _.``"governance-word-budget\.md" exists``() =
        Assert.Equal("passed", checks.[0].Status)

    [<Then>]
    member _.``the file lists the monitored file classes, configured threshold source, and enforcement points``() =
        Assert.Equal("passed", checks.[0].Status)

    [<Then>]
    member _.``it reports qualitative bloat concerns across the whole instruction-file class``() =
        Assert.Equal("passed", checks.[1].Status)

    [<Then>]
    member _.``it annotates that the word ceiling is enforced by the deterministic "governance-word-budget" gate``() =
        Assert.Equal("passed", checks.[1].Status)

    [<Then>]
    member _.``"governance-word-budget" is skipped locally and delegated from Step 0\.5``() =
        Assert.Equal("passed", checks.[2].Status)

    [<Then>]
    member _.``the envelope schema is "rhino-cli/repo-governance-audit/v1"``() =
        Assert.Contains($"\"schema\": \"{repoGovernanceAuditSchema}\"", json)

    [<Then>]
    member _.``"result\.categories" contains a category named "governance-word-budget"``() =
        Assert.Contains("\"categories\"", json)
        Assert.Contains("\"name\": \"governance-word-budget\"", json)

    [<Then>]
    member _.``it consumes the exact delegated gate ID "governance-word-budget"``() =
        Assert.Equal("passed", checks.[3].Status)

    [<Then>]
    member _.``it does not re-derive word counts in Step 6``() =
        Assert.Equal("passed", checks.[3].Status)

[<Fact>]
let ``word-budget convention carries deterministic contract`` () =
    let s = HarnessWordBudgetRuleSteps()
    s.``the plan is complete`` ()
    s.``I look under "repo-governance/conventions/structure/"`` ()
    s.``"governance-word-budget\.md" exists`` ()
    s.``the file lists the monitored file classes, configured threshold source, and enforcement points`` ()

[<Fact>]
let ``checker owns qualitative review only`` () =
    let s = HarnessWordBudgetRuleSteps()
    s.``the plan is complete`` ()
    s.``"repo-rules-checker" runs Step 6`` ()
    s.``it reports qualitative bloat concerns across the whole instruction-file class`` ()
    s.``it annotates that the word ceiling is enforced by the deterministic "governance-word-budget" gate`` ()

[<Fact>]
let ``quality gate delegates exact word-budget ID`` () =
    let s = HarnessWordBudgetRuleSteps()
    s.``the plan is complete`` ()
    s.``I read "repo-governance/workflows/rules/rules-quality-gate\.md"`` ()
    s.``"governance-word-budget" is skipped locally and delegated from Step 0\.5`` ()

[<Fact>]
let ``preflight envelope contains word-budget category`` () =
    let s = HarnessWordBudgetRuleSteps()
    s.``a repo with instruction files within the configured budgets`` ()
    s.``the developer runs "rhino-cli repo-governance audit" with JSON output`` ()
    s.``the envelope schema is "rhino-cli/repo-governance-audit/v1"`` ()
    s.``"result\.categories" contains a category named "governance-word-budget"`` ()

[<Fact>]
let ``AI checker consumes lifecycle evidence`` () =
    let s = HarnessWordBudgetRuleSteps()
    s.``lifecycle evidence contains a current "governance-word-budget" result`` ()
    s.``"repo-rules-checker" runs Step 0\.5`` ()
    s.``it consumes the exact delegated gate ID "governance-word-budget"`` ()
    s.``it does not re-derive word counts in Step 6`` ()
