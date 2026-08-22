---
title: "Plans Organization Convention"
description: Standards for organizing project planning documents in plans/ folder
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when deciding where a plan document belongs, how to name/structure it, or how it moves through the lifecycle.
---

# Plans Organization Convention

<!--
  MAINTENANCE NOTE: Master reference for plans organization
  This convention is referenced by:
  1. plans/README.md (brief landing page with link to this convention)
  2. AGENTS.md (summary with link to this convention)
  3. .claude/agents/plan/plan-maker.md (reference to this convention)
  When updating, ensure all references remain accurate.
-->

Standards for organizing planning documents in `plans/` — temporary, distinct from `docs/`.

## Foundations

- [Purpose, Scope, and Overview](./plans/purpose-scope-and-overview.md) — why this exists.
- [Folder Structure](./plans/folder-structure.md) — the four subfolders.

## Ideas Folder (Two-Pagers)

- [Ideas Folder (Two-Pagers)](./plans/ideas-folder-overview-rationale-and-file-layout.md) — rationale, layout.
- [Two-Pager Template](./plans/two-pager-template.md) — the eight sections.
- [Two-Page Discipline and Difference from backlog/](./plans/two-page-discipline-and-difference-from-backlog.md) — length rules.
- [Promoting Ideas and Worked Examples](./plans/promoting-ideas-and-worked-examples.md) — promotion.

## Plan Folder Naming

- [Plan Folder Naming](./plans/plan-folder-naming.md) — stage-aware naming.

## Plan Contents

- [Structure Decision](./plans/structure-decision.md) — single- vs. multi-file.
- [Single-File Structure](./plans/single-file-structure.md) — exception layout.
- [Multi-File Structure](./plans/multi-file-structure-layout-and-core-files.md) — README/brd/prd.
- [Multi-File — Additional Files](./plans/multi-file-structure-additional-file-purposes.md) — remaining.
- [File-Impact Analysis Format](./plans/file-impact-analysis-format.md) — annotated file tree.
- [The Knowledge Capture Phase](./plans/the-knowledge-capture-phase.md) — final phase.
- [Content-Placement Rules](./plans/content-placement-rules.md) — brd vs prd.
- [Granular Checklist Items](./plans/granular-checklist-items.md) — one action.
- [Execution-Grade Clarity](./plans/execution-grade-clarity.md) — checkbox rules.
- [Executor Tagging — Tags and Bias](./plans/executor-tagging-tags-and-bias.md) — [AI]/[HUMAN] tags.
- [Tagging — Git-Mechanical Steps](./plans/executor-tagging-git-mechanical-steps.md) — worktree/push.
- [Executor Tagging — Placement and Legend](./plans/executor-tagging-placement-legend-and-execution-semantics.md) — legend.
- [Phases as Natural Pauses](./plans/phases-as-natural-pauses.md) — gates.
- [Delivery Checklists Express a DAG](./plans/delivery-checklists-express-a-dag.md) — parallelization.
- [Delivery Units and Granularity](./plans/delivery-checklists-express-a-dag-continued.md) — units.
- [Phase 0 Opens No PR](./plans/phase-0-opens-no-pr.md) — no PR at setup.
- [Phase 0 — Rationale and Enforcement](./plans/phase-0-opens-no-pr-rationale-and-enforcement.md) — evidence.
- [PRs Open at Delivery Boundaries — Rules](./plans/prs-open-at-delivery-boundaries-rules.md) — rules 1-4.
- [PRs Open — Rules 5-7](./plans/prs-open-at-delivery-boundaries-rules-continued.md) — remaining rules.
- [PRs Open — Boundary Test](./plans/prs-open-at-delivery-boundaries-boundary-test.md) — the test.
- [PRs Open — PR Size](./plans/prs-open-at-delivery-boundaries-pr-size.md) — size bound.
- [PRs Open — PR Body](./plans/prs-open-at-delivery-boundaries-pr-body.md) — why, entry, skip.
- [Delivery Boundaries and Applicability](./plans/delivery-boundaries-and-applicability.md) — table.
- [Worktree Specification](./plans/worktree-specification.md) — declaring worktree.
- [Worktree Specification — Lifecycle](./plans/worktree-specification-continued.md) — cleanup.
- [Worktree Cap](./plans/worktree-cap.md) — one per repo.
- [Delivery Mode — The Four Modes](./plans/delivery-mode-the-four-modes.md) — mode table.
- [Delivery Mode — Content Restriction](./plans/delivery-mode-content-restriction.md) — validity.
- [Merge Authority](./plans/delivery-mode-merge-authority-and-precedence.md) — resolution.
- [Per-Repository Delivery Mode Restrictions](./plans/per-repository-delivery-mode-restrictions.md) — per-repo.
- [Per-Repo Restrictions — Enforcement](./plans/per-repository-restrictions-enforcement-and-file-naming.md) — enforces.

## Working with Plans

- [Key Differences and Creating Plans](./plans/key-differences-and-creating-plans.md) — plans/ vs. docs/.
- [Starting and Completing Work](./plans/starting-and-completing-work.md) — lifecycle moves.
- [Infra-Apply Gate and Indexes](./plans/infra-apply-gate-and-plan-index-files.md) — infra hold.

## Diagrams, Links, and Reference

- [Diagrams in Plans](./plans/diagrams-required.md) — Mermaid requirement.
- [Diagrams — Skipping and Accessibility](./plans/diagrams-skip-accessibility-and-example.md) — escape hatch.
- [Relative Link Paths in Plan Files](./plans/relative-link-paths.md) — depth rule.
- [Related Documentation](./plans/related-documentation.md) — cross-references.
- [Best Practices](./plans/best-practices.md) — working habits.
- [Examples](./plans/examples.md) — worked examples.
