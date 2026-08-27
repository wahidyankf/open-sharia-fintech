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
