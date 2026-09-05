module RhinoCli.Tests.Unit.Steps.HarnessPolicyCoverageTests

open Xunit
open RhinoCli.Application.HarnessPolicy

[<Fact>]
let ``Harness policy attributes every change combination`` () =
    Assert.Equal(NeitherChanged, attributeChanges false false)
    Assert.Equal(MirrorChanged, attributeChanges true false)
    Assert.Equal(CanonicalChanged, attributeChanges false true)
    Assert.Equal(BothChanged, attributeChanges true true)

[<Fact>]
let ``Harness request and catalog policy cover accepted absent drift and read failures`` () =
    Assert.Equal<Result<unit, string>>(Ok(), validateRequestedHarness [ "codex" ] "codex")
    Assert.True(Result.isError (validateRequestedHarness [ "codex"; "opencode" ] "cursor"))
    Assert.True(classifyCatalogPresence ".codex" false (Error "ignored") |> fst)
    Assert.False(classifyCatalogPresence ".codex" true (Error "read failed") |> fst)
    Assert.True(classifyCatalogPresence ".codex" true (Ok "row .codex") |> fst)
    Assert.False(classifyCatalogPresence ".codex" true (Ok "row .claude") |> fst)

[<Fact>]
let ``Harness binding policy covers matching missing drift and read failure`` () =
    Assert.True(classifyBindingContent "binding" "expected" (Ok(Some "expected")) |> fst)
    Assert.False(classifyBindingContent "binding" "expected" (Ok(Some "drift")) |> fst)
    Assert.False(classifyBindingContent "binding" "expected" (Ok None) |> fst)
    Assert.False(classifyBindingContent "binding" "expected" (Error "read failed") |> fst)

[<Fact>]
let ``Harness trigger and gate policy distinguish applicability pass and failure`` () =
    Assert.True(triggerMatches [ "repo-governance/rule.md" ] [ "repo-governance" ])
    Assert.True(triggerMatches [ "AGENTS.md" ] [ "AGENTS.md" ])
    Assert.False(triggerMatches [ "docs/guide.md" ] [ "repo-governance" ])
    Assert.Equal(NotApplicable, decideWordBudgetGate [ "docs/guide.md" ] [ "repo-governance" ] 1)
    Assert.Equal(Passed, decideWordBudgetGate [ "repo-governance/rule.md" ] [ "repo-governance" ] 0)
    Assert.Equal(Failed 2, decideWordBudgetGate [ "repo-governance/rule.md" ] [ "repo-governance" ] 2)

[<Fact>]
let ``Harness ownership policy chooses the longest declaration`` () =
    let declarations = [ ".agents", "generated"; ".agents/skills/vendor", "vendored" ]
    Assert.Equal(Some "vendored", classifyTrackedPath declarations ".agents/skills/vendor/SKILL.md")
    Assert.Equal(Some "generated", classifyTrackedPath declarations ".agents/skills/local/SKILL.md")
    Assert.Equal(None, classifyTrackedPath declarations ".claude/agents/demo.md")
