---
title: "Phase 4 — Backlog Plan Establishment, Phase 5 — Two-Pager Retirement, Phase 6 — Hand-back"
description: Invoking plan-planning to author the backlog plan, atomically retiring the source two-pager, then summarizing the outcome.
when_to_use: Use when authoring the backlog plan itself, deleting the promoted two-pager, or reporting the final result to the user.
---

# Phase 4 — Backlog Plan Establishment, Phase 5 — Two-Pager Retirement, Phase 6 — Hand-back

## 4. Backlog Plan Establishment (Sequential, nested workflow)

Invoke the [plan-planning workflow](../plan-planning.md) with:

- **Input** `target-stage`: `backlog` (lands at `plans/backlog/<identifier>/`, no date prefix).
- **Input** `push-target`: forwarded from this workflow's input.
- **Input** `prompt`: a self-contained handoff containing —
  - the two-pager's full text (problem, why-now, direction sketch, scope & non-goals, risks & open
    questions, success + promotion signal) carried forward verbatim as the plan's seed;
  - a link to the `prior-art-report` plus its key findings, to be folded into the plan's `brd.md` /
    `prd.md` as design input;
  - the Phase 3 decisions (identifier, structure, scope trims);
  - this **Definition of Done** for the plan it must author: the problem, scope, and open questions
    are carried into `brd.md` / `prd.md`; the deep prior-art findings and material alternatives are
    folded in; the plan uses the fixed mature core and one reader-led technical shape; it passes
    `plan-quality-gate` at strict mode.

Because `plan-planning` runs its own grill + research + `plan-maker` + `plan-quality-gate` + push
inside a dedicated worktree, this phase yields a strict-gate-passing backlog plan on the confirmed
target.

**Output**: `plan-path`, `final-status`, `final-report` (from the nested quality gate).

## 5. Two-Pager Retirement (Sequential)

Complete the promotion **move** so the idea now lives as a plan, not as both:

- On the **same branch/worktree** `plan-planning` authored the plan in — before that PR merges, so
  the promotion is **atomic** (the plan appears and the brief disappears together) — `git rm
plans/ideas/<slug>.md` and remove the brief's line from `plans/ideas/README.md`. Commit it as part
  of the plan's changeset.
- If the delivery mode already merged the plan before this step runs, land the deletion as a small
  follow-up commit to the same `push-target`.
- Verify on the target that `plans/ideas/<slug>.md` no longer exists and its README line is gone.

This is step 4 of the convention's promotion procedure. Retiring the brief is **not** optional: a
promoted idea that still sits in `plans/ideas/` is a duplicate.

**Output**: Two-pager deleted and de-indexed on the target.

## 6. Hand-back (Sequential)

Emit a user-visible summary: `plan-path`, the `prior-art-report` path, confirmation that the
two-pager is retired, and `final-status`. Remind the user that the plan is a **proposal in
`backlog/`**; scheduling it is a separate move to `plans/in-progress/` (a pure rename, no date
prefix) followed by the [Plan Execution workflow](../plan-execution.md).
