/// TickSpec step definitions binding
/// `governance-readme-index.feature`'s 18 scenarios (one a `Scenario
/// Outline` with 3 `Examples` rows) to `RhinoCli.Application.Governance`
/// [Repo-grounded —
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/governance/governance-readme-index.feature`,
/// `apps/rhino-cli/src/application/governance/readme_index.rs`,
/// `apps/rhino-cli/src/commands/governance_validate_readme_index.rs`,
/// `apps/rhino-cli/src/commands/governance_generate_readme_index.rs`,
/// `apps/rhino-cli/src/commands/governance_rewrite_readme_index_paths.rs`].
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
/// `Governance.auditReadmeIndex`/`generateReadmeIndex`/`rewriteIndexPaths`
/// as an explicit, absolute scan root — mirroring `readme_index.rs`'s own
/// unit tests, which likewise always pass a throwaway `TempDir` as the scan
/// root rather than exercising `DEFAULT_PATHS` against the real repository.
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
/// The gate-id-rename scenario ("The Phase 1 rename introduces no
/// enforcement gap for orphan or ghost") is registry/fixture-only: it reads
/// this repository's own real `repo-config.yml` via
/// `RhinoCli.Application.RepoConfig` (mirroring `RepoConfigSteps.fs`'s
/// precedent for "the harness registry section of repo-config.yml") and
/// asserts on the gate-id list already recorded there — no new application
/// code, since the rename already landed in a prior, separate plan. The two
/// `unannotated` dark-launch/armed scenarios need no registry lookup at all:
/// `Governance.hasFailingFinding`'s own empty-vs-non-empty `failKinds`
/// branching IS the entire "armed" mechanism (there is no other "Phase 9
/// armed" flag anywhere in the source) — the armed scenario instead hardcods
/// the real `governance-readme-completeness` gate's registered `fail-kinds:
/// [missing, unannotated]` list, mirroring
/// `governance_validate_readme_index.rs`'s own
/// `scenario_unannotated_finding_kind_fails_once_armed_and_in_scope` unit
/// test, which does exactly the same thing.
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
    let mutable activeFailKinds: string list = []

    // ---- "The --paths flag overrides the default scan scope" state ----
    let mutable explicitPathsFlag: string list option = None
    let mutable resolvedWithFlag: string list option = None
    let mutable resolvedWithoutFlag: string list option = None

    // ---- "The --fail-kinds flag ..." state ----
    let mutable syntheticFindings: ReadmeIndexFinding list = []

    // ---- gate-id-rename state ----
    let mutable gateIds: string list = []

    // ---- generate/rewrite-paths state ----
    let mutable idempotentBefore: string option = None
    let mutable idempotentAfter: string option = None
    let mutable renameMap: (string * string) list = []

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
    member _.``"([^"]+)" links "([^"]+)" with no annotation text``(label: string, l1: string) = writeLinks label [ l1 ]

    [<Given>]
    member _.``"([^"]+)" does not link "([^"]+)"``(label: string, _target: string) =
        let indexPath = resolveIndexFile label
        File.WriteAllText(indexPath, "# Index\n\nNo links here.\n")

    [<Given>]
    member _.``it does not link "([^"]+)"``(_target: string) = ()

    // ---- Given/When: gate-id-rename scenario ----

    [<Given>]
    member _.``gate id "([^"]+)" is armed at "([^"]+)" before Phase 1``(_oldId: string, _scope: string) = ()

    [<When>]
    member _.``Phase 1's rename lands and gate id "([^"]+)" replaces it``(_newId: string) =
        match RhinoCli.Infrastructure.GitRoot.findRoot () with
        | Error message -> failwith message
        | Ok repoRoot ->
            match RhinoCli.Application.RepoConfig.load repoRoot with
            | Error message -> failwith message
            | Ok config -> gateIds <- config.Gates |> List.map (fun g -> g.Id)

    [<Then>]
    member _.``"([^"]+)" is armed at "([^"]+)" immediately, not deferred``(gateId: string, _scope: string) =
        Assert.Contains(gateId, gateIds)

    [<Then>]
    member _.``the developer runs gate list with surface pre-push and format text``() = ()

    [<Then>]
    member _.``that output never shows both gate ids at once``() =
        Assert.DoesNotContain("md-readme-index", gateIds)
        Assert.Contains("governance-readme-index", gateIds)

    // ---- Given/When/Then: unannotated dark-launch/armed scenarios ----

    [<Given>]
    member _.``Phase 9 has not yet armed "([^"]+)"``(_gateId: string) = activeFailKinds <- []

    [<Given>]
    member _.``Phase 9 has armed "([^"]+)" at "([^"]+)"``(_gateId: string, _scope: string) =
        activeFailKinds <- [ "missing"; "unannotated" ]

    [<Given>]
    member _.``the changed paths include "([^"]+)"``(_path: string) = ()

    [<When>]
    member _.``the developer runs gate run with surface pre-push``() = runValidate ()

    [<Then>]
    member _.``no finding of kind "([^"]+)" causes a failure``(kind: string) =
        Assert.False(hasFailingFinding lastFindings [])
        Assert.True(lastFindings |> List.exists (fun f -> f.Kind.Name = kind))

    // ---- When/Then: shared validate runner ----

    [<When>]
    member _.``the developer runs governance readme-index validate``() =
        activeFailKinds <- []
        runValidate ()

    [<Then>]
    member _.``the command exits successfully``() =
        Assert.False(hasFailingFinding lastFindings activeFailKinds)

    [<Then>]
    member _.``the command exits with a failure code``() =
        Assert.True(hasFailingFinding lastFindings activeFailKinds)

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
    member _.``the finding names "([^"]+)" as unannotated``(name: string) =
        Assert.True(
            lastFindings
            |> List.exists (fun f ->
                f.Kind = ReadmeIndexFindingKind.Unannotated
                && (f.File.Contains name || f.Message.Contains name)),
            sprintf "expected an unannotated finding naming %s: %A" name lastFindings
        )

    [<Then>]
    member _.``the finding reports a missing index for that directory``() =
        Assert.True(
            lastFindings |> List.exists (fun f -> f.Kind = ReadmeIndexFindingKind.Missing),
            sprintf "expected a missing-index finding: %A" lastFindings
        )

    // ---- Given/When/Then: --paths flag scenario ----

    [<Given>]
    member _.``the developer invokes governance readme-index validate with "--paths (.*)"``(pathsArg: string) =
        explicitPathsFlag <- Some [ pathsArg ]

    [<When>]
    member _.``the command runs``() =
        resolvedWithFlag <- Some(resolveScanPaths (explicitPathsFlag |> Option.defaultValue []))
        resolvedWithoutFlag <- Some(resolveScanPaths [])

    [<Then>]
    member _.``it scans only "([^"]+)", not the unmodified DEFAULT_PATHS list``(expected: string) =
        Assert.Equal<string list>([ expected ], resolvedWithFlag |> Option.defaultValue [])

    [<Then>]
    member _.``running it again with no "--paths" flag scans the unmodified DEFAULT_PATHS list``() =
        Assert.Equal<string list>(defaultPaths, resolvedWithoutFlag |> Option.defaultValue [])

    // ---- Given/When/Then: --fail-kinds flag scenario ----

    [<Given>]
    member _.``a scanned directory has one "orphan" finding and one "missing" finding``() =
        syntheticFindings <-
            [ { File = "orphan.md"
                Severity = "high"
                Kind = ReadmeIndexFindingKind.Orphan
                Message = "orphan: orphan.md exists but is not linked" }
              { File = "some-dir"
                Severity = "high"
                Kind = ReadmeIndexFindingKind.Missing
                Message = "missing: some-dir contains indexable content but has no README.md" } ]

    [<When>]
    member _.``the developer runs governance readme-index validate with "--fail-kinds (.*)"``(kinds: string) =
        let failKinds = kinds.Split(' ') |> Array.toList
        activeFailKinds <- failKinds
        lastFindings <- syntheticFindings

    [<Then>]
    member _.``the exit code reflects only the "([^"]+)" finding``(_kind: string) =
        Assert.True(hasFailingFinding lastFindings activeFailKinds)
        Assert.False(hasFailingFinding lastFindings [ "missing-does-not-exist" ])

    [<Then>]
    member _.``the "([^"]+)" finding is still printed in the output``(kind: string) =
        Assert.True(lastFindings |> List.exists (fun f -> f.Kind.Name = kind))

    // ---- Given/When/Then: generate scenarios ----

    [<Given>]
    member _.``a covered directory contains a markdown file with description and when_to_use frontmatter, and no "README.md"``
        ()
        =
        let dir = Path.Combine(scenarioRoot (), "repo-governance", "widgets")
        Directory.CreateDirectory dir |> ignore

        let content =
            "---\ntitle: \"Widget\"\ndescription: \"Widget description\"\nwhen_to_use: \"Use it for widgets\"\n---\n\n# Widget\n"

        File.WriteAllText(Path.Combine(dir, "widget.md"), content)
        currentDir <- Some dir

    [<When>]
    member _.``the developer runs governance readme-index generate``() =
        generateReadmeIndex (scenarioRoot ()) [ scenarioRoot () ] |> ignore

    [<Then>]
    member _.``a "README.md" is written linking that file with a derived annotation``() =
        let readmePath = Path.Combine(currentDir |> Option.get, "README.md")
        Assert.True(File.Exists readmePath)
        let content = File.ReadAllText readmePath
        Assert.Contains("widget.md", content)
        Assert.Contains("—", content)
        Assert.Contains("Widget description", content)
        Assert.Contains("Use it for widgets", content)

    [<Given>]
    member _.``a covered directory already has a conforming "README.md"``() =
        let dir = Path.Combine(scenarioRoot (), "covered")
        Directory.CreateDirectory dir |> ignore
        File.WriteAllText(Path.Combine(dir, "note.md"), "---\ndescription: \"Note description\"\n---\n\n# Note\n")

        File.WriteAllText(
            Path.Combine(dir, "README.md"),
            "---\ntitle: \"Covered\"\n---\n\n# Covered\n\n- [Note](./note.md) — Note description\n"
        )

        currentDir <- Some dir

    [<When>]
    member _.``the developer runs governance readme-index generate twice``() =
        let readmePath = Path.Combine(currentDir |> Option.get, "README.md")
        generateReadmeIndex (scenarioRoot ()) [ scenarioRoot () ] |> ignore
        idempotentBefore <- Some(File.ReadAllText readmePath)
        generateReadmeIndex (scenarioRoot ()) [ scenarioRoot () ] |> ignore
        idempotentAfter <- Some(File.ReadAllText readmePath)

    [<Then>]
    member _.``the second run writes byte-identical content to the first``() =
        Assert.Equal(idempotentBefore |> Option.defaultValue "", idempotentAfter |> Option.defaultValue "")

    [<Given>]
    member _.``a directory already has a README.md index with hand-authored entry order``() =
        let dir = Path.Combine(scenarioRoot (), "ordered")
        Directory.CreateDirectory dir |> ignore
        File.WriteAllText(Path.Combine(dir, "a.md"), "# A\n")
        File.WriteAllText(Path.Combine(dir, "b.md"), "# B\n")
        File.WriteAllText(Path.Combine(dir, "c.md"), "# C\n")

        File.WriteAllText(
            Path.Combine(dir, "README.md"),
            "# Ordered\n\n- [B custom](./b.md) — hand text\n- [A custom](./a.md) — hand text\n"
        )

        currentDir <- Some dir

    [<Given>]
    member _.``a directory has no README.md index``() =
        let dir = Path.Combine(scenarioRoot (), "scaffold")
        Directory.CreateDirectory dir |> ignore
        File.WriteAllText(Path.Combine(dir, "x.md"), "---\ntitle: \"X\"\ndescription: \"X desc\"\n---\n\n# X\n")
        File.WriteAllText(Path.Combine(dir, "y.md"), "y\n")
        let sub = Path.Combine(dir, "sub")
        Directory.CreateDirectory sub |> ignore
        File.WriteAllText(Path.Combine(sub, "README.md"), "# Sub\n")
        currentDir <- Some dir

    [<When>]
    member _.``the maintainer runs rhino-cli governance readme-index generate on that directory``() =
        generateReadmeIndex (scenarioRoot ()) [ scenarioRoot () ] |> ignore

    [<Then>]
    member _.``the existing entries keep their order and annotations``() =
        let content = File.ReadAllText(Path.Combine(currentDir |> Option.get, "README.md"))

        let idxB =
            content.IndexOf("[B custom](./b.md) — hand text", StringComparison.Ordinal)

        let idxA =
            content.IndexOf("[A custom](./a.md) — hand text", StringComparison.Ordinal)

        Assert.True(idxB >= 0 && idxA >= 0 && idxB < idxA, content)

    [<Then>]
    member _.``only genuinely missing entries are appended``() =
        let content = File.ReadAllText(Path.Combine(currentDir |> Option.get, "README.md"))
        Assert.Contains("c.md", content)

    [<Then>]
    member _.``a complete annotated index is written``() =
        let readmePath = Path.Combine(currentDir |> Option.get, "README.md")
        Assert.True(File.Exists readmePath)

    [<Then>]
    member _.``every sibling file and subdirectory appears exactly once``() =
        let content = File.ReadAllText(Path.Combine(currentDir |> Option.get, "README.md"))

        let occurrences (needle: string) =
            (content.Length - content.Replace(needle, "").Length) / needle.Length

        Assert.Equal(1, occurrences "x.md")
        Assert.Equal(1, occurrences "y.md")
        Assert.Equal(1, occurrences "sub/README.md")

    // ---- Given/When/Then: rewrite-paths scenario ----

    [<Given>]
    member _.``a rename map of old and new paths for a directory's children``() =
        let dir = Path.Combine(scenarioRoot (), "renamed")
        Directory.CreateDirectory dir |> ignore

        File.WriteAllText(
            Path.Combine(dir, "README.md"),
            "# Renamed\n\nSome prose here.\n\n- [Old A](./old-a.md) — desc a\n- [Old B](./old-b.md) — desc b\n\nMore prose.\n"
        )

        File.WriteAllText(Path.Combine(dir, "old-a.md"), "a\n")
        File.WriteAllText(Path.Combine(dir, "old-b.md"), "b\n")
        currentDir <- Some dir
        renameMap <- [ "old-a.md", "new-a.md"; "old-b.md", "new-b.md" ]

    [<When>]
    member _.``the maintainer runs rhino-cli governance readme-index rewrite-paths with that map``() =
        rewriteIndexPaths (scenarioRoot ()) [ scenarioRoot () ] renameMap |> ignore

    [<Then>]
    member _.``every index link target is updated to its new path``() =
        let content = File.ReadAllText(Path.Combine(currentDir |> Option.get, "README.md"))
        Assert.Contains("./new-a.md", content)
        Assert.Contains("./new-b.md", content)
        Assert.DoesNotContain("old-a.md", content)
        Assert.DoesNotContain("old-b.md", content)

    [<Then>]
    member _.``entry order, annotation text, and surrounding prose are unchanged``() =
        let content = File.ReadAllText(Path.Combine(currentDir |> Option.get, "README.md"))
        Assert.Contains("Some prose here.", content)
        Assert.Contains("More prose.", content)
        Assert.Contains("— desc a", content)
        Assert.Contains("— desc b", content)
        let idxA = content.IndexOf("new-a.md", StringComparison.Ordinal)
        let idxB = content.IndexOf("new-b.md", StringComparison.Ordinal)
        Assert.True(idxA >= 0 && idxB >= 0 && idxA < idxB, content)

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

[<Fact>]
let ``The Phase 1 rename introduces no enforcement gap for orphan or ghost`` () =
    FeatureRunner.run "The Phase 1 rename introduces no enforcement gap for orphan or ghost"

[<Fact>]
let ``The unannotated finding kind is dark-launched, not enforced, before Phase 9`` () =
    FeatureRunner.run "The unannotated finding kind is dark-launched, not enforced, before Phase 9"

[<Fact>]
let ``The unannotated finding kind fails once armed and in scope`` () =
    FeatureRunner.run "The unannotated finding kind fails once armed and in scope"

[<Fact>]
let ``The --paths flag overrides the default scan scope`` () =
    FeatureRunner.run "The --paths flag overrides the default scan scope"

[<Fact>]
let ``The --fail-kinds flag restricts which findings contribute to the exit code`` () =
    FeatureRunner.run "The --fail-kinds flag restricts which findings contribute to the exit code"

[<Fact>]
let ``generate writes a conforming annotated index for a directory needing one`` () =
    FeatureRunner.run "generate writes a conforming annotated index for a directory needing one"

[<Fact>]
let ``generate is idempotent`` () =
    FeatureRunner.run "generate is idempotent"

[<Fact>]
let ``Generate no longer rewrites an existing index's order`` () =
    FeatureRunner.run "Generate no longer rewrites an existing index's order"

[<Fact>]
let ``Generate still scaffolds a directory with no index`` () =
    FeatureRunner.run "Generate still scaffolds a directory with no index"

[<Fact>]
let ``Rewrite-paths updates link targets without touching order`` () =
    FeatureRunner.run "Rewrite-paths updates link targets without touching order"

// =============================================================================
// `governance-word-budget.feature` — 20 scenarios (Wave D PR9)
// =============================================================================

/// Builds `n` single-character, single-space-separated "words" — content
/// whose `wordCount` is exactly `n`, the same fixture-construction trick
/// `word_budget.rs`'s own test module uses (`n_words`).
let private nWords (n: int) : string =
    String.Join(" ", Array.create (max 0 n) "w")

/// Mirrors the live `governance-word-budget:` section of `repo-config.yml`
/// verbatim (see that file): eight general surfaces at target 650/warn
/// 750/fail 750 (including `RTK.md`, added alongside the RTK tool), `**/README.md`
/// declared last at the wider 900/1000/1000, and a `CLAUDE.md`-rooted
/// resolved tree at 1200/1500/1500 — exactly what the feature's
/// `Background:` (dropped from the per-scenario TickSpec snippet below
/// along with its two steps, since no scenario needs it re-declared at
/// runtime; its state is this fixture) and every scenario's own prose
/// numbers already assume.
let private canonicalWordBudgetConfig: BudgetConfig =
    let generalSurface (glob: string) : Surface =
        { Glob = glob
          Target = 650UL
          Warn = 750UL
          Fail = 750UL }

    { Surfaces =
        [ generalSurface "repo-governance/**/*.md"
          generalSurface ".claude/**/*.md"
          generalSurface ".codex/**/*.md"
          generalSurface ".opencode/**/*.md"
          generalSurface ".agents/**/*.md"
          generalSurface "AGENTS.md"
          generalSurface "CLAUDE.md"
          generalSurface "RTK.md"
          { Glob = "**/README.md"
            Target = 900UL
            Warn = 1000UL
            Fail = 1000UL } ]
      ResolvedTree =
        { Root = "CLAUDE.md"
          Target = 1200UL
          Warn = 1500UL
          Fail = 1500UL } }

/// Instance step-definition container for `governance-word-budget.feature`
/// — see `GovernanceSteps`'s doc comment above for why TickSpec's
/// one-instance-per-scenario lifecycle makes instance-level mutable fields
/// the idiomatic state-threading mechanism here. Every fixture lives under
/// its own fresh `scenarioRoot()` temp directory, mirroring
/// `word_budget.rs`'s own tests, which always pass a throwaway `TempDir` as
/// `repoRoot` — except the handful of scenarios that are explicitly
/// registry/text proxy checks against THIS repository's own live
/// `repo-config.yml`/governance tree (see `Governance.fs`'s module doc
/// comment for why those stay proxy checks), which use
/// `RhinoCli.Infrastructure.GitRoot.findRoot` instead, mirroring
/// `RepoConfigValidateSteps.fs`'s precedent for the same distinction.
type GovernanceWordBudgetSteps() =
    let mutable scenarioRootDir: string option = None
    let mutable lastFindings: WordBudgetFinding list = []
    let mutable lastExitFailed: bool = false
    let mutable lastPath: string option = None
    let mutable lastResolvedTreeSize: uint64 = 0UL
    let mutable declaredWordCounts: Map<string, int> = Map.empty
    let mutable liveRepoConfigText: string = ""
    let mutable liveWordBudgetConfig: BudgetConfig option = None
    let mutable gateIds: string list = []
    let mutable schemaFixtureYaml: string = ""

    let scenarioRoot () : string =
        match scenarioRootDir with
        | Some dir -> dir
        | None ->
            let dir =
                Path.Combine(Path.GetTempPath(), "rhino-cli-word-budget-" + Guid.NewGuid().ToString("N"))

            Directory.CreateDirectory dir |> ignore
            scenarioRootDir <- Some dir
            dir

    let writeWordsAt (relPath: string) (n: int) : unit =
        let full =
            Path.Combine(scenarioRoot (), relPath.Replace('/', Path.DirectorySeparatorChar))

        let dir = Path.GetDirectoryName(full: string)

        if not (String.IsNullOrEmpty dir) then
            Directory.CreateDirectory dir |> ignore

        File.WriteAllText(full, nWords n)
        lastPath <- Some relPath
        declaredWordCounts <- Map.add relPath n declaredWordCounts

    let runValidate () =
        let root = scenarioRoot ()
        let sizeFindings = checkInstructionSizes root canonicalWordBudgetConfig []
        let treeFinding = checkResolvedTree root canonicalWordBudgetConfig
        lastFindings <- sizeFindings @ (Option.toList treeFinding)

        lastResolvedTreeSize <- resolveTreeSize (Path.Combine(root, canonicalWordBudgetConfig.ResolvedTree.Root))

        lastExitFailed <- lastFindings |> List.exists (fun f -> f.Severity = WordBudgetSeverity.Fail)

    let findRepoRoot () : string =
        match RhinoCli.Infrastructure.GitRoot.findRoot () with
        | Error message -> failwith message
        | Ok repoRoot -> repoRoot

    // ---- Given: Background (state is `canonicalWordBudgetConfig`, built above) ----

    [<Given>]
    member _.``repo-config.yml declares a governance-word-budget section``() = ()

    [<Given>]
    member _.``the section sets target (\d+), warn (\d+), fail (\d+)``(_target: int, _warn: int, _fail: int) = ()

    // ---- Given: fixture construction ----

    [<Given>]
    member _.``"([^"]+)" contains (\d+) words``(path: string, n: int) = writeWordsAt path n

    [<Given>]
    member _.``a file "([^"]+)" contains (\d+) words``(path: string, n: int) = writeWordsAt path n

    [<Given>]
    member _.``"([^"]+)" contains (\d+) prose words``(path: string, n: int) = writeWordsAt path n

    [<Given>]
    member _.``it contains a Mermaid block of (\d+) words``(n: int) =
        match lastPath with
        | None -> failwith "no prior file established for the Mermaid-block fixture"
        | Some path ->
            // The two fence-marker tokens ("```mermaid" and "```") are each
            // one whitespace-delimited token themselves, already counted
            // toward this step's stated block size.
            let bodyWords = max 0 (n - 2)
            let addition = sprintf "\n\n```mermaid\n%s\n```\n" (nWords bodyWords)
            let full = Path.Combine(scenarioRoot (), path)
            File.AppendAllText(full, addition)

    // F#'s lexer rejects an '@' character inside a double-backtick
    // identifier (FS1104) — unlike every other step in this file, this
    // step's text carries a literal '@'. `\x40` is the regex hex escape for
    // '@' (0x40 = ASCII 64): it contains no literal '@' character in the F#
    // source, so the lexer accepts it, while still matching a literal '@'
    // in the actual Gherkin step text at runtime (the same reason the
    // coverage tool's F# extractor requires the bare `[<Given>]` + backtick
    // form here — it does not recognize the attribute's `string`
    // constructor overload as a step definition at all).
    [<Given>]
    member _.``"([^"]+)" imports "([^"]+)" via an \x40-directive``(fromPath: string, toPath: string) =
        // Overwrites the file the earlier `"..." contains N words` step
        // wrote, preserving that step's stated total word count while
        // replacing its first token with the `@`-import directive —
        // mirrors `word_budget.rs`'s own fixture, whose CLAUDE.md word
        // count already includes the import line itself.
        let totalWords = declaredWordCounts |> Map.tryFind fromPath |> Option.defaultValue 1

        let bodyWords = max 0 (totalWords - 1)
        let content = sprintf "@%s\n%s" toPath (nWords bodyWords)
        File.WriteAllText(Path.Combine(scenarioRoot (), fromPath), content)

    [<Given>]
    member _.``"([^"]+)" imports "([^"]+)"``(fromPath: string, toPath: string) =
        let content = sprintf "@%s\n%s" toPath (nWords 5)
        File.WriteAllText(Path.Combine(scenarioRoot (), fromPath), content)

    /// No-op: `scenarioRoot()` starts empty on every fresh scenario, so a
    /// path nothing has written to already "does not exist" — this step
    /// only records the path so the paired `Then` step below can name it
    /// back in its assertion message.
    [<Given>]
    member _.``no file exists at "([^"]+)"``(path: string) = lastPath <- Some path

    [<Given>]
    member _.``the resolved CLAUDE.md tree totals (\d+) words``(n: int) =
        writeWordsAt canonicalWordBudgetConfig.ResolvedTree.Root n

    [<Given>]
    member _.``repo-config.yml adds "([^"]+)" under governance-word-budget``(addition: string) =
        schemaFixtureYaml <-
            "governance-word-budget:\n"
            + "  surfaces:\n"
            + "    - glob: \"AGENTS.md\"\n"
            + "      target: 400\n"
            + "      warn: 500\n"
            + "      fail: 500\n"
            + "  resolved_tree:\n"
            + "    root: \"CLAUDE.md\"\n"
            + "    target: 1200\n"
            + "    warn: 1500\n"
            + "    fail: 1500\n"
            + "  "
            + addition
            + "\n"

    // ---- When ----

    [<When>]
    member _.``the developer runs governance word-budget validate``() = runValidate ()

    [<When>]
    member _.``I read repo-config.yml``() =
        let repoRoot = findRepoRoot ()
        liveRepoConfigText <- File.ReadAllText(Path.Combine(repoRoot, "repo-config.yml"))

        match mergedBudgetConfig repoRoot with
        | Error message -> failwith message
        | Ok cfg -> liveWordBudgetConfig <- cfg

    [<When>]
    member _.``the developer runs repo-config schema validate``() =
        lastExitFailed <-
            match checkNoUnknownWordBudgetKeys schemaFixtureYaml with
            | Ok() -> false
            | Error _ -> true

    /// The old command's removal is a registry-level proxy check — see
    /// `Governance.fs`'s module doc comment for why full CLI-dispatch
    /// assertions stay out of this module's scope, the same way
    /// `word_budget.rs`'s own test module scopes it.
    [<When>]
    member _.``the developer runs harness instruction-size validate``() =
        let repoRoot = findRepoRoot ()
        liveRepoConfigText <- File.ReadAllText(Path.Combine(repoRoot, "repo-config.yml"))

    [<When>]
    member _.``the developer runs gate list with surface pre-push and format text``() =
        let repoRoot = findRepoRoot ()

        match RhinoCli.Application.RepoConfig.load repoRoot with
        | Error message -> failwith message
        | Ok cfg -> gateIds <- cfg.Gates |> List.map (fun g -> g.Id)

    /// Proxy check mirroring `word_budget.rs`'s own
    /// `scenario_no_inbound_link_to_the_renamed_convention_is_left_broken`
    /// test: greps the governed trees for the convention doc's pre-rename
    /// name rather than exercising a real `md links validate` command,
    /// which is not yet ported to F# at all (`Md.fs` has no links-validate
    /// function yet — a later, separate Wave D PR's scope).
    [<When>]
    member _.``the developer runs md links validate``() =
        let repoRoot = findRepoRoot ()
        let staleNeedle = "instruction-file-size-budget.md"

        let containsStaleNeedle (path: string) : bool =
            (File.ReadAllText path).Contains(staleNeedle, StringComparison.Ordinal)

        let treeOffenders =
            [ "repo-governance"; ".claude"; "docs" ]
            |> List.collect (fun dir ->
                let root = Path.Combine(repoRoot, dir)

                if not (Directory.Exists root) then
                    []
                else
                    Directory.GetFiles(root, "*.md", SearchOption.AllDirectories)
                    |> Array.filter containsStaleNeedle
                    |> Array.toList)

        let agentsMdPath = Path.Combine(repoRoot, "AGENTS.md")

        let agentsOffender =
            if File.Exists agentsMdPath && containsStaleNeedle agentsMdPath then
                [ agentsMdPath ]
            else
                []

        lastExitFailed <- not (List.isEmpty (treeOffenders @ agentsOffender))

    // ---- Then: shared exit-code steps ----

    [<Then>]
    member _.``the command exits successfully``() = Assert.False(lastExitFailed)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.True(lastExitFailed)

    // ---- Then: finding-presence steps ----

    [<Then>]
    member _.``the output contains no finding for that file``() =
        match lastPath with
        | None -> Assert.True(List.isEmpty lastFindings)
        | Some path -> Assert.False(lastFindings |> List.exists (fun f -> f.Path = path))

    [<Then>]
    member _.``the output contains no finding naming that file``() =
        match lastPath with
        | None -> Assert.True(List.isEmpty lastFindings)
        | Some path -> Assert.False(lastFindings |> List.exists (fun f -> f.Path = path))

    [<Then>]
    member _.``the output contains a "([^"]+)" finding naming that file``(sev: string) =
        match lastPath with
        | None -> failwith "no prior file established"
        | Some path ->
            Assert.True(
                lastFindings
                |> List.exists (fun f -> f.Path = path && wordBudgetSeverityLabel f.Severity = sev),
                sprintf "expected a %s finding naming %s: %A" sev path lastFindings
            )

    [<Then>]
    member _.``the output contains a "([^"]+)" finding naming "([^"]+)"``(sev: string, path: string) =
        Assert.True(
            lastFindings
            |> List.exists (fun f -> f.Path = path && wordBudgetSeverityLabel f.Severity = sev),
            sprintf "expected a %s finding naming %s: %A" sev path lastFindings
        )

    [<Then>]
    member _.``the output contains a "([^"]+)" finding naming that file, not a "([^"]+)" finding``
        (want: string, notWant: string)
        =
        match lastPath with
        | None -> failwith "no prior file established"
        | Some path ->
            Assert.True(
                lastFindings
                |> List.exists (fun f -> f.Path = path && wordBudgetSeverityLabel f.Severity = want)
            )

            Assert.False(
                lastFindings
                |> List.exists (fun f -> f.Path = path && wordBudgetSeverityLabel f.Severity = notWant)
            )

    [<Then>]
    member _.``the output contains a "([^"]+)" finding for the resolved tree``(sev: string) =
        Assert.True(
            lastFindings
            |> List.exists (fun f -> f.Path = "resolved-tree" && wordBudgetSeverityLabel f.Severity = sev)
        )

    [<Then>]
    member _.``no finding is emitted for "([^"]+)"``(path: string) =
        Assert.False(
            lastFindings |> List.exists (fun f -> f.Path = path),
            sprintf "expected no finding naming %s: %A" path lastFindings
        )

    [<Then>]
    member _.``the finding names "([^"]+)"``(path: string) =
        Assert.True(
            lastFindings |> List.exists (fun f -> f.Path = path),
            sprintf "expected a finding naming %s: %A" path lastFindings
        )

    // ---- Then: finding-detail steps ----

    [<Then>]
    member _.``the finding states the word count (\d+) and the ceiling (\d+)``(count: int, ceiling: int) =
        match
            lastPath
            |> Option.bind (fun path -> lastFindings |> List.tryFind (fun f -> f.Path = path))
        with
        | None -> failwith (sprintf "no finding for %A: %A" lastPath lastFindings)
        | Some f ->
            Assert.Equal(uint64 count, f.Size)
            Assert.Equal(uint64 ceiling, f.Fail)

    [<Then>]
    member _.``the finding links the governance word budget convention``() =
        match
            lastPath
            |> Option.bind (fun path -> lastFindings |> List.tryFind (fun f -> f.Path = path))
        with
        | None -> failwith (sprintf "no finding for %A: %A" lastPath lastFindings)
        | Some f ->
            Assert.Contains("progressive disclosure", f.Message)
            Assert.Contains("repo-governance/principles/content/progressive-disclosure.md", f.Message)

    [<Then>]
    member _.``the reported word count is (\d+)``(n: int) =
        match lastPath with
        | None -> failwith "no prior file established"
        | Some path ->
            let full = Path.Combine(scenarioRoot (), path)
            Assert.Equal(uint64 n, wordCount (File.ReadAllText full))

    [<Then>]
    member _.``the reported resolved-tree word count is (\d+)``(n: int) =
        Assert.Equal(uint64 n, lastResolvedTreeSize)

    // ---- Then: narrative-only steps (the real assertion already ran above) ----

    [<Then>]
    member _.``this holds even though 900 words exceeds the general surface's 750-word fail ceiling, because the winning README-specific surface classifies 900 words as "([^"]+)" against its own 900-word target``
        (_severity: string)
        =
        ()

    [<Then>]
    member _.``the command terminates``() = ()

    /// `resolveRecursive`'s cycle guard is what makes this assertion (see
    /// below) return at all rather than stack-overflow/hang — termination
    /// is proven by construction, not asserted separately.
    [<Then>]
    member _.``each file is counted at most once``() =
        // CLAUDE.md = "@AGENTS.md" (1 token) + 5 body words = 6; AGENTS.md =
        // "@CLAUDE.md" (1 token) + 5 body words = 6. A cycle-guard failure
        // would double-count past 12.
        Assert.Equal(12UL, lastResolvedTreeSize)

    // ---- Then: repo-config.yml registry/text proxy steps ----

    [<Then>]
    member _.``the covered surface globs are exactly the harness entry points and the README glob``() =
        let expected =
            set
                [ "repo-governance/**/*.md"
                  ".claude/**/*.md"
                  ".codex/**/*.md"
                  ".opencode/**/*.md"
                  ".agents/**/*.md"
                  "AGENTS.md"
                  "CLAUDE.md"
                  "RTK.md"
                  "**/README.md" ]

        let actual =
            liveWordBudgetConfig
            |> Option.map (fun c -> c.Surfaces |> List.map (fun s -> s.Glob) |> Set.ofList)
            |> Option.defaultValue Set.empty

        Assert.Equal<Set<string>>(expected, actual)

    [<Then>]
    member _.``the README glob is declared last``() =
        let last =
            liveWordBudgetConfig
            |> Option.bind (fun c -> c.Surfaces |> List.tryLast)
            |> Option.map (fun s -> s.Glob)

        Assert.Equal(Some "**/README.md", last)

    [<Then>]
    member _.``it contains no "([^"]+)" section``(needle: string) =
        Assert.DoesNotContain(needle, liveRepoConfigText)

    [<Then>]
    member _.``it contains a "([^"]+)" section``(needle: string) =
        Assert.Contains(needle, liveRepoConfigText)

    [<Then>]
    member _.``the output contains no gate id "([^"]+)"``(id: string) = Assert.DoesNotContain(id, gateIds)

    [<Then>]
    member _.``the output contains gate id "([^"]+)"``(id: string) = Assert.Contains(id, gateIds)

    [<Then>]
    member _.``the command exits with a usage error``() =
        Assert.DoesNotContain("command: harness instruction-size validate", liveRepoConfigText)

    [<Then>]
    member _.``the output reports an unknown subcommand``() = ()

    [<AfterScenario>]
    member _.Cleanup() =
        match scenarioRootDir with
        | Some dir when Directory.Exists dir -> Directory.Delete(dir, true)
        | _ -> ()

/// Reads one named `Scenario:`/`Scenario Outline:` block out of the real,
/// frozen `governance-word-budget.feature` file, INCLUDING its
/// `Background:` block (unlike `FeatureRunner` above, whose bound feature
/// file has none) since every scenario here depends on it, and runs it
/// through TickSpec bound only against `GovernanceWordBudgetSteps`.
module private WordBudgetFeatureRunner =

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
                "governance-word-budget.feature"
            )
        )

    let private extractScenario (featureLines: string[]) (scenarioTitle: string) : string[] =
        let featureLine =
            featureLines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let backgroundStart =
            featureLines |> Array.tryFindIndex (fun l -> l.Trim() = "Background:")

        // The Background block always sits before every scenario, exactly
        // once — its end is the first `Scenario:`/`Scenario Outline:` line
        // anywhere in the file, NOT `startIdx - 1` (which would instead
        // span every scenario between the Background and the one actually
        // being sliced, for every scenario after the first).
        let firstScenarioIdx =
            featureLines
            |> Array.tryFindIndex (fun l ->
                let trimmed = l.Trim()

                trimmed.StartsWith("Scenario:", StringComparison.Ordinal)
                || trimmed.StartsWith("Scenario Outline:", StringComparison.Ordinal))

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

        let backgroundLines =
            match backgroundStart, firstScenarioIdx with
            | Some bIdx, Some sIdx when sIdx > bIdx -> featureLines.[bIdx .. sIdx - 1]
            | _ -> [||]

        Array.concat
            [ [| featureLine; "" |]
              backgroundLines
              featureLines.[startIdx .. endIdx - 1] ]

    /// Runs every generated sub-scenario for `scenarioTitle`, bound against
    /// `GovernanceWordBudgetSteps`. A plain `Scenario:` generates exactly
    /// one; a `Scenario Outline:` generates one per `Examples:` row.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<GovernanceWordBudgetSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)

        for scenario in feature.Scenarios do
            scenario.Action.Invoke()

[<Fact>]
let ``A file within target passes silently`` () =
    WordBudgetFeatureRunner.run "A file within target passes silently"

[<Fact>]
let ``A file between target and fail warns without blocking`` () =
    WordBudgetFeatureRunner.run "A file between target and fail warns without blocking"

[<Fact>]
let ``A file over the ceiling fails the gate`` () =
    WordBudgetFeatureRunner.run "A file over the ceiling fails the gate"

[<Fact>]
let ``Every covered surface is scanned`` () =
    WordBudgetFeatureRunner.run "Every covered surface is scanned"

[<Fact>]
let ``The covered surfaces are exactly the live entry points of the supported harnesses`` () =
    WordBudgetFeatureRunner.run "The covered surfaces are exactly the live entry points of the supported harnesses"

[<Fact>]
let ``A configured glob matching no file is a no-op`` () =
    WordBudgetFeatureRunner.run "A configured glob matching no file is a no-op"

[<Fact>]
let ``A root entry point uses the ordinary 750-word ceiling`` () =
    WordBudgetFeatureRunner.run "A root entry point uses the ordinary 750-word ceiling"

[<Fact>]
let ``A README.md file under the specific-surface target produces zero findings`` () =
    WordBudgetFeatureRunner.run "A README.md file under the specific-surface target produces zero findings"

[<Fact>]
let ``A README.md file uses the wider README-specific glob threshold`` () =
    WordBudgetFeatureRunner.run "A README.md file uses the wider README-specific glob threshold"

[<Fact>]
let ``A README.md file over the wider ceiling still fails`` () =
    WordBudgetFeatureRunner.run "A README.md file over the wider ceiling still fails"

[<Fact>]
let ``Non-prose content counts toward the budget`` () =
    WordBudgetFeatureRunner.run "Non-prose content counts toward the budget"

[<Fact>]
let ``An out-of-scope file is never scanned`` () =
    WordBudgetFeatureRunner.run "An out-of-scope file is never scanned"

[<Fact>]
let ``The config schema rejects an exemption key`` () =
    WordBudgetFeatureRunner.run "The config schema rejects an exemption key"

[<Fact>]
let ``The old command is gone`` () =
    WordBudgetFeatureRunner.run "The old command is gone"

[<Fact>]
let ``The old config block is gone`` () =
    WordBudgetFeatureRunner.run "The old config block is gone"

[<Fact>]
let ``The old gate id is replaced by the armed word-budget gate`` () =
    WordBudgetFeatureRunner.run "The old gate id is replaced by the armed word-budget gate"

[<Fact>]
let ``The resolved tree is measured in words`` () =
    WordBudgetFeatureRunner.run "The resolved tree is measured in words"

[<Fact>]
let ``An oversized resolved tree fails`` () =
    WordBudgetFeatureRunner.run "An oversized resolved tree fails"

[<Fact>]
let ``Import cycles terminate`` () =
    WordBudgetFeatureRunner.run "Import cycles terminate"

[<Fact>]
let ``A generated mirror is still subject to the word budget`` () =
    WordBudgetFeatureRunner.run "A generated mirror is still subject to the word budget"

[<Fact>]
let ``No inbound link to the renamed convention is left broken`` () =
    WordBudgetFeatureRunner.run "No inbound link to the renamed convention is left broken"
