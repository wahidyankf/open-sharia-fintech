/// Plain xunit tests for `RhinoCli.Application.Md`'s Mermaid **warning**
/// renderers — the advisory half of `md mermaid validate`.
///
/// Violations are exercised by the existing `MdSteps.fs` scenarios and by
/// `shadow-diff.sh` against real repository diagrams. Warnings are not: this
/// repository's committed diagrams stay inside the default width, depth, and
/// subgraph-density thresholds, so `mermaidWarningDetail` and the JSON
/// `warningNode` builder never run on live data. Constructing the result
/// value directly pins both, and keeps them pinned no matter what the
/// corpus contains — the same corpus-independence rule the two Wave D
/// formatter defects taught (see `learnings.md`, 2026-08-28).
module RhinoCli.Tests.Unit.Steps.WaveDMermaidWarningUnitTests

open System.Text.Json
open Xunit
open RhinoCli.Application.Md

let private complexDiagramWarning: MermaidWarning =
    { Kind = MermaidComplexDiagram
      FilePath = "docs/wide.md"
      BlockIndex = 0
      StartLine = 4
      ActualWidth = 9
      ActualDepth = 7
      MaxWidth = 4
      MaxDepth = 5
      SubgraphLabel = ""
      SubgraphNodeCount = 0
      MaxSubgraphNodes = 6 }

let private denseSubgraphWarning: MermaidWarning =
    { Kind = MermaidSubgraphDense
      FilePath = "docs/dense.md"
      BlockIndex = 1
      StartLine = 20
      ActualWidth = 3
      ActualDepth = 2
      MaxWidth = 4
      MaxDepth = 5
      SubgraphLabel = "Ingest"
      SubgraphNodeCount = 11
      MaxSubgraphNodes = 6 }

let private unnamedSubgraphWarning: MermaidWarning =
    { denseSubgraphWarning with
        FilePath = "docs/unnamed.md"
        SubgraphLabel = "" }

let private resultWith (warnings: MermaidWarning list) : MermaidValidationResult =
    { FilesScanned = List.length warnings
      BlocksScanned = List.length warnings
      Violations = []
      Warnings = warnings }

// ---------------------------------------------------------------------------
// warning kind codes
// ---------------------------------------------------------------------------

[<Fact>]
let ``mermaidWarningKindCode returns the stable code for each kind`` () =
    Assert.Equal("complex_diagram", mermaidWarningKindCode MermaidComplexDiagram)
    Assert.Equal("subgraph_density", mermaidWarningKindCode MermaidSubgraphDense)

// ---------------------------------------------------------------------------
// text rendering
// ---------------------------------------------------------------------------

[<Fact>]
let ``formatMermaidText marks a warning-only file WARN rather than FAIL`` () =
    let text = formatMermaidText (resultWith [ complexDiagramWarning ]) false false
    Assert.Contains("[WARN] docs/wide.md", text)
    Assert.DoesNotContain("[FAIL]", text)

[<Fact>]
let ``formatMermaidText spells out a complex-diagram warning`` () =
    let text = formatMermaidText (resultWith [ complexDiagramWarning ]) true false
    Assert.Contains("docs/wide.md", text)
    // The detail line has to carry the measured figures against the
    // configured ceilings, or the advisory is unactionable.
    Assert.Contains("9", text)
    Assert.Contains("4", text)

[<Fact>]
let ``formatMermaidText names a dense subgraph by its label`` () =
    let text = formatMermaidText (resultWith [ denseSubgraphWarning ]) true false
    Assert.Contains("Ingest", text)
    Assert.Contains("11", text)

[<Fact>]
let ``formatMermaidText falls back to (unnamed) for a label-less subgraph`` () =
    let text = formatMermaidText (resultWith [ unnamedSubgraphWarning ]) true false
    Assert.Contains("(unnamed)", text)

[<Fact>]
let ``formatMermaidText stays silent under --quiet only when nothing was found`` () =
    Assert.Equal("", formatMermaidText (resultWith []) false true)
    Assert.NotEmpty(formatMermaidText (resultWith [ complexDiagramWarning ]) false true)

// ---------------------------------------------------------------------------
// JSON rendering
// ---------------------------------------------------------------------------

[<Fact>]
let ``formatMermaidJson emits one warning node per warning`` () =
    let json =
        formatMermaidJson (resultWith [ complexDiagramWarning; denseSubgraphWarning ])

    use doc = JsonDocument.Parse(json)
    Assert.Contains("complex_diagram", json)
    Assert.Contains("subgraph_density", json)
    Assert.Contains("docs/wide.md", json)
    Assert.Contains("docs/dense.md", json)
    Assert.Contains("Ingest", json)
    Assert.True(doc.RootElement.ValueKind = JsonValueKind.Object)

[<Fact>]
let ``formatMermaidMarkdown renders a warning-only result`` () =
    let markdown = formatMermaidMarkdown (resultWith [ denseSubgraphWarning ])
    Assert.NotEmpty(markdown)
