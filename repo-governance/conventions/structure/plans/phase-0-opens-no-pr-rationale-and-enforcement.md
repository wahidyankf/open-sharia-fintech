---
title: "Phase 0 Opens No PR — Baseline Artifacts, Rationale, and Enforcement"
description: Explains where Phase 0's evidence artifacts land, why opening a Phase 0 PR is prohibited, and how plan-maker, plan-checker, and plan-fixer enforce it.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when a Phase 0 step writes an evidence artifact, or when checking why a Phase 0 PR was flagged as a violation.
---

# Phase 0 Opens No PR — Baseline Artifacts, Rationale, and Enforcement

Continues [Phase 0 Opens No PR — the Earliest PR Is Phase 1](./phase-0-opens-no-pr.md).

**Baseline artifacts ride Phase 1's PR.** When Phase 0 writes evidence files — an `evidence/phase-0-snapshot.txt` baseline record, a slug register, a recorded path constant — those files land in the **first** PR the plan opens, which is the Phase 1 PR. A baseline artifact never justifies a PR of its own.

**Why this is a hard rule**: a PR whose diff is empty, or holds only a baseline text file, still
consumes PR CI and creates branch, merge, and cleanup obligations for no shippable increment. It
also trains executors to treat "phase complete" and "PR merged" as synonyms, which is exactly the
conflation the [Delivery Mode](./delivery-mode-the-four-modes.md#delivery-mode) table prevents.

**A plan whose Phase 0 genuinely produces reviewable changes has a mis-scoped Phase 0**, not an exemption. Move that work into Phase 1 (or a later phase) and leave Phase 0 as setup and baseline only. Splitting the work is always available; opening a Phase 0 PR is not.

**Enforcement**: `plan-maker` never emits a PR-creation, optional semantic-review, PR-CI, or merge
step inside Phase 0. `plan-checker` flags any such step as **HIGH** regardless of delivery mode.
`plan-fixer` removes the offending step and folds any Phase 0 evidence artifact into the Phase 1
PR. `plan-execution-checker` flags a PR actually opened for Phase 0 as **HIGH**.
`repo-setup-manager` carries no push or PR step.
