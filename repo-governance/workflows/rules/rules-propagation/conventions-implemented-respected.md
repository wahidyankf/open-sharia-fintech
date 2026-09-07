---
description: Which repository conventions this workflow enforces during a run and which it must not breach while placing a rule.
when_to_use: Use when tracing a step of this workflow to the convention that constrains it.
---

# Conventions Implemented/Respected

## Implemented

- **[Governance Word-Budget](../../../conventions/structure/governance-word-budget.md)** — the
  source of the fixed-size-cache model. Steps 4 and 5 exist because this convention forbids raising
  a threshold to fit content, leaving split and relocation as the only moves.
- **[Governance Word-Budget Remediation](../../../conventions/structure/governance-word-budget-remediation.md)** —
  the remedy the eviction protocol applies when a surface is full.
- **[Governance Vendor-Independence](../../../conventions/structure/governance-vendor-independence.md)** —
  Step 2's neutrality classification and Step 4's canonical-versus-shim routing. A neutral rule in a
  shim binds one harness and looks landed.
- **[Governance README Completeness](../../../conventions/structure/governance-readme-completeness.md)** —
  Step 6's reindexing requirement. A new document without an annotated index entry is unreachable.

## Respected

- **[Multi-Harness Binding](../../../conventions/structure/multi-harness-binding.md)** — mirrors
  are regenerated, never hand-edited, and land in the same commit as their source.
- **[File Naming](../../../conventions/structure/file-naming.md)** and
  **[Ordinal Filename Prefixes](../../../conventions/structure/ordinal-filename-prefixes.md)** —
  any document the run creates is named accordingly; a step keeps its number, a shard does not.
- **[Diátaxis Framework](../../../conventions/structure/diataxis-framework.md)** — placement inside
  a layer follows the category the document belongs to.
- **[Deterministic vs. AI Validation Split](../../../conventions/structure/deterministic-vs-ai-validation-split.md)** —
  Step 8 runs the deterministic gates first and never re-derives by judgement what a gate settles.
- **[Commit Messages](../../../development/workflow/commit-messages.md)** — Step 9's commit form.

## Related Documents

- [Principles Implemented/Respected](./principles-implemented-respected.md) — the layer above.
