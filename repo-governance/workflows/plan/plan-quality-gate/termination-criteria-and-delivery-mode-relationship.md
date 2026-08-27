---
title: "Termination Criteria and Relationship to Delivery-Mode Done-Definition"
description: States pass/partial/fail criteria and how document validation relates to PR delivery gates.
when_to_use: Use when determining whether a plan-quality-gate run should report pass, partial, or fail, or when reconciling it against the hardened merge preconditions.
---

# Termination Criteria and Relationship to Delivery-Mode Done-Definition

## Termination Criteria

**Success** (`pass`):

- **lax**: Zero CRITICAL findings on 2 consecutive checks (HIGH/MEDIUM/LOW may exist)
- **normal**: Zero CRITICAL/HIGH findings on 2 consecutive checks (MEDIUM/LOW may exist)
- **strict**: Zero CRITICAL/HIGH/MEDIUM findings on 2 consecutive checks (LOW may exist)
- **ocd**: Zero findings at all levels on 2 consecutive checks

**Partial** (`partial`):

- Threshold-level findings remain after max-iterations safety limit

**Failure** (`fail`):

- Checker or fixer encountered technical errors

`## User Decisions Required` is a resumable checkpoint, not a failure or partial result.

**Note**: Below-threshold findings are reported in final audit but don't prevent success status. Success requires two consecutive zero-finding validations (consecutive pass requirement).

## Relationship to Delivery-Mode Done-Definition

This workflow's `pass` status certifies the plan **document** is complete and technically accurate
before execution starts — it does not by itself certify the plan's **delivery** is done. Every plan
resolves to one of four [Delivery Modes](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode) via
the three-tier precedence (invocation argument > plan field > `worktree-to-pr` default). For a plan
executing under a `*-to-pr` mode (`worktree-to-pr` or `main-to-pr`), full delivery additionally
requires exact-current-head/base `Quality gate`, one authenticated current-head
[`pr-leak-review`](../../pr/pr-leak-review.md) pass, resolved conversations, applicable finite
surface gates, branch currency, and archival committed inside the PR. Broad semantic review is
absent unless directly requested. This workflow gates the plan document pre-execution; the
[PR Merge Protocol](../../../development/workflow/pr-merge-protocol.md) gates delivery pre-merge.
