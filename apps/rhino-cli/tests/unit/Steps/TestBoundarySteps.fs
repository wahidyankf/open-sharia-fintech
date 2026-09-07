/// In-process TickSpec proof for `repo-governance-test-boundary.feature`.
/// Filesystem discovery belongs to Integration; these Unit scenarios drive the
/// production audit over an in-memory project set, source map, and allowlist.
module RhinoCli.Tests.Unit.Steps.TestBoundarySteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/repo-governance/repo-governance-test-boundary.feature" ]

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application
open RhinoCli.Application.TestBoundary

/// The one project every scenario starts from.
let private beProject: IntegrationProject =
    { Name = "ose-be"
      Directory = "apps/ose-be" }

let private sourcePath (name: string) =
    sprintf "%s/%s" (integrationRoot beProject) name

/// An Integration source with no network API in sight.
let private cleanSource =
    "module Tests\n\nlet run () = File.ReadAllText \"fixture.txt\"\n"

/// An Integration source that opens an HTTP client.
let private networkSource =
    "module Tests\n\nlet run () = use client = new HttpClient()\n"

/// A package name that lives inside a JSON fixture string, never in import
/// position — the shape the repository's own suites already contain.
let private fixtureStringSource =
    "module Tests\n\nlet packageJson = \"{\\\"dependencies\\\":{\\\"axios\\\":\\\"^1.0.0\\\"}}\"\n"

let private entry project reason : RepoConfig.IntegrationLoopbackEntry = { Project = project; Reason = reason }

type TestBoundarySteps() =
    let mutable projects: IntegrationProject list = [ beProject ]
    let mutable sources: Map<string, string> = Map.empty
    let mutable allowlist: RepoConfig.IntegrationLoopbackEntry list = []
    let mutable findings: TestBoundaryFinding list = []
    let mutable output = ""
    let mutable exitCode = 0

    member private _.HandleGiven(step: string) =
        if step.Contains("no integration test source references a network API", StringComparison.Ordinal) then
            sources <- Map.ofList [ sourcePath "CleanTests.fs", cleanSource ]
        elif step.Contains("the project is not allowlisted", StringComparison.Ordinal) then
            sources <- Map.ofList [ sourcePath "HttpTests.fs", networkSource ]
        elif step.Contains("the project is allowlisted with a reason", StringComparison.Ordinal) then
            sources <- Map.ofList [ sourcePath "HttpTests.fs", networkSource ]
            allowlist <- [ entry "ose-be" "proves the SSE adapter over a socket the test starts" ]
        elif step.Contains("a project is allowlisted but no integration test", StringComparison.Ordinal) then
            sources <- Map.ofList [ sourcePath "CleanTests.fs", cleanSource ]
            allowlist <- [ entry "ose-be" "kept from an earlier loopback proof" ]
        elif step.Contains("declares no test:integration target", StringComparison.Ordinal) then
            sources <- Map.ofList [ sourcePath "CleanTests.fs", cleanSource ]
            allowlist <- [ entry "ghost-project" "names a project that does not exist" ]
        elif step.Contains("an allowlist entry omits its reason", StringComparison.Ordinal) then
            sources <- Map.ofList [ sourcePath "HttpTests.fs", networkSource ]
            allowlist <- [ entry "ose-be" "" ]
        elif step.Contains("embeds a package name inside a JSON fixture string", StringComparison.Ordinal) then
            sources <- Map.ofList [ sourcePath "FixtureTests.fs", fixtureStringSource ]
        else
            failwithf "unhandled test-boundary Given: %s" step

    member private _.HandleWhen(step: string) =
        if step.Contains("repo-governance test-boundary validate", StringComparison.Ordinal) then
            findings <- audit projects sources allowlist
            output <- formatText findings
            exitCode <- if hasBlocking findings then 1 else 0
        else
            failwithf "unhandled test-boundary When: %s" step

    member private _.HandleThen(step: string) =
        if step.Contains("exits successfully", StringComparison.Ordinal) then
            Assert.Equal(0, exitCode)
        elif step.Contains("exits with a failure code", StringComparison.Ordinal) then
            Assert.Equal(1, exitCode)
        elif step.Contains("reports zero findings", StringComparison.Ordinal) then
            Assert.Empty findings
            Assert.Contains("PASSED: zero findings", output, StringComparison.Ordinal)
        elif step.Contains("names the offending project and source file", StringComparison.Ordinal) then
            let finding = Assert.Single findings
            Assert.Equal(KindUnallowlistedNetworkUse, finding.Kind)
            Assert.Equal("ose-be", finding.Project)
            Assert.Equal(sourcePath "HttpTests.fs", finding.Path)
            Assert.Equal(3, finding.Line)
            Assert.Contains("HttpClient", output, StringComparison.Ordinal)
        elif step.Contains("reports the allowlist entry as stale", StringComparison.Ordinal) then
            let finding = Assert.Single findings
            Assert.Equal(KindStaleAllowlistEntry, finding.Kind)
            Assert.Contains("PASSED: 1 warning(s) reported", output, StringComparison.Ordinal)
        elif step.Contains("identifies the unknown allowlisted project", StringComparison.Ordinal) then
            let finding = Assert.Single findings
            Assert.Equal(KindUnknownAllowlistedProject, finding.Kind)
            Assert.Contains("ghost-project", output, StringComparison.Ordinal)
        elif step.Contains("identifies the allowlist entry with no reason", StringComparison.Ordinal) then
            let finding = Assert.Single findings
            Assert.Equal(KindAllowlistEntryMissingReason, finding.Kind)
            Assert.Contains("carries no reason", output, StringComparison.Ordinal)
        else
            failwithf "unhandled test-boundary Then: %s" step

    // GENERATED EXACT BINDINGS START

    [<Given>]
    member this.``a repository where no integration test source references a network API``() =
        this.HandleGiven("a repository where no integration test source references a network API")

    [<Given>]
    member this.``a repository where an integration test opens an HTTP client and the project is not allowlisted``() =
        this.HandleGiven(
            "a repository where an integration test opens an HTTP client and the project is not allowlisted"
        )

    [<Given>]
    member this.``a repository where an integration test opens an HTTP client and the project is allowlisted with a reason``
        ()
        =
        this.HandleGiven(
            "a repository where an integration test opens an HTTP client and the project is allowlisted with a reason"
        )

    [<Given>]
    member this.``a repository where a project is allowlisted but no integration test references a network API``() =
        this.HandleGiven("a repository where a project is allowlisted but no integration test references a network API")

    [<Given>]
    member this.``a repository where an allowlist entry names a project that declares no test:integration target``() =
        this.HandleGiven(
            "a repository where an allowlist entry names a project that declares no test:integration target"
        )

    [<Given>]
    member this.``a repository where an allowlist entry omits its reason``() =
        this.HandleGiven("a repository where an allowlist entry omits its reason")

    [<Given>]
    member this.``a repository where an integration test embeds a package name inside a JSON fixture string``() =
        this.HandleGiven("a repository where an integration test embeds a package name inside a JSON fixture string")

    [<When>]
    member this.``the developer runs repo-governance test-boundary validate``() =
        this.HandleWhen("the developer runs repo-governance test-boundary validate")

    [<Then>]
    member this.``the command exits successfully``() =
        this.HandleThen("the command exits successfully")

    [<Then>]
    member this.``the command exits with a failure code``() =
        this.HandleThen("the command exits with a failure code")

    [<Then>]
    member this.``the test-boundary output reports zero findings``() =
        this.HandleThen("the test-boundary output reports zero findings")

    [<Then>]
    member this.``the test-boundary output names the offending project and source file``() =
        this.HandleThen("the test-boundary output names the offending project and source file")

    [<Then>]
    member this.``the test-boundary output reports the allowlist entry as stale``() =
        this.HandleThen("the test-boundary output reports the allowlist entry as stale")

    [<Then>]
    member this.``the test-boundary output identifies the unknown allowlisted project``() =
        this.HandleThen("the test-boundary output identifies the unknown allowlisted project")

    [<Then>]
    member this.``the test-boundary output identifies the allowlist entry with no reason``() =
        this.HandleThen("the test-boundary output identifies the allowlist entry with no reason")

// GENERATED EXACT BINDINGS END

module private FeatureRunner =
    let private readEmbeddedFeature (featureFileName: string) =
        let assembly = typeof<TestBoundarySteps>.Assembly

        let resourceName =
            assembly.GetManifestResourceNames()
            |> Array.tryFind (fun name -> name.EndsWith("." + featureFileName, StringComparison.Ordinal))
            |> Option.defaultWith (fun () -> failwithf "embedded test-boundary feature not found: %s" featureFileName)

        use stream = assembly.GetManifestResourceStream(resourceName)
        use reader = new StreamReader(stream)
        reader.ReadToEnd().Split('\n')

    let run featureFileName =
        let definitions = StepDefinitions([| typeof<TestBoundarySteps> |])

        let feature =
            definitions.GenerateFeature(featureFileName, readEmbeddedFeature featureFileName)

        feature.Scenarios |> Seq.iter (fun scenario -> scenario.Action.Invoke())

[<Fact>]
let ``test-boundary behaviours have pure Unit proof`` () =
    FeatureRunner.run "repo-governance-test-boundary.feature"

[<Fact>]
let ``a source outside the project's Integration root never enters the audit`` () =
    let findings =
        audit
            [ beProject ]
            (Map.ofList
                [ "apps/ose-be/tests/unit/HttpTests.fs", networkSource
                  "apps/ose-be/src/Client.fs", networkSource ])
            []

    Assert.Empty findings

[<Fact>]
let ``a non-source file under the Integration root is not scanned`` () =
    Assert.False(isScannableSource (sourcePath "fixture.json"))
    Assert.True(isScannableSource (sourcePath "HttpTests.FS"))

    let findings =
        audit [ beProject ] (Map.ofList [ sourcePath "fixture.json", networkSource ]) []

    Assert.Empty findings

[<Fact>]
let ``every network API construct the audit knows about is detected`` () =
    let constructs =
        [ "new HttpListener()"
          "new HttpWebRequest()"
          "new TcpClient()"
          "new TcpListener()"
          "new UdpClient()"
          "new WebClient()"
          "new ClientWebSocket()"
          "new Socket(AddressFamily.InterNetwork)"
          "new XMLHttpRequest()"
          "await fetch(url)"
          "new WebSocket(url)"
          "import http from \"node:http\""
          "import \"node:net\""
          "const request = require(\"supertest\")"
          "import got from \"got\"" ]

    for construct in constructs do
        Assert.Equal(1, List.length (findNetworkUses construct))

[<Fact>]
let ``a network API name inside a string literal is data, not a call`` () =
    // The audit's own Integration fixtures embed these exact shapes.
    Assert.Empty(findNetworkUses "let networkSource = \"let c = new HttpClient()\"")
    Assert.Empty(findNetworkUses "let verbatim = @\"new TcpListener()\"")
    Assert.Empty(findNetworkUses "let escaped = \"a \\\" new UdpClient()\"")
    Assert.Empty(findNetworkUses "let json = \"\"\"{\"kind\":\"new WebClient()\"}\"\"\"")
    // The same construct outside a string is still caught.
    Assert.Equal(1, List.length (findNetworkUses "let c = new HttpClient()"))
    Assert.Equal(1, List.length (findNetworkUses "let label = \"harmless\" in new TcpClient()"))

[<Fact>]
let ``withoutStringLiterals removes every literal form`` () =
    Assert.Equal("let a =  + ", withoutStringLiterals "let a = \"one\" + \"two\"")
    Assert.Equal("let b = ", withoutStringLiterals "let b = @\"C:\\path\"")
    Assert.Equal("let c = ", withoutStringLiterals "let c = \"\"\"raw \"quoted\" text\"\"\"")
    Assert.Equal("let d = 1", withoutStringLiterals "let d = 1")

[<Fact>]
let ``a method call named fetch on an object is not a network use`` () =
    Assert.Empty(findNetworkUses "repository.fetch(id)")
    Assert.Empty(findNetworkUses "let axios = \"axios\"")

[<Fact>]
let ``findings sort by project then kind then path then line`` () =
    let other: IntegrationProject =
        { Name = "aaa-first"
          Directory = "apps/aaa-first" }

    let twoUses = "let a = new HttpClient()\nlet b = new TcpClient()\n"

    let findings =
        audit
            [ beProject; other ]
            (Map.ofList
                [ sourcePath "ZTests.fs", networkSource
                  sourcePath "ATests.fs", twoUses
                  "apps/aaa-first/tests/integration/Tests.fs", networkSource ])
            []

    let ordered = findings |> List.map (fun f -> f.Project, f.Path, f.Line)

    Assert.Equal<(string * string * int) list>(
        [ "aaa-first", "apps/aaa-first/tests/integration/Tests.fs", 3
          "ose-be", sourcePath "ATests.fs", 1
          "ose-be", sourcePath "ATests.fs", 2
          "ose-be", sourcePath "ZTests.fs", 3 ],
        ordered
    )

[<Fact>]
let ``a missing reason and a stale entry are reported together`` () =
    let findings = audit [ beProject ] Map.empty [ entry "ose-be" "  " ]

    Assert.Equal<string list>(
        [ KindAllowlistEntryMissingReason; KindStaleAllowlistEntry ],
        findings |> List.map (fun f -> f.Kind)
    )

    Assert.True(hasBlocking findings)
    Assert.Contains("FAILED: 2 finding(s) reported", formatText findings, StringComparison.Ordinal)

[<Fact>]
let ``an unknown allowlisted project is never also reported as stale`` () =
    let findings = audit [] Map.empty [ entry "ghost" "reason" ]
    let finding = Assert.Single findings
    Assert.Equal(KindUnknownAllowlistedProject, finding.Kind)
    Assert.Equal("ghost", finding.Project)
    Assert.Contains("  ghost  [blocking]", formatText findings, StringComparison.Ordinal)

[<Fact>]
let ``readIntegrationProject accepts only a named project declaring the target`` () =
    let named =
        readIntegrationProject "apps/ose-be" """{"name":"ose-be","targets":{"test:integration":{}}}"""

    Assert.Equal(
        Some
            { Name = "ose-be"
              Directory = "apps/ose-be" },
        named
    )

    Assert.Equal(None, readIntegrationProject "apps/x" """{"name":"x","targets":{"test:unit":{}}}""")
    Assert.Equal(None, readIntegrationProject "apps/x" """{"targets":{"test:integration":{}}}""")
    Assert.Equal(None, readIntegrationProject "apps/x" """{"name":7,"targets":{"test:integration":{}}}""")
    Assert.Equal(None, readIntegrationProject "apps/x" """{"name":null,"targets":{"test:integration":{}}}""")
    Assert.Equal(None, readIntegrationProject "apps/x" """{"name":"x"}""")
    Assert.Equal(None, readIntegrationProject "apps/x" """{}""")
    Assert.Equal(None, readIntegrationProject "apps/x" "not json")

[<Fact>]
let ``the Integration root tolerates a trailing separator in the project directory`` () =
    Assert.Equal(
        "apps/ose-be/tests/integration",
        integrationRoot
            { Name = "ose-be"
              Directory = "apps/ose-be/" }
    )

[<Fact>]
let ``a path-scoped finding with no line renders without a line suffix`` () =
    let rendered =
        formatText
            [ { Project = "ose-be"
                Path = "apps/ose-be/tests/integration/HttpTests.fs"
                Line = 0
                Severity = "warning"
                Kind = KindStaleAllowlistEntry
                Message = "no line" } ]

    Assert.Contains("  apps/ose-be/tests/integration/HttpTests.fs  [warning]", rendered, StringComparison.Ordinal)
    Assert.DoesNotContain(".fs:0", rendered, StringComparison.Ordinal)

[<Fact>]
let ``toRelativePath renders a repository-relative path with forward slashes`` () =
    let root = Path.Combine(Path.GetTempPath(), "rhino-relative-root")

    Assert.Equal("apps/ose-be/project.json", toRelativePath root (Path.Combine(root, "apps", "ose-be", "project.json")))

[<Fact>]
let ``the allowlist round-trips through repo-config parsing`` () =
    let document =
        "harness-catalog:\n"
        + "  document: docs/reference/platform-bindings.md\n"
        + "  verified: 2026-09-07\n"
        + "integration-loopback:\n"
        + "  - project: ose-be\n"
        + "    reason: proves the SSE adapter over a socket the test starts\n"
        + "  - project: rhino-cli\n"

    let expectedCatalog: RepoConfig.HarnessCatalog =
        { Document = "docs/reference/platform-bindings.md"
          Verified = "2026-09-07" }

    let expectedAllowlist: RepoConfig.IntegrationLoopbackEntry list =
        [ { Project = "ose-be"
            Reason = "proves the SSE adapter over a socket the test starts" }
          { Project = "rhino-cli"; Reason = "" } ]

    match RepoConfig.parse document with
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    | Ok config ->
        Assert.Equal(Some expectedCatalog, config.HarnessCatalog)
        Assert.Equal<RepoConfig.IntegrationLoopbackEntry list>(expectedAllowlist, config.IntegrationLoopback)

[<Fact>]
let ``an allowlist entry with no project key is dropped`` () =
    let expected: RepoConfig.IntegrationLoopbackEntry list =
        [ { Project = "ose-be"; Reason = "" } ]

    // The empty `-` item deserializes to a null entry; the missing-`project`
    // item deserializes to a non-null entry with a null name. Both are dropped.
    match RepoConfig.parse "integration-loopback:\n  -\n  - reason: nameless\n  - project: ose-be\n" with
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    | Ok config -> Assert.Equal<RepoConfig.IntegrationLoopbackEntry list>(expected, config.IntegrationLoopback)

[<Fact>]
let ``an absent allowlist parses to the empty list`` () =
    match RepoConfig.parse "doctor:\n  skip-tools: []\n" with
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    | Ok config -> Assert.Empty config.IntegrationLoopback
