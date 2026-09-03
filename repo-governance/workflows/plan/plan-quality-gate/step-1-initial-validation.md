---
title: "Step 1 — Initial Validation"
description: Lists the full validation scope plan-checker runs on its first pass, per its Steps 0-7 and the conditional 5b-5n sub-steps.
when_to_use: Use when checking exactly what plan-checker validates on the initial audit pass.
---

# Step 1. Initial Validation (Sequential)

## 0. Lifecycle Ownership Filter

First apply the
[lifecycle validation ownership policy](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md).
Record exact `delegated-gate-ids` and their evidence ledger. Deterministic gates own links, maps,
word budgets, formatting, Mermaid mechanics, and Gherkin cardinality. Plan semantics remain in
scope; remove only exact registry-owned predicates from checker prompts, and consume their evidence
without rederiving it.

Run plan validation to identify completeness, accuracy, and hallucination issues.

**Agent**: `plan-checker`

- **Args**: `scope: {input.scope}, delegated-gate-ids: {step0.outputs.delegated-gate-ids}, lifecycle-evidence: {step0.outputs.lifecycle-evidence}`
- **Output**: `{audit-report-1}` - Initial audit report in `generated-reports/`

**Validation scope** (per `plan-checker` Steps 0-7 + 5b/5c/5d/5e/5f/5g/5h/5i/5j/5k/5n):

- Prospective structure (fixed core and exactly one reader-led technical shape for newly created
  formal plans; no migration findings for `plans/done/` or the existing Rhino plan)
- Comprehensive bootcamp-graduate readability and decision-to-delivery traceability
- Material decisions (selected option plus two viable alternatives or evidence-backed
  disqualification, repository and applicable external prior art, trade-offs, consequences, revisit triggers)
- Requirements (BRD + PRD content placement, Gherkin)
- Technical documentation (architecture, design decisions, diagrams, and the annotated file-impact
  tree; `### More Detail` is optional supporting context, never a replacement for the tree)
- Delivery checklist (outcome-section cohesion; granular action detail; Input/Outcome/Proof; AC
  references; separate TDD actions; natural cohesive delivery seams; production-deployable
  resulting `main` states; applicable flag tests and rollout/rollback/removal; no LOC/file-count
  boundary tests; no copied full Gherkin)
- Operational readiness (Step 5b — quality gates, CI verification, env setup)
- Manual behavioral assertions (Step 5c — Playwright MCP / curl)
- Worktree specification (Step 5d — declared `## Worktree` section + path format)
- Execution-grade clarity (Step 5e — file paths, commands, acceptance criteria per checkbox)
- **Anti-hallucination scan** (Step 5f — confidence labels, Anti-Pattern Catalog AP-1 through
  AP-10, suggested-executor annotation validity, web-citation completeness) per the
  [Plan Anti-Hallucination Convention](../../../development/quality/plan-anti-hallucination.md)
- **Harness-neutrality scan** (Step 5g — conditional: fires only when the plan touches agents,
  skills, rules, or `repo-governance/` paths) per the
  [Multi-Harness Binding Convention](../../../conventions/structure/multi-harness-binding.md)
- Schema/migration contracts when persisted data changes: data-model diagram, exact old/new
  contracts, field lifecycle guide, compatibility, expand-migrate-verify-contract, rollback, and
  no-loss proof
- Rule propagation and exact as-built C4 packets in the phase that changes them, plus explicit
  triggers and evidence-backed `Not triggered` dispositions for dormant recovery work
- **Specs & Gherkin delivery coverage** (Step 5j — conditional: behavior-changing plans under
  `apps/`/`libs/`/`specs/` must carry companion Gherkin + a `specs:coverage` gate) per the
  [Feature Change Completeness Convention](../../../development/quality/feature-change-completeness.md)
- **UI-design-funnel completeness** (Step 5k — conditional: fires only on **UI-bearing** plans that
  add/change user-facing screens or components under `apps/` or `libs/`; FLAGS at HIGH any missing
  funnel artefact — ≥2 named low-fi alternatives, 2 hi-fi `.excalidraw.png` finalists, a named
  selection, a rationale, the grounding/prior-art note; pure-refactor / no-UI / governance-only
  plans are exempt). The gate fails when a UI-bearing plan skips the funnel. Per the
  [UI Mockups in Plan Docs convention](../../../conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope)
- **Learning-Bearing Syllabus Completeness** (Step 5n — conditional: fires only on
  **learning-bearing** plans whose delivery checklist authors or restructures course, tutorial, or
  curriculum content; FLAGS at HIGH any missing syllabus artefact — the required
  `syllabus/README.md` + `courses/` + `paths/` layout, the template-derived per-course shape, the
  `## Corpus Disposition` declaration, and the Custodian line; plans that only read or lightly
  correct an existing corpus are exempt). The gate fails when a learning-bearing plan skips the
  syllabus record. Per the
  [Learning-Plan `syllabus/` Folder Convention](../../../conventions/structure/learning-plan-syllabus.md)

For external claims that are not already documented in the repo and require more than a
single-shot URL fetch, `plan-checker` delegates research to
[`web-researcher`](../../../../.claude/agents/web/web-researcher.md) per the lower plan-content
threshold (any non-grep'd external claim → delegate). See
[Plan Anti-Hallucination Convention §Web-Research Delegation](../../../development/quality/plan-anti-hallucination/refuse-on-uncertainty-rule-and-web-research-delegation.md#web-research-delegation-lower-threshold-for-plans).

**Success criteria**: Checker completes and generates audit report.

**On failure**: Terminate workflow with status `fail`.
