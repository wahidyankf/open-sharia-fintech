---
title: "Standard 5 — Idle-Polling Status Heartbeat"
description: "Requires a five-minute user heartbeat only while the main thread has no useful work beyond polling non-CI background work."
category: explanation
subcategory: development
tags:
  - ai-agents
  - subagents
  - orchestration
  - development
created: 2025-11-23
when_to_use: Use when the main thread is idle except for polling a non-CI background agent or process.
---

# Standard 5 — Idle-Polling Status Heartbeat

When the main thread has no useful work left and is doing nothing except polling a non-CI
background agent or process, it MUST post a visible status update every **5 minutes**, even when
nothing changed. Report completion, failure, or a new blocker immediately.

Do not start this timer merely because a background agent or active task exists. While the main
thread is doing useful work, ordinary milestone commentary is sufficient. CI monitoring remains
governed by the separate [CI Monitoring Convention](../../workflow/ci-monitoring.md).

The canonical cross-task statement lives in
[Task List Discipline — Standard 6](../../practice/task-list-discipline/standard-6.md); this
subagent-specific surface keeps only the orchestration-facing summary.
