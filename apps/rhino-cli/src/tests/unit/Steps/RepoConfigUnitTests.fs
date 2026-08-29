/// Plain xunit tests exercising `RhinoCli.Application.RepoConfig` behaviour
/// that has no dedicated Gherkin scenario: `validateRepoRelativePath`'s guard
/// clauses, `confinedRepoPath`'s no-existing-ancestor case, malformed
/// `harness[].tier` values, and gate entries with no `exclude` argument.
/// Kept separate from `RepoConfigSteps.fs` (which binds only real, frozen
/// feature-file scenarios) so this file can grow test cases without
/// inflating the plan's tracked Gherkin scenario count — mirrors
/// `ConventionUnitTests.fs`'s own rationale.
module RhinoCli.Tests.Unit.Steps.RepoConfigUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Application.RepoConfig

let private newTempDir () =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-repo-config-unit-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private writeFile (root: string) (relativePath: string) (content: string) =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
    File.WriteAllText(full, content)

// ---- validateRepoRelativePath guard clauses ----

[<Fact>]
let ``validateRepoRelativePath rejects an empty value`` () =
    match validateRepoRelativePath "" with
    | Error message -> Assert.Contains("non-empty", message)
    | Ok() -> Assert.Fail("expected an empty value to be rejected")

[<Fact>]
let ``validateRepoRelativePath rejects an absolute value`` () =
    match validateRepoRelativePath "/etc/passwd" with
    | Error message -> Assert.Contains("non-empty repository-relative path", message)
    | Ok() -> Assert.Fail("expected an absolute value to be rejected")

[<Fact>]
let ``validateRepoRelativePath rejects a value with leading whitespace`` () =
    match validateRepoRelativePath " tooling/sdk/global.json" with
    | Error message -> Assert.Contains("leading or trailing whitespace", message)
    | Ok() -> Assert.Fail("expected a leading-whitespace value to be rejected")

[<Fact>]
let ``validateRepoRelativePath rejects a value with trailing whitespace`` () =
    match validateRepoRelativePath "tooling/sdk/global.json " with
    | Error message -> Assert.Contains("leading or trailing whitespace", message)
    | Ok() -> Assert.Fail("expected a trailing-whitespace value to be rejected")

[<Fact>]
let ``validateRepoRelativePath rejects a parent-directory component`` () =
    match validateRepoRelativePath "tooling/../secrets" with
    | Error message -> Assert.Contains("parent-directory", message)
    | Ok() -> Assert.Fail("expected a parent-directory component to be rejected")

[<Fact>]
let ``validateRepoRelativePath accepts a clean repository-relative path`` () =
    match validateRepoRelativePath "tooling/sdk/global.json" with
    | Ok() -> ()
    | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)

// ---- confinedRepoPath: nearest existing ancestor is repoRoot itself ----

// A repository root always exists (this function's caller already required
// that), so the nearest ancestor `candidate.ancestors()` finds is never
// `None` in practice — mirrors the Rust port's own `# Panics`-adjacent doc
// comment noting the equivalent branch there "can never fail". A configured
// value naming a not-yet-created nested file therefore still resolves
// lexically to a location under `repoRoot`, without requiring the leaf file
// itself to exist yet.
[<Fact>]
let ``confinedRepoPath resolves a not-yet-existing nested path lexically under repoRoot`` () =
    let root = newTempDir ()

    try
        match confinedRepoPath root "nowhere/at/all.json" with
        | Ok path ->
            Assert.False(File.Exists path)
            Assert.StartsWith(Path.GetFullPath root, path, StringComparison.Ordinal)
        | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``confinedRepoPath rejects a lexically unsafe value before touching the filesystem`` () =
    let root = newTempDir ()

    try
        match confinedRepoPath root "../escape.json" with
        | Ok path -> Assert.Fail(sprintf "expected Error, got Ok %s" path)
        | Error message -> Assert.Contains("parent-directory", message)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``confinedRepoPath resolves a path nested under an existing directory ancestor`` () =
    let root = newTempDir ()

    try
        writeFile root "tooling/sdk/global.json" "{}"

        match confinedRepoPath root "tooling/sdk/global.json" with
        | Ok path -> Assert.True(File.Exists path)
        | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    finally
        Directory.Delete(root, true)

// ---- load: malformed harness[].tier ----

[<Fact>]
let ``load rejects a harness entry with an unrecognised tier value`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "harness:\n  - name: mystery\n    tier: sideways\n"

        match load root with
        | Error message ->
            Assert.Contains("harness[0].tier", message)
            Assert.Contains("sideways", message)
        | Ok _ -> Assert.Fail("expected an unrecognised tier value to be rejected")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``load rejects a harness entry with a missing tier key`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "harness:\n  - name: mystery\n"

        match load root with
        | Error message -> Assert.Contains("required key is missing", message)
        | Ok _ -> Assert.Fail("expected a missing tier key to be rejected")
    finally
        Directory.Delete(root, true)

// ---- load: sections absent entirely ----

[<Fact>]
let ``load defaults every section to empty when repo-config.yml declares none of them`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "unrelated-top-level-key: 1\n"

        match load root with
        | Ok config ->
            Assert.Empty(config.Harness)
            Assert.Empty(config.Gates)
            Assert.Empty(config.Specs.DddAreas)
            Assert.Empty(config.Specs.DomainAreas)
            Assert.Equal<string option>(None, config.Doctor.DotnetGlobalJson)
        | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    finally
        Directory.Delete(root, true)

// ---- gate entries: exclude argument absent ----

[<Fact>]
let ``a gate entry with no args carries an empty exclusion list`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" (String.concat "\n" [ "gates:"; "  - id: no-args-gate"; "" ])

        match load root with
        | Ok config ->
            let gate = config.Gates |> List.find (fun g -> g.Id = "no-args-gate")
            Assert.True(Map.isEmpty gate.Args)
        | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    finally
        Directory.Delete(root, true)

// ---- loadOrDefault: falls back on parse failure ----

[<Fact>]
let ``loadOrDefault falls back to an empty configuration on unparseable YAML`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "harness: [this is not valid yaml:\n"
        let config = loadOrDefault root
        Assert.Empty(config.Harness)
    finally
        Directory.Delete(root, true)

// ---- validateAtRoot: passing configuration ----

[<Fact>]
let ``validateAtRoot passes when no doctor path is configured`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "harness: []\n"
        let ok, output = validateAtRoot root
        Assert.True(ok, output)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``validateAtRoot passes when the configured doctor path is repository-relative and clean`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "doctor:\n  dotnet-global-json: tooling/sdk/global.json\n"
        let ok, output = validateAtRoot root
        Assert.True(ok, output)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``validateAtRoot fails loudly when repo-config.yml cannot be parsed`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "harness: [this is not valid yaml:\n"
        let ok, output = validateAtRoot root
        Assert.False(ok)
        Assert.Contains("failed strict schema deserialization", output)
    finally
        Directory.Delete(root, true)

// ---- buildDotnetToolDef: falls back to the conventional root global.json ----

[<Fact>]
let ``buildDotnetToolDef falls back to the repository root's global.json when unconfigured`` () =
    let root = newTempDir ()

    try
        writeFile root "global.json" "{\"sdk\":{\"version\":\"9.0.100\"}}"
        let config = loadOrDefault root
        let toolDef = buildDotnetToolDef root config
        Assert.Equal("9.0.100", toolDef.ReadReq())
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``buildDotnetToolDef falls back when the configured path is invalid`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "doctor:\n  dotnet-global-json: ./escapes/invalid.json\n"
        writeFile root "global.json" "{\"sdk\":{\"version\":\"9.0.100\"}}"
        let config = loadOrDefault root
        let toolDef = buildDotnetToolDef root config
        Assert.Equal("9.0.100", toolDef.ReadReq())
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``buildDotnetToolDef reads an empty string when global.json is absent`` () =
    let root = newTempDir ()

    try
        let config = loadOrDefault root
        let toolDef = buildDotnetToolDef root config
        Assert.Equal("", toolDef.ReadReq())
    finally
        Directory.Delete(root, true)
