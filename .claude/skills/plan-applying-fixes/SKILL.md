---
name: plan-applying-fixes
description: Full fix-recipe catalog for plan-fixer — the merge-step structural guard (no recipe may weaken a merge step's human gate, under any confidence/mode/verb), confidence assessment, and per-finding-type repair recipes covering content placement, delivery mode, operational readiness, manual assertions, UI/syllabus scaffolding, diagrams, worktree, execution clarity, executor tagging, anti-hallucination, and Knowledge Capture.
when_to_use: When applying validated fixes from a plan-checker audit report, or extending/auditing the plan-fixer agent's fix recipes.
---

# Applying Plan Fixes

Full fix-recipe catalog for `plan-fixer`: how to repair each `plan-checker` finding type, and the
confidence framework governing when a fix auto-applies versus escalates.

## Read First

`reference/01-merge-step-guard.md` — the merge-step structural guard MUST be read before any other
reference module. It states what it protects (a merge step's human gate) rather than enumerating
tags/verbs/modes, because two prior enumeration-style guards were each defeated by an axis nobody had
named. Every other reference module's recipes are subordinate to this guard.

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
- `reference/08-manual-behavioral-assertion-fixes.md` — manual behavioral assertion fixes (3 items).
- `reference/09-ui-design-funnel-scaffolding-fixes.md` — UI-design-funnel scaffolding.
- `reference/10-learning-bearing-syllabus-scaffolding-fixes.md` — learning-bearing syllabus
  scaffolding.
- `reference/11-diagram-format-fixes.md` — diagram format fixes (ASCII→Mermaid, under-diagrammed
  plans).
- `reference/12-worktree-and-delivery-mode-scaffolding-fixes.md` — worktree specification fixes,
  delivery mode fixes.
- `reference/13-pr-review-cycle-and-merge-tag-fixes.md` — PR-Review Maker→Fixer Cycle scaffolding,
  the merge-tag mismatch recipe.
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

## Missing Minimal-Sufficiency Rationale

When a checker finds a lasting mechanism without its concrete-need and existing-mechanism
rationale, add only a clearly marked scaffold in `tech-docs.md` or the single-file plan's
`Technical Approach`: `[AUTHOR INPUT REQUIRED] Concrete requirement, correctness/safety obligation,
or demonstrated recurring risk`; `[AUTHOR INPUT REQUIRED] Existing mechanisms evaluated and why
they are insufficient`. Grill the author for both answers. Never infer them from the proposed
implementation, and never mark the finding fixed while either placeholder remains unresolved.

## Related

`plan-validating-quality` (the checker methodology this fixer's recipes repair), `plan-creating-project-plans`
(the authoring templates several recipes insert verbatim), `repo-applying-maker-checker-fixer` (mode
parameter and report discovery mechanics), `repo-assessing-criticality-confidence` (confidence-level
definitions), `repo-generating-validation-reports` (fix report format).
