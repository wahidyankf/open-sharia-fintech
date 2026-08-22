---
title: "Termination Criteria and Relationship to Delivery-Mode Done-Definition"
description: States the pass/partial/fail termination criteria per mode, and how this workflow's document-level pass relates to the PR-review cycle's delivery-level done-definition.
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
executing under a `*-to-pr` mode (`worktree-to-pr` or `main-to-pr`), full "done" for the plan's
actual delivery additionally requires satisfying the
[PR-Review Maker→Fixer Cycle](../../pr/pr-review-quality-gate.md)'s
[Route-Specific Done-Definition](../../pr/pr-review-quality-gate/route-specific-done-definition.md)
— the route's review complete, every inline comment answered and every accepted fix committed and
pushed, all PR gates GREEN, archival committed inside the PR — before the merge. The two gates sit at different lifecycle stages: this workflow
gates the plan document pre-execution; the PR-review cycle gates the delivered change pre-merge.

**The hardened merge preconditions** that gate that eventual merge — **all five** required: (a) the
PR's route is complete — an eligible PR stopped at two consecutive clean cycles
under previously-unused probe classes, neither leaving a code-related MEDIUM/HIGH/CRITICAL
finding, within the **ceiling of seven** (a ceiling, **not a floor** — a PR
merges once (b)-(e) also hold, never on additional cycles), while a noneligible PR has recorded
classifier evidence and a green `pr-quality-gate.yml` run; a `blocked` route never merges;
(b) 0 code-related CRITICAL + 0 HIGH + 0 MEDIUM findings outstanding;
(c) the branch **up-to-date with the latest `origin/main`**, brought forward **non-destructively**
if behind (never a shared-history rewrite); (d) all PR quality gates green; (e) the
surface-conditional tester gates run and their defect findings resolved, or the exemption explicitly
recorded. `[AI]` merges once they hold; a `[HUMAN]` merge gate applies only where a plan's own step
says so explicitly, with identical preconditions either way.
