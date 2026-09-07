---
description: How to tell a genuinely hung job step from a merely slow one, and remediate by cancelling and rerunning only the affected jobs.
when_to_use: Use when a self-hosted-runner job step shows zero progress for an extended period and contention has already been ruled out.
---

# Diagnosing a Stuck Self-Hosted Runner Job

Because CI runs on shared self-hosted runners (see the
[Same-machine assumption](../../../../AGENTS.md#agent-workflow-orchestration)), a job's step can hang
indefinitely with zero progress — e.g. a `setup-node` (or `rustup`, see the
[CI Blocker Resolution Convention](../../quality/ci-blocker-resolution/scope.md#scope) infra-failure
exclusion) step stalling for 10+ minutes while every sibling job's equivalent step completes in
seconds. This is a runner contention symptom, not a code defect — do not debug the code.

**Diagnose** by comparing a job's step-level `startedAt` timestamp across two polls spaced by the
normal 2-minute interval:

```bash
gh run view <run-id> --json jobs \
  --jq '.jobs[] | select(.status!="completed") | .steps[]'
```

If the same step's `startedAt` is unchanged across multiple polls and grossly exceeds the duration
that step takes in a sibling job of the same run, it is stuck, not merely slow.

**Remediate** — cancel and rerun only the affected jobs; already-passed jobs keep their
`success` conclusion:

```bash
gh run cancel <run-id>          # cascades to any job depending on the stuck job's output
gh run rerun <run-id> --failed  # reruns only cancelled/failed jobs, not the whole run
```
