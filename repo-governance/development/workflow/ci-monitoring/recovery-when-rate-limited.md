---
title: "Recovery When Rate-Limited"
description: The scheduled-wait recovery procedure for an HTTP 403 from gh, and why a retry loop is forbidden.
category: explanation
subcategory: development
tags:
  - ci
  - github-actions
  - rate-limiting
  - monitoring
  - workflow
when_to_use: Use when a gh command returns HTTP 403 during CI monitoring.
---

# Recovery When Rate-Limited

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
