---
title: "Manual Poll Loop With 2-Minute Sleep (Unavoidable Loop Cases)"
description: The fallback poll pattern when ScheduleWakeup is unavailable, and why gh run watch is prohibited.
category: explanation
subcategory: development
tags:
  - ci
  - github-actions
  - rate-limiting
  - monitoring
  - workflow
when_to_use: Use only when ScheduleWakeup is unavailable and a manual poll loop is unavoidable.
---

# Manual Poll Loop With 2-Minute Sleep (Unavoidable Loop Cases)

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
