---
title: "Plans Organization Convention"
description: "Standards for organizing project planning documents in plans/ folder"
when_to_use: "Read this index to find the right Plans Organization Convention child document."
---

# Plans Organization Convention

- [Purpose, Scope, and Overview](./purpose-scope-and-overview.md) — Why the plans/ convention exists, what it covers and excludes, and the high-level lifecycle and no-secrets rule for plan documents.
- [Folder Structure](./folder-structure.md) — The four top-level plans/ subfolders (ideas/, backlog/, in-progress/, done/) and the purpose of each.
- [Ideas Folder (Two-Pagers)](./ideas-folder-overview-rationale-and-file-layout.md) — Capturing a new idea in plans/ideas/ or deciding whether it duplicates an existing two-pager.
- [Two-Pager Template](./two-pager-template.md) — Writing or reviewing the section structure of a plans/ideas/<slug>.md file.
- [Two-Page Discipline and Difference from backlog/](./two-page-discipline-and-difference-from-backlog.md) — A two-pager is growing too detailed or when deciding whether an idea is ready to become a full plan.
- [Promoting a Two-Pager, Ideas as a Home for Learnings, and Worked Examples](./promoting-ideas-and-worked-examples.md) — Promoting a two-pager to backlog/, or filing a learning in ideas/.
- [Plan Folder Naming](./plan-folder-naming.md) — Naming or renaming a plan folder as it moves between lifecycle stages.
- [Structure Decision](./structure-decision.md) — Deciding whether a new plan should use the single-file or multi-file structure.
- [Single-File Structure](./single-file-structure.md) — Authoring a plan that meets all single-file exception criteria.
- [Multi-File Structure](./multi-file-structure-layout-and-core-files.md) — Scaffolding a multi-file plan folder or clarifying what belongs in README.md, brd.md, or prd.md.
- [Additional File Purposes](./multi-file-structure-additional-file-purposes.md) — Clarifying what belongs in tech-docs.md, delivery.md, learnings.md, or evidence/.
- [File-Impact Analysis Format](./file-impact-analysis-format.md) — Writing or reviewing a plan's tech-docs.md File-Impact Analysis section.
- [The Knowledge Capture Phase (Final Phase Before Archival)](./the-knowledge-capture-phase.md) — Authoring or executing a plan's final Knowledge Capture phase before moving it to done/.
- [Content-Placement Rules (brd.md vs prd.md)](./content-placement-rules.md) — Deciding whether a piece of plan content belongs in brd.md or prd.md.
- [Granular Checklist Items in delivery.md](./granular-checklist-items.md) — Writing or reviewing delivery.md checkboxes to check whether an item is too coarse.
- [Execution-Grade Clarity](./execution-grade-clarity.md) — Writing or reviewing a delivery.md checkbox for execution-grade clarity.
- [[AI] vs [HUMAN]](./executor-tagging-tags-and-bias.md) — Deciding whether a delivery.md checkbox should be tagged [AI], [HUMAN], or [AI+HUMAN].
- [Git-Mechanical Steps Are [AI]](./executor-tagging-git-mechanical-steps.md) — Tagging a worktree-provisioning, push, or worktree-removal step in delivery.md.
- [Placement, Legend, and Execution Semantics](./executor-tagging-placement-legend-and-execution-semantics.md) — Adding the executor-tag legend to a delivery.md file or handling a [HUMAN] stop during execution.
- [Phases as Natural Pauses With Clear Gates](./phases-as-natural-pauses.md) — Writing a delivery.md phase's closing gate and Pause Safety note.
- [Delivery Checklists Express a DAG](./delivery-checklists-express-a-dag.md) — Requires a Parallelization Model naming concurrent vs. serial delivery nodes.
- [Delivery Units and Planning Granularity](./delivery-checklists-express-a-dag-continued.md) — Mapping a plan's DAG nodes onto delivery units, branches, and PRs.
- [the Earliest PR Is Phase 1](./phase-0-opens-no-pr.md) — Scoping a plan's Phase 0 to confirm it contains no PR-creation or merge step.
- [Baseline Artifacts, Rationale, and Enforcement](./phase-0-opens-no-pr-rationale-and-enforcement.md) — A Phase 0 step writes evidence, or its PR was flagged.
- [PRs Open at Delivery Boundaries, Not Every Phase](./prs-open-at-delivery-boundaries-rules.md) — Deciding if a phase should open a PR.
- [Rules 5-7 and \*-to-pr Scope](./prs-open-at-delivery-boundaries-rules-continued.md) — Deciding whether independent work may share a PR, or whether an already-open PR may wait for a later merge.
- [Boundary Test and Rationale](./prs-open-at-delivery-boundaries-boundary-test.md) — Testing whether a specific phase qualifies as a delivery boundary.
- [Delivery Boundaries Declaration and Applicability](./delivery-boundaries-and-applicability.md) — Writing a plan's Delivery Boundaries table or checking whether a grandfathered in-progress plan must retrofit gates.
- [Worktree Specification](./worktree-specification.md) — Writing a plan's Worktree section or resolving worktree entry/cleanup.
- [Executor Lifecycle and Example](./worktree-specification-continued.md) — Implementing or auditing worktree entry, sync, and cleanup behavior.
- [One Worktree Per Repository Per Plan](./worktree-cap.md) — A plan produces a second delivery unit in the same repository.
- [Delivery Mode](./delivery-mode-the-four-modes.md) — The four delivery modes (worktree-to-pr, worktree-to-origin-main, main-to-origin-main, main-to-pr), their work location, integration target, and merge authority.
- [main-to-origin-main Content Restriction](./delivery-mode-content-restriction.md) — Deciding whether a plan may select main-to-origin-main as its delivery mode.
- [Merge Authority and Resolution Precedence](./delivery-mode-merge-authority-and-precedence.md) — Determining which delivery mode actually applies to a plan, or when deciding whether a merge step needs an explicit [HUMAN] gate.
- [Per-Repository Delivery Mode Restrictions](./per-repository-delivery-mode-restrictions.md) — Confirming which delivery modes are actually permitted in the specific repository a plan targets.
- [Enforcement and File Naming](./per-repository-restrictions-enforcement-and-file-naming.md) — Checking why main-to-pr is never selected, or when naming a file inside a plan folder.
- [Key Differences from Documentation and Creating Plans](./key-differences-and-creating-plans.md) — Deciding whether new content belongs in plans/ or docs/, or when starting to author a new plan.
- [Starting and Completing Work](./starting-and-completing-work.md) — Moving a plan from backlog/ to in-progress/, or from in-progress/ to done/.
- [Infra-Apply Gate and Plan Index Files](./infra-apply-gate-and-plan-index-files.md) — Why pending infra-apply steps keep a plan in in-progress/, plus each subfolder's index rules.
- [Diagrams in Plans](./diagrams-required.md) — Deciding whether a plan section needs its own Mermaid diagram.
- [Skipping, Accessibility, and Example](./diagrams-skip-accessibility-and-example.md) — A plan is simple enough to consider skipping diagrams, or when applying the accessible color palette to a plan diagram.
- [Relative Link Paths in Plan Files](./relative-link-paths.md) — Three-level `../../../` depth to repo-root files, one level shallower for two-pagers.
- [Related Documentation](./related-documentation.md) — The decision guides, related conventions, and development guides that cross-reference the plans organization convention.
- [Best Practices](./best-practices.md) — Looking for day-to-day working habits for maintaining plan documents over their lifecycle.
- [Examples](./examples.md) — You want a concrete worked example of a single-file plan, a multi-file plan layout, or a two-pager.
