---
title: "Plans Organization Convention"
description: "Standards for organizing project planning documents in plans/ folder"
when_to_use: "Read this index to find the right Plans Organization Convention child document."
---

# Plans Organization Convention

- [Purpose, Scope, and Overview](./01-purpose-scope-and-overview.md) — Orienting to why plans/ is organized the way it is.
- [Folder Structure](./02-folder-structure.md) — The four top-level plans/ subfolders (ideas/, backlog/, in-progress/, done/) and the purpose of each.
- [Ideas Folder (Two-Pagers)](./03-ideas-folder-overview-rationale-and-file-layout.md) — Capturing a new idea in plans/ideas/ or deciding whether it duplicates an existing two-pager.
- [Two-Pager Template](./04-two-pager-template.md) — Writing or reviewing the section structure of a plans/ideas/<slug>.md file.
- [Two-Page Discipline and Difference from backlog/](./05-two-page-discipline-and-difference-from-backlog.md) — The length- and rigor-discipline rules that keep a two-pager short.
- [Promoting a Two-Pager](./06-promoting-ideas-and-worked-examples.md) — Promoting a two-pager to a backlog/ plan or routing a plan-execution learning into the ideas folder.
- [Plan Folder Naming](./07-plan-folder-naming.md) — Naming or renaming a plan folder as it moves between lifecycle stages.
- [Structure Decision](./08-structure-decision.md) — Deciding whether a new plan should use the single-file or multi-file structure.
- [Single-File Structure](./09-single-file-structure.md) — Authoring a plan that meets all single-file exception criteria.
- [Multi-File Structure](./10-multi-file-structure-layout-and-core-files.md) — Scaffolding a multi-file plan folder or clarifying what belongs in README.md, brd.md, or prd.md.
- [Additional File Purposes](./11-multi-file-structure-additional-file-purposes.md) — Clarifying what belongs in tech-docs.md, delivery.md, learnings.md, or evidence/.
- [File-Impact Analysis Format](./12-file-impact-analysis-format.md) — Writing or reviewing a plan's tech-docs.md File-Impact Analysis section.
- [The Knowledge Capture Phase (Final Phase Before Archival)](./13-the-knowledge-capture-phase.md) — Authoring or executing a plan's final Knowledge Capture phase before moving it to done/.
- [Content-Placement Rules (brd.md vs prd.md)](./14-content-placement-rules.md) — The authoritative split of which content belongs in brd.md versus prd.md.
- [Granular Checklist Items in delivery.md](./15-granular-checklist-items.md) — Writing or reviewing delivery.md checkboxes to check whether an item is too coarse.
- [Execution-Grade Clarity](./16-execution-grade-clarity.md) — Writing or reviewing a delivery.md checkbox for execution-grade clarity.
- [[AI] vs [HUMAN]](./17-executor-tagging-tags-and-bias.md) — Deciding whether a delivery.md checkbox should be tagged [AI], [HUMAN], or [AI+HUMAN].
- [Git-Mechanical Steps Are [AI]](./18-executor-tagging-git-mechanical-steps.md) — Tagging a worktree-provisioning, push, or worktree-removal step in delivery.md.
- [Placement, Legend, and Execution Semantics](./19-executor-tagging-placement-legend-and-execution-semantics.md) — Adding the executor-tag legend to a delivery.md file or handling a [HUMAN] stop during execution.
- [Phases as Natural Pauses With Clear Gates](./20-phases-as-natural-pauses.md) — Writing a delivery.md phase's closing gate and Pause Safety note.
- [Delivery Checklists Express a DAG](./21-delivery-checklists-express-a-dag.md) — Requires a Parallelization Model naming concurrent vs. serial delivery nodes.
- [Delivery Units and Planning Granularity](./22-delivery-checklists-express-a-dag-continued.md) — Mapping a plan's DAG nodes onto delivery units, branches, and PRs.
- [the Earliest PR Is Phase 1](./23-phase-0-opens-no-pr.md) — Scoping a plan's Phase 0 to confirm it contains no PR-creation or merge step.
- [Baseline Artifacts, Rationale, and Enforcement](./24-phase-0-opens-no-pr-rationale-and-enforcement.md) — A Phase 0 step writes an evidence artifact.
- [PRs Open at Delivery Boundaries](./25-prs-open-at-delivery-boundaries-rules.md) — Deciding if a phase should open a PR.
- [Rules 5-7 and \*-to-pr Scope](./26-prs-open-at-delivery-boundaries-rules-continued.md) — Deciding whether independent work may share a PR, or whether an already-open PR may wait for a later merge.
- [Boundary Test and Rationale](./27-prs-open-at-delivery-boundaries-boundary-test.md) — Testing whether a specific phase qualifies as a delivery boundary.
- [Delivery Boundaries Declaration and Applicability](./28-delivery-boundaries-and-applicability.md) — Shows the required Delivery Boundaries table format mapping phases to delivery units.
- [Worktree Specification](./29-worktree-specification.md) — Writing a plan's Worktree section or resolving worktree entry/cleanup.
- [Executor Lifecycle and Example](./30-worktree-specification-continued.md) — Implementing or auditing worktree entry, sync, and cleanup behavior.
- [One Worktree Per Repository Per Plan](./31-worktree-cap.md) — Caps a plan to at most one worktree per repository, reused across every delivery unit landed there.
- [Delivery Mode](./32-delivery-mode-the-four-modes.md) — The four delivery modes (worktree-to-pr, worktree-to-origin-main, main-to-origin-main, main-to-pr), their work location, integration target, and merge authority.
- [main-to-origin-main Content Restriction](./33-delivery-mode-content-restriction.md) — Deciding whether a plan may select main-to-origin-main as its delivery mode.
- [Merge Authority and Resolution Precedence](./34-delivery-mode-merge-authority-and-precedence.md) — Determining which delivery mode actually applies to a plan.
- [Per-Repository Delivery Mode Restrictions](./35-per-repository-delivery-mode-restrictions.md) — Confirming which delivery modes are actually permitted in the specific repository a plan targets.
- [Enforcement and File Naming](./36-per-repository-restrictions-enforcement-and-file-naming.md) — Checking why main-to-pr is never selected, or when naming a file inside a plan folder.
- [Key Differences from Documentation](./37-key-differences-and-creating-plans.md) — Contrasts plans/ against docs/ across location, purpose, and lifecycle.
- [Starting and Completing Work](./38-starting-and-completing-work.md) — Moving a plan from backlog/ to in-progress/, or from in-progress/ to done/.
- [Infra-Apply Gate and Plan Index Files](./39-infra-apply-gate-and-plan-index-files.md) — That a plan with pending infrastructure-apply steps must stay in in-progress/.
- [Diagrams in Plans](./40-diagrams-required.md) — Deciding whether a plan section needs its own Mermaid diagram.
- [Skipping, Accessibility, and Example](./41-diagrams-skip-accessibility-and-example.md) — A plan is simple enough to consider skipping diagrams.
- [Relative Link Paths in Plan Files](./42-relative-link-paths.md) — The three-level ../../../ relative-path depth for links from a plan file to repo-root directories.
- [Related Documentation](./43-related-documentation.md) — The decision guides, related conventions, and development guides that cross-reference the plans organization convention.
- [Best Practices](./44-best-practices.md) — Looking for day-to-day working habits for maintaining plan documents over their lifecycle.
- [Examples](./45-examples.md) — You want a concrete worked example of a single-file plan, a multi-file plan layout, or a two-pager.
