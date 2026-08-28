/// TickSpec step definitions binding `harness/agents-bindings.feature`'s 10
/// scenarios to `RhinoCli.Application.Harness`
/// [Repo-grounded —
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/harness/agents-bindings.feature`,
/// `apps/rhino-cli/src/application/agents/bindings.rs`,
/// `apps/rhino-cli/src/commands/harness_generate_bindings.rs`].
///
/// Follows `GovernanceSteps.fs`'s per-scenario slicing convention: each xunit
/// `[<Fact>]` below runs exactly one scenario, extracted from the real, frozen
/// feature file. `harness` is not yet listed in `FSHARP_NAMESPACES` (that flip
/// closes Wave E), so every scenario calls `RhinoCli.Application.Harness`'s
/// functions directly rather than through CLI argv parsing.
///
/// Two scenario families read this repository itself rather than a fixture,
/// because that is what they assert about:
///
///   - the `@harness-purge` scenario is a claim about the committed tree —
///     that `.cursor/`, `.amazonq/`, and `.pi/` hold zero tracked files — so
///     it shells out to `git ls-files` at the real repository root, the same
///     evidence the scenario's own `When` step names;
///   - the `@harness-name-registry-derived` scenarios assert that `--harness`
///     acceptance is derived from `repo-config.yml`'s `harness:` registry, so
///     they load this repository's real registry (mirroring
///     `RepoConfigSteps.fs`'s precedent) instead of a synthetic one — a
///     fixture registry would prove only that the lookup works, never that
///     the live registry declares `codex` and does not declare `cursor`.
///
/// Every other scenario builds a throwaway fixture repository under its own
/// fresh `scenarioRoot()` temp directory, mirroring `bindings.rs`'s own unit
/// tests, which likewise always pass a `TempDir` as the repository root.
module RhinoCli.Tests.Unit.Steps.HarnessSteps

open System
open System.Diagnostics
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application

/// Absolute path of the repository root this test assembly was built from,
/// derived from the source location so a worktree checkout resolves to its
/// own root rather than the primary checkout's.
let private repositoryRoot: string =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "..", "..", ".."))

/// The binding surfaces the purge removed. Every assertion about "a dropped
/// harness surface" is stated against this list, so re-adding one of them to
/// `knownBindingDirs` fails the `@binding-surface-set` scenarios rather than
/// silently passing.
let private droppedHarnessSurfaces: string list = [ ".cursor"; ".amazonq"; ".pi" ]

/// Instance step-definition container — see `ConventionSteps.fs`'s module doc
/// comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism here.
type HarnessSteps() =
    let mutable scenarioRootDir: string option = None
    let mutable lastResult: Harness.ValidationResult option = None
    let mutable lastExitCode: int option = None
    let mutable lastNameError: string option = None
    let mutable trackedFileCounts: (string * int) list = []
    let mutable expectedPaths: string list = []
    let mutable knownDirs: string list = []

    let scenarioRoot () : string =
        match scenarioRootDir with
        | Some dir -> dir
        | None ->
            let dir =
                Path.Combine(Path.GetTempPath(), "rhino-cli-harness-" + Guid.NewGuid().ToString("N"))

            Directory.CreateDirectory dir |> ignore
            scenarioRootDir <- Some dir
            dir

    /// The smallest registry a fixture repository needs: a source tier plus the
    /// two generated mirrors, matching the shape production carries
    /// [Repo-grounded — `bindings.rs`'s `write_three_harness_config`].
    let writeThreeHarnessConfig (root: string) : unit =
        File.WriteAllText(
            Path.Combine(root, "repo-config.yml"),
            String.Join(
                "\n",
                [ "harness:"
                  "  - { name: claude-code, tier: source, agent-dir: .claude/agents }"
                  "  - name: opencode"
                  "    tier: generated"
                  "    agent-dir: .opencode/agents"
                  "    mirrors: .claude/agents"
                  "  - name: codex"
                  "    tier: generated"
                  "    agent-dir: .codex/agents"
                  "    mirrors: .claude/agents"
                  "coverage:"
                  "  projects: []"
                  "" ]
            )
        )

    /// Materializes the mirror pair every sync check expects to find
    /// [Repo-grounded — `bindings.rs`'s `write_empty_mirror_pair`].
    let writeEmptyMirrorPair (root: string) : unit =
        Directory.CreateDirectory(Path.Combine(root, ".claude", "agents")) |> ignore
        Directory.CreateDirectory(Path.Combine(root, ".opencode", "agents")) |> ignore

    let writeCatalog (root: string) (body: string) : unit =
        let path = Path.Combine(root, "docs", "reference", "platform-bindings.md")
        Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
        File.WriteAllText(path, body)

    /// A catalog body referencing every known binding directory, so coverage
    /// passes for whichever directories a fixture materializes
    /// [Repo-grounded — `bindings.rs`'s `full_catalog`].
    let fullCatalog () : string =
        let rows =
            Harness.knownBindingDirs |> List.map (fun dir -> sprintf "- `%s` row" dir)

        String.Join("\n", "# Platform Bindings" :: "" :: rows) + "\n"

    let runValidate (root: string) : unit =
        let result = Harness.validateBindings root
        lastResult <- Some result
        lastExitCode <- Some(if result.FailedChecks = 0 then 0 else 1)

    let result () : Harness.ValidationResult =
        match lastResult with
        | Some r -> r
        | None -> failwith "no validation has been run in this scenario"

    let exitCode () : int =
        match lastExitCode with
        | Some code -> code
        | None -> failwith "no command has been run in this scenario"

    /// Runs `git ls-files -- <path>` at the repository root and returns the
    /// number of tracked paths it reports.
    let trackedFileCount (path: string) : int =
        let psi = ProcessStartInfo("git")
        psi.WorkingDirectory <- repositoryRoot
        psi.RedirectStandardOutput <- true
        psi.RedirectStandardError <- true
        psi.UseShellExecute <- false
        psi.ArgumentList.Add "ls-files"
        psi.ArgumentList.Add "--"
        psi.ArgumentList.Add path

        use proc = Process.Start psi
        let stdout = proc.StandardOutput.ReadToEnd()
        proc.WaitForExit()

        Assert.Equal(0, proc.ExitCode)

        stdout.Split('\n')
        |> Array.filter (fun line -> line.Trim() <> "")
        |> Array.length

    // ---- @harness-purge ----

    [<Given>]
    member _.``\.cursor/ tracked (\d+) files, \.amazonq/ tracked (\d+) files, and \.pi/ tracked (\d+) file before the purge``
        (cursor: int, amazonq: int, pi: int)
        =
        // Narrative provenance only: the pre-purge counts are history, not
        // state this test can reconstruct. Recording them keeps the scenario's
        // claim ("these three surfaces used to carry tracked files") legible
        // next to the post-purge assertion that they no longer do.
        Assert.True(cursor > 0 && amazonq > 0 && pi > 0)

    [<When>]
    member _.``git ls-files is run against those three paths after the purge``() =
        trackedFileCounts <- droppedHarnessSurfaces |> List.map (fun dir -> dir, trackedFileCount dir)

    [<Then>]
    member _.``each returns zero tracked files``() =
        for dir, count in trackedFileCounts do
            Assert.Equal((dir, 0), (dir, count))

    [<Then>]
    member _.``harness bindings validate exits successfully, where before the purge it required \.amazonq/ byte-parity``
        ()
        =
        let actual = Harness.validateBindings repositoryRoot
        Assert.Equal(0, actual.FailedChecks)

        // The `.amazonq` bridge required byte-parity of its own binding files
        // before the purge; no check may name it now.
        Assert.DoesNotContain(
            actual.Checks,
            fun (check: Harness.ValidationCheck) ->
                check.Name.Contains(".amazonq", StringComparison.Ordinal)
                || check.Message.Contains(".amazonq", StringComparison.Ordinal)
        )

    // ---- @binding-surface-set ----

    [<Given>]
    member _.``the compiled set of known binding directories``() = knownDirs <- Harness.knownBindingDirs

    [<When>]
    member _.``the set is inspected``() = ()

    [<Then>]
    member _.``it contains exactly \.claude, \.opencode, \.codex, \.agents, and \.github``() =
        Assert.Equal<string list>([ ".claude"; ".opencode"; ".codex"; ".agents"; ".github" ], knownDirs)

    [<Then>]
    member _.``it names no dropped harness surface``() =
        for dropped in droppedHarnessSurfaces do
            Assert.DoesNotContain(dropped, knownDirs)

    [<When>]
    member _.``the expected binding files are computed``() =
        match Harness.expectedBindingPaths repositoryRoot with
        | Ok paths -> expectedPaths <- paths
        | Error e -> failwith e

    [<Then>]
    member _.``no expected file lives under a dropped harness surface``() =
        for dropped in droppedHarnessSurfaces do
            Assert.DoesNotContain(
                expectedPaths,
                fun (path: string) -> path.StartsWith(dropped + "/", StringComparison.Ordinal)
            )

    // ---- @harness-name-registry-derived ----

    [<Given>]
    member _.``the repo-config\.yml harness registry declares ([a-z-]+)``(name: string) =
        match RepoConfig.load repositoryRoot with
        | Ok config -> Assert.Contains(name, Harness.acceptedHarnessNames config)
        | Error e -> failwith e

    [<Given>]
    member _.``the repo-config\.yml harness registry does not declare ([a-z-]+)``(name: string) =
        match RepoConfig.load repositoryRoot with
        | Ok config -> Assert.DoesNotContain(name, Harness.acceptedHarnessNames config)
        | Error e -> failwith e

    [<When>]
    member _.``the developer runs harness bindings generate for ([a-z-]+)``(name: string) =
        match RepoConfig.load repositoryRoot with
        | Error e -> failwith e
        | Ok config ->
            match Harness.validateHarnessName config name with
            | Ok() ->
                lastNameError <- None
                lastExitCode <- Some 0
            | Error message ->
                lastNameError <- Some message
                lastExitCode <- Some 1

    [<Then>]
    member _.``the harness name is not rejected as unknown``() =
        Assert.Null(Option.toObj lastNameError)
        Assert.Equal(0, exitCode ())

    [<Then>]
    member _.``the error names the registry-derived accepted set``() =
        let message =
            match lastNameError with
            | Some m -> m
            | None -> failwith "the command did not report a harness-name error"

        match RepoConfig.load repositoryRoot with
        | Error e -> failwith e
        | Ok config ->
            // Every registry-declared name, quoted, has to appear — a message
            // naming only some of them would send the developer looking for
            // the rest.
            for name in Harness.acceptedHarnessNames config do
                Assert.Contains(sprintf "'%s'" name, message)

    // ---- @agents-validate-bindings ----

    [<Given>]
    member _.``a repository whose generated binding files match the generated content``() =
        let root = scenarioRoot ()
        writeThreeHarnessConfig root
        writeEmptyMirrorPair root
        Directory.CreateDirectory(Path.Combine(root, ".github")) |> ignore
        Directory.CreateDirectory(Path.Combine(root, ".codex")) |> ignore

    [<Given>]
    member _.``the platform-bindings catalog references every present binding directory``() =
        writeCatalog (scenarioRoot ()) (fullCatalog ())

    [<Given>]
    member _.``a repository with a known binding directory that the platform-bindings catalog does not reference``() =
        let root = scenarioRoot ()
        writeThreeHarnessConfig root
        writeEmptyMirrorPair root
        // `.github` is materialized but deliberately left out of the catalog.
        Directory.CreateDirectory(Path.Combine(root, ".github")) |> ignore
        writeCatalog root "# Platform Bindings\n\n- `.claude` row\n- `.opencode` row\n"

    [<Given>]
    member _.``a repository where some known binding directories do not exist on disk``() =
        let root = scenarioRoot ()
        writeThreeHarnessConfig root
        writeEmptyMirrorPair root
        // `.codex`, `.agents`, and `.github` are never created; the catalog
        // references only the two directories that are.
        writeCatalog root "# Platform Bindings\n\n- `.claude` row\n- `.opencode` row\n"

    [<When>]
    member _.``the developer runs harness bindings validate``() = runValidate (scenarioRoot ())

    [<Then>]
    member _.``the command exits successfully``() =
        let notPassed =
            (result ()).Checks
            |> List.filter (fun (check: Harness.ValidationCheck) -> check.Status <> "passed")

        // Asserted before the exit code so a failure names the offending
        // check rather than reporting only "expected 0, got 1".
        Assert.Equal<Harness.ValidationCheck list>([], notPassed)
        Assert.Equal(0, exitCode ())

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.Equal(1, exitCode ())

    [<Then>]
    member _.``the output reports all binding checks as passing``() =
        let actual = (result ())
        Assert.Equal(actual.TotalChecks, actual.PassedChecks)
        Assert.True(actual.TotalChecks > 0)

    [<Then>]
    member _.``the output identifies the binding directory missing a catalog row``() =
        let failing =
            (result ()).Checks
            |> List.filter (fun (check: Harness.ValidationCheck) ->
                check.Status = "failed" && check.Name = "Catalog Coverage: .github")

        Assert.NotEmpty failing

        for check in failing do
            Assert.Contains(Harness.platformBindingsCatalog, check.Message)

    [<Then>]
    member _.``no catalog row is required for the absent binding directories``() =
        let absent =
            Harness.knownBindingDirs
            |> List.filter (fun dir -> not (Directory.Exists(Path.Combine(scenarioRoot (), dir))))

        Assert.NotEmpty absent

        for dir in absent do
            let check =
                (result ()).Checks
                |> List.find (fun (c: Harness.ValidationCheck) -> c.Name = sprintf "Catalog Coverage: %s" dir)

            Assert.Equal("passed", check.Status)
            Assert.Contains("no catalog row required", check.Message)

    // ---- @codex-agents-extension ----

    [<Given>]
    member _.``a repository whose \.codex/agents directory holds a standalone \.toml agent file``() =
        let root = scenarioRoot ()
        writeThreeHarnessConfig root
        writeEmptyMirrorPair root
        Directory.CreateDirectory(Path.Combine(root, ".github")) |> ignore
        writeCatalog root (fullCatalog ())

        let agentsDir = Path.Combine(root, ".codex", "agents")
        Directory.CreateDirectory agentsDir |> ignore
        File.WriteAllText(Path.Combine(agentsDir, "probe-maker.toml"), "description = \"probe\"\n")

    [<Given>]
    member _.``a repository whose \.codex/agents directory holds a \.md agent file``() =
        let root = scenarioRoot ()
        writeThreeHarnessConfig root
        writeEmptyMirrorPair root
        Directory.CreateDirectory(Path.Combine(root, ".github")) |> ignore
        writeCatalog root (fullCatalog ())

        let agentsDir = Path.Combine(root, ".codex", "agents")
        Directory.CreateDirectory agentsDir |> ignore
        File.WriteAllText(Path.Combine(agentsDir, "probe-maker.md"), "# probe\n")

    [<Then>]
    member _.``the output names \.toml as the officially-correct extension``() =
        let failing =
            (result ()).Checks
            |> List.filter (fun (check: Harness.ValidationCheck) ->
                check.Status = "failed"
                && check.Message.Contains("probe-maker.md", StringComparison.Ordinal))

        Assert.NotEmpty failing

        for check in failing do
            Assert.Contains(".toml", check.Message)

/// Slices one scenario out of the real, frozen feature file and runs it
/// against `HarnessSteps` — see `GovernanceSteps.fs`'s runner for the shared
/// convention.
module private FeatureRunner =

    let private featurePath: string =
        Path.GetFullPath(
            Path.Combine(
                __SOURCE_DIRECTORY__,
                "..",
                "..",
                "..",
                "..",
                "..",
                "..",
                "specs",
                "apps",
                "rhino",
                "behavior",
                "rhino-cli",
                "gherkin",
                "harness",
                "agents-bindings.feature"
            )
        )

    let private extractScenario (featureLines: string[]) (scenarioTitle: string) : string[] =
        let featureLine =
            featureLines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let startIdx =
            featureLines
            |> Array.findIndex (fun l -> l.Trim() = sprintf "Scenario: %s" scenarioTitle)

        let endIdx =
            featureLines
            |> Array.skip (startIdx + 1)
            |> Array.tryFindIndex (fun l ->
                let trimmed = l.Trim()

                // A `Rule:` block is introduced by its own `@tag` line, which
                // sits BEFORE the `Rule:` keyword. Stopping only at `Rule:`
                // would leave that dangling tag as the slice's last line, and
                // TickSpec rejects a tag with no block after it ("File
                // continues unexpectedly").
                trimmed.StartsWith("Scenario:", StringComparison.Ordinal)
                || trimmed.StartsWith("Rule:", StringComparison.Ordinal)
                || trimmed.StartsWith("@", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.concat [ [| featureLine; "" |]; featureLines.[startIdx .. endIdx - 1] ]

    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<HarnessSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)

        for scenario in feature.Scenarios do
            scenario.Action.Invoke()

[<Fact>]
let ``Generated binding directories for dropped harnesses no longer exist`` () =
    FeatureRunner.run "Generated binding directories for dropped harnesses no longer exist"

[<Fact>]
let ``Only surviving harness surfaces are known`` () =
    FeatureRunner.run "Only surviving harness surfaces are known"

[<Fact>]
let ``No dropped-harness binding file is expected any more`` () =
    FeatureRunner.run "No dropped-harness binding file is expected any more"

[<Fact>]
let ``A registry-declared harness name is accepted`` () =
    FeatureRunner.run "A registry-declared harness name is accepted"

[<Fact>]
let ``A harness name absent from the registry is rejected`` () =
    FeatureRunner.run "A harness name absent from the registry is rejected"

[<Fact>]
let ``A repository matching the generator passes validation`` () =
    FeatureRunner.run "A repository matching the generator passes validation"

[<Fact>]
let ``A present binding directory absent from the catalog fails validation`` () =
    FeatureRunner.run "A present binding directory absent from the catalog fails validation"

[<Fact>]
let ``Absent binding directories require no catalog row`` () =
    FeatureRunner.run "Absent binding directories require no catalog row"

[<Fact>]
let ``A .codex/agents directory holding only .toml files passes validation`` () =
    FeatureRunner.run "A .codex/agents directory holding only .toml files passes validation"

[<Fact>]
let ``A .md file under .codex/agents fails validation`` () =
    FeatureRunner.run "A .md file under .codex/agents fails validation"
