---
title: "Plans Organization Convention"
description: "Standards for organizing project planning documents in plans/ folder"
when_to_use: "Read this index to find the right Plans Organization Convention child document."
---

# Plans Organization Convention

- [Purpose, Scope, and Overview](./01-purpose-scope-and-overview.md) — Explains why the plans/ convention exists, what it covers
- [Folder Structure](./02-folder-structure.md) — Describes the four top-level plans/ subfolders (ideas/, backlog/, in-progress/,
- [Ideas Folder (Two-Pagers)](./03-ideas-folder-overview-rationale-and-file-layout.md) — Defines the two-pager idea-brief format, why it exists between
- [Two-Pager Template](./04-two-pager-template.md) — Specifies the eight required sections of a two-pager idea
- [Two-Page Discipline and Difference from backlog/](./05-two-page-discipline-and-difference-from-backlog.md) — States the length- and rigor-discipline rules that keep a
- [Promoting a Two-Pager, Ideas as a Home for Learnings, and Worked Examples](./06-promoting-ideas-and-worked-examples.md) — Explains the four-step promotion of a ripe two-pager into
- [Plan Folder Naming](./07-plan-folder-naming.md) — Defines the stage-aware folder naming rules for backlog/, in-progress/,
- [Structure Decision](./08-structure-decision.md) — States the no-secrets rule for plan content and the
- [Single-File Structure](./09-single-file-structure.md) — Specifies the mandatory section order for a single-file README.md
- [Multi-File Structure](./10-multi-file-structure-layout-and-core-files.md) — Shows the five-document plan folder layout and defines the
- [Multi-File Structure — Additional File Purposes](./11-multi-file-structure-additional-file-purposes.md) — Defines the purpose of tech-docs.md, delivery.md, learnings.md, and the
- [File-Impact Analysis Format (HARD RULE)](./12-file-impact-analysis-format.md) — Specifies the required annotated file-tree format for a plan's
- [The Knowledge Capture Phase (Final Phase Before Archival)](./13-the-knowledge-capture-phase.md) — Requires every substantive plan's delivery.md to end with a
- [Content-Placement Rules (brd.md vs prd.md)](./14-content-placement-rules.md) — Gives the authoritative split of which content belongs in
- [Granular Checklist Items in delivery.md](./15-granular-checklist-items.md) — States the one-checkbox-one-action rule for delivery.md and shows a
- [Execution-Grade Clarity (HARD RULE)](./16-execution-grade-clarity.md) — Lists what every delivery.md checkbox must contain — explicit
- [Executor Tagging — [AI] vs [HUMAN] (HARD RULE)](./17-executor-tagging-tags-and-bias.md) — Defines the [AI]/[HUMAN]/[AI+HUMAN] executor tags and the hard-rule bias
- [Executor Tagging — Git-Mechanical Steps Are [AI]](./18-executor-tagging-git-mechanical-steps.md) — States that worktree creation, commit-and-push, and worktree removal are
- [Executor Tagging — Placement, Legend, and Execution Semantics](./19-executor-tagging-placement-legend-and-execution-semantics.md) — Covers the fourth PR-merge step's default [AI] tagging, where
- [Phases as Natural Pauses With Clear Gates (HARD RULE)](./20-phases-as-natural-pauses.md) — Requires every delivery phase to end in a coherent
- [Delivery Checklists Express a DAG (HARD RULE)](./21-delivery-checklists-express-a-dag.md) — Requires a Parallelization Model naming concurrent vs.
- [Delivery Checklists Express a DAG — Delivery Units and Planning Granularity](./22-delivery-checklists-express-a-dag-continued.md) — Explains how each independent DAG node that produces changes
- [Phase 0 Opens No PR — the Earliest PR Is Phase 1 (HARD RULE)](./23-phase-0-opens-no-pr.md) — States that Phase 0 (environment setup and baseline) never
- [Phase 0 Opens No PR — Baseline Artifacts, Rationale, and Enforcement](./24-phase-0-opens-no-pr-rationale-and-enforcement.md) — Explains where Phase 0's evidence artifacts land, why opening
- [PRs Open at Delivery Boundaries, Not Every Phase (HARD RULE)](./25-prs-open-at-delivery-boundaries-rules.md) — States the first four of seven rules for when
- [PRs Open at Delivery Boundaries — Rules 5-7 and \*-to-pr Scope](./26-prs-open-at-delivery-boundaries-rules-continued.md) — Gives the remaining three PR-boundary rules (independent nodes deliver
- [PRs Open at Delivery Boundaries — Boundary Test and Rationale](./27-prs-open-at-delivery-boundaries-boundary-test.md) — Gives the four-part boundary test (coherent, green standalone, defensible
- [Delivery Boundaries Declaration and Applicability](./28-delivery-boundaries-and-applicability.md) — Shows the required Delivery Boundaries table format mapping phases
- [Worktree Specification](./29-worktree-specification.md) — Defines where a plan declares its worktree path and
- [Worktree Specification — Executor Lifecycle and Example](./30-worktree-specification-continued.md) — Defines the executor's enter/sync/cleanup lifecycle for a plan's worktree
- [Worktree Cap — One Worktree Per Repository Per Plan (HARD RULE)](./31-worktree-cap.md) — Caps a plan to at most one worktree per
- [Delivery Mode](./32-delivery-mode-the-four-modes.md) — Introduces the four delivery modes (worktree-to-pr, worktree-to-origin-main, main-to-origin-main, main-to-pr),
- [Delivery Mode — main-to-origin-main Content Restriction](./33-delivery-mode-content-restriction.md) — States the two-condition test (.md-only changes or explicit standing
- [Delivery Mode — Merge Authority and Resolution Precedence](./34-delivery-mode-merge-authority-and-precedence.md) — Explains the default [AI]-merges-by-default policy, when a plan should
- [Per-Repository Delivery Mode Restrictions (HARD RULE)](./35-per-repository-delivery-mode-restrictions.md) — States which delivery modes are actually available in ose-public
- [Per-Repository Delivery Mode Restrictions — Enforcement and File Naming](./36-per-repository-restrictions-enforcement-and-file-naming.md) — States that main-to-pr is unused despite being technically available,
- [Key Differences from Documentation and Creating Plans](./37-key-differences-and-creating-plans.md) — Contrasts plans/ against docs/ across location, purpose, and lifecycle,
- [Starting and Completing Work](./38-starting-and-completing-work.md) — Details the steps to promote a plan from backlog/
- [Infra-Apply Gate and Plan Index Files](./39-infra-apply-gate-and-plan-index-files.md) — States that a plan with pending infrastructure-apply steps must
- [Diagrams in Plans](./40-diagrams-required.md) — Requires Mermaid as the primary diagram format in plans/
- [Diagrams in Plans — Skipping, Accessibility, and Example](./41-diagrams-skip-accessibility-and-example.md) — States when a plan may skip diagrams, the color-blind-safe
- [Relative Link Paths in Plan Files](./42-relative-link-paths.md) — Explains the three-level ../../../ relative-path depth for links from
- [Related Documentation](./43-related-documentation.md) — Lists the decision guides, related conventions, and development guides
- [Best Practices](./44-best-practices.md) — Gives working habits for plans - never put secrets
- [Examples](./45-examples.md) — Shows a complete worked single-file plan, a multi-file plan's
