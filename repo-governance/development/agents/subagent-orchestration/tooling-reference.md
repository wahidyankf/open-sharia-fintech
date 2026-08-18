---
title: "Tooling Reference"
description: "Lists the tools available for orchestrating and monitoring background subagents."
category: explanation
subcategory: development
tags:
  - ai-agents
  - subagents
  - orchestration
  - development
created: 2025-11-23
when_to_use: Use when looking for the right tool to launch, poll, or inspect a background agent.
---

# Tooling Reference

| Tool             | Purpose in This Convention                                     |
| ---------------- | -------------------------------------------------------------- |
| `Agent`          | Spawns subagent; returns `agentId`                             |
| `TaskStop`       | Terminates stuck agent by `agentId`                            |
| `SendMessage`    | Sends new instructions to a running agent                      |
| `TaskList`       | Lists TaskCreate tasks — does NOT show Agent IDs               |
| `ScheduleWakeup` | Schedules the main agent's next poll (use 180-second interval) |

**Note**: `ScheduleWakeup(delaySeconds=180)` is the preferred mechanism for 3-minute polling cadence. This is consistent with the pattern established by [CI Monitoring Convention](../../workflow/ci-monitoring.md) for other scheduled checks.
