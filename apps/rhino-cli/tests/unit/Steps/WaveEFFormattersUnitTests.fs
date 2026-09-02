/// Plain xunit tests calling `RhinoCli.Cli.Formatters`'s Wave E/F rendering
/// functions directly with synthetic domain records — no CLI dispatch, no
/// fixture filesystem. These formatters are exercised end-to-end by the
/// Gherkin specs and `WaveEFDispatchUnitTests.fs`, but only through their
/// empty-findings "clean pass" branch: every real validator run against this
/// checkout or a minimal synthetic fixture finds zero findings, so the
/// non-empty-findings (FAILED/table-row) branches of these public formatters
/// never execute under coverlet. See `learnings.md`, 2026-08-30.
module RhinoCli.Tests.Unit.Steps.WaveEFFormattersUnitTests

open System
open Xunit
open RhinoCli.Cli.Formatters
open RhinoCli.Application

// ---------------------------------------------------------------------------
// formatGoDuration — every magnitude branch
// ---------------------------------------------------------------------------

[<Fact>]
let ``formatGoDuration renders zero as 0s`` () =
    Assert.Equal("0s", formatGoDuration TimeSpan.Zero)

[<Fact>]
let ``formatGoDuration renders sub-microsecond durations in nanoseconds`` () =
    let d = TimeSpan.FromMilliseconds(500.0 / 1_000_000.0)
    Assert.Equal("500ns", formatGoDuration d)

[<Fact>]
let ``formatGoDuration renders microseconds with a trimmed fraction`` () =
    let d = TimeSpan.FromMilliseconds(1.5 / 1_000.0)
    Assert.Equal("1.5µs", formatGoDuration d)

[<Fact>]
let ``formatGoDuration renders whole microseconds with no fraction`` () =
    let d = TimeSpan.FromMilliseconds(2.0 / 1_000.0)
    Assert.Equal("2µs", formatGoDuration d)

[<Fact>]
let ``formatGoDuration renders milliseconds with a trimmed fraction`` () =
    let d = TimeSpan.FromMilliseconds(1.5)
    Assert.Equal("1.5ms", formatGoDuration d)

[<Fact>]
let ``formatGoDuration renders whole milliseconds with no fraction`` () =
    let d = TimeSpan.FromMilliseconds(100.0)
    Assert.Equal("100ms", formatGoDuration d)

[<Fact>]
let ``formatGoDuration renders whole seconds with no fraction`` () =
    let d = TimeSpan.FromSeconds(1.0)
    Assert.Equal("1s", formatGoDuration d)

[<Fact>]
let ``formatGoDuration renders seconds with a fractional part`` () =
    let d = TimeSpan.FromMilliseconds(1500.0)
    Assert.Equal("1.5s", formatGoDuration d)

[<Fact>]
let ``formatGoDuration renders minutes and seconds`` () =
    let d = TimeSpan.FromSeconds(65.0)
    Assert.Equal("1m5s", formatGoDuration d)

[<Fact>]
let ``formatGoDuration renders hours, minutes, and seconds`` () =
    let d = TimeSpan.FromSeconds(3665.0)
    Assert.Equal("1h1m5s", formatGoDuration d)

// ---------------------------------------------------------------------------
// validationText / validationMarkdown — warning + failed branches, verbose,
// quiet
// ---------------------------------------------------------------------------

let private mixedValidationResult: Harness.ValidationResult =
    Harness.ValidationResult.empty
    |> Harness.ValidationResult.tally (Harness.ValidationCheck.passed "check-a" "all good")
    |> Harness.ValidationResult.tally (Harness.ValidationCheck.warning "check-b" "expected-b" "actual-b" "warn message")
    |> Harness.ValidationResult.tally (Harness.ValidationCheck.failed "check-c" "expected-c" "actual-c" "fail message")
    |> fun r ->
        { r with
            Duration = TimeSpan.FromMilliseconds 42.0 }

[<Fact>]
let ``validationText reports warnings and failed checks`` () =
    let text = validationText mixedValidationResult false false
    Assert.Contains("Warnings: 1", text)
    Assert.Contains("Failed: 1", text)
    Assert.Contains("fail message", text)

[<Fact>]
let ``validationText in quiet mode omits the banner`` () =
    let text = validationText mixedValidationResult false true
    Assert.DoesNotContain("Validation Complete", text)

[<Fact>]
let ``validationText in verbose mode lists every check`` () =
    let text = validationText mixedValidationResult true false
    Assert.Contains("All Checks:", text)
    Assert.Contains("check-a", text)

[<Fact>]
let ``validationMarkdown reports warnings and failed sections`` () =
    let markdown = validationMarkdown mixedValidationResult false
    Assert.Contains("## Failed Checks", markdown)
    Assert.Contains("## Warnings", markdown)
    Assert.Contains("expected-c", markdown)

[<Fact>]
let ``validationMarkdown in verbose mode lists every check`` () =
    let markdown = validationMarkdown mixedValidationResult true
    Assert.Contains("## All Checks", markdown)

// ---------------------------------------------------------------------------
// duplicationText / duplicationMarkdown — non-empty findings
// ---------------------------------------------------------------------------

let private oneDuplicationFinding: Harness.DuplicationFinding =
    { Files = [ "a.md"; "b.md" ]
      StartLines = [ 3; 9 ]
      WindowSize = 5
      Severity = "high"
      Message = "identical workflow boilerplate" }

[<Fact>]
let ``duplicationText reports a cluster`` () =
    let text = duplicationText [ oneDuplicationFinding ]
    Assert.Contains("FAILED: 1 cluster", text)
    Assert.Contains("a.md:3", text)

[<Fact>]
let ``duplicationMarkdown reports a cluster`` () =
    let markdown = duplicationMarkdown [ oneDuplicationFinding ]
    Assert.Contains("**FAILED**: 1 duplication cluster", markdown)
    Assert.Contains("a.md<br>b.md", markdown)

// ---------------------------------------------------------------------------
// vendorAuditMarkdown / layerCoherenceMarkdown / traceabilityMarkdown —
// non-empty findings
// ---------------------------------------------------------------------------

[<Fact>]
let ``vendorAuditMarkdown reports a violation`` () =
    let finding: RepoGovernance.VendorFinding =
        { Path = "docs/foo.md"
          Line = 7
          Match = "master"
          Replacement = "main" }

    let markdown = vendorAuditMarkdown [ finding ]
    Assert.Contains("**FAILED**: 1 violation", markdown)
    Assert.Contains("docs/foo.md", markdown)

[<Fact>]
let ``layerCoherenceMarkdown reports a finding`` () =
    let finding: RepoGovernance.LayerCoherenceFinding =
        { File = "arch.md"
          Severity = "high"
          Kind = RepoGovernance.KindMissingDoc
          Message = "missing companion doc" }

    let markdown = layerCoherenceMarkdown [ finding ]
    Assert.Contains("**FAILED**: 1 finding", markdown)
    Assert.Contains("missing-doc", markdown)

[<Fact>]
let ``traceabilityMarkdown reports a finding`` () =
    let finding: RepoGovernance.TraceabilityFinding =
        { Path = "repo-governance/foo.md"
          Line = 1
          Kind = RepoGovernance.KindMissingVisionSupported
          Message = "missing Vision Supported section" }

    let markdown = traceabilityMarkdown [ finding ]
    Assert.Contains("**FAILED**: 1 finding", markdown)
    Assert.Contains("missing-vision-supported", markdown)

// ---------------------------------------------------------------------------
// governanceAuditText / governanceAuditMarkdown — failed + skipped
// false-positives
// ---------------------------------------------------------------------------

let private failingAuditEnvelope: RepoGovernance.AuditEnvelope =
    let finding: RepoGovernance.AuditFinding =
        { Key = "cat|file|abcd1234"
          Severity = "high"
          Criticality = "blocking"
          File = "docs/foo.md"
          Line = 5
          Message = "broken link" }

    let category: RepoGovernance.AuditCategoryResult =
        { Name = "validate-links"
          Command = "md links validate"
          Passed = false
          Findings = [ finding ] }

    { Schema = "rhino-cli/repo-governance-audit/v1"
      Status = "failed"
      Result =
        { GitSha = "deadbeef"
          RanAt = "2026-08-30T00:00:00Z"
          TotalFindings = 1
          BySeverity = Map.ofList [ "high", 1 ]
          ByCategory = Map.ofList [ "validate-links", 1 ]
          Categories = [ category ]
          SkippedFalsePositives = [ finding ] } }

[<Fact>]
let ``governanceAuditText reports failures and skipped false-positives`` () =
    let text = governanceAuditText failingAuditEnvelope
    Assert.Contains("GOVERNANCE AUDIT FAILED: 1 finding(s)", text)
    Assert.Contains("docs/foo.md:5", text)
    Assert.Contains("1 skipped false-positive(s)", text)

[<Fact>]
let ``governanceAuditMarkdown reports failures and skipped false-positives`` () =
    let markdown = governanceAuditMarkdown failingAuditEnvelope
    Assert.Contains("**FAILED**: 1 finding(s)", markdown)
    Assert.Contains("skipped false-positive(s)", markdown)

// ---------------------------------------------------------------------------
// cardinalityMarkdown — non-empty findings
// ---------------------------------------------------------------------------

[<Fact>]
let ``cardinalityMarkdown reports a violation`` () =
    let finding: Specs.GherkinCardinalityFinding =
        { File = "specs/foo.feature"
          Line = 3
          Scenario = "Does the thing"
          Keyword = "Given"
          Count = 2
          Severity = "high" }

    let markdown = cardinalityMarkdown [ finding ]
    Assert.Contains("**FAILED**: 1 violation", markdown)
    Assert.Contains("specs/foo.feature", markdown)

// ---------------------------------------------------------------------------
// dartScaffoldText / dartScaffoldJson / dartScaffoldMarkdown
// ---------------------------------------------------------------------------

let private dartResultWithModels: Contracts.DartScaffoldResult =
    { PubspecCreated = true
      BarrelCreated = true
      ModelFiles = [ "user.dart"; "order.dart" ] }

[<Fact>]
let ``dartScaffoldText lists model files`` () =
    let text = dartScaffoldText dartResultWithModels
    Assert.Contains("2 model files", text)
    Assert.Contains("user.dart", text)

[<Fact>]
let ``dartScaffoldJson reports success`` () =
    let json = dartScaffoldJson dartResultWithModels
    Assert.Contains("\"status\"", json)
    Assert.Contains("user.dart", json)

[<Fact>]
let ``dartScaffoldMarkdown lists model files`` () =
    let markdown = dartScaffoldMarkdown dartResultWithModels
    Assert.Contains("## Model Files", markdown)
    Assert.Contains("order.dart", markdown)

[<Fact>]
let ``dartScaffoldMarkdown omits the model-files section when there are none`` () =
    let empty: Contracts.DartScaffoldResult =
        { PubspecCreated = true
          BarrelCreated = true
          ModelFiles = [] }

    let markdown = dartScaffoldMarkdown empty
    Assert.DoesNotContain("## Model Files", markdown)

// ---------------------------------------------------------------------------
// syncText / syncJson / syncMarkdown — the `harness bindings generate`
// report, driven directly instead of through the (deferred, schema-heavy)
// `runHarnessBindingsGenerateLeaf` fixture
// ---------------------------------------------------------------------------

let private syncResultWithFailuresAndWarnings: Harness.ConvertAllResult =
    { Converted = 3
      Failed = 1
      FailedFiles = [ "broken-agent.md" ]
      Warnings =
        [ { AgentName = "some-agent"
            Field = "color"
            Reason = "unrecognized value" } ] }

[<Fact>]
let ``syncText reports failures and, when verbose, warnings`` () =
    let text =
        syncText syncResultWithFailuresAndWarnings (TimeSpan.FromMilliseconds 10.0) true false

    Assert.Contains("1 failed", text)
    Assert.Contains("broken-agent.md", text)
    Assert.Contains("FAILED", text)
    Assert.Contains("dropped field", text)

[<Fact>]
let ``syncText in quiet mode omits the banner`` () =
    let text =
        syncText syncResultWithFailuresAndWarnings (TimeSpan.FromMilliseconds 10.0) false true

    Assert.DoesNotContain("Sync Complete", text)

[<Fact>]
let ``syncJson reports a failure status`` () =
    let json =
        syncJson syncResultWithFailuresAndWarnings (TimeSpan.FromMilliseconds 10.0)

    Assert.Contains("\"failure\"", json)
    Assert.Contains("broken-agent.md", json)

[<Fact>]
let ``syncMarkdown reports failed files`` () =
    let markdown =
        syncMarkdown syncResultWithFailuresAndWarnings (TimeSpan.FromMilliseconds 10.0)

    Assert.Contains("## Failed Files", markdown)
    Assert.Contains("broken-agent.md", markdown)

let private cleanSyncResult: Harness.ConvertAllResult =
    { Converted = 3
      Failed = 0
      FailedFiles = []
      Warnings = [] }

[<Fact>]
let ``syncText reports success when nothing failed`` () =
    let text = syncText cleanSyncResult (TimeSpan.FromMilliseconds 5.0) false false
    Assert.Contains("SUCCESS", text)

[<Fact>]
let ``syncJson reports a success status when nothing failed`` () =
    let json = syncJson cleanSyncResult (TimeSpan.FromMilliseconds 5.0)
    Assert.Contains("\"success\"", json)

[<Fact>]
let ``syncMarkdown reports success when nothing failed`` () =
    let markdown = syncMarkdown cleanSyncResult (TimeSpan.FromMilliseconds 5.0)
    Assert.Contains("SUCCESS", markdown)

// ---------------------------------------------------------------------------
// coverageJson / coverageMarkdown — direct calls, since the CLI's own
// behavior-coverage leaves only render Text in this file's fixtures
// ---------------------------------------------------------------------------

let private emptyCheckResult: RhinoCli.Application.Specs.CheckResult =
    { TotalSpecs = 1
      TotalScenarios = 1
      TotalSteps = 1
      Gaps = []
      ScenarioGaps = []
      StepGaps = []
      OrphanStepImpls = [] }

[<Fact>]
let ``coverageJson renders a clean result`` () =
    let json = coverageJson emptyCheckResult
    Assert.Contains("\"success\"", json)

[<Fact>]
let ``coverageMarkdown renders a clean result`` () =
    let markdown = coverageMarkdown emptyCheckResult
    Assert.NotEmpty markdown

// ---------------------------------------------------------------------------
// statusJson / statusBanner (via validationText) — the warning-only branch,
// never hit by `mixedValidationResult` since it also carries a failed check
// ---------------------------------------------------------------------------

let private warningOnlyValidationResult: Harness.ValidationResult =
    Harness.ValidationResult.empty
    |> Harness.ValidationResult.tally (Harness.ValidationCheck.passed "check-a" "all good")
    |> Harness.ValidationResult.tally (Harness.ValidationCheck.warning "check-b" "expected-b" "actual-b" "warn message")

[<Fact>]
let ``validationText reports a warnings-only banner`` () =
    let text = validationText warningOnlyValidationResult false false
    Assert.Contains("VALIDATION PASSED WITH WARNINGS", text)

// ---------------------------------------------------------------------------
// coverageJson's "failure" branch — a non-empty gap list
// ---------------------------------------------------------------------------

let private checkResultWithGap: RhinoCli.Application.Specs.CheckResult =
    { TotalSpecs = 1
      TotalScenarios = 1
      TotalSteps = 1
      Gaps =
        [ { RhinoCli.Application.Specs.SpecFile = "specs/example.feature"
            RhinoCli.Application.Specs.Stem = "example" } ]
      ScenarioGaps = []
      StepGaps = []
      OrphanStepImpls = [] }

[<Fact>]
let ``coverageJson renders a failure status when gaps are present`` () =
    let json = coverageJson checkResultWithGap
    Assert.Contains("\"failure\"", json)
    Assert.Contains("specs/example.feature", json)

// ---------------------------------------------------------------------------
// validationJson / statusJson — a direct-call fixture per branch, since
// `statusJson` is reached only through `validationJson`, never through
// `validationText`/`validationMarkdown` (which use the sibling private
// function `statusBanner` instead).
// ---------------------------------------------------------------------------

let private allPassValidationResult: Harness.ValidationResult =
    Harness.ValidationResult.empty
    |> Harness.ValidationResult.tally (Harness.ValidationCheck.passed "check-a" "all good")

[<Fact>]
let ``validationJson reports a failure status`` () =
    let json = validationJson mixedValidationResult
    Assert.Contains("\"failure\"", json)

[<Fact>]
let ``validationJson reports a warning status`` () =
    let json = validationJson warningOnlyValidationResult
    Assert.Contains("\"warning\"", json)

[<Fact>]
let ``validationJson reports a success status`` () =
    let json = validationJson allPassValidationResult
    Assert.Contains("\"success\"", json)
