---
title: "Conventions Implemented/Respected"
description: "Lists the related repository conventions this convention implements and respects."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - workflow
  - orchestration
created: 2025-11-23
when_to_use: Use when checking which sibling conventions govern agent workflow orchestration.
---

# Conventions Implemented/Respected

This practice respects the following conventions:

- **[Content Quality Principles](../../../conventions/writing/quality.md)**: Plan documents and lessons files follow active voice, clear structure, and actionable content - not vague notes.

- **[CI Monitoring Convention](../../workflow/ci-monitoring.md)**: Agents performing post-push CI verification MUST check every 2-5 minutes via `ScheduleWakeup(delaySeconds=120)` + one `gh run view` per wakeup. `gh run watch` is only safe for jobs <5 min (it polls every ~3s and exhausts the 5,000 req/hour quota on longer jobs). Manual tight-loop polling is forbidden. When rate-limited (HTTP 403): `ScheduleWakeup(delaySeconds=2100)` — not a retry loop.
