---
name: plan-creating-project-plans
description: Comprehensive project planning standards for plans/ directory including folder structure (ideas/, backlog/, in-progress/, done/), stage-aware naming convention (done uses YYYY-MM-DD__identifier/; backlog and in-progress use identifier/ with no date prefix), five-document file organization (README.md, brd.md, prd.md, tech-docs.md, delivery.md for multi-file default; single README.md for trivially-small single-file exception), BRD/PRD content-placement rules, Gherkin acceptance criteria, and the mandatory structured multiple-choice grilling gates (pre-write and post-write) for resolving design decisions with the user. Essential for creating structured, executable project plans.
---

# Creating Project Plans

## Purpose

This Skill provides comprehensive guidance for creating **structured project plans** in the plans/ directory. Plans follow standardized organization, naming conventions, and acceptance criteria patterns for executable, traceable project work.

**When to use this Skill:**

- Creating new project plans
- Organizing backlog items
- Converting ideas to structured plans
- Writing Gherkin acceptance criteria
- Structuring multi-phase projects
- Moving plans through workflow stages

**Start here — mandatory grilling**: before writing any plan content, resolve every open design
decision through a structured multiple-choice pre-write grill; after writing, run the same
post-write validation grill. Neither gate is optional. See
[mandatory-grilling.md](reference/mandatory-grilling.md).

## Reference Modules

- [mandatory-grilling.md](reference/mandatory-grilling.md) — pre/post-write grilling (2-4 options HARD RULE)
- [plan-lifecycle-and-git-workflow.md](reference/plan-lifecycle-and-git-workflow.md) — 4-stage lifecycle + git workflow
- [plan-folder-and-naming.md](reference/plan-folder-and-naming.md) — `plans/` folder layout + stage-aware naming
- [plan-structure-multi-and-single-file.md](reference/plan-structure-multi-and-single-file.md) — five-document structure vs. single-file exception
- [mermaid-diagrams.md](reference/mermaid-diagrams.md) — Mermaid diagram requirements
- [ui-design-funnel.md](reference/ui-design-funnel.md) — UI-design-funnel HARD RULE (diverge→narrow→select→justify)
- [ui-design-funnel-grilling-and-learning-plans.md](reference/ui-design-funnel-grilling-and-learning-plans.md) — funnel grilling questions + Learning-Bearing syllabus record
- [worktree-specification.md](reference/worktree-specification.md) — mandatory `## Worktree` declaration
- [delivery-mode.md](reference/delivery-mode.md) — the four Delivery Modes + per-repo restriction
- [execution-grade-clarity.md](reference/execution-grade-clarity.md) — Execution-Grade Clarity HARD RULE
- [executor-tagging.md](reference/executor-tagging.md) — `[AI]`/`[HUMAN]` tagging HARD RULE
- [phases-as-natural-pauses.md](reference/phases-as-natural-pauses.md) — Phase-Gate + Pause-Safety template
- [verification-recipes.md](reference/verification-recipes.md) — pre-write verification recipes + confidence labels
- [refuse-uncertainty-and-anti-patterns.md](reference/refuse-uncertainty-and-anti-patterns.md) — refuse-on-uncertainty + AP-1..AP-10 catalog
- [specialized-executor-annotation.md](reference/specialized-executor-annotation.md) — suggested-executor annotation
- [gherkin-acceptance-criteria.md](reference/gherkin-acceptance-criteria.md) — Gherkin format + Step-Keyword Cardinality
- [delivery-plan-tdd-structure.md](reference/delivery-plan-tdd-structure.md) — RED/GREEN/REFACTOR checkbox shape
- [operational-readiness.md](reference/operational-readiness.md) — Local Quality Gates, Post-Push, Env Setup, Commits
- [manual-ui-and-api-verification.md](reference/manual-ui-and-api-verification.md) — Playwright/curl manual verification
- [manual-verification-retest-rules.md](reference/manual-verification-retest-rules.md) — rule-15/rule-16 pre-archival retests
- [knowledge-capture-scaffold-and-entries.md](reference/knowledge-capture-scaffold-and-entries.md) — `learnings.md` scaffold + entry shape
- [knowledge-capture-phase-template.md](reference/knowledge-capture-phase-template.md) — Knowledge Capture phase template
- [plan-archival.md](reference/plan-archival.md) — Plan Archival section template
- [common-mistakes.md](reference/common-mistakes.md) — 5 common authoring mistakes

## References

**Primary Convention**: [Plans Organization Convention](../../../repo-governance/conventions/structure/plans.md)

**Related Skills**: `grill-me`, `plan-writing-gherkin-criteria`, `repo-practicing-trunk-based-development`, `docs-applying-content-quality`.
