/// Port of the per-level `@covers` behavior coverage engine
/// [Repo-grounded — `apps/rhino-cli/src/application/behavior_coverage/types.rs`,
/// `apps/rhino-cli/src/application/behavior_coverage/validator.rs`] for
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/specs/behavior-coverage.feature`'s
/// 6 scenarios, plus the `domain/**`-scoped allowlist gate
/// [Repo-grounded — `apps/rhino-cli/src/application/domain_coverage/mod.rs`]
/// for `domain-coverage.feature`'s 2 scenarios, which reuses [`validate`]
/// rather than duplicating it.
///
/// Scope: this first PR against the `specs` subsystem ports only what
/// [`validate`] itself needs — [`TestLevel`], [`ScenarioSpec`],
/// [`CoversMarker`], [`ProjectEnvelope`], and [`BehaviorCoverageViolation`].
/// No Rust command wrapper for `specs behavior-coverage validate` is wired
/// through this file — the live CLI verb (`commands::specs_coverage::run`)
/// calls the same engine as one leg of a larger three-level check that this
/// plan's later `spec-coverage-validate.feature` PR ports — so, matching
/// `TestCoverage.fs`'s own established precedent for a feature with no
/// F# CLI dispatch arm yet, every scenario calls [`validate`] directly.
module RhinoCli.Application.Specs

open System
open System.Globalization
open System.IO
open System.Text
open System.Text.Json
open System.Text.Json.Nodes
open System.Text.RegularExpressions

/// Test level: unit, integration, or e2e.
type TestLevel =
    | Unit
    | Integration
    | E2e

/// A Gherkin scenario extracted from a feature file.
type ScenarioSpec =
    {
        FeaturePath: string
        Title: string
        /// Level tags declared on this scenario (@unit, @integration, @e2e).
        /// Empty means untagged (a lint error).
        LevelTags: Set<TestLevel>
        /// True if the scenario is tagged @wip (exempt from coverage).
        IsWip: bool
    }

/// An `@covers` marker found in a test source file.
type CoversMarker =
    {
        SourceFile: string
        /// Test level derived from the owning test target (unit/integration/e2e).
        Level: TestLevel
        FeaturePath: string
        ScenarioTitle: string
    }

/// The set of test levels a project supports (its level envelope P).
type ProjectEnvelope = { Levels: Set<TestLevel> }

/// A violation found by the behavior coverage engine.
type BehaviorCoverageViolation =
    /// A scenario has no @unit/@integration/@e2e level tags.
    | UntaggedScenario of FeaturePath: string * Title: string
    /// A scenario's tag names a level not in the project envelope P.
    | LevelOutsideEnvelope of FeaturePath: string * Title: string * RequiredLevel: TestLevel
    /// A scenario requires a level (from S) but has no @covers marker at that level.
    | MissingCoverage of FeaturePath: string * Title: string * MissingLevel: TestLevel
    /// A @covers marker targets a level not in the scenario's own tags S (over-coverage).
    | CoverageAtUndeclaredLevel of SourceFile: string * FeaturePath: string * Title: string * ExtraLevel: TestLevel
    /// A @covers marker references a scenario title that no feature file contains.
    | OrphanMarker of SourceFile: string * FeaturePath: string * ScenarioTitle: string

/// Validates `@covers` coverage for the given scenarios and markers.
///
/// Rules enforced:
/// - Untagged non-wip scenario → `UntaggedScenario`
/// - Scenario tag outside project envelope P → `LevelOutsideEnvelope`
/// - Missing marker at a required level → `MissingCoverage`
/// - Marker at a level not in the scenario's own tags S → `CoverageAtUndeclaredLevel`
/// - Marker referencing an unknown scenario → `OrphanMarker`
/// - `@wip` scenarios are fully exempt.
let validate
    (scenarios: ScenarioSpec list)
    (markers: CoversMarker list)
    (envelope: ProjectEnvelope)
    : BehaviorCoverageViolation list =
    let scenarioLookup =
        scenarios |> List.map (fun s -> (s.FeaturePath, s.Title), s) |> Map.ofList

    let scenarioViolations =
        scenarios
        |> List.collect (fun scenario ->
            if scenario.IsWip then
                []
            elif Set.isEmpty scenario.LevelTags then
                [ UntaggedScenario(scenario.FeaturePath, scenario.Title) ]
            else
                scenario.LevelTags
                |> Set.toList
                |> List.collect (fun level ->
                    let envelopeViolation =
                        if Set.contains level envelope.Levels then
                            []
                        else
                            [ LevelOutsideEnvelope(scenario.FeaturePath, scenario.Title, level) ]

                    let covered =
                        markers
                        |> List.exists (fun m ->
                            m.FeaturePath = scenario.FeaturePath
                            && m.ScenarioTitle = scenario.Title
                            && m.Level = level)

                    let coverageViolation =
                        if covered then
                            []
                        else
                            [ MissingCoverage(scenario.FeaturePath, scenario.Title, level) ]

                    envelopeViolation @ coverageViolation))

    let markerViolations =
        markers
        |> List.collect (fun marker ->
            match Map.tryFind (marker.FeaturePath, marker.ScenarioTitle) scenarioLookup with
            | None -> [ OrphanMarker(marker.SourceFile, marker.FeaturePath, marker.ScenarioTitle) ]
            | Some scenario ->
                if not scenario.IsWip && not (Set.contains marker.Level scenario.LevelTags) then
                    [ CoverageAtUndeclaredLevel(marker.SourceFile, marker.FeaturePath, scenario.Title, marker.Level) ]
                else
                    [])

    scenarioViolations @ markerViolations

/// `true` iff `projectName` is listed in `domainAreas`.
///
/// A project absent from the allowlist is skipped even if it has `domain/**`
/// feature files.
let isEligible (projectName: string) (domainAreas: string list) : bool =
    domainAreas |> List.contains projectName

/// Returns only those scenarios whose `FeaturePath` contains a `domain`
/// path component.
let filterDomainScenarios (scenarios: ScenarioSpec list) : ScenarioSpec list =
    scenarios
    |> List.filter (fun s -> s.FeaturePath.Split('/') |> Array.contains "domain")

// ---------------------------------------------------------------------------
// `specs e2e-coverage validate` — playwright-bdd unbound-scenario gap detector
// [Repo-grounded — `apps/rhino-cli/src/application/e2e_coverage/{types,diff,
// parser,reporter}.rs` and `apps/rhino-cli/src/commands/specs_e2e_coverage.rs`]
// for `specs/apps/rhino/behavior/rhino-cli/gherkin/specs/e2e-coverage.feature`'s
// 13 scenarios.
// ---------------------------------------------------------------------------

/// A `{feature, scenario}` pair — the key used throughout the declared,
/// fixme, and baseline sets.
///
/// Keying on the pair (rather than the scenario title alone) lets scenario
/// titles repeat across different `.feature` files without collision.
type BaselineEntry = { Feature: string; Scenario: string }

/// The result of diffing a project's current unbound scenarios against its
/// checked-in baseline manifest.
type GapReport =
    {
        /// Scenarios unbound today (declared ∩ fixme) the baseline has not
        /// yet accepted — a non-empty set fails the gate. Sorted by
        /// `(Feature, Scenario)`.
        NewGaps: BaselineEntry list
        /// Baseline entries no longer emitted as `test.fixme`
        /// (baseline \ fixme) — never affects `Failed`. Two readings of the
        /// same computed set: a previously-unbound scenario that is now
        /// bound, and a stale baseline entry that can be pruned.
        Stale: BaselineEntry list
        /// `true` when `NewGaps` is non-empty.
        Failed: bool
    }

/// The checked-in per-project baseline manifest (`e2e-coverage-baseline.json`).
type BaselineManifest =
    { Project: string
      AllowedUnbound: BaselineEntry list }

/// A generated `.spec.js` file's two title sets, keyed together per mirror
/// file so [`isUnboundOrAbsent`] can answer both "is this title unbound?"
/// and "is this title rendered here at all?" from one lookup.
type FileTitles =
    {
        /// Titles playwright-bdd marked unbound: a plain `test.fixme(...)`
        /// call title, a `Scenario Outline`'s wrapping `describe` title with
        /// at least one nested `test.fixme`, or a wrapping `describe` title
        /// suffixed `.skip`/`.fixme` by a first-class special tag.
        Unbound: Set<string>
        /// EVERY title playwright-bdd rendered anything for at all — always
        /// a superset of `Unbound`.
        Rendered: Set<string>
    }

/// Matches a single-, double-, or backtick-quoted JS string literal,
/// respecting backslash-escaped characters (including an escaped instance of
/// the literal's own delimiter) so a match never terminates early at an
/// escaped quote. Capture group 1 holds a single-quoted body, group 2 a
/// double-quoted body, group 3 a backtick-quoted body — exactly one
/// participates per match.
[<Literal>]
let private QuotedJsString =
    """(?:'((?:\\.|[^'\\])*)'|"((?:\\.|[^"\\])*)"|`((?:\\.|[^`\\])*)`)"""

/// Matches a bound `test("<title>", ...)` call's title argument —
/// deliberately excludes `test.fixme(` and `test.describe(` (both carry a `.`
/// right after `test`, which this pattern's literal `(` does not allow) so it
/// never double-counts either.
let private boundTestTitleRe = Regex(@"test\(\s*" + QuotedJsString)

/// Matches a `test.fixme("<title>", ...)` call's title argument —
/// playwright-bdd emits `test.fixme` exclusively for scenarios its
/// `missingSteps: "skip-scenario"` setting silently skipped.
let private fixmeTitleRe = Regex(@"test\.fixme\(\s*" + QuotedJsString)

/// Matches a `test.describe("<title>", ...)` (or any `.`-suffixed variant)
/// block's title argument — never an anonymous
/// `test.describe(() => { ... })`, which has no quoted string in the title
/// position at all.
let private describeRe = Regex(@"test\.describe(?:\.\w+)?\(\s*" + QuotedJsString)

/// Matches specifically a `test.describe.skip(...)` or
/// `test.describe.fixme(...)` block's title argument — never a plain
/// `test.describe(` and never a `.only`-suffixed one, which genuinely
/// executes its wrapped tests.
let private skipOrFixmeDescribeRe =
    Regex(@"test\.describe\.(?:skip|fixme)\(\s*" + QuotedJsString)

/// Reverses playwright-bdd's `jsStringWrap` escaping: it backslash-escapes
/// only the wrapping quote character and `\` itself, and turns line
/// terminators into `\n`, `\r`, or a `\uNNNN` escape. Any other
/// backslash-escaped character is passed through literally (the backslash is
/// dropped), matching ordinary JS semantics for an unrecognized escape.
let private unescapeJsString (raw: string) : string =
    let out = StringBuilder(raw.Length)
    let mutable i = 0

    while i < raw.Length do
        let c = raw.[i]

        if c <> '\\' then
            out.Append(c) |> ignore
            i <- i + 1
        elif i + 1 >= raw.Length then
            // Trailing backslash with nothing after it — preserve as-is.
            out.Append('\\') |> ignore
            i <- i + 1
        else
            let next = raw.[i + 1]
            i <- i + 2

            match next with
            | 'n' -> out.Append('\n') |> ignore
            | 'r' -> out.Append('\r') |> ignore
            | 't' -> out.Append('\t') |> ignore
            | 'u' ->
                let available = min 4 (raw.Length - i)
                let hex = raw.Substring(i, available)
                i <- i + available

                let isHex = hex.Length = 4 && hex |> Seq.forall (fun ch -> Uri.IsHexDigit ch)

                let decoded =
                    if isHex then
                        let code =
                            Int32.Parse(hex, NumberStyles.AllowHexSpecifier, CultureInfo.InvariantCulture)

                        if code >= 0xD800 && code <= 0xDFFF then
                            // Lone surrogate — not a scalar value, so Rust's
                            // `char::from_u32` rejects it too.
                            None
                        else
                            Some(Char.ConvertFromUtf32 code)
                    else
                        None

                match decoded with
                | Some text -> out.Append(text) |> ignore
                | None ->
                    // Malformed/short \u escape — preserve the raw text
                    // rather than silently losing data.
                    out.Append("\\u").Append(hex) |> ignore
            | other -> out.Append(other) |> ignore

    out.ToString()

/// Extracts and unescapes a [`QuotedJsString`] match's captured body —
/// whichever of the three alternative capture groups participated.
let private capturedTitle (m: Match) : string =
    let raw =
        if m.Groups.[1].Success then m.Groups.[1].Value
        elif m.Groups.[2].Success then m.Groups.[2].Value
        elif m.Groups.[3].Success then m.Groups.[3].Value
        else ""

    unescapeJsString raw

/// Splits `text` the way Rust's `str::lines` does: on `\n`, stripping a
/// trailing `\r` from each line and never yielding a trailing empty line for
/// a `\n`-terminated input.
let private splitLines (text: string) : string[] =
    if text.Length = 0 then
        [||]
    else
        let body =
            if text.EndsWith("\n", StringComparison.Ordinal) then
                text.Substring(0, text.Length - 1)
            else
                text

        body.Split('\n')
        |> Array.map (fun line ->
            if line.EndsWith("\r", StringComparison.Ordinal) then
                line.Substring(0, line.Length - 1)
            else
                line)

/// Returns the number of leading whitespace characters on `line` —
/// playwright-bdd's generator indents with plain ASCII spaces only.
let private leadingWhitespaceLen (line: string) : int = line.Length - line.TrimStart().Length

/// Collects the body lines of a block opened at index `openIndex`, whose
/// extent ends at the first `});` line indented identically to the open line.
/// playwright-bdd's generator always indents a block's open and close lines
/// identically, so this never requires full JS parsing or brace-balancing.
let private blockBody (lines: string[]) (openIndex: int) : string[] =
    let indent = leadingWhitespaceLen lines.[openIndex]

    lines.[openIndex + 1 ..]
    |> Array.takeWhile (fun candidate -> not (candidate.Trim() = "});" && leadingWhitespaceLen candidate = indent))

/// `true` when `line` opens a block playwright-bdd collapsed onto a single
/// line (`test.describe('title', () => {});`) — its body is trivially empty,
/// so there is nothing nested to recurse into.
let private isCollapsedBlock (line: string) : bool =
    line.TrimEnd().EndsWith("{});", StringComparison.Ordinal)

/// Scans generated `.spec.js` source for `test.fixme(...)` call titles — the
/// literal signal playwright-bdd emits for a scenario its
/// `missingSteps: "skip-scenario"` config silently skipped for lacking a step
/// definition.
///
/// Only sees a plain `Scenario:`'s own title this way — a `Scenario
/// Outline`'s Examples-row tests are titled `Example #<N>` by
/// playwright-bdd's own convention, never the outline's declared title, so an
/// unbound Outline is invisible here; see [`scanUnboundDescribeTitles`].
let scanFixmeTitles (specJs: string) : string list =
    fixmeTitleRe.Matches(specJs) |> Seq.map capturedTitle |> List.ofSeq

/// Scans generated `.spec.js` source for `test.describe(...)` blocks that
/// contain at least one nested `test.fixme(...)` call, returning each such
/// block's own (unescaped) title.
///
/// playwright-bdd wraps every `Scenario Outline`'s Examples-row-derived tests
/// in one `test.describe` block titled with the outline's own raw Gherkin
/// title, while the individual tests inside are auto-titled `Example #<N>` —
/// which never exact-matches the outline's declared title. So
/// [`scanFixmeTitles`] alone can never see an unbound Outline; this closes
/// that gap by matching the wrapping block's title instead. An enclosing
/// `Feature`/`Rule`-level `describe` is matched too, which is harmless: a
/// Feature or Rule name never collides with a declared scenario title.
let scanUnboundDescribeTitles (specJs: string) : string list =
    let lines = splitLines specJs

    [ for i in 0 .. lines.Length - 1 do
          let line = lines.[i]
          let m = describeRe.Match(line)

          if m.Success && not (isCollapsedBlock line) then
              let body = blockBody lines i

              if
                  body
                  |> Array.exists (fun candidate -> candidate.Contains("test.fixme(", StringComparison.Ordinal))
              then
                  yield capturedTitle m ]

/// Scans generated `.spec.js` source for a `Feature`-, `Rule`-, or
/// `Scenario Outline`-level wrapping `test.describe.skip(...)` or
/// `test.describe.fixme(...)` block — playwright-bdd's rendering for a
/// first-class `@skip`/`@fixme` special tag at any of those three levels —
/// returning the block's own title AND every plain (unsuffixed) `test(...)`
/// and `test.describe(...)` title nested anywhere inside its span.
///
/// Playwright enforces the skip/fixme entirely at the PARENT level: none of
/// the wrapped children are individually re-marked, so they remain ordinary
/// plain calls. Collecting their titles is what lets a `Scenario` nested
/// under a skipped `Rule`/`Feature` be flagged under its OWN declared title.
/// Recursing is harmless for the Outline case — it merely adds
/// `Example #<N>`-shaped entries that never collide with a real title.
///
/// Deliberately excludes `.only`: a `.only`-suffixed suite genuinely executes
/// its wrapped tests, so treating it as unbound would be a false positive.
let scanSkipOrFixmeDescribeTitles (specJs: string) : string list =
    let lines = splitLines specJs
    let result = ResizeArray<string>()

    for i in 0 .. lines.Length - 1 do
        let line = lines.[i]
        let m = skipOrFixmeDescribeRe.Match(line)

        if m.Success then
            result.Add(capturedTitle m)

            if not (isCollapsedBlock line) then
                let bodyText = String.Join("\n", blockBody lines i)

                for bound in boundTestTitleRe.Matches(bodyText) do
                    result.Add(capturedTitle bound)

                for nested in describeRe.Matches(bodyText) do
                    result.Add(capturedTitle nested)

    List.ofSeq result

/// Scans generated `.spec.js` source for EVERY title playwright-bdd rendered
/// anything for at all — the union of bound (`test(...)`) and unbound
/// (`test.fixme(...)`) leaf titles plus every `test.describe(...)` block
/// title.
///
/// A declared title absent from this set is an additional gap category: a
/// `Scenario Outline` whose `Examples:` table carries zero data rows renders
/// nothing whatsoever, making it structurally indistinguishable from a
/// fully-covered scenario to [`scanFixmeTitles`] and
/// [`scanUnboundDescribeTitles`] alone. The same absence signal equally
/// catches a scenario excluded by a `tags` filter, or one carrying a
/// leaf-level `@only`/`@skip` special tag (whose `test.only(`/`test.skip(`
/// rendering matches none of the three sources below).
let scanAllRenderedTitles (specJs: string) : Set<string> =
    let boundTitles = boundTestTitleRe.Matches(specJs) |> Seq.map capturedTitle
    let describeTitles = describeRe.Matches(specJs) |> Seq.map capturedTitle

    scanFixmeTitles specJs
    |> Seq.append boundTitles
    |> Seq.append describeTitles
    |> Set.ofSeq

/// Extracts the declared `@e2e` scenario set from `scenarios` — untagged and
/// `@unit`/`@integration`-only scenarios are not part of this gate's declared
/// set.
let declaredE2eEntries (scenarios: ScenarioSpec list) : BaselineEntry list =
    scenarios
    |> List.filter (fun s -> Set.contains E2e s.LevelTags)
    |> List.map (fun s ->
        { Feature = s.FeaturePath
          Scenario = s.Title })

/// Computes the coverage gap diff for a project.
///
/// `NewGaps` is `(declared ∩ fixme) \ baseline` — scenarios unbound today the
/// baseline has not yet accepted; a non-empty set fails the gate. `Stale` is
/// `baseline \ fixme` — baseline entries no longer emitted as `test.fixme`;
/// it never affects `Failed`.
let diffGaps (declared: BaselineEntry list) (fixme: BaselineEntry list) (baseline: BaselineEntry list) : GapReport =
    let fixmeSet = Set.ofList fixme
    let baselineSet = Set.ofList baseline

    let newGaps =
        declared
        |> List.filter (fun e -> Set.contains e fixmeSet && not (Set.contains e baselineSet))
        |> List.sortBy (fun e -> e.Feature, e.Scenario)

    let stale =
        baseline
        |> List.filter (fun e -> not (Set.contains e fixmeSet))
        |> List.sortBy (fun e -> e.Feature, e.Scenario)

    { NewGaps = newGaps
      Stale = stale
      Failed = not (List.isEmpty newGaps) }

/// `true` when `mirrorKey`'s path components are an exact, component-wise
/// suffix of `path`'s components — never a partial path segment.
let pathEndsWith (path: string) (mirrorKey: string) : bool =
    let split (value: string) =
        value.Split([| '/'; '\\' |], StringSplitOptions.RemoveEmptyEntries)

    let pathSegments = split path
    let keySegments = split mirrorKey

    keySegments.Length > 0
    && keySegments.Length <= pathSegments.Length
    && Array.forall2
        (fun (a: string) (b: string) -> String.Equals(a, b, StringComparison.Ordinal))
        (pathSegments.[pathSegments.Length - keySegments.Length ..])
        keySegments

/// `true` when `scenario` currently has no passing e2e test for this exact
/// `.feature` file — either because it is an unbound title, or because it is
/// absent from the file's rendered set entirely (the zero-Examples-row
/// `Scenario Outline` case, among others).
///
/// The originating file is resolved as the LONGEST (most specific) mirror key
/// whose mirrored relative path is a component-wise suffix of `featurePath`.
/// Two `.feature` files can share a tail directory/basename sequence at
/// different nesting depths, so accepting any suffix match would let the
/// shallower file's title sets falsely bind to the deeper file's scenario. If
/// NO mirror key resolves at all, every declared scenario in that file is
/// trivially absent, so this returns `true`.
let isUnboundOrAbsent (featurePath: string) (scenario: string) (byFile: Map<string, FileTitles>) : bool =
    let bestKey =
        byFile
        |> Map.toList
        |> List.map fst
        |> List.filter (pathEndsWith featurePath)
        |> List.sortByDescending (fun key -> key.Split([| '/'; '\\' |], StringSplitOptions.RemoveEmptyEntries).Length)
        |> List.tryHead

    match bestKey with
    | None -> true
    | Some key ->
        let titles = byFile.[key]

        Set.contains scenario titles.Unbound
        || not (Set.contains scenario titles.Rendered)

/// Strict UTF-8 decoder — a non-UTF-8 `.spec.js` must be recorded with empty
/// title sets rather than silently decoded with replacement characters, since
/// Rust's `fs::read_to_string` errors outright on one.
let private strictUtf8 = UTF8Encoding(false, true)

/// Recursively scans `dir` for both title sets, keyed by EVERY generated
/// `.spec.js` file's path relative to `dir` with the trailing `.spec.js`
/// suffix stripped — including files with empty title sets, so a fully-bound
/// file at a deeper nesting depth always out-competes a shorter, unrelated
/// suffix match in [`isUnboundOrAbsent`].
///
/// playwright-bdd generates exactly one `.spec.js` per `.feature` file,
/// mirroring the directory structure below its `featuresRoot`, so stripping
/// the suffix reconstructs that `.feature` file's path relative to it.
let scanFixmeDir (dir: string) : Result<Map<string, FileTitles>, string> =
    if not (Directory.Exists dir) then
        Error(sprintf "generated output directory %s not found — run `npx bddgen` first to produce it" dir)
    else
        Directory.EnumerateFiles(dir, "*", SearchOption.AllDirectories)
        |> Seq.choose (fun path ->
            let rel = Path.GetRelativePath(dir, path)

            if not (rel.EndsWith(".spec.js", StringComparison.Ordinal)) then
                None
            else
                let mirrorKey = rel.Substring(0, rel.Length - ".spec.js".Length)

                let content =
                    try
                        Some(strictUtf8.GetString(File.ReadAllBytes path))
                    with _ ->
                        None

                match content with
                | Some text ->
                    let unbound =
                        scanFixmeTitles text
                        |> Seq.append (scanUnboundDescribeTitles text)
                        |> Seq.append (scanSkipOrFixmeDescribeTitles text)
                        |> Set.ofSeq

                    Some(
                        mirrorKey,
                        { Unbound = unbound
                          Rendered = scanAllRenderedTitles text }
                    )
                | None ->
                    Some(
                        mirrorKey,
                        { Unbound = Set.empty
                          Rendered = Set.empty }
                    ))
        |> Map.ofSeq
        |> Ok

/// Shared `System.Text.Json` write options — `serde_json::to_string_pretty`'s
/// two-space indentation is `WriteIndented`'s default.
let private baselineWriteOptions = JsonSerializerOptions(WriteIndented = true)

/// Loads a baseline manifest from `path`, returning an empty manifest when
/// `path` does not exist — the "no baseline manifest yet" first-time
/// generation case.
let loadBaseline (path: string) : Result<BaselineManifest, string> =
    if not (File.Exists path) then
        Ok { Project = ""; AllowedUnbound = [] }
    else
        try
            let root = JsonNode.Parse(File.ReadAllText path)

            let project =
                match root.["project"] with
                | null -> ""
                | node -> node.GetValue<string>()

            let allowed =
                match root.["allowedUnbound"] with
                | :? JsonArray as arr ->
                    arr
                    |> Seq.map (fun entry ->
                        { Feature = entry.["feature"].GetValue<string>()
                          Scenario = entry.["scenario"].GetValue<string>() })
                    |> List.ofSeq
                | _ -> []

            Ok
                { Project = project
                  AllowedUnbound = allowed }
        with _ ->
            Error(sprintf "failed to parse baseline manifest %s" path)

/// Serializes `manifest` as pretty-printed JSON and writes it to `path`.
let saveBaseline (path: string) (manifest: BaselineManifest) : Result<unit, string> =
    try
        let entries = JsonArray()

        for entry in manifest.AllowedUnbound do
            let node = JsonObject()
            node.["feature"] <- JsonValue.Create(entry.Feature)
            node.["scenario"] <- JsonValue.Create(entry.Scenario)
            entries.Add(node)

        let root = JsonObject()
        root.["project"] <- JsonValue.Create(manifest.Project)
        root.["allowedUnbound"] <- entries

        File.WriteAllText(path, root.ToJsonString(baselineWriteOptions) + "\n")
        Ok()
    with _ ->
        Error(sprintf "failed to write baseline manifest %s" path)

/// Renders the pass/fail summary line shared by [`formatGapText`] and
/// [`formatGapMarkdown`].
let private gapHeaderLine (report: GapReport) (prefix: string) (passLabel: string) (failLabel: string) : string =
    if List.isEmpty report.NewGaps then
        sprintf "%s%s: 0 new unbound scenario(s) beyond baseline" prefix passLabel
    else
        sprintf
            "%s%s: %d new unbound scenario(s) found (increase of %d over baseline)"
            prefix
            failLabel
            (List.length report.NewGaps)
            (List.length report.NewGaps)

/// Renders one `{feature, scenario}` entry as the two-line text/`->` block
/// both the new-gap and stale sections use.
let private gapEntryLines (entry: BaselineEntry) : string =
    sprintf "  %s\n    -> Scenario: \"%s\"\n" entry.Feature entry.Scenario

/// Formats `report` as human-readable text.
let formatGapText (report: GapReport) : string =
    let sb = StringBuilder()

    sb.Append(gapHeaderLine report "E2E COVERAGE GAP DETECTOR " "PASSED" "FAILED").Append('\n')
    |> ignore

    for gap in report.NewGaps do
        sb.Append(gapEntryLines gap) |> ignore

    if not (List.isEmpty report.Stale) then
        sb.Append(sprintf "\n%d stale baseline entries can be pruned:\n" (List.length report.Stale))
        |> ignore

        for entry in report.Stale do
            sb.Append(gapEntryLines entry) |> ignore

    sb.ToString()

/// JSON output schema identifier for `specs e2e-coverage validate`.
[<Literal>]
let private GapSchema = "rhino-cli/e2e-coverage/v1"

/// Serializes `report` as a JSON envelope string.
let formatGapJson (report: GapReport) : string =
    let toArray (entries: BaselineEntry list) =
        let arr = JsonArray()

        for entry in entries do
            let node = JsonObject()
            node.["feature"] <- JsonValue.Create(entry.Feature)
            node.["scenario"] <- JsonValue.Create(entry.Scenario)
            arr.Add(node)

        arr

    let root = JsonObject()
    root.["schema"] <- JsonValue.Create(GapSchema)

    root.["status"] <- JsonValue.Create(if List.isEmpty report.NewGaps then "passed" else "failed")

    root.["result"] <- toArray report.NewGaps
    root.["stale"] <- toArray report.Stale
    root.ToJsonString(baselineWriteOptions) + "\n"

/// Formats `report` as a Markdown report.
let formatGapMarkdown (report: GapReport) : string =
    let sb = StringBuilder()

    sb.Append(sprintf "## E2E Coverage Gap Detector\n\n**%s**\n\n" (gapHeaderLine report "" "PASSED" "FAILED"))
    |> ignore

    let appendTable (entries: BaselineEntry list) =
        sb.Append("| Feature | Scenario |\n|---------|----------|\n") |> ignore

        for entry in entries do
            sb.Append(sprintf "| %s | %s |\n" entry.Feature entry.Scenario) |> ignore

    if not (List.isEmpty report.NewGaps) then
        appendTable report.NewGaps

    if not (List.isEmpty report.Stale) then
        sb.Append(sprintf "\n### Stale baseline entries (%d)\n\n" (List.length report.Stale))
        |> ignore

        appendTable report.Stale

    sb.ToString()
