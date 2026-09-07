/// TickSpec step definitions binding
/// `repo-governance/repo-governance-test-boundary.feature`'s scenarios to
/// `RhinoCli.Application.TestBoundary.auditRepository`, the filesystem half of
/// the audit that the Unit bindings deliberately do not touch.
///
/// Every scenario builds a throwaway repository containing a real
/// `project.json`, a real `repo-config.yml`, and real Integration sources, so
/// project discovery, source globbing, and allowlist loading are proved
/// against the boundary they actually cross.
module RhinoCli.Tests.Integration.Steps.TestBoundaryResourceSteps

/// Explicit static-coverage ownership; the validator scopes this file's
/// TickSpec bindings to these canonical features.
let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/repo-governance/repo-governance-test-boundary.feature" ]

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.TestBoundary

let private featurePath =
    Path.Combine(
        __SOURCE_DIRECTORY__,
        "..",
        "..",
        "..",
        "..",
        "..",
        "specs",
        "apps",
        "rhino",
        "cli",
        "behaviours",
        "repo-governance",
        "repo-governance-test-boundary.feature"
    )

let private cleanSource =
    "module Tests\n\nlet run () = File.ReadAllText \"fixture.txt\"\n"

let private networkSource =
    "module Tests\n\nlet run () = use client = new HttpClient()\n"

let private fixtureStringSource =
    "module Tests\n\nlet packageJson = \"{\\\"dependencies\\\":{\\\"axios\\\":\\\"^1.0.0\\\"}}\"\n"

type TestBoundaryResourceSteps() =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-test-boundary-" + Guid.NewGuid().ToString("N"))

    let mutable findings: TestBoundaryFinding list = []
    let mutable output = ""
    let mutable exitCode = 0

    do Directory.CreateDirectory root |> ignore

    let write (relative: string) (content: string) =
        let absolute =
            Path.Combine(root, relative.Replace('/', Path.DirectorySeparatorChar))

        Directory.CreateDirectory(Path.GetDirectoryName absolute) |> ignore
        File.WriteAllText(absolute, content)

    /// Writes a project that declares `test:integration` plus one Integration source.
    let writeProject (name: string) (sourceName: string) (source: string) =
        write (sprintf "apps/%s/project.json" name) (sprintf """{"name":"%s","targets":{"test:integration":{}}}""" name)

        write (sprintf "apps/%s/tests/integration/%s" name sourceName) source

    /// Writes a `repo-config.yml` carrying only the allowlist under test.
    let writeAllowlist (entries: (string * string option) list) =
        let body =
            match entries with
            | [] -> "integration-loopback: []\n"
            | entries ->
                entries
                |> List.map (fun (project, reason) ->
                    match reason with
                    | Some reason -> sprintf "  - project: %s\n    reason: %s\n" project reason
                    | None -> sprintf "  - project: %s\n" project)
                |> String.concat ""
                |> sprintf "integration-loopback:\n%s"

        write "repo-config.yml" body

    member private _.HandleGiven(step: string) =
        if step.Contains("no integration test source references a network API", StringComparison.Ordinal) then
            writeProject "ose-be" "CleanTests.fs" cleanSource
            writeAllowlist []
        elif step.Contains("the project is not allowlisted", StringComparison.Ordinal) then
            writeProject "ose-be" "HttpTests.fs" networkSource
            writeAllowlist []
        elif step.Contains("the project is allowlisted with a reason", StringComparison.Ordinal) then
            writeProject "ose-be" "HttpTests.fs" networkSource
            writeAllowlist [ "ose-be", Some "proves the SSE adapter over a socket the test starts" ]
        elif step.Contains("a project is allowlisted but no integration test", StringComparison.Ordinal) then
            writeProject "ose-be" "CleanTests.fs" cleanSource
            writeAllowlist [ "ose-be", Some "kept from an earlier loopback proof" ]
        elif step.Contains("declares no test:integration target", StringComparison.Ordinal) then
            writeProject "ose-be" "CleanTests.fs" cleanSource
            writeAllowlist [ "ghost-project", Some "names a project that does not exist" ]
        elif step.Contains("an allowlist entry omits its reason", StringComparison.Ordinal) then
            writeProject "ose-be" "HttpTests.fs" networkSource
            writeAllowlist [ "ose-be", None ]
        elif step.Contains("embeds a package name inside a JSON fixture string", StringComparison.Ordinal) then
            writeProject "ose-be" "FixtureTests.fs" fixtureStringSource
            writeAllowlist []
        else
            failwithf "unhandled test-boundary Given: %s" step

    member private _.HandleWhen(step: string) =
        if step.Contains("repo-governance test-boundary validate", StringComparison.Ordinal) then
            findings <- auditRepository root
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
        elif step.Contains("names the offending project and source file", StringComparison.Ordinal) then
            let finding = Assert.Single findings
            Assert.Equal(KindUnallowlistedNetworkUse, finding.Kind)
            Assert.Equal("ose-be", finding.Project)
            Assert.Equal("apps/ose-be/tests/integration/HttpTests.fs", finding.Path)
        elif step.Contains("reports the allowlist entry as stale", StringComparison.Ordinal) then
            Assert.Equal(KindStaleAllowlistEntry, (Assert.Single findings).Kind)
        elif step.Contains("identifies the unknown allowlisted project", StringComparison.Ordinal) then
            let finding = Assert.Single findings
            Assert.Equal(KindUnknownAllowlistedProject, finding.Kind)
            Assert.Contains("ghost-project", output, StringComparison.Ordinal)
        elif step.Contains("identifies the allowlist entry with no reason", StringComparison.Ordinal) then
            Assert.Equal(KindAllowlistEntryMissingReason, (Assert.Single findings).Kind)
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
    let private extractScenario (lines: string[]) (title: string) =
        let featureLine =
            lines
            |> Array.find (fun line -> line.StartsWith("Feature:", StringComparison.Ordinal))

        let startIndex =
            lines
            |> Array.findIndex (fun line -> line.Trim() = sprintf "Scenario: %s" title)

        let endIndex =
            lines
            |> Array.skip (startIndex + 1)
            |> Array.tryFindIndex (fun line -> line.Trim().StartsWith("Scenario:", StringComparison.Ordinal))
            |> Option.map (fun offset -> startIndex + 1 + offset)
            |> Option.defaultValue lines.Length

        Array.append [| featureLine; "" |] lines.[startIndex .. endIndex - 1]

    let run (title: string) : unit =
        let snippet = extractScenario (File.ReadAllLines featurePath) title
        let definitions = StepDefinitions([| typeof<TestBoundaryResourceSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        (Seq.exactlyOne feature.Scenarios).Action.Invoke()

[<Fact>]
let ``No project uses a network API in Integration tests passes`` () =
    FeatureRunner.run "No project uses a network API in Integration tests passes"

[<Fact>]
let ``An unallowlisted project using a network API fails`` () =
    FeatureRunner.run "An unallowlisted project using a network API fails"

[<Fact>]
let ``An allowlisted project using a network API passes`` () =
    FeatureRunner.run "An allowlisted project using a network API passes"

[<Fact>]
let ``An allowlist entry whose project uses no network API warns`` () =
    FeatureRunner.run "An allowlist entry whose project uses no network API warns"

[<Fact>]
let ``An allowlist entry naming a project without Integration tests fails`` () =
    FeatureRunner.run "An allowlist entry naming a project without Integration tests fails"

[<Fact>]
let ``An allowlist entry with no reason fails`` () =
    FeatureRunner.run "An allowlist entry with no reason fails"

[<Fact>]
let ``A module specifier inside a fixture string is not a network API use`` () =
    FeatureRunner.run "A module specifier inside a fixture string is not a network API use"
