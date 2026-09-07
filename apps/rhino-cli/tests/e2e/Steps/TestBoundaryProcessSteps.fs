/// TickSpec step definitions proving the published binary's
/// `repo-governance test-boundary validate` behaviour through the real process
/// boundary: a throwaway git repository on disk, the shipped executable, and
/// its exit code and stdout.
module RhinoCli.Tests.E2e.Steps.TestBoundaryProcessSteps

/// Explicit static-coverage ownership; the validator scopes this file's
/// TickSpec bindings to these canonical features.
let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/repo-governance/repo-governance-test-boundary.feature" ]

open System
open System.Diagnostics
open System.IO
open TickSpec
open Xunit

let private repositoryRoot =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "..", ".."))

let private executable =
    Path.Combine(repositoryRoot, "apps", "rhino-cli", "src", "dist", "rhino-cli-fsharp")

let private cleanSource =
    "module Tests\n\nlet run () = File.ReadAllText \"fixture.txt\"\n"

let private networkSource =
    "module Tests\n\nlet run () = use client = new HttpClient()\n"

let private fixtureStringSource =
    "module Tests\n\nlet packageJson = \"{\\\"dependencies\\\":{\\\"axios\\\":\\\"^1.0.0\\\"}}\"\n"

type TestBoundaryProcessSteps() =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-test-boundary-e2e-" + Guid.NewGuid().ToString("N"))

    let mutable exitCode = 0
    let mutable stdout = ""

    do
        Directory.CreateDirectory root |> ignore
        let info = ProcessStartInfo("git", WorkingDirectory = root)
        info.ArgumentList.Add "init"
        info.ArgumentList.Add "--quiet"
        use childProcess = Process.Start info
        childProcess.WaitForExit()
        Assert.Equal(0, childProcess.ExitCode)

    let write (relative: string) (content: string) =
        let absolute =
            Path.Combine(root, relative.Replace('/', Path.DirectorySeparatorChar))

        Directory.CreateDirectory(Path.GetDirectoryName absolute) |> ignore
        File.WriteAllText(absolute, content)

    let writeProject (name: string) (sourceName: string) (source: string) =
        write (sprintf "apps/%s/project.json" name) (sprintf """{"name":"%s","targets":{"test:integration":{}}}""" name)

        write (sprintf "apps/%s/tests/integration/%s" name sourceName) source

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
            let info =
                ProcessStartInfo(
                    executable,
                    WorkingDirectory = root,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true
                )

            [ "repo-governance"; "test-boundary"; "validate" ]
            |> List.iter info.ArgumentList.Add

            info.Environment.["GIT_CONFIG_GLOBAL"] <- "/dev/null"
            info.Environment.["GIT_CONFIG_SYSTEM"] <- "/dev/null"
            use childProcess = Process.Start info
            stdout <- childProcess.StandardOutput.ReadToEnd()
            childProcess.StandardError.ReadToEnd() |> ignore
            childProcess.WaitForExit()
            exitCode <- childProcess.ExitCode
        else
            failwithf "unhandled test-boundary When: %s" step

    member private _.HandleThen(step: string) =
        if step.Contains("exits successfully", StringComparison.Ordinal) then
            Assert.Equal(0, exitCode)
        elif step.Contains("exits with a failure code", StringComparison.Ordinal) then
            Assert.Equal(1, exitCode)
        elif step.Contains("reports zero findings", StringComparison.Ordinal) then
            Assert.Contains("PASSED: zero findings", stdout, StringComparison.Ordinal)
        elif step.Contains("names the offending project and source file", StringComparison.Ordinal) then
            Assert.Contains("apps/ose-be/tests/integration/HttpTests.fs", stdout, StringComparison.Ordinal)
            Assert.Contains("unallowlisted-network-use", stdout, StringComparison.Ordinal)
        elif step.Contains("reports the allowlist entry as stale", StringComparison.Ordinal) then
            Assert.Contains("stale-allowlist-entry", stdout, StringComparison.Ordinal)
        elif step.Contains("identifies the unknown allowlisted project", StringComparison.Ordinal) then
            Assert.Contains("unknown-allowlisted-project", stdout, StringComparison.Ordinal)
            Assert.Contains("ghost-project", stdout, StringComparison.Ordinal)
        elif step.Contains("identifies the allowlist entry with no reason", StringComparison.Ordinal) then
            Assert.Contains("allowlist-entry-missing-reason", stdout, StringComparison.Ordinal)
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
    let private directory =
        Path.Combine(repositoryRoot, "specs", "apps", "rhino", "cli", "behaviours", "repo-governance")

    let run featureFileName =
        let path = Path.Combine(directory, featureFileName)
        let definitions = StepDefinitions([| typeof<TestBoundaryProcessSteps> |])
        let feature = definitions.GenerateFeature(path, File.ReadAllLines path)
        feature.Scenarios |> Seq.iter (fun scenario -> scenario.Action.Invoke())

[<Fact>]
let ``published Rhino proves the Integration network boundary`` () =
    FeatureRunner.run "repo-governance-test-boundary.feature"
