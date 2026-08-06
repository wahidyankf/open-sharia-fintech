---
title: "CI Monitoring Convention"
description: Standards for monitoring GitHub Actions CI runs without exhausting the GitHub API rate limit — required tooling, default 2-minute poll interval, no stream-watching, trigger discipline, and recovery procedures
category: explanation
subcategory: development
tags:
  - ci
  - github-actions
  - rate-limiting
  - monitoring
  - workflow
---

# CI Monitoring Convention

Monitoring CI runs is a required step after every push, whether the target is a PR branch (the default `worktree-to-pr`) or `origin main` (the direct-push modes). How you monitor matters as much as whether you monitor. Polling `gh run view` in a tight loop without delay can exhaust the GitHub API rate limit (5,000 requests/hour) within minutes, blocking all subsequent `gh` commands for up to an hour. This convention defines the correct tools, minimum intervals, trigger discipline, and recovery procedures to ensure CI monitoring never burns API quota unnecessarily.

**Default poll interval: 2 minutes.** Schedule a wakeup every 2 minutes (or slower) and issue one `gh run view --json status,conclusion` per wakeup. Do not use `gh run watch` (stream-watching is prohibited for CI monitoring).

**Absolute floor: never poll CI or GitHub Actions faster than once every 2 minutes.** Two minutes is the hard, never-exceed minimum spacing for any CI or Actions status check; the 2-minute default above sits exactly at this floor — going slower (longer intervals) is always fine, going faster is forbidden. Any cadence faster than once per 2 minutes is forbidden regardless of mechanism (manual loop, scheduled wakeup, or stream-watch).

## Runner Contention Across the OSE Repos (Read First)

**Runner capacity across the OSE repos is limited and shared — contention is expected, not a bug.** `ose-public`, `ose-primer`, and `beaver-nest` run CI on GitHub's free-tier hosted runners (`runs-on: ubuntu-latest`), which share GitHub's per-account concurrent-job cap across every public repo under [github.com/wahidyankf](https://github.com/wahidyankf). `ose-private` runs on a small, fixed pool of self-hosted runners (`runs-on: [self-hosted, linux, ose-self-hosted]`). Both pools are finite. When multiple repos or workflows queue jobs at the same time, a run can sit `queued`, or a step can stall with no progress — this is runner/action contention, not a defect in the pushed code, and it is not something a code fix or a retry resolves.

**Response: wait patiently, then check what else is running before assuming anything is broken.**

```bash
# Queued/in-progress runs in one repo
gh run list --status=queued --status=in_progress --limit=20

# Same check across every OSE repo
for repo in ose-public ose-primer ose-private beaver-nest; do
  echo "== $repo =="
  gh run list --repo wahidyankf/$repo --status=queued --status=in_progress --limit=10
done

# Org/account-wide view (browser) — https://github.com/wahidyankf, then each repo's Actions tab
```

Keep the same [2-minute `ScheduleWakeup` cadence](#preferred-monitoring-approaches-priority-order) already required by this convention while waiting — do not shorten it because the cause is suspected to be contention rather than a normal-length job. Do not cancel/rerun a queued or stalled job as a first response to suspected contention: that only consumes another slot in the same congested pool. Only escalate to the [stuck-runner diagnosis](#diagnosing-a-stuck-self-hosted-runner-job) below once contention has been ruled out — i.e., nothing else is queued or running and the job is still making zero progress.

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: The required default approach for monitoring CI runs is `ScheduleWakeup` every 2 minutes (2-5 minutes acceptable) with a single `gh run view --json status,conclusion` check per wakeup — this replaces error-prone manual polling without exhausting the API rate limit. Stream-watching via `gh run watch` is prohibited for CI monitoring.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: `ScheduleWakeup` + a single `gh run view --json status,conclusion` is simpler than a while-loop, a sleep, a JSON parser, and retry logic. A scheduled wakeup removes code that must be written, debugged, and maintained — and avoids the rate limit hazard that stream-watching via `gh run watch` introduces on jobs longer than 5 minutes.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Rate limit budget is a finite, shared resource. This convention makes its constraints explicit — quota size, window duration, recovery delay — so agents and developers can reason about impact before issuing commands rather than discovering exhaustion after the fact.

- **[Reproducibility First](../../principles/software-engineering/reproducibility.md)**: A plan execution that burns the API rate limit mid-run is non-reproducible: repeating the same sequence on the same codebase produces a different outcome depending on how many prior API calls were made. Safe monitoring practices make CI verification a reliable, repeatable step.

## Conventions Implemented/Respected

This convention implements/respects the following development practices:

- **[CI Post-Push Verification Convention](./ci-post-push-verification.md)**: That convention mandates triggering and monitoring CI after every push. This convention specifies HOW to perform that monitoring safely — `ScheduleWakeup` every 2 minutes (default) as the required approach for standard CI jobs, `gh run watch` prohibited for CI monitoring, minimum 2-minute sleep if a manual poll loop is unavoidable, and recovery procedures when rate-limited.

- **[CI Blocker Resolution Convention](../quality/ci-blocker-resolution.md)**: When a rate limit prevents CI verification, it is a blocker. This convention provides the correct recovery path (scheduled wakeup, not retry loop) rather than treating a 403 as a transient error and spinning.

## Purpose

This convention exists to prevent GitHub API rate limit exhaustion during CI monitoring in plan execution and manual development workflows. The rate limit is a shared resource across all authenticated `gh` commands in the same hour window. Burning it on tight-poll loops blocks the entire toolchain — not just CI monitoring — for up to an hour.

The target audience is any agent or developer performing the post-push CI verification step described in the [CI Post-Push Verification Convention](./ci-post-push-verification.md).

## Scope

### What This Convention Covers

- Correct tool selection for watching CI runs to completion
- Minimum poll intervals when manual polling is unavoidable
- Trigger discipline to avoid redundant concurrent runs
- Rate limit budget facts and window behavior
- Recovery procedure when rate-limited (HTTP 403 from `gh`)
- Runner/action contention across the shared, limited OSE runner pools (free hosted + self-hosted) and the wait-and-check response
- Retriggering a genuinely stuck run (no contention) via rebase-and-push
- Application of these rules in plan execution (Step 2c of `plan-execution.md`)

### What This Convention Does NOT Cover

- Which workflows to trigger after a push (see [CI Post-Push Verification Convention](./ci-post-push-verification.md))
- How to investigate and fix a failed CI run (see [CI Blocker Resolution Convention](../quality/ci-blocker-resolution.md))
- GitHub Actions workflow authoring standards (see [CI/CD Conventions](../infra/ci-conventions.md))

## Standards

### Rate Limit Budget Facts

Understanding the budget prevents accidental exhaustion.

| Parameter            | Value                                                                          |
| -------------------- | ------------------------------------------------------------------------------ |
| Quota                | 5,000 requests/hour per authenticated user                                     |
| Reset window         | Rolling 1 hour from the first request                                          |
| When exhausted       | HTTP 403 on all subsequent `gh` commands                                       |
| Reset timing         | Top of the next hour from first call                                           |
| Single `gh run view` | 1 request per invocation                                                       |
| `gh run watch`       | Polls internally every ~3s; **prohibited for CI monitoring** (stream-watching) |

A tight loop with no sleep issues hundreds of requests per minute. At 200 calls/minute, the 5,000-request quota exhausts in 25 minutes. **`gh run watch` on a 30-minute CI run also exhausts the quota** — it polls ~3 times/minute for 30 minutes = ~90 calls just for watching. Combined with triggers and other list calls this crosses 5,000 quickly. Any `gh` command — list, trigger, view — then returns HTTP 403 until the window resets.

### Preferred Monitoring Approaches (Priority Order)

Use the first approach that fits the situation. Only fall back to lower-priority approaches when the higher-priority one is not applicable.

#### 1. `ScheduleWakeup` Every 2 Minutes (Required Default)

Trigger the run, record the run ID, schedule a wakeup for 2 minutes (2-5 minutes acceptable), check status once, repeat until done. Each check is **one** `gh run view --json status,conclusion` call.

**Why 2 min default:** Fast enough for responsive feedback; safe forever at 30 req/hour (0.6% of the 5,000/hour budget). The 2-5 min window gives flexibility — 2 min is the recommended default for active monitoring.

```bash
# Step 1: trigger and capture run ID
gh workflow run organiclever-app-test-local-deploy-stag.yml
# URL output contains run ID, e.g. https://github.com/.../runs/12345678

# Step 2: ScheduleWakeup(delaySeconds=120)  ← check in 2 min (default)

# Step 3: On wakeup — one check
gh run view <run-id> --json status,conclusion
# If status != "completed" → ScheduleWakeup(delaySeconds=120) and check again
# If status == "completed" → read conclusion and proceed
```

At 2 min intervals a 35-min CI job needs ~18 checks = **18 API calls total**. Zero burst.

**Rate limit math:** 1 call every 2 min = 30 calls/hour. Budget: 5,000/hour. Usage: 0.6%. Safe forever.

#### 2. Manual Poll Loop With 2-Minute Sleep (Unavoidable Loop Cases)

**Do not use `gh run watch`** — stream-watching is prohibited for CI monitoring. If `ScheduleWakeup` is not available, use a manual poll loop with a minimum 2-minute sleep between checks.

**Why `gh run watch` is prohibited:** It streams output by polling internally every ~3 seconds. This (1) ties up a foreground tool slot for the entire duration of the run, (2) exhausts the API rate limit on any job longer than ~5 minutes (~3 calls/min × 30 min = 90 calls just for watching), and (3) produces verbose unstructured output that must be parsed. A single `gh run view --json status,conclusion` per wakeup is cheaper, parseable, and non-blocking.

**Canonical poll-loop pattern (when `ScheduleWakeup` is unavailable):**

```bash
# PASS: Correct — 2-minute minimum sleep, structured JSON output
run_id=<run-id>
while true; do
  result=$(gh run view "$run_id" --json status,conclusion)
  status=$(echo "$result" | jq -r '.status')
  conclusion=$(echo "$result" | jq -r '.conclusion')
  if [ "$status" = "completed" ]; then
    echo "Run completed with conclusion: $conclusion"
    break
  fi
  sleep 120  # 2-minute minimum — never shorten this
done
```

```bash
# FAIL: Forbidden — tight loop with no sleep
while [ "$(gh run view $run_id --json status | python3 -c ...)" != "completed" ]; do
  echo "waiting..."
done
```

```bash
# FAIL: Forbidden — stream-watching (ties up tool slot, exhausts rate limit on long jobs)
gh run watch <run-id>
```

The tight-loop pattern can issue 500+ API calls in minutes. `gh run watch` exhausts the quota on any job longer than ~5 minutes. There is no scenario in which either of these patterns is acceptable for CI monitoring.

### Trigger Discipline

Triggering the same workflow repeatedly before prior runs complete multiplies API quota consumption (setup calls, list calls, view calls per run) and risks concurrency cancellation — where GitHub's `concurrency` group cancels an in-progress run when a new one is queued, sending both to a non-green terminal state.

**Rules:**

1. Never trigger the same workflow more than once every 10 minutes.
2. Before triggering, check whether a run is already in progress:

   ```bash
   # Check for an active run before triggering
   gh run list --workflow=<workflow-file> --limit=1 --json status --jq '.[0].status'
   # If status is "in_progress" or "queued", do NOT trigger again
   ```

3. If a run was cancelled by a concurrency group, wait for the currently-running run to reach a terminal state before deciding whether to trigger again.
4. In plan execution, if CI was triggered for a push and the run is still in progress, schedule a wakeup and poll the existing run with `gh run view <id> --json status,conclusion` — do not trigger a new run.

### Diagnosing a Stuck Self-Hosted Runner Job

Because CI runs on shared self-hosted runners (see the
[Same-machine assumption](../../../AGENTS.md#agent-workflow-orchestration)), a job's step can hang
indefinitely with zero progress — e.g. a `setup-node` (or `rustup`, see the
[CI Blocker Resolution Convention](../quality/ci-blocker-resolution.md#scope) infra-failure
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

### Retriggering a Stuck Run With No Contention (PR Branches)

If [runner contention across the OSE repos](#runner-contention-across-the-ose-repos-read-first) has
been ruled out (nothing else queued or running) and a `worktree-to-pr` run is still stuck — queued
indefinitely, or wedged in a way `gh run cancel`/`gh run rerun` does not clear — rebase the PR branch
onto latest `origin/main` and push. The new commit SHA registers as a fresh trigger, which often
clears whatever the platform wedged on:

```bash
git fetch origin main
git rebase origin/main
git push --force-with-lease
```

Use `--force-with-lease`, never `--force`, per the
[No Destructive Git Operations Convention](./no-destructive-git-operations.md). This applies to
`worktree-to-pr` branches only — a direct push to `main` has no PR branch to rebase; if that is stuck
with contention ruled out, use `gh run rerun` (above) or wait longer.

The rebase lands foreign `origin/main` commits on the branch — apply the
[Integration Diff Review Convention](./integration-diff-review.md) before continuing. Retriggering
CI is not a reason to skip diff review of what just landed.

### Recovery When Rate-Limited

An HTTP 403 response from any `gh` command during CI monitoring means the rate limit is exhausted. The correct response is a scheduled wait, not a retry loop.

**Recovery procedure:**

1. Stop all `gh` calls immediately. Do NOT retry the failing command.
2. Note the time. The rate limit resets approximately at the top of the next hour from when the window opened (not from when the 403 occurred).
3. Use `ScheduleWakeup` with `delaySeconds=2100` (35 minutes) to resume CI verification after the reset.
4. On wakeup, run `gh run list --limit=5` once to verify the rate limit has cleared before proceeding with full monitoring.
5. If still rate-limited on wakeup, schedule another wakeup for `delaySeconds=1800` (30 minutes) and do not issue further calls.

```bash
# PASS: Correct recovery — scheduled wait, not retry loop
# [Detected HTTP 403 from gh run list]
# [ScheduleWakeup delaySeconds=2100 — rate limit recovery]
# [On wakeup: gh run list --limit=1 to verify reset, then resume polling with gh run view <id> --json status,conclusion]
```

```bash
# FAIL: Forbidden — retry loop after rate limit
while true; do
  result=$(gh run view "$run_id" --json status 2>&1)
  if echo "$result" | grep -q "403"; then
    sleep 60  # insufficient; still burning quota on each iteration
    continue
  fi
  break
done
```

## Application in Plan Execution (Step 2c)

The [plan-execution workflow](../../workflows/plan/plan-execution.md) Step 2c (Post-Push CI Verification) requires monitoring all GitHub Actions workflows after every push. This convention governs how that monitoring executes.

**Required pattern for Step 2c (standard CI jobs, 10–35 min):**

```bash
# 1. Identify the triggered run
gh run list --workflow=<workflow-file> --limit=3

# 2. Schedule a wakeup for expected completion time + buffer
# [ScheduleWakeup delaySeconds=2100]  ← 35 min for a typical 30-min job

# 3. On wakeup — ONE check, not a loop
gh run view <run-id> --json conclusion,status,jobs

# 4. On failure: pull logs and diagnose
gh run view <run-id> --log-failed
```

**`gh run watch` is prohibited in Step 2c** (and all CI monitoring). Use `ScheduleWakeup` + single `gh run view --json status,conclusion` for all CI jobs regardless of expected duration.

**Forbidden in Step 2c:**

- Using `gh run watch` for any CI job (stream-watching prohibited)
- Tight-loop polling with `gh run view` and no sleep
- Polling intervals shorter than 2 minutes if a manual loop is unavoidable
- Triggering a new run while the previous one is still active
- Treating an HTTP 403 as a transient error and retrying immediately

**When rate-limited during plan execution:**

If the rate limit is hit mid-plan, use `ScheduleWakeup delaySeconds=2100` and resume CI verification after the reset. Do not spin in a retry loop. The delivery checklist item for Step 2c stays in-progress until CI verification completes. The plan execution checkpoint survives the wakeup pause via the on-disk delivery checklist (disk-is-truth invariant from Iron Rule 10).

## Examples

### PASS: Correct — Poll single run to completion (ScheduleWakeup pattern)

```bash
gh workflow run organiclever-app-test-local-deploy-stag.yml
run_id=$(gh run list --workflow=organiclever-app-test-local-deploy-stag.yml \
  --limit=1 --json databaseId --jq '.[0].databaseId')
# [ScheduleWakeup delaySeconds=120]  ← default 2-minute interval
# On wakeup:
gh run view "$run_id" --json status,conclusion
# Repeat wakeup until status == "completed"
```

### FAIL: Forbidden — Stream-watching a run

```bash
# BAD: stream-watching is prohibited — ties up tool slot, exhausts rate limit on long jobs
gh run watch 98765432
```

### PASS: Correct — Check before triggering, then poll

```bash
active=$(gh run list --workflow=organiclever-app-test-local-deploy-stag.yml \
  --limit=1 --json status --jq '.[0].status')
if [ "$active" = "in_progress" ] || [ "$active" = "queued" ]; then
  echo "Run already active — polling existing run instead of triggering new one"
  run_id=$(gh run list --workflow=organiclever-app-test-local-deploy-stag.yml \
    --limit=1 --json databaseId --jq '.[0].databaseId')
  # [ScheduleWakeup delaySeconds=120] then: gh run view "$run_id" --json status,conclusion
else
  gh workflow run organiclever-app-test-local-deploy-stag.yml
fi
```

### FAIL: Forbidden — Tight-loop polling

```bash
# BAD: burns 500+ API calls in minutes
while [ "$(gh run view $id --json status --jq '.status')" != "completed" ]; do
  echo "waiting..."
done
```

### FAIL: Forbidden — Multiple rapid triggers

```bash
# BAD: triggers three runs within two minutes, risking concurrency cancellation
gh workflow run organiclever-app-test-local-deploy-stag.yml
gh workflow run organiclever-app-test-local-deploy-stag.yml
gh workflow run organiclever-app-test-local-deploy-stag.yml
```

### PASS: Correct — Rate limit recovery

```bash
# Detected: gh run list returned HTTP 403
# Action: stop all gh calls, schedule wakeup
# [ScheduleWakeup delaySeconds=2100]
# On wakeup:
gh run list --limit=1  # verify rate limit cleared
gh run view 98765432 --json status,conclusion  # resume polling — do NOT use gh run watch
# [ScheduleWakeup delaySeconds=120] and repeat until status == "completed"
```

## Related Documentation

- [CI Post-Push Verification Convention](./ci-post-push-verification.md) — Mandates triggering and monitoring CI after every push; this convention specifies safe monitoring mechanics.
- [CI Blocker Resolution Convention](../quality/ci-blocker-resolution.md) — How to investigate and fix CI failures once a run completes.
- [CI/CD Conventions](../infra/ci-conventions.md) — Central reference for GitHub Actions workflow structure and naming.
- [Plan Execution Workflow](../../workflows/plan/plan-execution.md) — Step 2c uses this convention for all post-push CI monitoring.
