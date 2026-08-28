/// Plain xunit tests exercising `RhinoCli.Application.RepoConfig`'s
/// ownership/vendored machinery directly (`parseOwnershipClass`,
/// `pathsEqual`, `pathIsUnder`, the two cross-checks, the unknown-harness-key
/// structural check, and `validateAtRoot` end to end against hand-built
/// fixtures) — behaviour with no dedicated Gherkin scenario, or exercised
/// only indirectly there. Kept separate from `RepoConfigValidateSteps.fs`
/// (which binds only real, frozen feature-file scenarios) so this file can
/// grow test cases without inflating the plan's tracked Gherkin scenario
/// count — mirrors `RepoConfigUnitTests.fs`'s own rationale.
module RhinoCli.Tests.Unit.Steps.RepoConfigValidateUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Application.RepoConfig

let private newTempDir () =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-repo-config-validate-unit-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private writeFile (root: string) (relativePath: string) (content: string) =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
    File.WriteAllText(full, content)

/// A minimal `HarnessEntry`, built with an explicit type annotation and
/// updated via `with` in every test below — `HarnessEntryDto` declares the
/// same field labels (`Name`, `Tier`, `AgentDir`, ...), so a bare record
/// literal here would otherwise leave the compiler to pick between the two
/// candidate record types by label-set + declaration order rather than
/// intent.
let private defaultHarnessEntry: HarnessEntry =
    { Name = "probe"
      Tier = Generated
      AgentDir = None
      Mirrors = None
      ForbidDir = None
      SkillsDir = None
      SkillsMirrors = None
      Vendored = []
      Catalog = None
      Ownership = [] }

/// A minimal `OwnershipEntry`, for the same reason as `defaultHarnessEntry`
/// above (`OwnershipEntryDto` shares its field labels).
let private defaultOwnershipEntry: OwnershipEntry =
    { Path = "somewhere"
      Class = ClassSource
      Reason = None }

// ---- pathsEqual ----

[<Fact>]
let ``pathsEqual treats identical paths as equal`` () =
    Assert.True(pathsEqual ".agents/skills/probe" ".agents/skills/probe")

[<Fact>]
let ``pathsEqual tolerates a trailing separator difference`` () =
    Assert.True(pathsEqual ".agents/skills/probe/" ".agents/skills/probe")

[<Fact>]
let ``pathsEqual rejects a real typo`` () =
    Assert.False(pathsEqual ".agents/skills/porbe" ".agents/skills/probe")

// ---- pathIsUnder ----

[<Fact>]
let ``pathIsUnder is true for a direct child`` () =
    Assert.True(pathIsUnder ".agents/skills/probe" ".agents/skills")

[<Fact>]
let ``pathIsUnder is true for the directory itself`` () =
    Assert.True(pathIsUnder ".agents/skills" ".agents/skills")

[<Fact>]
let ``pathIsUnder is false for a sibling directory`` () =
    Assert.False(pathIsUnder ".agents/other/probe" ".agents/skills")

[<Fact>]
let ``pathIsUnder is false when dir is empty`` () =
    Assert.False(pathIsUnder ".agents/skills/probe" "")

// ---- vendoredMissingFromOwnershipBackedList ----

[<Fact>]
let ``vendoredMissingFromOwnershipBackedList is empty when skills-dir is unset`` () =
    let entry =
        { defaultHarnessEntry with
            Ownership =
                [ { defaultOwnershipEntry with
                      Path = ".agents/skills/probe"
                      Class = ClassVendored
                      Reason = Some "reason" } ] }

    Assert.Empty(vendoredMissingFromOwnershipBackedList 0 entry)

[<Fact>]
let ``vendoredMissingFromOwnershipBackedList finds an ownership entry with no matching vendored entry`` () =
    let entry =
        { defaultHarnessEntry with
            SkillsDir = Some ".agents/skills"
            Ownership =
                [ { defaultOwnershipEntry with
                      Path = ".agents/skills/probe"
                      Class = ClassVendored
                      Reason = Some "reason" } ] }

    let findings = vendoredMissingFromOwnershipBackedList 0 entry
    Assert.Single(findings) |> ignore
    Assert.Contains(".agents/skills/probe", List.head findings)
    Assert.Contains("no matching harness[0].vendored", List.head findings)

[<Fact>]
let ``vendoredMissingFromOwnershipBackedList is empty when the vendored entry matches`` () =
    let entry =
        { defaultHarnessEntry with
            SkillsDir = Some ".agents/skills"
            Vendored = [ ".agents/skills/probe" ]
            Ownership =
                [ { defaultOwnershipEntry with
                      Path = ".agents/skills/probe"
                      Class = ClassVendored
                      Reason = Some "reason" } ] }

    Assert.Empty(vendoredMissingFromOwnershipBackedList 0 entry)

[<Fact>]
let ``vendoredMissingFromOwnershipBackedList ignores ownership entries outside skills-dir`` () =
    let entry =
        { defaultHarnessEntry with
            SkillsDir = Some ".agents/skills"
            Ownership =
                [ { defaultOwnershipEntry with
                      Path = ".codex/config.toml"
                      Class = ClassVendored
                      Reason = Some "reason" } ] }

    Assert.Empty(vendoredMissingFromOwnershipBackedList 0 entry)

// ---- vendoredWithoutOwnershipEntry ----

[<Fact>]
let ``vendoredWithoutOwnershipEntry finds a vendored entry with no matching ownership declaration`` () =
    let entry =
        { defaultHarnessEntry with
            SkillsDir = Some ".agents/skills"
            Vendored = [ ".agents/skills/probe" ] }

    let findings = vendoredWithoutOwnershipEntry 0 entry
    Assert.Single(findings) |> ignore
    Assert.Contains(".agents/skills/probe", List.head findings)
    Assert.Contains("no matching harness[0].ownership", List.head findings)

[<Fact>]
let ``vendoredWithoutOwnershipEntry is empty when the ownership declaration matches`` () =
    let entry =
        { defaultHarnessEntry with
            SkillsDir = Some ".agents/skills"
            Vendored = [ ".agents/skills/probe" ]
            Ownership =
                [ { defaultOwnershipEntry with
                      Path = ".agents/skills/probe"
                      Class = ClassVendored
                      Reason = Some "reason" } ] }

    Assert.Empty(vendoredWithoutOwnershipEntry 0 entry)

[<Fact>]
let ``vendoredWithoutOwnershipEntry rejects a matching path declared under the wrong class`` () =
    let entry =
        { defaultHarnessEntry with
            SkillsDir = Some ".agents/skills"
            Vendored = [ ".agents/skills/probe" ]
            Ownership =
                [ { defaultOwnershipEntry with
                      Path = ".agents/skills/probe"
                      Class = ClassGenerated
                      Reason = None } ] }

    Assert.Single(vendoredWithoutOwnershipEntry 0 entry) |> ignore

// ---- harnessEntrySemanticFindings: reason required for vendored ----

[<Fact>]
let ``harnessEntrySemanticFindings rejects an empty reason on a vendored declaration`` () =
    let entry =
        { defaultHarnessEntry with
            Ownership =
                [ { defaultOwnershipEntry with
                      Path = "somewhere"
                      Class = ClassVendored
                      Reason = Some "   " } ] }

    let findings = harnessEntrySemanticFindings 0 entry
    Assert.Single(findings) |> ignore
    Assert.Contains("required non-empty value", List.head findings)

[<Fact>]
let ``harnessEntrySemanticFindings rejects a missing reason on a vendored declaration`` () =
    let entry =
        { defaultHarnessEntry with
            Ownership =
                [ { defaultOwnershipEntry with
                      Path = "somewhere"
                      Class = ClassVendored
                      Reason = None } ] }

    Assert.Single(harnessEntrySemanticFindings 0 entry) |> ignore

[<Fact>]
let ``harnessEntrySemanticFindings does not require a reason on source or generated declarations`` () =
    let entry =
        { defaultHarnessEntry with
            Ownership =
                [ { defaultOwnershipEntry with
                      Path = "a"
                      Class = ClassSource
                      Reason = None }
                  { defaultOwnershipEntry with
                      Path = "b"
                      Class = ClassGenerated
                      Reason = None } ] }

    Assert.Empty(harnessEntrySemanticFindings 0 entry)

// ---- load: ownership parsing ----

[<Fact>]
let ``load parses a well-formed ownership entry`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "harness:"
                  "  - name: probe"
                  "    tier: generated"
                  "    skills-dir: .agents/skills"
                  "    skills-mirrors: .claude/skills"
                  "    vendored:"
                  "      - .agents/skills/example"
                  "    ownership:"
                  "      - { path: .agents/skills/example, class: vendored, reason: third-party payload }"
                  "" ])

        match load root with
        | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
        | Ok config ->
            let entry = config.Harness |> List.find (fun h -> h.Name = "probe")
            Assert.Equal<string option>(Some ".agents/skills", entry.SkillsDir)
            Assert.Equal<string option>(Some ".claude/skills", entry.SkillsMirrors)
            Assert.Equal<string list>([ ".agents/skills/example" ], entry.Vendored)
            let owned = Assert.Single(entry.Ownership)
            Assert.Equal(".agents/skills/example", owned.Path)
            Assert.Equal(ClassVendored, owned.Class)
            Assert.Equal<string option>(Some "third-party payload", owned.Reason)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``load rejects an ownership entry declaring a fourth class value`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "harness:"
                  "  - name: probe"
                  "    tier: generated"
                  "    ownership:"
                  "      - { path: somewhere, class: bespoke, reason: nope }"
                  "" ])

        match load root with
        | Error message ->
            Assert.Contains("harness[0].ownership[0].class", message)
            Assert.Contains("bespoke", message)
        | Ok _ -> Assert.Fail("expected a fourth class value to be rejected")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``load rejects an ownership entry with a missing class key`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "harness:"
                  "  - name: probe"
                  "    tier: generated"
                  "    ownership:"
                  "      - { path: somewhere }"
                  "" ])

        match load root with
        | Error message -> Assert.Contains("required key is missing", message)
        | Ok _ -> Assert.Fail("expected a missing class key to be rejected")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``a harness entry with no ownership carries an empty ownership list`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "harness:\n  - name: probe\n    tier: source\n"

        match load root with
        | Ok config ->
            let entry = config.Harness |> List.find (fun h -> h.Name = "probe")
            Assert.Empty(entry.Ownership)
            Assert.Empty(entry.Vendored)
            Assert.Equal<string option>(None, entry.SkillsDir)
            Assert.Equal<string option>(None, entry.SkillsMirrors)
        | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
    finally
        Directory.Delete(root, true)

// ---- load: unknown-key structural check ----

[<Fact>]
let ``load rejects an unknown key inside a harness entry`` () =
    let root = newTempDir ()

    try
        writeFile root "repo-config.yml" "harness:\n  - name: probe\n    tier: source\n    bogus-key: true\n"

        match load root with
        | Error message -> Assert.Contains("harness[0]: unknown key \"bogus-key\"", message)
        | Ok _ -> Assert.Fail("expected an unknown harness key to be rejected")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``load rejects an unknown key inside an ownership entry`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "harness:"
                  "  - name: probe"
                  "    tier: source"
                  "    ownership:"
                  "      - { path: somewhere, class: source, resaon: typo }"
                  "" ])

        match load root with
        | Error message -> Assert.Contains("harness[0].ownership[0]: unknown key \"resaon\"", message)
        | Ok _ -> Assert.Fail("expected an unknown ownership key to be rejected")
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``load accepts every recognised harness and ownership key`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "harness:"
                  "  - name: probe"
                  "    tier: generated"
                  "    agent-dir: .probe/agents"
                  "    skills-dir: .probe/skills"
                  "    rules-dir: .probe/rules"
                  "    agent-name: probe"
                  "    mirrors: .claude/agents"
                  "    skills-mirrors: .claude/skills"
                  "    vendored: []"
                  "    config: .probe/config.toml"
                  "    forbid-dir: .probe/forbidden"
                  "    shadow: true"
                  "    instruction:"
                  "      - AGENTS.md"
                  "    catalog:"
                  "      platform: Probe"
                  "    ownership:"
                  "      - { path: somewhere, class: source, reason: fine }"
                  "" ])

        match load root with
        | Ok _ -> ()
        | Error message -> Assert.Fail(sprintf "expected every recognised key to be accepted, got Error %s" message)
    finally
        Directory.Delete(root, true)

// ---- semanticFindings: harness-entry findings folded in ----

[<Fact>]
let ``semanticFindings includes harness ownership findings alongside the doctor path finding`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "doctor:"
                  "  dotnet-global-json: ./bad-path.json"
                  "harness:"
                  "  - name: probe"
                  "    tier: generated"
                  "    ownership:"
                  "      - { path: somewhere, class: vendored, reason: \"\" }"
                  "" ])

        match load root with
        | Error message -> Assert.Fail(sprintf "expected Ok, got Error %s" message)
        | Ok config ->
            let findings = semanticFindings config
            Assert.True(findings.Length >= 2, sprintf "expected at least two findings, got %A" findings)
            Assert.True(findings |> List.exists (fun f -> f.Contains("dotnet-global-json")))
            Assert.True(findings |> List.exists (fun f -> f.Contains("required non-empty value")))
    finally
        Directory.Delete(root, true)

// ---- validateAtRoot: end to end against the cross-checks ----

[<Fact>]
let ``validateAtRoot fails when a vendored ownership declaration has no matching vendored entry`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "harness:"
                  "  - name: probe"
                  "    tier: generated"
                  "    skills-dir: .agents/skills"
                  "    ownership:"
                  "      - { path: .agents/skills/probe, class: vendored, reason: fine }"
                  "" ])

        let ok, output = validateAtRoot root
        Assert.False(ok, output)
        Assert.Contains(".agents/skills/probe", output)
        Assert.Contains("no matching harness[0].vendored", output)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``validateAtRoot fails when a vendored entry has no matching ownership declaration`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "harness:"
                  "  - name: probe"
                  "    tier: generated"
                  "    skills-dir: .agents/skills"
                  "    vendored:"
                  "      - .agents/skills/probe"
                  "" ])

        let ok, output = validateAtRoot root
        Assert.False(ok, output)
        Assert.Contains(".agents/skills/probe", output)
        Assert.Contains("no matching harness[0].ownership", output)
    finally
        Directory.Delete(root, true)

[<Fact>]
let ``validateAtRoot passes when vendored and ownership agree`` () =
    let root = newTempDir ()

    try
        writeFile
            root
            "repo-config.yml"
            (String.concat
                "\n"
                [ "harness:"
                  "  - name: probe"
                  "    tier: generated"
                  "    skills-dir: .agents/skills"
                  "    vendored:"
                  "      - .agents/skills/probe"
                  "    ownership:"
                  "      - { path: .agents/skills/probe, class: vendored, reason: third-party payload }"
                  "" ])

        let ok, output = validateAtRoot root
        Assert.True(ok, output)
    finally
        Directory.Delete(root, true)
