/// Plain xunit tests calling `RhinoCli.Application.Specs`'s public helper
/// functions directly with synthetic strings/records — no CLI dispatch, no
/// subprocess. `SpecsSteps.fs`'s Gherkin scenarios exercise the
/// spec-coverage/behavior-coverage engine end-to-end but drive it through a
/// subprocess spawning the compiled CLI, which is invisible to coverlet; the
/// small string-transform/regex helpers this file targets (Cucumber
/// expression compilation, JS/TS source unescaping, comment stripping,
/// per-language step-text extraction, coverage-report rendering) have no
/// other in-process caller anywhere in the test suite. See `learnings.md`,
/// 2026-08-30.
module RhinoCli.Tests.Unit.Steps.WaveEFApplicationUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Application

let private newTempDir () =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-waveef-app-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private writeFile (root: string) (relativePath: string) (content: string) =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName full) |> ignore
    File.WriteAllText(full, content)

// ---------------------------------------------------------------------------
// unescapeJsString / capturedTitle — via the public scanAllRenderedTitles,
// their only call site
// ---------------------------------------------------------------------------

[<Fact>]
let ``scanAllRenderedTitles decodes every JS escape sequence in a rendered title`` () =
    let specJs =
        "test('plain title', () => {});\n"
        + "test('has a \\ttab and \\r\\n breaks', () => {});\n"
        + "test('unicode \\u0041 letter', () => {});\n"
        + "test('malformed \\uZZ12 escape', () => {});\n"
        + "test('truncated \\u12', () => {});\n"
        + "test('lone surrogate \\uD800 here', () => {});\n"
        + "test('other escape \\q passthrough', () => {});\n"

    let titles = Specs.scanAllRenderedTitles specJs

    Assert.Contains("plain title", titles)
    Assert.Contains("has a \ttab and \r\n breaks", titles)
    Assert.Contains("unicode A letter", titles)
    Assert.Contains("malformed \\uZZ12 escape", titles)
    Assert.Contains("truncated \\u12", titles)
    Assert.Contains("lone surrogate \\uD800 here", titles)
    Assert.Contains("other escape q passthrough", titles)

// ---------------------------------------------------------------------------
// unescapeSourceString — every JS/TS escape branch plus the passthrough arm
// ---------------------------------------------------------------------------

[<Fact>]
let ``unescapeSourceString decodes every recognised escape and passes through the rest`` () =
    let decoded = Specs.unescapeSourceString "a\\'b\\\"c\\\\d\\/e\\nf\\tg\\rh\\zi"

    Assert.Equal("a'b\"c\\d/e\nf\tg\rh zi".Replace(" z", "z"), decoded)

[<Fact>]
let ``unescapeSourceString leaves a trailing backslash untouched`` () =
    Assert.Equal("abc\\", Specs.unescapeSourceString "abc\\")

// ---------------------------------------------------------------------------
// Cucumber expression compilation: findNextParam (via hasCucumberExpressions
// and cucumberExprToRegex), unescapeCucumberExpr, cucumberParamToRegex,
// cucumberExprToRegex, tryRegex (via addStepToMatcher)
// ---------------------------------------------------------------------------

[<Fact>]
let ``hasCucumberExpressions is false for plain text and true for a placeholder`` () =
    Assert.False(Specs.hasCucumberExpressions "plain text with no braces")
    Assert.True(Specs.hasCucumberExpressions "I have {int} cukes")

[<Fact>]
let ``hasCucumberExpressions treats an unclosed brace as no placeholder`` () =
    Assert.False(Specs.hasCucumberExpressions "I have {int cukes with no close")

[<Fact>]
let ``hasCucumberExpressions skips a backslash-escaped brace`` () =
    Assert.False(Specs.hasCucumberExpressions "literal \\{ not a param")

[<Fact>]
let ``unescapeCucumberExpr decodes a backslash-escaped character`` () =
    Assert.Equal("a{b}c", Specs.unescapeCucumberExpr "a\\{b\\}c")

[<Fact>]
let ``cucumberParamToRegex maps every known type and falls back for unknown types`` () =
    Assert.Equal("\"[^\"]*\"", Specs.cucumberParamToRegex "string")
    Assert.Equal(@"-?\d+", Specs.cucumberParamToRegex "int")
    Assert.Equal(@"-?\d+", Specs.cucumberParamToRegex "byte")
    Assert.Equal(@"-?\d+", Specs.cucumberParamToRegex "short")
    Assert.Equal(@"-?\d+", Specs.cucumberParamToRegex "long")
    Assert.Equal(@"-?\d+\.?\d*", Specs.cucumberParamToRegex "float")
    Assert.Equal(@"-?\d+\.?\d*", Specs.cucumberParamToRegex "double")
    Assert.Equal(@"-?\d+\.?\d*", Specs.cucumberParamToRegex "bigdecimal")
    Assert.Equal(@"\S+", Specs.cucumberParamToRegex "word")
    Assert.Equal(".+", Specs.cucumberParamToRegex "anything-else")

[<Fact>]
let ``cucumberExprToRegex compiles a placeholder into an anchored-ready fragment`` () =
    let pattern = Specs.cucumberExprToRegex "I have {int} cukes"
    let re = Text.RegularExpressions.Regex(sprintf "^%s$" pattern)
    Assert.True(re.IsMatch "I have 42 cukes")
    Assert.False(re.IsMatch "I have many cukes")

[<Fact>]
let ``cucumberExprToRegex with no placeholder escapes the literal text`` () =
    let pattern = Specs.cucumberExprToRegex "a.b*c"
    Assert.Equal(Text.RegularExpressions.Regex.Escape "a.b*c", pattern)

// ---------------------------------------------------------------------------
// addStepToMatcher / StepMatcher — the three registration branches plus
// tryRegex's failure arm
// ---------------------------------------------------------------------------

[<Fact>]
let ``addStepToMatcher registers a leading-caret text as a compiled pattern`` () =
    let sm = Specs.StepMatcher()
    Specs.addStepToMatcher sm "^a step with (\\d+) items$" "file-a"
    Assert.True(sm.Matches "a step with 5 items")
    Assert.False(sm.Matches "a step with five items")

[<Fact>]
let ``addStepToMatcher drops an uncompilable leading-caret pattern`` () =
    let sm = Specs.StepMatcher()
    Specs.addStepToMatcher sm "^(unclosed group" "file-b"
    Assert.True sm.IsEmpty

[<Fact>]
let ``addStepToMatcher registers a cucumber-expression text as a compiled pattern`` () =
    let sm = Specs.StepMatcher()
    Specs.addStepToMatcher sm "I have {int} cukes" "file-c"
    Assert.True(sm.Matches "I have 7 cukes")

[<Fact>]
let ``addStepToMatcher registers plain text as an exact entry`` () =
    let sm = Specs.StepMatcher()
    Specs.addStepToMatcher sm "a plain literal step" "file-d"
    Assert.True(sm.Matches "a plain literal step")
    Assert.False(sm.Matches "a plain literal step extra")

[<Fact>]
let ``addStepToMatcher ignores blank text`` () =
    let sm = Specs.StepMatcher()
    Specs.addStepToMatcher sm "   " "file-e"
    Assert.True sm.IsEmpty

// ---------------------------------------------------------------------------
// stripJsComments — line comments, block comments (with embedded newlines),
// string/template literals (with an escaped delimiter), and content that
// merely resembles a comment inside a string
// ---------------------------------------------------------------------------

[<Fact>]
let ``stripJsComments strips full-line and block comments while preserving strings verbatim`` () =
    let src =
        "// a full line comment\n"
        + "const a = 1; // trailing comment is not a full-line comment\n"
        + "/* a block\n   comment spanning lines */\n"
        + "const s = \"http://not-a-comment\";\n"
        + "const t = 'has \\' an escaped quote';\n"

    let stripped = Specs.stripJsComments src

    Assert.DoesNotContain("a full line comment", stripped)
    Assert.DoesNotContain("a block", stripped)
    Assert.Contains("const a = 1; // trailing comment is not a full-line comment", stripped)
    Assert.Contains("\"http://not-a-comment\"", stripped)
    Assert.Contains("'has \\' an escaped quote'", stripped)

// ---------------------------------------------------------------------------
// extractAllStepTexts — one real fixture file per supported language,
// exercising every extract*StepTexts function plus addFsharpStepPattern
// ---------------------------------------------------------------------------

[<Fact>]
let ``extractAllStepTexts collects step definitions from every supported language`` () =
    let root = newTempDir ()

    writeFile
        root
        "app/steps.ts"
        ("Given('a plain ts step', () => {});\n"
         + "When(/^a ts regex step (\\d+)$/, () => {});\n")

    writeFile
        root
        "app/steps.rs"
        ("#[given(\"a rust literal step\")]\n"
         + "#[given(regex = r#\"^a rust regex step$\"#)]\n"
         + "#[given(regex = r\"^a rust bare regex step$\")]\n"
         + "#[given(expr = \"a rust cucumber {int} step\")]\n")

    writeFile
        root
        "app/steps.dart"
        ("s.given('a dart given step', (context) {});\n"
         + "scenario.when(\"a dart when step\", (context) {});\n")

    writeFile root "app/Steps.cs" ("[Given(@\"a csharp verbatim step\")]\n" + "[When(\"a csharp regular step\")]\n")

    // Built from fragments, never spelling out a literal `[<Given>]`/`[<When>]`
    // step attribute in this file's own source — this file lives under
    // `apps/rhino-cli/src/tests/unit/Steps/`, which the real
    // `specs behavior-coverage validate` smoke test (elsewhere in this suite)
    // scans as genuine F# step-definition source; a literal attribute here
    // would register as a bogus/orphan step against this repo's own specs.
    let stepAttr (name: string) = "[" + "<" + name + ">" + "]"
    let backtickQuoted (text: string) = "``" + text + "``"

    writeFile
        root
        "app/Steps.fs"
        (sprintf "let %s %s () = ()\n" (stepAttr "Given") (backtickQuoted "a fsharp let step")
         + stepAttr "When"
         + "\n"
         + sprintf "member _.%s() = ()\n" (backtickQuoted "a fsharp member step"))

    let sm = Specs.extractAllStepTexts root []

    Assert.True(sm.Matches "a plain ts step")
    Assert.True(sm.Matches "a ts regex step 9")
    Assert.True(sm.Matches "a rust literal step")
    Assert.True(sm.Matches "a rust regex step")
    Assert.True(sm.Matches "a rust bare regex step")
    Assert.True(sm.Matches "a rust cucumber 3 step")
    Assert.True(sm.Matches "a dart given step")
    Assert.True(sm.Matches "a dart when step")
    Assert.True(sm.Matches "a csharp verbatim step")
    Assert.True(sm.Matches "a csharp regular step")
    Assert.True(sm.Matches "a fsharp let step")
    Assert.True(sm.Matches "a fsharp member step")

// ---------------------------------------------------------------------------
// formatCoverageText — the quiet/success/empty branches plus every populated
// gap-section branch, including the step-gap grouping loop
// ---------------------------------------------------------------------------

let private emptyCoverageResult: Specs.CheckResult =
    { TotalSpecs = 1
      TotalScenarios = 1
      TotalSteps = 1
      Gaps = []
      ScenarioGaps = []
      StepGaps = []
      OrphanStepImpls = [] }

let private populatedCoverageResult: Specs.CheckResult =
    { TotalSpecs = 2
      TotalScenarios = 3
      TotalSteps = 5
      Gaps =
        [ { Specs.CoverageGap.SpecFile = "specs/a.feature"
            Stem = "a" } ]
      ScenarioGaps =
        [ { Specs.ScenarioGap.SpecFile = "specs/b.feature"
            ScenarioTitle = "B scenario" } ]
      StepGaps =
        [ { Specs.StepGap.SpecFile = "specs/c.feature"
            ScenarioTitle = "C scenario"
            StepKeyword = "Given"
            StepText = "a precondition" }
          { Specs.StepGap.SpecFile = "specs/c.feature"
            ScenarioTitle = "C scenario"
            StepKeyword = "When"
            StepText = "an action" } ]
      OrphanStepImpls =
        [ { Specs.OrphanStepImpl.File = "steps/orphan.ts"
            MatcherKind = "exact"
            MatcherText = "an orphan step" } ] }

[<Fact>]
let ``formatCoverageText renders an empty string in quiet mode with no gaps`` () =
    Assert.Equal("", Specs.formatCoverageText emptyCoverageResult true)

[<Fact>]
let ``formatCoverageText renders a success banner in non-quiet mode with no gaps`` () =
    let text = Specs.formatCoverageText emptyCoverageResult false
    Assert.Contains("Spec coverage valid!", text)

[<Fact>]
let ``formatCoverageText renders every gap section when all four are populated`` () =
    let text = Specs.formatCoverageText populatedCoverageResult false

    Assert.Contains("Missing test files (1):", text)
    Assert.Contains("specs/a.feature", text)
    Assert.Contains("Missing scenarios (1):", text)
    Assert.Contains("B scenario", text)
    Assert.Contains("Missing steps (2):", text)
    Assert.Contains("Given a precondition", text)
    Assert.Contains("When an action", text)
    Assert.Contains("Orphan step implementations (1)", text)
    Assert.Contains("steps/orphan.ts", text)

// ---------------------------------------------------------------------------
// parseRunReport / checkRuntime — every status branch, the malformed-input
// arms, and the empty-markers short-circuit
// ---------------------------------------------------------------------------

[<Fact>]
let ``parseRunReport decodes passed, failed, and skipped statuses`` () =
    let json =
        """[{"feature_path":"a.feature","scenario_title":"A","status":"passed"},
            {"feature_path":"b.feature","scenario_title":"B","status":"failed"},
            {"feature_path":"c.feature","scenario_title":"C","status":"skipped"}]"""

    match Specs.parseRunReport json with
    | Ok entries ->
        Assert.Equal(3, List.length entries)
        Assert.Equal(Specs.Passed, entries.[0].Status)
        Assert.Equal(Specs.Failed, entries.[1].Status)
        Assert.Equal(Specs.Skipped, entries.[2].Status)
    | Error e -> failwithf "expected Ok, got Error %s" e

[<Fact>]
let ``parseRunReport reports an error for a non-array JSON document`` () =
    match Specs.parseRunReport """{"not": "an array"}""" with
    | Ok _ -> failwith "expected an Error"
    | Error e -> Assert.Contains("must be a JSON array", e)

[<Fact>]
let ``parseRunReport reports an error for an unknown status value`` () =
    match Specs.parseRunReport """[{"feature_path":"a.feature","scenario_title":"A","status":"pending"}]""" with
    | Ok _ -> failwith "expected an Error"
    | Error e -> Assert.Contains("unknown run status", e)

[<Fact>]
let ``parseRunReport reports an error for malformed JSON`` () =
    match Specs.parseRunReport "not json at all" with
    | Ok _ -> failwith "expected an Error"
    | Error _ -> ()

[<Fact>]
let ``checkRuntime short-circuits to an empty list when there are no markers`` () =
    Assert.Empty(Specs.checkRuntime [] [])

// ---------------------------------------------------------------------------
// auditGherkinKeywordCardinality — the empty-paths guard and the sort
// comparator's line/keyword tie-break branches
// ---------------------------------------------------------------------------

[<Fact>]
let ``auditGherkinKeywordCardinality requires at least one path`` () =
    match Specs.auditGherkinKeywordCardinality [] with
    | Ok _ -> failwith "expected an Error"
    | Error e -> Assert.Contains("at least one path is required", e)

[<Fact>]
let ``auditGherkinKeywordCardinality sorts findings by file, then line, then keyword`` () =
    let root = newTempDir ()

    writeFile
        root
        "specs/dup.feature"
        ("Feature: Dup\n"
         + "  Scenario: Repeats two keywords\n"
         + "    Given a precondition\n"
         + "    Given another precondition\n"
         + "    When an action\n"
         + "    When another action\n")

    match Specs.auditGherkinKeywordCardinality [ root ] with
    | Error e -> failwithf "expected Ok, got Error %s" e
    | Ok findings ->
        Assert.Equal(2, List.length findings)
        Assert.Equal("Given", findings.[0].Keyword)
        Assert.Equal("When", findings.[1].Keyword)

// ---------------------------------------------------------------------------
// formatGapText / formatGapMarkdown — the passed/failed banner and the
// new-gaps/stale-entries sections
// ---------------------------------------------------------------------------

let private cleanGapReport: Specs.GapReport =
    { NewGaps = []
      Stale = []
      Failed = false }

let private populatedGapReport: Specs.GapReport =
    { NewGaps =
        [ { Specs.Feature = "specs/a.feature"
            Scenario = "New scenario" } ]
      Stale =
        [ { Specs.Feature = "specs/b.feature"
            Scenario = "Old scenario" } ]
      Failed = true }

[<Fact>]
let ``formatGapText renders a passed banner when there are no new gaps`` () =
    let text = Specs.formatGapText cleanGapReport
    Assert.Contains("PASSED", text)
    Assert.Contains("0 new unbound scenario(s) beyond baseline", text)

[<Fact>]
let ``formatGapText renders new gaps and stale entries when both are present`` () =
    let text = Specs.formatGapText populatedGapReport
    Assert.Contains("FAILED", text)
    Assert.Contains("New scenario", text)
    Assert.Contains("stale baseline entries can be pruned", text)
    Assert.Contains("Old scenario", text)

[<Fact>]
let ``formatGapMarkdown renders new gaps and stale entries when both are present`` () =
    let markdown = Specs.formatGapMarkdown populatedGapReport
    Assert.Contains("| Feature | Scenario |", markdown)
    Assert.Contains("New scenario", markdown)
    Assert.Contains("Stale baseline entries", markdown)
    Assert.Contains("Old scenario", markdown)

// ---------------------------------------------------------------------------
// checkOrphanStepImpls — the empty-matcher short-circuit and a populated
// matcher with one matched exact entry and one unmatched pattern entry
// ---------------------------------------------------------------------------

[<Fact>]
let ``checkOrphanStepImpls returns an empty list for an empty matcher`` () =
    Assert.Empty(Specs.checkOrphanStepImpls (Specs.StepMatcher()) [ "anything" ] "/repo")

[<Fact>]
let ``checkOrphanStepImpls reports only the entry matching no Gherkin step`` () =
    let root = newTempDir ()
    let sm = Specs.StepMatcher()
    Specs.addStepToMatcher sm "a matched step" (Path.Combine(root, "steps/a.ts"))
    Specs.addStepToMatcher sm "^an unrelated (\\d+) step$" (Path.Combine(root, "steps/b.ts"))

    let orphans = Specs.checkOrphanStepImpls sm [ "a matched step" ] root

    Assert.Equal(1, List.length orphans)
    Assert.Equal("pattern", orphans.[0].MatcherKind)
    Assert.Contains("steps", orphans.[0].File)
