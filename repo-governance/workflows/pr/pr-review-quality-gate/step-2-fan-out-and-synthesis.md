---
title: "PR-Review Quality Gate — Step 2: Fan-Out + Synthesis Pass"
description: "How route-selected specialists fan out concurrently and pr-review-synthesis-maker consolidates their raw findings into exactly ONE posted review, including the standard-route trivial branch."
when_to_use: "Use when checking how the fan-out is dispatched, what the coordinator's output contract is, or how the standard-route trivial tier changes this step."
---

# Step 2 — Per-Cycle Fan-Out + Synthesis Pass

## 2. Per-Cycle Fan-Out + Synthesis Pass (Sequential, Repeats for cycle = 1..N)

- **Agent**: `pr-review-synthesis-maker` (coordinator, fresh state each cycle), fed the raw findings
  from the route-selected subset of the nine discipline specialists (`pr-review-architecture-maker`,
  `pr-review-logic-maker`, `pr-review-governance-maker`, `pr-review-security-maker`,
  `pr-review-integrity-maker`, `pr-review-performance-maker`, `pr-review-docs-maker`,
  `pr-review-instruction-maker`, `pr-review-types-maker`). **The orchestrating workflow performs the
  actual fan-out dispatch** (the Loop Algorithm's `fan_out(scout.specialists, ...)` call), driven by
  Step 1's scout pass, which selects the current route's subset and assembles the shared-context
  brief every selected specialist and the coordinator both read. The coordinator never dispatches
  specialists itself — it only consumes the raw findings they and the scout hand it. Selected
  specialists run **concurrently** within the fan-out
- **Args**: PR reference, pinned head SHA, the `specialists` and `context_brief` outputs from Step 1,
  `prior` consolidated findings and resolution state fed from previous cycles
- **Output**: The route-selected specialists emit raw, discipline-scoped findings to the coordinator;
  the coordinator deduplicates, re-categorizes, reasonableness-filters, and tool-verifies them, then
  posts exactly ONE consolidated review via the GitHub Reviews API (see
  [GitHub Reviews API Mechanics](./github-reviews-api-mechanics-part-1.md) below). The review STATE is always
  `COMMENT` — `REQUEST_CHANGES` is structurally unavailable here; blocking status lives in each
  finding's severity label, never in the review STATE
- **Depends on**: Step 1 (same cycle)
- **Condition**: Runs once per eligible cycle, for `cycle` in `1..={input.cycles}`, stopping at [its clean exit](./probe-variation-and-exit.md)
- **Success criteria**: Every finding surviving to the consolidated review carries confidence ≥ 80,
  cited evidence (blob URL + SHA + line range), and a CRITICAL/HIGH/MEDIUM/LOW severity mapping; the
  review's header records the risk tier, the specialist set fanned out, any diff-slicing applied, and
  the cycle number (N of {input.cycles}) (see the
  [PR Reviewer-Discipline Convention](../../../development/quality/pr-review-disciplines.md))
- **On failure**: If a specialist or the coordinator cannot access the PR or an API call fails, retry
  once and record the blocked condition; do not silently suppress the affected lens.
- **Standard-route trivial branch**: when Step 1 records a non-plans-only `tier: trivial` route,
  `specialists` is empty and there is no fan-out to dispatch. `pr-review-synthesis-maker` instead performs one consolidated generalist
  pass over the full PR context itself, originating the findings that in every other tier the
  specialists would have raised, then runs the same four coordination functions and posts the same
  single consolidated review. This is the sole condition under which the coordinator originates a
  finding no specialist raised (see the carve-out in
  [`pr-review-synthesis-maker.md`](../../../../.claude/agents/pr-review/pr-review-synthesis-maker.md)).
