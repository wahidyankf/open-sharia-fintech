---
name: plan-applying-fixes
description: Full fix-recipe catalog for plan-fixer — the merge-step structural guard (no recipe may weaken a merge step's human gate, under any confidence/mode/verb), confidence assessment, and per-finding-type repair recipes covering content placement, delivery mode, operational readiness, manual assertions, UI/syllabus scaffolding, diagrams, worktree, execution clarity, executor tagging, anti-hallucination, and Knowledge Capture.
when_to_use: When applying validated fixes from a plan-checker audit report, or extending/auditing the plan-fixer agent's fix recipes.
---

# Applying Plan Fixes

Full fix-recipe catalog for `plan-fixer`: how to repair each `plan-checker` finding type, and the
confidence framework governing when a fix auto-applies versus escalates.

## Read First

Read `reference/01-merge-step-guard.md` before every other module. Its protection of a merge step's
human gate governs every recipe, tag, verb, and delivery mode.

## Reference Modules

- `reference/01-merge-step-guard.md` — the merge-step guard (read first).
- `reference/02-confidence-assessment-and-agent-mechanics.md` — confidence assessment, web-research
  delegation, mode-parameter handling, grilling interaction contract, validation strategy.
- `reference/03-content-placement-and-file-impact-fixes.md` — BRD/PRD content-placement fixes,
  file-impact tree repairs.
- `reference/04-delivery-mode-reconciliation-fixes.md` — PR-step/delivery-mode reconciliation,
  per-repository restriction fixes.
- `reference/05-delivery-boundary-step-placement-fixes.md` — Phase 0 PR/push removal,
  PR-steps-outside-boundary relocation.
- `reference/06-report-generation-and-confidence-examples.md` — fix-report generation, changed-files
  capture, FALSE_POSITIVE persistence, self-verification, confidence-level domain examples, factual
  accuracy fixes.
- `reference/07-operational-readiness-fixes.md` — operational readiness fixes (5 items).
- `reference/08-manual-behavioural-assertion-fixes.md` — manual behavioural assertion fixes (3 items).
- `reference/09-ui-design-funnel-scaffolding-fixes.md` — UI-design-funnel scaffolding.
- `reference/10-learning-bearing-syllabus-scaffolding-fixes.md` — learning-bearing syllabus
  scaffolding.
- `reference/11-diagram-format-fixes.md` — diagram format fixes (ASCII→Mermaid, under-diagrammed
  plans).
- `reference/12-worktree-and-delivery-mode-scaffolding-fixes.md` — worktree specification fixes,
  delivery mode fixes.
- `reference/pr-ci-and-merge-tag-fixes.md` — exact-head PR-CI scaffolding and the merge-tag recipe.
- `reference/14-execution-grade-clarity-fixes.md` — execution-grade clarity fixes (HARD RULE).
- `reference/15-executor-tagging-and-phase-gate-fixes-part1.md` and
  `reference/16-executor-tagging-and-phase-gate-fixes-part2.md` — executor-tagging/phase-gate fixes.
- `reference/17-anti-hallucination-fixes-part1.md` and
  `reference/18-anti-hallucination-fixes-part2.md` — anti-hallucination fixes (AP-1 through AP-10).
- `reference/19-knowledge-capture-phase-scaffolding-fixes-part1.md` and
  `reference/20-knowledge-capture-phase-scaffolding-fixes-part2.md` — Knowledge Capture phase
  scaffolding.

## Core Principles

**Never fabricate — scaffold, don't invent.** Every scaffolding recipe (UI funnel, syllabus,
Knowledge Capture, phase gates) inserts placeholders for the author to fill, never invented content.
**Re-validate before applying.** Every fix confirms the finding still exists (the file may have
changed since audit) before acting. **A more-plausible-sounding hallucination is the worst outcome**
of an anti-hallucination fix — refuse rather than replace one wrong claim with another.

## Quality-Gate Lifecycle Handoff

When given `delegated-gate-ids` and an evidence ledger, preserve both and skip exact delegated
predicates. Never revalidate, infer, or fix delegated work; missing or stale evidence remains
pending. Plan-domain findings remain actionable. See the
[lifecycle ownership policy](../../../repo-governance/workflows/meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md).
After edits, invalidate evidence whose registered scope intersects changed files.

## Missing Minimal-Sufficiency Rationale

For a lasting mechanism missing concrete-need and existing-mechanism rationale, add only two
`[AUTHOR INPUT REQUIRED]` scaffolds: the requirement/risk, and why evaluated mechanisms are
insufficient. Grill for both; never infer answers or mark unresolved placeholders fixed.

## Current Formal-Plan Contract

For newly created formal plans, repair toward the fixed core plus exactly one reader-led technical
shape, bootcamp-graduate readability, evidence-backed alternatives/prior art, schema/migration
contracts when applicable, and cohesive outcome sections with Input/Outcome/Proof plus granular
action checkboxes and separate detailed RED/GREEN/REFACTOR cycles. Reference
canonical Gherkin; never add copied scenarios or detail-free/keystroke checkboxes. Preserve
phase gates, ownership, natural cohesive delivery seams, production-deployable `main` states,
delivery mode, manual/operational verification, and Knowledge Capture. Remove LOC or file-count
boundary tests. Keep every artifact needed to build, verify, operate, roll back, and remain
internally consistent in its delivery unit; incomplete behaviour requires a temporary
production-disabled flag with both paths tested and rollout, rollback, and removal recorded. Do not
migrate archived plans or the existing Rhino plan.

## Related

`plan-validating-quality` (the checker methodology this fixer's recipes repair), `plan-creating-project-plans`
(the authoring templates several recipes insert verbatim), `repo-applying-maker-checker-fixer` (mode
parameter and report discovery mechanics), `repo-assessing-criticality-confidence` (confidence-level
definitions), `repo-generating-validation-reports` (fix report format).
