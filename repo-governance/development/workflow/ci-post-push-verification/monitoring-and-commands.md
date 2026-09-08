---
description: How to monitor CI without exhausting the GitHub API rate limit, and the reference command set.
when_to_use: Use when polling a CI run's status, or when you need the exact gh commands for triggering and checking a workflow.
---

# Monitoring and Commands

## Monitoring Without Rate-Limiting

Check every **2 minutes** using a scheduled wakeup plus one `gh run view <run-id> --json conclusion,status,jobs` per wakeup. Repeat until complete.

**Never use `gh run watch`.** Its internal stream polling violates the repository's explicit polling cadence regardless of expected job duration. Tight-loop polling is forbidden for the same reason.

See [CI Monitoring Convention](../../workflow/ci-monitoring.md) for:

- Full rate limit budget facts and window behaviour
- Required approach: one scheduled status check every 2 minutes; never `gh run watch`
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

# Check run status once every 2 minutes — never use gh run watch
gh run view <run-id> --json conclusion,status,jobs

# View logs for a failed run
gh run view <run-id> --log-failed

# Quick overall status check
gh run list --limit=10
```
