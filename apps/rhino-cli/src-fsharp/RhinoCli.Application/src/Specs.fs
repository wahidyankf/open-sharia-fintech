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

// ---------------------------------------------------------------------------
// Spec-tree validators
// [Repo-grounded — `apps/rhino-cli/src/application/specs.rs`] for
// `validate-adoption.feature`, `validate-counts.feature`, and
// `validate-tree.feature`.
// ---------------------------------------------------------------------------

/// A single validation finding produced by one of the `validateSpec*`
/// functions.
type SpecFinding =
    {
        /// Validation category (`"adoption"`, `"count"`, `"links"`,
        /// `"tree-shape"`).
        Category: string
        /// Severity level: `"HIGH"`, `"MEDIUM"`, or `"LOW"`.
        Criticality: string
        /// Repo-relative path to the offending file or directory.
        File: string
        /// Human-readable description of what was found.
        Evidence: string
        /// Suggested remediation step.
        Expected: string
    }

/// The ordered list of subfolder names every spec tree must contain.
let requiredSpecFolders: string list =
    [ "product"; "system-context"; "containers"; "components"; "behavior" ]

/// Ordinal path sort matching Rust's `PathBuf` ordering.
let private sortPaths (paths: string list) : string list =
    paths |> List.sortWith (fun a b -> String.CompareOrdinal(a, b))

/// Recursively walks `dir` returning all files whose name ends with
/// `suffix` (case-insensitively), in sorted order. Returns an empty list if
/// `dir` cannot be read.
let rec private walkBySuffix (dir: string) (suffix: string) : string list =
    if not (Directory.Exists dir) then
        []
    else
        let entries =
            try
                Directory.GetFileSystemEntries dir |> List.ofArray |> sortPaths
            with _ ->
                []

        entries
        |> List.collect (fun path ->
            if Directory.Exists path then
                walkBySuffix path suffix
            elif Path.GetFileName(path).ToLowerInvariant().EndsWith(suffix, StringComparison.Ordinal) then
                [ path ]
            else
                [])

/// Recursively walks `dir` and returns all `.feature` files in sorted order.
let walkFeatureFiles (dir: string) : string list = walkBySuffix dir ".feature"

/// Recursively walks `dir` and returns all `.md` files in sorted order.
let walkMdFiles (dir: string) : string list = walkBySuffix dir ".md"

/// Counts `.feature` files and non-`README.md` `.md` files under `dir`
/// recursively. `README.md` is the required per-folder index, not a spec, so
/// it never counts.
let countNonReadmeMdFiles (dir: string) : int =
    if not (Directory.Exists dir) then
        0
    else
        Directory.EnumerateFiles(dir, "*", SearchOption.AllDirectories)
        |> Seq.filter (fun path ->
            let name = Path.GetFileName path
            let lower = name.ToLowerInvariant()

            lower.EndsWith(".feature", StringComparison.Ordinal)
            || (lower.EndsWith(".md", StringComparison.Ordinal)
                && not (String.Equals(name, "README.md", StringComparison.OrdinalIgnoreCase))))
        |> Seq.length

/// The two adoption findings shared by [`validateSpecAdoption`] and
/// [`validateSpecAdoptionDddAware`]: a missing `behavior/` directory, or one
/// holding no `.feature` file at all.
let private behaviorAdoptionFindings (repoRoot: string) (app: string) : SpecFinding list =
    let behaviorDir = Path.Combine(repoRoot, "specs/apps", app, "behavior")

    if not (Directory.Exists behaviorDir) then
        [ { Category = "adoption"
            Criticality = "HIGH"
            File = sprintf "specs/apps/%s/behavior" app
            Evidence = sprintf "no feature files found under specs/apps/%s/behavior/ (directory does not exist)" app
            Expected = sprintf "create specs/apps/%s/behavior/ with at least one .feature file" app } ]
    elif List.isEmpty (walkFeatureFiles behaviorDir) then
        [ { Category = "adoption"
            Criticality = "HIGH"
            File = sprintf "specs/apps/%s/behavior" app
            Evidence = sprintf "no feature files found under specs/apps/%s/behavior/" app
            Expected = sprintf "add at least one .feature file under specs/apps/%s/behavior/" app } ]
    else
        []

/// The missing-`bounded-contexts.yaml` finding shared by both adoption
/// validators.
let private missingBoundedContextsFinding (app: string) : SpecFinding =
    { Category = "adoption"
      Criticality = "HIGH"
      File = sprintf "specs/apps/%s/ddd" app
      Evidence = sprintf "missing bounded-contexts.yaml at specs/apps/%s/ddd/bounded-contexts.yaml" app
      Expected = sprintf "create specs/apps/%s/ddd/bounded-contexts.yaml" app }

/// Checks that `app` has adopted the spec conventions: a `behavior/` folder
/// holding at least one `.feature` file, and a
/// `ddd/bounded-contexts.yaml`.
let validateSpecAdoption (repoRoot: string) (app: string) : SpecFinding list =
    let bcYaml =
        Path.Combine(repoRoot, "specs/apps", app, "ddd", "bounded-contexts.yaml")

    behaviorAdoptionFindings repoRoot app
    @ (if File.Exists bcYaml then
           []
       else
           [ missingBoundedContextsFinding app ])

/// Config-aware adoption validator: requires `ddd/` only when `isDddArea` is
/// true, and flags an unexpected `ddd/` directory when it is not.
let validateSpecAdoptionDddAware (repoRoot: string) (app: string) (isDddArea: bool) : SpecFinding list =
    let dddDir = Path.Combine(repoRoot, "specs/apps", app, "ddd")
    let bcYaml = Path.Combine(dddDir, "bounded-contexts.yaml")

    let dddFindings =
        if isDddArea then
            if File.Exists bcYaml then
                []
            else
                [ missingBoundedContextsFinding app ]
        elif Directory.Exists dddDir then
            [ { Category = "adoption"
                Criticality = "HIGH"
                File = sprintf "specs/apps/%s/ddd" app
                Evidence = sprintf "unexpected ddd/ at specs/apps/%s/ddd — area not listed in specs.ddd-areas" app
                Expected = sprintf "remove specs/apps/%s/ddd/ or add %s to specs.ddd-areas in repo-config.yml" app app } ]
        else
            []

    behaviorAdoptionFindings repoRoot app @ dddFindings

/// Checks that `folder` exists and that each required subfolder is present
/// and holds at least one non-`README.md` spec file.
let validateSpecCounts (repoRoot: string) (folder: string) : SpecFinding list =
    let abs =
        if Path.IsPathRooted folder then
            folder
        else
            Path.Combine(repoRoot, folder)

    if not (Directory.Exists abs || File.Exists abs) then
        [ { Category = "count"
            Criticality = "HIGH"
            File = folder
            Evidence = sprintf "spec folder does not exist: %s" folder
            Expected = "create the spec folder with required subfolders" } ]
    else
        requiredSpecFolders
        |> List.collect (fun sub ->
            let subPath = Path.Combine(abs, sub)
            let rel = sprintf "%s/%s" folder sub

            if not (Directory.Exists subPath) then
                [ { Category = "count"
                    Criticality = "HIGH"
                    File = rel
                    Evidence = sprintf "missing required folder: %s" sub
                    Expected = sprintf "create %s/README.md plus at least one spec .md file" rel } ]
            elif countNonReadmeMdFiles subPath = 0 then
                [ { Category = "count"
                    Criticality = "MEDIUM"
                    File = rel
                    Evidence = sprintf "empty subfolder: %s contains no spec files (only README.md or nothing)" sub
                    Expected = sprintf "add at least one non-README .md spec file to %s/" rel } ]
            else
                [])

/// Checks that the spec tree for `app` has every required subfolder and that
/// each one carries a `README.md`.
let validateSpecTree (repoRoot: string) (app: string) : SpecFinding list =
    let baseDir = Path.Combine(repoRoot, "specs/apps", app)

    requiredSpecFolders
    |> List.collect (fun folder ->
        let folderPath = Path.Combine(baseDir, folder)

        if not (Directory.Exists folderPath) then
            [ { Category = "tree-shape"
                Criticality = "HIGH"
                File = sprintf "specs/apps/%s" app
                Evidence = sprintf "missing required folder: %s" folder
                Expected = sprintf "create specs/apps/%s/%s/ with README.md" app folder } ]
        elif not (File.Exists(Path.Combine(folderPath, "README.md"))) then
            [ { Category = "tree-shape"
                Criticality = "HIGH"
                File = sprintf "specs/apps/%s/%s" app folder
                Evidence = sprintf "missing README.md in required folder: %s" folder
                Expected = sprintf "create specs/apps/%s/%s/README.md" app folder } ]
        else
            [])

// ---------------------------------------------------------------------------
// Gherkin step-keyword cardinality audit
// [Repo-grounded —
// `apps/rhino-cli/src/application/repo_governance/gherkin_keyword_cardinality_audit.rs`]
// for `gherkin-cardinality.feature`.
// ---------------------------------------------------------------------------

/// A single step-keyword cardinality violation found in a `.feature` file.
type GherkinCardinalityFinding =
    {
        /// Path of the `.feature` file containing the violation.
        File: string
        /// 1-based line number of the scenario declaration.
        Line: int
        /// Name of the offending scenario (text after `Scenario:`).
        Scenario: string
        /// Primary keyword that appears more than once.
        Keyword: string
        /// Number of primary occurrences of `Keyword` in the scenario.
        Count: int
        /// Severity; currently always `"high"`.
        Severity: string
    }

/// Primary Gherkin step keywords subject to the cardinality rule.
let private primaryKeywords = [| "Given"; "When"; "Then" |]

/// Directory names skipped during the walk (build outputs, vendored code,
/// worktrees, and archived sources).
let private gherkinSkipDirs =
    [ "node_modules"
      ".git"
      "bin"
      "build"
      "target"
      "dist"
      "worktrees"
      "archived" ]

/// Path fragments excluded from the scan: BDD-library self-test fixtures that
/// deliberately use non-conforming Gherkin shapes.
let private excludedFeaturePathFragments =
    [ "libs/elixir-cabbage/test/features/"; "libs/elixir-gherkin/test/fixtures/" ]

/// `true` when the slash-normalised `path` falls inside an excluded fixture
/// fragment.
let private isExcludedFeaturePath (path: string) : bool =
    let slashed = path.Replace('\\', '/')

    excludedFeaturePathFragments
    |> List.exists (fun fragment -> slashed.Contains(fragment, StringComparison.Ordinal))

/// Recursively walks `root` returning sorted `.feature` paths, skipping
/// [`gherkinSkipDirs`] directories and excluded fixture paths.
let rec private walkFeaturePaths (root: string) : string list =
    if not (Directory.Exists root) then
        []
    else
        let entries =
            try
                Directory.GetFileSystemEntries root |> List.ofArray
            with _ ->
                []

        entries
        |> List.collect (fun path ->
            if Directory.Exists path then
                if gherkinSkipDirs |> List.contains (Path.GetFileName path) then
                    []
                else
                    walkFeaturePaths path
            elif Path.GetFileName(path).ToLowerInvariant().EndsWith(".feature", StringComparison.Ordinal) then
                [ path ]
            else
                [])
        |> List.filter (isExcludedFeaturePath >> not)
        |> sortPaths

/// A Gherkin block header recognised by the cardinality scanner.
type private BlockHeader =
    /// `Background:` — exempt from the cardinality rule.
    | Background
    /// `Scenario:` / `Scenario Outline:` / `Scenario Template:` with its name.
    | ScenarioHeader of string
    /// `Examples:` / `Scenarios:` — a `Scenario Outline` table, exempt.
    | ExamplesHeader
    /// `Feature:` / `Rule:` — structural headers that end any open scenario.
    | Structural

/// Classification of a single trimmed `.feature` line.
type private LineClass =
    | DocStringDelimiter
    | CommentLine
    | HeaderLine of BlockHeader
    | PrimaryStep of int
    | OtherLine

/// Parses `trimmed` as a Gherkin block header, if it is one.
let private parseBlockHeader (trimmed: string) : BlockHeader option =
    if trimmed.StartsWith("Background:", StringComparison.Ordinal) then
        Some Background
    else
        let scenarioPrefix =
            [ "Scenario Outline:"; "Scenario Template:"; "Scenario:" ]
            |> List.tryFind (fun prefix -> trimmed.StartsWith(prefix, StringComparison.Ordinal))

        match scenarioPrefix with
        | Some prefix -> Some(ScenarioHeader(trimmed.Substring(prefix.Length).Trim()))
        | None ->
            if
                trimmed.StartsWith("Examples:", StringComparison.Ordinal)
                || trimmed.StartsWith("Scenarios:", StringComparison.Ordinal)
            then
                Some ExamplesHeader
            elif
                trimmed.StartsWith("Feature:", StringComparison.Ordinal)
                || trimmed.StartsWith("Rule:", StringComparison.Ordinal)
            then
                Some Structural
            else
                None

/// Returns the [`primaryKeywords`] index when `trimmed` opens with a primary
/// keyword followed by whitespace. `And`/`But`/`*` continuations return
/// `None`.
let private primaryKeywordIndex (trimmed: string) : int option =
    primaryKeywords
    |> Array.tryFindIndex (fun keyword ->
        trimmed.StartsWith(keyword, StringComparison.Ordinal)
        && trimmed.Length > keyword.Length
        && Char.IsWhiteSpace trimmed.[keyword.Length])

/// Classifies a trimmed `.feature` line for the cardinality scanner.
let private classifyLine (trimmed: string) : LineClass =
    if
        trimmed.StartsWith("\"\"\"", StringComparison.Ordinal)
        || trimmed.StartsWith("```", StringComparison.Ordinal)
    then
        DocStringDelimiter
    elif trimmed.StartsWith("#", StringComparison.Ordinal) then
        CommentLine
    else
        match parseBlockHeader trimmed with
        | Some header -> HeaderLine header
        | None ->
            match primaryKeywordIndex trimmed with
            | Some index -> PrimaryStep index
            | None -> OtherLine

/// Scans one `.feature` file's `content` (reported as `file`) and returns
/// every step-keyword cardinality violation.
let scanFeatureContent (file: string) (content: string) : GherkinCardinalityFinding list =
    let findings = ResizeArray<GherkinCardinalityFinding>()
    let counts = Array.zeroCreate<int> primaryKeywords.Length
    let mutable inDocString = false
    let mutable inExamples = false
    let mutable scenario: (string * int) option = None

    let flushScenario () =
        match scenario with
        | Some(name, line) ->
            primaryKeywords
            |> Array.iteri (fun i keyword ->
                if counts.[i] > 1 then
                    findings.Add
                        { File = file
                          Line = line
                          Scenario = name
                          Keyword = keyword
                          Count = counts.[i]
                          Severity = "high" })

            scenario <- None
        | None -> ()

        Array.fill counts 0 counts.Length 0

    splitLines content
    |> Array.iteri (fun index raw ->
        let lineNum = index + 1
        let cls = classifyLine (raw.Trim())

        if inDocString then
            match cls with
            | DocStringDelimiter -> inDocString <- false
            | _ -> ()
        else
            match cls with
            | DocStringDelimiter -> inDocString <- true
            | CommentLine
            | OtherLine -> ()
            | HeaderLine header ->
                match header with
                | ScenarioHeader name ->
                    flushScenario ()
                    scenario <- Some(name, lineNum)
                    inExamples <- false
                | Background
                | Structural ->
                    flushScenario ()
                    inExamples <- false
                | ExamplesHeader -> inExamples <- true
            | PrimaryStep k ->
                if scenario.IsSome && not inExamples then
                    counts.[k] <- counts.[k] + 1)

    flushScenario ()
    List.ofSeq findings

/// Walks each directory in `paths` and reports every scenario using a primary
/// keyword more than once, sorted by file, then line, then keyword.
let auditGherkinKeywordCardinality (paths: string list) : Result<GherkinCardinalityFinding list, string> =
    if List.isEmpty paths then
        Error "at least one path is required"
    else
        try
            paths
            |> List.collect (fun root ->
                walkFeaturePaths root
                |> List.collect (fun file -> scanFeatureContent file (File.ReadAllText file)))
            |> List.sortWith (fun a b ->
                match String.CompareOrdinal(a.File, b.File) with
                | 0 ->
                    match compare a.Line b.Line with
                    | 0 -> String.CompareOrdinal(a.Keyword, b.Keyword)
                    | other -> other
                | other -> other)
            |> Ok
        with ex ->
            Error(sprintf "gherkin keyword cardinality audit failed: %s" ex.Message)

/// Formats cardinality findings as human-readable text.
let formatCardinalityText (findings: GherkinCardinalityFinding list) : string =
    if List.isEmpty findings then
        "GHERKIN KEYWORD CARDINALITY AUDIT PASSED: every scenario uses each primary keyword at most once\n"
    else
        let sb = StringBuilder()

        sb.Append(sprintf "GHERKIN KEYWORD CARDINALITY AUDIT FAILED: %d violation(s) found\n" (List.length findings))
        |> ignore

        for f in findings do
            sb.Append(
                sprintf
                    "  %s:%d  [%s]  scenario '%s' uses primary '%s' %d times (chain extras with And/But)\n"
                    f.File
                    f.Line
                    f.Severity
                    f.Scenario
                    f.Keyword
                    f.Count
            )
            |> ignore

        sb.ToString()

// ---------------------------------------------------------------------------
// `specs audit` aggregation
// [Repo-grounded — `apps/rhino-cli/src/commands/specs_audit.rs`] for
// `specs-audit.feature`.
// ---------------------------------------------------------------------------

/// Member validators `specs audit` runs, in order. `behavior-coverage`,
/// `domain-coverage`, `bc`, and `ul` are excluded because they need
/// domain-specific positional arguments `audit` cannot default.
let specsAuditMembers: string list =
    [ "structure-validate"; "validate-links"; "gherkin-cardinality" ]

/// The aggregated result of one `specs audit` run.
type SpecsAuditOutcome =
    {
        /// `true` when every non-skipped member passed.
        Passed: bool
        /// The single summary line printed to stdout (pass) or stderr (fail).
        Summary: string
        /// `"<member>: <error>"` for each failing member, in member order.
        Failures: string list
    }

/// Runs each non-skipped member through `runMember` and aggregates the result.
let runSpecsAudit (skip: string list) (runMember: string -> Result<unit, string>) : SpecsAuditOutcome =
    let failures =
        specsAuditMembers
        |> List.filter (fun name -> not (List.contains name skip))
        |> List.choose (fun name ->
            match runMember name with
            | Ok() -> None
            | Error message -> Some(sprintf "%s: %s" name message))

    if List.isEmpty failures then
        { Passed = true
          Summary =
            sprintf "SPECS AUDIT PASSED: all %d validators passed" (List.length specsAuditMembers - List.length skip)
          Failures = [] }
    else
        { Passed = false
          Summary = sprintf "SPECS AUDIT FAILED: %d validator(s) reported failures" (List.length failures)
          Failures = failures }

/// Returns `path` relative to `basePath` by stripping the prefix, or `path`
/// unchanged when it does not start with `basePath`.
let private pathdiffStartsWith (path: string) (basePath: string) : string =
    if path.StartsWith(basePath, StringComparison.Ordinal) then
        path.Substring(basePath.Length).TrimStart('/', '\\')
    else
        path

/// Checks that every `.feature` file under `behavior/<surface>/gherkin/`
/// lives inside a domain subdirectory rather than directly at the `gherkin/`
/// root.
let validateSpecGherkinDomains (repoRoot: string) (app: string) : SpecFinding list =
    let behavior = Path.Combine(repoRoot, "specs/apps", app, "behavior")

    if not (Directory.Exists behavior) then
        []
    else
        Directory.GetDirectories behavior
        |> List.ofArray
        |> sortPaths
        |> List.collect (fun surfacePath ->
            let gherkin = Path.Combine(surfacePath, "gherkin")

            if not (Directory.Exists gherkin) then
                []
            else
                Directory.GetFiles gherkin
                |> List.ofArray
                |> sortPaths
                |> List.filter (fun p ->
                    Path.GetFileName(p).ToLowerInvariant().EndsWith(".feature", StringComparison.Ordinal))
                |> List.map (fun p ->
                    let rel = pathdiffStartsWith p repoRoot

                    { Category = "tree-shape"
                      Criticality = "HIGH"
                      File = rel
                      Evidence =
                        sprintf
                            "flat feature file at %s; expected behavior/<surface>/gherkin/<domain>/<feature>.feature"
                            rel
                      Expected = sprintf "move %s into a domain subdirectory under the gherkin/ folder" rel }))

/// Validates every relative markdown link reachable from `folder`, reported
/// as `"links"` findings. A `folder` that does not exist is itself a
/// `"HIGH"` finding rather than an empty pass
/// [Repo-grounded — `specs_audit.rs` routes `validate-links` through
/// `md_validate_links::run`, whose engine is `Md.validateDocsLinks`].
let validateSpecLinks (repoRoot: string) (folder: string) : SpecFinding list =
    let abs =
        if Path.IsPathRooted folder then
            folder
        else
            Path.Combine(repoRoot, folder)

    if not (Directory.Exists abs) then
        [ { Category = "links"
            Criticality = "HIGH"
            File = folder
            Evidence = sprintf "spec folder does not exist: %s" folder
            Expected = "create the spec folder with required subfolders" } ]
    else
        Md.validateDocsLinks
            { RepoRoot = abs
              StagedFiles = None
              ExcludePrefixes = [] }
        |> List.map (fun finding ->
            { Category = "links"
              Criticality = "HIGH"
              File = finding.Path |> Option.defaultValue folder
              Evidence = sprintf "broken link: %s" finding.Message
              Expected = "point the link at an existing file, or remove it" })

/// Renders `findings` the way `specs structure validate` prints them —
/// `"<category>: <file>: HIGH: <evidence>"` per finding — followed by the
/// per-app `"0 finding(s)"` line when nothing was found
/// [Repo-grounded — `specs_structure_validate.rs::run_at_root`].
let formatSpecFindingsText (app: string) (findings: SpecFinding list) : string =
    if List.isEmpty findings then
        sprintf "specs structure validate: 0 finding(s) for \"%s\"\n" app
    else
        findings
        |> List.map (fun f -> sprintf "%s: %s: HIGH: %s\n" f.Category f.File f.Evidence)
        |> String.concat ""

// ---------------------------------------------------------------------------
// BDD spec-to-test coverage validation
// [Repo-grounded — `apps/rhino-cli/src/application/speccoverage/{types,util,
// cucumber_expr,matcher,parser,extractors,checker,reporter,runtime_check}.rs`]
// for `spec-coverage-validate.feature`'s 12 scenarios.
// ---------------------------------------------------------------------------

/// Collapses runs of ASCII whitespace to a single space and trims.
let normalizeWs (s: string) : string =
    s.Split([| ' '; '\t'; '\n'; '\r'; '\f'; '\v' |], StringSplitOptions.RemoveEmptyEntries)
    |> String.concat " "

/// Returns `a` when non-empty, otherwise `b`.
let private firstNonEmpty (a: string) (b: string) : string = if a = "" then b else a

/// Interprets JS/TS-style escape sequences (`\'`, `\"`, `\\`, `\/`, `\n`,
/// `\t`, `\r`); any other `\X` pair passes `X` through unchanged.
let unescapeSourceString (s: string) : string =
    let out = StringBuilder(s.Length)
    let mutable i = 0

    while i < s.Length do
        if s.[i] = '\\' && i + 1 < s.Length then
            let decoded =
                match s.[i + 1] with
                | '\'' -> '\''
                | '"' -> '"'
                | '\\' -> '\\'
                | '/' -> '/'
                | 'n' -> '\n'
                | 't' -> '\t'
                | 'r' -> '\r'
                | other -> other

            out.Append(decoded) |> ignore
            i <- i + 2
        else
            out.Append(s.[i]) |> ignore
            i <- i + 1

    out.ToString()

/// Finds the index range of the next Cucumber parameter placeholder (`{type}`)
/// in `text`, skipping any brace escaped with a backslash.
let private findNextParam (text: string) : (int * int) option =
    let mutable i = 0
    let mutable result = None

    while result.IsNone && i < text.Length do
        if text.[i] = '\\' then
            i <- i + 2
        elif text.[i] = '{' then
            let start = i
            let mutable j = i + 1
            let mutable closed = -1

            while closed < 0 && j < text.Length do
                if text.[j] = '\\' then j <- j + 2
                elif text.[j] = '}' then closed <- j
                else j <- j + 1

            result <- (if closed < 0 then Some(-1, -1) else Some(start, closed + 1))
            i <- text.Length
        else
            i <- i + 1

    match result with
    | Some(-1, -1) -> None
    | other -> other

/// Decodes Cucumber expression escape sequences: `\X` becomes `X`.
let unescapeCucumberExpr (s: string) : string =
    let out = StringBuilder(s.Length)
    let mutable i = 0

    while i < s.Length do
        if s.[i] = '\\' && i + 1 < s.Length then
            out.Append(s.[i + 1]) |> ignore
            i <- i + 2
        else
            out.Append(s.[i]) |> ignore
            i <- i + 1

    out.ToString()

/// Maps a Cucumber parameter type name to its regex fragment; an unknown name
/// maps to `.+`.
let cucumberParamToRegex (paramName: string) : string =
    match paramName with
    | "string" -> "\"[^\"]*\""
    | "int"
    | "byte"
    | "short"
    | "long" -> @"-?\d+"
    | "float"
    | "double"
    | "bigdecimal" -> @"-?\d+\.?\d*"
    | "word" -> @"\S+"
    | _ -> ".+"

/// Converts a Cucumber expression into an unanchored regex pattern string.
let cucumberExprToRegex (text: string) : string =
    let sb = StringBuilder()
    let mutable remaining = text
    let mutable finished = false

    while not finished do
        match findNextParam remaining with
        | None ->
            sb.Append(Regex.Escape(unescapeCucumberExpr remaining)) |> ignore
            finished <- true
        | Some(start, endIdx) ->
            sb.Append(Regex.Escape(unescapeCucumberExpr (remaining.Substring(0, start))))
            |> ignore

            let param = remaining.Substring(start, endIdx - start)
            sb.Append(cucumberParamToRegex (param.Substring(1, param.Length - 2))) |> ignore
            remaining <- remaining.Substring(endIdx)

    sb.ToString()

/// `true` when `text` carries at least one Cucumber parameter placeholder.
let hasCucumberExpressions (text: string) : bool = (findNextParam text).IsSome

/// Distinguishes how a step entry was registered.
type MatcherKind =
    | Exact
    | Pattern

/// A single step-definition record stored inside a [`StepMatcher`].
type StepMatcherEntry =
    {
        Kind: MatcherKind
        /// Whitespace-normalised text, when `Kind = Exact`.
        ExactText: string
        /// Raw pattern source, when `Kind = Pattern`.
        PatternText: string
        /// Absolute path of the source file defining this step.
        File: string
        /// The compiled pattern, when `Kind = Pattern`. Held on the entry
        /// itself rather than in a parallel list — Rust reaches the same
        /// regex through `pattern_index_for_entry`'s lockstep index.
        Compiled: Regex option
    }

/// In-memory collection of step definitions extracted from source files:
/// O(1) exact lookup after whitespace normalisation, linear scan over
/// compiled patterns.
type StepMatcher() =
    let entries = ResizeArray<StepMatcherEntry>()
    let exactTexts = Collections.Generic.HashSet<string>()
    let patterns = ResizeArray<Regex>()

    /// All registered entries, in insertion order.
    member _.Entries: StepMatcherEntry list = List.ofSeq entries

    member _.IsEmpty: bool = entries.Count = 0

    /// `true` when `stepText` matches an exact entry or any compiled pattern.
    member _.Matches(stepText: string) : bool =
        let normalized = normalizeWs stepText

        exactTexts.Contains normalized
        || patterns |> Seq.exists (fun re -> re.IsMatch normalized)

    /// Registers `text` as an exact entry; empty text is ignored.
    member _.AddExact(text: string, originFile: string) : unit =
        let normalized = normalizeWs text

        if normalized <> "" then
            entries.Add
                { Kind = Exact
                  ExactText = normalized
                  PatternText = ""
                  File = originFile
                  Compiled = None }

            exactTexts.Add normalized |> ignore

    /// Registers `re` as a compiled pattern entry, keeping `patternText` for
    /// display.
    member _.AddPattern(re: Regex, patternText: string, originFile: string) : unit =
        entries.Add
            { Kind = Pattern
              ExactText = ""
              PatternText = patternText
              File = originFile
              Compiled = Some re }

        patterns.Add re

/// Compiles `re` defensively — an unparseable pattern is dropped rather than
/// raised, matching Rust's `if let Ok(re) = Regex::new(...)`.
let private tryRegex (pattern: string) : Regex option =
    try
        Some(Regex pattern)
    with _ ->
        None

/// Inserts a step-text string into `sm`, choosing the entry kind: a leading
/// `^` compiles as a traditional regex, a `{…}` placeholder compiles as an
/// anchored Cucumber expression, anything else stores as an exact literal.
let addStepToMatcher (sm: StepMatcher) (text: string) (originFile: string) : unit =
    let text = normalizeWs text

    if text <> "" then
        if text.StartsWith("^", StringComparison.Ordinal) then
            match tryRegex text with
            | Some re -> sm.AddPattern(re, text, originFile)
            | None -> ()
        elif hasCucumberExpressions text then
            match tryRegex (sprintf "^%s$" (cucumberExprToRegex text)) with
            | Some re -> sm.AddPattern(re, text, originFile)
            | None -> ()
        else
            sm.AddExact(unescapeCucumberExpr text, originFile)

/// A single parsed Gherkin step.
type ParsedStep =
    {
        /// Gherkin keyword without trailing whitespace.
        Keyword: string
        /// Step text after the keyword, with `<placeholder>` tokens verbatim.
        Text: string
        /// Step texts produced by substituting each `Examples` row; empty for
        /// a plain (non-outline) step.
        Variants: string list
    }

/// A parsed Gherkin scenario, or the synthetic `(Background)` scenario.
type ParsedScenario =
    {
        Title: string
        Steps: ParsedStep list
        /// `true` when a `@wip` tag line precedes this scenario, surviving
        /// intervening blank and `#`-comment lines.
        IsWip: bool
    }

type private MutStep =
    { Keyword: string
      Text: string
      Variants: ResizeArray<string> }

type private MutScenario =
    { Title: string
      IsWip: bool
      Steps: ResizeArray<MutStep> }

let private stepKeywords = [| "Given "; "When "; "Then "; "And "; "But " |]

/// Splits a Gherkin table row into trimmed cell values, dropping the leading
/// and trailing pipes.
let private parseRow (line: string) : string list =
    line.Trim().Trim('|').Split('|')
    |> Array.map (fun p -> p.Trim())
    |> List.ofArray

/// Substitutes `<header>` tokens in `text` with the row value at the same
/// index; excess headers are left unexpanded.
let private expandStep (text: string) (headers: string list) (row: string list) : string =
    let mutable out = text
    let rowArr = List.toArray row

    headers
    |> List.iteri (fun i h ->
        if i < rowArr.Length then
            out <- out.Replace(sprintf "<%s>" h, rowArr.[i]))

    out

/// Parses Gherkin `content`, returning its scenarios (a synthetic
/// `(Background)` scenario is prepended when a `Background:` block exists) and
/// every expanded `Scenario Outline` step text.
let parseFeatureContent (content: string) : ParsedScenario list * string list =
    let scenarios = ResizeArray<MutScenario>()
    let expandedSteps = ResizeArray<string>()
    let bgSteps = ResizeArray<MutStep>()
    let mutable inBackground = false
    let mutable current: MutScenario option = None
    let mutable pendingOutline: ResizeArray<MutStep> option = None
    let mutable inExamples = false
    let mutable exHeaders: string list option = None
    let mutable pendingWip = false

    let pushScenario (title: string) (isOutline: bool) =
        inExamples <- false
        exHeaders <- None
        inBackground <- false

        let sc =
            { Title = title
              IsWip = pendingWip
              Steps = ResizeArray<MutStep>() }

        scenarios.Add sc
        current <- Some sc
        pendingOutline <- (if isOutline then Some(ResizeArray<MutStep>()) else None)
        pendingWip <- false

    let tryPushStep (line: string) =
        stepKeywords
        |> Array.tryFind (fun kw -> line.StartsWith(kw, StringComparison.Ordinal))
        |> Option.map (fun kw ->
            let step =
                { Keyword = kw.Trim()
                  Text = line.Substring(kw.Length).Trim()
                  Variants = ResizeArray<string>() }

            if inBackground then
                bgSteps.Add step
            else
                match current with
                | Some sc ->
                    sc.Steps.Add step

                    match pendingOutline with
                    | Some outline -> outline.Add step
                    | None -> ()
                | None -> ())
        |> Option.isSome

    let handleExamplesRow (line: string) =
        let row = parseRow line

        match exHeaders with
        | None -> exHeaders <- Some row
        | Some headers ->
            match pendingOutline with
            | Some outline when current.IsSome ->
                for step in outline do
                    let exp = expandStep step.Text headers row
                    step.Variants.Add exp
                    expandedSteps.Add exp
            | _ -> ()

    for raw in content.Split('\n') do
        let line = raw.Trim()

        if line = "" then
            ()
        elif line.StartsWith("@", StringComparison.Ordinal) then
            if
                line.Split([| ' '; '\t' |], StringSplitOptions.RemoveEmptyEntries)
                |> Array.exists (fun tag -> tag = "@wip")
            then
                pendingWip <- true
        elif line.StartsWith("#", StringComparison.Ordinal) then
            ()
        elif line.StartsWith("Background:", StringComparison.Ordinal) then
            inExamples <- false
            exHeaders <- None
            pendingOutline <- None
            inBackground <- true
            current <- None
            pendingWip <- false
        elif line.StartsWith("Scenario Outline:", StringComparison.Ordinal) then
            pushScenario (line.Substring("Scenario Outline:".Length).Trim()) true
        elif line.StartsWith("Scenario:", StringComparison.Ordinal) then
            pushScenario (line.Substring("Scenario:".Length).Trim()) false
        elif line.StartsWith("Examples:", StringComparison.Ordinal) then
            inExamples <- true
            exHeaders <- None
        elif inExamples && line.StartsWith("|", StringComparison.Ordinal) then
            handleExamplesRow line
        elif tryPushStep line then
            ()
        else
            pendingWip <- false

    if bgSteps.Count > 0 then
        scenarios.Insert(
            0,
            { Title = "(Background)"
              IsWip = false
              Steps = bgSteps }
        )

    let parsed =
        scenarios
        |> Seq.map (fun sc ->
            { ParsedScenario.Title = sc.Title
              IsWip = sc.IsWip
              Steps =
                sc.Steps
                |> Seq.map (fun st ->
                    { ParsedStep.Keyword = st.Keyword
                      Text = st.Text
                      Variants = List.ofSeq st.Variants })
                |> List.ofSeq })
        |> List.ofSeq

    parsed, List.ofSeq expandedSteps

/// Parses the `.feature` file at `path`.
let parseFeatureFile (path: string) : ParsedScenario list =
    fst (parseFeatureContent (File.ReadAllText path))

/// Inputs for one spec-coverage scan.
type ScanOptions =
    {
        /// Absolute repo root, stripped from every reported path.
        RepoRoot: string
        /// Single spec directory, used when `SpecsDirs` is empty.
        SpecsDir: string
        /// Spec directories to walk for `.feature` files.
        SpecsDirs: string list
        /// Source tree scanned for test files and step definitions.
        AppDir: string
        /// `true` selects shared-step mode (no filename correspondence).
        SharedSteps: bool
        /// Directory names skipped while walking the spec tree.
        ExcludeDirs: string list
        /// Extra directory names skipped while walking `AppDir`.
        ExcludeSourceDirs: string list
    }

/// A `.feature` file with no corresponding test file (1-to-1 mode only).
type CoverageGap = { SpecFile: string; Stem: string }

/// A scenario whose title appears in no test file (1-to-1 mode only).
type ScenarioGap =
    { SpecFile: string
      ScenarioTitle: string }

/// A Gherkin step matched by no step definition.
type StepGap =
    { SpecFile: string
      ScenarioTitle: string
      StepKeyword: string
      StepText: string }

/// A step definition matching no Gherkin step anywhere.
type OrphanStepImpl =
    { File: string
      MatcherKind: string
      MatcherText: string }

/// Outcome of one spec-coverage scan.
type CheckResult =
    { TotalSpecs: int
      TotalScenarios: int
      TotalSteps: int
      Gaps: CoverageGap list
      ScenarioGaps: ScenarioGap list
      StepGaps: StepGap list
      OrphanStepImpls: OrphanStepImpl list }

let private dotAll = RegexOptions.Singleline

let private scenarioDefRe =
    Regex(@"Scenario\s*\(\s*(?:""((?:[^""\\]|\\.)*)""|'((?:[^'\\]|\\.)*)')\s*,", dotAll)

let private stepDefRe =
    Regex(@"(?:Given|When|Then|And|But)\s*\(\s*(?:""((?:[^""\\]|\\.)*)""|'((?:[^'\\]|\\.)*)')\s*,", dotAll)

let private tsRegexStepRe =
    Regex(@"(?:Given|When|Then|And|But)\s*\(\s*/\^?(.*?)\$?\s*/\s*,", dotAll)

let private scenarioCommentRe = Regex(@"//\s*Scenario:\s*(.+?)\s*$")

let private rsStepLiteralRe =
    Regex(@"#\[(?:given|when|then)\s*\(\s*""((?:[^""\\]|\\.)*)""\s*\)\s*\]")

let private rsStepLiteralRawRe =
    Regex(@"#\[(?:given|when|then)\s*\(\s*r#""(.*?)""#\s*\)\s*\]")

let private rsStepExprRe =
    Regex(@"#\[(?:given|when|then)\s*\(\s*expr\s*=\s*""((?:[^""\\]|\\.)*)""\s*\)\s*\]")

let private rsStepRegexRe =
    Regex(@"#\[(?:given|when|then)\s*\(\s*regex\s*=\s*r#""(.*?)""#\s*\)\s*\]")

let private rsStepRegexBareRe =
    Regex(@"#\[(?:given|when|then)\s*\(\s*regex\s*=\s*r""(.*?)""\s*\)\s*\]")

let private dartStepRe =
    Regex(
        @"\b(?:s|scenario)\.(?:given|when|then|and|but)\s*\(\s*(?:""((?:[^""\\]|\\.)*)""|'((?:[^'\\]|\\.)*)')\s*,",
        dotAll
    )

let private csVerbatimStepRe =
    Regex(@"\[(?:Given|When|Then|And|But)\s*\(\s*@""((?:[^""]|"""")*)""\s*\)\s*\]", dotAll)

let private csRegularStepRe =
    Regex(@"\[(?:Given|When|Then|And|But)\s*\(\s*""((?:[^""\\]|\\.)*)""\s*\)\s*\]", dotAll)

let private fsStepAttrRe = Regex(@"\[<(?:Given|When|Then|And|But)>]")

let private fsStepRe =
    Regex(
        @"(?:let\s+(?:\[<(?:Given|When|Then|And|But)>\]\s*)?|\[<(?:Given|When|Then|And|But)>\]\s*member\s+\S+\s*\.\s*)``((?:[^`]|`[^`])*)``"
    )

let private fsLetBacktickRe =
    Regex(@"(?:let\s+|member\s+\S+\s*\.\s*)``((?:[^`]|`[^`])*)``")

/// Directory names never scanned: generated output, dependency caches, and
/// `fixtures` (step-def-shaped content authored only to exercise this
/// checker's own tests, which would otherwise read as orphan step impls).
let private coverageSkipDirs =
    Collections.Generic.HashSet<string>(
        [ "node_modules"
          ".next"
          "build"
          "dist"
          "storybook-static"
          "coverage"
          ".git"
          "target"
          "_build"
          "deps"
          "bin"
          "obj"
          "__pycache__"
          ".pytest_cache"
          ".venv"
          "generated-contracts"
          "generated_contracts"
          ".dart_tool"
          ".features-gen"
          "fixtures" ]
    )

/// `true` when `name` is skipped while walking an app source tree. Kept
/// separate from the spec-tree `--exclude-dir` list so that excluding a name
/// in one tree never silently excludes the same name in the other.
let private isExcludedSourceDir (name: string) (excludeSourceDirs: string list) : bool =
    coverageSkipDirs.Contains name || List.contains name excludeSourceDirs

/// Recursively lists files under `dir`, pruning any directory whose name
/// satisfies `skipDir`. Returns `[]` when `dir` does not exist.
let rec private walkFiltered (dir: string) (skipDir: string -> bool) : string list =
    if not (Directory.Exists dir) then
        []
    else
        let files = Directory.GetFiles dir |> Array.sort |> List.ofArray

        let subdirs =
            Directory.GetDirectories dir
            |> Array.sort
            |> Array.filter (fun d -> not (skipDir (Path.GetFileName d)))
            |> List.ofArray

        files @ (subdirs |> List.collect (fun d -> walkFiltered d skipDir))

/// Recursively lists every `.feature` file under `dir`, skipping directories
/// named in `excludeDirs`.
let coverageWalkFeatureFiles (dir: string) (excludeDirs: string list) : string list =
    walkFiltered dir (fun name -> List.contains name excludeDirs)
    |> List.filter (fun p -> p.EndsWith(".feature", StringComparison.Ordinal))

/// Returns `p` relative to `root`, or `p` unchanged when `root` is empty or
/// is not a prefix of `p`.
let private relTo (root: string) (p: string) : string =
    if root = "" then
        p
    else
        let prefix =
            if root.EndsWith(string Path.DirectorySeparatorChar, StringComparison.Ordinal) then
                root
            else
                root + string Path.DirectorySeparatorChar

        if p.StartsWith(prefix, StringComparison.Ordinal) then
            p.Substring(prefix.Length)
        else
            p

/// Converts a kebab-case stem to `PascalCase`, skipping empty segments.
let private toPascalCase (stem: string) : string =
    stem.Split('-')
    |> Array.filter (fun p -> p <> "")
    |> Array.map (fun p -> string (Char.ToUpper(p.[0], CultureInfo.InvariantCulture)) + p.Substring 1)
    |> String.concat ""

/// `true` when file base name `base'` is a plausible test file for feature
/// stem `stem`, across kebab-case, `snake_case`, `PascalCase`, and
/// `test_<snake>` conventions.
let private matchesStem (base': string) (stem: string) : bool =
    let snake = stem.Replace('-', '_')
    let pascal = toPascalCase stem
    let testSnake = "test_" + snake

    let prefixes =
        [ stem + "."
          stem + "_"
          snake + "."
          snake + "_"
          pascal
          testSnake + "."
          testSnake + "_" ]

    prefixes |> List.exists (fun p -> base'.StartsWith(p, StringComparison.Ordinal))
    || base' = stem
    || base' = snake

/// `true` when any path component of `path` is `test`, `tests`, or `Tests`.
let private isInTestDir (path: string) : bool =
    path.Split([| Path.DirectorySeparatorChar; '/' |])
    |> Array.exists (fun c -> c = "test" || c = "tests" || c = "Tests")

/// `true` when `path` is a test/step file, judged by extension plus each
/// language's own test-file naming convention.
let private isTestFile (path: string) : bool =
    let base' = Path.GetFileName path
    let ext = Path.GetExtension(path).TrimStart('.')

    match ext with
    | "" -> true
    | "ts"
    | "tsx"
    | "js"
    | "jsx" ->
        base'.Contains ".test."
        || base'.Contains ".spec."
        || base'.Contains ".steps."
        || base'.Contains ".integration."
        || base'.Contains "_test."
    | "rs" -> base'.EndsWith("_test.rs", StringComparison.Ordinal) || isInTestDir path
    | "fs"
    | "cs" ->
        isInTestDir path
        || base'.EndsWith("Steps.cs", StringComparison.Ordinal)
        || base'.EndsWith("Tests.cs", StringComparison.Ordinal)
        || base'.EndsWith("Steps.fs", StringComparison.Ordinal)
        || base'.EndsWith("Tests.fs", StringComparison.Ordinal)
    | "dart" -> base'.EndsWith("_test.dart", StringComparison.Ordinal) || isInTestDir path
    | _ -> false

/// Lists every test/step file under `appDir` whose base name matches `stem`.
let private findAllMatchingTestFiles (appDir: string) (stem: string) (excludeSourceDirs: string list) : string list =
    walkFiltered appDir (fun name -> isExcludedSourceDir name excludeSourceDirs)
    |> List.filter (fun p -> matchesStem (Path.GetFileName p) stem && isTestFile p)

/// Returns the first non-empty capture of groups 1 and 2.
let private altGroup (m: Match) : string =
    firstNonEmpty (m.Groups.[1].Value) (m.Groups.[2].Value)

/// Strips JS/TS comments, preserving string and template literals verbatim and
/// removing `// …` only when it starts a line, so an inline trailing comment
/// after real code survives.
let stripJsComments (src: string) : string =
    let chars = src.ToCharArray()
    let n = chars.Length
    let out = StringBuilder(src.Length)
    let mutable i = 0
    let mutable atLineStart = true

    while i < n do
        let c = chars.[i]

        if c = '\n' then
            out.Append '\n' |> ignore
            i <- i + 1
            atLineStart <- true
        elif c = '/' && i + 1 < n && chars.[i + 1] = '*' then
            let mutable j = i + 2

            while j + 1 < n && not (chars.[j] = '*' && chars.[j + 1] = '/') do
                if chars.[j] = '\n' then
                    out.Append '\n' |> ignore

                j <- j + 1

            i <- j + 2
        elif atLineStart && c = '/' && i + 1 < n && chars.[i + 1] = '/' then
            let mutable j = i + 2

            while j < n && chars.[j] <> '\n' do
                j <- j + 1

            i <- j
        elif c = '"' || c = '\'' || c = '`' then
            let quote = c
            out.Append c |> ignore
            i <- i + 1
            let mutable closed = false

            while not closed && i < n do
                if chars.[i] = '\\' && i + 1 < n then
                    out.Append(chars.[i]).Append(chars.[i + 1]) |> ignore
                    i <- i + 2
                else
                    out.Append(chars.[i]) |> ignore

                    if chars.[i] = quote then
                        i <- i + 1
                        closed <- true
                    else
                        i <- i + 1

            atLineStart <- false
        else
            out.Append c |> ignore

            if c <> ' ' && c <> '\t' then
                atLineStart <- false

            i <- i + 1

    out.ToString()

/// Extracts TypeScript/JavaScript step definitions: string-literal step calls
/// and `/regex/` step calls, after comment stripping.
let extractTsStepTexts (path: string) (sm: StepMatcher) : unit =
    let src = stripJsComments (File.ReadAllText path)

    for m in stepDefRe.Matches src do
        addStepToMatcher sm (unescapeSourceString (altGroup m)) path

    for m in tsRegexStepRe.Matches src do
        let pattern = m.Groups.[1].Value

        match tryRegex pattern with
        | Some re -> sm.AddPattern(re, pattern, path)
        | None -> ()

/// Extracts Rust `cucumber-rs` step definitions, most specific form first:
/// hash-delimited raw regex, bare raw regex, Cucumber expression, string
/// literal, hash-delimited raw literal.
let extractRustStepTexts (path: string) (sm: StepMatcher) : unit =
    let content = File.ReadAllText path

    for re' in [ rsStepRegexRe; rsStepRegexBareRe ] do
        for m in re'.Matches content do
            let pattern = m.Groups.[1].Value

            match tryRegex pattern with
            | Some re -> sm.AddPattern(re, pattern, path)
            | None -> ()

    for re' in [ rsStepExprRe; rsStepLiteralRe; rsStepLiteralRawRe ] do
        for m in re'.Matches content do
            addStepToMatcher sm (m.Groups.[1].Value) path

/// Extracts Dart step definitions from `s.given("…", …)`-style calls.
let extractDartStepTexts (path: string) (sm: StepMatcher) : unit =
    let content = File.ReadAllText path

    for m in dartStepRe.Matches content do
        addStepToMatcher sm (unescapeSourceString (altGroup m)) path

/// Extracts C# `SpecFlow` step attributes, verbatim strings first, collapsing
/// their `""` escape to a single quote.
let extractCsharpStepTexts (path: string) (sm: StepMatcher) : unit =
    let content = File.ReadAllText path

    for m in csVerbatimStepRe.Matches content do
        addStepToMatcher sm (m.Groups.[1].Value.Replace("\"\"", "\"")) path

    for m in csRegularStepRe.Matches content do
        addStepToMatcher sm (m.Groups.[1].Value) path

/// Registers an F# backtick-quoted step name as an anchored `^…$` pattern —
/// `TickSpec` treats backtick names as patterns.
let private addFsharpStepPattern (name: string) (path: string) (sm: StepMatcher) : unit =
    let pattern = sprintf "^%s$" (normalizeWs name)

    match tryRegex pattern with
    | Some re -> sm.AddPattern(re, pattern, path)
    | None -> ()

/// Extracts F# `TickSpec` step definitions in both layouts — attribute and
/// backtick name on one line, or the attribute on the line above — each in
/// module-level `let` and instance `member` form.
let extractFsharpStepTexts (path: string) (sm: StepMatcher) : unit =
    let mutable prevLineHasStepAttr = false

    for line in (File.ReadAllText path).Split('\n') do
        let thisLineHasStepAttr = fsStepAttrRe.IsMatch line

        if thisLineHasStepAttr then
            for m in fsStepRe.Matches line do
                addFsharpStepPattern (m.Groups.[1].Value) path sm

        if prevLineHasStepAttr && not thisLineHasStepAttr then
            for m in fsLetBacktickRe.Matches line do
                addFsharpStepPattern (m.Groups.[1].Value) path sm

        prevLineHasStepAttr <- thisLineHasStepAttr

/// Walks `appDir` and aggregates every recognised source file's step
/// definitions into one [`StepMatcher`].
let extractAllStepTexts (appDir: string) (excludeSourceDirs: string list) : StepMatcher =
    let sm = StepMatcher()

    for path in walkFiltered appDir (fun name -> isExcludedSourceDir name excludeSourceDirs) do
        match Path.GetExtension(path).TrimStart('.') with
        | "ts"
        | "tsx"
        | "js"
        | "jsx" -> extractTsStepTexts path sm
        | "rs" -> extractRustStepTexts path sm
        | "cs" -> extractCsharpStepTexts path sm
        | "fs" -> extractFsharpStepTexts path sm
        | "dart" -> extractDartStepTexts path sm
        | _ -> ()

    sm

/// Extracts `Scenario("…", …)` titles from a TypeScript/JavaScript test file,
/// scanning whole-file so a title wrapped onto the next physical line is still
/// recognised.
let private extractTsScenarioTitles (path: string) : Set<string> =
    let content = File.ReadAllText path

    scenarioDefRe.Matches content
    |> Seq.map (fun m -> normalizeWs (unescapeSourceString (altGroup m)))
    |> Set.ofSeq

/// Extracts titles declared by `// Scenario: Title` comment markers.
let private extractCommentScenarioTitles (path: string) : Set<string> =
    (File.ReadAllText path).Split('\n')
    |> Seq.choose (fun line ->
        let m = scenarioCommentRe.Match line

        if m.Success then
            Some(normalizeWs (m.Groups.[1].Value))
        else
            None)
    |> Set.ofSeq

/// Dispatches scenario-title extraction by file extension. F# is an auto-bind
/// framework (matching is implicit) and any unrecognised extension returns an
/// empty set rather than falling through to another language's parser.
let private extractScenarioTitles (path: string) : Set<string> =
    match Path.GetExtension(path).TrimStart('.') with
    | "cs"
    | "rs"
    | "dart" -> extractCommentScenarioTitles path
    | "ts"
    | "tsx"
    | "js"
    | "jsx" -> extractTsScenarioTitles path
    | _ -> Set.empty

/// `true` when `step` is covered: its primary text matches, or every expanded
/// outline variant matches.
let private stepCovered (sm: StepMatcher) (step: ParsedStep) : bool =
    if sm.Matches step.Text then true
    elif List.isEmpty step.Variants then false
    else step.Variants |> List.forall sm.Matches

/// Reports every step-definition entry matching no Gherkin step at all.
let checkOrphanStepImpls (sm: StepMatcher) (allGherkinSteps: string list) (repoRoot: string) : OrphanStepImpl list =
    if sm.IsEmpty then
        []
    else
        let normalized = allGherkinSteps |> List.map normalizeWs

        sm.Entries
        |> List.choose (fun e ->
            let matched =
                match e.Kind with
                | Exact -> normalized |> List.exists (fun gs -> gs = e.ExactText)
                | Pattern ->
                    e.Compiled
                    |> Option.map (fun re -> normalized |> List.exists re.IsMatch)
                    |> Option.defaultValue false

            if matched then
                None
            else
                Some
                    { File = relTo repoRoot e.File
                      MatcherKind =
                        (match e.Kind with
                         | Exact -> "exact"
                         | Pattern -> "pattern")
                      MatcherText =
                        (match e.Kind with
                         | Exact -> e.ExactText
                         | Pattern -> e.PatternText) })

/// Collects every `.feature` file from `opts`, falling back to `SpecsDir` when
/// `SpecsDirs` is empty.
let private collectFeatureFiles (opts: ScanOptions) : string list =
    let dirs =
        if not (List.isEmpty opts.SpecsDirs) then opts.SpecsDirs
        elif opts.SpecsDir <> "" then [ opts.SpecsDir ]
        else []

    dirs |> List.collect (fun d -> coverageWalkFeatureFiles d opts.ExcludeDirs)

/// Shared-step mode: every step definition is matched against every Gherkin
/// step, with no filename correspondence required.
let private checkSharedSteps (opts: ScanOptions) : CheckResult =
    let specFiles = collectFeatureFiles opts
    let allStepTexts = extractAllStepTexts opts.AppDir opts.ExcludeSourceDirs
    let stepGaps = ResizeArray<StepGap>()
    let allGherkinSteps = ResizeArray<string>()
    let mutable totalScenarios = 0
    let mutable totalSteps = 0

    for specFile in specFiles do
        let relSpec = relTo opts.RepoRoot specFile

        for sc in parseFeatureFile specFile do
            totalScenarios <- totalScenarios + 1

            for step in sc.Steps do
                totalSteps <- totalSteps + 1

                // `@wip` scenarios are fully exempt from step-coverage checking
                // (the rule the marker-existence engine applies too) — still
                // counted as physical inventory, never a gap, and never
                // matched against for orphan detection.
                if not sc.IsWip then
                    allGherkinSteps.Add step.Text
                    allGherkinSteps.AddRange step.Variants

                    if not (stepCovered allStepTexts step) then
                        stepGaps.Add
                            { SpecFile = relSpec
                              ScenarioTitle = sc.Title
                              StepKeyword = step.Keyword
                              StepText = step.Text }

    { TotalSpecs = List.length specFiles
      TotalScenarios = totalScenarios
      TotalSteps = totalSteps
      Gaps = []
      ScenarioGaps = []
      StepGaps = List.ofSeq stepGaps
      OrphanStepImpls = checkOrphanStepImpls allStepTexts (List.ofSeq allGherkinSteps) opts.RepoRoot }

/// 1-to-1 mode: every `.feature` file must have a stem-matching test file, and
/// each of its scenarios and steps must be covered there.
let private checkOneToOne (opts: ScanOptions) : CheckResult =
    let specFiles = collectFeatureFiles opts
    let allStepTexts = extractAllStepTexts opts.AppDir opts.ExcludeSourceDirs
    let gaps = ResizeArray<CoverageGap>()
    let scenarioGaps = ResizeArray<ScenarioGap>()
    let stepGaps = ResizeArray<StepGap>()
    let allGherkinSteps = ResizeArray<string>()
    let mutable totalScenarios = 0
    let mutable totalSteps = 0

    for specFile in specFiles do
        let stem = Path.GetFileNameWithoutExtension specFile
        let testFilePaths = findAllMatchingTestFiles opts.AppDir stem opts.ExcludeSourceDirs
        let relSpec = relTo opts.RepoRoot specFile
        let scenarios = parseFeatureFile specFile

        if List.isEmpty testFilePaths then
            gaps.Add { SpecFile = relSpec; Stem = stem }
            // Still harvest this file's step texts so the orphan check sees them.
            for sc in scenarios do
                for step in sc.Steps do
                    allGherkinSteps.Add step.Text
        else
            let scenarioTitles =
                testFilePaths |> List.map extractScenarioTitles |> Set.unionMany

            for sc in scenarios do
                totalScenarios <- totalScenarios + 1

                if not sc.IsWip && not (scenarioTitles.Contains(normalizeWs sc.Title)) then
                    scenarioGaps.Add
                        { SpecFile = relSpec
                          ScenarioTitle = sc.Title }

                for step in sc.Steps do
                    totalSteps <- totalSteps + 1

                    if not sc.IsWip then
                        allGherkinSteps.Add step.Text
                        allGherkinSteps.AddRange step.Variants

                        if not (stepCovered allStepTexts step) then
                            stepGaps.Add
                                { SpecFile = relSpec
                                  ScenarioTitle = sc.Title
                                  StepKeyword = step.Keyword
                                  StepText = step.Text }

    { TotalSpecs = List.length specFiles
      TotalScenarios = totalScenarios
      TotalSteps = totalSteps
      Gaps = List.ofSeq gaps
      ScenarioGaps = List.ofSeq scenarioGaps
      StepGaps = List.ofSeq stepGaps
      OrphanStepImpls = checkOrphanStepImpls allStepTexts (List.ofSeq allGherkinSteps) opts.RepoRoot }

/// Runs the spec-coverage scan described by `opts`, in shared-step or 1-to-1
/// mode.
let checkAll (opts: ScanOptions) : CheckResult =
    let effective =
        if List.isEmpty opts.SpecsDirs && opts.SpecsDir <> "" then
            { opts with
                SpecsDirs = [ opts.SpecsDir ] }
        else
            opts

    if effective.SharedSteps then
        checkSharedSteps effective
    else
        checkOneToOne effective

/// `true` when `r` records any gap of any kind.
let hasCoverageGaps (r: CheckResult) : bool =
    not (
        List.isEmpty r.Gaps
        && List.isEmpty r.ScenarioGaps
        && List.isEmpty r.StepGaps
        && List.isEmpty r.OrphanStepImpls
    )

/// Renders `r` as human-readable text. With `quiet` and no gaps the result is
/// empty; otherwise a success banner or the structured gap report.
let formatCoverageText (r: CheckResult) (quiet: bool) : string =
    if not (hasCoverageGaps r) then
        if quiet then
            ""
        else
            sprintf
                "Spec coverage valid! %d specs, %d scenarios, %d steps — all covered.\n"
                r.TotalSpecs
                r.TotalScenarios
                r.TotalSteps
    else
        let out = StringBuilder()
        out.Append "Spec coverage gaps found!\n\n" |> ignore

        if not (List.isEmpty r.Gaps) then
            out.Append(sprintf "Missing test files (%d):\n" (List.length r.Gaps)) |> ignore

            for gap in r.Gaps do
                out.Append(sprintf "  - %s\n    (expected test file with stem: %s)\n" gap.SpecFile gap.Stem)
                |> ignore

        if not (List.isEmpty r.ScenarioGaps) then
            if not (List.isEmpty r.Gaps) then
                out.Append '\n' |> ignore

            out.Append(sprintf "Missing scenarios (%d):\n" (List.length r.ScenarioGaps))
            |> ignore

            for sg in r.ScenarioGaps do
                out.Append(sprintf "  - %s\n    → Scenario: \"%s\"\n" sg.SpecFile sg.ScenarioTitle)
                |> ignore

        if not (List.isEmpty r.StepGaps) then
            if not (List.isEmpty r.Gaps) || not (List.isEmpty r.ScenarioGaps) then
                out.Append '\n' |> ignore

            out.Append(sprintf "Missing steps (%d):\n" (List.length r.StepGaps)) |> ignore

            // Group by (spec file, scenario title), preserving first-seen order.
            let order = ResizeArray<string * string>()

            for sg in r.StepGaps do
                let k = (sg.SpecFile, sg.ScenarioTitle)

                if not (order.Contains k) then
                    order.Add k

            for (specFile, title) in order do
                out.Append(sprintf "  - %s\n    → Scenario: \"%s\"\n" specFile title) |> ignore

                for sg in r.StepGaps do
                    if sg.SpecFile = specFile && sg.ScenarioTitle = title then
                        out.Append(sprintf "      · %s %s\n" sg.StepKeyword sg.StepText) |> ignore

        if not (List.isEmpty r.OrphanStepImpls) then
            if
                not (List.isEmpty r.Gaps)
                || not (List.isEmpty r.ScenarioGaps)
                || not (List.isEmpty r.StepGaps)
            then
                out.Append '\n' |> ignore

            out.Append(
                sprintf "Orphan step implementations (%d) — no Gherkin step matches:\n" (List.length r.OrphanStepImpls)
            )
            |> ignore

            for o in r.OrphanStepImpls do
                out.Append(sprintf "  - %s\n      [%s] %s\n" o.File o.MatcherKind o.MatcherText)
                |> ignore

        out.ToString()

/// Execution status of one scenario in a tier's machine-readable run report.
type RunStatus =
    | Passed
    | Failed
    | Skipped

/// One scenario execution result. Each test-runner ecosystem normalises its
/// native report into this flat shape before the cross-check reads it.
type RunReportEntry =
    { FeaturePath: string
      ScenarioTitle: string
      Status: RunStatus }

/// A `@covers` marker whose covering test did not execute-and-pass at its
/// declared level — the gap neither the step-text scan nor the
/// marker-existence engine can see, since both only prove an implementation
/// exists, never that it ran.
type RuntimeCoverageViolation =
    /// No run-report entry names this marker's scenario.
    | NotExecuted of sourceFile: string * featurePath: string * scenarioTitle: string * level: TestLevel
    /// A run-report entry exists but did not pass.
    | RunFailed of sourceFile: string * featurePath: string * scenarioTitle: string * level: TestLevel

/// Renders a [`TestLevel`] as the lowercase name used in diagnostics and in
/// `--<level>-report` flags.
let testLevelName (level: TestLevel) : string =
    match level with
    | Unit -> "unit"
    | Integration -> "integration"
    | E2e -> "e2e"

/// Parses a run report: a flat JSON array of
/// `{feature_path, scenario_title, status}` objects.
let parseRunReport (json: string) : Result<RunReportEntry list, string> =
    try
        match JsonNode.Parse json with
        | :? JsonArray as arr ->
            arr
            |> Seq.map (fun node ->
                let o = node.AsObject()
                let str (key: string) = o.[key].GetValue<string>()

                { FeaturePath = str "feature_path"
                  ScenarioTitle = str "scenario_title"
                  Status =
                    match str "status" with
                    | "passed" -> Passed
                    | "failed" -> Failed
                    | "skipped" -> Skipped
                    | other -> failwithf "unknown run status: %s" other })
            |> List.ofSeq
            |> Ok
        | _ -> Error "run report must be a JSON array"
    with ex ->
        Error ex.Message

/// Cross-checks one marker against `report`: a missing entry is
/// [`NotExecuted`], a present but non-passing entry is [`RunFailed`].
let private checkMarker (marker: CoversMarker) (report: RunReportEntry list) : RuntimeCoverageViolation option =
    let entry =
        report
        |> List.tryFind (fun e -> e.FeaturePath = marker.FeaturePath && e.ScenarioTitle = marker.ScenarioTitle)

    match entry with
    | None -> Some(NotExecuted(marker.SourceFile, marker.FeaturePath, marker.ScenarioTitle, marker.Level))
    | Some e when e.Status <> Passed ->
        Some(RunFailed(marker.SourceFile, marker.FeaturePath, marker.ScenarioTitle, marker.Level))
    | Some _ -> None

/// Runs the runtime cross-check for one tier's markers against its run report.
let checkRuntime (markers: CoversMarker list) (report: RunReportEntry list) : RuntimeCoverageViolation list =
    if List.isEmpty markers then
        []
    else
        markers |> List.choose (fun m -> checkMarker m report)

/// Renders runtime cross-check violations as a detailed listing; empty when
/// there are none.
let formatRuntimeViolations (violations: RuntimeCoverageViolation list) : string =
    if List.isEmpty violations then
        ""
    else
        let out = StringBuilder()

        out.Append(sprintf "\nRuntime cross-check violations (%d):\n" (List.length violations))
        |> ignore

        for v in violations do
            let sourceFile, featurePath, scenarioTitle, level, verdict =
                match v with
                | NotExecuted(s, f, t, l) -> s, f, t, l, "marked-but-not-executed"
                | RunFailed(s, f, t, l) -> s, f, t, l, "marked-but-failed"

            out.Append(
                sprintf
                    "  - %s\n    → Scenario: \"%s\" [%s] %s (marker: %s)\n"
                    featurePath
                    scenarioTitle
                    (testLevelName level)
                    verdict
                    sourceFile
            )
            |> ignore

        out.ToString()
