---
description: Worked pass/fail examples covering correct polling, trigger checks, and rate-limit recovery versus forbidden stream-watching and tight loops.
when_to_use: Use when you need a concrete example of correct or incorrect CI monitoring behaviour.
---

# Examples

## PASS: Correct — Poll single run to completion (ScheduleWakeup pattern)

```bash
gh workflow run organiclever-app-test-local-deploy-stag.yml
run_id=$(gh run list --workflow=organiclever-app-test-local-deploy-stag.yml \
  --limit=1 --json databaseId --jq '.[0].databaseId')
# [ScheduleWakeup delaySeconds=120]  ← default 2-minute interval
# On wakeup:
gh run view "$run_id" --json status,conclusion
# Repeat wakeup until status == "completed"
```

## FAIL: Forbidden — Stream-watching a run

```bash
# BAD: stream-watching is prohibited — ties up tool slot, exhausts rate limit on long jobs
gh run watch 98765432
```

## PASS: Correct — Check before triggering, then poll

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

## FAIL: Forbidden — Tight-loop polling

```bash
# BAD: burns 500+ API calls in minutes
while [ "$(gh run view $id --json status --jq '.status')" != "completed" ]; do
  echo "waiting..."
done
```

## FAIL: Forbidden — Multiple rapid triggers

```bash
# BAD: triggers three runs within two minutes, risking concurrency cancellation
gh workflow run organiclever-app-test-local-deploy-stag.yml
gh workflow run organiclever-app-test-local-deploy-stag.yml
gh workflow run organiclever-app-test-local-deploy-stag.yml
```

## PASS: Correct — Rate limit recovery

```bash
# Detected: gh run list returned HTTP 403
# Action: stop all gh calls, schedule wakeup
# [ScheduleWakeup delaySeconds=2100]
# On wakeup:
gh run list --limit=1  # verify rate limit cleared
gh run view 98765432 --json status,conclusion  # resume polling — do NOT use gh run watch
# [ScheduleWakeup delaySeconds=120] and repeat until status == "completed"
```
