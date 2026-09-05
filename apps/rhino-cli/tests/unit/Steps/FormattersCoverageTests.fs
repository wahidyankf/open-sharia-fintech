/// Focused resource-free coverage for formatter branches not selected by the
/// canonical repository's current clean state.
module RhinoCli.Tests.Unit.Steps.FormattersCoverageTests

open Xunit
open RhinoCli.Application
open RhinoCli.Cli.Formatters

let private vendorFinding: RepoGovernance.VendorFinding =
    { Path = "docs/example.md"
      Line = 7
      Match = "master"
      Replacement = "main" }

let private layerFinding: RepoGovernance.LayerCoherenceFinding =
    { File = "docs/architecture.md"
      Severity = "high"
      Kind = RepoGovernance.KindMissingDoc
      Message = "missing companion" }

let private traceFinding: RepoGovernance.TraceabilityFinding =
    { Path = "repo-governance/example.md"
      Line = 3
      Kind = RepoGovernance.KindMissingVisionSupported
      Message = "missing vision" }

let private auditEnvelope: RepoGovernance.AuditEnvelope =
    let category: RepoGovernance.AuditCategoryResult =
        { Name = "validate-links"
          Command = "md links validate"
          Passed = true
          Findings = [] }

    { Schema = "rhino-cli/repo-governance-audit/v1"
      Status = "passed"
      Result =
        { GitSha = "deadbeef"
          RanAt = "2026-09-05T00:00:00Z"
          TotalFindings = 0
          BySeverity = Map.empty
          ByCategory = Map.empty
          Categories = [ category ]
          SkippedFalsePositives = [] } }

let private duplicationFinding: Harness.DuplicationFinding =
    { Files = [ "a.md"; "b.md" ]
      StartLines = [ 2; 8 ]
      WindowSize = 5
      Severity = "high"
      Message = "duplicate window" }

[<Fact>]
let ``word budget text renders a failing row`` () =
    let finding: Governance.WordBudgetFinding =
        { Path = "AGENTS.md"
          Size = 1001UL
          Target = 900UL
          Warn = 950UL
          Fail = 1000UL
          Severity = Governance.WordBudgetSeverity.Fail
          Message = "over fail ceiling" }

    Assert.Contains("[FAIL] AGENTS.md", wordBudgetText [ finding ])

[<Fact>]
let ``vendor formatters render clean and failing results`` () =
    Assert.Contains("PASSED", vendorAuditText [])
    Assert.Contains("master", vendorAuditText [ vendorFinding ])
    Assert.Contains("\"status\": \"passed\"", vendorAuditJson [])
    Assert.Contains("\"replacement\": \"main\"", vendorAuditJson [ vendorFinding ])
    Assert.Contains("**PASSED**", vendorAuditMarkdown [])

[<Fact>]
let ``layer coherence formatters render clean and failing results`` () =
    Assert.Contains("PASSED", layerCoherenceText [])
    Assert.Contains("missing companion", layerCoherenceText [ layerFinding ])
    Assert.Contains("\"status\": \"passed\"", layerCoherenceJson [])
    Assert.Contains("missing-doc", layerCoherenceJson [ layerFinding ])
    Assert.Contains("**PASSED**", layerCoherenceMarkdown [])

[<Fact>]
let ``traceability formatters render clean and failing results`` () =
    Assert.Contains("PASSED", traceabilityText [])
    Assert.Contains("missing vision", traceabilityText [ traceFinding ])
    Assert.Contains("\"status\": \"passed\"", traceabilityJson [])
    Assert.Contains("missing-vision-supported", traceabilityJson [ traceFinding ])
    Assert.Contains("**PASSED**", traceabilityMarkdown [])

[<Fact>]
let ``governance audit formatters render a clean envelope`` () =
    Assert.Contains("GOVERNANCE AUDIT PASSED", governanceAuditText auditEnvelope)
    Assert.Contains("\"status\": \"passed\"", governanceAuditJson auditEnvelope)
    Assert.Contains("**PASSED**", governanceAuditMarkdown auditEnvelope)

[<Fact>]
let ``validation banner renders a clean result`` () =
    Assert.Contains("VALIDATION PASSED", validationText Harness.ValidationResult.empty false false)

[<Fact>]
let ``duplication formatters render clean and failing JSON`` () =
    Assert.Contains("PASSED", duplicationText [])
    Assert.Contains("\"status\": \"passed\"", duplicationJson [])
    Assert.Contains("duplicate window", duplicationJson [ duplicationFinding ])
    Assert.Contains("**PASSED**", duplicationMarkdown [])
