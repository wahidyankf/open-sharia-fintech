/// TickSpec step definitions binding
/// `governance-readme-index.feature`'s scenarios 1-9 ("A complete index
/// passes" through "A generated mirror directory is not scanned") to
/// `RhinoCli.Application.Governance`
/// [Repo-grounded —
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/governance/governance-readme-index.feature`,
/// `apps/rhino-cli/src/application/governance/readme_index.rs`,
/// `apps/rhino-cli/src/commands/governance_validate_readme_index.rs`].
///
/// This is PR8a of a three-way split (the feature file's 19 scenarios
/// exceed this repository's per-PR line ceilings — see `delivery.md`'s
/// `governance-readme-index.feature` heading). PR8b adds the `Unannotated`
/// finding kind, the gate-id-rename registry check, and the
/// `--paths`/`--fail-kinds` flags (scenarios 10-14); PR8c adds
/// `generate`/`rewrite-paths` (scenarios 15-19). Both later PRs extend THIS
/// same file — they do not fork a separate one.
///
/// Follows `MdSteps.fs`'s/`EnvStagedGuardSteps.fs`'s per-scenario slicing
/// convention: each xunit `[<Fact>]` below runs exactly one scenario,
/// extracted from the real, frozen feature file. `governance` is not yet
/// listed in `FSHARP_NAMESPACES` (that flip is later, separate Wave D
/// integration work), so every scenario below calls
/// `RhinoCli.Application.Governance`'s functions directly with an explicit
/// path list, never through CLI argv parsing.
///
/// Most fixture `Given` steps below name repo-realistic-looking paths (e.g.
/// `"repo-governance/conventions/formatting/"`, `".claude/skills/grill-me/
/// reference/"`) purely for narrative flavor: `.claude/skills/grill-me/
/// reference/` genuinely has a `README.md` in this very repository today, so
/// a scenario asserting it is missing one is necessarily building an
/// isolated, throwaway temp-directory fixture, not reading the real tree —
/// only the final path SEGMENT of each such label is used to name the
/// on-disk fixture directory (`resolveIndexFile`/the `directory "..."
/// contains ...` steps below), and every scenario's fixture lives under its
/// own fresh `scenarioRoot()` temp directory, always passed to
/// `Governance.auditReadmeIndex` as an explicit, absolute scan root —
/// mirroring `readme_index.rs`'s own unit tests, which likewise always pass
/// a throwaway `TempDir` as the scan root rather than exercising
/// `DEFAULT_PATHS` against the real repository.
///
/// The two scenarios that DO need `DEFAULT_PATHS`'s actual routing behavior
/// ("An uncovered tree is not scanned", "A generated mirror directory is not
/// scanned") deliberately leave `scanPathsOverride` unset so the shared "the
/// developer runs governance readme-index validate" `When` step falls back
/// to `Governance.resolveScanPaths []` — proving a fixture placed outside
/// `docs/`, `repo-governance/`, `specs/`, `.claude/` is never reached, the
/// same way `readme_index.rs`'s own
/// `scenario_a_generated_mirror_directory_is_not_scanned` test only ever
/// scans a `repo-governance` root and leaves an out-of-scope mirror tree
/// beside it.
///
/// This PR's "the command exits successfully"/"exits with a failure code"
/// steps check `List.isEmpty lastFindings` directly rather than calling a
/// `hasFailingFinding` predicate — that predicate (and the `Unannotated`
/// exemption it exists for) does not arrive until PR8b. The check is
/// behaviorally identical for scenarios 1-9: none of `Governance.fs`'s
/// PR8a-scoped finding kinds (`Orphan`/`Ghost`/`Missing`) are ever exempt
/// from failing, so "any finding exists" and "isEmpty is false" agree.
module RhinoCli.Tests.Unit.Steps.GovernanceSteps

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Governance

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type GovernanceSteps() =
    let mutable scenarioRootDir: string option = None
    let mutable currentDir: string option = None
    let mutable scanPathsOverride: string list option = None
    let mutable lastFindings: ReadmeIndexFinding list = []

    let scenarioRoot () : string =
        match scenarioRootDir with
        | Some dir -> dir
        | None ->
            let dir =
                Path.Combine(Path.GetTempPath(), "rhino-cli-governance-" + Guid.NewGuid().ToString("N"))

            Directory.CreateDirectory dir |> ignore
            scenarioRootDir <- Some dir
            dir

    /// The final path segment of a repo-realistic-looking label — see this
    /// module's doc comment for why only the basename is used.
    let basename (p: string) : string =
        let trimmed = p.TrimEnd('/')
        let idx = trimmed.LastIndexOf('/')
        if idx < 0 then trimmed else trimmed.Substring(idx + 1)

    let dirPrefix (p: string) : string =
        let trimmed = p.TrimEnd('/')
        let idx = trimmed.LastIndexOf('/')
        if idx < 0 then "" else trimmed.Substring(0, idx)

    let useScenarioRootAsScanPath () =
        scanPathsOverride <- Some [ scenarioRoot () ]

    /// Resolves the on-disk index-file path a `"..." links ...`/`"..." does
    /// not link ...` step's quoted source label refers to: relative to the
    /// already-established `currentDir` when one exists, or — for the one
    /// scenario with no prior `directory "..." contains ...` step — derives
    /// a fresh directory from the label's own prefix.
    let resolveIndexFile (label: string) : string =
        match currentDir with
        | Some dir -> Path.Combine(dir, basename label)
        | None ->
            let prefix = dirPrefix label

            let newRoot =
                Path.Combine(scenarioRoot (), (if prefix = "" then "root" else basename prefix))

            Directory.CreateDirectory newRoot |> ignore
            currentDir <- Some newRoot
            useScenarioRootAsScanPath ()
            Path.Combine(newRoot, basename label)

    let ensureLinkTarget (baseDir: string) (rawTarget: string) : unit =
        let cleaned = rawTarget.Replace('\\', '/')

        let cleaned =
            if cleaned.StartsWith("./", StringComparison.Ordinal) then
                cleaned.Substring(2)
            else
                cleaned

        if cleaned <> "" then
            let full = Path.Combine(baseDir, cleaned.Replace('/', Path.DirectorySeparatorChar))

            if cleaned.EndsWith("/README.md", StringComparison.Ordinal) then
                if not (File.Exists full) then
                    Directory.CreateDirectory(Path.GetDirectoryName(full: string)) |> ignore
                    File.WriteAllText(full, "# Stub\n")
            elif not (File.Exists full) then
                let dir = Path.GetDirectoryName(full: string)

                if not (String.IsNullOrEmpty dir) then
                    Directory.CreateDirectory dir |> ignore

                File.WriteAllText(full, "x\n")

    let writeLinks (label: string) (links: string list) : unit =
        let indexPath = resolveIndexFile label
        let dir = Path.GetDirectoryName(indexPath: string)
        links |> List.iter (ensureLinkTarget dir)
        let bullets = links |> List.mapi (fun i l -> sprintf "- [Item %d](%s)" i l)
        let content = "# Index\n\n" + String.Join("\n", bullets) + "\n"
        File.WriteAllText(indexPath, content)

    let runValidate () =
        let paths = scanPathsOverride |> Option.defaultValue (resolveScanPaths [])
        lastFindings <- auditReadmeIndex (scenarioRoot ()) paths

    // ---- Given: fixture construction ----

    [<Given>]
    member _.``directory "([^"]+)" contains "([^"]+)", "([^"]+)", "([^"]+)"``
        (dirLabel: string, f1: string, f2: string, f3: string)
        =
        let dir = Path.Combine(scenarioRoot (), basename dirLabel)
        Directory.CreateDirectory dir |> ignore

        [ f1; f2; f3 ]
        |> List.iter (fun f ->
            File.WriteAllText(Path.Combine(dir, f), (if f = "README.md" then "# Index\n" else "x\n")))

        currentDir <- Some dir
        useScenarioRootAsScanPath ()

    [<Given>]
    member _.``directory "([^"]+)" contains "([^"]+)"``(dirLabel: string, f1: string) =
        let dir = Path.Combine(scenarioRoot (), basename dirLabel)
        Directory.CreateDirectory dir |> ignore
        File.WriteAllText(Path.Combine(dir, f1), (if f1 = "README.md" then "# Index\n" else "x\n"))
        currentDir <- Some dir
        useScenarioRootAsScanPath ()

    [<Given>]
    member _.``directory "([^"]+)" contains "([^"]+)" and "([^"]+)"``(dirLabel: string, f1: string, f2: string) =
        let parent = currentDir |> Option.defaultValue (scenarioRoot ())
        let dir = Path.Combine(parent, basename dirLabel)
        Directory.CreateDirectory dir |> ignore

        [ f1; f2 ]
        |> List.iter (fun f -> File.WriteAllText(Path.Combine(dir, f), "x\n"))

    [<Given>]
    member _.``directory "([^"]+)" contains "([^"]+)" and no "([^"]+)"``
        (dirLabel: string, f1: string, _readme: string)
        =
        // The two "uncovered tree" fixtures always live outside DEFAULT_PATHS
        // — `scanPathsOverride` is deliberately left unset (see module doc
        // comment) so the shared validate `When` step falls back to
        // `resolveScanPaths []`.
        let dir =
            Path.Combine(scenarioRoot (), dirLabel.TrimEnd('/').Replace('/', Path.DirectorySeparatorChar))

        Directory.CreateDirectory dir |> ignore
        File.WriteAllText(Path.Combine(dir, f1), "x\n")
        currentDir <- Some dir

    [<Given>]
    member _.``directory "([^"]+)" contains (\d+) agent files``(dirLabel: string, count: int) =
        let dir =
            Path.Combine(scenarioRoot (), dirLabel.TrimEnd('/').Replace('/', Path.DirectorySeparatorChar))

        Directory.CreateDirectory dir |> ignore

        for i in 0 .. count - 1 do
            File.WriteAllText(Path.Combine(dir, sprintf "agent-%d.md" i), "x\n")

        currentDir <- Some dir

    [<Given>]
    member _.``it contains subdirectory "([^"]+)" containing "([^"]+)"``(subLabel: string, fileName: string) =
        let parent = currentDir |> Option.defaultValue (scenarioRoot ())
        let sub = Path.Combine(parent, basename subLabel)
        Directory.CreateDirectory sub |> ignore
        File.WriteAllText(Path.Combine(sub, fileName), (if fileName = "README.md" then "# Sub\n" else "x\n"))

    [<Given>]
    member _.``it contains no "([^"]+)"``(_name: string) = ()

    [<Given>]
    member _.``"([^"]+)" contains no "([^"]+)"``(_dirLabel: string, _name: string) = ()

    [<Given>]
    member _.``file "([^"]+)" exists``(path: string) =
        let dir = Path.Combine(scenarioRoot (), basename (dirPrefix path))
        Directory.CreateDirectory dir |> ignore
        File.WriteAllText(Path.Combine(dir, basename path), "# Ai Agents\n")
        currentDir <- Some dir
        // The split-directory's parent ("agents/") is itself the scan root
        // here — it is legitimately exempt from its own missing-README
        // check even though it holds indexable content (the split-index
        // file), matching `readme_index.rs::audit_one_dir`'s root-exemption
        // rationale ("a caller passes a covered-tree root deliberately").
        // The child directory under test is never exempt.
        scanPathsOverride <- Some [ dir ]

    [<Given>]
    member _.``"([^"]+)" links "([^"]+)" and "([^"]+)"``(label: string, l1: string, l2: string) =
        writeLinks label [ l1; l2 ]

    [<Given>]
    member _.``"([^"]+)" links "([^"]+)"``(label: string, l1: string) = writeLinks label [ l1 ]

    [<Given>]
    member _.``"([^"]+)" links "([^"]+)" only``(label: string, l1: string) = writeLinks label [ l1 ]

    [<Given>]
    member _.``"([^"]+)" does not link "([^"]+)"``(label: string, _target: string) =
        let indexPath = resolveIndexFile label
        File.WriteAllText(indexPath, "# Index\n\nNo links here.\n")

    [<Given>]
    member _.``it does not link "([^"]+)"``(_target: string) = ()

    // ---- When/Then: shared validate runner ----

    [<When>]
    member _.``the developer runs governance readme-index validate``() = runValidate ()

    [<Then>]
    member _.``the command exits successfully``() = Assert.True(List.isEmpty lastFindings)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.False(List.isEmpty lastFindings)

    [<Then>]
    member _.``the finding names "([^"]+)" as unindexed``(name: string) =
        Assert.True(
            lastFindings
            |> List.exists (fun f ->
                f.Kind = ReadmeIndexFindingKind.Orphan
                && (f.File.Contains name || f.Message.Contains name)),
            sprintf "expected an orphan finding naming %s: %A" name lastFindings
        )

    [<Then>]
    member _.``the finding reports a missing index for that directory``() =
        Assert.True(
            lastFindings |> List.exists (fun f -> f.Kind = ReadmeIndexFindingKind.Missing),
            sprintf "expected a missing-index finding: %A" lastFindings
        )

    [<AfterScenario>]
    member _.Cleanup() =
        match scenarioRootDir with
        | Some dir when Directory.Exists dir -> Directory.Delete(dir, true)
        | _ -> ()

/// Reads one named `Scenario:`/`Scenario Outline:` block out of the real,
/// frozen `governance-readme-index.feature` file (leaving the file itself
/// untouched) and runs it through TickSpec bound only against
/// `GovernanceSteps` — see `EnvStagedGuardSteps.fs`'s `FeatureRunner` for why
/// this is per-scenario rather than per-file, and why a `Scenario Outline`
/// runs every generated `Examples:` row.
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
                "governance",
                "governance-readme-index.feature"
            )
        )

    let private extractScenario (featureLines: string[]) (scenarioTitle: string) : string[] =
        let featureLine =
            featureLines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let startIdx =
            featureLines
            |> Array.findIndex (fun l ->
                let trimmed = l.Trim()

                trimmed = sprintf "Scenario: %s" scenarioTitle
                || trimmed = sprintf "Scenario Outline: %s" scenarioTitle)

        let endIdx =
            featureLines
            |> Array.skip (startIdx + 1)
            |> Array.tryFindIndex (fun l ->
                let trimmed = l.Trim()

                trimmed.StartsWith("Scenario:", StringComparison.Ordinal)
                || trimmed.StartsWith("Scenario Outline:", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    /// Runs every generated sub-scenario for `scenarioTitle`, bound against
    /// `GovernanceSteps`. A plain `Scenario:` generates exactly one; the
    /// `Scenario Outline:` generates one per `Examples:` row.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<GovernanceSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)

        for scenario in feature.Scenarios do
            scenario.Action.Invoke()

[<Fact>]
let ``A complete index passes`` () =
    FeatureRunner.run "A complete index passes"

[<Fact>]
let ``A missing sibling link fails`` () =
    FeatureRunner.run "A missing sibling link fails"

[<Fact>]
let ``A missing subdirectory README link fails`` () =
    FeatureRunner.run "A missing subdirectory README link fails"

[<Fact>]
let ``A missing README fails when siblings exist`` () =
    FeatureRunner.run "A missing README fails when siblings exist"

[<Fact>]
let ``The rule does not reach grandchildren`` () =
    FeatureRunner.run "The rule does not reach grandchildren"

[<Fact>]
let ``A split directory still needs its own README`` () =
    FeatureRunner.run "A split directory still needs its own README"

[<Fact>]
let ``A split directory whose parent omits a child fails`` () =
    FeatureRunner.run "A split directory whose parent omits a child fails"

[<Fact>]
let ``An uncovered tree is not scanned`` () =
    FeatureRunner.run "An uncovered tree is not scanned"

[<Fact>]
let ``A generated mirror directory is not scanned`` () =
    FeatureRunner.run "A generated mirror directory is not scanned"
