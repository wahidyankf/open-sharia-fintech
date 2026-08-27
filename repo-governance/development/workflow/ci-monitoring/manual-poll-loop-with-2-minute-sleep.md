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

**Why `gh run watch` is prohibited:** Its default 3-second refresh cadence performs about 20
refreshes per minute, ties up a foreground tool slot, and produces verbose streaming output. A
single `gh run view --json status,conclusion` per 2-minute wakeup is bounded, parseable, and
non-blocking.

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

The tight-loop pattern can issue hundreds of status reads in minutes. Stream watching performs
about 40 times as many refreshes as the required 2-minute cadence. There is no scenario in which
either pattern is acceptable for CI monitoring.
