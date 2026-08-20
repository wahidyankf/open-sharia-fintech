# Diagram Format Fixes

Covers two finding types from the Diagram Format Check: (1) ASCII art that should be Mermaid, (2)
under-diagrammed plans.

### Finding Type 1: ASCII Art Should Be Mermaid

**Confidence**: **HIGH** — ASCII art clearly depicts a flow/sequence/state machine/component
interaction, the Mermaid equivalent is unambiguous — auto-convert. **MEDIUM** — ambiguous (hybrid
table/diagram) — flag for review. **FALSE_POSITIVE** — a simple directory tree or file listing —
exempt.

**How to convert**: follow
[repo-governance/conventions/formatting/diagrams.md](../../../../repo-governance/conventions/formatting/diagrams.md).
Choose the right type (component interactions/decision branches → `flowchart LR`; order-of-operations
→ `sequenceDiagram`; entity lifecycle → `stateDiagram-v2`; database schema → `erDiagram`). Default to
`flowchart LR` unless top-down is semantically required, with a `%%` comment explaining why. Follow
the color-blind-friendly palette and `%%` comment syntax from `docs-creating-accessible-diagrams`.

**Do not convert**: simple directory trees, or tables/matrices where Mermaid would reduce
readability.

### Finding Type 2: Under-Diagrammed Plan

**Confidence**: **HIGH** — the concern is unambiguous and the diagram type is deterministic —
auto-add. **MEDIUM** — the concern is present but plan prose is too sparse to derive a correct
diagram without invention — flag for review, never fabricate nodes/edges. **FALSE_POSITIVE** — the
plan is genuinely trivial/linear — exempt.

**How to add**: identify the concern from the finding; choose the diagram type (component
interactions/dependency position/decision branches → `flowchart LR`; sequence/flow →
`sequenceDiagram`; state transitions/phase flow → `stateDiagram-v2` or `flowchart LR`); derive nodes
and edges from plan prose only; apply the color-blind-friendly palette (verified hex codes, black
borders, white text on dark fills); place the diagram where the concern is first described. After
adding, re-read the containing section and confirm the diagram nodes match the surrounding prose.
