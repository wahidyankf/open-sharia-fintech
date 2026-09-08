---
description: Why CI monitoring must be rate-limit-safe, the required default poll interval, and the hard 2-minute minimum spacing.
when_to_use: Use when starting CI monitoring, to confirm the default poll interval and the absolute floor on polling frequency.
---

# Overview and Absolute Floor

Monitoring CI runs is a required step after every push, whether the target is a PR branch (the default `worktree-to-pr`) or `origin main` (the direct-push modes). How you monitor matters as much as whether you monitor. Polling `gh run view` in a tight loop without delay can exhaust the GitHub API rate limit (5,000 requests/hour) within minutes, blocking all subsequent `gh` commands for up to an hour. This convention defines the correct tools, minimum intervals, trigger discipline, and recovery procedures to ensure CI monitoring never burns API quota unnecessarily.

**Default poll interval: 2 minutes.** Schedule a wakeup every 2 minutes (or slower) and issue one `gh run view --json status,conclusion` per wakeup. Do not use `gh run watch` (stream-watching is prohibited for CI monitoring).

**Absolute floor: never poll CI or GitHub Actions faster than once every 2 minutes.** Two minutes is the hard, never-exceed minimum spacing for any CI or Actions status check; the 2-minute default above sits exactly at this floor — going slower (longer intervals) is always fine, going faster is forbidden. Any cadence faster than once per 2 minutes is forbidden regardless of mechanism (manual loop, scheduled wakeup, or stream-watch).
