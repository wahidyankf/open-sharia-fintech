---
title: "PR-Review Quality Gate — Related Workflows and Success Metrics"
description: "How this workflow composes with plan-execution and plan-quality-gate, and the four success metrics tracked across executions (cycles to clean exit, non-convergence rate, findings trend, CI-green time)."
when_to_use: "Use when checking which workflows call into or relate to this one, or what metrics to track when auditing this workflow's health."
---

# Related Workflows and Success Metrics

## Related Workflows

This workflow is composed with:

- [`plan-execution`](../../plan/plan-execution.md) — invokes this workflow from Step 8 (Finalization and
  Archival) for every `*-to-pr` delivery mode, before the merge.
- [`plan-quality-gate`](../../plan/plan-quality-gate.md) — a related but distinct
  iterate-to-zero-findings pattern; this workflow instead runs a **fixed** N-cycle loop, not an
  until-zero-findings loop.

## Success Metrics

Track across executions:

- **Cycles to clean exit**: how often eligible PRs reach `done` before cycle six versus requiring
  late-cycle learning capture.
- **Non-convergence rate**: percentage of eligible PRs that reach the ceiling blocked by unresolved
  code-related MEDIUM/HIGH/CRITICAL findings.
- **Findings-per-cycle trend**: whether later cycles produce fewer consolidated findings than
  earlier ones (a healthy trend), tracked as an observability signal, not a loop-exit condition.
- **Time to CI-green per cycle**: how many fix-and-push attempts each cycle needs to clear the
  CI-green gate.
