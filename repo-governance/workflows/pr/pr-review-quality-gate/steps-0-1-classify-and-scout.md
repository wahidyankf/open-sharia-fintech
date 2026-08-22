---
title: "PR-Review Quality Gate — Steps 0-1: Classify and Scout Pass"
description: "Step 0 (classify the PR and resolve loop inputs) and Step 1 (the per-cycle scout pass that produces risk tier, specialist set, and shared-context brief)."
when_to_use: "Use when checking the args/outputs/success criteria for the classification step or the per-cycle scout step."
---

# Steps 0-1 — Classify the PR and Per-Cycle Scout Pass

## 0. Classify the PR and Resolve Loop Inputs (Sequential)

- **Agent**: Orchestrator (the caller — `plan-execution.md` Step 8, or a direct invocation)
- **Args**: `{input.pr}`, `{input.cycles}` (default maximum 7)
- **Output**: Confirmed PR reference, behavior classification, classification evidence, and maximum
  cycle count when eligible
- **Success criteria**: The PR exists and is open; the classifier has recorded `eligible` or
  `noneligible`; `cycles` is a positive integer no greater than 7 unless the caller explicitly
  authorizes a different ceiling
- **Route**: A noneligible PR skips Steps 1–3 and proceeds to the `pr-quality-gate.yml` verification
  in Step 4. An eligible PR proceeds through the loop.

## 1. Per-Cycle Scout Pass (Sequential, Repeats for cycle = 1..N)

- **Agent**: `pr-review-scout-maker` (fresh state each cycle)
- **Args**: PR reference, `prior` state (prior-cycle thread-resolution/dismissal state)
- **Output**: Pinned head SHA, risk tier, specialist set, shared-context brief, dismissal state
- **Depends on**: Step 0 (cycle 1); the previous cycle's CI-green gate (cycle > 1)
- **Condition**: Runs once per eligible cycle, for `cycle` in `1..={input.cycles}`, stopping at [its clean exit](./probe-variation-and-exit.md)
- **Success criteria**: `tier` is exactly one of `trivial`/`lite`/`full` and is recorded for the
  header
- **On failure**: If the scout cannot access the PR or an API call fails, retry once and record the
  blocked condition. Do not relabel the PR noneligible merely because classification evidence is
  unavailable.
