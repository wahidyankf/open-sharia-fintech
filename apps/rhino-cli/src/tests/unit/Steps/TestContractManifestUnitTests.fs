/// Contract cases for the project-local `package.json` policy. Every case pins
/// one clause of
/// [Target Contract and Project Matrix](../../../../../../plans/in-progress/adopt-beavernest-test-automation/tech-docs/target-contract-and-project-matrix.md):
/// a parse rule, one fixture in the negative corpus, or one of the two
/// legitimate dispositions. The fixtures under `Fixtures/TestContract/Manifest`
/// are copied beside the test assembly by `RhinoCli.UnitTests.fsproj`.
module RhinoCli.Tests.Unit.Steps.TestContractManifestUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Application

let private fixtureFile (name: string) : string =
    Path.Combine(AppContext.BaseDirectory, "Fixtures", "TestContract", "Manifest", name + ".json")

let private fixtureText (name: string) : string =
    let path = fixtureFile name
    Assert.True(File.Exists path, "missing fixture " + path)
    File.ReadAllText path

let private parsed (name: string) : TestContractManifest.ManifestDocument =
    match TestContractManifest.parseDocument (fixtureText name) with
    | Ok document -> document
    | Error(TestContract.Misuse message) -> failwith ("fixture " + name + " rejected as misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("fixture " + name + " rejected: " + message)

let private rejected (name: string) : string =
    match TestContractManifest.validateDocument (parsed name) with
    | Error(TestContract.ContractFailure message) -> message
    | Error(TestContract.Misuse message) ->
        failwith ("fixture " + name + " was misuse, not a contract failure: " + message)
    | Ok _ -> failwith ("fixture " + name + " passed; it must fail")

let private accepted (name: string) : TestContractManifest.ManifestReport =
    match TestContractManifest.validateDocument (parsed name) with
    | Ok report -> report
    | Error(TestContract.ContractFailure message) -> failwith ("fixture " + name + " failed: " + message)
    | Error(TestContract.Misuse message) -> failwith ("fixture " + name + " was misuse: " + message)

let private misused (text: string) : string =
    match TestContractManifest.parseDocument text with
    | Error(TestContract.Misuse message) -> message
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, got contract failure: " + message)
    | Ok _ -> failwith "expected the document to be rejected"

let private minimal (body: string) : string =
    "{\"schema\":\"" + TestContractManifest.SchemaVersion + "\"," + body + "}"

// ---------------------------------------------------------------------------
// Schema and identity
// ---------------------------------------------------------------------------

[<Fact>]
let ``a document that is not valid JSON is misuse`` () =
    Assert.Contains("not valid JSON", misused "{")

[<Fact>]
let ``a JSON array is not a manifest document`` () =
    Assert.Contains("must be a JSON object", misused "[]")

[<Fact>]
let ``a foreign schema version is rejected by exact string`` () =
    Assert.Contains(TestContractManifest.SchemaVersion, misused "{\"schema\":\"ose-test-contract-layout-fixture/v1\"}")

[<Fact>]
let ``an unknown top-level key is rejected rather than ignored`` () =
    Assert.Contains("unknown key nonsense", misused (minimal "\"nonsense\":1"))

[<Fact>]
let ``a project outside the three inventoried groups is unclassified`` () =
    let text =
        minimal "\"case\":\"c\",\"project\":\"p\",\"owner\":\"o\",\"group\":\"cli-tool\""

    Assert.Contains("must be web-application, dedicated-e2e, or typescript-library", misused text)

[<Fact>]
let ``a disposition outside retained and removed is rejected`` () =
    let text =
        minimal
            "\"case\":\"c\",\"project\":\"p\",\"owner\":\"o\",\"group\":\"web-application\",\"disposition\":\"deferred\""

    Assert.Contains("must be retained or removed", misused text)

[<Fact>]
let ``an absolute manifest path is rejected`` () =
    let text =
        minimal
            "\"case\":\"c\",\"project\":\"p\",\"owner\":\"o\",\"group\":\"web-application\",\"disposition\":\"retained\",\"manifestPath\":\"/etc/package.json\""

    Assert.Contains("must not be an absolute path", misused text)

[<Fact>]
let ``a repeated script name is rejected`` () =
    let text =
        minimal (
            "\"case\":\"c\",\"project\":\"p\",\"owner\":\"o\",\"group\":\"web-application\","
            + "\"disposition\":\"retained\",\"manifestPath\":\"apps/p/package.json\",\"consumer\":\"c\","
            + "\"requiredFields\":[\"name\"],\"verification\":\"v\","
            + "\"scripts\":[{\"name\":\"test\",\"command\":\"a\"},{\"name\":\"test\",\"command\":\"b\"}],"
            + "\"commands\":[]"
        )

    Assert.Contains("repeats test", misused text)

// ---------------------------------------------------------------------------
// The negative corpus
// ---------------------------------------------------------------------------

[<Fact>]
let ``a retained manifest without a consumer is reported`` () =
    let message = rejected "retained-without-consumer"
    Assert.StartsWith("manifest-retained-without-consumer", message)
    Assert.Contains("consumer=null", message)

[<Fact>]
let ``Nx project discovery is not a valid consumer`` () =
    let message = rejected "invalid-consumer-nx-discovery"
    Assert.StartsWith("manifest-invalid-consumer", message)
    Assert.Contains("consumer=Nx project discovery", message)

[<Fact>]
let ``an invalid consumer is matched regardless of casing`` () =
    let message = rejected "invalid-consumer-npm-script"
    Assert.StartsWith("manifest-invalid-consumer", message)
    Assert.Contains("Convenient NPM Script", message)

[<Fact>]
let ``a retained manifest with no verification command is reported`` () =
    Assert.StartsWith("manifest-missing-verification", rejected "missing-verification")

[<Fact>]
let ``a retained manifest naming no required field is reported`` () =
    let message = rejected "missing-required-fields"
    Assert.StartsWith("manifest-missing-required-fields", message)
    Assert.Contains("requiredFields=0", message)

[<Fact>]
let ``a script that only forwards to its own Nx target is reported`` () =
    let message = rejected "script-proxies-nx-target"
    Assert.StartsWith("manifest-script-proxies-nx-target", message)
    Assert.Contains("item=test", message)
    Assert.Contains("widget-e2e:test:e2e", message)

[<Fact>]
let ``a removed manifest whose commands still use npm --prefix is reported`` () =
    let message = rejected "removed-still-prefixed"
    Assert.StartsWith("manifest-removed-still-prefixed", message)
    Assert.Contains("npm --prefix apps/widget-e2e", message)

[<Fact>]
let ``a removed manifest that still names a path is reported`` () =
    let message = rejected "removed-with-path"
    Assert.StartsWith("manifest-removed-with-path", message)
    Assert.Contains("expected=null", message)

// ---------------------------------------------------------------------------
// The two legitimate dispositions
// ---------------------------------------------------------------------------

[<Fact>]
let ``a web application with a real direct consumer passes`` () =
    let report = accepted "retained-web-app"
    Assert.Equal("widget-www", report.Project)
    Assert.Equal(TestContractManifest.Retained, report.Disposition)

[<Fact>]
let ``a postinstall script is not an Nx proxy`` () =
    Assert.Contains("link-assets", (parsed "retained-web-app").Scripts.Head.Command)

[<Fact>]
let ``a removed manifest whose commands moved to project json passes`` () =
    let report = accepted "removed-clean"
    Assert.Equal(TestContractManifest.Removed, report.Disposition)
    Assert.Equal(None, report.Consumer)

[<Fact>]
let ``an nx command outside a script does not trip the proxy rule`` () =
    // removed-clean carries `npx nx run widget-e2e:test:e2e` as a command, not
    // as a manifest script; only scripts can proxy.
    Assert.Contains("native-manifest-valid", TestContractManifest.formatReport (accepted "removed-clean"))

[<Fact>]
let ``the success line names group disposition and consumer`` () =
    let rendered = TestContractManifest.formatReport (accepted "retained-web-app")
    Assert.Contains("group=web-application", rendered)
    Assert.Contains("disposition=retained", rendered)
    Assert.Contains("consumer=the deployment platform", rendered)

[<Fact>]
let ``a removed manifest renders no consumer`` () =
    Assert.Contains("consumer=none", TestContractManifest.formatReport (accepted "removed-clean"))

// ---------------------------------------------------------------------------
// Fixture resolution and naming
// ---------------------------------------------------------------------------

[<Fact>]
let ``an absolute fixture path is refused before any read`` () =
    match TestContractManifest.loadDocument "/repo" "/etc/passwd" with
    | Error(TestContract.Misuse message) -> Assert.Contains("must not be an absolute path", message)
    | _ -> failwith "an absolute fixture path must be refused"

[<Fact>]
let ``a traversal fixture path is refused before any read`` () =
    match TestContractManifest.loadDocument "/repo" "../secrets.json" with
    | Error(TestContract.Misuse message) -> Assert.Contains("must not contain a traversal segment", message)
    | _ -> failwith "a traversal fixture path must be refused"

[<Fact>]
let ``every group renders its contract name`` () =
    Assert.Equal("web-application", TestContractManifest.groupName TestContractManifest.WebApplication)
    Assert.Equal("dedicated-e2e", TestContractManifest.groupName TestContractManifest.DedicatedE2e)
    Assert.Equal("typescript-library", TestContractManifest.groupName TestContractManifest.TypeScriptLibrary)

[<Fact>]
let ``the fixture root is the manifest corpus`` () =
    Assert.Equal("apps/rhino-cli/src/tests/unit/Fixtures/TestContract/Manifest", TestContractManifest.FixtureRoot)
