/// Plain xunit tests for the branches of `RhinoCli.Application.Harness` that
/// `agents-bindings.feature`'s 10 scenarios never reach.
///
/// The scenarios exercise the happy paths and the two failure modes they
/// specify. Everything else in the module — the frontmatter parser's four
/// rejection arms, agent-name collision detection, group nesting, the
/// unreadable-catalog arm, and the `warning` check constructor — is reachable
/// only from inputs a well-formed repository never produces. Pinning them
/// directly keeps them pinned regardless of what the corpus contains, the
/// same corpus-independence rule the two Wave D formatter defects taught (see
/// `learnings.md`, 2026-08-28).
module RhinoCli.Tests.Unit.Steps.HarnessUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Application.Harness

let private scratch () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-harness-unit-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory dir |> ignore
    dir

let private writeFile (path: string) (content: string) : unit =
    Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
    File.WriteAllText(path, content)

// ---------------------------------------------------------------------------
// ValidationCheck / ValidationResult
// ---------------------------------------------------------------------------

[<Fact>]
let ``passed carries no expected-actual pair`` () =
    let check = ValidationCheck.passed "Name" "all good"
    Assert.Equal("passed", check.Status)
    Assert.Equal("", check.Expected)
    Assert.Equal("", check.Actual)
    Assert.Equal("all good", check.Message)

[<Fact>]
let ``warning carries the expected-actual pair`` () =
    let check = ValidationCheck.warning "Name" "want" "got" "advisory"
    Assert.Equal("warning", check.Status)
    Assert.Equal("want", check.Expected)
    Assert.Equal("got", check.Actual)

[<Fact>]
let ``failedMsg carries no expected-actual pair`` () =
    let check = ValidationCheck.failedMsg "Name" "io error"
    Assert.Equal("failed", check.Status)
    Assert.Equal("", check.Expected)
    Assert.Equal("", check.Actual)

[<Fact>]
let ``tally counts each status into its own bucket`` () =
    let result =
        ValidationResult.empty
        |> ValidationResult.tally (ValidationCheck.passed "a" "ok")
        |> ValidationResult.tally (ValidationCheck.warning "b" "w" "x" "advisory")
        |> ValidationResult.tally (ValidationCheck.failed "c" "w" "x" "bad")
        |> ValidationResult.tally (ValidationCheck.failedMsg "d" "io")

    Assert.Equal(4, result.TotalChecks)
    Assert.Equal(1, result.PassedChecks)
    Assert.Equal(1, result.WarningChecks)
    Assert.Equal(2, result.FailedChecks)

[<Fact>]
let ``tally preserves insertion order`` () =
    let result =
        ValidationResult.empty
        |> ValidationResult.tally (ValidationCheck.passed "first" "ok")
        |> ValidationResult.tally (ValidationCheck.passed "second" "ok")

    Assert.Equal<string list>([ "first"; "second" ], result.Checks |> List.map (fun c -> c.Name))

// ---------------------------------------------------------------------------
// Frontmatter
// ---------------------------------------------------------------------------

[<Fact>]
let ``normalizeYaml inserts the missing space after a colon`` () =
    Assert.Equal("name: value\ndescription: ok\n", normalizeYaml "name:value\ndescription: ok\n")

[<Fact>]
let ``normalizeYaml leaves list items alone`` () =
    // The key must start the line, so an indented `- Read` never matches.
    Assert.Equal("tools:\n  - Read\n  - Write\n", normalizeYaml "tools:\n  - Read\n  - Write\n")

[<Fact>]
let ``extractFrontmatter splits a well-formed file`` () =
    match extractFrontmatter "---\nname: foo\ndescription: bar\n---\nbody here\n" with
    | Ok(front, body) ->
        Assert.Equal("name: foo\ndescription: bar", front)
        Assert.Equal("body here\n", body)
    | Error e -> failwith e

[<Fact>]
let ``extractFrontmatter rejects a file too short to hold frontmatter`` () =
    Assert.Equal(Error "file too short to contain frontmatter", extractFrontmatter "---\n")

[<Fact>]
let ``extractFrontmatter rejects a missing opening marker`` () =
    Assert.Equal(Error "frontmatter does not start with ---", extractFrontmatter "name: foo\n---\nbody\n")

[<Fact>]
let ``extractFrontmatter rejects a missing closing marker`` () =
    Assert.Equal(Error "frontmatter closing --- not found", extractFrontmatter "---\nname: foo\nbody\nstuff\n")

[<Fact>]
let ``extractFrontmatter yields an empty body when the file ends at the closing marker`` () =
    match extractFrontmatter "---\nname: foo\n---" with
    | Ok(front, body) ->
        Assert.Equal("name: foo", front)
        Assert.Equal("", body)
    | Error e -> failwith e

// ---------------------------------------------------------------------------
// Agent source discovery
// ---------------------------------------------------------------------------

[<Fact>]
let ``isMirrorableAgentFilename accepts only a non-README markdown file`` () =
    Assert.True(isMirrorableAgentFilename "probe-maker.md" false)
    Assert.False(isMirrorableAgentFilename "probe-maker.md" true)
    Assert.False(isMirrorableAgentFilename "README.md" false)
    Assert.False(isMirrorableAgentFilename "notes.txt" false)

[<Fact>]
let ``readAgentName reads the frontmatter name rather than the filename`` () =
    let root = scratch ()
    let path = Path.Combine(root, "on-disk-filename.md")
    writeFile path "---\nname: frontmatter-name\ndescription: probe\n---\nbody\n"
    Assert.Equal(Ok "frontmatter-name", readAgentName path)

[<Fact>]
let ``readAgentName rejects a file with no name field`` () =
    let root = scratch ()
    let path = Path.Combine(root, "nameless.md")
    writeFile path "---\ndescription: probe\n---\nbody\n"

    match readAgentName path with
    | Ok name -> failwithf "expected a failure, got %s" name
    | Error message -> Assert.Contains("has no scalar 'name' frontmatter field", message)

[<Fact>]
let ``readAgentName rejects a non-mapping frontmatter block`` () =
    let root = scratch ()
    let path = Path.Combine(root, "sequence.md")
    writeFile path "---\n- one\n- two\n---\nbody\n"

    match readAgentName path with
    | Ok name -> failwithf "expected a failure, got %s" name
    | Error message -> Assert.Contains(path, message)

[<Fact>]
let ``readAgentName reports an unreadable file`` () =
    let root = scratch ()
    let path = Path.Combine(root, "absent.md")

    match readAgentName path with
    | Ok name -> failwithf "expected a failure, got %s" name
    | Error message -> Assert.Contains("failed to read file", message)

[<Fact>]
let ``readAgentName reports a malformed frontmatter block`` () =
    let root = scratch ()
    let path = Path.Combine(root, "no-marker.md")
    writeFile path "name: foo\ndescription: bar\nbody\n"

    match readAgentName path with
    | Ok name -> failwithf "expected a failure, got %s" name
    | Error message -> Assert.Contains("failed to extract frontmatter from", message)

[<Fact>]
let ``discoverAgentSources walks one level of group nesting and sorts by name`` () =
    let root = scratch ()
    writeFile (Path.Combine(root, "zulu.md")) "---\nname: zulu\n---\nbody\n"
    writeFile (Path.Combine(root, "group", "alpha.md")) "---\nname: alpha\n---\nbody\n"
    // Neither of these is mirrorable, and the second level of nesting is
    // deliberately not walked.
    writeFile (Path.Combine(root, "README.md")) "# index\n"
    writeFile (Path.Combine(root, "group", "deeper", "hidden.md")) "---\nname: hidden\n---\nbody\n"

    match discoverAgentSources root with
    | Ok sources -> Assert.Equal<string list>([ "alpha"; "zulu" ], sources |> List.map snd)
    | Error e -> failwith e

[<Fact>]
let ``discoverAgentSources rejects two sources flattening to one mirror name`` () =
    let root = scratch ()
    writeFile (Path.Combine(root, "first.md")) "---\nname: same\n---\nbody\n"
    writeFile (Path.Combine(root, "group", "second.md")) "---\nname: same\n---\nbody\n"

    match discoverAgentSources root with
    | Ok sources -> failwithf "expected a collision, got %A" (sources |> List.map snd)
    | Error message ->
        Assert.Contains("agent name collision: 'same'", message)
        Assert.Contains("flat mirror filenames must be unique", message)

[<Fact>]
let ``discoverAgentSources reports an unreadable directory`` () =
    let root = scratch ()

    match discoverAgentSources (Path.Combine(root, "absent")) with
    | Ok sources -> failwithf "expected a failure, got %A" sources
    | Error message -> Assert.Contains("failed to read", message)

[<Fact>]
let ``expectedBindingPaths is empty when there is no claude agents directory`` () =
    Assert.Equal(Ok([]: string list), expectedBindingPaths (scratch ()))

[<Fact>]
let ``expectedBindingPaths names one codex toml mirror per discovered agent`` () =
    let root = scratch ()
    writeFile (Path.Combine(root, ".claude", "agents", "probe.md")) "---\nname: probe-maker\n---\nbody\n"
    Assert.Equal(Ok [ ".codex/agents/probe-maker.toml" ], expectedBindingPaths root)

[<Fact>]
let ``expectedBindingPaths propagates a discovery failure`` () =
    let root = scratch ()
    writeFile (Path.Combine(root, ".claude", "agents", "nameless.md")) "---\ndescription: probe\n---\nbody\n"

    match expectedBindingPaths root with
    | Ok paths -> failwithf "expected a failure, got %A" paths
    | Error message -> Assert.Contains("has no scalar 'name' frontmatter field", message)

// ---------------------------------------------------------------------------
// Catalog coverage
// ---------------------------------------------------------------------------

[<Fact>]
let ``validateCatalogCoverage tolerates a leading slash in the directory name`` () =
    let root = scratch ()
    Directory.CreateDirectory(Path.Combine(root, ".github")) |> ignore
    writeFile (Path.Combine(root, platformBindingsCatalog)) "# Platform Bindings\n\n- `/.github` row\n"

    let check = validateCatalogCoverage root "/.github"
    Assert.Equal("passed", check.Status)
    Assert.Equal("Catalog Coverage: /.github", check.Name)

[<Fact>]
let ``validateCatalogCoverage reports an unreadable catalog`` () =
    let root = scratch ()
    Directory.CreateDirectory(Path.Combine(root, ".github")) |> ignore
    // The directory is present, so the catalog must be read — and it is absent.
    let check = validateCatalogCoverage root ".github"
    Assert.Equal("failed", check.Status)
    Assert.Contains("failed to read " + platformBindingsCatalog, check.Message)

[<Fact>]
let ``validateCatalogCoverage covers a present file, not only a directory`` () =
    let root = scratch ()
    // `.github` is listed as a directory in production, but the check accepts
    // any present path so a single-file binding surface would still be covered.
    writeFile (Path.Combine(root, ".github")) "placeholder\n"
    writeFile (Path.Combine(root, platformBindingsCatalog)) "# Platform Bindings\n\n- `.github` row\n"
    Assert.Equal("passed", (validateCatalogCoverage root ".github").Status)

// ---------------------------------------------------------------------------
// Codex agent files
// ---------------------------------------------------------------------------

[<Fact>]
let ``isRejectedCodexAgentFilename accepts only a toml file`` () =
    Assert.False(isRejectedCodexAgentFilename "probe-maker.toml")
    Assert.True(isRejectedCodexAgentFilename "probe-maker.md")
    Assert.True(isRejectedCodexAgentFilename "probe-maker")

[<Fact>]
let ``validateCodexAgentsDir passes when the directory is absent`` () =
    let check = validateCodexAgentsDir (scratch ())
    Assert.Equal("passed", check.Status)
    Assert.Contains("absent; nothing to check", check.Message)

[<Fact>]
let ``validateCodexAgentsDir passes on an empty directory`` () =
    let root = scratch ()
    Directory.CreateDirectory(Path.Combine(root, ".codex", "agents")) |> ignore
    Assert.Equal("passed", (validateCodexAgentsDir root).Status)

[<Fact>]
let ``validateCodexAgentsDir names every offender in sorted order`` () =
    let root = scratch ()
    let agents = Path.Combine(root, ".codex", "agents")
    writeFile (Path.Combine(agents, "zulu.md")) "# z\n"
    writeFile (Path.Combine(agents, "alpha.md")) "# a\n"
    writeFile (Path.Combine(agents, "keep.toml")) "description = \"keep\"\n"

    let check = validateCodexAgentsDir root
    Assert.Equal("failed", check.Status)
    Assert.Contains("non-.toml file(s): alpha.md, zulu.md", check.Actual)
    Assert.DoesNotContain("keep.toml", check.Actual)
    Assert.Contains("[agents.<name>] table in .codex/config.toml", check.Message)

// ---------------------------------------------------------------------------
// validateBindings composition
// ---------------------------------------------------------------------------

[<Fact>]
let ``validateBindings tallies one catalog check per known binding dir plus the codex check`` () =
    let result = validateBindings (scratch ())
    Assert.Equal(List.length knownBindingDirs + 1, result.TotalChecks)
    Assert.Equal(result.TotalChecks, result.PassedChecks)

// ---------------------------------------------------------------------------
// `--harness` name acceptance
// ---------------------------------------------------------------------------

/// A registry holding exactly the names a test needs, so the assertions below
/// do not depend on this repository's live `harness:` list.
let private registryWith (names: string list) : RhinoCli.Application.RepoConfig.RepoConfig =
    { RhinoCli.Application.RepoConfig.empty with
        Harness =
            names
            |> List.map (fun name ->
                { RhinoCli.Application.RepoConfig.HarnessEntry.Name = name
                  Tier = RhinoCli.Application.RepoConfig.Tier.Generated
                  AgentDir = None
                  Mirrors = None
                  ForbidDir = None
                  SkillsDir = None
                  SkillsMirrors = None
                  Vendored = []
                  Ownership = [] }) }

[<Fact>]
let ``acceptedHarnessNames is the registry order`` () =
    Assert.Equal<string list>(
        [ "claude-code"; "opencode"; "codex" ],
        acceptedHarnessNames (registryWith [ "claude-code"; "opencode"; "codex" ])
    )

[<Fact>]
let ``validateHarnessName accepts a declared name`` () =
    Assert.Equal(Ok(), validateHarnessName (registryWith [ "claude-code"; "codex" ]) "codex")

[<Fact>]
let ``validateHarnessName rejects an undeclared name and quotes the accepted set`` () =
    match validateHarnessName (registryWith [ "claude-code"; "codex" ]) "cursor" with
    | Ok() -> failwith "expected 'cursor' to be rejected"
    | Error message -> Assert.Equal("unknown harness name 'cursor'; expected one of 'claude-code', 'codex'", message)

[<Fact>]
let ``validateHarnessName rejects every name against an empty registry`` () =
    // A registry contraction to nothing rejects the previously-accepted name
    // automatically — the accepted set is never hard-coded.
    match validateHarnessName (registryWith []) "codex" with
    | Ok() -> failwith "expected 'codex' to be rejected"
    | Error message -> Assert.Equal("unknown harness name 'codex'; expected one of ", message)

// ---------------------------------------------------------------------------
// Duplication detection — helpers
// ---------------------------------------------------------------------------

let private proseLines (tag: string) (count: int) : string =
    String.Join("\n", [ for i in 1..count -> sprintf "%s line %d carries its own sentence." tag i ])
    + "\n"

let private agentAt (root: string) (name: string) (body: string) : string =
    let path = Path.Combine(root, ".claude", "agents", name + ".md")
    writeFile path (sprintf "---\nname: %s\n---\n%s" name body)
    path

let private skillAt (root: string) (name: string) (body: string) : string =
    let path = Path.Combine(root, ".claude", "skills", name, "SKILL.md")
    writeFile path (sprintf "---\nname: %s\n---\n%s" name body)
    path

[<Fact>]
let ``stripFrontmatterBody returns a file with no frontmatter unchanged`` () =
    // Unlike `extractFrontmatter`, which rejects such a file: a duplication
    // scan still has to read its body.
    Assert.Equal("# Title\n", stripFrontmatterBody "# Title\n")

[<Fact>]
let ``stripFrontmatterBody removes an LF frontmatter block`` () =
    Assert.Equal("Body\n", stripFrontmatterBody "---\nname: foo\n---\nBody\n")

[<Fact>]
let ``stripFrontmatterBody removes a CRLF frontmatter block`` () =
    Assert.Contains("Body", stripFrontmatterBody "---\r\nname: foo\r\n---\r\nBody\r\n")

[<Fact>]
let ``stripFrontmatterBody returns the input when the fence never closes`` () =
    let unclosed = "---\nname: foo\nstill frontmatter\n"
    Assert.Equal(unclosed, stripFrontmatterBody unclosed)

[<Fact>]
let ``stripFrontmatterBody yields an empty body when the file ends at the closing fence`` () =
    Assert.Equal("", stripFrontmatterBody "---\nname: foo\n---")

[<Fact>]
let ``normalizeLines trims trailing whitespace and collapses blank runs`` () =
    Assert.Equal<string list>([ "a"; "b"; "c" ], normalizeLines "a  \nb\t\nc")
    Assert.Equal<string list>([ "a"; ""; "b" ], normalizeLines "a\n\n\nb")

[<Fact>]
let ``isExcludedWindow skips blank-only and heading-only windows`` () =
    Assert.True(isExcludedWindow (List.replicate duplicationWindowSize ""))
    Assert.True(isExcludedWindow [ "# One"; ""; "## Two"; "" ])
    Assert.False(isExcludedWindow [ "# One"; "prose carries meaning" ])

// ---------------------------------------------------------------------------
// Duplication detection — scanning
// ---------------------------------------------------------------------------

[<Fact>]
let ``detectDuplication reports nothing for a repository with no agents`` () =
    Assert.Equal(Ok([]: DuplicationFinding list), detectDuplication (scratch ()))

[<Fact>]
let ``detectDuplication ignores a window repeated inside one file`` () =
    // Repetition within a single file is not cross-file duplication, so the
    // cluster never reaches two distinct files.
    let root = scratch ()
    let block = proseLines "shared" 12
    agentAt root "alpha-one" (block + block) |> ignore

    match detectDuplication root with
    | Ok findings -> Assert.Equal<DuplicationFinding list>([], findings)
    | Error e -> failwith e

[<Fact>]
let ``detectDuplication exempts two files in the same role family`` () =
    // `*-checker` agents are *designed* to share workflow boilerplate.
    let root = scratch ()
    let block = proseLines "shared" 12
    agentAt root "alpha-checker" (block + proseLines "alpha" 4) |> ignore
    agentAt root "beta-checker" (block + proseLines "beta" 4) |> ignore

    match detectDuplication root with
    | Ok findings -> Assert.Equal<DuplicationFinding list>([], findings)
    | Error e -> failwith e

[<Fact>]
let ``detectDuplication exempts the maker-checker-fixer trio of one domain`` () =
    let root = scratch ()
    let block = proseLines "shared" 12
    agentAt root "alpha-maker" (block + proseLines "one" 4) |> ignore
    agentAt root "alpha-checker" (block + proseLines "two" 4) |> ignore
    agentAt root "alpha-fixer" (block + proseLines "three" 4) |> ignore

    match detectDuplication root with
    | Ok findings -> Assert.Equal<DuplicationFinding list>([], findings)
    | Error e -> failwith e

[<Fact>]
let ``detectDuplication reports duplication spanning different roles and domains`` () =
    let root = scratch ()
    let block = proseLines "shared" 12
    let alpha = agentAt root "alpha-one" (block + proseLines "alpha" 4)
    let beta = agentAt root "beta-two" (block + proseLines "beta" 4)

    match detectDuplication root with
    | Error e -> failwith e
    | Ok findings ->
        Assert.NotEmpty findings

        for finding in findings do
            Assert.Equal<string list>([ alpha; beta ] |> List.sort, finding.Files |> List.sort)
            Assert.Equal(duplicationWindowSize, finding.WindowSize)
            Assert.Equal("high", finding.Severity)
            Assert.Contains("verbatim duplication across 2 files", finding.Message)

[<Fact>]
let ``detectDuplication reports an agent duplicating a skill body`` () =
    let root = scratch ()
    let block = proseLines "shared" 11
    let agent = agentAt root "alpha-one" (block + proseLines "alpha" 4)
    let skill = skillAt root "gamma-notes" (block + proseLines "gamma" 4)

    match detectDuplication root with
    | Error e -> failwith e
    | Ok findings ->
        Assert.NotEmpty findings
        let files = findings |> List.collect (fun f -> f.Files) |> List.distinct
        Assert.Contains(agent, files)
        Assert.Contains(skill, files)

[<Fact>]
let ``detectDuplication skips a file shorter than one window`` () =
    let root = scratch ()
    agentAt root "alpha-one" (proseLines "alpha" 3) |> ignore
    agentAt root "beta-two" (proseLines "alpha" 3) |> ignore

    match detectDuplication root with
    | Ok findings -> Assert.Equal<DuplicationFinding list>([], findings)
    | Error e -> failwith e

[<Fact>]
let ``detectDuplication orders findings by first file then first start line`` () =
    let root = scratch ()
    // Two independent shared blocks, seeded so the sort has something to do.
    let first = proseLines "first" 10
    let second = proseLines "second" 10
    agentAt root "alpha-one" (first + proseLines "pad" 3 + second) |> ignore
    agentAt root "beta-two" (first + proseLines "other" 3 + second) |> ignore

    match detectDuplication root with
    | Error e -> failwith e
    | Ok findings ->
        Assert.NotEmpty findings

        let keys = findings |> List.map (fun f -> List.head f.Files, List.head f.StartLines)

        Assert.Equal<(string * int) list>(List.sort keys, keys)

[<Fact>]
let ``detectDuplication reads the registry-declared source directory`` () =
    // The scan follows `harness:` rather than assuming `.claude/`, so a
    // registry that names another directory is honoured.
    let root = scratch ()
    let block = proseLines "shared" 12

    writeFile
        (Path.Combine(root, "repo-config.yml"))
        "harness:\n  - { name: claude-code, tier: source, agent-dir: .custom/agents }\n"

    let write (name: string) (body: string) =
        let path = Path.Combine(root, ".custom", "agents", name + ".md")
        writeFile path (sprintf "---\nname: %s\n---\n%s" name body)
        path

    let alpha = write "alpha-one" (block + proseLines "alpha" 4)
    // Placed under `.claude/`, which the registry does NOT declare.
    agentAt root "beta-two" (block + proseLines "beta" 4) |> ignore

    match detectDuplication root with
    | Error e -> failwith e
    | Ok findings ->
        // Only one declared directory was scanned, so the pair never meets.
        Assert.Equal<DuplicationFinding list>([], findings)
        Assert.True(File.Exists alpha)

[<Fact>]
let ``detectDuplication skips README.md in an agent directory`` () =
    let root = scratch ()
    let block = proseLines "shared" 12
    writeFile (Path.Combine(root, ".claude", "agents", "README.md")) (sprintf "---\nname: readme\n---\n%s" block)
    agentAt root "alpha-one" (block + proseLines "alpha" 4) |> ignore

    match detectDuplication root with
    | Ok findings -> Assert.Equal<DuplicationFinding list>([], findings)
    | Error e -> failwith e

[<Fact>]
let ``detectDuplication ignores a skill directory with no SKILL.md`` () =
    let root = scratch ()

    Directory.CreateDirectory(Path.Combine(root, ".claude", "skills", "empty-skill"))
    |> ignore

    Assert.Equal(Ok([]: DuplicationFinding list), detectDuplication root)

// ---------------------------------------------------------------------------
// Skills mirror
// ---------------------------------------------------------------------------

let private mirrorConfig (extra: string) : string =
    "harness:\n"
    + "  - name: codex\n"
    + "    tier: generated\n"
    + "    skills-dir: .agents/skills\n"
    + "    skills-mirrors: .claude/skills\n"
    + extra

[<Fact>]
let ``mirrorResultEmpty is all zero`` () =
    Assert.Equal(0, mirrorResultEmpty.Copied)
    Assert.Equal(0, mirrorResultEmpty.Removed)
    Assert.Equal(0, mirrorResultEmpty.VendoredSkipped)

[<Fact>]
let ``emitSkillsMirrors is a no-op when no harness entry declares both skills-dir and skills-mirrors`` () =
    let root = scratch ()
    writeFile (Path.Combine(root, "repo-config.yml")) "harness:\n  - { name: claude-code, tier: source }\n"

    Assert.Equal(Ok mirrorResultEmpty, emitSkillsMirrors root false)

[<Fact>]
let ``emitSkillsMirrors propagates a malformed registry as an error`` () =
    let root = scratch ()
    writeFile (Path.Combine(root, "repo-config.yml")) "harness: [this is not a mapping list\n"

    match emitSkillsMirrors root false with
    | Ok _ -> failwith "expected the malformed registry to fail"
    | Error _ -> ()

[<Fact>]
let ``emitSkillsMirrors rejects a vendored entry with no matching ownership declaration`` () =
    let root = scratch ()
    writeFile (Path.Combine(root, "repo-config.yml")) (mirrorConfig "    vendored: [.agents/skills/plugin]\n")
    writeFile (Path.Combine(root, ".claude", "skills", "alpha", "SKILL.md")) "body\n"

    match emitSkillsMirrors root false with
    | Ok _ -> failwith "expected the vendored/ownership disagreement to fail"
    | Error message -> Assert.Contains("no matching harness[0].ownership entry", message)

[<Fact>]
let ``emitSkillsMirrors under dryRun reports the pending copy without writing`` () =
    let root = scratch ()
    writeFile (Path.Combine(root, "repo-config.yml")) (mirrorConfig "")
    writeFile (Path.Combine(root, ".claude", "skills", "alpha", "SKILL.md")) "body\n"

    match emitSkillsMirrors root true with
    | Error e -> failwith e
    | Ok result ->
        Assert.Equal(1, result.Copied)
        Assert.False(File.Exists(Path.Combine(root, ".agents", "skills", "alpha", "SKILL.md")))

[<Fact>]
let ``emitSkillsMirrors removes a stale mirrored file and prunes its now-empty directory`` () =
    let root = scratch ()
    writeFile (Path.Combine(root, "repo-config.yml")) (mirrorConfig "")
    writeFile (Path.Combine(root, ".claude", "skills", "alpha", "SKILL.md")) "body\n"

    match emitSkillsMirrors root false with
    | Error e -> failwith e
    | Ok _ -> ()

    // The source skill is gone; its mirror is now an orphan.
    Directory.Delete(Path.Combine(root, ".claude", "skills", "alpha"), true)

    match emitSkillsMirrors root false with
    | Error e -> failwith e
    | Ok result ->
        Assert.Equal(1, result.Removed)
        Assert.False(File.Exists(Path.Combine(root, ".agents", "skills", "alpha", "SKILL.md")))
        Assert.False(Directory.Exists(Path.Combine(root, ".agents", "skills", "alpha")))

[<Fact>]
let ``auditSkillsMirrors does not flag a vendored directory with no source counterpart`` () =
    let root = scratch ()

    writeFile
        (Path.Combine(root, "repo-config.yml"))
        (mirrorConfig
            "    vendored: [.agents/skills/plugin]\n    ownership:\n      - path: .agents/skills/plugin\n        class: vendored\n        reason: third-party payload\n")

    writeFile (Path.Combine(root, ".agents", "skills", "plugin", "SKILL.md")) "third-party\n"

    match auditSkillsMirrors root with
    | Error e -> failwith e
    | Ok drift -> Assert.Equal<MirrorDrift list>([], drift)

[<Fact>]
let ``emitSkillsMirrors treats a missing source directory as a no-op, not an error`` () =
    let root = scratch ()
    writeFile (Path.Combine(root, "repo-config.yml")) (mirrorConfig "")

    Assert.Equal(Ok mirrorResultEmpty, emitSkillsMirrors root false)

[<Fact>]
let ``emitSkillsMirrors rejects a skills-dir that escapes the repository root`` () =
    let root = scratch ()

    writeFile
        (Path.Combine(root, "repo-config.yml"))
        ("harness:\n"
         + "  - name: codex\n"
         + "    tier: generated\n"
         + "    skills-dir: ../outside\n"
         + "    skills-mirrors: .claude/skills\n")

    writeFile (Path.Combine(root, ".claude", "skills", "alpha", "SKILL.md")) "body\n"

    match emitSkillsMirrors root false with
    | Ok _ -> failwith "expected an out-of-repository skills-dir to fail"
    | Error message -> Assert.Contains("skills-dir", message)

// ---------------------------------------------------------------------------
// Agent sync — branches `agents-sync.feature`'s 8 scenarios never reach
// ---------------------------------------------------------------------------

let private writeAgent (root: string) (name: string) (frontmatterExtra: string) (body: string) : unit =
    writeFile
        (Path.Combine(root, ".claude", "agents", name + ".md"))
        (sprintf "---\nname: %s\ndescription: fixture\n%s---\n%s" name frontmatterExtra body)

[<Fact>]
let ``convertColor passes an unrecognized color through unchanged, and empty stays empty`` () =
    Assert.Equal("primary", convertColor "blue")
    Assert.Equal("mauve", convertColor "mauve")
    Assert.Equal("", convertColor "")

[<Fact>]
let ``convertPermission lower-cases, trims, and dedupes tool names`` () =
    let perm = convertPermission [ " Read "; "read"; "Write" ]
    Assert.Equal<Map<string, string>>(Map.ofList [ "read", "allow"; "write", "allow" ], perm)

[<Fact>]
let ``convertModel always resolves to the single OpenCode model id`` () =
    Assert.Equal("zai-coding-plan/glm-5.2", convertModel "sonnet")
    Assert.Equal("zai-coding-plan/glm-5.2", convertModel "opus")
    Assert.Equal("zai-coding-plan/glm-5.2", convertModel "")

[<Fact>]
let ``parseClaudeTools accepts a YAML sequence as well as a comma-separated string`` () =
    Assert.Equal<string list>([ "Read"; "Write" ], parseClaudeTools (box "Read, Write"))
    Assert.Equal<string list>([], parseClaudeTools (box 42))

[<Fact>]
let ``convertAllAgents translates maxTurns into a steps field`` () =
    let root = scratch ()
    writeAgent root "steps-agent" "maxTurns: 7\n" "Body.\n"

    match convertAllAgents root false with
    | Error e -> failwith e
    | Ok result ->
        Assert.Equal(1, result.Converted)

        let mirror =
            File.ReadAllText(Path.Combine(root, ".opencode", "agents", "steps-agent.md"))

        Assert.Contains("steps: 7", mirror)

[<Fact>]
let ``convertAllAgents preserves a skills list into the mirror`` () =
    let root = scratch ()
    writeAgent root "skills-agent" "skills:\n  - alpha-skill\n  - beta-skill\n" "Body.\n"

    match convertAllAgents root false with
    | Error e -> failwith e
    | Ok _ ->
        let mirror =
            File.ReadAllText(Path.Combine(root, ".opencode", "agents", "skills-agent.md"))

        Assert.Contains("skills:\n  - alpha-skill\n  - beta-skill", mirror)

[<Fact>]
let ``convertAllAgents warns on an unknown field and on a DropWarn field with its own reason`` () =
    let root = scratch ()
    writeAgent root "warn-agent" "customField: value\nmcpServers: foo\n" "Body.\n"

    match convertAllAgents root false with
    | Error e -> failwith e
    | Ok result ->
        Assert.Contains(result.Warnings, fun w -> w.Field = "customField" && w.Reason = unknownFieldReason)

        Assert.Contains(
            result.Warnings,
            fun w ->
                w.Field = "mcpServers"
                && w.Reason = "OpenCode declares MCP servers at the config level"
        )

[<Fact>]
let ``convertAllAgents rebases a relative link and passes an absolute, URL, or anchor link through unchanged`` () =
    let root = scratch ()

    writeAgent
        root
        "link-agent"
        ""
        "See [other](./other-agent.md), [site](https://example.com), [here](#section), and [empty]().\n"

    writeAgent root "other-agent" "" "Body.\n"

    match convertAllAgents root false with
    | Error e -> failwith e
    | Ok _ ->
        let mirror =
            File.ReadAllText(Path.Combine(root, ".opencode", "agents", "link-agent.md"))

        Assert.Contains("[other](other-agent.md)", mirror)
        Assert.Contains("[site](https://example.com)", mirror)
        Assert.Contains("[here](#section)", mirror)
        Assert.Contains("[empty]()", mirror)

[<Fact>]
let ``validateSync fails a claude source with no frontmatter as a discovery error, not a per-agent check`` () =
    let root = scratch ()
    writeFile (Path.Combine(root, ".claude", "agents", "broken.md")) "no frontmatter here\n"
    Directory.CreateDirectory(Path.Combine(root, ".opencode", "agents")) |> ignore

    let result = validateSync root

    Assert.Contains(
        result.Checks,
        fun c ->
            c.Name = "Agent Equivalence"
            && c.Status = "failed"
            && c.Message.Contains("failed to discover")
    )

[<Fact>]
let ``validateSync reports a missing OpenCode mirror by name`` () =
    let root = scratch ()
    writeAgent root "orphan-agent" "" "Body.\n"
    writeFile (Path.Combine(root, ".opencode", "agents", "placeholder.md")) "---\ndescription: x\n---\nx\n"

    let result = validateSync root

    Assert.Contains(
        result.Checks,
        fun c ->
            c.Name = "Agent Equivalence: orphan-agent"
            && c.Status = "failed"
            && c.Message.Contains("OpenCode mirror not found")
    )

[<Fact>]
let ``validateSync fails when the OpenCode mirror's own frontmatter cannot be parsed`` () =
    let root = scratch ()
    writeAgent root "bad-mirror-agent" "" "Body.\n"
    writeFile (Path.Combine(root, ".opencode", "agents", "bad-mirror-agent.md")) "no frontmatter here\n"

    let result = validateSync root

    Assert.Contains(
        result.Checks,
        fun c ->
            c.Name = "Agent Equivalence: bad-mirror-agent"
            && c.Status = "failed"
            && c.Message.Contains("failed to parse OpenCode frontmatter")
    )

[<Fact>]
let ``validateSync fails a skills-list mismatch and a body mismatch`` () =
    let root = scratch ()
    writeAgent root "skills-mismatch-agent" "model: sonnet\nskills:\n  - alpha\n" "Body.\n"

    match convertAllAgents root false with
    | Error e -> failwith e
    | Ok _ -> ()

    let mirrorPath =
        Path.Combine(root, ".opencode", "agents", "skills-mismatch-agent.md")

    File.WriteAllText(mirrorPath, File.ReadAllText(mirrorPath).Replace("- alpha", "- beta"))

    let result = validateSync root

    Assert.Contains(
        result.Checks,
        fun c ->
            c.Name = "Agent Equivalence: skills-mismatch-agent"
            && c.Message = "skills mismatch"
    )

    writeAgent root "body-mismatch-agent" "model: sonnet\n" "Original body.\n"

    match convertAllAgents root false with
    | Error e -> failwith e
    | Ok _ -> ()

    let bodyMirrorPath =
        Path.Combine(root, ".opencode", "agents", "body-mismatch-agent.md")

    File.WriteAllText(bodyMirrorPath, File.ReadAllText(bodyMirrorPath).Replace("Original body.", "Edited body."))

    let bodyResult = validateSync root

    Assert.Contains(
        bodyResult.Checks,
        fun c -> c.Name = "Agent Equivalence: body-mismatch-agent" && c.Message = "body mismatch"
    )

[<Fact>]
let ``syncAll with SkillsOnly is a no-op that still reports success`` () =
    let root = scratch ()
    writeAgent root "unsynced-agent" "" "Body.\n"

    let opts =
        { syncOptionsDefault root with
            SkillsOnly = true }

    match syncAll opts with
    | Error e -> failwith e
    | Ok result ->
        Assert.Equal(syncResultEmpty, result)
        Assert.False(File.Exists(Path.Combine(root, ".opencode", "agents", "unsynced-agent.md")))
