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

- **[CI Monitoring Convention](../../workflow/ci-monitoring.md)**: Agents performing post-push CI verification MUST make one status read every 2 minutes via a scheduled wakeup. `gh run watch` and manual tight-loop polling are forbidden regardless of job duration. When rate-limited (HTTP 403): `ScheduleWakeup(delaySeconds=2100)` — not a retry loop.
