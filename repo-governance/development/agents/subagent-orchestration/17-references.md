---
title: "References"
description: "Links to related conventions and documents referenced by the subagent-orchestration convention."
category: explanation
subcategory: development
tags:
  - ai-agents
  - subagents
  - orchestration
  - development
created: 2025-11-23
when_to_use: Use when looking for further reading on subagent orchestration.
---

# References

**Related Principles:**

- [Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md) - Bounded, pre-decided constraints over reactive improvisation
- [Root Cause Orientation](../../../principles/general/root-cause-orientation.md) - Relaunch addresses the actual cause of stuck behavior
- [Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md) - Fixed cap and concrete threshold over adaptive scheduling
- [Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md) - Documented constants, not inferred limits

**Related Practices:**

- [Agent Workflow Orchestration Convention](../agent-workflow-orchestration.md) - Delegated agent strategy; this convention specializes that model for background spawning
- [AI Agents Convention](../ai-agents.md) - Agent file structure and frontmatter standards
- [CI Monitoring Convention](../../workflow/ci-monitoring.md) - `ScheduleWakeup` polling pattern reused here for stuck detection

**Agents:**

- `repo-rules-checker` - Validates convention compliance
- `repo-rules-maker` - Creates and updates conventions
