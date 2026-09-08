---
description: Standards for monitoring GitHub Actions CI runs without exhausting the GitHub API rate limit — required tooling, default 2-minute poll interval, no stream-watching, trigger discipline, and recovery procedures
when_to_use: Use whenever monitoring a CI run to completion, to poll safely without exhausting the GitHub API rate limit.
---

# CI Monitoring Convention

Monitoring CI runs is a required step after every push, whether the target is a PR branch (the default `worktree-to-pr`) or `origin main` (the direct-push modes). This convention defines the correct tools, minimum intervals, trigger discipline, and recovery procedures — see the first entry below for the required default interval and the hard 2-minute floor.

## Contents

- [Overview and Absolute Floor](./ci-monitoring/overview-and-absolute-floor.md) — Default poll interval and the hard 2-minute minimum spacing.
- [Runner Contention Across the OSE Repos (Read First)](./ci-monitoring/runner-contention-across-the-ose-repos.md) — Shared, finite runner pools; wait-and-check response.
- [Principles and Conventions Implemented](./ci-monitoring/principles-and-conventions-implemented.md) — Why this convention exists.
- [Purpose and Scope](./ci-monitoring/purpose-and-scope.md) — What this convention covers and defers.
- [Rate Limit Budget Facts](./ci-monitoring/rate-limit-budget-facts.md) — Quota, window, and exhaustion math.
- [ScheduleWakeup Every 2 Minutes (Required Default)](./ci-monitoring/schedulewakeup-every-2-minutes.md) — The required default polling pattern.
- [Manual Poll Loop With 2-Minute Sleep (Unavoidable Loop Cases)](./ci-monitoring/manual-poll-loop-with-2-minute-sleep.md) — The fallback when ScheduleWakeup is unavailable.
- [Trigger Discipline](./ci-monitoring/trigger-discipline.md) — Never retrigger a workflow within 10 minutes.
- [Diagnosing a Stuck Self-Hosted Runner Job](./ci-monitoring/diagnosing-a-stuck-self-hosted-runner-job.md) — Telling hung from slow, and remediating.
- [Retriggering a Stuck Run With No Contention (PR Branches)](./ci-monitoring/retriggering-a-stuck-run-with-no-contention.md) — Rebase-and-push as last resort.
- [Recovery When Rate-Limited](./ci-monitoring/recovery-when-rate-limited.md) — Scheduled-wait recovery from HTTP 403.
- [Locating the Failing Task in a Parallel Runner's Log](./ci-monitoring/locating-the-failing-task-in-a-parallel-runners-log.md) — Why the log tail misleads under Nx.
- [Application in Plan Execution (Step 2c)](./ci-monitoring/application-in-plan-execution-step-2c.md) — Required pattern and forbidden shortcuts.
- [Examples](./ci-monitoring/examples.md) — Worked pass/fail examples.

## Related Documentation

- [CI Post-Push Verification Convention](../workflow/ci-post-push-verification.md) — Mandates triggering and monitoring CI after every push; this convention specifies safe monitoring mechanics.
- [CI Blocker Resolution Convention](../quality/ci-blocker-resolution.md) — How to investigate and fix CI failures once a run completes.
- [CI/CD Conventions](../infra/ci-conventions.md) — Central reference for GitHub Actions workflow structure and naming.
- [Plan Execution Workflow](../../workflows/plan/plan-execution.md) — Step 2c uses this convention for all post-push CI monitoring.
