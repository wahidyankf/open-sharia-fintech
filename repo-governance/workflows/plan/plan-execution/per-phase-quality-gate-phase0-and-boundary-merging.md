---
title: "Per-Phase Quality Gate — Phase 0 Exemption and Delivery-Boundary Merging"
description: Defines Phase 0's exemption from pushing or opening a PR, and the delivery-boundary merge-not-batch rule.
when_to_use: Use when confirming Phase 0 pushes nothing, or deciding whether a delivery unit's PR should open now or wait.
---

# Per-Phase Quality Gate — Phase 0 Exemption and Delivery-Boundary Merging

**Continues** [Per-Phase Quality Gate — Push Targets](./per-phase-quality-gate-push-targets.md).

**Phase 0 is exempt from this entire step — it pushes nothing and opens no PR (HARD RULE)**: Phase 0 is Environment Setup and Baseline. It installs dependencies, converges the toolchain, records the baseline, and resolves preexisting failures; it produces no reviewable change, so it is not a delivery DAG node and has no push target under **any** delivery mode. Do not push a Phase 0 branch, do not run `gh pr create` for Phase 0, do not run the PR-Review Maker→Fixer Cycle for it, and do not proceed to Step 2c after it — there is no CI run to verify. Any evidence file Phase 0 wrote (a baseline snapshot, a recorded path constant) stays on the plan branch and lands in the **first** PR the plan opens, which is the Phase 1 PR. The earliest phase that may open a PR is **Phase 1**. See [Plans Organization Convention §Phase 0 Opens No PR](../../../conventions/structure/plans/phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).

**Delivery-boundary merging (not per-phase, not batch)**: each delivery unit's PR is **opened and merged** as that unit's **delivery boundary** completes, once the hardened merge preconditions hold. Do **not** open a PR at every intermediate phase — that spends a full review cycle on scaffolding the next phase rewrites. Do **not** hold delivery-unit PRs open for a batch merge at plan end either — that re-serialises work the DAG declared independent and grows the divergence each PR must reconcile. Grouping **dependent** phases into one delivery unit is not batching; holding **independent, already-open** PRs is. The **merge actor** is `[AI]` by default; `[HUMAN]` applies only where the plan's own step declares that gate. Partial work reaches `main` **merged but dark** behind a feature flag rather than waiting on a long-lived branch.
