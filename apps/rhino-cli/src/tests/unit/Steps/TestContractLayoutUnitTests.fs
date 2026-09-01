/// Contract cases for the physical test-layout validator. Every case pins one
/// clause of
/// [Target Contract and Project Matrix](../../../../../../plans/in-progress/adopt-beavernest-test-automation/tech-docs/target-contract-and-project-matrix.md):
/// a parse rule, one fixture in the negative corpus, or the one positive
/// dedicated-E2E shape. The fixtures under `Fixtures/TestContract/Layout` are
/// copied beside the test assembly by `RhinoCli.UnitTests.fsproj`.
module RhinoCli.Tests.Unit.Steps.TestContractLayoutUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Application

let private fixtureFile (name: string) : string =
    Path.Combine(AppContext.BaseDirectory, "Fixtures", "TestContract", "Layout", name + ".json")

let private fixtureText (name: string) : string =
    let path = fixtureFile name
    Assert.True(File.Exists path, "missing fixture " + path)
    File.ReadAllText path

let private parsed (name: string) : TestContractLayout.LayoutDocument =
    match TestContractLayout.parseDocument (fixtureText name) with
    | Ok document -> document
    | Error(TestContract.Misuse message) -> failwith ("fixture " + name + " rejected as misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("fixture " + name + " rejected: " + message)

let private rejected (name: string) : string =
    match TestContractLayout.validateDocument (parsed name) with
    | Error(TestContract.ContractFailure message) -> message
    | Error(TestContract.Misuse message) ->
        failwith ("fixture " + name + " was misuse, not a contract failure: " + message)
    | Ok _ -> failwith ("fixture " + name + " passed; it must fail")

let private accepted (name: string) : TestContractLayout.LayoutReport =
    match TestContractLayout.validateDocument (parsed name) with
    | Ok report -> report
    | Error(TestContract.ContractFailure message) -> failwith ("fixture " + name + " failed: " + message)
    | Error(TestContract.Misuse message) -> failwith ("fixture " + name + " was misuse: " + message)

let private misused (text: string) : string =
    match TestContractLayout.parseDocument text with
    | Error(TestContract.Misuse message) -> message
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, got contract failure: " + message)
    | Ok _ -> failwith "expected the document to be rejected"

let private minimal (body: string) : string =
    "{\"schema\":\"" + TestContractLayout.SchemaVersion + "\"," + body + "}"

// ---------------------------------------------------------------------------
// Schema and identity
// ---------------------------------------------------------------------------

[<Fact>]
let ``a document that is not valid JSON is misuse`` () =
    Assert.Contains("not valid JSON", misused "{")

[<Fact>]
let ``a JSON array is not a layout document`` () =
    Assert.Contains("must be a JSON object", misused "[]")

[<Fact>]
let ``a foreign schema version is rejected by exact string`` () =
    let text = "{\"schema\":\"ose-test-contract-coverage-fixture/v1\"}"
    Assert.Contains(TestContractLayout.SchemaVersion, misused text)

[<Fact>]
let ``an unknown top-level key is rejected rather than ignored`` () =
    let text = minimal "\"nonsense\":1"
    Assert.Contains("unknown key nonsense", misused text)

[<Fact>]
let ``a blank project is rejected`` () =
    let text = minimal "\"case\":\"c\",\"project\":\"  \""
    Assert.Contains("\"project\" must not be blank", misused text)

[<Fact>]
let ``an absolute project root is rejected`` () =
    let text =
        minimal "\"case\":\"c\",\"project\":\"p\",\"owner\":\"o\",\"root\":\"/etc/widget\""

    Assert.Contains("must not be an absolute path", misused text)

[<Fact>]
let ``a traversal segment in the project root is rejected`` () =
    let text =
        minimal "\"case\":\"c\",\"project\":\"p\",\"owner\":\"o\",\"root\":\"apps/../etc\""

    Assert.Contains("must not contain a traversal segment", misused text)

[<Fact>]
let ``an unknown layer name is rejected`` () =
    let text =
        minimal "\"case\":\"c\",\"project\":\"p\",\"owner\":\"o\",\"root\":\"apps/p\",\"ownedLayers\":[\"smoke\"]"

    Assert.Contains("must be unit, integration, or e2e", misused text)

[<Fact>]
let ``an empty owned-layer list is rejected`` () =
    let text =
        minimal "\"case\":\"c\",\"project\":\"p\",\"owner\":\"o\",\"root\":\"apps/p\",\"ownedLayers\":[]"

    Assert.Contains("at least one layer", misused text)

[<Fact>]
let ``a repeated owned layer is rejected`` () =
    let text =
        minimal
            "\"case\":\"c\",\"project\":\"p\",\"owner\":\"o\",\"root\":\"apps/p\",\"ownedLayers\":[\"unit\",\"unit\"]"

    Assert.Contains("repeats unit", misused text)

// ---------------------------------------------------------------------------
// The negative corpus — one fixture per way the layout rule is broken
// ---------------------------------------------------------------------------

[<Fact>]
let ``an executable test in src is reported against its own path`` () =
    let message = rejected "executable-test-in-src"
    Assert.StartsWith("layout-test-in-forbidden-directory", message)
    Assert.Contains("item=apps/widget-app/src/widget/legacy.test.ts", message)
    Assert.Contains("directory=src", message)

[<Fact>]
let ``a generic test directory is reported`` () =
    let message = rejected "generic-test-directory"
    Assert.StartsWith("layout-test-in-forbidden-directory", message)
    Assert.Contains("directory=test", message)

[<Fact>]
let ``a dunder tests directory is reported`` () =
    let message = rejected "dunder-tests-directory"
    Assert.StartsWith("layout-test-in-forbidden-directory", message)
    Assert.Contains("directory=__tests__", message)

[<Fact>]
let ``an executable test under tests support is reported`` () =
    let message = rejected "executable-in-support"
    Assert.StartsWith("layout-test-in-forbidden-directory", message)
    Assert.Contains("directory=tests/support", message)

[<Fact>]
let ``a non-executable helper under tests support is allowed`` () =
    // The same fixture proves the rule is about executability, not location
    // alone: builders.ts sits beside the offending file and is not reported.
    Assert.DoesNotContain("builders.ts", rejected "executable-in-support")

[<Fact>]
let ``a test in a layer the project does not own is reported`` () =
    let message = rejected "layer-not-owned"
    Assert.StartsWith("layout-layer-not-owned", message)
    Assert.Contains("item=apps/widget-app/tests/integration/api.test.ts", message)
    Assert.Contains("owned=unit", message)

[<Fact>]
let ``a file two targets select is reported with both target names`` () =
    let message = rejected "file-selected-twice"
    Assert.StartsWith("layout-file-selected-twice", message)
    Assert.Contains("selectors=2", message)
    Assert.Contains("targets=test:unit,test:integration", message)

[<Fact>]
let ``an executable test no target selects is reported`` () =
    let message = rejected "file-unselected"
    Assert.StartsWith("layout-file-unselected", message)
    Assert.Contains("item=apps/widget-app/tests/unit/orphan.test.ts", message)

[<Fact>]
let ``an empty placeholder directory for an unowned layer is reported`` () =
    let message = rejected "placeholder-directory"
    Assert.StartsWith("layout-placeholder-directory", message)
    Assert.Contains("item=apps/widget-app/tests/e2e", message)

[<Fact>]
let ``an owned layer with no executable test is reported`` () =
    let message = rejected "owned-layer-empty"
    Assert.StartsWith("layout-owned-layer-empty", message)
    Assert.Contains("item=integration", message)

// ---------------------------------------------------------------------------
// The one positive
// ---------------------------------------------------------------------------

[<Fact>]
let ``a dedicated E2E project with no placeholders passes`` () =
    let report = accepted "e2e-only-project"
    Assert.Equal("widget-app-e2e", report.Project)
    Assert.Equal<TestContractLayout.Layer list>([ TestContractLayout.LayerE2e ], report.OwnedLayers)

[<Fact>]
let ``the positive report counts only executable files`` () =
    // The fixture ships one spec and one JSON fixture; only the spec counts.
    Assert.Equal(1, (accepted "e2e-only-project").ExecutableFiles)

[<Fact>]
let ``a tests fixtures directory is not a placeholder`` () =
    Assert.Contains("native-layout-valid", TestContractLayout.formatReport (accepted "e2e-only-project"))

[<Fact>]
let ``the success line names the project owner and layers`` () =
    let rendered = TestContractLayout.formatReport (accepted "e2e-only-project")
    Assert.Contains("project=widget-app-e2e", rendered)
    Assert.Contains("owner=widget-app", rendered)
    Assert.Contains("layers=e2e", rendered)
    Assert.Contains("executable=1", rendered)

// ---------------------------------------------------------------------------
// Fixture resolution
// ---------------------------------------------------------------------------

[<Fact>]
let ``an absolute fixture path is refused before any read`` () =
    match TestContractLayout.loadDocument "/repo" "/etc/passwd" with
    | Error(TestContract.Misuse message) -> Assert.Contains("must not be an absolute path", message)
    | _ -> failwith "an absolute fixture path must be refused"

[<Fact>]
let ``a traversal fixture path is refused before any read`` () =
    match TestContractLayout.loadDocument "/repo" "../secrets.json" with
    | Error(TestContract.Misuse message) -> Assert.Contains("must not contain a traversal segment", message)
    | _ -> failwith "a traversal fixture path must be refused"

[<Fact>]
let ``the fixture root is the layout corpus`` () =
    Assert.Equal("apps/rhino-cli/src/tests/unit/Fixtures/TestContract/Layout", TestContractLayout.FixtureRoot)

[<Fact>]
let ``every layer renders its contract name`` () =
    Assert.Equal("unit", TestContractLayout.layerName TestContractLayout.LayerUnit)
    Assert.Equal("integration", TestContractLayout.layerName TestContractLayout.LayerIntegration)
    Assert.Equal("e2e", TestContractLayout.layerName TestContractLayout.LayerE2e)

[<Fact>]
let ``an executable test outside the tests root is reported`` () =
    let message = rejected "test-outside-tests-root"
    Assert.StartsWith("layout-test-outside-tests-root", message)
    Assert.Contains("item=apps/widget-app/e2e/checkout.test.ts", message)
    Assert.Contains("expected=apps/widget-app/tests/*", message)
