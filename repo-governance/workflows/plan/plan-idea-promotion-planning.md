---
name: plan-idea-promotion-planning
title: "plan-idea-promotion-planning"
description: Promotes one ripe two-pager idea brief into a full five-document backlog plan, gated, researched, and retired atomically.
when_to_use: Use when a two-pager in plans/ideas/ has matured and should become a scheduled backlog plan.
goal: >
  Promote one ripe two-pager idea brief from plans/ideas/ into a full five-document backlog plan at
  plans/backlog/<identifier>/: gate the brief for completeness, run the deep prior-art study the
  capture phase deferred, then hand the enriched brief to plan-planning (target-stage=backlog) and
  retire the two-pager. The deliverable is the backlog plan, never any implementation.
termination: >
  Either (a) a grill-validated plan exists at plans/backlog/<identifier>/, passes plan-quality-gate
  at strict mode, is pushed to the confirmed target, and the source two-pager is deleted and removed
  from plans/ideas/README.md — promotion is atomic; or (b) the brief is judged not-yet-ripe, a
  readiness report naming the gaps is emitted, and NO plan is created (the legitimate "not promoted
  yet" state). No application or library code is modified either way.
inputs:
  - name: two-pager
    type: string
    description: >
      The idea brief to promote — a slug (e.g. `iam-service-module`) or a path under `plans/ideas/`.
      Must resolve to an existing `plans/ideas/<slug>.md` two-pager (not the folder README).
    required: true
  - name: plan-identifier
    type: string
    description: >
      Slug for the backlog plan folder at plans/backlog/<identifier>/. Defaults to the two-pager's
      own slug, so the idea keeps its name as it becomes a plan.
    required: false
  - name: push-target
    type: string
    description: "Git push destination for the backlog plan. Forwarded to plan-planning."
    required: false
    default: "origin main"
outputs:
  - name: prior-art-report
    type: file
    pattern: generated-reports/plan-idea-promotion-planning__*__report.md
    description: >
      The deep prior-art survey (precedents, standards, existing solutions) produced in Phase 2 and
      folded into the plan's brd.md / prd.md. Written whenever the brief passes the ripeness gate.
  - name: readiness-report
    type: file
    pattern: generated-reports/plan-idea-promotion-planning__*__readiness.md
    description: >
      Section-by-section completeness verdict. Written whenever the brief FAILS the ripeness gate,
      naming exactly which sections are stubs so the author can enrich the brief and retry.
  - name: plan-path
    type: string
    description: Path to the created backlog plan at plans/backlog/<identifier>/ (ripe path only).
  - name: final-status
    type: enum
    values: [pass, partial, fail, not-ripe]
    description: >
      Final status. `not-ripe` when the brief failed the completeness gate and no plan was authored;
      otherwise the status of the backlog plan's quality gate.
---

# Plan Idea Promotion Planning Workflow

Turns one ripe two-pager into a full five-document backlog plan: gates it for completeness, runs the
deferred deep prior-art study, hands it to `plan-planning`, and retires the source two-pager.

## Contents

- [Purpose, Execution Mode, and When to Use](./plan-idea-promotion-planning/purpose-execution-mode-and-when-to-use.md) — what it does, who runs it.
- [Phase 0 and Phase 1](./plan-idea-promotion-planning/phase-0-pre-flight-and-phase-1-ripeness-gate.md) — pre-flight, then the ripeness gate.
- [Phase 2 and Phase 3](./plan-idea-promotion-planning/phase-2-prior-art-and-phase-3-promotion-checkpoint.md) — prior-art study, then the checkpoint.
- [Phases 4-6](./plan-idea-promotion-planning/phases-4-6-establishment-retirement-and-hand-back.md) — plan authoring, retirement, hand-back.
- [Gherkin and Related Documents](./plan-idea-promotion-planning/gherkin-success-criteria-and-related-documents.md) — acceptance scenarios, cross-references.
- [Principles and Conventions](./plan-idea-promotion-planning/principles-and-conventions.md) — governance this workflow implements.
