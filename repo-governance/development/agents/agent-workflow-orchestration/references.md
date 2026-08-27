---
title: "References"
description: "Links to related conventions and workflows referenced throughout this convention."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - workflow
  - orchestration
created: 2025-11-23
when_to_use: Use when looking for further reading on agent workflow orchestration.
---

# References

**Related Principles:**

- [Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md) - Think before acting; surface assumptions
- [Root Cause Orientation](../../../principles/general/root-cause-orientation.md) - Fix root causes; minimal impact; senior engineer standard
- [Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md) - Simple delegated agent structures; focused responsibilities

**Related Practices:**

- [Implementation Workflow](../../workflow/implementation.md) - Make it work, make it right, make it fast; surgical changes; goal-driven execution
- [Maker-Checker-Fixer Pattern](../../pattern/maker-checker-fixer.md) - Multi-agent orchestration for content quality workflows
- [AI Agents Convention](../ai-agents.md) - Agent structure, frontmatter, and tool access standards
- [File-Touch Discipline](../../practice/file-touch-discipline.md) - The touched-file ledger every actor keeps and carries through compaction; operationalizes the same-machine assumption, since concurrent orchestration is exactly what makes `git status` unreliable as a record of your own work
- [Skill Context Architecture](../skill-context-architecture.md) - Inline vs fork skills for delegated agent invocation
- [Subagent Orchestration Convention](../subagent-orchestration.md) - Concurrency cap (max 2 simultaneous background Agent-tool spawns) and 3-minute stuck-detection polling for background subagents; specializes the delegated agent model for background execution
- [CI Post-Push Verification Convention](../../workflow/ci-post-push-verification.md) - Trigger and monitor CI after every push; required final step in plan execution
- [CI Monitoring Convention](../../workflow/ci-monitoring.md) - Check once every 2 minutes via a scheduled wakeup; never use `gh run watch`; rate-limit recovery uses `ScheduleWakeup(delaySeconds=2100)`

**Related Agents / Workflows:**

- `plan-maker` - Creates structured plans following the plan format in this convention
