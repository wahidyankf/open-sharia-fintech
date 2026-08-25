---
title: "PR-Review Quality Gate — Steps 0-1: Classify and Scout Pass"
description: "Step 0 (classify the PR and resolve loop inputs) and Step 1 (the per-cycle scout pass that produces risk tier, specialist set, and shared-context brief)."
when_to_use: "Use when checking the args/outputs/success criteria for the classification step or the per-cycle scout step."
---

# Steps 0-1 — Classify the PR and Per-Cycle Scout Pass

## 0. Classify the PR and Resolve Loop Inputs (Sequential)

- **Agent**: Orchestrator (the caller — `plan-execution.md` Step 8, or a direct invocation)
- **Args**: `{input.pr}`, `{input.cycles}` (default maximum 7)
- **Output**: Confirmed PR reference, behavior classification, classification evidence, maximum
  cycle count when eligible, and a reader-facing review-route record in the PR body before fan-out
- **Success criteria**: The PR exists and is open; the classifier has recorded `eligible` or
  `noneligible`; `cycles` is a positive integer no greater than 5 unless the caller explicitly
  authorizes a different ceiling
- **Route**: A noneligible PR skips Steps 1–3 and proceeds to the `pr-quality-gate.yml` verification
  in Step 4. An eligible PR proceeds through the loop.

Before specialist fan-out, the coordinator records the current base/head and diff scope, plain-language
risk tier, review route, selected specialists and safely skipped specialists with their reasons, current check
evidence, settled review history, the frozen outcome, and this cycle's changed probe in the PR
body. This is a human-readable audit aid, not a new classifier or mechanical gate.

## 1. Per-Cycle Scout Pass (Sequential, Repeats for cycle = 1..N)

- **Agent**: `pr-review-scout-maker` (fresh state each cycle)
- **Args**: PR reference, `prior` state (prior-cycle thread-resolution/dismissal state)
- **Output**: Pinned head SHA, risk tier, review route, route-selected specialist set,
  shared-context brief, dismissal state
- **Depends on**: Step 0 (cycle 1); the previous cycle's CI-green gate (cycle > 1)
- **Condition**: Runs once per eligible cycle, for `cycle` in `1..={input.cycles}`, stopping at [its clean exit](./probe-variation-and-exit.md)
- **Success criteria**: `tier` is exactly one of `trivial`/`lite`/`full`; the current route and its
  selected set are recorded for the header
- **On failure**: If the scout cannot access the PR or an API call fails, retry once and record the
  blocked condition. Do not relabel the PR noneligible merely because classification evidence is
  unavailable.

Before selecting the ordinal or probe, rehydrate `prior`, ceiling use, the probe register, clean
streak, and checkpoint history from the durable PR record as required by
[Cycle Authority and Restart Recovery](./cycle-authority-and-restart-recovery.md). Conflicting or
malformed history stops the cycle; it never resets to cycle 1.

For a paired public/private delivery, read the predecessor's terminal handoff before this pass.
Do not start a new sibling-repository cycle while its source PR is still being fixed or awaiting
current-head CI: that creates stale evidence and an avoidable review chain reaction.
