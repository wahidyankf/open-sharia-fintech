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
            Assert.Empty(config.GateSurfaceGuards)
            Assert.Empty(config.Doctor.SkipTools)
            Assert.Equal<string option>(None, config.Doctor.DotnetGlobalJson)
        | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    finally
        Directory.Delete(root, true)

// ---- load: optional gate surface execution guards ----

[<Fact>]
let ``load parses a tool-neutral gate surface execution guard`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "gate-surface-guards:"
                  "  pre-push:"
                  "    command: ./hippo"
                  "    args:"
                  "      - run"
                  "      - --class=ephemeral"
                  "      - --"
                  "    active-env: HIPPO_SESSION"
                  "" ])

        match load root with
        | Ok config ->
            match Map.tryFind PrePush config.GateSurfaceGuards with
            | Some guard ->
                Assert.Equal("./hippo", guard.Command)
                Assert.Equal<string list>([ "run"; "--class=ephemeral"; "--" ], guard.Args)
                Assert.Equal("HIPPO_SESSION", guard.ActiveEnv)
            | None -> Assert.Fail("expected a pre-push surface guard")
        | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``load rejects an execution guard for an unknown gate surface`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            "gate-surface-guards:\n  release: { command: ./guard, active-env: GUARD_ACTIVE }\n"

        match load root with
        | Error message -> Assert.Contains("unknown gate surface", message)
        | Ok _ -> Assert.Fail("expected the unknown guard surface to be rejected")
    finally
        Directory.Delete(root, true)

[<Theory>]
[<InlineData("", "GUARD_ACTIVE", "command")>]
[<InlineData("./guard", "", "active-env")>]
[<InlineData("./guard", "BAD=NAME", "active-env")>]
[<InlineData("./guard", "BAD NAME", "active-env")>]
[<InlineData("./guard", "BAD-NAME", "active-env")>]
[<InlineData("./guard", "1BAD_NAME", "active-env")>]
let ``load rejects a malformed gate surface execution guard`` command activeEnv expectedField =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "gate-surface-guards:"
                  "  pre-push:"
                  sprintf "    command: '%s'" command
                  sprintf "    active-env: '%s'" activeEnv
                  "" ])

        match load root with
        | Error message -> Assert.Contains(expectedField, message)
        | Ok _ -> Assert.Fail("expected the malformed guard to be rejected")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``load rejects a null gate surface execution guard argument`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "gate-surface-guards:"
                  "  pre-push:"
                  "    command: ./guard"
                  "    args: [run, null, --]"
                  "    active-env: HIPPO_SESSION"
                  "" ])

        match load root with
        | Error message -> Assert.Contains("args[1]", message)
        | Ok _ -> Assert.Fail("expected a null guard argument to be rejected")
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

[<Fact>]
let ``buildDotnetToolDef reads an empty string when the sdk key is absent from global.json`` () =
    let root = newTempDir ()

    try
        writeFile root "global.json" "{\"foo\":\"bar\"}"
        let config = loadOrDefault root
        let toolDef = buildDotnetToolDef root config
        Assert.Equal("", toolDef.ReadReq())
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``buildDotnetToolDef reads an empty string when the sdk key has no version property`` () =
    let root = newTempDir ()

    try
        writeFile root "global.json" "{\"sdk\":{\"other\":1}}"
        let config = loadOrDefault root
        let toolDef = buildDotnetToolDef root config
        Assert.Equal("", toolDef.ReadReq())
    finally
        Directory.Delete(root, true)

// ---- sequenceResults: an Error surfacing from further down the list ----

[<Fact>]
let ``load rejects the second of two harness entries when the first is valid`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "harness:"
                  "  - name: first"
                  "    tier: source"
                  "  - name: second"
                  "    tier: sideways"
                  "" ])

        match load root with
        | Error message ->
            Assert.Contains("harness[1].tier", message)
            Assert.Contains("sideways", message)
        | Ok _ -> Assert.Fail("expected the second harness entry's bad tier to be rejected")
    finally
        Directory.Delete(root, true)

// ---- checkNoUnknownHarnessKeys: shapes the raw-YAML walk tolerates ----

[<Fact>]
let ``load tolerates a non-mapping top-level document when checking for unknown harness keys`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "just-a-scalar-document\n"

        match load root with
        | Error message -> Assert.DoesNotContain("unknown key", message)
        | Ok _ -> ()
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``the unknown-harness-key check is a no-op when harness is a mapping instead of a list`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "harness:\n  name: mystery\n"

        match load root with
        | Error message -> Assert.DoesNotContain("unknown key", message)
        | Ok _ -> ()
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``the unknown-harness-key check skips a harness list item that is not a mapping`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "harness:\n  - just-a-string\n  - name: proper\n    tier: source\n"

        match load root with
        | Error message -> Assert.DoesNotContain("unknown key", message)
        | Ok _ -> ()
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``the unknown-harness-key check skips an ownership list item that is not a mapping`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "harness:"
                  "  - name: mystery"
                  "    tier: source"
                  "    ownership:"
                  "      - just-a-string"
                  "      - path: a"
                  "        class: source"
                  "" ])

        match load root with
        | Error message -> Assert.DoesNotContain("unknown key", message)
        | Ok _ -> ()
    finally
        Directory.Delete(root, true)

// ---- gateEnumFindings: non-mapping/non-scalar raw YAML nodes ----

[<Fact>]
let ``load reports gate id as empty when the id value is not a scalar`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" (String.concat "\n" [ "gates:"; "  - id: [a, b]"; "    type: bogus"; "" ])

        match load root with
        | Error message -> Assert.Contains("(gate id \"\")", message)
        | Ok _ -> Assert.Fail("expected an unknown gate type value to be rejected")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``load reports an unknown gate kind value`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat "\n" [ "gates:"; "  - id: bogus-kind"; "    type: check"; "    kind: mystery"; "" ])

        match load root with
        | Error message ->
            Assert.Contains("gates[0].kind", message)
            Assert.Contains("mystery", message)
        | Ok _ -> Assert.Fail("expected an unknown gate kind value to be rejected")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``load reports an unknown gate wiring value`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "gates:"
                  "  - id: bogus-wiring"
                  "    type: check"
                  "    kind: rhino-cli"
                  "    wiring: mystery"
                  "" ])

        match load root with
        | Error message ->
            Assert.Contains("gates[0].wiring", message)
            Assert.Contains("mystery", message)
        | Ok _ -> Assert.Fail("expected an unknown gate wiring value to be rejected")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``load reports an unknown gate carve-out value`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "gates:"
                  "  - id: bogus-carve-out"
                  "    type: check"
                  "    kind: rhino-cli"
                  "    wiring: matrix"
                  "    carve-out: mystery"
                  "" ])

        match load root with
        | Error message ->
            Assert.Contains("gates[0].carve-out", message)
            Assert.Contains("mystery", message)
        | Ok _ -> Assert.Fail("expected an unknown gate carve-out value to be rejected")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``load reports an unknown surface scope value under a complex (non-scalar) surface key`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "gates:"
                  "  - id: complex-surface-key"
                  "    surfaces:"
                  "      ? [pre-commit]"
                  "      : { scope: mystery-scope }"
                  "" ])

        match load root with
        | Error message ->
            Assert.Contains("scope", message)
            Assert.Contains("mystery-scope", message)
        | Ok _ -> Assert.Fail("expected an unknown surface scope value to be rejected")
    finally
        Directory.Delete(root, true)

// ---- parseRepoConfig: a genuinely empty document ----

[<Fact>]
let ``load returns the empty configuration for a genuinely empty repo-config.yml`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" ""

        match load root with
        | Ok config ->
            Assert.Empty(config.Harness)
            Assert.Empty(config.Gates)
        | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    finally
        Directory.Delete(root, true)

// ---- confinedRepoPath: existing-ancestor edge cases ----

[<Fact>]
let ``confinedRepoPath reports no existing ancestor for an entirely relative repoRoot`` () =
    match confinedRepoPath "definitely-not-a-real-relative-dir-xyz" "nested/value.json" with
    | Error message -> Assert.Contains("no existing repository ancestor", message)
    | Ok path -> Assert.Fail(sprintf "expected Error, got Ok %s" path)

[<Fact>]
let ``confinedRepoPath rejects a repoRoot that does not itself exist as escaping the repository root`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-cli-repo-config-unit-missing-" + Guid.NewGuid().ToString("N"))

    match confinedRepoPath root "nested/value.json" with
    | Error message -> Assert.Contains("escapes the repository root", message)
    | Ok path -> Assert.Fail(sprintf "expected Error, got Ok %s" path)

[<Fact>]
let ``confinedRepoPath surfaces a filesystem exception as an Error`` () =
    let root = newTempDir ()

    try
        match confinedRepoPath root ("nested/" + string (char 0) + "bad.json") with
        | Error message -> Assert.NotEqual<string>("", message)
        | Ok path -> Assert.Fail(sprintf "expected an exception-derived Error, got Ok %s" path)
    finally
        Directory.Delete(root, true)

// ---- globPatternError: character-class and wildcard edge cases ----

[<Fact>]
let ``globPatternError accepts a well-formed character-class range`` () =
    Assert.Equal<string option>(None, globPatternError "file[0-9].txt")

[<Fact>]
let ``globPatternError rejects a descending character-class range`` () =
    Assert.Equal(Some "Pattern syntax error near position 0: invalid range pattern", globPatternError "[9-0]")

[<Fact>]
let ``globPatternError accepts a literal close-bracket as the first class member`` () =
    Assert.Equal<string option>(None, globPatternError "[]abc]")

[<Fact>]
let ``globPatternError rejects an unclosed character class`` () =
    Assert.Equal(Some "Pattern syntax error near position 0: unclosed character class", globPatternError "[abc")

[<Fact>]
let ``globPatternError rejects three or more consecutive wildcards`` () =
    Assert.Equal(
        Some "Pattern syntax error near position 0: wildcards are either regular `*` or recursive `**`",
        globPatternError "***"
    )

[<Fact>]
let ``globPatternError rejects a recursive wildcard that does not form its own path component`` () =
    Assert.Equal(
        Some "Pattern syntax error near position 1: recursive wildcards must form a single path component",
        globPatternError "a**b"
    )

// ---- doctorToolsSemanticFindings: unknown and duplicate Doctor tools ----

[<Fact>]
let ``gateSemanticFindings reports unknown and duplicate Doctor tools`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "gates:"
                  "  - id: doctor-tools-gate"
                  "    doctor-tools:"
                  "      - git"
                  "      - git"
                  "      - mystery-tool"
                  "" ])

        let findings = gateSemanticFindings (loadOrDefault root)

        Assert.Contains(findings, (fun f -> f.Contains "unknown Doctor tool \"mystery-tool\""))
        Assert.Contains(findings, (fun f -> f.Contains "duplicate Doctor tool \"git\""))
    finally
        Directory.Delete(root, true)

// ---- lintStagedShellFindings: placement, blank, and placeholder-count checks ----

[<Fact>]
let ``gateSemanticFindings reports lint-staged-shell placement and blank findings together`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "gates:"
                  "  - id: shell-gate-placement-blank"
                  "    surfaces:"
                  "      ci:"
                  "        scope: all-file-type"
                  "        lint-staged-shell: \"   \""
                  "" ])

        let findings = gateSemanticFindings (loadOrDefault root)

        Assert.Contains(findings, (fun f -> f.Contains "only valid for pre-commit affected-file-type"))
        Assert.Contains(findings, (fun f -> f.Contains "must not be blank"))
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``gateSemanticFindings reports a repeated {command} placeholder`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "gates:"
                  "  - id: shell-gate-placeholder"
                  "    surfaces:"
                  "      pre-commit:"
                  "        scope: affected-file-type"
                  "        lint-staged-shell: \"{{command}} && {{command}}\""
                  "" ])

        let findings = gateSemanticFindings (loadOrDefault root)

        Assert.Contains(findings, (fun f -> f.Contains "{command} may appear at most once"))
    finally
        Directory.Delete(root, true)

// ---- gateSurfaceSemanticFindings: glob/trigger/nx-scope combinations ----

[<Fact>]
let ``gateSemanticFindings reports glob-scope, trigger-scope, missing-trigger, and nx-scope violations`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "gates:"
                  "  - id: surface-semantics-gate"
                  "    surfaces:"
                  "      pre-push:"
                  "        scope: other"
                  "        glob: \"*.md\""
                  "      ci:"
                  "        scope: all-file-type"
                  "        trigger:"
                  "          - some-trigger"
                  "      commit-msg:"
                  "        scope: path-gated"
                  "      pre-commit:"
                  "        scope: affected-projects"
                  "  - id: surface-semantics-nx-gate"
                  "    kind: nx"
                  "    surfaces:"
                  "      pre-push:"
                  "        scope: all-file-type"
                  "" ])

        let findings = gateSemanticFindings (loadOrDefault root)

        Assert.Contains(findings, (fun f -> f.Contains "glob and globs require a file scope"))
        Assert.Contains(findings, (fun f -> f.Contains "only valid for path-gated scope"))
        Assert.Contains(findings, (fun f -> f.Contains "path-gated scope requires at least one trigger"))
        Assert.Contains(findings, (fun f -> f.Contains "nx kind requires an affected-projects or all-projects scope"))
        Assert.Contains(findings, (fun f -> f.Contains "project scopes require kind nx"))
    finally
        Directory.Delete(root, true)

// ---- parseCoverageProjects: frozen legacy coverage block edge cases ----

[<Fact>]
let ``parseCoverageProjects tolerates a document that fails to parse as YAML`` () =
    match parseCoverageProjects "coverage: [this is not valid yaml:\n" with
    | Ok rows -> Assert.Empty(rows)
    | Error messages -> Assert.Fail(sprintf "expected Ok, got Error %A" messages)

[<Fact>]
let ``parseCoverageProjects returns no rows when the document root is not a mapping`` () =
    match parseCoverageProjects "- a\n- b\n" with
    | Ok rows -> Assert.Empty(rows)
    | Error messages -> Assert.Fail(sprintf "expected Ok, got Error %A" messages)

[<Fact>]
let ``parseCoverageProjects returns no rows when the coverage key is absent`` () =
    match parseCoverageProjects "unrelated: 1\n" with
    | Ok rows -> Assert.Empty(rows)
    | Error messages -> Assert.Fail(sprintf "expected Ok, got Error %A" messages)

[<Fact>]
let ``parseCoverageProjects rejects a row whose name is not a scalar value`` () =
    let data =
        String.concat
            "\n"
            [ "coverage:"
              "  projects:"
              "    - name:"
              "        nested: true"
              "      specs: \"foo/**\""
              "" ]

    match parseCoverageProjects data with
    | Error messages -> Assert.Contains(messages, (fun m -> m.Contains "requires both a name and a specs glob"))
    | Ok rows -> Assert.Fail(sprintf "expected Error, got Ok %A" rows)

[<Fact>]
let ``parseCoverageProjects defaults levels to empty when the levels key is not a sequence`` () =
    let data =
        String.concat
            "\n"
            [ "coverage:"
              "  projects:"
              "    - name: sample-project"
              "      specs: \"apps/sample/**\""
              "      levels: not-a-list"
              "" ]

    match parseCoverageProjects data with
    | Ok [ row ] ->
        Assert.Equal("sample-project", row.Name)
        Assert.Empty(row.Levels)
    | Ok rows -> Assert.Fail(sprintf "expected exactly one row, got %A" rows)
    | Error messages -> Assert.Fail(sprintf "expected Ok, got Error %A" messages)
