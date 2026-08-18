---
title: "Safety Features and Related Workflows"
description: Lists the composite's inherited and composite-specific safety guarantees, and links to the workflows it nests or relates to.
when_to_use: Use when verifying what protections this composite provides, or navigating to a related workflow.
---

# Safety Features

- **Everything its constituents guarantee**: gate-before-delivery and no-silent-deviation from
  the planning workflow; worktree isolation + freshness sync, Iron Rules, CI verification, and
  prompted worktree cleanup from the execution workflow
- **Hard phase gate**: no execution on missing, un-gated, undelivered, or worktree-less plans
- **Sequential by default**: one repo executes at a time; cross-repo blast radius is bounded to
  the repo currently in flight
- **Stop-on-failure default**: a failing repo halts the composite unless the invoker explicitly
  chose continue-on-failure in the pre-execution grill
- **No PR-mode execution**: plans awaiting review are never executed by this composite
- **Hook compliance and secrets rule**: every commit in every repo passes that repo's hooks; the
  [No Secrets in Git convention](../../../conventions/security/no-secrets-in-committed-files.md) applies in full

## Related Workflows

- [Plan Multi-Repo Parity Planning](../plan-multi-repo-parity-planning.md) — nested as the
  planning phase (Step 1); use it alone when execution should not follow immediately
- [Plan Execution](../plan-execution.md) — nested per repo as the execution phase (Step 4); use it
  alone for plans that already exist
- [Plan Quality Gate](../plan-quality-gate.md) — nested inside the planning phase per plan
- [Plan Planning](../plan-planning.md) — the single-repo analogue of the
  planning phase
- [PR-Review Maker→Fixer Cycle](../../pr/pr-review-quality-gate.md) — nested inside
  plan-execution's Step 8 for any repo whose plan resolves to a `*-to-pr` delivery mode
