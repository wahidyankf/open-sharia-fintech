---
name: plan-applying-fixes
description: Full fix-recipe catalog for plan-fixer — the merge-step structural guard (no recipe may weaken a merge step's human gate, under any confidence/mode/verb), confidence assessment, and per-finding-type repair recipes covering content placement, delivery mode, operational readiness, manual assertions, UI/syllabus scaffolding, diagrams, worktree, execution clarity, executor tagging, anti-hallucination, and Knowledge Capture.
when_to_use: When applying validated fixes from a plan-checker audit report, or extending/auditing the plan-fixer agent's fix recipes.
---

# Applying Plan Fixes

Full fix-recipe catalog for `plan-fixer`: how to repair each `plan-checker` finding type, and the
confidence framework governing when a fix auto-applies versus escalates.

## Read First

`reference/01-merge-step-guard-and-confidence.md` — the merge-step structural guard MUST be read
before any other reference module. It states what it protects (a merge step's human gate) rather than
enumerating tags/verbs/modes, because two prior enumeration-style guards were each defeated by an
axis nobody had named. Every other reference module's recipes are subordinate to this guard.

## Reference Modules

- `reference/01-merge-step-guard-and-confidence.md` — the merge-step guard (read first), confidence
  assessment, web-research delegation, mode-parameter handling, grilling interaction contract,
  validation strategy.
- `reference/02-content-placement-and-mode-fixes.md` — BRD/PRD content-placement fixes, file-impact
  tree repairs, PR-step/delivery-mode reconciliation, per-repository restriction fixes, Phase 0
  PR/push removal, PR-steps-outside-boundary relocation.
- `reference/03-report-generation-and-confidence-examples.md` — fix-report generation, changed-files
  capture, FALSE_POSITIVE persistence, self-verification, confidence-level domain examples, factual
  accuracy fixes.
- `reference/04-operational-manual-assertion-fixes.md` — operational readiness fixes (5 items),
  manual behavioral assertion fixes (3 items).
- `reference/05-ui-funnel-syllabus-diagram-fixes.md` — UI-design-funnel scaffolding, learning-bearing
  syllabus scaffolding, diagram format fixes (ASCII→Mermaid, under-diagrammed plans).
- `reference/06-worktree-delivery-mode-clarity-fixes.md` — worktree specification fixes, delivery
  mode fixes (including the merge-tag mismatch recipe), execution-grade clarity fixes.
- `reference/07-executor-tag-hallucination-knowledge-fixes.md` — executor-tagging/phase-gate fixes,
  anti-hallucination fixes (AP-1 through AP-10), Knowledge Capture phase scaffolding.

## Core Principles

**Never fabricate — scaffold, don't invent.** Every scaffolding recipe (UI funnel, syllabus,
Knowledge Capture, phase gates) inserts placeholders for the author to fill, never invented content.
**Re-validate before applying.** Every fix confirms the finding still exists (the file may have
changed since audit) before acting. **A more-plausible-sounding hallucination is the worst outcome**
of an anti-hallucination fix — refuse rather than replace one wrong claim with another.

## Related

`plan-validating-quality` (the checker methodology this fixer's recipes repair), `plan-creating-project-plans`
(the authoring templates several recipes insert verbatim), `repo-applying-maker-checker-fixer` (mode
parameter and report discovery mechanics), `repo-assessing-criticality-confidence` (confidence-level
definitions), `repo-generating-validation-reports` (fix report format).
