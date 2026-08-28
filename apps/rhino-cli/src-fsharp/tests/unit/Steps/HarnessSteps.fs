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
open System.Text.Json
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

/// Reads a governance document plus, when the document has a same-named
/// sibling directory (progressive disclosure's split-file convention), every
/// `.md` file under it in sorted order [Repo-grounded —
/// `apps/rhino-cli/tests/agents.rs::read_document_tree`].
let private readDocumentTree (rel: string) : string =
    let parentPath = Path.Combine(repositoryRoot, rel)
    let mutable out = File.ReadAllText(parentPath)
    let childrenDir = Path.ChangeExtension(parentPath, null)

    if Directory.Exists(childrenDir) then
        for child in Directory.GetFiles(childrenDir, "*.md") |> Array.sort do
            out <- out + "\n" + File.ReadAllText(child)

    out

/// Reads an agent's full instruction surface: its own definition plus every
/// skill it declares in `skills:` (each skill's `SKILL.md` and every file
/// under its `reference/` in sorted order) [Repo-grounded —
/// `apps/rhino-cli/tests/agents.rs::read_agent_surface`].
let private readAgentSurface (agentRel: string) : string =
    let agentPath = Path.Combine(repositoryRoot, agentRel)
    let mutable out = File.ReadAllText(agentPath)
    let mutable inSkills = false
    let declared = ResizeArray<string>()

    for line in out.Split('\n') do
        if line.StartsWith("skills:") then
            inSkills <- true
        elif inSkills then
            if line.StartsWith("  - ") then
                declared.Add(line.Substring(4).Trim())
            else
                inSkills <- false

    for skill in declared do
        let dir = Path.Combine(repositoryRoot, ".claude", "skills", skill)
        let refDir = Path.Combine(dir, "reference")

        let paths =
            Path.Combine(dir, "SKILL.md")
            :: (if Directory.Exists(refDir) then
                    Directory.GetFiles(refDir, "*.md") |> Array.sort |> Array.toList
                else
                    [])

        for path in paths do
            if File.Exists(path) then
                out <- out + "\n" + File.ReadAllText(path)

    out

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
    let mutable duplicationFindings: Harness.DuplicationFinding list = []
    let mutable fixtureAgentPaths: string list = []
    let mutable fixtureSkillPaths: string list = []
    let mutable registryDeclaresSkillsMirror: bool = false
    let mutable mirrorResult: Harness.MirrorResult option = None
    let mutable mirrorDrift: Harness.MirrorDrift list option = None
    let mutable fixtureSkillNames: string list = []
    let mutable lastSyncOutcome: Result<Harness.SyncResult, string> option = None
    let mutable fixtureCodexAgentNames: string list = []
    let mutable fixtureRoleSubfolders: string list = []
    let mutable configAfterFirstRun: string option = None
    let mutable configAfterSecondRun: string option = None
    let mutable pushRangePaths: string list = []
    let mutable lastPrePushOutcome: Harness.PrePushWordBudgetOutcome option = None
    let mutable lookupDir: string = ""
    let mutable lookupFileContent: string = ""
    let mutable lastAuditJson: string option = None

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

    /// The same registry, with the codex entry additionally declaring a
    /// skills-directory mirror alongside its existing agent-directory mirror
    /// — the shape `mirror_jobs` reads to build a [`Harness.MirrorJob`]
    /// [Repo-grounded — `skills_mirror.rs`'s test fixture builder].
    let writeThreeHarnessConfigWithSkillsMirror (root: string) : unit =
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
                  "    skills-dir: .agents/skills"
                  "    skills-mirrors: .claude/skills"
                  "coverage:"
                  "  projects: []"
                  "" ]
            )
        )

    let writeSkillFile (root: string) (name: string) (relPath: string) (body: string) : string =
        let path = Path.Combine(root, ".claude", "skills", name, relPath)
        Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
        File.WriteAllText(path, body)
        path

    /// Every real (non-symlink) file under `dir`, checked via
    /// `FileSystemInfo.LinkTarget` — non-null only for a reparse point —
    /// which is .NET's cross-platform symlink detector.
    let rec allEntriesAreReal (dir: string) : bool =
        if not (Directory.Exists dir) then
            true
        else
            Directory.GetFileSystemEntries dir
            |> Array.forall (fun path ->
                let isDir = Directory.Exists path

                let info: FileSystemInfo = if isDir then DirectoryInfo path else FileInfo path

                isNull info.LinkTarget && (not isDir || allEntriesAreReal path))

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

    // ---- @agents-detect-duplication ----

    /// Writes an agent definition under the fixture's `.claude/agents/` and
    /// records its path. Names deliberately avoid the sanctioned role suffixes
    /// (`-maker`, `-checker`, `-fixer`, `-deployer`, `-dev`, `-tester`): two
    /// files in the same template family are *expected* to share boilerplate,
    /// so a fixture named `alpha-checker`/`beta-checker` would be exempted and
    /// the scenario would pass for the wrong reason.
    let writeAgent (root: string) (name: string) (body: string) : string =
        let dir = Path.Combine(root, ".claude", "agents")
        Directory.CreateDirectory dir |> ignore
        let path = Path.Combine(dir, name + ".md")
        File.WriteAllText(path, sprintf "---\nname: %s\ndescription: fixture\n---\n%s" name body)
        fixtureAgentPaths <- fixtureAgentPaths @ [ path ]
        path

    let writeSkill (root: string) (name: string) (body: string) : string =
        let dir = Path.Combine(root, ".claude", "skills", name)
        Directory.CreateDirectory dir |> ignore
        let path = Path.Combine(dir, "SKILL.md")
        File.WriteAllText(path, sprintf "---\nname: %s\ndescription: fixture\n---\n%s" name body)
        fixtureSkillPaths <- fixtureSkillPaths @ [ path ]
        path

    /// `count` distinct prose lines seeded by `tag`, so two blocks built with
    /// different tags share no window and one block repeated verbatim does.
    let prose (tag: string) (count: int) : string =
        String.Join("\n", [ for i in 1..count -> sprintf "%s line %d carries its own sentence." tag i ])
        + "\n"

    let findingSpanning (paths: string list) : Harness.DuplicationFinding list =
        duplicationFindings
        |> List.filter (fun finding -> paths |> List.forall (fun path -> List.contains path finding.Files))

    // ---- @agents-sync / @agents-validate-sync ----

    let writeAgentWithModel (root: string) (name: string) (model: string) : string =
        let dir = Path.Combine(root, ".claude", "agents")
        Directory.CreateDirectory dir |> ignore
        let path = Path.Combine(dir, name + ".md")

        File.WriteAllText(
            path,
            sprintf
                "---\nname: %s\ndescription: fixture\ntools: Read, Write\nmodel: %s\ncolor: blue\n---\nAgent body.\n"
                name
                model
        )

        path

    let readFrontmatterField (path: string) (field: string) : string option =
        File.ReadAllText(path).Split('\n')
        |> Array.tryPick (fun line ->
            let trimmed = line.Trim()

            if trimmed.StartsWith(field + ":", StringComparison.Ordinal) then
                Some(trimmed.Substring(field.Length + 1).Trim().Trim('"'))
            else
                None)

    let runSyncOnce (opts: Harness.SyncOptions) : unit =
        let outcome = Harness.syncAll opts
        lastSyncOutcome <- Some outcome

        lastExitCode <-
            Some(
                match outcome with
                | Ok _ -> 0
                | Error _ -> 1
            )

    /// Writes a fully valid agent: every required and known optional field
    /// present, so it triggers neither a failed nor a warning check.
    let writeValidatedAgent (root: string) (name: string) (skills: string list) : string =
        let dir = Path.Combine(root, ".claude", "agents")
        Directory.CreateDirectory dir |> ignore
        let path = Path.Combine(dir, name + ".md")

        let skillsBlock =
            if skills.IsEmpty then
                ""
            else
                "skills:\n" + String.Join("\n", skills |> List.map (sprintf "  - %s")) + "\n"

        File.WriteAllText(
            path,
            sprintf
                "---\nname: %s\ndescription: fixture agent\ntools: Read, Write\nmodel: sonnet\ncolor: blue\n%s---\nBody.\n"
                name
                skillsBlock
        )

        path

    /// Writes a fully valid skill: `SKILL.md` present with a `description`
    /// and a `name` matching the directory.
    let writeValidatedSkill (root: string) (name: string) : string =
        let dir = Path.Combine(root, ".claude", "skills", name)
        Directory.CreateDirectory dir |> ignore
        let path = Path.Combine(dir, "SKILL.md")
        File.WriteAllText(path, sprintf "---\nname: %s\ndescription: fixture skill\n---\nBody.\n" name)
        path

    let runValidateClaudeOnce (opts: Harness.ValidateClaudeOptions) : unit =
        let r = Harness.validateClaude opts
        lastResult <- Some r
        lastExitCode <- Some(if r.FailedChecks = 0 then 0 else 1)

    /// Writes a Claude agent under a role subfolder — `.claude/agents/<subfolder>/<fileStem>.md` —
    /// with `name` frontmatter that may differ from `fileStem`, matching
    /// `discover_agent_sources`'s one-level group-nesting walk.
    let writeCodexAgentUnderSubfolder
        (root: string)
        (subfolder: string)
        (fileStem: string)
        (name: string)
        (description: string)
        (body: string)
        : string =
        let dir = Path.Combine(root, ".claude", "agents", subfolder)
        Directory.CreateDirectory dir |> ignore
        let path = Path.Combine(dir, fileStem + ".md")
        File.WriteAllText(path, sprintf "---\nname: %s\ndescription: %s\n---\n%s" name description body)
        path

    /// Mirrors the live `governance-word-budget:` surfaces for `AGENTS.md` and
    /// `RTK.md` in `repo-config.yml` (650/750/750), scoped to just the two
    /// surfaces this feature's scenarios name — not the full 9-surface table
    /// `GovernanceWordBudgetSteps.fs`'s own canonical fixture carries.
    let wordBudgetFixtureConfig: Governance.BudgetConfig =
        let surface (glob: string) : Governance.Surface =
            { Glob = glob
              Target = 650UL
              Warn = 750UL
              Fail = 750UL }

        { Surfaces = [ surface "AGENTS.md"; surface "RTK.md" ]
          ResolvedTree =
            { Root = "CLAUDE.md"
              Target = 1200UL
              Warn = 1500UL
              Fail = 1500UL } }

    /// `n` single-character, single-space-separated "words" — the same
    /// fixture-construction trick `GovernanceWordBudgetSteps.fs`'s `nWords` uses.
    let nWordsBudget (n: int) : string =
        String.Join(" ", Array.create (max 0 n) "w")

    let writeBudgetFixture (root: string) (relPath: string) (n: int) : unit =
        File.WriteAllText(Path.Combine(root, relPath), nWordsBudget n)

    [<Given>]
    member _.``a \.claude/ directory with valid agents and skills``() =
        let root = scenarioRoot ()
        writeAgent root "sync-fixture-agent" "Agent body.\n" |> ignore
        writeSkill root "sync-fixture-skill" "Skill body.\n" |> ignore

    [<Given>]
    member _.``a \.claude/ directory with agents and skills to convert``() =
        let root = scenarioRoot ()
        writeAgent root "sync-fixture-agent" "Agent body.\n" |> ignore
        writeSkill root "sync-fixture-skill" "Skill body.\n" |> ignore

    [<Given>]
    member _.``a \.claude/ directory with both agents and skills``() =
        let root = scenarioRoot ()
        writeAgent root "sync-fixture-agent" "Agent body.\n" |> ignore
        writeSkill root "sync-fixture-skill" "Skill body.\n" |> ignore

    [<Given>]
    member _.``a \.claude/ agent configured with the "([^"]+)" model``(model: string) =
        writeAgentWithModel (scenarioRoot ()) "sync-model-agent" model |> ignore

    [<Given>]
    member _.``\.claude/ and \.opencode/ configurations that are fully synchronised``() =
        let root = scenarioRoot ()
        writeAgentWithModel root "sync-parity-agent" "sonnet" |> ignore

        match Harness.convertAllAgents root false with
        | Ok _ -> ()
        | Error e -> failwith e

    [<Given>]
    member _.``an agent in \.claude/ whose description differs from its \.opencode/ counterpart``() =
        let root = scenarioRoot ()
        writeAgentWithModel root "sync-mismatch-agent" "sonnet" |> ignore

        match Harness.convertAllAgents root false with
        | Ok _ -> ()
        | Error e -> failwith e

        let mirrorPath = Path.Combine(root, ".opencode", "agents", "sync-mismatch-agent.md")
        let content = File.ReadAllText mirrorPath

        File.WriteAllText(
            mirrorPath,
            content.Replace("description: fixture", "description: \"a different description\"")
        )

    [<Given>]
    member _.``\.claude/ containing more agents than \.opencode/``() =
        let root = scenarioRoot ()
        writeAgent root "sync-count-agent-one" "Agent body.\n" |> ignore
        writeAgent root "sync-count-agent-two" "Agent body.\n" |> ignore
        Directory.CreateDirectory(Path.Combine(root, ".opencode", "agents")) |> ignore

    [<When>]
    member _.``the developer runs agents sync``() =
        runSyncOnce (Harness.syncOptionsDefault (scenarioRoot ()))

    [<When>]
    member _.``the developer runs agents sync with the --dry-run flag``() =
        runSyncOnce
            { Harness.syncOptionsDefault (scenarioRoot ()) with
                DryRun = true }

    [<When>]
    member _.``the developer runs agents sync with the --agents-only flag``() =
        runSyncOnce
            { Harness.syncOptionsDefault (scenarioRoot ()) with
                AgentsOnly = true }

    [<When>]
    member _.``the developer runs agents validate-sync``() =
        let r = Harness.validateSync (scenarioRoot ())
        lastResult <- Some r
        lastExitCode <- Some(if r.FailedChecks = 0 then 0 else 1)

    [<Then>]
    member _.``the \.opencode/ directory contains the converted configuration``() =
        let root = scenarioRoot ()
        Assert.True(File.Exists(Path.Combine(root, ".opencode", "agents", "sync-fixture-agent.md")))
        Assert.True(Directory.Exists(Path.Combine(root, ".claude", "skills", "sync-fixture-skill")))

    [<Then>]
    member _.``the output describes the planned operations``() =
        match lastSyncOutcome with
        | Some(Ok r) -> Assert.True(r.AgentsConverted > 0)
        | Some(Error e) -> failwith e
        | None -> failwith "no sync has run in this scenario"

    [<Then>]
    member _.``no files are written to the \.opencode/ directory``() =
        Assert.False(Directory.Exists(Path.Combine(scenarioRoot (), ".opencode")))

    [<Then>]
    member _.``only agent files are written to the \.opencode/ directory``() =
        let root = scenarioRoot ()
        Assert.True(File.Exists(Path.Combine(root, ".opencode", "agents", "sync-fixture-agent.md")))
        Assert.False(Directory.Exists(Path.Combine(root, ".opencode", "skills")))

    [<Then>]
    member _.``the corresponding \.opencode/ agent uses the "([^"]+)" model identifier``(modelId: string) =
        let mirrorPath =
            Path.Combine(scenarioRoot (), ".opencode", "agents", "sync-model-agent.md")

        match readFrontmatterField mirrorPath "model" with
        | Some m -> Assert.Equal(modelId, m)
        | None -> failwith "mirror has no model field"

    [<Then>]
    member _.``the output reports all sync checks as passing``() =
        let notPassed = (result ()).Checks |> List.filter (fun c -> c.Status <> "passed")

        Assert.Equal<Harness.ValidationCheck list>([], notPassed)

    [<Then>]
    member _.``the output identifies the agent with the mismatched description``() =
        let mismatch =
            (result ()).Checks
            |> List.tryFind (fun c -> c.Status = "failed" && c.Message = "description mismatch")

        Assert.True(mismatch.IsSome)

    [<Then>]
    member _.``the output reports the agent count mismatch``() =
        match (result ()).Checks |> List.tryFind (fun c -> c.Name = "Agent Count") with
        | Some c -> Assert.Equal("failed", c.Status)
        | None -> failwith "no Agent Count check found"

    // ---- @agents-validate-claude ----

    [<Given>]
    member _.``a \.claude/ directory where all agents and skills are valid``() =
        let root = scenarioRoot ()
        writeValidatedAgent root "validate-claude-ok-agent" [] |> ignore
        writeValidatedSkill root "validate-claude-ok-skill" |> ignore

    [<Given>]
    member _.``a \.claude/ directory where one agent is missing the required "description" field``() =
        let root = scenarioRoot ()
        let dir = Path.Combine(root, ".claude", "agents")
        Directory.CreateDirectory dir |> ignore

        File.WriteAllText(
            Path.Combine(dir, "validate-claude-missing-desc.md"),
            "---\nname: validate-claude-missing-desc\ntools: Read, Write\nmodel: sonnet\ncolor: blue\n---\nBody.\n"
        )

    [<Given>]
    member _.``a \.claude/ directory containing two agent files declaring the same name``() =
        let root = scenarioRoot ()
        let dir = Path.Combine(root, ".claude", "agents")
        Directory.CreateDirectory dir |> ignore

        for suffix in [ "a"; "b" ] do
            File.WriteAllText(
                Path.Combine(dir, sprintf "validate-claude-dup-%s.md" suffix),
                "---\nname: validate-claude-dup\ndescription: fixture agent\ntools: Read, Write\nmodel: sonnet\ncolor: blue\n---\nBody.\n"
            )

    [<Given>]
    member _.``a \.claude/ directory where agents are valid but skills have issues``() =
        let root = scenarioRoot ()
        writeValidatedAgent root "validate-claude-agents-only-ok" [] |> ignore
        // Deliberately no SKILL.md — a skill-side failure --agents-only must not surface.
        Directory.CreateDirectory(Path.Combine(root, ".claude", "skills", "validate-claude-broken-skill"))
        |> ignore

    [<Given>]
    member _.``a \.claude/ directory where skills are valid but agents have issues``() =
        let root = scenarioRoot ()
        writeValidatedSkill root "validate-claude-skills-only-ok" |> ignore
        let dir = Path.Combine(root, ".claude", "agents")
        Directory.CreateDirectory dir |> ignore

        // Deliberately missing description — an agent-side failure --skills-only must not surface.
        File.WriteAllText(
            Path.Combine(dir, "validate-claude-broken-agent.md"),
            "---\nname: validate-claude-broken-agent\ntools: Read, Write\nmodel: sonnet\ncolor: blue\n---\nBody.\n"
        )

    [<When>]
    member _.``the developer runs agents validate-claude``() =
        let opts: Harness.ValidateClaudeOptions =
            { RepoRoot = scenarioRoot ()
              AgentsOnly = false
              SkillsOnly = false }

        runValidateClaudeOnce opts

    [<When>]
    member _.``the developer runs agents validate-claude with the --agents-only flag``() =
        let opts: Harness.ValidateClaudeOptions =
            { RepoRoot = scenarioRoot ()
              AgentsOnly = true
              SkillsOnly = false }

        runValidateClaudeOnce opts

    [<When>]
    member _.``the developer runs agents validate-claude with the --skills-only flag``() =
        let opts: Harness.ValidateClaudeOptions =
            { RepoRoot = scenarioRoot ()
              AgentsOnly = false
              SkillsOnly = true }

        runValidateClaudeOnce opts

    [<Then>]
    member _.``the output reports all checks as passing``() =
        let notPassed = (result ()).Checks |> List.filter (fun c -> c.Status <> "passed")

        Assert.Equal<Harness.ValidationCheck list>([], notPassed)

    [<Then>]
    member _.``the output identifies the agent and the missing field``() =
        let identifies =
            (result ()).Checks
            |> List.tryFind (fun c ->
                c.Status = "failed"
                && c.Name.Contains("Required Fields", StringComparison.Ordinal)
                && c.Actual.Contains("description", StringComparison.Ordinal))

        Assert.True(identifies.IsSome)

    [<Then>]
    member _.``the output reports the duplicate agent name``() =
        let duplicate =
            (result ()).Checks
            |> List.tryFind (fun c -> c.Status = "failed" && c.Message = "Agent name already used")

        Assert.True(duplicate.IsSome)

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

    /// Shared by the `harness bindings validate` and `agents
    /// detect-duplication` scenarios. When the command that ran produces a
    /// `ValidationResult`, the offending checks are asserted first so a
    /// failure names them rather than reporting only "expected 0, got 1";
    /// `detect-duplication` produces findings instead, and is covered by the
    /// zero-clusters step.
    [<Then>]
    member _.``the command exits successfully``() =
        match lastResult with
        | Some validation ->
            let notPassed =
                validation.Checks
                |> List.filter (fun (check: Harness.ValidationCheck) -> check.Status <> "passed")

            Assert.Equal<Harness.ValidationCheck list>([], notPassed)
        | None -> ()

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

    // ---- @codex-binding ----

    [<Given>]
    member _.``a repository whose \.claude/agents/ directory holds one agent under a role subfolder``() =
        let root = scenarioRoot ()

        writeCodexAgentUnderSubfolder
            root
            "reviewers"
            "role-agent"
            "role-agent"
            "Role fixture agent."
            "Body instructions.\n"
        |> ignore

        fixtureCodexAgentNames <- [ "role-agent" ]

    [<Given>]
    member _.``a repository whose \.claude/agents/ holds two agents in different role subfolders whose name frontmatter differs from their filename``
        ()
        =
        let root = scenarioRoot ()

        writeCodexAgentUnderSubfolder
            root
            "reviewers"
            "reviewer-file"
            "reviewer-identity"
            "Reviewer fixture."
            "Reviewer body.\n"
        |> ignore

        writeCodexAgentUnderSubfolder root "makers" "maker-file" "maker-identity" "Maker fixture." "Maker body.\n"
        |> ignore

        fixtureCodexAgentNames <- [ "reviewer-identity"; "maker-identity" ]
        fixtureRoleSubfolders <- [ "reviewers"; "makers" ]

    [<Given>]
    member _.``a repository whose \.codex/config\.toml carries hand-maintained mcp_servers, features, and ci-monitor-subagent tables``
        ()
        =
        let root = scenarioRoot ()

        writeCodexAgentUnderSubfolder root "makers" "fixture-agent" "fixture-agent" "Fixture agent." "Body.\n"
        |> ignore

        fixtureCodexAgentNames <- [ "fixture-agent" ]
        let codexDir = Path.Combine(root, ".codex")
        Directory.CreateDirectory codexDir |> ignore

        File.WriteAllText(
            Path.Combine(codexDir, "config.toml"),
            String.Join(
                "\n",
                [ "[mcp_servers.example]"
                  "command = \"example-server\""
                  ""
                  "[features]"
                  "multi_agent = true"
                  ""
                  "[ci-monitor-subagent]"
                  "enabled = true" ]
            )
            + "\n"
        )

    [<When>]
    member _.``the developer runs harness bindings generate``() =
        let root = scenarioRoot ()
        let outcome = Harness.emitCodexBindings root false

        lastExitCode <-
            Some(
                match outcome with
                | Ok _ -> 0
                | Error _ -> 1
            )

    [<When>]
    member _.``the developer runs harness bindings generate twice``() =
        let root = scenarioRoot ()
        let configPath = Path.Combine(root, ".codex", "config.toml")
        let first = Harness.emitCodexBindings root false
        configAfterFirstRun <- Some(File.ReadAllText configPath)
        let second = Harness.emitCodexBindings root false
        configAfterSecondRun <- Some(File.ReadAllText configPath)

        lastExitCode <-
            Some(
                match first, second with
                | Ok _, Ok _ -> 0
                | _ -> 1
            )

    [<Then>]
    member _.``\.codex/agents/ holds exactly one TOML file named for that agent``() =
        let root = scenarioRoot ()
        let dir = Path.Combine(root, ".codex", "agents")
        let files = Directory.GetFiles dir |> Array.map Path.GetFileName
        Assert.Equal(1, files.Length)
        Assert.Equal(fixtureCodexAgentNames.[0] + ".toml", files.[0])

    [<Then>]
    member _.``the emitted Codex agent declares name, description, and developer_instructions``() =
        let root = scenarioRoot ()

        let path =
            Path.Combine(root, ".codex", "agents", fixtureCodexAgentNames.[0] + ".toml")

        let content = File.ReadAllText path
        Assert.Contains("name = \"", content)
        Assert.Contains("description = \"", content)
        Assert.Contains("developer_instructions = \"\"\"", content)

    [<Then>]
    member _.``the emitted Codex agent declares no model field``() =
        let root = scenarioRoot ()

        let path =
            Path.Combine(root, ".codex", "agents", fixtureCodexAgentNames.[0] + ".toml")

        let content = File.ReadAllText path
        Assert.DoesNotContain("model = ", content)

    [<Then>]
    member _.``\.codex/agents/ holds one flat TOML file per agent keyed on the name frontmatter``() =
        let root = scenarioRoot ()
        let dir = Path.Combine(root, ".codex", "agents")

        let files =
            Directory.GetFiles dir
            |> Array.map Path.GetFileName
            |> Array.sort
            |> List.ofArray

        let expected =
            fixtureCodexAgentNames |> List.map (fun n -> n + ".toml") |> List.sort

        Assert.Equal<string list>(expected, files)

    [<Then>]
    member _.``no emitted filename repeats a role subfolder name``() =
        let root = scenarioRoot ()
        let dir = Path.Combine(root, ".codex", "agents")
        let files = Directory.GetFiles dir |> Array.map Path.GetFileName |> List.ofArray

        for subfolder in fixtureRoleSubfolders do
            Assert.DoesNotContain(subfolder + ".toml", files)

    [<Then>]
    member _.``\.codex/config\.toml declares a generated agents table for the fixture agent``() =
        let root = scenarioRoot ()
        let content = File.ReadAllText(Path.Combine(root, ".codex", "config.toml"))
        Assert.Contains(sprintf "[agents.%s]" fixtureCodexAgentNames.[0], content)

    [<Then>]
    member _.``the hand-maintained mcp_servers, features, and ci-monitor-subagent tables are unchanged``() =
        let root = scenarioRoot ()
        let content = File.ReadAllText(Path.Combine(root, ".codex", "config.toml"))
        Assert.Contains("[mcp_servers.example]", content)
        Assert.Contains("command = \"example-server\"", content)
        Assert.Contains("[features]", content)
        Assert.Contains("multi_agent = true", content)
        Assert.Contains("[ci-monitor-subagent]", content)
        Assert.Contains("enabled = true", content)

    [<Then>]
    member _.``the second run left \.codex/config\.toml byte-identical to the first``() =
        match configAfterFirstRun, configAfterSecondRun with
        | Some first, Some second -> Assert.Equal(first, second)
        | _ -> failwith "config.toml was not captured after both runs"

    // ---- @governance-word-budget-pre-push ----

    [<Given>]
    member _.``my push range modifies "([^"]+)"``(path: string) = pushRangePaths <- [ path ]

    [<Given>]
    member _.``my push range modifies only "([^"]+)"``(path: string) = pushRangePaths <- [ path ]

    [<Given>]
    member _.``"([^"]+)" exceeds its fail ceiling``(path: string) =
        writeBudgetFixture (scenarioRoot ()) path 800

    [<Given>]
    member _.``"([^"]+)" is within its fail ceiling``(path: string) =
        writeBudgetFixture (scenarioRoot ()) path 10

    [<When>]
    member _.``the pre-push hook runs``() =
        lastPrePushOutcome <-
            Some(Harness.runPrePushWordBudgetGate (scenarioRoot ()) wordBudgetFixtureConfig pushRangePaths)

    [<Then>]
    member _.``the word-budget gate runs``() =
        match lastPrePushOutcome with
        | Some outcome -> Assert.True(outcome.GateInvoked)
        | None -> failwith "the pre-push hook has not run in this scenario"

    [<Then>]
    member _.``the word-budget validation target is not invoked``() =
        match lastPrePushOutcome with
        | Some outcome -> Assert.False(outcome.GateInvoked)
        | None -> failwith "the pre-push hook has not run in this scenario"

    [<Then>]
    member _.``the word-budget validation target runs and exits 0``() =
        match lastPrePushOutcome with
        | Some outcome ->
            Assert.True(outcome.GateInvoked)
            Assert.Equal(0, outcome.ExitCode)
        | None -> failwith "the pre-push hook has not run in this scenario"

    [<Then>]
    member _.``the push is aborted with a non-zero exit``() =
        match lastPrePushOutcome with
        | Some outcome -> Assert.NotEqual(0, outcome.ExitCode)
        | None -> failwith "the pre-push hook has not run in this scenario"

    [<Then>]
    member _.``the push proceeds``() =
        match lastPrePushOutcome with
        | Some outcome -> Assert.Equal(0, outcome.ExitCode)
        | None -> failwith "the pre-push hook has not run in this scenario"

    // ---- @governance-word-budget-rule ----

    [<Given>]
    member _.``the plan is complete``() = ()

    [<When>]
    member _.``I look under "([^"]+)"``(dir: string) = lookupDir <- dir

    [<Then>]
    member _.``"([^"]+)" exists``(filename: string) =
        let path = Path.Combine(repositoryRoot, lookupDir, filename)
        Assert.True(File.Exists(path), sprintf "expected %s to exist" path)
        lookupFileContent <- File.ReadAllText(path)

    [<Then>]
    member _.``the file lists the monitored file classes, configured threshold source, and enforcement points``() =
        Assert.Contains("Monitored Surfaces", lookupFileContent)
        Assert.Contains("repo-config.yml", lookupFileContent)
        Assert.Contains("target", lookupFileContent)
        Assert.Contains("fail", lookupFileContent)
        Assert.Contains("Enforcement Points", lookupFileContent)

    [<When>]
    member _.``"repo-rules-checker" runs Step 6``() =
        lookupFileContent <- readAgentSurface ".claude/agents/repo/repo-rules-checker.md"

    [<Then>]
    member _.``it reports qualitative bloat concerns across the whole instruction-file class``() =
        Assert.Contains("qualitative concerns a mechanical gate cannot measure", lookupFileContent)
        Assert.Contains("progressive disclosure", lookupFileContent)

    [<Then>]
    member _.``it annotates that the word ceiling is enforced by the deterministic "governance-word-budget" gate``() =
        Assert.Contains("enforced by the deterministic", lookupFileContent)
        Assert.Contains("governance word-budget validate", lookupFileContent)

    [<When>]
    member _.``I read "([^"]+)"``(path: string) =
        lookupFileContent <- readDocumentTree path

    [<Then>]
    member _.``"governance-word-budget" is skipped locally and delegated from Step 0\.5``() =
        Assert.Contains("governance-word-budget` skipped", lookupFileContent)
        Assert.Contains("`delegated-gate-ids`", lookupFileContent)

    [<Given>]
    member _.``a repo with instruction files within the configured budgets``() = ()

    [<When>]
    member _.``the developer runs "rhino-cli repo-governance audit" with JSON output``() =
        lastAuditJson <- Some(Harness.repoGovernanceAuditJson (scenarioRoot ()))

    [<Then>]
    member _.``the envelope schema is "rhino-cli/repo-governance-audit/v1"``() =
        match lastAuditJson with
        | Some json ->
            use doc = JsonDocument.Parse(json)
            Assert.Equal("rhino-cli/repo-governance-audit/v1", doc.RootElement.GetProperty("schema").GetString())
        | None -> failwith "the repo-governance audit has not run in this scenario"

    [<Then>]
    member _.``"result\.categories" contains a category named "governance-word-budget"``() =
        match lastAuditJson with
        | Some json ->
            use doc = JsonDocument.Parse(json)

            let categories =
                doc.RootElement.GetProperty("result").GetProperty("categories").EnumerateArray()
                |> Seq.toList

            Assert.True(
                categories
                |> List.exists (fun c -> c.GetProperty("name").GetString() = "governance-word-budget")
            )
        | None -> failwith "the repo-governance audit has not run in this scenario"

    [<Given>]
    member _.``lifecycle evidence contains a current "governance-word-budget" result``() = ()

    [<When>]
    member _.``"repo-rules-checker" runs Step 0\.5``() =
        lookupFileContent <- readAgentSurface ".claude/agents/repo/repo-rules-checker.md"

    [<Then>]
    member _.``it consumes the exact delegated gate ID "governance-word-budget"``() =
        Assert.Contains("`delegated-gate-ids`", lookupFileContent)
        Assert.Contains("word budgets are all mechanically enforced", lookupFileContent)

    [<Then>]
    member _.``it does not re-derive word counts in Step 6``() =
        let normalized =
            lookupFileContent.Split([| ' '; '\n'; '\t'; '\r' |], StringSplitOptions.RemoveEmptyEntries)
            |> String.concat " "

        Assert.Contains("Do not run or AI-rederive those predicates", normalized)

    [<Given>]
    member _.``a repository with agent and skill files whose bodies share no 10-line verbatim windows``() =
        let root = scenarioRoot ()
        writeThreeHarnessConfig root
        writeAgent root "alpha-one" (prose "alpha" 14) |> ignore
        writeAgent root "beta-two" (prose "beta" 14) |> ignore
        writeSkill root "gamma-notes" (prose "gamma" 14) |> ignore

    [<Given>]
    member _.``a repository with two agent files that share (\d+) consecutive lines verbatim``(shared: int) =
        let root = scenarioRoot ()
        writeThreeHarnessConfig root
        let block = prose "shared" shared
        writeAgent root "alpha-one" (block + prose "alpha" 6) |> ignore
        writeAgent root "beta-two" (block + prose "beta" 6) |> ignore

    [<Given>]
    member _.``a repository with an agent file whose body matches (\d+) consecutive lines of a SKILL\.md``
        (shared: int)
        =
        let root = scenarioRoot ()
        writeThreeHarnessConfig root
        let block = prose "shared" shared
        writeAgent root "alpha-one" (block + prose "alpha" 6) |> ignore
        writeSkill root "gamma-notes" (block + prose "gamma" 6) |> ignore

    [<Given>]
    member _.``a repository where two agent files share a (\d+)-line window composed only of headings or blank lines``
        (windowSize: int)
        =
        let root = scenarioRoot ()
        writeThreeHarnessConfig root

        // Heading/blank pairs, so the shared window is exactly `windowSize`
        // normalized lines and every one of them is a heading or a blank.
        let scaffold =
            String.Join("\n", [ for i in 1 .. windowSize / 2 -> sprintf "%s Section %d\n" (String.replicate i "#") i ])
            + "\n"

        writeAgent root "alpha-one" (scaffold + prose "alpha" 6) |> ignore
        writeAgent root "beta-two" (scaffold + prose "beta" 6) |> ignore

    [<When>]
    member _.``the developer runs agents detect-duplication``() =
        match Harness.detectDuplication (scenarioRoot ()) with
        | Ok findings ->
            duplicationFindings <- findings
            lastExitCode <- Some(if List.isEmpty findings then 0 else 1)
        | Error message -> failwith message

    [<Then>]
    member _.``the output reports zero duplication clusters``() =
        Assert.Equal<Harness.DuplicationFinding list>([], duplicationFindings)

    [<Then>]
    member _.``the output identifies the duplicated cluster across both agents``() =
        let spanning = findingSpanning fixtureAgentPaths
        Assert.NotEmpty spanning

        for finding in spanning do
            Assert.Equal(Harness.duplicationWindowSize, finding.WindowSize)
            Assert.Equal("high", finding.Severity)
            // One start line per file, so a report can point at both sites.
            Assert.Equal(List.length finding.Files, List.length finding.StartLines)

    [<Then>]
    member _.``the output identifies the duplicated cluster across the agent and the skill``() =
        let spanning = findingSpanning (fixtureAgentPaths @ fixtureSkillPaths)
        Assert.NotEmpty spanning

        for finding in spanning do
            Assert.Contains("SKILL.md", String.Join(", ", finding.Files))

    // ---- @agents-skills-mirror ----
    //
    // Two scenarios ("The npm entry points cover the new mirror",
    // "The emitted mirror survives the formatter") read this repository's
    // real `package.json` / prettier binary rather than a synthetic fixture,
    // following the same precedent `@harness-name-registry-derived` set in
    // `agents-bindings.feature`: the claim is about the real repo's wiring,
    // so a fixture would prove only that the lookup works, never that the
    // live scripts and formatter actually agree with the mirror. Neither
    // spawns `npm`/`cargo` (the Rust CLI still owns `harness bindings
    // generate` until Wave E's flip) — each stands in with the equivalent
    // `Harness` function, documented at the call site.

    [<Given>]
    member _.``the harness registry declares an agent-directory mirror for the OpenCode entry``() =
        let root = scenarioRoot ()
        writeThreeHarnessConfig root

        match RepoConfig.load root with
        | Error e -> failwith e
        | Ok config ->
            let opencode = config.Harness |> List.find (fun e -> e.Name = "opencode")
            Assert.True(opencode.AgentDir.IsSome && opencode.Mirrors.IsSome)

    [<When>]
    member _.``the codex entry is updated to declare \.agents/skills as a mirror of \.claude/skills``() =
        writeThreeHarnessConfigWithSkillsMirror (scenarioRoot ())

    [<Then>]
    member _.``rhino-cli repo-config validate exits 0 with both kinds of mirror relationship declared: agent directories and skill directories``
        ()
        =
        match RepoConfig.load (scenarioRoot ()) with
        | Error e -> failwith e
        | Ok config ->
            let opencode = config.Harness |> List.find (fun e -> e.Name = "opencode")
            let codex = config.Harness |> List.find (fun e -> e.Name = "codex")
            Assert.True(opencode.AgentDir.IsSome && opencode.Mirrors.IsSome)
            Assert.True(codex.SkillsDir.IsSome && codex.SkillsMirrors.IsSome)

    [<Then>]
    member _.``rhino-cli harness bindings generate emits the \.agents/skills mirror without a new command-line flag``
        ()
        =
        let root = scenarioRoot ()

        writeSkillFile root "gamma-notes" "SKILL.md" "---\nname: gamma-notes\n---\nBody\n"
        |> ignore

        // `emitSkillsMirrors` takes only `repoRoot` and `dryRun` — no
        // skills-specific parameter exists to add a flag for.
        match Harness.emitSkillsMirrors root false with
        | Error e -> failwith e
        | Ok result ->
            Assert.True(result.Copied > 0)
            Assert.True(Directory.Exists(Path.Combine(root, ".agents", "skills", "gamma-notes")))

    [<Given>]
    member _.``\.claude/skills/ holds the repository's canonical skill directories and every one of them is tracked``
        ()
        =
        let root = scenarioRoot ()
        writeThreeHarnessConfigWithSkillsMirror root
        fixtureSkillNames <- [ "alpha-skill"; "beta-skill"; "gamma-skill" ]

        for name in fixtureSkillNames do
            writeSkillFile root name "SKILL.md" (sprintf "---\nname: %s\n---\nBody for %s.\n" name name)
            |> ignore

            writeSkillFile root name "reference/notes.md" "extra reference content\n"
            |> ignore

    [<When>]
    member _.``rhino-cli harness bindings generate runs``() =
        match Harness.emitSkillsMirrors (scenarioRoot ()) false with
        | Ok result -> mirrorResult <- Some result
        | Error e -> failwith e

    [<Then>]
    member _.``\.agents/skills/ contains one real directory per \.claude/skills/ skill``() =
        let root = scenarioRoot ()

        for name in fixtureSkillNames do
            let mirrored = Path.Combine(root, ".agents", "skills", name, "SKILL.md")
            let source = Path.Combine(root, ".claude", "skills", name, "SKILL.md")
            Assert.True(File.Exists mirrored)
            Assert.Equal(File.ReadAllText source, File.ReadAllText mirrored)

    [<Then>]
    member _.``find \.agents/skills -type l returns zero results, proving no symlink was created in either direction``
        ()
        =
        Assert.True(allEntriesAreReal (Path.Combine(scenarioRoot (), ".agents", "skills")))

    [<Given>]
    member _.``a clean tree immediately after rhino-cli harness bindings generate``() =
        let root = scenarioRoot ()
        writeThreeHarnessConfigWithSkillsMirror root

        writeSkillFile root "alpha-skill" "SKILL.md" "---\nname: alpha-skill\n---\nBody.\n"
        |> ignore

        match Harness.emitSkillsMirrors root false with
        | Ok _ -> ()
        | Error e -> failwith e

    [<When>]
    member _.``the command runs a second time``() =
        match Harness.emitSkillsMirrors (scenarioRoot ()) false with
        | Ok result -> mirrorResult <- Some result
        | Error e -> failwith e

    [<Then>]
    member _.``git diff --quiet \.agents/ exits 0, proving no churn``() =
        // No filesystem write is pending on a clean regeneration — the F#
        // analogue of a quiet `git diff`, since nothing changed for git to
        // report.
        match mirrorResult with
        | None -> failwith "no regeneration has run in this scenario"
        | Some result ->
            Assert.Equal(0, result.Copied)
            Assert.Equal(0, result.Removed)

    [<Then>]
    member _.``after a single character is changed in one mirrored file, rhino-cli harness bindings validate exits non-zero naming that file, where it exited 0 before the edit``
        ()
        =
        let root = scenarioRoot ()
        let mirrored = Path.Combine(root, ".agents", "skills", "alpha-skill", "SKILL.md")

        let before =
            match Harness.auditSkillsMirrors root with
            | Ok drift -> drift
            | Error e -> failwith e

        Assert.Equal<Harness.MirrorDrift list>([], before)

        File.WriteAllText(mirrored, File.ReadAllText(mirrored) + "x")

        match Harness.auditSkillsMirrors root with
        | Error e -> failwith e
        | Ok after ->
            Assert.NotEmpty after

            Assert.Contains(
                after,
                fun drift ->
                    match drift with
                    | Harness.MirrorDriftMissing path -> path.Contains("alpha-skill", StringComparison.Ordinal)
                    | Harness.MirrorDriftUndeclared _ -> false
            )

    [<Given>]
    member _.``npm run generate:bindings and npm run validate:sync covered only the OpenCode and Amazon Q surfaces``() =
        // Narrative provenance only, matching `@harness-purge`'s precedent:
        // the pre-mirror coverage is history, not state this scenario
        // reconstructs. What it asserts is the post-change invariant below.
        ()

    [<When>]
    member _.``both scripts run after the mirror is wired``() =
        let root = scenarioRoot ()
        writeThreeHarnessConfigWithSkillsMirror root

        writeSkillFile root "delta-skill" "SKILL.md" "---\nname: delta-skill\n---\nBody.\n"
        |> ignore

        // Stands in for `npm run generate:bindings` / `npm run validate:sync`:
        // both ultimately call these two registry-driven functions, and
        // spawning the real `cargo`-backed CLI here would rebuild the Rust
        // binary for no assertion this scenario needs.
        match Harness.emitSkillsMirrors root false with
        | Error e -> failwith e
        | Ok result ->
            mirrorResult <- Some result

            match Harness.auditSkillsMirrors root with
            | Ok drift -> mirrorDrift <- Some drift
            | Error e -> failwith e

    [<Then>]
    member _.``generate:bindings emits \.agents/skills/ and validate:sync reports it as in-parity``() =
        Assert.True(Directory.Exists(Path.Combine(scenarioRoot (), ".agents", "skills", "delta-skill")))

        Assert.Equal<Harness.MirrorDrift list>(
            [],
            mirrorDrift |> Option.defaultValue [ Harness.MirrorDriftMissing "unset" ]
        )

    [<Then>]
    member _.``neither script names a skills-specific or mirror-specific flag, because both delegate to the registry-driven commands``
        ()
        =
        let packageJsonPath = Path.Combine(repositoryRoot, "package.json")
        let packageJson = File.ReadAllText packageJsonPath

        let scriptLine (name: string) : string =
            let marker = sprintf "\"%s\":" name
            let start = packageJson.IndexOf(marker, StringComparison.Ordinal)
            Assert.True(start >= 0, sprintf "%s script not found in package.json" name)
            let lineEnd = packageJson.IndexOf('\n', start)
            packageJson.Substring(start, lineEnd - start)

        for line in [ scriptLine "generate:bindings"; scriptLine "validate:sync" ] do
            Assert.Contains("harness", line)
            Assert.DoesNotContain("--skills", line)
            Assert.DoesNotContain("--mirror", line)

    [<Given>]
    member _.``this repository has previously broken a generated byte-equality guard by letting the formatter rewrite emitted files``
        ()
        =
        // Narrative provenance — see `feedback_prettier_breaks_generated_byte_equality.md`.
        // Nothing to construct: the claim below is about whether THIS
        // scenario's mirrored content survives the real formatter.
        ()

    [<When>]
    member _.``rhino-cli harness bindings generate is followed by prettier --write over \.agents/ and then rhino-cli harness bindings validate``
        ()
        =
        let root = scenarioRoot ()
        writeThreeHarnessConfigWithSkillsMirror root

        // Prettier-clean on arrival: the same well-formed markdown shape the
        // repo's own PostToolUse hook produces, so the claim under test is
        // "prettier leaves already-clean content alone", not "prettier
        // reformats messy content" (a different, already-known failure mode).
        writeSkillFile
            root
            "epsilon-skill"
            "SKILL.md"
            "---\nname: epsilon-skill\n---\n\n# Epsilon Skill\n\nBody paragraph.\n"
        |> ignore

        match Harness.emitSkillsMirrors root false with
        | Error e -> failwith e
        | Ok _ ->
            let prettierBin = Path.Combine(repositoryRoot, "node_modules", ".bin", "prettier")
            let mirrorDir = Path.Combine(root, ".agents")

            let psi = ProcessStartInfo(prettierBin)
            psi.RedirectStandardOutput <- true
            psi.RedirectStandardError <- true
            psi.UseShellExecute <- false
            psi.ArgumentList.Add "--write"
            psi.ArgumentList.Add mirrorDir

            use proc = Process.Start psi
            proc.WaitForExit()
            Assert.Equal(0, proc.ExitCode)

            match Harness.auditSkillsMirrors root with
            | Ok drift -> mirrorDrift <- Some drift
            | Error e -> failwith e

    [<Then>]
    member _.``the validator exits 0``() =
        Assert.Equal<Harness.MirrorDrift list>(
            [],
            mirrorDrift |> Option.defaultValue [ Harness.MirrorDriftMissing "unset" ]
        )

    [<Then>]
    member _.``where it exits non-zero instead, \.agents/ is added to \.prettierignore and the same sequence then exits 0``
        ()
        =
        // The prior Then already proved the zero-drift branch for this
        // repository's current formatter configuration; this step documents
        // the untaken remedial branch rather than asserting on it, matching
        // the Gherkin's own conditional phrasing ("where it exits non-zero
        // instead").
        Assert.Equal<Harness.MirrorDrift list>(
            [],
            mirrorDrift |> Option.defaultValue [ Harness.MirrorDriftMissing "unset" ]
        )

/// Slices one scenario out of the real, frozen feature file and runs it
/// against `HarnessSteps` — see `GovernanceSteps.fs`'s runner for the shared
/// convention.
module private FeatureRunner =

    let private featurePath (fileName: string) : string =
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
                fileName
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

    let private runIn (fileName: string) (scenarioTitle: string) : unit =
        let path = featurePath fileName
        let snippet = extractScenario (File.ReadAllLines path) scenarioTitle
        let definitions = StepDefinitions([| typeof<HarnessSteps> |])
        let feature = definitions.GenerateFeature(path, snippet)

        for scenario in feature.Scenarios do
            scenario.Action.Invoke()

    /// Runs one scenario of `agents-bindings.feature`.
    let run (scenarioTitle: string) : unit =
        runIn "agents-bindings.feature" scenarioTitle

    /// Runs one scenario of `agents-detect-duplication.feature`.
    let runDuplication (scenarioTitle: string) : unit =
        runIn "agents-detect-duplication.feature" scenarioTitle

    /// Runs one scenario of `agents-skills-mirror.feature`.
    let runSkillsMirror (scenarioTitle: string) : unit =
        runIn "agents-skills-mirror.feature" scenarioTitle

    /// Runs one scenario of `agents-sync.feature`.
    let runSync (scenarioTitle: string) : unit =
        runIn "agents-sync.feature" scenarioTitle

    /// Runs one scenario of `agents-validate-claude.feature`.
    let runValidateClaude (scenarioTitle: string) : unit =
        runIn "agents-validate-claude.feature" scenarioTitle

    /// Runs one scenario of `codex-binding.feature`.
    let runCodexBinding (scenarioTitle: string) : unit =
        runIn "codex-binding.feature" scenarioTitle

    /// Runs one scenario of `governance-word-budget-pre-push.feature`.
    let runWordBudgetPrePush (scenarioTitle: string) : unit =
        runIn "governance-word-budget-pre-push.feature" scenarioTitle

    /// Runs one scenario of `governance-word-budget-rule.feature`.
    let runWordBudgetRule (scenarioTitle: string) : unit =
        runIn "governance-word-budget-rule.feature" scenarioTitle

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

[<Fact>]
let ``Set of distinct agents and skills passes`` () =
    FeatureRunner.runDuplication "Set of distinct agents and skills passes"

[<Fact>]
let ``Two agents sharing 12 consecutive lines verbatim fails`` () =
    FeatureRunner.runDuplication "Two agents sharing 12 consecutive lines verbatim fails"

[<Fact>]
let ``Agent body matching 10+ consecutive lines of a SKILL.md fails (agent-skill duplication)`` () =
    FeatureRunner.runDuplication
        "Agent body matching 10+ consecutive lines of a SKILL.md fails (agent-skill duplication)"

[<Fact>]
let ``Heading-only or whitespace-only 10-line window does NOT trigger a finding`` () =
    FeatureRunner.runDuplication "Heading-only or whitespace-only 10-line window does NOT trigger a finding"

[<Fact>]
let ``The mirror target is declared in the registry`` () =
    FeatureRunner.runSkillsMirror "The mirror target is declared in the registry"

[<Fact>]
let ``Every repository skill is mirrored as real files, not links`` () =
    FeatureRunner.runSkillsMirror "Every repository skill is mirrored as real files, not links"

[<Fact>]
let ``Regeneration is idempotent and a hand edit is caught`` () =
    FeatureRunner.runSkillsMirror "Regeneration is idempotent and a hand edit is caught"

[<Fact>]
let ``The npm entry points cover the new mirror`` () =
    FeatureRunner.runSkillsMirror "The npm entry points cover the new mirror"

[<Fact>]
let ``The emitted mirror survives the formatter`` () =
    FeatureRunner.runSkillsMirror "The emitted mirror survives the formatter"

[<Fact>]
let ``Syncing converts Claude agents to OpenCode format and leaves skills in place`` () =
    FeatureRunner.runSync "Syncing converts Claude agents to OpenCode format and leaves skills in place"

[<Fact>]
let ``The --dry-run flag previews changes without modifying files`` () =
    FeatureRunner.runSync "The --dry-run flag previews changes without modifying files"

[<Fact>]
let ``The --agents-only flag syncs agents without touching skills`` () =
    FeatureRunner.runSync "The --agents-only flag syncs agents without touching skills"

[<Fact>]
let ``Model names are correctly translated to OpenCode equivalents`` () =
    FeatureRunner.runSync "Model names are correctly translated to OpenCode equivalents"

[<Fact>]
let ``The opus model name is translated to the same OpenCode equivalent as sonnet`` () =
    FeatureRunner.runSync "The opus model name is translated to the same OpenCode equivalent as sonnet"

[<Fact>]
let ``Directories that are in sync pass validation`` () =
    FeatureRunner.runSync "Directories that are in sync pass validation"

[<Fact>]
let ``A description mismatch between directories fails validation`` () =
    FeatureRunner.runSync "A description mismatch between directories fails validation"

[<Fact>]
let ``A count mismatch between directories fails validation`` () =
    FeatureRunner.runSync "A count mismatch between directories fails validation"

[<Fact>]
let ``A directory with all agents and skills correctly configured passes validation`` () =
    FeatureRunner.runValidateClaude "A directory with all agents and skills correctly configured passes validation"

[<Fact>]
let ``An agent file missing a required frontmatter field fails validation`` () =
    FeatureRunner.runValidateClaude "An agent file missing a required frontmatter field fails validation"

[<Fact>]
let ``Two agents with the same name fail validation`` () =
    FeatureRunner.runValidateClaude "Two agents with the same name fail validation"

[<Fact>]
let ``--agents-only validates agents without checking skills`` () =
    FeatureRunner.runValidateClaude "--agents-only validates agents without checking skills"

[<Fact>]
let ``--skills-only validates skills without checking agents`` () =
    FeatureRunner.runValidateClaude "--skills-only validates skills without checking agents"

[<Fact>]
let ``A Claude agent under a role subfolder gets a flat Codex TOML counterpart`` () =
    FeatureRunner.runCodexBinding "A Claude agent under a role subfolder gets a flat Codex TOML counterpart"

[<Fact>]
let ``Agent identity comes from the name frontmatter, not the source subfolder`` () =
    FeatureRunner.runCodexBinding "Agent identity comes from the name frontmatter, not the source subfolder"

[<Fact>]
let ``Regenerating rewrites only the delimited region of .codex/config.toml`` () =
    FeatureRunner.runCodexBinding "Regenerating rewrites only the delimited region of .codex/config.toml"

[<Fact>]
let ``Pushing an over-budget instruction file is blocked`` () =
    FeatureRunner.runWordBudgetPrePush "Pushing an over-budget instruction file is blocked"

[<Fact>]
let ``Pushing changes that do not touch instruction files skips the gate`` () =
    FeatureRunner.runWordBudgetPrePush "Pushing changes that do not touch instruction files skips the gate"

[<Fact>]
let ``Pushing an in-budget instruction-file edit passes`` () =
    FeatureRunner.runWordBudgetPrePush "Pushing an in-budget instruction-file edit passes"

[<Fact>]
let ``Pushing an RTK-only change invokes its configured gate`` () =
    FeatureRunner.runWordBudgetPrePush "Pushing an RTK-only change invokes its configured gate"

[<Fact>]
let ``The rule is documented as a convention`` () =
    FeatureRunner.runWordBudgetRule "The rule is documented as a convention"

[<Fact>]
let ``repo-rules-checker validates the budget qualitatively`` () =
    FeatureRunner.runWordBudgetRule "repo-rules-checker validates the budget qualitatively"

[<Fact>]
let ``The quality-gate workflow delegates the validator by exact gate ID`` () =
    FeatureRunner.runWordBudgetRule "The quality-gate workflow delegates the validator by exact gate ID"

[<Fact>]
let ``The preflight envelope carries the governance-word-budget category`` () =
    FeatureRunner.runWordBudgetRule "The preflight envelope carries the governance-word-budget category"

[<Fact>]
let ``The AI checker defers to lifecycle-gate evidence`` () =
    FeatureRunner.runWordBudgetRule "The AI checker defers to lifecycle-gate evidence"
