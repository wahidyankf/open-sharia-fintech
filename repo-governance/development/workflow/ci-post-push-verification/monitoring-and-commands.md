---
title: "Monitoring and Commands"
description: How to monitor CI without exhausting the GitHub API rate limit, and the reference command set.
category: explanation
subcategory: development
tags:
  - ci
  - github-actions
  - verification
  - quality-gates
  - workflow
when_to_use: Use when polling a CI run's status, or when you need the exact gh commands for triggering and checking a workflow.
---

# Monitoring and Commands

## Monitoring Without Rate-Limiting

Check every **2-5 minutes** using `ScheduleWakeup(delaySeconds=120)` + one `gh run view <run-id> --json conclusion,status,jobs` per wakeup. Repeat until complete. This uses 7-18 API calls for a 35-min job (well under 1% of the 5,000/hour budget).

**`gh run watch` is only safe for jobs <5 min** — it polls every ~3 seconds internally and exhausts the rate limit on any longer job. Tight-loop polling of `gh run view` with no sleep is **forbidden** for the same reason.

See [CI Monitoring Convention](../../workflow/ci-monitoring.md) for:

- Full rate limit budget facts and window behavior
- Required approach: `ScheduleWakeup` every 2-5 min (default) vs `gh run watch` for <5 min jobs
- Trigger discipline (never trigger the same workflow more than once every 10 minutes)
- Recovery procedure when rate-limited (HTTP 403): `ScheduleWakeup(delaySeconds=2100)`, not retry loop

## Commands

```bash
# Identify blast radius
git diff HEAD~1 --name-only

# Trigger a specific workflow on main
gh workflow run ayokoding-www-test-local-deploy-prod.yml

# List recent runs for a workflow to find the run ID
gh run list --workflow=ayokoding-www-test-local-deploy-prod.yml --limit=5

# Check run status (call every 2-5 min via ScheduleWakeup — do NOT use gh run watch for long jobs)
gh run view <run-id> --json conclusion,status,jobs

# View logs for a failed run
gh run view <run-id> --log-failed

# Quick overall status check
gh run list --limit=10
```
