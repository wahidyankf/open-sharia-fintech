/// Contract cases for the exact Gherkin/BDD adapter validator. Every case
/// pins one clause of
/// [Static Adapter Contract](../../../../../../plans/in-progress/adopt-beavernest-test-automation/tech-docs/gherkin-coverage-and-adapter-design.md):
/// a parse rule, one of the nine negative fixtures, or an exact
/// covered/total pair. The nine fixtures under `Fixtures/TestContract/Bdd`
/// are copied beside the test assembly by `RhinoCli.UnitTests.fsproj`.
module RhinoCli.Tests.Unit.Steps.TestContractBddUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Application

// ---------------------------------------------------------------------------
// Fixture access
// ---------------------------------------------------------------------------

let private fixtureFile (name: string) : string =
    Path.Combine(AppContext.BaseDirectory, "Fixtures", "TestContract", "Bdd", name + ".json")

let private fixtureText (name: string) : string =
    let path = fixtureFile name
    Assert.True(File.Exists path, "missing fixture " + path)
    File.ReadAllText path

let private parsed (name: string) : TestContractBdd.BddDocument =
    match TestContractBdd.parseDocument (fixtureText name) with
    | Ok document -> document
    | Error(TestContract.Misuse message) -> failwith ("fixture " + name + " rejected as misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("fixture " + name + " rejected: " + message)

/// Validates a fixture that must fail, returning the joined diagnostic text.
let private rejected (name: string) : string =
    match TestContractBdd.validateDocument (parsed name) with
    | Error(TestContract.ContractFailure message) -> message
    | Error(TestContract.Misuse message) ->
        failwith ("fixture " + name + " was misuse, not a contract failure: " + message)
    | Ok _ -> failwith ("fixture " + name + " passed; it must fail")

// ---------------------------------------------------------------------------
// Inline document construction
// ---------------------------------------------------------------------------

let private checkoutFeature =
    "specs/apps/widget/behavior/widget-app/gherkin/checkout.feature"

let private searchFeature =
    "specs/apps/widget/behavior/widget-app/gherkin/search.feature"

let private checkoutScenario = "Checkout succeeds"
let private searchScenario = "Search returns a match"

let private checkoutSteps =
    [ "Given a cart with one item"; "When I check out"; "Then I see a receipt" ]

let private searchSteps =
    [ "Given an indexed catalog"
      "When I search for a widget"
      "Then I see the widget" ]

let private unitDriver = "apps/widget-app/src/testing/bdd/unit-driver.ts"

let private quoted (values: string list) : string =
    values |> List.map (fun value -> sprintf "\"%s\"" value) |> String.concat ","

let private scenarioJson (name: string) (examples: int) (steps: string list) : string =
    sprintf "{\"name\":\"%s\",\"examples\":%d,\"steps\":[%s]}" name examples (quoted steps)

let private featureJson (path: string) (scenarios: string list) : string =
    sprintf "{\"path\":\"%s\",\"scenarios\":[%s]}" path (String.concat "," scenarios)

let private bindingKey (path: string) (scenario: string) (example: int) (step: string) : string =
    sprintf "%s|%s|%d|%s" path scenario example step

let private explicitBody (features: string list) (bindings: string list) : string =
    sprintf "\"corpus\":[%s],\"bindings\":[%s]" (String.concat "," features) (quoted bindings)

/// Builds a whole fixture document. `head` carries the identity fields so a
/// case can mutate exactly one of them.
let private documentJson (head: string) (body: string) : string =
    sprintf "{\"schema\":\"%s\",%s,%s}" TestContractBdd.SchemaVersion head body

let private requiredUnitHead =
    sprintf
        "\"case\":\"inline\",\"project\":\"widget-app\",\"owner\":\"widget-app\",\"adapter\":\"unit\",\"disposition\":\"required\",\"driver\":\"%s\""
        unitDriver

let private checkoutKeys =
    checkoutSteps |> List.map (bindingKey checkoutFeature checkoutScenario 1)

let private searchKeys =
    searchSteps |> List.map (bindingKey searchFeature searchScenario 1)

let private oneFeatureBody =
    explicitBody [ featureJson checkoutFeature [ scenarioJson checkoutScenario 1 checkoutSteps ] ] checkoutKeys

let private boundDocument = documentJson requiredUnitHead oneFeatureBody

let private misuse (text: string) : string =
    match TestContractBdd.parseDocument text with
    | Error(TestContract.Misuse message) -> message
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, got a contract failure: " + message)
    | Ok _ -> failwith "expected misuse, but the document parsed"

let private validated (text: string) : TestContractBdd.BddReport =
    match TestContractBdd.parseDocument text with
    | Error(TestContract.Misuse message) -> failwith ("document rejected as misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("document rejected: " + message)
    | Ok document ->
        match TestContractBdd.validateDocument document with
        | Ok report -> report
        | Error(TestContract.Misuse message) -> failwith ("validation misuse: " + message)
        | Error(TestContract.ContractFailure message) -> failwith ("validation failed: " + message)

// ---------------------------------------------------------------------------
// Schema and identity parsing
// ---------------------------------------------------------------------------

[<Fact>]
let ``the fixture schema string is exact`` () =
    Assert.Equal("ose-test-contract-bdd-fixture/v1", TestContractBdd.SchemaVersion)

[<Fact>]
let ``the fixture root is the unit-test fixture directory`` () =
    Assert.Equal("apps/rhino-cli/src/tests/unit/Fixtures/TestContract/Bdd", TestContractBdd.FixtureRoot)

[<Fact>]
let ``a document with another schema is misuse`` () =
    let text =
        boundDocument.Replace(TestContractBdd.SchemaVersion, "ose-test-contract-bdd-fixture/v2")

    Assert.Contains("ose-test-contract-bdd-fixture/v2", misuse text)

[<Fact>]
let ``an unknown top-level key is misuse`` () =
    let text = documentJson requiredUnitHead (oneFeatureBody + ",\"extra\":true")
    Assert.Contains("extra", misuse text)

[<Fact>]
let ``a missing case field is misuse`` () =
    let head = requiredUnitHead.Replace("\"case\":\"inline\",", "")
    Assert.Contains("case", misuse (documentJson head oneFeatureBody))

[<Fact>]
let ``a blank project is misuse`` () =
    let head =
        requiredUnitHead.Replace("\"project\":\"widget-app\"", "\"project\":\"  \"")

    Assert.Contains("project", misuse (documentJson head oneFeatureBody))

[<Fact>]
let ``a blank owner is misuse`` () =
    let head = requiredUnitHead.Replace("\"owner\":\"widget-app\"", "\"owner\":\"\"")
    Assert.Contains("owner", misuse (documentJson head oneFeatureBody))

[<Fact>]
let ``an unknown adapter level is misuse`` () =
    let head =
        requiredUnitHead.Replace("\"adapter\":\"unit\"", "\"adapter\":\"contract\"")

    Assert.Contains("contract", misuse (documentJson head oneFeatureBody))

[<Fact>]
let ``an unknown disposition is misuse`` () =
    let head =
        requiredUnitHead.Replace("\"disposition\":\"required\"", "\"disposition\":\"optional\"")

    Assert.Contains("optional", misuse (documentJson head oneFeatureBody))

[<Fact>]
let ``the three adapter levels parse`` () =
    let levels =
        [ "unit", TestContractBdd.AdapterUnit
          "integration", TestContractBdd.AdapterIntegration
          "e2e", TestContractBdd.AdapterE2e ]

    for name, expected in levels do
        let head =
            requiredUnitHead.Replace("\"adapter\":\"unit\"", sprintf "\"adapter\":\"%s\"" name)

        Assert.Equal(expected, (validated (documentJson head oneFeatureBody)).Adapter)

[<Fact>]
let ``adapter names round-trip`` () =
    Assert.Equal("unit", TestContractBdd.adapterName TestContractBdd.AdapterUnit)
    Assert.Equal("integration", TestContractBdd.adapterName TestContractBdd.AdapterIntegration)
    Assert.Equal("e2e", TestContractBdd.adapterName TestContractBdd.AdapterE2e)

[<Fact>]
let ``disposition names round-trip`` () =
    Assert.Equal("required", TestContractBdd.dispositionName TestContractBdd.BddRequired)
    Assert.Equal("delegated", TestContractBdd.dispositionName TestContractBdd.BddDelegated)
    Assert.Equal("inapplicable", TestContractBdd.dispositionName TestContractBdd.BddInapplicable)

// ---------------------------------------------------------------------------
// Conditional field parsing
// ---------------------------------------------------------------------------

[<Fact>]
let ``a required adapter carrying a reason is misuse`` () =
    let body = oneFeatureBody + ",\"reason\":\"no boundary\""
    Assert.Contains("reason", misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``an inapplicable adapter carrying a driver is misuse`` () =
    let head =
        requiredUnitHead.Replace("\"disposition\":\"required\"", "\"disposition\":\"inapplicable\"")

    let body = oneFeatureBody + ",\"reason\":\"no isolated local-resource boundary\""
    Assert.Contains("driver", misuse (documentJson head body))

[<Fact>]
let ``an inapplicable adapter without a reason is misuse`` () =
    let head =
        requiredUnitHead
            .Replace("\"disposition\":\"required\"", "\"disposition\":\"inapplicable\"")
            .Replace(sprintf ",\"driver\":\"%s\"" unitDriver, ",\"driver\":null")

    Assert.Contains("reason", misuse (documentJson head oneFeatureBody))

[<Fact>]
let ``a delegated adapter without a driver is an uncovered owner-adapter pair`` () =
    let head =
        requiredUnitHead
            .Replace("\"disposition\":\"required\"", "\"disposition\":\"delegated\"")
            .Replace(sprintf ",\"driver\":\"%s\"" unitDriver, ",\"driver\":null")

    match TestContractBdd.parseDocument (documentJson head oneFeatureBody) with
    | Ok document ->
        match TestContractBdd.validateDocument document with
        | Error(TestContract.ContractFailure message) ->
            Assert.Contains("bdd-uncovered-owner-adapter", message)
            Assert.Contains("pairs=0/1", message)
        | other -> failwith (sprintf "expected an uncovered owner-adapter pair, got %A" other)
    | other -> failwith (sprintf "expected the document to parse, got %A" other)

[<Fact>]
let ``a document declaring neither corpus nor synthetic is misuse`` () =
    Assert.Contains("corpus", misuse (documentJson requiredUnitHead "\"bindings\":[]"))

[<Fact>]
let ``a document declaring both corpus and synthetic is misuse`` () =
    let body =
        oneFeatureBody
        + sprintf ",\"synthetic\":{\"path\":\"%s\",\"scenarios\":2,\"bound\":1}" checkoutFeature

    Assert.Contains("synthetic", misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``an empty corpus is misuse`` () =
    Assert.Contains("corpus", misuse (documentJson requiredUnitHead (explicitBody [] [])))

[<Fact>]
let ``a feature without scenarios is misuse`` () =
    let body = explicitBody [ featureJson checkoutFeature [] ] []
    Assert.Contains("scenarios", misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``a duplicate feature path is misuse`` () =
    let feature =
        featureJson checkoutFeature [ scenarioJson checkoutScenario 1 checkoutSteps ]

    let body = explicitBody [ feature; feature ] checkoutKeys
    Assert.Contains(checkoutFeature, misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``a duplicate scenario name inside one feature is misuse`` () =
    let scenario = scenarioJson checkoutScenario 1 checkoutSteps

    let body =
        explicitBody [ featureJson checkoutFeature [ scenario; scenario ] ] checkoutKeys

    Assert.Contains(checkoutScenario, misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``a zero example count is misuse`` () =
    let body =
        explicitBody [ featureJson checkoutFeature [ scenarioJson checkoutScenario 0 checkoutSteps ] ] []

    Assert.Contains("examples", misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``a scenario without steps is misuse`` () =
    let body =
        explicitBody [ featureJson checkoutFeature [ scenarioJson checkoutScenario 1 [] ] ] []

    Assert.Contains("steps", misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``an absolute feature path is misuse`` () =
    let body =
        explicitBody [ featureJson "/tmp/checkout.feature" [ scenarioJson checkoutScenario 1 checkoutSteps ] ] []

    Assert.Contains("/tmp/checkout.feature", misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``a traversal feature path is misuse`` () =
    let body =
        explicitBody [ featureJson "specs/../checkout.feature" [ scenarioJson checkoutScenario 1 checkoutSteps ] ] []

    Assert.Contains("specs/../checkout.feature", misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``a binding without four fields is misuse`` () =
    let body =
        explicitBody
            [ featureJson checkoutFeature [ scenarioJson checkoutScenario 1 checkoutSteps ] ]
            [ "checkout.feature|Checkout succeeds" ]

    Assert.Contains("checkout.feature|Checkout succeeds", misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``a blank binding is misuse`` () =
    let body =
        explicitBody [ featureJson checkoutFeature [ scenarioJson checkoutScenario 1 checkoutSteps ] ] [ "   " ]

    Assert.Contains("binding", misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``a synthetic corpus with more bound than declared scenarios is misuse`` () =
    let body =
        sprintf "\"synthetic\":{\"path\":\"%s\",\"scenarios\":5,\"bound\":6}" checkoutFeature

    Assert.Contains("bound", misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``a synthetic corpus with no scenarios is misuse`` () =
    let body =
        sprintf "\"synthetic\":{\"path\":\"%s\",\"scenarios\":0,\"bound\":0}" checkoutFeature

    Assert.Contains("scenarios", misuse (documentJson requiredUnitHead body))

[<Fact>]
let ``malformed JSON is misuse`` () =
    Assert.Contains("JSON", misuse "{\"schema\":")

// ---------------------------------------------------------------------------
// Fixture resolution
// ---------------------------------------------------------------------------

[<Fact>]
let ``an absolute fixture path is misuse`` () =
    match TestContractBdd.loadDocument "/repo" "/etc/passwd" with
    | Error(TestContract.Misuse message) -> Assert.Contains("/etc/passwd", message)
    | other -> failwith (sprintf "expected misuse, got %A" other)

[<Fact>]
let ``a traversal fixture path is misuse`` () =
    match TestContractBdd.loadDocument "/repo" (TestContractBdd.FixtureRoot + "/../escape.json") with
    | Error(TestContract.Misuse message) -> Assert.Contains("..", message)
    | other -> failwith (sprintf "expected misuse, got %A" other)

[<Fact>]
let ``a fixture outside the BDD fixture root is misuse`` () =
    match
        TestContractBdd.loadDocument "/repo" "apps/rhino-cli/src/tests/unit/Fixtures/TestContract/Layout/src-root.json"
    with
    | Error(TestContract.Misuse message) -> Assert.Contains(TestContractBdd.FixtureRoot, message)
    | other -> failwith (sprintf "expected misuse, got %A" other)

[<Fact>]
let ``a missing fixture file is misuse`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-cli-bdd-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory root |> ignore

    match TestContractBdd.loadDocument root (TestContractBdd.FixtureRoot + "/absent.json") with
    | Error(TestContract.Misuse message) -> Assert.Contains("absent.json", message)
    | other -> failwith (sprintf "expected misuse, got %A" other)

[<Fact>]
let ``a resolved fixture parses through loadDocument`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-cli-bdd-" + Guid.NewGuid().ToString("N"))

    let directory = Path.Combine(root, TestContractBdd.FixtureRoot)
    Directory.CreateDirectory directory |> ignore
    File.WriteAllText(Path.Combine(directory, "missing-binding.json"), fixtureText "missing-binding")

    match TestContractBdd.loadDocument root (TestContractBdd.FixtureRoot + "/missing-binding.json") with
    | Ok document -> Assert.Equal("missing-binding", document.Case)
    | other -> failwith (sprintf "expected a parsed document, got %A" other)

// ---------------------------------------------------------------------------
// Every negative fixture parses
// ---------------------------------------------------------------------------

[<Fact>]
let ``every negative fixture parses and declares its own case`` () =
    let names =
        [ "duplicate-binding"
          "missing-binding"
          "missing-example"
          "missing-feature"
          "missing-owner-adapter"
          "missing-scenario"
          "missing-step"
          "rounded-999-of-1000"
          "unused-binding" ]

    for name in names do
        Assert.Equal(name, (parsed name).Case)

[<Fact>]
let ``every negative fixture names the widget-app owner and the unit adapter`` () =
    let document = parsed "missing-binding"
    Assert.Equal("widget-app", document.Project)
    Assert.Equal("widget-app", document.Owner)
    Assert.Equal(TestContractBdd.AdapterUnit, document.Adapter)

// ---------------------------------------------------------------------------
// The nine negative fixtures
// ---------------------------------------------------------------------------

[<Fact>]
let ``an unbound feature is reported with its exact file counts`` () =
    let message = rejected "missing-feature"
    Assert.Contains("bdd-uncovered-feature", message)
    Assert.Contains("item=" + searchFeature, message)
    Assert.Contains("files=1/2", message)

[<Fact>]
let ``an unbound scenario is reported with its exact scenario counts`` () =
    let message = rejected "missing-scenario"
    Assert.Contains("bdd-uncovered-scenario", message)
    Assert.Contains("scenarios=1/2", message)

[<Fact>]
let ``an unbound outline example is reported with its exact example counts`` () =
    let message = rejected "missing-example"
    Assert.Contains("bdd-uncovered-example", message)
    Assert.Contains("examples=1/2", message)

[<Fact>]
let ``a scenario without an explicit When is reported`` () =
    let message = rejected "missing-step"
    Assert.Contains("bdd-missing-required-keyword", message)
    Assert.Contains("keyword=When", message)

[<Fact>]
let ``an unbound step is reported as an undefined binding with zero candidates`` () =
    let message = rejected "missing-binding"
    Assert.Contains("bdd-undefined-binding", message)
    Assert.Contains("candidates=0", message)
    Assert.Contains("steps=2/3", message)

[<Fact>]
let ``a required adapter without a driver is reported as an uncovered owner-adapter pair`` () =
    let message = rejected "missing-owner-adapter"
    Assert.Contains("bdd-uncovered-owner-adapter", message)
    Assert.Contains("item=widget-app@unit", message)
    Assert.Contains("pairs=0/1", message)

[<Fact>]
let ``a binding matching no enumerated step is reported as unused`` () =
    let message = rejected "unused-binding"
    Assert.Contains("bdd-unused-binding", message)
    Assert.Contains("Then I see a coupon", message)

[<Fact>]
let ``a repeated binding is reported as ambiguous with its candidate count`` () =
    let message = rejected "duplicate-binding"
    Assert.Contains("bdd-ambiguous-binding", message)
    Assert.Contains("candidates=2", message)

[<Fact>]
let ``a 999 of 1000 corpus fails on integers rather than a rounded percentage`` () =
    let message = rejected "rounded-999-of-1000"
    Assert.Contains("scenarios=999/1000", message)
    Assert.DoesNotContain("100%", message)
    Assert.DoesNotContain("100.0", message)

// ---------------------------------------------------------------------------
// Every failure names owner, adapter, item, covered, and total
// ---------------------------------------------------------------------------

[<Fact>]
let ``every negative fixture names owner adapter item covered and total`` () =
    let names =
        [ "duplicate-binding"
          "missing-binding"
          "missing-example"
          "missing-feature"
          "missing-owner-adapter"
          "missing-scenario"
          "missing-step"
          "rounded-999-of-1000"
          "unused-binding" ]

    for name in names do
        let message = rejected name
        Assert.Contains("project=widget-app", message)
        Assert.Contains("owner=widget-app", message)
        Assert.Contains("adapter=unit", message)
        Assert.Contains("item=", message)
        Assert.Contains("covered=", message)
        Assert.Contains("total=", message)
        Assert.Contains("remediation=", message)

[<Fact>]
let ``every negative fixture ends with the five-category summary line`` () =
    let names =
        [ "duplicate-binding"
          "missing-binding"
          "missing-example"
          "missing-feature"
          "missing-owner-adapter"
          "missing-scenario"
          "missing-step"
          "rounded-999-of-1000"
          "unused-binding" ]

    for name in names do
        let message = rejected name
        Assert.Contains("behavior-coverage-failed", message)
        Assert.Contains("files=", message)
        Assert.Contains("examples=", message)
        Assert.Contains("scenarios=", message)
        Assert.Contains("steps=", message)
        Assert.Contains("pairs=", message)

// ---------------------------------------------------------------------------
// Exact positives
// ---------------------------------------------------------------------------

[<Fact>]
let ``a fully bound single-feature corpus is exactly equal in all five categories`` () =
    let report = validated boundDocument
    Assert.Equal(report.Total, report.Covered)
    Assert.Equal(1, report.Total.Files)
    Assert.Equal(1, report.Total.Examples)
    Assert.Equal(1, report.Total.Scenarios)
    Assert.Equal(3, report.Total.Steps)
    Assert.Equal(1, report.Total.Pairs)

[<Fact>]
let ``a fully bound two-feature corpus counts both files`` () =
    let body =
        explicitBody
            [ featureJson checkoutFeature [ scenarioJson checkoutScenario 1 checkoutSteps ]
              featureJson searchFeature [ scenarioJson searchScenario 1 searchSteps ] ]
            (checkoutKeys @ searchKeys)

    let report = validated (documentJson requiredUnitHead body)
    Assert.Equal(report.Total, report.Covered)
    Assert.Equal(2, report.Total.Files)
    Assert.Equal(6, report.Total.Steps)

[<Fact>]
let ``a fully bound scenario outline counts every expanded example`` () =
    let keys =
        [ for example in 1..3 do
              for step in checkoutSteps -> bindingKey checkoutFeature checkoutScenario example step ]

    let body =
        explicitBody [ featureJson checkoutFeature [ scenarioJson checkoutScenario 3 checkoutSteps ] ] keys

    let report = validated (documentJson requiredUnitHead body)
    Assert.Equal(report.Total, report.Covered)
    Assert.Equal(1, report.Total.Scenarios)
    Assert.Equal(3, report.Total.Examples)
    Assert.Equal(9, report.Total.Steps)

[<Fact>]
let ``a fully bound delegated adapter is valid`` () =
    let head =
        requiredUnitHead.Replace("\"disposition\":\"required\"", "\"disposition\":\"delegated\"")

    let report = validated (documentJson head oneFeatureBody)
    Assert.Equal(TestContractBdd.BddDelegated, report.Disposition)
    Assert.Equal(report.Total, report.Covered)
    Assert.Equal(1, report.Total.Pairs)

[<Fact>]
let ``an inapplicable adapter builds no denominator`` () =
    let head =
        requiredUnitHead
            .Replace("\"disposition\":\"required\"", "\"disposition\":\"inapplicable\"")
            .Replace(sprintf ",\"driver\":\"%s\"" unitDriver, ",\"driver\":null")

    let body = oneFeatureBody + ",\"reason\":\"no isolated local-resource boundary\""
    let report = validated (documentJson head body)
    Assert.Equal(TestContractBdd.BddInapplicable, report.Disposition)
    Assert.Equal(0, report.Total.Pairs)
    Assert.Equal(0, report.Total.Steps)

[<Fact>]
let ``a synthetic corpus with every scenario bound is valid`` () =
    let body =
        sprintf "\"synthetic\":{\"path\":\"%s\",\"scenarios\":1000,\"bound\":1000}" checkoutFeature

    let report = validated (documentJson requiredUnitHead body)
    Assert.Equal(report.Total, report.Covered)
    Assert.Equal(1000, report.Total.Scenarios)

// ---------------------------------------------------------------------------
// Report rendering
// ---------------------------------------------------------------------------

[<Fact>]
let ``the success line names the project owner adapter disposition and five pairs`` () =
    let report = validated boundDocument

    Assert.Equal(
        "behavior-coverage-valid project=widget-app owner=widget-app adapter=unit disposition=required files=1/1 examples=1/1 scenarios=1/1 steps=3/3 pairs=1/1",
        TestContractBdd.formatReport report
    )

[<Fact>]
let ``an inapplicable adapter renders the governed not-applicable line`` () =
    let head =
        requiredUnitHead
            .Replace("\"disposition\":\"required\"", "\"disposition\":\"inapplicable\"")
            .Replace(sprintf ",\"driver\":\"%s\"" unitDriver, ",\"driver\":null")

    let body = oneFeatureBody + ",\"reason\":\"no isolated local-resource boundary\""
    let report = validated (documentJson head body)

    Assert.Equal(
        "behavior-coverage-not-applicable project=widget-app owner=widget-app adapter=unit reason=no isolated local-resource boundary",
        TestContractBdd.formatReport report
    )

[<Fact>]
let ``the success line never renders a percentage`` () =
    let text = TestContractBdd.formatReport (validated boundDocument)
    Assert.DoesNotContain("%", text)
