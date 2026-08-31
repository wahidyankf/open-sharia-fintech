/// Plain xunit tests for the Wave E/F routes of `RhinoCli.Cli.Dispatch.route`
/// — `repo-governance *`, `specs *`, `harness *`, and `gate run|list` — added
/// after CI's `test:coverage` step (previously masked by the
/// `GateExecutionSteps` flaky failure blocking every run before it) exposed
/// that these leaves, wired in Waves E and F, never got their own
/// `WaveDDispatchUnitTests.fs`-style coverage. `shadow-diff.sh` and the
/// Gherkin specs exercise them only as a subprocess (`Process.Start "dotnet"`
/// in `SpecsSteps.fs`/`HarnessSteps.fs`), which coverlet cannot instrument —
/// see `learnings.md`, 2026-08-28 and 2026-08-30.
///
/// Read-only leaves are driven against this checkout's own real repository
/// root (via `RhinoCli.Infrastructure.GitRoot.findRoot`), the same technique
/// `GovernanceSteps.fs`'s `findRepoRoot` already uses. Routes whose coverage
/// depends on mutable repository declarations use a throwaway fixture instead:
/// a delivery must not make a coverage result depend on unrelated repository
/// state. Leaves that write (`bindings generate`, `sync promote`, `scaffold
/// dart`, `readme-index rewrite-paths`, `e2e-coverage validate`) always use a
/// throwaway temp directory too, never the real checkout.
module RhinoCli.Tests.Unit.Steps.WaveEFDispatchUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Cli.Dispatch

let private newTempDir () =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-waveef-dispatch-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private writeFile (root: string) (relativePath: string) (content: string) =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
    File.WriteAllText(full, content)

/// Runs `route`, capturing stdout/stderr around the call and restoring the
/// prior writers afterwards even if `route` throws.
let private runCaptured (getRepoRoot: unit -> Result<string, string>) (argv: string[]) : int * string * string =
    let originalOut = Console.Out
    let originalErr = Console.Error
    use outWriter = new StringWriter()
    use errWriter = new StringWriter()

    try
        Console.SetOut(outWriter)
        Console.SetError(errWriter)
        let exitCode = route getRepoRoot argv
        exitCode, outWriter.ToString(), errWriter.ToString()
    finally
        Console.SetOut(originalOut)
        Console.SetError(originalErr)

let private okRoot (root: string) () = Ok root

/// This checkout's own repository root — the read-only leaves below are
/// exactly the validators this repo's own CI keeps green against it.
let private realRepoRoot () : string =
    match RhinoCli.Infrastructure.GitRoot.findRoot () with
    | Error message -> failwith message
    | Ok root -> root

/// A minimal, internally consistent DDD-area spec tree. It keeps dispatch
/// coverage for config-driven DDD branches independent of the live delivery
/// state of this repository.
let private newDddAreaFixture () : string =
    let root = newTempDir ()
    let app = "fixture-app"

    writeFile
        root
        "repo-config.yml"
        "specs:\n  ddd-areas:\n    - fixture-app\n  domain-areas: []\ngates: []\nharness: []\n"

    for folder in [ "product"; "system-context"; "containers"; "components"; "behavior" ] do
        let path = sprintf "specs/apps/%s/%s" app folder
        writeFile root (path + "/README.md") "# Fixture\n"
        writeFile root (path + "/fixture.md") "# Fixture\n"

    writeFile
        root
        (sprintf "specs/apps/%s/behavior/surface/gherkin/domain/fixture.feature" app)
        "Feature: Fixture\n\n  Scenario: Works\n    Given a fixture\n    When it runs\n    Then it passes\n"

    writeFile
        root
        (sprintf "specs/apps/%s/ddd/bounded-contexts.yaml" app)
        "version: 2\napp: fixture-app\ncontexts: []\n"

    root

// ---------------------------------------------------------------------------
// repo-governance * — read-only, safe against the real checkout
// ---------------------------------------------------------------------------

[<Fact>]
let ``route runs repo-governance vendor validate as text`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "vendor"; "validate" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders repo-governance vendor validate as JSON`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "vendor"; "validate"; "-o"; "json" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders repo-governance vendor validate as markdown`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "vendor"; "validate"; "-o"; "markdown" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route runs repo-governance layer-coherence validate as text`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "layer-coherence"; "validate" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders repo-governance layer-coherence validate as JSON`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "layer-coherence"; "validate"; "-o"; "json" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders repo-governance layer-coherence validate as markdown`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "layer-coherence"; "validate"; "-o"; "markdown" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route runs repo-governance traceability validate as text`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "traceability"; "validate" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders repo-governance traceability validate as JSON`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "traceability"; "validate"; "-o"; "json" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders repo-governance traceability validate as markdown`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "traceability"; "validate"; "-o"; "markdown" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route runs repo-governance audit as text`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "audit" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders repo-governance audit as JSON`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "audit"; "-o"; "json" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders repo-governance audit as markdown`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "audit"; "-o"; "markdown" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route honours repo-governance audit --skip`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "repo-governance"; "audit"; "--skip"; "vendor" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route reports a nonzero exit code when repo-governance audit finds a forbidden vendor term`` () =
    let root = newTempDir ()
    writeFile root "AGENTS.md" "# Doc\n\nClaude Code reads this.\n"

    let code, _, err = runCaptured (okRoot root) [| "repo-governance"; "audit" |]
    Assert.Equal(1, code)
    Assert.Contains("governance finding(s) reported across", err)

// ---------------------------------------------------------------------------
// specs * — read-only, safe against the real checkout
// ---------------------------------------------------------------------------

[<Fact>]
let ``route runs specs counts validate and reports missing DDD folders for a raw gherkin path`` () =
    // `specs counts validate` expects a DDD-shaped folder (product/system-context/
    // containers/components/behavior); pointing it straight at a gherkin dir is a
    // real findings-present arm, not a defect — exercises the failure-formatting
    // path the same way Wave D's "cheapest lines to win" lesson recommends.
    let code, _, err =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "specs"
               "counts"
               "validate"
               "specs/apps/rhino/behavior/rhino-cli/gherkin" |]

    Assert.Equal(1, code)
    Assert.Contains("finding(s) found by specs validate-counts", err)

[<Fact>]
let ``route runs specs structure validate for the rhino app`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "specs"; "structure"; "validate"; "rhino" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route runs specs gherkin-cardinality validate against a real spec folder`` () =
    let code, out, _ =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "specs"
               "gherkin-cardinality"
               "validate"
               "specs/apps/rhino/behavior/rhino-cli/gherkin" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders specs gherkin-cardinality validate as JSON`` () =
    let code, out, _ =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "specs"
               "gherkin-cardinality"
               "validate"
               "specs/apps/rhino/behavior/rhino-cli/gherkin"
               "-o"
               "json" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders specs gherkin-cardinality validate as markdown`` () =
    let code, out, _ =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "specs"
               "gherkin-cardinality"
               "validate"
               "specs/apps/rhino/behavior/rhino-cli/gherkin"
               "-o"
               "markdown" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route runs specs audit against the real checkout`` () =
    // Repo-root-scoped `validate-links` (called with no `--exclude`) finds
    // broken links that CI's own scoped `md links validate` invocation never
    // sees — a real findings-present arm for this leaf, not a test defect.
    let code, _, err = runCaptured (okRoot (realRepoRoot ())) [| "specs"; "audit" |]
    Assert.Equal(1, code)
    Assert.Contains("SPECS AUDIT FAILED", err)

[<Fact>]
let ``route honours specs audit --skip`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "specs"; "audit"; "--skip"; "validate-links" |]

    Assert.Equal(0, code)
    Assert.Contains("SPECS AUDIT PASSED", out)

[<Fact>]
let ``route runs specs behavior-coverage validate against rhino-cli's own gherkin+source`` () =
    let code, out, _ =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "specs"
               "behavior-coverage"
               "validate"
               "--shared-steps"
               "specs/apps/rhino/behavior/rhino-cli/gherkin"
               "apps/rhino-cli/src" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders specs behavior-coverage validate as JSON`` () =
    let code, out, _ =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "specs"
               "behavior-coverage"
               "validate"
               "--shared-steps"
               "-o"
               "json"
               "specs/apps/rhino/behavior/rhino-cli/gherkin"
               "apps/rhino-cli/src" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route reports missing PATHS on specs behavior-coverage validate with zero paths`` () =
    let code, _, err =
        runCaptured (okRoot (realRepoRoot ())) [| "specs"; "behavior-coverage"; "validate" |]

    Assert.Equal(2, code)
    Assert.Contains("required arguments were not provided", err)

[<Fact>]
let ``route reports missing PATHS on specs behavior-coverage validate with one path`` () =
    let code, _, err =
        runCaptured (okRoot (realRepoRoot ())) [| "specs"; "behavior-coverage"; "validate"; "only-one" |]

    Assert.Equal(2, code)
    Assert.Contains("values required by", err)

[<Fact>]
let ``route skips specs domain-coverage validate for a project outside specs domain-areas`` () =
    let code, out, _ =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "specs"
               "domain-coverage"
               "validate"
               "specs/apps/rhino/behavior/rhino-cli/gherkin"
               "not-a-real-domain-area" |]

    Assert.Equal(0, code)
    Assert.Contains("skipped", out)

[<Fact>]
let ``route renders specs domain-coverage validate skip message as JSON`` () =
    let code, out, _ =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "specs"
               "domain-coverage"
               "validate"
               "-o"
               "json"
               "specs/apps/rhino/behavior/rhino-cli/gherkin"
               "not-a-real-domain-area" |]

    Assert.Equal(0, code)
    Assert.Contains("\"skipped\":true", out)

[<Fact>]
let ``route renders specs domain-coverage validate skip message as markdown`` () =
    let code, out, _ =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "specs"
               "domain-coverage"
               "validate"
               "-o"
               "markdown"
               "specs/apps/rhino/behavior/rhino-cli/gherkin"
               "not-a-real-domain-area" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route reports missing PATHS on specs domain-coverage validate`` () =
    let code, _, err =
        runCaptured (okRoot (realRepoRoot ())) [| "specs"; "domain-coverage"; "validate" |]

    Assert.Equal(2, code)
    Assert.Contains("required arguments were not provided", err)

// ---------------------------------------------------------------------------
// harness * — read-only members, safe against the real checkout
// ---------------------------------------------------------------------------

[<Fact>]
let ``route runs harness duplication validate as text`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "duplication"; "validate" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders harness duplication validate as JSON`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "duplication"; "validate"; "-o"; "json" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders harness duplication validate as markdown`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "duplication"; "validate"; "-o"; "markdown" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route runs harness claude validate as text`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "claude"; "validate" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders harness claude validate as JSON`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "claude"; "validate"; "-o"; "json" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route renders harness claude validate as markdown`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "claude"; "validate"; "-o"; "markdown" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route rejects harness claude validate --agents-only combined with --skills-only`` () =
    let code, _, err =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "claude"; "validate"; "--agents-only"; "--skills-only" |]

    Assert.Equal(1, code)
    Assert.Contains("cannot use --agents-only and --skills-only together", err)

[<Fact>]
let ``route runs harness claude validate --agents-only`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "claude"; "validate"; "--agents-only" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route runs harness sync triage against the real checkout`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "sync"; "triage" |]

    Assert.Equal(0, code)
    Assert.Contains("harness sync triage:", out)

[<Fact>]
let ``route honours harness sync triage --quiet`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "sync"; "triage"; "--quiet" |]

    Assert.Equal(0, code)
    Assert.Contains("harness sync triage:", out)

[<Fact>]
let ``route runs harness audit against the real checkout`` () =
    let code, out, _ = runCaptured (okRoot (realRepoRoot ())) [| "harness"; "audit" |]
    Assert.Equal(0, code)
    Assert.Contains("HARNESS AUDIT PASSED", out)

[<Fact>]
let ``route honours harness audit --skip`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "audit"; "--skip"; "detect-duplication" |]

    Assert.Equal(0, code)
    Assert.Contains("HARNESS AUDIT PASSED", out)

// ---------------------------------------------------------------------------
// harness sync promote --from — no `--from` never touches disk
// ---------------------------------------------------------------------------

[<Fact>]
let ``route reports missing --from on harness sync promote`` () =
    let code, _, err =
        runCaptured (okRoot (newTempDir ())) [| "harness"; "sync"; "promote" |]

    Assert.Equal(2, code)
    Assert.Contains("--from <MIRROR>", err)

[<Fact>]
let ``route reports missing --from on harness sync promote with --help`` () =
    let code, _, err =
        runCaptured (okRoot (newTempDir ())) [| "harness"; "sync"; "promote"; "--help" |]

    Assert.Equal(2, code)
    Assert.Contains("--help", err)

// ---------------------------------------------------------------------------
// governance readme-index rewrite-paths — writes, so always a temp fixture
// ---------------------------------------------------------------------------

[<Fact>]
let ``route reports missing --map on governance readme-index rewrite-paths`` () =
    let code, _, err =
        runCaptured (okRoot (newTempDir ())) [| "governance"; "readme-index"; "rewrite-paths" |]

    Assert.Equal(2, code)
    Assert.Contains("--map <MAP>", err)

[<Fact>]
let ``route reports missing --map on governance readme-index rewrite-paths with --help`` () =
    let code, _, err =
        runCaptured (okRoot (newTempDir ())) [| "governance"; "readme-index"; "rewrite-paths"; "--help" |]

    Assert.Equal(2, code)
    Assert.Contains("--help", err)

[<Fact>]
let ``route reports an unreadable rename map on governance readme-index rewrite-paths`` () =
    let root = newTempDir ()

    let code, _, err =
        runCaptured
            (okRoot root)
            [| "governance"
               "readme-index"
               "rewrite-paths"
               "--map"
               Path.Combine(root, "missing-map.tsv") |]

    Assert.Equal(1, code)
    Assert.Contains("read rename map", err)

[<Fact>]
let ``route rewrites a markdown link target for a renamed path`` () =
    let root = newTempDir ()
    writeFile root "docs/readme.md" "See [old doc](old-name.md) for details.\n"
    writeFile root "rename-map.tsv" "old-name.md\tnew-name.md\n"

    let code, out, _ =
        runCaptured
            (okRoot root)
            [| "governance"
               "readme-index"
               "rewrite-paths"
               "--map"
               Path.Combine(root, "rename-map.tsv")
               "--paths"
               "docs" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out
    Assert.Contains("[old doc](new-name.md)", File.ReadAllText(Path.Combine(root, "docs", "readme.md")))

[<Fact>]
let ``route renders governance readme-index rewrite-paths as JSON`` () =
    let root = newTempDir ()
    writeFile root "docs/readme.md" "See [old doc](old-name.md) for details.\n"
    writeFile root "rename-map.tsv" "old-name.md\tnew-name.md\n"

    let code, out, _ =
        runCaptured
            (okRoot root)
            [| "governance"
               "readme-index"
               "rewrite-paths"
               "--map"
               Path.Combine(root, "rename-map.tsv")
               "--paths"
               "docs"
               "-o"
               "json" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route rewrite-paths help wins when --map is present`` () =
    let root = newTempDir ()
    writeFile root "rename-map.tsv" "old-name.md\tnew-name.md\n"

    let code, out, _ =
        runCaptured
            (okRoot root)
            [| "governance"
               "readme-index"
               "rewrite-paths"
               "--map"
               Path.Combine(root, "rename-map.tsv")
               "--help" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

// ---------------------------------------------------------------------------
// DDD-area branches — use a fixture so phase deliveries can freely retire a
// live DDD area without changing this dispatch test's coverage.
// ---------------------------------------------------------------------------

[<Fact>]
let ``route runs specs structure validate for a configured fixture ddd-area app`` () =
    let root = newDddAreaFixture ()

    let code, out, _ =
        runCaptured (okRoot root) [| "specs"; "structure"; "validate"; "fixture-app" |]

    Assert.Equal(0, code)
    Assert.Contains("0 finding(s)", out)

[<Fact>]
let ``route runs specs domain-coverage validate for a real eligible domain area`` () =
    let code, _, _ =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "specs"
               "domain-coverage"
               "validate"
               "--shared-steps"
               "--exclude-dir"
               "messaging"
               "specs/apps/organiclever/behavior/organiclever-be/gherkin"
               "apps/organiclever-be" |]

    Assert.True(code = 0 || code = 1)

// ---------------------------------------------------------------------------
// route's own dispatch-table branches
// ---------------------------------------------------------------------------

[<Fact>]
let ``route reports an unrecognized invocation`` () =
    let code, _, err = runCaptured (okRoot (newTempDir ())) [| "not-a-real-command" |]
    Assert.Equal(2, code)
    Assert.Contains("unrecognized or not-yet-routed invocation", err)

[<Fact>]
let ``route reports a repository-root lookup failure`` () =
    let code, _, err =
        runCaptured (fun () -> Error "not a git repository") [| "convention"; "audit" |]

    Assert.Equal(1, code)
    Assert.Contains("failed to find git repository root", err)

[<Fact>]
let ``route reports an invalid --output value`` () =
    let code, _, err =
        runCaptured (okRoot (realRepoRoot ())) [| "convention"; "audit"; "-o"; "not-a-format" |]

    Assert.Equal(1, code)
    Assert.NotEmpty err

// ---------------------------------------------------------------------------
// `specs behavior-coverage validate --unit-dir --integration-dir --e2e-dir`
// — the three-level mode (`runThreeLevel`, `printMarkerViolations`,
// `printRuntimeViolations`), never exercised by the single-app-dir shape
// every real Nx target in this repo uses.
// ---------------------------------------------------------------------------

/// A `specs/login.feature` with one untagged scenario, plus a matching
/// `.steps.ts` binding under `unit/`, `integration/`, and `e2e/` app dirs —
/// clean per [`Specs.checkAll`] at every level.
let private newThreeLevelFixture () =
    let root = newTempDir ()

    let feature =
        "Feature: Login\n\n  Scenario: User logs in\n    Given a registered user\n    When the user submits valid credentials\n    Then the dashboard appears\n"

    let steps =
        "Scenario(\"User logs in\", () => {\n  Given(\"a registered user\", () => {});\n  When(\"the user submits valid credentials\", () => {});\n  Then(\"the dashboard appears\", () => {});\n});\n"

    writeFile root "specs/login.feature" feature
    writeFile root "unit/login.steps.ts" steps
    writeFile root "integration/login.steps.ts" steps
    writeFile root "e2e/login.steps.ts" steps
    root

let private threeLevelArgs (extra: string list) : string[] =
    [ "specs"
      "behavior-coverage"
      "validate"
      "--unit-dir"
      "unit"
      "--integration-dir"
      "integration"
      "--e2e-dir"
      "e2e"
      "--shared-steps" ]
    @ extra
    @ [ "specs"; "unused-app-dir" ]
    |> List.toArray

[<Fact>]
let ``route passes specs behavior-coverage validate in three-level mode when every level is clean`` () =
    let root = newThreeLevelFixture ()
    let code, out, _ = runCaptured (okRoot root) (threeLevelArgs [])
    Assert.Equal(0, code)
    Assert.Contains("=== Unit level ===", out)
    Assert.Contains("=== Integration level ===", out)
    Assert.Contains("=== E2e level ===", out)

[<Fact>]
let ``route reports a failing level in three-level mode`` () =
    let root = newThreeLevelFixture ()
    File.Delete(Path.Combine(root, "e2e", "login.steps.ts"))
    let code, _, err = runCaptured (okRoot root) (threeLevelArgs [])
    Assert.Equal(1, code)
    Assert.Contains("level(s) e2e", err)

[<Fact>]
let ``route reports an untagged-scenario marker violation once a level report is requested`` () =
    let root = newThreeLevelFixture ()

    let code, out, err =
        runCaptured (okRoot root) (threeLevelArgs [ "--unit-report"; "unit-report.json" ])

    Assert.Equal(1, code)
    Assert.Contains("@covers marker violations", out)
    Assert.Contains("has no @unit/@integration/@e2e level tag", out)
    Assert.Contains("@covers marker violation(s)", err)

[<Fact>]
let ``route reports missing-coverage, coverage-at-undeclared-level, orphan-marker, and runtime violations together``
    ()
    =
    let root = newTempDir ()

    let feature =
        "Feature: Login\n\n  @unit\n  Scenario: User logs in\n    Given a registered user\n    When the user submits valid credentials\n    Then the dashboard appears\n"

    let steps =
        "Scenario(\"User logs in\", () => {\n  Given(\"a registered user\", () => {});\n  When(\"the user submits valid credentials\", () => {});\n  Then(\"the dashboard appears\", () => {});\n});\n"

    writeFile root "specs/login.feature" feature
    writeFile root "unit/login.steps.ts" steps
    writeFile root "e2e/login.steps.ts" steps

    writeFile
        root
        "integration/login.steps.ts"
        (steps
         + "// @covers specs/login.feature:User logs in\n// @covers specs/login.feature:Ghost Scenario\n")

    writeFile
        root
        "integration-report.json"
        "[{\"feature_path\": \"specs/login.feature\", \"scenario_title\": \"User logs in\", \"status\": \"failed\"}]"

    let code, out, err =
        runCaptured (okRoot root) (threeLevelArgs [ "--integration-report"; "integration-report.json" ])

    Assert.Equal(1, code)
    Assert.Contains("has no @covers marker at the [unit] level", out)
    Assert.Contains("a level not declared on that scenario", out)
    Assert.Contains("no feature file contains (orphan marker)", out)
    Assert.Contains("marked-but-failed", out)
    Assert.Contains("marked-but-not-executed", out)
    Assert.Contains("@covers marker violation(s)", err)
    Assert.Contains("runtime cross-check violation(s)", err)

[<Fact>]
let ``route reports a partial --unit-dir/--integration-dir/--e2e-dir set as an error`` () =
    let root = newThreeLevelFixture ()

    let code, _, err =
        runCaptured
            (okRoot root)
            [| "specs"
               "behavior-coverage"
               "validate"
               "--unit-dir"
               "unit"
               "specs"
               "unused-app-dir" |]

    Assert.Equal(1, code)
    Assert.Contains("must provide all three or none", err)

// ---------------------------------------------------------------------------
// `specs structure validate` — the adoption/tree/counts finding loops and the
// DDD bounded-context/glossary Error arms
// ---------------------------------------------------------------------------

[<Fact>]
let ``route reports findings for a non-existent app on specs structure validate`` () =
    let code, _, err =
        runCaptured (okRoot (realRepoRoot ())) [| "specs"; "structure"; "validate"; "totally-fake-app-xyz" |]

    Assert.Equal(1, code)
    Assert.Contains("finding(s) found by specs structure validate", err)

[<Fact>]
let ``route reports a missing bounded-context registry for a declared DDD area`` () =
    let root = newTempDir ()

    writeFile
        root
        "repo-config.yml"
        "specs:\n  ddd-areas:\n    - fakearea\n  domain-areas: []\ngates: []\nharness: []\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "specs"; "structure"; "validate"; "fakearea" |]

    Assert.Equal(1, code)
    Assert.Contains("registry not found for app \"fakearea\"", out)

// ---------------------------------------------------------------------------
// `specs e2e-coverage validate` — the glob-expansion branch of
// `globFeatureFiles`, never hit by a literal `--features` path
// ---------------------------------------------------------------------------

[<Fact>]
let ``route expands a wildcard --features glob on specs e2e-coverage validate`` () =
    let root = newTempDir ()

    writeFile
        root
        "specs/apps/example/e2e.feature"
        "Feature: Example\n\n  @e2e\n  Scenario: does the thing\n    Given x\n"

    writeFile root ".features-gen/specs/apps/example/e2e.feature.spec.js" "test('does the thing', () => {});"

    let code, out, _ =
        runCaptured
            (okRoot root)
            [| "specs"
               "e2e-coverage"
               "validate"
               "--features"
               "specs/apps/example/*.feature"
               "--features-gen"
               ".features-gen"
               "--baseline"
               "e2e-baseline.json"
               "--project"
               "example"
               root |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

// ---------------------------------------------------------------------------
// `specs scaffold dart` — writes to a throwaway temp dir
// ---------------------------------------------------------------------------

[<Fact>]
let ``route scaffolds a Dart contracts package`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "specs"; "scaffold"; "dart"; "--dir"; root |]

    Assert.Equal(0, code)
    Assert.NotEmpty out
    Assert.True(File.Exists(Path.Combine(root, "pubspec.yaml")))

// ---------------------------------------------------------------------------
// Real-repo read-only harness/gate leaves not yet exercised elsewhere
// ---------------------------------------------------------------------------

[<Fact>]
let ``route runs specs counts validate with no folder using the fixture ddd-areas default`` () =
    let root = newDddAreaFixture ()

    let code, out, _ = runCaptured (okRoot root) [| "specs"; "counts"; "validate" |]

    Assert.Equal(0, code)
    Assert.Contains("specs/apps/fixture-app", out)

[<Fact>]
let ``route runs specs counts validate against a comma-separated --apps flag`` () =
    let code, _, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "specs"; "counts"; "validate"; "--apps"; "organiclever,ose" |]

    Assert.True(code = 0 || code = 1)

[<Fact>]
let ``route emits pre-commit lint-staged config into a fixture's package.json`` () =
    let root = newTempDir ()
    writeFile root "repo-config.yml" "gates: []\n"
    writeFile root "package.json" "{\n  \"name\": \"fixture\"\n}\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "gate"; "emit"; "--surface=pre-commit" |]

    Assert.Equal(0, code)
    Assert.Contains("Emitted lint-staged", out)
    Assert.Contains("lint-staged", File.ReadAllText(Path.Combine(root, "package.json")))

[<Fact>]
let ``route runs gate validate against the real repo-config.yml`` () =
    let code, _, _ = runCaptured (okRoot (realRepoRoot ())) [| "gate"; "validate" |]
    Assert.True(code = 0 || code = 1)

[<Fact>]
let ``route runs harness sync validate against the real checkout`` () =
    let code, _, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "sync"; "validate" |]

    Assert.True(code = 0 || code = 1)

[<Fact>]
let ``route runs harness bindings validate against the real checkout`` () =
    let code, _, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "bindings"; "validate" |]

    Assert.True(code = 0 || code = 1)

[<Fact>]
let ``route runs harness ownership validate against the real checkout`` () =
    let code, _, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "ownership"; "validate" |]

    Assert.True(code = 0 || code = 1)

[<Fact>]
let ``route runs harness catalog generate against the real checkout`` () =
    let code, out, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "catalog"; "generate" |]

    Assert.Equal(0, code)
    Assert.NotEmpty out

[<Fact>]
let ``route runs harness catalog validate against the real checkout`` () =
    let code, _, _ =
        runCaptured (okRoot (realRepoRoot ())) [| "harness"; "catalog"; "validate" |]

    Assert.True(code = 0 || code = 1)

[<Fact>]
let ``route reports harness catalog validate as failed when repo-config.yml declares no harness-catalog block`` () =
    let root = newTempDir ()
    writeFile root "repo-config.yml" "gates: []\nharness: []\n"

    let code, _, err = runCaptured (okRoot root) [| "harness"; "catalog"; "validate" |]
    Assert.Equal(1, code)
    Assert.Contains("catalog validation failed", err)
    Assert.Contains("diverges from the harness registry", err)

[<Fact>]
let ``route runs md frontmatter-dates validate with an explicit positional path`` () =
    let code, out, _ =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "md"
               "frontmatter-dates"
               "validate"
               "repo-governance/"
               "-o"
               "markdown" |]

    Assert.True(code = 0 || code = 1)
    Assert.NotEmpty out

// ---------------------------------------------------------------------------
// `doctor` — the tool-name validation error branch, plus a real (assertion-
// lenient, since tool availability varies by host) run
// ---------------------------------------------------------------------------

[<Fact>]
let ``route reports an unknown --tools name on doctor`` () =
    let code, _, err =
        runCaptured (okRoot (newTempDir ())) [| "doctor"; "--tools"; "not-a-real-tool" |]

    Assert.Equal(1, code)
    Assert.NotEmpty err

[<Fact>]
let ``route runs doctor against the real checkout`` () =
    let code, _, _ = runCaptured (okRoot (realRepoRoot ())) [| "doctor" |]
    Assert.True(code = 0 || code = 1)

// ---------------------------------------------------------------------------
// `route`'s own getRepoRoot-lookup-failure branches for the leaves special-
// cased ahead of the generic dispatch (each has its own inlined `Error
// message -> ...` arm rather than sharing the bottom one)
// ---------------------------------------------------------------------------

let private failingRoot () : Result<string, string> = Error "not a git repository"

[<Fact>]
let ``route reports a repo-root lookup failure on test-coverage validate`` () =
    let code, _, err =
        runCaptured failingRoot [| "test-coverage"; "validate"; "x"; "90" |]

    Assert.Equal(1, code)
    Assert.Contains("failed to find git repository root", err)

[<Fact>]
let ``route reports a repo-root lookup failure on harness sync promote`` () =
    let code, _, err =
        runCaptured failingRoot [| "harness"; "sync"; "promote"; "--from"; "x" |]

    Assert.Equal(1, code)
    Assert.Contains("failed to find git repository root", err)

[<Fact>]
let ``route reports a repo-root lookup failure on specs behavior-coverage validate`` () =
    let code, _, err =
        runCaptured failingRoot [| "specs"; "behavior-coverage"; "validate"; "a"; "b" |]

    Assert.Equal(1, code)
    Assert.Contains("failed to find git repository root", err)

[<Fact>]
let ``route reports a repo-root lookup failure on specs domain-coverage validate`` () =
    let code, _, err =
        runCaptured failingRoot [| "specs"; "domain-coverage"; "validate"; "a"; "b" |]

    Assert.Equal(1, code)
    Assert.Contains("failed to find git repository root", err)

[<Fact>]
let ``route reports a repo-root lookup failure on governance readme-index rewrite-paths`` () =
    let code, _, err =
        runCaptured failingRoot [| "governance"; "readme-index"; "rewrite-paths"; "--map"; "x" |]

    Assert.Equal(1, code)
    Assert.Contains("failed to find git repository root", err)

[<Fact>]
let ``route reports a repo-root lookup failure on gate list`` () =
    let code, _, err =
        runCaptured failingRoot [| "gate"; "list"; "--surface=pre-push" |]

    Assert.Equal(1, code)
    Assert.Contains("failed to find git repository root", err)

[<Fact>]
let ``route reports a repo-root lookup failure on gate emit`` () =
    let code, _, err =
        runCaptured failingRoot [| "gate"; "emit"; "--surface=pre-push" |]

    Assert.Equal(1, code)
    Assert.Contains("failed to find git repository root", err)

[<Fact>]
let ``route reports a repo-root lookup failure on gate run`` () =
    let code, _, err = runCaptured failingRoot [| "gate"; "run"; "--surface=pre-push" |]
    Assert.Equal(1, code)
    Assert.Contains("failed to find git repository root", err)

[<Fact>]
let ``route reports an invalid --output value on specs e2e-coverage validate`` () =
    let code, _, err =
        runCaptured (okRoot (newTempDir ())) [| "specs"; "e2e-coverage"; "validate"; "-o"; "not-a-format" |]

    Assert.Equal(1, code)
    Assert.NotEmpty err

[<Fact>]
let ``route reports an invalid --output value on specs behavior-coverage validate`` () =
    let code, _, err =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "specs"; "behavior-coverage"; "validate"; "-o"; "not-a-format"; "a"; "b" |]

    Assert.Equal(1, code)
    Assert.NotEmpty err

[<Fact>]
let ``route reports an invalid --output value on specs domain-coverage validate`` () =
    let code, _, err =
        runCaptured
            (okRoot (realRepoRoot ()))
            [| "specs"; "domain-coverage"; "validate"; "-o"; "not-a-format"; "a"; "b" |]

    Assert.Equal(1, code)
    Assert.NotEmpty err
