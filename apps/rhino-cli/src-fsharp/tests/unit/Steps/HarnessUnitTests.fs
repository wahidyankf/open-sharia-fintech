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
