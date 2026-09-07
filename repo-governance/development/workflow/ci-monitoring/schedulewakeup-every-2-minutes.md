---
description: The required default monitoring pattern — schedule a wakeup, then issue one status check per wakeup until the run completes.
when_to_use: Use as the default way to poll any CI run to completion.
---

# ScheduleWakeup Every 2 Minutes (Required Default)

Use the first approach that fits the situation. Only fall back to lower-priority approaches when the higher-priority one is not applicable — see [Manual Poll Loop With 2-Minute Sleep](./manual-poll-loop-with-2-minute-sleep.md) for the fallback.

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
