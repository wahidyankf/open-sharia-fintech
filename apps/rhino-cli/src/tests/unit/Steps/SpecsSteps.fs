/// TickSpec step definitions binding the 12 feature files under
/// `specs/apps/rhino/cli/behaviors/specs/` to
/// `RhinoCli.Application.Specs`'s ports, mirroring the single monolithic
/// Rust `tests/specs_tree.rs` runner that owns all of them
/// [Repo-grounded — `apps/rhino-cli/tests/specs_tree.rs`].
///
/// Follows `TestCoverageSteps.fs`'s per-scenario slicing convention: each xunit
/// `[<Fact>]` below runs exactly one scenario, extracted from the real,
/// frozen feature file.
module RhinoCli.Tests.Unit.Steps.SpecsSteps

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application
open RhinoCli.Application.Specs

/// Repo-relative feature-file path shared by every synthetic `@covers`
/// scenario/marker built below — matches Rust's `BC_FEATURE_PATH` constant.
[<Literal>]
let private BcFeaturePath = "specs/apps/example/foo.feature"

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type SpecsSteps() =
    // ---- behavior-coverage.feature (pure engine) state ----
    let mutable bcScenarios: ScenarioSpec list = []
    let mutable bcMarkers: CoversMarker list = []
    let mutable bcEnvelope: ProjectEnvelope = { Levels = Set.empty }
    let mutable bcViolations: BehaviorCoverageViolation list = []
    let mutable bcExemptCount: int = 0

    // ---- e2e-coverage.feature state ----

    /// Repo-relative feature path every synthetic e2e-coverage entry below
    /// shares — paired with `E2eMirrorKey` so `isUnboundOrAbsent` resolves the
    /// fixture's single generated `.spec.js` file to it.
    let e2eFeaturePath = "specs/apps/example/e2e.feature"
    let e2eMirrorKey = "e2e.feature"
    let mutable e2eScenarioRoot: string option = None
    let mutable e2eDeclared: BaselineEntry list = []
    let mutable e2eFixme: BaselineEntry list = []
    let mutable e2eBaseline: BaselineEntry list = []
    let mutable e2eGenDir: string option = None
    let mutable e2eGeneratedJs: string option = None
    let mutable e2eReport: GapReport option = None
    let mutable e2eError: string option = None
    let mutable e2eText: string = ""
    let mutable e2eBaselinePath: string option = None
    let mutable e2eSaveOutcome: Result<unit, string> option = None
    let mutable e2eLoaded: BaselineManifest option = None
    let mutable e2eCliFixtureRoot: string option = None
    let mutable e2eCliExitCode: int option = None

    let e2eRoot () : string =
        match e2eScenarioRoot with
        | Some dir -> dir
        | None ->
            let dir =
                Path.Combine(Path.GetTempPath(), "rhino-cli-e2e-coverage-" + Guid.NewGuid().ToString("N"))

            Directory.CreateDirectory dir |> ignore
            e2eScenarioRoot <- Some dir
            dir

    /// Builds a `{feature, scenario}` entry against the shared fixture path.
    let e2eEntry (title: string) : BaselineEntry =
        { Feature = e2eFeaturePath
          Scenario = title }

    /// Writes `js` as the single generated `.spec.js` file playwright-bdd
    /// would emit for `e2eFeaturePath`, inside a fresh `.features-gen`
    /// directory, and points the validate step at it.
    let e2eWriteGenerated (js: string) : unit =
        let dir = Path.Combine(e2eRoot (), ".features-gen")
        Directory.CreateDirectory dir |> ignore
        File.WriteAllText(Path.Combine(dir, e2eMirrorKey + ".spec.js"), js)
        e2eGenDir <- Some dir
        e2eGeneratedJs <- Some js

    /// The `GapReport` the validate step produced, or a failure if the step
    /// errored before diffing.
    let e2eRequireReport () : GapReport =
        match e2eReport with
        | Some report -> report
        | None -> failwith "validate did not produce a gap report"

    // ---- spec-tree validator state (validate-adoption/counts/links/tree,
    // gherkin-cardinality, specs-audit) ----

    let mutable specRoot: string option = None
    let mutable specApp: string = "testapp"
    let mutable specFolder: string = ""
    let mutable specFindings: SpecFinding list = []
    let mutable specOutput: string = ""
    let mutable specExit: int = 0

    // ---- harness-bindings / harness-registry-driven state ----

    let mutable harnessEntries: RepoConfig.HarnessEntry list = []
    let mutable harnessAccepted: string list = []
    let mutable harnessKnownNameResult: Result<unit, string> option = None
    let mutable harnessUnknownNameResult: Result<unit, string> option = None
    let mutable harnessTargetDirs: (string list * string list) option = None
    let mutable harnessExtendedDirs: (string list * string list) option = None
    let mutable retiredTierParse: Result<RepoConfig.RepoConfig, string> option = None

    // ---- worktree-agnostic state ----

    let mutable worktreeDetection: Result<Env.WorktreeInfo, string> option = None
    let mutable worktreeToplevel: string = ""

    /// Repository root, six levels above this steps file.
    let repositoryRoot: string =
        Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "..", "..", ".."))

    let specFixtureRoot () : string =
        match specRoot with
        | Some dir -> dir
        | None ->
            let dir =
                Path.Combine(Path.GetTempPath(), "rhino-cli-specs-" + Guid.NewGuid().ToString("N"))

            Directory.CreateDirectory dir |> ignore
            specRoot <- Some dir
            dir

    /// Creates the five retired spec subfolders for `app`, each with a
    /// `README.md`; `withSpecFile` additionally drops one non-README spec file
    /// into each. Only negative scenarios use this — it builds the shape the
    /// validators no longer accept.
    let specCreateTree (app: string) (withSpecFile: bool) : string =
        let baseDir = Path.Combine(specFixtureRoot (), "specs", "apps", app)

        for folder in retiredSpecFolders do
            let dir = Path.Combine(baseDir, folder)
            Directory.CreateDirectory dir |> ignore
            File.WriteAllText(Path.Combine(dir, "README.md"), "# Index\n")

            if withSpecFile then
                File.WriteAllText(Path.Combine(dir, "spec.md"), "# Spec\n")

        baseDir

    /// Builds one logical owner corpus under `specs/apps/<app>/<owner>/` and
    /// returns its absolute root. Each `with*` flag drops exactly one required
    /// entry, so a scenario names the single thing it is proving the validator
    /// notices rather than assembling a tree by hand.
    let specCreateCorpus
        (app: string)
        (owner: string)
        (withReadme: bool)
        (withBehaviors: bool)
        (withFeature: bool)
        (withBehaviorsReadme: bool)
        : string =
        let ownerDir = Path.Combine(specFixtureRoot (), "specs", "apps", app, owner)
        Directory.CreateDirectory ownerDir |> ignore
        File.WriteAllText(Path.Combine(ownerDir, "architecture.md"), "# Architecture\n")

        if withReadme then
            File.WriteAllText(Path.Combine(ownerDir, "README.md"), "# Index\n")

        if withBehaviors then
            let behaviorsDir = Path.Combine(ownerDir, "behaviors")
            Directory.CreateDirectory behaviorsDir |> ignore

            if withBehaviorsReadme then
                File.WriteAllText(Path.Combine(behaviorsDir, "README.md"), "# Index\n")

            if withFeature then
                File.WriteAllText(
                    Path.Combine(behaviorsDir, "example.feature"),
                    String.Join(
                        "\n",
                        [ "Feature: Example"
                          ""
                          "  Scenario: Works"
                          "    Given a thing"
                          "    When it runs"
                          "    Then it passes"
                          "" ]
                    )
                )

        ownerDir

    /// Builds one library corpus under `specs/libs/<lib>/` — the same three
    /// entries as an owner corpus, sitting at the library root because a
    /// library has no product directory to nest an owner under.
    let specCreateLibCorpus (lib: string) (withBehaviorsReadme: bool) : string =
        let libDir = Path.Combine(specFixtureRoot (), "specs", "libs", lib)
        let behaviorsDir = Path.Combine(libDir, "behaviors")
        Directory.CreateDirectory behaviorsDir |> ignore
        File.WriteAllText(Path.Combine(libDir, "architecture.md"), "# Architecture\n")
        File.WriteAllText(Path.Combine(libDir, "README.md"), "# Index\n")

        if withBehaviorsReadme then
            File.WriteAllText(Path.Combine(behaviorsDir, "README.md"), "# Index\n")

        File.WriteAllText(
            Path.Combine(behaviorsDir, "example.feature"),
            String.Join(
                "\n",
                [ "Feature: Example"
                  ""
                  "  Scenario: Works"
                  "    Given a thing"
                  "    When it runs"
                  "    Then it passes"
                  "" ]
            )
        )

        libDir

    /// Records one validator run's findings, rendered output, and exit code.
    let specRecord (findings: SpecFinding list) : unit =
        specFindings <- findings
        specOutput <- formatSpecFindingsText specApp findings
        specExit <- (if List.isEmpty findings then 0 else 1)

    /// Builds a `HarnessEntry` with only the fields these scenarios read.
    let harnessEntry (name: string) (tier: RepoConfig.Tier) (agentDir: string option) : RepoConfig.HarnessEntry =
        { Name = name
          Tier = tier
          AgentDir = agentDir
          Mirrors = None
          ForbidDir = None
          SkillsDir = None
          SkillsMirrors = None
          Vendored = []
          Catalog = None
          Ownership = [] }

    // ---- spec-coverage-validate.feature state ----

    let mutable scRoot: string option = None
    let mutable scRan: bool = false
    let mutable scResult: CheckResult option = None
    let mutable scOutput: string = ""
    let mutable scExit: int = 0
    let mutable scMarkers: CoversMarker list = []
    let mutable scReport: RunReportEntry list = []
    let mutable scViolations: RuntimeCoverageViolation list = []

    /// Fixture root holding a `specs/` spec tree and an `app/` source tree.
    let scFixtureRoot () : string =
        match scRoot with
        | Some dir -> dir
        | None ->
            let dir =
                Path.Combine(Path.GetTempPath(), "rhino-cli-speccov-" + Guid.NewGuid().ToString("N"))

            Directory.CreateDirectory(Path.Combine(dir, "specs")) |> ignore
            Directory.CreateDirectory(Path.Combine(dir, "app")) |> ignore
            scRoot <- Some dir
            dir

    /// Writes `content` at fixture-relative `rel`, creating parent folders.
    let scWrite (rel: string) (content: string) : unit =
        let path =
            Path.Combine(scFixtureRoot (), rel.Replace('/', Path.DirectorySeparatorChar))

        Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
        File.WriteAllText(path, content)

    /// Scans the fixture's `specs/` tree against its `app/` tree.
    let scRun (sharedSteps: bool) : unit =
        let root = scFixtureRoot ()

        let result =
            checkAll
                { RepoRoot = root
                  SpecsDir = Path.Combine(root, "specs")
                  SpecsDirs = []
                  AppDir = Path.Combine(root, "app")
                  SharedSteps = sharedSteps
                  ExcludeDirs = []
                  ExcludeSourceDirs = [] }

        scResult <- Some result
        scOutput <- formatCoverageText result false
        scExit <- (if hasCoverageGaps result then 1 else 0)
        scRan <- true

    let scRequire () : CheckResult =
        match scResult with
        | Some result -> result
        | None -> failwith "the spec-coverage scan never ran"

    /// Cross-checks the recorded markers against the recorded run report.
    let scRunRuntime () : unit =
        let violations = checkRuntime scMarkers scReport
        scViolations <- violations
        scOutput <- formatRuntimeViolations violations
        scExit <- (if List.isEmpty violations then 0 else 1)
        scRan <- true

    /// The one `@covers` marker every runtime cross-check scenario declares.
    let scLoginMarker: CoversMarker =
        { SourceFile = "tests/unit/login_test.rs"
          Level = Unit
          FeaturePath = "specs/login.feature"
          ScenarioTitle = "User logs in" }

    /// A one-scenario feature file plus the TypeScript test binding it.
    let scWriteLoginPair () : unit =
        scWrite
            "specs/login.feature"
            """Feature: Login

  Scenario: User logs in
    Given a registered user
    When the user submits valid credentials
    Then the dashboard appears
"""

        scWrite
            "app/login.steps.ts"
            """Scenario("User logs in", () => {
  Given("a registered user", () => {});
  When("the user submits valid credentials", () => {});
  Then("the dashboard appears", () => {});
});
"""

    // ---- Given (`behavior-coverage.feature`) ----

    [<Given>]
    member _.``a scenario with no \x40unit, \x40integration, or \x40e2e level tag``() =
        bcScenarios <-
            bcScenarios
            @ [ { FeaturePath = BcFeaturePath
                  Title = "Untagged scenario"
                  LevelTags = Set.empty
                  IsWip = false } ]

        bcEnvelope <- { Levels = Set.ofList [ Unit ] }

    [<Given>]
    member _.``a project whose coverage registry declares only the unit level``() =
        bcEnvelope <- { Levels = Set.ofList [ Unit ] }

    [<Given>]
    member _.``a scenario in that project tagged \x40integration``() =
        bcScenarios <-
            bcScenarios
            @ [ { FeaturePath = BcFeaturePath
                  Title = "Integration scenario"
                  LevelTags = Set.ofList [ Integration ]
                  IsWip = false } ]

    [<Given>]
    member _.``a scenario tagged \x40unit and \x40e2e``() =
        bcScenarios <-
            bcScenarios
            @ [ { FeaturePath = BcFeaturePath
                  Title = "Multi-level scenario"
                  LevelTags = Set.ofList [ Unit; E2e ]
                  IsWip = false } ]

        bcEnvelope <- { Levels = Set.ofList [ Unit; E2e ] }

    [<Given>]
    member _.``a test marks it \x40covers at the unit level only``() =
        let title = (List.last bcScenarios).Title

        bcMarkers <-
            bcMarkers
            @ [ { SourceFile = "apps/example/src/test.rs"
                  Level = Unit
                  FeaturePath = BcFeaturePath
                  ScenarioTitle = title } ]

    [<Given>]
    member _.``a scenario tagged \x40unit only``() =
        bcScenarios <-
            bcScenarios
            @ [ { FeaturePath = BcFeaturePath
                  Title = "Unit-only scenario"
                  LevelTags = Set.ofList [ Unit ]
                  IsWip = false } ]

        bcEnvelope <- { Levels = Set.ofList [ Unit; E2e ] }

    [<Given>]
    member _.``a test marks it \x40covers at the e2e level``() =
        let title = (List.last bcScenarios).Title

        bcMarkers <-
            bcMarkers
            @ [ { SourceFile = "apps/example-e2e/tests/test.spec.ts"
                  Level = E2e
                  FeaturePath = BcFeaturePath
                  ScenarioTitle = title } ]

    [<Given>]
    member _.``a test with an \x40covers marker referencing a scenario title that no feature file contains``() =
        bcMarkers <-
            bcMarkers
            @ [ { SourceFile = "apps/example/src/test.rs"
                  Level = Unit
                  FeaturePath = BcFeaturePath
                  ScenarioTitle = "Non-existent scenario" } ]

        bcEnvelope <- { Levels = Set.ofList [ Unit ] }

    [<Given>]
    member _.``a scenario tagged \x40wip with no \x40covers markers``() =
        bcScenarios <-
            bcScenarios
            @ [ { FeaturePath = BcFeaturePath
                  Title = "WIP scenario"
                  LevelTags = Set.empty
                  IsWip = true } ]

        bcEnvelope <- { Levels = Set.ofList [ Unit ] }

    // ---- When / Then (`behavior-coverage.feature`) ----

    [<When>]
    member _.``rhino-cli specs behavior-coverage validate runs``() =
        bcViolations <- validate bcScenarios bcMarkers bcEnvelope
        bcExemptCount <- bcScenarios |> List.filter (fun s -> s.IsWip) |> List.length

    [<Then>]
    member _.``it fails and names the untagged scenario``() =
        Assert.True(
            bcViolations
            |> List.exists (function
                | UntaggedScenario(_, title) -> title = "Untagged scenario"
                | _ -> false),
            sprintf "got: %A" bcViolations
        )

    [<Then>]
    member _.``it fails because the scenario requires a level not in the project envelope``() =
        Assert.True(
            bcViolations
            |> List.exists (function
                | LevelOutsideEnvelope _ -> true
                | _ -> false),
            sprintf "got: %A" bcViolations
        )

    [<Then>]
    member _.``it fails and names the missing e2e coverage``() =
        Assert.True(
            bcViolations
            |> List.exists (function
                | MissingCoverage(_, _, E2e) -> true
                | _ -> false),
            sprintf "got: %A" bcViolations
        )

    [<Then>]
    member _.``it fails because the e2e level is not declared for that scenario``() =
        Assert.True(
            bcViolations
            |> List.exists (function
                | CoverageAtUndeclaredLevel _ -> true
                | _ -> false),
            sprintf "got: %A" bcViolations
        )

    [<Then>]
    member _.``it fails and names the orphan marker``() =
        Assert.True(
            bcViolations
            |> List.exists (function
                | OrphanMarker(_, _, scenarioTitle) -> scenarioTitle = "Non-existent scenario"
                | _ -> false),
            sprintf "got: %A" bcViolations
        )

    [<Then>]
    member _.``it does not fail and reports the scenario in the exempt count``() =
        Assert.Empty(bcViolations: BehaviorCoverageViolation list)
        Assert.Equal(1, bcExemptCount)

    // ---- Given (`e2e-coverage.feature`) ----

    [<Given>]
    member _.``a playwright-bdd project whose generated output marks scenarios "A" and "B" as test.fixme``() =
        e2eDeclared <- [ e2eEntry "A"; e2eEntry "B" ]
        e2eFixme <- [ e2eEntry "A"; e2eEntry "B" ]

    [<Given>]
    member _.``a baseline manifest that lists exactly scenarios "A" and "B" as allowed unbound``() =
        e2eBaseline <- [ e2eEntry "A"; e2eEntry "B" ]

    [<Given>]
    member _.``a baseline manifest that lists exactly scenario "A" as allowed unbound``() =
        e2eBaseline <- [ e2eEntry "A" ]

    [<Given>]
    member _.``generated output that marks scenarios "A" and "C" as test.fixme``() =
        e2eDeclared <- [ e2eEntry "A"; e2eEntry "C" ]
        e2eFixme <- [ e2eEntry "A"; e2eEntry "C" ]

    [<Given>]
    member _.``a baseline manifest that lists scenarios "A" and "B" as allowed unbound``() =
        e2eBaseline <- [ e2eEntry "A"; e2eEntry "B" ]

    [<Given>]
    member _.``generated output that marks only scenario "A" as test.fixme``() =
        e2eDeclared <- [ e2eEntry "A"; e2eEntry "B" ]
        e2eFixme <- [ e2eEntry "A" ]

    [<Given>]
    member _.``a scenario tagged \x40unit only that appears as test.fixme in the generated output``() =
        let scenarios =
            [ { FeaturePath = e2eFeaturePath
                Title = "Unit-only scenario"
                LevelTags = Set.ofList [ Unit ]
                IsWip = false } ]

        e2eDeclared <- declaredE2eEntries scenarios

        e2eWriteGenerated (
            String.Join(
                "\n",
                [ "test.describe('Feature: Example', () => {"
                  ""
                  "  test.fixme('Unit-only scenario', () => {});"
                  ""
                  "});"
                  "" ]
            )
        )

    [<Given>]
    member _.``a baseline manifest that lists no allowed unbound scenarios``() = e2eBaseline <- []

    [<Given>]
    member _.``an \x40e2e Scenario Outline whose generated Examples-row tests include one test.fixme``() =
        e2eDeclared <- [ e2eEntry "Resize the sidebar" ]

        e2eWriteGenerated (
            String.Join(
                "\n",
                [ "test.describe('Feature: Example', () => {"
                  ""
                  "  test.describe('Resize the sidebar', () => {"
                  ""
                  "    test('Example #1', () => {});"
                  ""
                  "    test.fixme('Example #2', () => {});"
                  ""
                  "  });"
                  ""
                  "});"
                  "" ]
            )
        )

    [<Given>]
    member _.``an \x40e2e Scenario Outline whose Examples table has zero data rows``() =
        e2eDeclared <- [ e2eEntry "Resize the sidebar" ]

        // A zero-row Examples table makes playwright-bdd render NOTHING for
        // the outline — only the file's other, unrelated content appears.
        e2eWriteGenerated (
            String.Join(
                "\n",
                [ "test.describe('Feature: Example', () => {"
                  ""
                  "  test('An unrelated bound scenario', () => {});"
                  ""
                  "});"
                  "" ]
            )
        )

    [<Given>]
    member _.``a .feature file with a "Rule:" block tagged "\x40skip"``() =
        e2eWriteGenerated (
            String.Join(
                "\n",
                [ "test.describe('Feature: Example', () => {"
                  ""
                  "  test.describe.skip('Rule: gated behaviour', () => {"
                  ""
                  "    test('Nested scenario', () => {});"
                  ""
                  "  });"
                  ""
                  "  test('Other scenario', () => {});"
                  ""
                  "});"
                  "" ]
            )
        )

    [<Given>]
    member _.``the Rule contains at least one Scenario``() =
        e2eDeclared <- e2eDeclared @ [ e2eEntry "Nested scenario" ]

    [<Given>]
    member _.``the file also has other, non-skipped content so it still generates``() =
        e2eDeclared <- e2eDeclared @ [ e2eEntry "Other scenario" ]

    [<Given>]
    member _.``a .feature file whose top-level "Feature:" is tagged "\x40fixme"``() =
        e2eDeclared <- [ e2eEntry "First scenario"; e2eEntry "Second scenario" ]

        e2eWriteGenerated (
            String.Join(
                "\n",
                [ "test.describe.fixme('Feature: Gated feature', () => {"
                  ""
                  "  test('First scenario', () => {});"
                  ""
                  "  test('Second scenario', () => {});"
                  ""
                  "});"
                  "" ]
            )
        )

    [<Given>]
    member _.``an \x40e2e scenario titled with an apostrophe that appears as test.fixme using playwright-bdd's escaped single-quote convention``
        ()
        =
        e2eDeclared <- [ e2eEntry "User's dashboard loads" ]

        e2eWriteGenerated (
            String.Join(
                "\n",
                [ "test.describe('Feature: Example', () => {"
                  ""
                  @"  test.fixme('User\'s dashboard loads', () => {});"
                  ""
                  "});"
                  "" ]
            )
        )

    [<Given>]
    member _.``a new unbound scenario "Resize the sidebar by keyboard" in "resizable-panel.feature"``() =
        let gap =
            { Feature = "specs/libs/web-ui/behaviors/resizable-panel/resizable-panel.feature"
              Scenario = "Resize the sidebar by keyboard" }

        e2eReport <-
            Some
                { NewGaps = [ gap ]
                  Stale = []
                  Failed = true }

    [<Given>]
    member _.``a project with no baseline manifest yet``() =
        let path = Path.Combine(e2eRoot (), "e2e-coverage-baseline.json")
        Assert.False(File.Exists path, "fixture must start with no baseline manifest")
        e2eBaselinePath <- Some path

    [<Given>]
    member _.``generated output that marks scenarios "A" and "B" as test.fixme``() =
        e2eDeclared <- [ e2eEntry "A"; e2eEntry "B" ]
        e2eFixme <- [ e2eEntry "A"; e2eEntry "B" ]

    [<Given>]
    member _.``a project whose .features-gen directory does not exist``() =
        let dir = Path.Combine(e2eRoot (), ".features-gen")
        Assert.False(Directory.Exists dir, "fixture must start with no generated-output directory")
        e2eGenDir <- Some dir

    // ---- When (`e2e-coverage.feature`) ----

    [<When>]
    member _.``rhino-cli specs e2e-coverage validate runs for that project``() =
        match e2eGenDir with
        | Some dir ->
            match scanFixmeDir dir with
            | Error message -> e2eError <- Some message
            | Ok byFile ->
                let fixme =
                    e2eDeclared
                    |> List.filter (fun entry -> isUnboundOrAbsent entry.Feature entry.Scenario byFile)

                e2eReport <- Some(diffGaps e2eDeclared fixme e2eBaseline)
        | None -> e2eReport <- Some(diffGaps e2eDeclared e2eFixme e2eBaseline)

    [<When>]
    member _.``rhino-cli specs e2e-coverage validate runs and detects it as a new gap``() =
        e2eText <- formatGapText (e2eRequireReport ())

    [<When>]
    member _.``rhino-cli specs e2e-coverage validate runs with the --update-baseline flag``() =
        let path =
            match e2eBaselinePath with
            | Some p -> p
            | None -> failwith "no baseline path established"

        e2eSaveOutcome <-
            Some(
                saveBaseline
                    path
                    { Project = "example-e2e"
                      AllowedUnbound = e2eFixme }
            )

    // ---- Then (`e2e-coverage.feature`) ----

    [<Then>]
    member _.``it passes with exit code 0``() =
        Assert.True(e2eError.IsNone, "validate must not error")
        Assert.False((e2eRequireReport ()).Failed, "validate must pass")

    [<Then>]
    member _.``it reports 2 declared-but-unbound scenarios all covered by the baseline``() =
        let report = e2eRequireReport ()
        let unbound = e2eDeclared |> List.filter (fun entry -> List.contains entry e2eFixme)
        Assert.Equal(2, List.length unbound)
        Assert.Empty(report.NewGaps)

    [<Then>]
    member _.``it fails with a non-zero exit code``() =
        match e2eError with
        | Some message -> Assert.False(String.IsNullOrWhiteSpace message, "error message must be populated")
        | None -> Assert.True((e2eRequireReport ()).Failed, "validate must fail")

    [<Then>]
    member _.``it names scenario "C" and its containing .feature file as a new unbound gap``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "C" ], report.NewGaps)

    [<Then>]
    member _.``it does not report scenario "A" as a new gap``() =
        let report = e2eRequireReport ()
        Assert.DoesNotContain(e2eEntry "A", report.NewGaps)

    [<Then>]
    member _.``it reports scenario "B" as newly bound relative to the baseline``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "B" ], report.Stale)

    [<Then>]
    member _.``it reports scenario "B" as a stale baseline entry that can be pruned``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "B" ], report.Stale)

    [<Then>]
    member _.``it does not report the \x40unit-only scenario as an unbound gap``() =
        let report = e2eRequireReport ()
        Assert.Empty(report.NewGaps)

        // Two-way check: the title IS emitted as test.fixme, so the pass above
        // comes from the @e2e declared-set filter, not from an empty fixture.
        let js =
            match e2eGeneratedJs with
            | Some content -> content
            | None -> failwith "no generated output written"

        Assert.Contains("Unit-only scenario", scanFixmeTitles js)

    [<Then>]
    member _.``it reports exactly one new unbound scenario for the outline``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "Resize the sidebar" ], report.NewGaps)

    [<Then>]
    member _.``it reports exactly one new unbound scenario for the zero-row outline``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "Resize the sidebar" ], report.NewGaps)

    [<Then>]
    member _.``every scenario nested under the skipped Rule is reported as unbound``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "Nested scenario" ], report.NewGaps)

    [<Then>]
    member _.``every scenario in the file is reported as unbound``() =
        let report = e2eRequireReport ()

        Assert.Equal<BaselineEntry list>([ e2eEntry "First scenario"; e2eEntry "Second scenario" ], report.NewGaps)

    [<Then>]
    member _.``it reports exactly one new unbound scenario for the apostrophe-bearing title``() =
        let report = e2eRequireReport ()
        Assert.Equal<BaselineEntry list>([ e2eEntry "User's dashboard loads" ], report.NewGaps)

    [<Then>]
    member _.``the failure output contains the scenario title "Resize the sidebar by keyboard"``() =
        Assert.Contains("Resize the sidebar by keyboard", e2eText, StringComparison.Ordinal)

    [<Then>]
    member _.``the failure output contains the feature file path ending in "resizable-panel.feature"``() =
        Assert.Contains("resizable-panel.feature", e2eText, StringComparison.Ordinal)

    [<Then>]
    member _.``the failure output states the delta is an increase of 1 over baseline``() =
        Assert.Contains("increase of 1 over baseline", e2eText, StringComparison.Ordinal)

    [<Then>]
    member _.``it writes a baseline manifest listing scenarios "A" and "B" as allowed unbound``() =
        Assert.Equal<Result<unit, string> option>(Some(Ok()), e2eSaveOutcome)

        let path =
            match e2eBaselinePath with
            | Some p -> p
            | None -> failwith "no baseline path established"

        match loadBaseline path with
        | Error message -> failwith message
        | Ok manifest ->
            e2eLoaded <- Some manifest
            Assert.Equal<BaselineEntry list>([ e2eEntry "A"; e2eEntry "B" ], manifest.AllowedUnbound)

    [<Then>]
    member _.``a subsequent validate run for that project passes with exit code 0``() =
        let manifest =
            match e2eLoaded with
            | Some m -> m
            | None -> failwith "baseline manifest was not reloaded"

        let report = diffGaps e2eDeclared e2eFixme manifest.AllowedUnbound
        Assert.False(report.Failed, "a validate run against the freshly written baseline must pass")

    [<Then>]
    member _.``it reports that bddgen output was not found and must be generated first``() =
        let message =
            match e2eError with
            | Some m -> m
            | None -> failwith "validate did not report an error"

        Assert.Contains("not found", message, StringComparison.Ordinal)
        Assert.Contains("npx bddgen", message, StringComparison.Ordinal)

    // ---- Given/When/Then (`e2e-coverage.feature` — CLI glob-resolution regression) ----
    //
    // Every other e2e-coverage.feature step above drives `diffGaps`/
    // `scanFixmeDir` directly, bypassing `Dispatch.fs`'s own `--features`
    // glob resolution entirely. That CLI-layer path-joining step is where a
    // real bug shipped: `Path.Combine(".", pattern)` (the default
    // `--project-dir`) produces a literal `./`-prefixed string that
    // `Directory.GetFiles` preserves verbatim, while the checked-in baseline
    // manifest's `feature` entries never carry that prefix — so every
    // already-accepted unbound scenario in a real (non-rhino-cli) consuming
    // project falsely reported as a brand-new gap. This scenario spawns the
    // real CLI as a subprocess specifically to exercise that layer.
    [<Given>]
    member _.``a project fixture with a repo-relative --features glob and a baseline keyed on the unprefixed match``() =
        let dir =
            Path.Combine(Path.GetTempPath(), "rhino-cli-e2e-cli-fixture-" + Guid.NewGuid().ToString("N"))

        let specDir = Path.Combine(dir, "specs", "sample")
        Directory.CreateDirectory specDir |> ignore

        File.WriteAllText(
            Path.Combine(specDir, "thing.feature"),
            String.Join(
                "\n",
                [ "Feature: Sample"
                  ""
                  "  @e2e"
                  "  Scenario: Sample scenario"
                  "    Given a step"
                  "" ]
            )
        )

        let genDir = Path.Combine(dir, ".features-gen", "specs", "sample")
        Directory.CreateDirectory genDir |> ignore

        File.WriteAllText(
            Path.Combine(genDir, "thing.feature.spec.js"),
            "test.fixme('Sample scenario', {}, async () => {});\n"
        )

        File.WriteAllText(
            Path.Combine(dir, "e2e-coverage-baseline.json"),
            """{"project":"fixture","allowedUnbound":[{"feature":"specs/sample/thing.feature","scenario":"Sample scenario"}]}"""
            + "\n"
        )

        e2eCliFixtureRoot <- Some dir

    [<When>]
    member _.``rhino-cli specs e2e-coverage validate runs as a subprocess against that fixture``() =
        let dir =
            match e2eCliFixtureRoot with
            | Some d -> d
            | None -> failwith "fixture was not created"

        let repoRoot =
            match RhinoCli.Infrastructure.GitRoot.findRoot () with
            | Ok root -> root
            | Error message -> failwithf "locate repository root: %s" message

        let fsproj =
            Path.Combine(repoRoot, "apps", "rhino-cli", "src", "RhinoCli.Program", "RhinoCli.Program.fsproj")

        let psi =
            Diagnostics.ProcessStartInfo(
                FileName = "dotnet",
                UseShellExecute = false,
                WorkingDirectory = dir,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            )

        for a in
            [ "run"
              "--project"
              fsproj
              "--"
              "specs"
              "e2e-coverage"
              "validate"
              "--features"
              "specs/**/*.feature"
              "--features-gen"
              ".features-gen"
              "--baseline"
              "e2e-coverage-baseline.json"
              "--project"
              "fixture" ] do
            psi.ArgumentList.Add a

        use p = Diagnostics.Process.Start psi
        p.StandardOutput.ReadToEnd() |> ignore
        p.StandardError.ReadToEnd() |> ignore
        p.WaitForExit()
        e2eCliExitCode <- Some p.ExitCode

    [<Then>]
    member _.``the subprocess exits 0``() = Assert.Equal(Some 0, e2eCliExitCode)

    // ---- Given (`gherkin-cardinality.feature`) ----

    [<Given>]
    member _.``a feature file containing a scenario with two primary "When" keywords``() =
        let dir = Path.Combine(specFixtureRoot (), "features")
        Directory.CreateDirectory dir |> ignore

        File.WriteAllText(
            Path.Combine(dir, "double-when.feature"),
            String.Join(
                "\n",
                [ "Feature: Cardinality fixture"
                  ""
                  "  Scenario: Two primary When keywords"
                  "    Given a starting state"
                  "    When the first action runs"
                  "    When the second action runs"
                  "    Then something is asserted"
                  "" ]
            )
        )

    [<When>]
    member _.``the developer runs specs gherkin-cardinality validate on the file``() =
        match auditGherkinKeywordCardinality [ Path.Combine(specFixtureRoot (), "features") ] with
        | Error message -> failwith message
        | Ok findings ->
            specOutput <- formatCardinalityText findings
            specExit <- (if List.isEmpty findings then 0 else 1)

    [<Then>]
    member _.``the output names the offending file and scenario``() =
        Assert.Contains("double-when.feature", specOutput, StringComparison.Ordinal)
        Assert.Contains("Two primary When keywords", specOutput, StringComparison.Ordinal)

    // ---- Given/When/Then (`specs-audit.feature`) ----

    [<Given>]
    member _.``a repository with no spec-tree violations``() =
        specApp <- "testapp"
        specCreateCorpus "testapp" "cli" true true true true |> ignore

    [<When>]
    member _.``the developer runs rhino-cli specs audit``() =
        let root = specFixtureRoot ()

        // Every member runs for real against the clean fixture — a stubbed
        // runner would make the PASSED assertion vacuous.
        let runMember (name: string) : Result<unit, string> =
            let findings =
                match name with
                | "structure-validate" ->
                    validateSpecAdoption root specApp
                    @ validateSpecTree root specApp
                    @ validateSpecCounts root (sprintf "specs/apps/%s" specApp)
                | "validate-links" -> validateSpecLinks root (sprintf "specs/apps/%s" specApp)
                | "gherkin-cardinality" ->
                    match auditGherkinKeywordCardinality [ root ] with
                    | Error message -> failwith message
                    | Ok cardinality ->
                        cardinality
                        |> List.map (fun c ->
                            { Category = "gherkin-cardinality"
                              Criticality = "HIGH"
                              File = c.File
                              Evidence = c.Scenario
                              Expected = "chain extras with And/But" })
                | other -> failwithf "unknown specs audit member: %s" other

            if List.isEmpty findings then
                Ok()
            else
                Error(sprintf "%d finding(s)" (List.length findings))

        let outcome = runSpecsAudit [] runMember
        specOutput <- outcome.Summary
        specExit <- (if outcome.Passed then 0 else 1)

    // ---- Given (`validate-adoption.feature`) ----

    [<Given>]
    member _.``an app "testapp" with an owner corpus and no ddd tree at specs/apps/testapp/ddd``() =
        specApp <- "testapp"
        specCreateCorpus "testapp" "cli" true true true true |> ignore

    [<Given>]
    member _.``an app "testapp" holding only the retired five folders``() =
        specApp <- "testapp"
        specCreateTree "testapp" true |> ignore

    [<Given>]
    member _.``an app "testapp" with an owner corpus and a retired ddd tree at specs/apps/testapp/ddd``() =
        specApp <- "testapp"
        specCreateCorpus "testapp" "cli" true true true true |> ignore

        Directory.CreateDirectory(Path.Combine(specFixtureRoot (), "specs", "apps", "testapp", "ddd"))
        |> ignore

    [<Given>]
    member _.``an app "unknownapp" with no spec tree at all``() =
        specApp <- "unknownapp"
        specFixtureRoot () |> ignore

    [<When>]
    member _.``the developer runs "rhino-cli specs validate-adoption testapp"``() =
        specRecord (validateSpecAdoption (specFixtureRoot ()) "testapp")

    [<When>]
    member _.``the developer runs "rhino-cli specs validate-adoption unknownapp"``() =
        specRecord (validateSpecAdoption (specFixtureRoot ()) "unknownapp")

    // ---- Given (`validate-counts.feature`) ----

    [<Given>]
    member _.``no directory exists at "specs/apps/nosuchapp"``() =
        specApp <- "nosuchapp"
        specFolder <- "specs/apps/nosuchapp"

        Assert.False(
            Directory.Exists(Path.Combine(specFixtureRoot (), "specs", "apps", "nosuchapp")),
            "fixture must not create the folder under test"
        )

    [<When>]
    member _.``the developer runs "rhino-cli specs validate-counts specs/apps/testapp"``() =
        specRecord (validateSpecCounts (specFixtureRoot ()) "specs/apps/testapp")

    [<When>]
    member _.``the developer runs "rhino-cli specs validate-counts specs/apps/nosuchapp"``() =
        specRecord (validateSpecCounts (specFixtureRoot ()) "specs/apps/nosuchapp")

    [<Given>]
    member _.``a library corpus at "specs/libs/testlib" carrying architecture.md and a non-empty behaviors/``() =
        specFolder <- "specs/libs/testlib"
        specCreateLibCorpus "testlib" true |> ignore

    [<Given>]
    member _.``a library corpus at "specs/libs/testlib" whose behaviors/ folder has no README.md``() =
        specFolder <- "specs/libs/testlib"
        specCreateLibCorpus "testlib" false |> ignore

    [<When>]
    member _.``the developer runs "rhino-cli specs validate-counts specs/libs/testlib"``() =
        specRecord (validateSpecCounts (specFixtureRoot ()) "specs/libs/testlib")

    // ---- Given (`validate-links.feature`) ----

    [<Given>]
    member _.``a spec folder at "specs/apps/testapp" where all internal markdown links resolve to existing files``() =
        specApp <- "testapp"
        let baseDir = specCreateTree "testapp" true
        File.WriteAllText(Path.Combine(baseDir, "product", "target.md"), "# Target\n")
        File.WriteAllText(Path.Combine(baseDir, "product", "spec.md"), "# Spec\n\n[target](./target.md)\n")

    [<Given>]
    member _.``a spec folder at "specs/apps/testapp" containing a markdown file with a broken internal link``() =
        specApp <- "testapp"
        let baseDir = specCreateTree "testapp" true
        File.WriteAllText(Path.Combine(baseDir, "product", "spec.md"), "# Spec\n\n[missing](./no-such-file.md)\n")

    [<Given>]
    member _.``a spec folder at "specs/apps/testapp" containing only markdown files with external HTTPS links``() =
        specApp <- "testapp"
        let baseDir = specCreateTree "testapp" true
        File.WriteAllText(Path.Combine(baseDir, "product", "spec.md"), "# Spec\n\n[home](https://example.com)\n")

    [<When>]
    member _.``the developer runs "rhino-cli specs validate-links specs/apps/testapp"``() =
        specRecord (validateSpecLinks (specFixtureRoot ()) "specs/apps/testapp")

    [<When>]
    member _.``the developer runs "rhino-cli specs validate-links specs/apps/nosuchapp"``() =
        specRecord (validateSpecLinks (specFixtureRoot ()) "specs/apps/nosuchapp")

    // ---- Given (`validate-tree.feature`) ----

    [<Given>]
    member _.``a spec tree for "testapp" whose one owner corpus is complete``() =
        specApp <- "testapp"
        specFolder <- "specs/apps/testapp"
        specCreateCorpus "testapp" "cli" true true true true |> ignore

    [<Given>]
    member _.``a spec tree for "testapp" holding only the retired five folders``() =
        specApp <- "testapp"
        specFolder <- "specs/apps/testapp"
        specCreateTree "testapp" true |> ignore

    [<Given>]
    member _.``no spec tree exists for "unknownapp"``() =
        specApp <- "unknownapp"

        Assert.False(
            Directory.Exists(Path.Combine(specFixtureRoot (), "specs", "apps", "unknownapp")),
            "fixture must not create a spec tree for unknownapp"
        )

    [<When>]
    member _.``the developer runs "rhino-cli specs validate-tree testapp"``() =
        specRecord (validateSpecTree (specFixtureRoot ()) "testapp")

    [<When>]
    member _.``the developer runs "rhino-cli specs validate-tree unknownapp"``() =
        specRecord (validateSpecTree (specFixtureRoot ()) "unknownapp")

    // ---- Given/When (`validate-logical-corpus.feature`) ----

    [<Given>]
    member _.``a logical owner corpus for "testapp" at "cli" with its README, architecture, and a behaviors feature``
        ()
        =
        specApp <- "testapp"
        specCreateCorpus "testapp" "cli" true true true true |> ignore

    [<Given>]
    member _.``a logical owner corpus for "testapp" at "cli" whose README.md is absent``() =
        specApp <- "testapp"
        specCreateCorpus "testapp" "cli" false true true true |> ignore

    [<Given>]
    member _.``a logical owner corpus for "testapp" at "cli" whose behaviors directory is absent``() =
        specApp <- "testapp"
        specCreateCorpus "testapp" "cli" true false false false |> ignore

    [<Given>]
    member _.``a logical owner corpus for "testapp" at "cli" whose behaviors directory holds no feature file``() =
        specApp <- "testapp"
        specCreateCorpus "testapp" "cli" true true false true |> ignore

    [<Given>]
    member _.``a logical owner corpus for "testapp" at "cli" whose behaviors directory has no README.md``() =
        specApp <- "testapp"
        specCreateCorpus "testapp" "cli" true true true false |> ignore

    [<Given>]
    member _.``a logical owner corpus for "testapp" at "cli" beside a surviving "product" folder``() =
        specApp <- "testapp"
        specCreateCorpus "testapp" "cli" true true true true |> ignore

        Directory.CreateDirectory(Path.Combine(specFixtureRoot (), "specs", "apps", "testapp", "product"))
        |> ignore

    // ---- Then (shared by every spec-tree validator scenario) ----

    [<Then>]
    member _.``the command exits successfully``() =
        Assert.Equal(0, (if scRan then scExit else specExit))

    [<Then>]
    member _.``the command exits with a failure code``() =
        Assert.NotEqual(0, (if scRan then scExit else specExit))

    [<Then>]
    member _.``the output contains "0 finding"``() =
        Assert.Contains("0 finding", specOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output contains "missing required entry: README.md"``() =
        Assert.Contains("missing required entry: README.md", specOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output contains "missing required entry: behaviors"``() =
        Assert.Contains("missing required entry: behaviors", specOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output contains "missing required entry: behaviors/README.md"``() =
        Assert.Contains("missing required entry: behaviors/README.md", specOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output contains "legacy folder product survives beside a logical owner corpus"``() =
        Assert.Contains(
            "legacy folder product survives beside a logical owner corpus",
            specOutput,
            StringComparison.Ordinal
        )

    [<Then>]
    member _.``the output contains "no feature files"``() =
        Assert.Contains("no feature files", specOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output contains "no logical owner corpus"``() =
        Assert.Contains("no logical owner corpus", specOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output contains "is neither a logical owner corpus nor a product holding one"``() =
        Assert.Contains(
            "is neither a logical owner corpus nor a product holding one",
            specOutput,
            StringComparison.Ordinal
        )

    [<Then>]
    member _.``the output contains "retired ddd/ tree"``() =
        Assert.Contains("retired ddd/ tree", specOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output contains "does not exist"``() =
        Assert.Contains("does not exist", specOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output contains "broken link"``() =
        Assert.Contains("broken link", specOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output contains "SPECS AUDIT PASSED"``() =
        Assert.Contains("SPECS AUDIT PASSED", specOutput, StringComparison.Ordinal)

    // ---- harness-bindings.feature ----

    [<Given>]
    member _.``the harness binding commands and the repo-config.yml harness section``() =
        match RepoConfig.load repositoryRoot with
        | Error message -> failwith message
        | Ok config -> harnessEntries <- config.Harness

    [<When>]
    member _.``the harness coverage is inspected``() =
        harnessAccepted <- harnessEntries |> List.map (fun entry -> entry.Name)

        let retiredRoot =
            Path.Combine(specFixtureRoot (), "retired-tier-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory retiredRoot |> ignore

        File.WriteAllText(
            Path.Combine(retiredRoot, "repo-config.yml"),
            String.Join("\n", [ "harness:"; "  - name: legacy"; "    tier: native"; "" ])
        )

        retiredTierParse <- Some(RepoConfig.load retiredRoot)

    [<Then>]
    member _.``all 3 supported harnesses are listed \(Claude Code, OpenCode, Codex\)``() =
        Assert.Equal<string list>([ "claude-code"; "codex"; "opencode" ], List.sort harnessAccepted)

    [<Then>]
    member _.``the source tier \(Claude Code\) is the single hand-authored origin every mirror derives from``() =
        let sources =
            harnessEntries
            |> List.filter (fun entry -> entry.Tier = RepoConfig.Tier.Source)
            |> List.map (fun entry -> entry.Name)

        Assert.Equal<string list>([ "claude-code" ], sources)

    [<Then>]
    member _.``the generated tier \(OpenCode, Codex\) is regenerated and byte-parity-validated``() =
        let generated =
            harnessEntries
            |> List.filter (fun entry -> entry.Tier = RepoConfig.Tier.Generated)
            |> List.map (fun entry -> entry.Name)
            |> List.sort

        Assert.Equal<string list>([ "codex"; "opencode" ], generated)

    [<Then>]
    member _.``the harness set is data in repo-config.yml, identical across both parity repos, not a hard-coded directory list``
        ()
        =
        // Falsifiable both ways: the names come from the parsed registry, and
        // an empty registry would leave this list empty rather than defaulting
        // to a hard-coded triple.
        Assert.Equal(3, List.length harnessEntries)
        Assert.NotEmpty(harnessAccepted)

    [<Then>]
    member _.``no entry declares the retired source-config or native tier``() =
        for entry in harnessEntries do
            Assert.True(
                entry.Tier = RepoConfig.Tier.Source || entry.Tier = RepoConfig.Tier.Generated,
                sprintf "harness %s declares a tier outside {source, generated}" entry.Name
            )

        match retiredTierParse with
        | Some(Error _) -> ()
        | Some(Ok _) -> failwith "a repo-config.yml declaring the retired native tier must fail to parse"
        | None -> failwith "the retired-tier parse was never attempted"

    // ---- harness-registry-driven.feature ----

    [<Given>]
    member _.``the repo-config.yml harness section lists an agent-bearing generated tier and a source tier``() =
        let root =
            Path.Combine(specFixtureRoot (), "registry-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory root |> ignore

        File.WriteAllText(
            Path.Combine(root, "repo-config.yml"),
            String.Join(
                "\n",
                [ "harness:"
                  "  - name: primary"
                  "    tier: source"
                  "    agent-dir: .primary/agents"
                  "    skills-dir: .primary/skills"
                  "  - name: mirror"
                  "    tier: generated"
                  "    agent-dir: .mirror/agents"
                  "" ]
            )
        )

        specFolder <- root

    [<When>]
    member _.``harness duplication validate runs``() =
        harnessTargetDirs <- Some(Harness.sourceDirsFromRegistry specFolder)

        let extendedRoot =
            Path.Combine(specFixtureRoot (), "registry-extended-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory extendedRoot |> ignore

        File.WriteAllText(
            Path.Combine(extendedRoot, "repo-config.yml"),
            String.Join(
                "\n",
                [ "harness:"
                  "  - name: primary"
                  "    tier: source"
                  "    agent-dir: .primary/agents"
                  "    skills-dir: .primary/skills"
                  "  - name: second-source"
                  "    tier: source"
                  "    agent-dir: .second/agents"
                  "    skills-dir: .second/skills"
                  "" ]
            )
        )

        harnessExtendedDirs <- Some(Harness.sourceDirsFromRegistry extendedRoot)

    [<Then>]
    member _.``it derives its target set from the registry, not a hard-coded .claude/.opencode pair``() =
        match harnessTargetDirs with
        | None -> failwith "duplication validate never resolved its target set"
        | Some(agentDirs, skillDirs) ->
            Assert.Equal<string list>([ Path.Combine(specFolder, ".primary/agents") ], agentDirs)
            Assert.Equal<string list>([ Path.Combine(specFolder, ".primary/skills") ], skillDirs)

            for dir in agentDirs @ skillDirs do
                Assert.DoesNotContain(".claude", dir, StringComparison.Ordinal)
                Assert.DoesNotContain(".opencode", dir, StringComparison.Ordinal)

    [<Then>]
    member _.``a config-only addition of a new agent-bearing tier is covered with no source edit``() =
        match harnessExtendedDirs with
        | None -> failwith "the extended registry was never resolved"
        | Some(agentDirs, _) ->
            Assert.Equal(2, List.length agentDirs)
            Assert.Contains(agentDirs, fun dir -> dir.EndsWith(".second/agents", StringComparison.Ordinal))

    [<Given>]
    member _.``a repo-config.yml whose harness registry names a harness the source code never mentions``() =
        harnessEntries <-
            [ harnessEntry "unheard-of-harness" RepoConfig.Tier.Source (Some ".unheard/agents")
              harnessEntry "mirror" RepoConfig.Tier.Generated (Some ".mirror/agents") ]

    [<When>]
    member _.``harness bindings generate is asked for that registry-declared name``() =
        let config =
            { RepoConfig.empty with
                Harness = harnessEntries }

        harnessAccepted <- Harness.acceptedHarnessNames config
        harnessKnownNameResult <- Some(Harness.validateHarnessName config "unheard-of-harness")
        harnessUnknownNameResult <- Some(Harness.validateHarnessName config "never-declared")

    [<Then>]
    member _.``the name is not rejected as unknown``() =
        match harnessKnownNameResult with
        | Some(Ok()) -> ()
        | Some(Error message) -> failwith message
        | None -> failwith "the registry-declared name was never validated"

    [<Then>]
    member _.``asking for a name the registry omits is rejected, listing the registry-derived set``() =
        match harnessUnknownNameResult with
        | Some(Error message) ->
            for name in harnessAccepted do
                Assert.Contains(name, message, StringComparison.Ordinal)
        | Some(Ok()) -> failwith "an undeclared harness name must be rejected"
        | None -> failwith "the undeclared name was never validated"

    // ---- worktree-agnostic.feature ----

    [<Given>]
    member _.``a synthetic linked worktree in the rhino-cli test suite``() =
        let root = Path.Combine(specFixtureRoot (), "linked-worktree")
        Directory.CreateDirectory root |> ignore

        File.WriteAllText(
            Path.Combine(root, ".git"),
            sprintf "gitdir: %s\n" (Path.Combine(specFixtureRoot (), ".git", "worktrees", "linked-worktree"))
        )

        worktreeToplevel <- root

    [<When>]
    member _.``a guardrail command runs inside it``() =
        worktreeDetection <- Some(Env.detectWorktree worktreeToplevel)

    [<Then>]
    member _.``it resolves to the worktree's own toplevel and exits successfully``() =
        match worktreeDetection with
        | Some(Ok info) ->
            Assert.True(info.IsWorktree, "a linked worktree must be detected as one")
            Assert.Equal("linked-worktree", info.WorktreeName)
            Assert.Equal("linked-worktree", Path.GetFileName worktreeToplevel)
        | Some(Error message) -> failwith message
        | None -> failwith "the guardrail never ran"

    // ---- Given (`spec-coverage-validate.feature`) ----

    [<Given>]
    member _.``a specs directory where every feature file has a corresponding test file``() = scWriteLoginPair ()

    [<Given>]
    member _.``a specs directory containing a feature file with no corresponding test file``() =
        scWrite
            "specs/orphan.feature"
            """Feature: Orphan

  Scenario: Nothing binds this
    Given an unbound precondition
    Then an unbound outcome
"""

    [<Given>]
    member _.``a feature file with a scenario whose title does not appear in any test file``() =
        scWrite
            "specs/profile.feature"
            """Feature: Profile

  Scenario: Profile is unimplemented
    Given a stored profile
    Then the profile renders
"""

        scWrite
            "app/profile.steps.ts"
            """Scenario("A different title entirely", () => {
  Given("a stored profile", () => {});
  Then("the profile renders", () => {});
});
"""

    [<Given>]
    member _.``a feature file with a step text that does not appear in any test file``() =
        scWrite
            "specs/search.feature"
            """Feature: Search

  Scenario: Search returns results
    Given an indexed corpus
    When the user searches for a term
    Then the results list is not empty
"""

        scWrite
            "app/search.steps.ts"
            """Scenario("Search returns results", () => {
  Given("an indexed corpus", () => {});
  When("the user searches for a term", () => {});
});
"""

    [<Given>]
    member _.``feature files with steps implemented in shared step files``() =
        scWrite
            "specs/alpha.feature"
            """Feature: Alpha

  Scenario: Alpha runs
    Given a shared precondition
    Then a shared outcome
"""

        scWrite
            "specs/beta.feature"
            """Feature: Beta

  Scenario: Beta runs
    Given a shared precondition
    Then another shared outcome
"""

        scWrite
            "app/common.steps.ts"
            """Given("a shared precondition", () => {});
Then("a shared outcome", () => {});
Then("another shared outcome", () => {});
"""

    [<Given>]
    member _.``feature files with test implementations in multiple languages``() =
        scWrite
            "specs/rust-side.feature"
            """Feature: Rust side

  Scenario: Rust scenario runs
    Given a rust precondition
    Then a rust outcome
"""

        scWrite
            "app/tests/rust_side.rs"
            """// Scenario: Rust scenario runs
#[given("a rust precondition")]
fn given_rust_precondition() {}

#[then("a rust outcome")]
fn then_rust_outcome() {}
"""

        scWrite
            "specs/dotnet-side.feature"
            """Feature: Dotnet side

  Scenario: Dotnet scenario runs
    Given a dotnet precondition
    Then a dotnet outcome
"""

        scWrite
            "app/DotnetSideSteps.cs"
            """// Scenario: Dotnet scenario runs
[Given("a dotnet precondition")]
public void GivenDotnetPrecondition() { }

[Then("a dotnet outcome")]
public void ThenDotnetOutcome() { }
"""

        scWrite
            "specs/ts-side.feature"
            """Feature: TypeScript side

  Scenario: TypeScript scenario runs
    Given a typescript precondition
    Then a typescript outcome
"""

        scWrite
            "app/ts-side.steps.ts"
            """Scenario("TypeScript scenario runs", () => {
  Given("a typescript precondition", () => {});
  Then("a typescript outcome", () => {});
});
"""

    [<Given>]
    member _.``a scenario with a valid \x40covers marker whose covering test is skipped at runtime``() =
        scMarkers <- [ scLoginMarker ]
        scReport <- []

    [<Given>]
    member _.``a scenario with a valid \x40covers marker whose covering test ran and failed at runtime``() =
        scMarkers <- [ scLoginMarker ]

        scReport <-
            [ { FeaturePath = "specs/login.feature"
                ScenarioTitle = "User logs in"
                Status = Failed } ]

    [<Given>]
    member _.``a scenario with a valid \x40covers marker whose covering test ran and passed at runtime``() =
        scMarkers <- [ scLoginMarker ]

        scReport <-
            [ { FeaturePath = "specs/login.feature"
                ScenarioTitle = "User logs in"
                Status = Passed } ]

    [<Given>]
    member _.``a feature file whose scenario is bound by a test whose Scenario\(\.\.\.\) title wraps onto the next physical line``
        ()
        =
        scWrite
            "specs/wrapped.feature"
            """Feature: Wrapped

  Scenario: A scenario whose binding title wraps
    Given a wrapped precondition
    Then a wrapped outcome
"""

        scWrite
            "app/wrapped.steps.ts"
            """Scenario(
  "A scenario whose binding title wraps",
  () => {
    Given("a wrapped precondition", () => {});
    Then("a wrapped outcome", () => {});
  },
);
"""

    [<Given>]
    member _.``a specs directory with an untagged scenario and a sibling \x40wip scenario, each with its own uncovered step``
        ()
        =
        scWrite
            "specs/wip.feature"
            """Feature: Work in progress

  Scenario: Untagged scenario
    Given an untagged uncovered step

  @wip
  Scenario: Wip scenario
    Given a wip uncovered step
"""

    // TickSpec reads `#` as a Gherkin inline comment and truncates this step's
    // text there, while the spec-coverage checker matches the whole `.feature`
    // line — so the tail is an optional group, satisfying both readers with one
    // binding.
    [<Given>]
    member _.``a specs directory with an untagged scenario and a sibling \x40wip scenario separated from its Scenario line by a(?: #-comment, each with its own uncovered step)?``
        ()
        =
        scWrite
            "specs/wip-comment.feature"
            """Feature: Work in progress

  Scenario: Untagged scenario
    Given an untagged uncovered step

  @wip
  # deliberately parked until the API lands
  Scenario: Wip scenario
    Given a wip uncovered step
"""

    // ---- When (`spec-coverage-validate.feature`) ----

    [<When>]
    member _.``the developer runs spec-coverage validate on the specs and app directories``() = scRun false

    [<When>]
    member _.``the developer runs spec-coverage validate with shared-steps flag``() = scRun true

    [<When>]
    member _.``the developer runs behavior-coverage validate with the runtime cross-check``() = scRunRuntime ()

    // ---- Then (`spec-coverage-validate.feature`) ----

    [<Then>]
    member _.``the output reports all specs as covered``() =
        match scResult with
        | Some result ->
            Assert.Empty result.Gaps
            Assert.Empty result.ScenarioGaps
            Assert.Empty result.StepGaps
            Assert.Contains("Spec coverage valid!", scOutput, StringComparison.Ordinal)
        | None ->
            Assert.Empty scViolations
            Assert.Equal("", scOutput)

    [<Then>]
    member _.``the output identifies the feature file as an uncovered spec``() =
        Assert.Contains("Missing test files (1):", scOutput, StringComparison.Ordinal)
        Assert.Contains("orphan.feature", scOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output identifies the scenario as an unimplemented scenario``() =
        Assert.Contains("Missing scenarios (1):", scOutput, StringComparison.Ordinal)
        Assert.Contains("Profile is unimplemented", scOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output identifies the step as an undefined step``() =
        Assert.Contains("Missing steps (1):", scOutput, StringComparison.Ordinal)
        Assert.Contains("Then the results list is not empty", scOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the command validates steps across all source files without file matching``() =
        let result = scRequire ()
        Assert.Equal(2, result.TotalSpecs)
        // Shared-step mode never reports a missing test file: no `.feature`
        // stem has to correspond to any one source file.
        Assert.Empty result.Gaps
        Assert.Empty result.StepGaps
        Assert.Equal(0, scExit)

    [<Then>]
    member _.``test files are matched using language-specific conventions``() =
        let result = scRequire ()
        Assert.Equal(3, result.TotalSpecs)
        Assert.Empty result.Gaps
        Assert.Empty result.ScenarioGaps
        Assert.Empty result.StepGaps

    [<Then>]
    member _.``the output names the scenario as marked-but-not-executed``() =
        Assert.Contains("marked-but-not-executed", scOutput, StringComparison.Ordinal)
        Assert.Contains("User logs in", scOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output names the scenario as marked-but-failed``() =
        Assert.Contains("marked-but-failed", scOutput, StringComparison.Ordinal)
        Assert.Contains("User logs in", scOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output does not report the wrapped-title scenario as an unimplemented scenario``() =
        Assert.Empty(scRequire().ScenarioGaps)
        Assert.DoesNotContain("Missing scenarios", scOutput, StringComparison.Ordinal)

    [<Then>]
    member _.``the output reports only the untagged scenario's step as undefined, not the \x40wip scenario's step``() =
        Assert.Contains("an untagged uncovered step", scOutput, StringComparison.Ordinal)
        Assert.DoesNotContain("a wip uncovered step", scOutput, StringComparison.Ordinal)

module private FeatureRunner =

    let private featureDir: string =
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
                "cli",
                "behaviors",
                "specs"
            )
        )

    let private extractScenario (featureLines: string[]) (scenarioTitle: string) : string[] =
        let featureLine =
            featureLines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", System.StringComparison.Ordinal))

        let scenarioHeader = sprintf "Scenario: %s" scenarioTitle

        let startIdx = featureLines |> Array.findIndex (fun l -> l.Trim() = scenarioHeader)

        let endIdx =
            featureLines
            |> Array.skip (startIdx + 1)
            |> Array.tryFindIndex (fun l ->
                let trimmed = l.Trim()

                trimmed.StartsWith("Scenario:", System.StringComparison.Ordinal)
                || trimmed.StartsWith("Scenario Outline:", System.StringComparison.Ordinal)
                || trimmed.StartsWith("@", System.StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    let private runPath (featurePath: string) (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<SpecsSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

    /// Runs the single scenario named `scenarioTitle` from `featureFileName`
    /// (a file directly inside `gherkin/specs/`), bound against `SpecsSteps`.
    let run (featureFileName: string) (scenarioTitle: string) : unit =
        runPath (Path.Combine(featureDir, featureFileName)) scenarioTitle

    /// Same as [`run`], for a feature file in a sibling `gherkin/<subdir>/`
    /// folder rather than `gherkin/specs/`.
    let runFrom (subdir: string) (featureFileName: string) (scenarioTitle: string) : unit =
        runPath (Path.Combine(featureDir, "..", subdir, featureFileName)) scenarioTitle

[<Fact>]
let ``An untagged scenario fails the gate`` () =
    FeatureRunner.run "behavior-coverage.feature" "An untagged scenario fails the gate"

[<Fact>]
let ``A scenario requiring a level outside the project envelope fails`` () =
    FeatureRunner.run "behavior-coverage.feature" "A scenario requiring a level outside the project envelope fails"

[<Fact>]
let ``A scenario not covered at a required level fails`` () =
    FeatureRunner.run "behavior-coverage.feature" "A scenario not covered at a required level fails"

[<Fact(DisplayName = "An @covers at an undeclared level fails")>]
let ``An covers at an undeclared level fails`` () =
    FeatureRunner.run "behavior-coverage.feature" "An @covers at an undeclared level fails"

[<Fact(DisplayName = "An orphan @covers marker fails the gate")>]
let ``An orphan covers marker fails the gate`` () =
    FeatureRunner.run "behavior-coverage.feature" "An orphan @covers marker fails the gate"

[<Fact(DisplayName = "A @wip scenario is exempt from coverage")>]
let ``A wip scenario is exempt from coverage`` () =
    FeatureRunner.run "behavior-coverage.feature" "A @wip scenario is exempt from coverage"

[<Fact>]
let ``A project's current unbound gaps exactly match its checked-in baseline`` () =
    FeatureRunner.run "e2e-coverage.feature" "A project's current unbound gaps exactly match its checked-in baseline"

[<Fact(DisplayName = "A newly added @e2e scenario ships without a step definition")>]
let ``A newly added e2e scenario ships without a step definition`` () =
    FeatureRunner.run "e2e-coverage.feature" "A newly added @e2e scenario ships without a step definition"

[<Fact>]
let ``A previously-unbound scenario is now bound`` () =
    FeatureRunner.run "e2e-coverage.feature" "A previously-unbound scenario is now bound"

[<Fact>]
let ``The baseline lists a scenario that is no longer unbound`` () =
    FeatureRunner.run "e2e-coverage.feature" "The baseline lists a scenario that is no longer unbound"

[<Fact(DisplayName = "A test.fixme scenario that is not @e2e-tagged is ignored")>]
let ``A test fixme scenario that is not e2e-tagged is ignored`` () =
    FeatureRunner.run "e2e-coverage.feature" "A test.fixme scenario that is not @e2e-tagged is ignored"

[<Fact>]
let ``A Scenario Outline ships an unbound Examples-row test`` () =
    FeatureRunner.run "e2e-coverage.feature" "A Scenario Outline ships an unbound Examples-row test"

[<Fact>]
let ``A Scenario Outline has zero Examples data rows`` () =
    FeatureRunner.run "e2e-coverage.feature" "A Scenario Outline has zero Examples data rows"

[<Fact(DisplayName = "A Rule-level @skip tag is detected as unbound")>]
let ``A Rule-level skip tag is detected as unbound`` () =
    FeatureRunner.run "e2e-coverage.feature" "A Rule-level @skip tag is detected as unbound"

[<Fact(DisplayName = "A Feature-level @fixme tag is detected as unbound")>]
let ``A Feature-level fixme tag is detected as unbound`` () =
    FeatureRunner.run "e2e-coverage.feature" "A Feature-level @fixme tag is detected as unbound"

[<Fact>]
let ``A test fixme title contains an escaped apostrophe`` () =
    FeatureRunner.run "e2e-coverage.feature" "A test.fixme title contains an escaped apostrophe"

[<Fact>]
let ``Output identifies each new gap by feature path and scenario title`` () =
    FeatureRunner.run "e2e-coverage.feature" "Output identifies each new gap by feature path and scenario title"

[<Fact>]
let ``First-time baseline generation snapshots current unbound scenarios`` () =
    FeatureRunner.run "e2e-coverage.feature" "First-time baseline generation snapshots current unbound scenarios"

[<Fact>]
let ``The generated output directory is absent`` () =
    FeatureRunner.run "e2e-coverage.feature" "The generated output directory is absent"

[<Fact>]
let ``A --features glob resolves against the default project directory without a stray path prefix`` () =
    FeatureRunner.run
        "e2e-coverage.feature"
        "A --features glob resolves against the default project directory without a stray path prefix"

[<Fact>]
let ``A scenario with two primary When keywords fails the audit`` () =
    FeatureRunner.run "gherkin-cardinality.feature" "A scenario with two primary When keywords fails the audit"

[<Fact>]
let ``Every specs validator passes on a repository with no spec violations`` () =
    FeatureRunner.run "specs-audit.feature" "Every specs validator passes on a repository with no spec violations"

[<Fact>]
let ``app with an owner corpus and no retired ddd tree passes validation`` () =
    FeatureRunner.run "validate-adoption.feature" "app with an owner corpus and no retired ddd tree passes validation"

[<Fact>]
let ``app with no owner corpus reports a finding`` () =
    FeatureRunner.run "validate-adoption.feature" "app with no owner corpus reports a finding"

[<Fact>]
let ``app with a surviving retired ddd tree reports a finding`` () =
    FeatureRunner.run "validate-adoption.feature" "app with a surviving retired ddd tree reports a finding"

[<Fact>]
let ``unknown app with no spec tree at all reports an adoption finding`` () =
    FeatureRunner.run "validate-adoption.feature" "unknown app with no spec tree at all reports an adoption finding"

[<Fact>]
let ``product directory whose owners are corpora passes validation`` () =
    FeatureRunner.run "validate-counts.feature" "product directory whose owners are corpora passes validation"

[<Fact>]
let ``folder that is neither a corpus nor a product holding one reports a finding`` () =
    FeatureRunner.run
        "validate-counts.feature"
        "folder that is neither a corpus nor a product holding one reports a finding"

[<Fact(DisplayName = "folder path that does not exist reports an error (validate-counts)")>]
let ``folder path that does not exist reports an error - counts`` () =
    FeatureRunner.run "validate-counts.feature" "folder path that does not exist reports an error"

[<Fact>]
let ``a library corpus at the folder root is measured by the corpus rules`` () =
    FeatureRunner.run "validate-counts.feature" "a library corpus at the folder root is measured by the corpus rules"

[<Fact>]
let ``a library corpus missing its behaviors index reports a finding`` () =
    FeatureRunner.run "validate-counts.feature" "a library corpus missing its behaviors index reports a finding"

[<Fact>]
let ``folder with all valid internal links passes validation`` () =
    FeatureRunner.run "validate-links.feature" "folder with all valid internal links passes validation"

[<Fact>]
let ``markdown file with broken internal link reports a finding`` () =
    FeatureRunner.run "validate-links.feature" "markdown file with broken internal link reports a finding"

[<Fact>]
let ``markdown file with only external HTTPS links passes validation`` () =
    FeatureRunner.run "validate-links.feature" "markdown file with only external HTTPS links passes validation"

[<Fact(DisplayName = "folder path that does not exist reports an error (validate-links)")>]
let ``folder path that does not exist reports an error - links`` () =
    FeatureRunner.run "validate-links.feature" "folder path that does not exist reports an error"

[<Fact>]
let ``product whose owner corpus is complete passes validation`` () =
    FeatureRunner.run "validate-tree.feature" "product whose owner corpus is complete passes validation"

[<Fact>]
let ``product with no owner corpus at all reports a finding`` () =
    FeatureRunner.run "validate-tree.feature" "product with no owner corpus at all reports a finding"

[<Fact>]
let ``product directory holding only retired folders reports a finding`` () =
    FeatureRunner.run "validate-tree.feature" "product directory holding only retired folders reports a finding"

[<Fact>]
let ``a product whose single owner corpus is complete passes validation`` () =
    FeatureRunner.run
        "validate-logical-corpus.feature"
        "a product whose single owner corpus is complete passes validation"

[<Fact>]
let ``an owner corpus missing its README reports a finding`` () =
    FeatureRunner.run "validate-logical-corpus.feature" "an owner corpus missing its README reports a finding"

[<Fact>]
let ``an owner corpus with no behaviors directory reports a finding`` () =
    FeatureRunner.run "validate-logical-corpus.feature" "an owner corpus with no behaviors directory reports a finding"

[<Fact>]
let ``an owner corpus whose behaviors tree holds no feature file reports a finding`` () =
    FeatureRunner.run
        "validate-logical-corpus.feature"
        "an owner corpus whose behaviors tree holds no feature file reports a finding"

[<Fact>]
let ``an owner corpus whose behaviors tree has no index reports a finding`` () =
    FeatureRunner.run
        "validate-logical-corpus.feature"
        "an owner corpus whose behaviors tree has no index reports a finding"

[<Fact>]
let ``legacy five-folder scaffolding surviving beside a corpus reports a finding`` () =
    FeatureRunner.run
        "validate-logical-corpus.feature"
        "legacy five-folder scaffolding surviving beside a corpus reports a finding"

[<Fact>]
let ``All 3 harnesses are accounted for at their tier`` () =
    FeatureRunner.run "harness-bindings.feature" "All 3 harnesses are accounted for at their tier"

[<Fact>]
let ``No retired tier survives the contraction`` () =
    FeatureRunner.run "harness-bindings.feature" "No retired tier survives the contraction"

[<Fact>]
let ``The duplication validator is registry-driven, not hard-coded`` () =
    FeatureRunner.run "harness-registry-driven.feature" "The duplication validator is registry-driven, not hard-coded"

[<Fact>]
let ``The bindings generator derives its accepted harness names from the registry`` () =
    FeatureRunner.run
        "harness-registry-driven.feature"
        "The bindings generator derives its accepted harness names from the registry"

[<Fact>]
let ``A regression test locks worktree-safe execution`` () =
    FeatureRunner.run "worktree-agnostic.feature" "A regression test locks worktree-safe execution"

[<Fact>]
let ``All feature files have matching test implementations`` () =
    FeatureRunner.runFrom
        "spec-coverage"
        "spec-coverage-validate.feature"
        "All feature files have matching test implementations"

[<Fact>]
let ``A feature file without a matching test is reported as a gap`` () =
    FeatureRunner.runFrom
        "spec-coverage"
        "spec-coverage-validate.feature"
        "A feature file without a matching test is reported as a gap"

[<Fact>]
let ``A scenario without a matching implementation is reported as a gap`` () =
    FeatureRunner.runFrom
        "spec-coverage"
        "spec-coverage-validate.feature"
        "A scenario without a matching implementation is reported as a gap"

[<Fact>]
let ``A step without a matching step definition is reported as a gap`` () =
    FeatureRunner.runFrom
        "spec-coverage"
        "spec-coverage-validate.feature"
        "A step without a matching step definition is reported as a gap"

[<Fact>]
let ``Shared-steps mode validates steps across all source files`` () =
    FeatureRunner.runFrom
        "spec-coverage"
        "spec-coverage-validate.feature"
        "Shared-steps mode validates steps across all source files"

[<Fact>]
let ``Multi-language test file matching recognizes language-specific patterns`` () =
    FeatureRunner.runFrom
        "spec-coverage"
        "spec-coverage-validate.feature"
        "Multi-language test file matching recognizes language-specific patterns"

[<Fact(DisplayName = "A marked-but-unexecuted scenario fails the runtime cross-check")>]
let ``A marked-but-unexecuted scenario fails the runtime cross-check`` () =
    FeatureRunner.runFrom
        "spec-coverage"
        "spec-coverage-validate.feature"
        "A marked-but-unexecuted scenario fails the runtime cross-check"

[<Fact(DisplayName = "A marked-but-failed scenario fails the runtime cross-check")>]
let ``A marked-but-failed scenario fails the runtime cross-check`` () =
    FeatureRunner.runFrom
        "spec-coverage"
        "spec-coverage-validate.feature"
        "A marked-but-failed scenario fails the runtime cross-check"

[<Fact(DisplayName = "A marked-and-passed scenario passes the runtime cross-check")>]
let ``A marked-and-passed scenario passes the runtime cross-check`` () =
    FeatureRunner.runFrom
        "spec-coverage"
        "spec-coverage-validate.feature"
        "A marked-and-passed scenario passes the runtime cross-check"

[<Fact>]
let ``A scenario whose title wraps onto a following physical line is still recognized as covered`` () =
    FeatureRunner.runFrom
        "spec-coverage"
        "spec-coverage-validate.feature"
        "A scenario whose title wraps onto a following physical line is still recognized as covered"

[<Fact(DisplayName = "A @wip-tagged scenario is exempt from step-gap reporting in shared-steps mode")>]
let ``A wip-tagged scenario is exempt from step-gap reporting in shared-steps mode`` () =
    FeatureRunner.runFrom
        "spec-coverage"
        "spec-coverage-validate.feature"
        "A @wip-tagged scenario is exempt from step-gap reporting in shared-steps mode"

[<Fact(DisplayName = "A @wip tag survives an intervening #-comment line before its Scenario line")>]
let ``A wip tag survives an intervening comment line before its Scenario line`` () =
    FeatureRunner.runFrom
        "spec-coverage"
        "spec-coverage-validate.feature"
        "A @wip tag survives an intervening #-comment line before its Scenario line"
