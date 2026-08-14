---
name: plan-verifying-execution
description: Post-execution verification methodology for plan-execution-checker — confirms completed plan implementation actually did what the plan said, as the temporal sibling of plan-validating-quality's pre-execution rules (same rule domains — operational readiness, manual assertions, worktree usage, anti-hallucination, knowledge capture, delivery mode — checked against the post-execution repo state instead of the authored plan text).
when_to_use: When validating that a completed plan implementation meets requirements, follows technical documentation, completes the delivery checklist, and passed all execution-time gates before archival to plans/done/.
---

# Verifying Plan Execution

Full post-execution validation methodology for `plan-execution-checker`: confirms a completed plan's
implementation matches what was promised, and that every execution-time gate actually held.

## Reference Modules

- `reference/01-scope-and-workflow.md` — Validation Scope (Requirements Coverage, Technical
  Documentation Alignment, Delivery Checklist Completion, Code Quality, Integration Validation),
  Workflow Overview (Steps 0-7).
- `reference/02-operational-readiness-and-manual-assertions.md` — Step 5b (Operational Readiness
  Execution) and Step 5c (Manual Behavioral Assertions) verification.
- `reference/03-archival-and-worktree-verification.md` — Step 5d (Plan Archival and README Updates)
  and Step 5e (Worktree Usage) verification.
- `reference/04-phase-gate-and-anti-hallucination.md` — Step 5f-gates (Phase Gate and Execution
  Marker) and Step 5f (Anti-Hallucination) post-execution verification.
- `reference/05-knowledge-capture-and-delivery-mode.md` — Step 5h (Knowledge Capture Routing,
  blocking gate) and Step 5i (Delivery Mode and PR-Review Cycle) verification.

## Core Principles

**This is the final quality gate** — be thorough, independent, and uncompromising. **Every rule
states its own criticality** per finding, not a blanket file-level severity. **Post-execution
re-checks, not re-derives**: `plan-checker` validates the plan is well-formed at authoring time;
this skill validates execution actually did what the well-formed plan said, against the
post-execution repo state (git log, CI status, delivered files) — the finding types overlap in name
but the evidence source never does. **Blocking gates block archival unconditionally** — Knowledge
Capture (Step 5h) and any CRITICAL finding halt archival regardless of how many other checks passed.

## Related

`plan-validating-quality` (the authoring-time sibling methodology — Anti-Hallucination and
criticality-table shapes track it closely), `plan-applying-fixes` (repairs findings this skill's
pre-execution counterpart raises), `repo-generating-validation-reports` (report format),
`repo-assessing-criticality-confidence` (criticality/confidence framework).
