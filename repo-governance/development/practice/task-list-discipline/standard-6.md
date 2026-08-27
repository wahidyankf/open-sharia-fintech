---
title: "Task List Discipline — Standard 6: Idle-Polling Status Heartbeat"
description: The five-minute user heartbeat required only while the main thread has no useful work beyond polling non-CI background work
category: explanation
subcategory: development
tags:
  - task-management
  - planning
  - execution
  - ai-agents
  - discipline
created: 2026-06-23
when_to_use: Use when the main thread is idle except for polling a non-CI background agent or process.
---

# Standard 6: Idle-Polling Status Heartbeat

When the main thread has no useful work left and is doing nothing except polling a non-CI
background agent or process, post a visible status update every **5 minutes** until that work
finishes or the main thread resumes useful work. The heartbeat is required even when the external
state has not changed; say briefly that the work remains in progress and what is being awaited.

This heartbeat does **not** apply merely because a task-list item or background agent exists. If the
main thread is still doing useful work, report meaningful milestones and blockers through ordinary
commentary without starting a second timer.

CI monitoring has its own 2-minute status-read cadence in the
[CI Monitoring Convention](../../workflow/ci-monitoring.md). This Standard does not add a separate
timer for user-facing CI updates.

State changes such as completion, failure, or a newly discovered blocker should be reported when
they occur; do not delay them until the heartbeat.
