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

Standards for organizing planning documents in `plans/` — temporary, distinct from `docs/`. Covers folder structure, naming, plan-content rules, worktree/delivery-mode mechanics, and diagramming/linking standards below.

## Foundations

- [Purpose, Scope, and Overview](./plans/01-purpose-scope-and-overview.md) — why this exists.
- [Folder Structure](./plans/02-folder-structure.md) — the four subfolders.

## Ideas Folder (Two-Pagers)

- [Ideas Folder (Two-Pagers)](./plans/03-ideas-folder-overview-rationale-and-file-layout.md) — rationale, layout.
- [Two-Pager Template](./plans/04-two-pager-template.md) — the eight sections.
- [Two-Page Discipline and Difference from backlog/](./plans/05-two-page-discipline-and-difference-from-backlog.md) — length rules.
- [Promoting Ideas and Worked Examples](./plans/06-promoting-ideas-and-worked-examples.md) — promotion.

## Plan Folder Naming

- [Plan Folder Naming](./plans/07-plan-folder-naming.md) — stage-aware naming.

## Plan Contents

- [Structure Decision](./plans/08-structure-decision.md) — single- vs. multi-file.
- [Single-File Structure](./plans/09-single-file-structure.md) — exception layout.
- [Multi-File Structure](./plans/10-multi-file-structure-layout-and-core-files.md) — README/brd/prd.
- [Multi-File Structure — Additional Files](./plans/11-multi-file-structure-additional-file-purposes.md) — remaining.
- [File-Impact Analysis Format](./plans/12-file-impact-analysis-format.md) — annotated file tree.
- [The Knowledge Capture Phase](./plans/13-the-knowledge-capture-phase.md) — final phase.
- [Content-Placement Rules](./plans/14-content-placement-rules.md) — brd vs prd.
- [Granular Checklist Items](./plans/15-granular-checklist-items.md) — one action.
- [Execution-Grade Clarity](./plans/16-execution-grade-clarity.md) — checkbox rules.
- [Executor Tagging — Tags and Bias](./plans/17-executor-tagging-tags-and-bias.md) — [AI]/[HUMAN] tags.
- [Executor Tagging — Git-Mechanical Steps](./plans/18-executor-tagging-git-mechanical-steps.md) — worktree/push.
- [Executor Tagging — Placement, Legend, Semantics](./plans/19-executor-tagging-placement-legend-and-execution-semantics.md) — legend.
- [Phases as Natural Pauses](./plans/20-phases-as-natural-pauses.md) — gates.
- [Delivery Checklists Express a DAG](./plans/21-delivery-checklists-express-a-dag.md) — parallelization.
- [Delivery Checklists — Units and Granularity](./plans/22-delivery-checklists-express-a-dag-continued.md) — units.
- [Phase 0 Opens No PR](./plans/23-phase-0-opens-no-pr.md) — no PR at setup.
- [Phase 0 — Rationale and Enforcement](./plans/24-phase-0-opens-no-pr-rationale-and-enforcement.md) — evidence.
- [PRs Open at Delivery Boundaries — Rules](./plans/25-prs-open-at-delivery-boundaries-rules.md) — rules 1-4.
- [PRs Open — Rules 5-7](./plans/26-prs-open-at-delivery-boundaries-rules-continued.md) — remaining rules.
- [PRs Open — Boundary Test](./plans/27-prs-open-at-delivery-boundaries-boundary-test.md) — the test.
- [Delivery Boundaries and Applicability](./plans/28-delivery-boundaries-and-applicability.md) — table.
- [Worktree Specification](./plans/29-worktree-specification.md) — declaring worktree.
- [Worktree Specification — Lifecycle](./plans/30-worktree-specification-continued.md) — cleanup.
- [Worktree Cap](./plans/31-worktree-cap.md) — one per repo.
- [Delivery Mode — The Four Modes](./plans/32-delivery-mode-the-four-modes.md) — mode table.
- [Delivery Mode — Content Restriction](./plans/33-delivery-mode-content-restriction.md) — validity.
- [Delivery Mode — Merge Authority](./plans/34-delivery-mode-merge-authority-and-precedence.md) — resolution.
- [Per-Repository Delivery Mode Restrictions](./plans/35-per-repository-delivery-mode-restrictions.md) — per-repo.
- [Per-Repository Restrictions — Enforcement](./plans/36-per-repository-restrictions-enforcement-and-file-naming.md) — enforces.

## Working with Plans

- [Key Differences and Creating Plans](./plans/37-key-differences-and-creating-plans.md) — plans/ vs. docs/.
- [Starting and Completing Work](./plans/38-starting-and-completing-work.md) — lifecycle moves.
- [Infra-Apply Gate and Plan Index Files](./plans/39-infra-apply-gate-and-plan-index-files.md) — infra hold.

## Diagrams, Links, and Reference

- [Diagrams in Plans](./plans/40-diagrams-required.md) — Mermaid requirement.
- [Diagrams — Skipping, Accessibility, Example](./plans/41-diagrams-skip-accessibility-and-example.md) — escape hatch.
- [Relative Link Paths in Plan Files](./plans/42-relative-link-paths.md) — depth rule.
- [Related Documentation](./plans/43-related-documentation.md) — cross-references.
- [Best Practices](./plans/44-best-practices.md) — working habits.
- [Examples](./plans/45-examples.md) — worked examples.
