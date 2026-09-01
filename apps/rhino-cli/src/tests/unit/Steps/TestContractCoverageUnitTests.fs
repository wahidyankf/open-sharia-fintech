/// Contract cases for the 99% native-coverage validator. Every case pins one
/// clause of
/// [Target Contract and Project Matrix](../../../../../../plans/in-progress/adopt-beavernest-test-automation/tech-docs/target-contract-and-project-matrix.md):
/// a parse rule, one of the nine fixtures, or an exact expected/actual pair.
/// The fixtures under `Fixtures/TestContract/Coverage` are copied beside the
/// test assembly by `RhinoCli.UnitTests.fsproj`.
module RhinoCli.Tests.Unit.Steps.TestContractCoverageUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Application

// ---------------------------------------------------------------------------
// Fixture access
// ---------------------------------------------------------------------------

let private fixtureFile (name: string) : string =
    Path.Combine(AppContext.BaseDirectory, "Fixtures", "TestContract", "Coverage", name + ".json")

let private fixtureText (name: string) : string =
    let path = fixtureFile name
    Assert.True(File.Exists path, "missing fixture " + path)
    File.ReadAllText path

let private parsed (name: string) : TestContractCoverage.CoverageDocument =
    match TestContractCoverage.parseDocument (fixtureText name) with
    | Ok document -> document
    | Error(TestContract.Misuse message) -> failwith ("fixture " + name + " rejected as misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("fixture " + name + " rejected: " + message)

/// Validates a fixture that must fail, returning the joined diagnostic text.
let private rejected (name: string) : string =
    match TestContractCoverage.validateDocument (parsed name) with
    | Error(TestContract.ContractFailure message) -> message
    | Error(TestContract.Misuse message) ->
        failwith ("fixture " + name + " was misuse, not a contract failure: " + message)
    | Ok _ -> failwith ("fixture " + name + " passed; it must fail")

/// Validates a fixture that must pass, returning its report.
let private accepted (name: string) : TestContractCoverage.CoverageReport =
    match TestContractCoverage.validateDocument (parsed name) with
    | Ok report -> report
    | Error(TestContract.Misuse message) -> failwith ("fixture " + name + " rejected as misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("fixture " + name + " failed; it must pass: " + message)

let private negativeFixtures =
    [ "98-percent"
      "broad-exclusion"
      "conflicting-threshold"
      "echo-placeholder"
      "lower-threshold"
      "missing-threshold"
      "omitted-slice"
      "overlapping-output" ]

// ---------------------------------------------------------------------------
// Inline document construction
// ---------------------------------------------------------------------------

let private nativeCommand =
    "dotnet test widget-app.Tests --collect:\\\"XPlat Code Coverage\\\""

let private thresholdJson (source: string) (value: int) : string =
    sprintf "{\"source\":\"%s\",\"value\":%d}" source value

let private sliceJson (path: string) (applicable: bool) (measured: bool) (covered: int) (total: int) (output: string) =
    sprintf
        "{\"path\":\"%s\",\"applicable\":%s,\"measured\":%s,\"covered\":%d,\"total\":%d,\"output\":\"%s\"}"
        path
        (if applicable then "true" else "false")
        (if measured then "true" else "false")
        covered
        total
        output

let private documentJson
    (adapter: string)
    (profile: string)
    (reason: string)
    (thresholds: string list)
    (command: string)
    (exclusions: string list)
    (slices: string list)
    : string =
    sprintf
        "{\"schema\":\"%s\",\"case\":\"inline\",\"project\":\"widget-app\",\"owner\":\"widget-app\",\"adapter\":\"%s\",\"profile\":\"%s\",\"reason\":%s,\"thresholds\":[%s],\"target\":{\"name\":\"test:unit\",\"command\":\"%s\"},\"exclusions\":[%s],\"slices\":[%s]}"
        TestContractCoverage.SchemaVersion
        adapter
        profile
        reason
        (String.concat "," thresholds)
        command
        (exclusions
         |> List.map (fun value -> sprintf "\"%s\"" value)
         |> String.concat ",")
        (String.concat "," slices)

let private standardThreshold = thresholdJson "project.json:coverage.lines" 99

let private fullSlice =
    sliceJson "src/widget/core.fs" true true 100 100 "coverage/unit/core"

let private validDocumentJson =
    documentJson "unit" "measured" "null" [ standardThreshold ] nativeCommand [] [ fullSlice ]

let private parseInline (text: string) : Result<TestContractCoverage.CoverageDocument, TestContract.Failure> =
    TestContractCoverage.parseDocument text

let private misuseMessage (text: string) : string =
    match parseInline text with
    | Error(TestContract.Misuse message) -> message
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, got contract failure: " + message)
    | Ok _ -> failwith "expected misuse; the document parsed"

let private parseOk (text: string) : TestContractCoverage.CoverageDocument =
    match parseInline text with
    | Ok document -> document
    | Error(TestContract.Misuse message) -> failwith ("unexpected misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("unexpected contract failure: " + message)

let private validateInline (text: string) : Result<TestContractCoverage.CoverageReport, TestContract.Failure> =
    TestContractCoverage.validateDocument (parseOk text)

// ---------------------------------------------------------------------------
// Schema and identity parse rules
// ---------------------------------------------------------------------------

[<Fact>]
let ``the fixture schema string is pinned`` () =
    Assert.Equal("ose-test-contract-coverage-fixture/v1", TestContractCoverage.SchemaVersion)

[<Fact>]
let ``the native floor is pinned at 99`` () =
    Assert.Equal(99, TestContractCoverage.Floor)

[<Fact>]
let ``the fixture root is pinned`` () =
    Assert.Equal("apps/rhino-cli/src/tests/unit/Fixtures/TestContract/Coverage", TestContractCoverage.FixtureRoot)

[<Fact>]
let ``malformed JSON is misuse`` () =
    Assert.False(String.IsNullOrWhiteSpace(misuseMessage "{"))

[<Fact>]
let ``a wrong schema string is misuse`` () =
    let text =
        validDocumentJson.Replace(TestContractCoverage.SchemaVersion, "ose-test-contract-coverage-fixture/v2")

    Assert.Contains("schema", misuseMessage text)

[<Fact>]
let ``an unknown key is rejected`` () =
    let text = validDocumentJson.Replace("\"case\":", "\"extra\":1,\"case\":")
    Assert.Contains("extra", misuseMessage text)

[<Fact>]
let ``a blank project is misuse`` () =
    let text =
        validDocumentJson.Replace("\"project\":\"widget-app\"", "\"project\":\"\"")

    Assert.Contains("project", misuseMessage text)

[<Fact>]
let ``a blank owner is misuse`` () =
    let text = validDocumentJson.Replace("\"owner\":\"widget-app\"", "\"owner\":\"\"")
    Assert.Contains("owner", misuseMessage text)

[<Fact>]
let ``the three adapter levels parse`` () =
    let read (adapter: string) =
        (parseOk (documentJson adapter "measured" "null" [ standardThreshold ] nativeCommand [] [ fullSlice ])).Adapter

    Assert.Equal(TestContractCoverage.CoverageUnit, read "unit")
    Assert.Equal(TestContractCoverage.CoverageIntegration, read "integration")
    Assert.Equal(TestContractCoverage.CoverageE2e, read "e2e")

[<Fact>]
let ``an unknown adapter is misuse`` () =
    let text =
        documentJson "smoke" "measured" "null" [ standardThreshold ] nativeCommand [] [ fullSlice ]

    Assert.Contains("adapter", misuseMessage text)

[<Fact>]
let ``the two profiles parse`` () =
    Assert.Equal(TestContractCoverage.MeasuredProfile, (parseOk validDocumentJson).Profile)

    let governed =
        documentJson "e2e" "no-denominator" "\"no native denominator\"" [] "playwright test" [] []

    Assert.Equal(TestContractCoverage.NoDenominatorProfile, (parseOk governed).Profile)

[<Fact>]
let ``an unknown profile is misuse`` () =
    let text =
        documentJson "unit" "partial" "null" [ standardThreshold ] nativeCommand [] [ fullSlice ]

    Assert.Contains("profile", misuseMessage text)

[<Fact>]
let ``a no-denominator profile without a reason is misuse`` () =
    let text = documentJson "e2e" "no-denominator" "null" [] "playwright test" [] []
    Assert.Contains("reason", misuseMessage text)

[<Fact>]
let ``a measured profile carrying a reason is misuse`` () =
    let text =
        documentJson "unit" "measured" "\"not allowed here\"" [ standardThreshold ] nativeCommand [] [ fullSlice ]

    Assert.Contains("reason", misuseMessage text)

[<Fact>]
let ``a no-denominator profile declaring slices is misuse`` () =
    let text =
        documentJson "e2e" "no-denominator" "\"governed\"" [] "playwright test" [] [ fullSlice ]

    Assert.Contains("slices", misuseMessage text)

[<Fact>]
let ``a blank threshold source is misuse`` () =
    let text =
        documentJson "unit" "measured" "null" [ thresholdJson "" 99 ] nativeCommand [] [ fullSlice ]

    Assert.Contains("source", misuseMessage text)

[<Fact>]
let ``a negative threshold value is misuse`` () =
    let text =
        documentJson "unit" "measured" "null" [ thresholdJson "project.json" -1 ] nativeCommand [] [ fullSlice ]

    Assert.Contains("value", misuseMessage text)

[<Fact>]
let ``a threshold above 100 is misuse`` () =
    let text =
        documentJson "unit" "measured" "null" [ thresholdJson "project.json" 101 ] nativeCommand [] [ fullSlice ]

    Assert.Contains("value", misuseMessage text)

[<Fact>]
let ``a blank target command is misuse`` () =
    let text =
        documentJson "unit" "measured" "null" [ standardThreshold ] "" [] [ fullSlice ]

    Assert.Contains("command", misuseMessage text)

[<Fact>]
let ``a covered count above its total is misuse`` () =
    let text =
        documentJson
            "unit"
            "measured"
            "null"
            [ standardThreshold ]
            nativeCommand
            []
            [ sliceJson "src/widget/core.fs" true true 101 100 "coverage/unit/core" ]

    Assert.Contains("covered", misuseMessage text)

[<Fact>]
let ``a negative covered count is misuse`` () =
    let text =
        documentJson
            "unit"
            "measured"
            "null"
            [ standardThreshold ]
            nativeCommand
            []
            [ sliceJson "src/widget/core.fs" true true -1 100 "coverage/unit/core" ]

    Assert.Contains("covered", misuseMessage text)

[<Fact>]
let ``a duplicate slice path is misuse`` () =
    let text =
        documentJson "unit" "measured" "null" [ standardThreshold ] nativeCommand [] [ fullSlice; fullSlice ]

    Assert.Contains("src/widget/core.fs", misuseMessage text)

[<Fact>]
let ``an absolute slice path is misuse`` () =
    let text =
        documentJson
            "unit"
            "measured"
            "null"
            [ standardThreshold ]
            nativeCommand
            []
            [ sliceJson "/etc/passwd" true true 100 100 "coverage/unit/core" ]

    Assert.Contains("absolute", misuseMessage text)

[<Fact>]
let ``a traversal slice path is misuse`` () =
    let text =
        documentJson
            "unit"
            "measured"
            "null"
            [ standardThreshold ]
            nativeCommand
            []
            [ sliceJson "src/../../etc/passwd" true true 100 100 "coverage/unit/core" ]

    Assert.Contains("traversal", misuseMessage text)

[<Fact>]
let ``a measured profile with no slice at all is misuse`` () =
    let text =
        documentJson "unit" "measured" "null" [ standardThreshold ] nativeCommand [] []

    Assert.Contains("slices", misuseMessage text)

// ---------------------------------------------------------------------------
// Fixture resolution
// ---------------------------------------------------------------------------

[<Fact>]
let ``an absolute fixture path is misuse`` () =
    match TestContractCoverage.loadDocument "/repo" "/etc/passwd" with
    | Error(TestContract.Misuse message) -> Assert.Contains("absolute", message)
    | _ -> failwith "an absolute fixture path must be misuse"

[<Fact>]
let ``a traversal fixture path is misuse`` () =
    match TestContractCoverage.loadDocument "/repo" "../../etc/passwd" with
    | Error(TestContract.Misuse message) -> Assert.Contains("traversal", message)
    | _ -> failwith "a traversal fixture path must be misuse"

[<Fact>]
let ``a missing fixture file is misuse`` () =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-coverage-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory root |> ignore

    match TestContractCoverage.loadDocument root "absent.json" with
    | Error(TestContract.Misuse message) -> Assert.Contains("absent.json", message)
    | _ -> failwith "a missing fixture must be misuse"

// ---------------------------------------------------------------------------
// Every negative fixture
// ---------------------------------------------------------------------------

[<Fact>]
let ``every negative fixture parses and declares its own case`` () =
    for name in negativeFixtures do
        let document = parsed name
        Assert.False(String.IsNullOrWhiteSpace document.Case, name + " must declare a case")
        Assert.Equal("widget-app", document.Project)

[<Fact>]
let ``every negative fixture names project owner adapter item expected and actual`` () =
    for name in negativeFixtures do
        let message = rejected name
        Assert.Contains("project=widget-app", message)
        Assert.Contains("owner=widget-app", message)
        Assert.Contains("adapter=unit", message)
        Assert.Contains("item=", message)
        Assert.Contains("expected=99", message)
        Assert.Contains("actual=", message)
        Assert.Contains("remediation=", message)

[<Fact>]
let ``every negative fixture ends with the native summary line`` () =
    for name in negativeFixtures do
        let message = rejected name
        Assert.Contains("native-coverage-failed", message)
        Assert.Contains("floor=99", message)

[<Fact>]
let ``every negative fixture reports exactly one diagnostic code`` () =
    for name in negativeFixtures do
        let message = rejected name

        let codes =
            message.Split('\n')
            |> Array.filter (fun line -> line.StartsWith("coverage-", StringComparison.Ordinal))

        Assert.Equal(1, codes.Length)

[<Fact>]
let ``a 98 of 100 slice fails below the floor with its measured value`` () =
    let message = rejected "98-percent"
    Assert.Contains("coverage-below-floor", message)
    Assert.Contains("item=src/widget/core.fs", message)
    Assert.Contains("expected=99", message)
    Assert.Contains("actual=98", message)

[<Fact>]
let ``a declared threshold below the floor names its source and value`` () =
    let message = rejected "lower-threshold"
    Assert.Contains("coverage-threshold-below-floor", message)
    Assert.Contains("item=project.json:coverage.lines", message)
    Assert.Contains("actual=95", message)

[<Fact>]
let ``a measured adapter declaring no threshold is reported as missing`` () =
    let message = rejected "missing-threshold"
    Assert.Contains("coverage-threshold-missing", message)
    Assert.Contains("item=widget-app@unit", message)
    Assert.Contains("actual=0", message)

[<Fact>]
let ``two disagreeing thresholds are reported as a conflict with their count`` () =
    let message = rejected "conflicting-threshold"
    Assert.Contains("coverage-threshold-conflict", message)
    Assert.Contains("sources=2", message)
    Assert.Contains("actual=95", message)

[<Fact>]
let ``an echo placeholder target is not executable coverage`` () =
    let message = rejected "echo-placeholder"
    Assert.Contains("coverage-target-not-executable", message)
    Assert.Contains("item=test:unit", message)
    Assert.Contains("actual=0", message)

[<Fact>]
let ``an exclusion that empties the denominator is too broad`` () =
    let message = rejected "broad-exclusion"
    Assert.Contains("coverage-exclusion-too-broad", message)
    Assert.Contains("item=src/**", message)
    Assert.Contains("actual=0", message)

[<Fact>]
let ``an applicable slice left unmeasured is reported by path`` () =
    let message = rejected "omitted-slice"
    Assert.Contains("coverage-slice-omitted", message)
    Assert.Contains("item=src/widget/shell.fs", message)

[<Fact>]
let ``two slices sharing an output are reported as overlapping with their count`` () =
    let message = rejected "overlapping-output"
    Assert.Contains("coverage-output-overlap", message)
    Assert.Contains("item=coverage/unit/shared", message)
    Assert.Contains("candidates=2", message)

[<Fact>]
let ``the governed E2E-only fixture has no denominator and passes`` () =
    let report = accepted "e2e-no-denominator"
    Assert.Equal(TestContractCoverage.NoDenominatorProfile, report.Profile)
    Assert.Equal(TestContractCoverage.CoverageE2e, report.Adapter)
    Assert.Equal(0, report.Total)
    Assert.True(report.Reason.IsSome, "a governed no-denominator profile must carry its reason")

[<Fact>]
let ``the governed E2E-only fixture renders the no-denominator line`` () =
    let rendered = TestContractCoverage.formatReport (accepted "e2e-no-denominator")
    Assert.Contains("native-coverage-no-denominator", rendered)
    Assert.Contains("adapter=e2e", rendered)
    Assert.Contains("reason=", rendered)

// ---------------------------------------------------------------------------
// Exact arithmetic
// ---------------------------------------------------------------------------

[<Fact>]
let ``a fully covered slice set is valid`` () =
    match validateInline validDocumentJson with
    | Ok report ->
        Assert.Equal(100, report.Covered)
        Assert.Equal(100, report.Total)
    | Error(TestContract.Misuse message) -> failwith ("unexpected misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("a fully covered set must pass: " + message)

[<Fact>]
let ``exactly 99 of 100 meets the floor`` () =
    let text =
        documentJson
            "unit"
            "measured"
            "null"
            [ standardThreshold ]
            nativeCommand
            []
            [ sliceJson "src/widget/core.fs" true true 99 100 "coverage/unit/core" ]

    match validateInline text with
    | Ok report -> Assert.Equal(99, report.Covered)
    | Error(TestContract.ContractFailure message) -> failwith ("99 of 100 must pass: " + message)
    | Error(TestContract.Misuse message) -> failwith ("unexpected misuse: " + message)

[<Fact>]
let ``98 of 100 fails the floor`` () =
    let text =
        documentJson
            "unit"
            "measured"
            "null"
            [ standardThreshold ]
            nativeCommand
            []
            [ sliceJson "src/widget/core.fs" true true 98 100 "coverage/unit/core" ]

    match validateInline text with
    | Error(TestContract.ContractFailure message) -> Assert.Contains("coverage-below-floor", message)
    | _ -> failwith "98 of 100 must fail"

[<Fact>]
let ``989 of 1000 fails rather than rounding up to 99`` () =
    let text =
        documentJson
            "unit"
            "measured"
            "null"
            [ standardThreshold ]
            nativeCommand
            []
            [ sliceJson "src/widget/core.fs" true true 989 1000 "coverage/unit/core" ]

    match validateInline text with
    | Error(TestContract.ContractFailure message) ->
        Assert.Contains("coverage-below-floor", message)
        Assert.DoesNotContain("99%", message)
    | _ -> failwith "989 of 1000 must fail on integers"

[<Fact>]
let ``990 of 1000 meets the floor exactly`` () =
    let text =
        documentJson
            "unit"
            "measured"
            "null"
            [ standardThreshold ]
            nativeCommand
            []
            [ sliceJson "src/widget/core.fs" true true 990 1000 "coverage/unit/core" ]

    match validateInline text with
    | Ok report -> Assert.Equal(1000, report.Total)
    | Error(TestContract.ContractFailure message) -> failwith ("990 of 1000 must pass: " + message)
    | Error(TestContract.Misuse message) -> failwith ("unexpected misuse: " + message)

[<Fact>]
let ``the denominator sums every measured applicable slice`` () =
    let text =
        documentJson
            "unit"
            "measured"
            "null"
            [ standardThreshold ]
            nativeCommand
            []
            [ sliceJson "src/widget/core.fs" true true 100 100 "coverage/unit/core"
              sliceJson "src/widget/shell.fs" true true 100 100 "coverage/unit/shell" ]

    match validateInline text with
    | Ok report ->
        Assert.Equal(200, report.Covered)
        Assert.Equal(200, report.Total)
    | Error(TestContract.ContractFailure message) -> failwith ("two full slices must pass: " + message)
    | Error(TestContract.Misuse message) -> failwith ("unexpected misuse: " + message)

[<Fact>]
let ``an inapplicable slice is excluded from the denominator without a finding`` () =
    let text =
        documentJson
            "unit"
            "measured"
            "null"
            [ standardThreshold ]
            nativeCommand
            []
            [ sliceJson "src/widget/core.fs" true true 100 100 "coverage/unit/core"
              sliceJson "src/widget/generated.fs" false false 0 500 "coverage/unit/generated" ]

    match validateInline text with
    | Ok report -> Assert.Equal(100, report.Total)
    | Error(TestContract.ContractFailure message) -> failwith ("an inapplicable slice must not fail: " + message)
    | Error(TestContract.Misuse message) -> failwith ("unexpected misuse: " + message)

// ---------------------------------------------------------------------------
// Report rendering
// ---------------------------------------------------------------------------

[<Fact>]
let ``the success line names project owner adapter profile threshold and the pair`` () =
    match validateInline validDocumentJson with
    | Ok report ->
        let rendered = TestContractCoverage.formatReport report
        Assert.Contains("native-coverage-valid", rendered)
        Assert.Contains("project=widget-app", rendered)
        Assert.Contains("owner=widget-app", rendered)
        Assert.Contains("adapter=unit", rendered)
        Assert.Contains("profile=measured", rendered)
        Assert.Contains("threshold=99", rendered)
        Assert.Contains("covered=100/100", rendered)
        Assert.Contains("floor=99", rendered)
    | Error(TestContract.Misuse message) -> failwith ("unexpected misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("a valid document must pass: " + message)

[<Fact>]
let ``the success line never renders a percent sign`` () =
    match validateInline validDocumentJson with
    | Ok report -> Assert.DoesNotContain("%", TestContractCoverage.formatReport report)
    | Error(TestContract.Misuse message) -> failwith ("unexpected misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("a valid document must pass: " + message)

[<Fact>]
let ``adapter names round-trip`` () =
    Assert.Equal("unit", TestContractCoverage.adapterName TestContractCoverage.CoverageUnit)
    Assert.Equal("integration", TestContractCoverage.adapterName TestContractCoverage.CoverageIntegration)
    Assert.Equal("e2e", TestContractCoverage.adapterName TestContractCoverage.CoverageE2e)

[<Fact>]
let ``profile names round-trip`` () =
    Assert.Equal("measured", TestContractCoverage.profileName TestContractCoverage.MeasuredProfile)
    Assert.Equal("no-denominator", TestContractCoverage.profileName TestContractCoverage.NoDenominatorProfile)
