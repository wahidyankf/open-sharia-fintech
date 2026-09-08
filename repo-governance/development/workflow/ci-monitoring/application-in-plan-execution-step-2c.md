---
description: How the plan-execution workflow's Step 2c post-push CI verification applies this convention's monitoring rules.
when_to_use: Use when executing Step 2c of the plan-execution workflow, for the exact required monitoring pattern and forbidden shortcuts.
---

# Application in Plan Execution (Step 2c)

The [plan-execution workflow](../../../workflows/plan/plan-execution.md) Step 2c (Post-Push CI Verification) requires monitoring all GitHub Actions workflows after every push. This convention governs how that monitoring executes.

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

**Step 1 can legitimately find nothing, and that is not the same as "not finished yet".** GitHub
builds `refs/pull/<n>/merge` before dispatching a `pull_request` event, so a PR whose
`mergeStateStatus` is `DIRTY` — conflicted with its base — dispatches **no run at all**: not
queued, not failed, absent. In `gh run list` that is indistinguishable from a slow queue, and
waiting is the wrong response, because only the author can clear it by rebasing. So assert that a
run exists for the head you pinned before waiting on that run's conclusion:

```bash
gh pr view <n> --json mergeStateStatus,headRefOid
gh run list --commit <head-sha> --limit 5
```

An empty second result alongside a `DIRTY` first result means rebase, not wait. A poll keyed on
run status cannot distinguish the two, because there is no run to carry a status.

**`gh run watch` is prohibited in Step 2c** (and all CI monitoring). Use `ScheduleWakeup` + single `gh run view --json status,conclusion` for all CI jobs regardless of expected duration.

**Forbidden in Step 2c:**

- Using `gh run watch` for any CI job (stream-watching prohibited)
- Tight-loop polling with `gh run view` and no sleep
- Polling intervals shorter than 2 minutes if a manual loop is unavoidable
- Triggering a new run while the previous one is still active
- Treating an HTTP 403 as a transient error and retrying immediately

**When rate-limited during plan execution:**

If the rate limit is hit mid-plan, use `ScheduleWakeup delaySeconds=2100` and resume CI verification after the reset. Do not spin in a retry loop. The delivery checklist item for Step 2c stays in-progress until CI verification completes. The plan execution checkpoint survives the wakeup pause via the on-disk delivery checklist (disk-is-truth invariant from Iron Rule 10).
