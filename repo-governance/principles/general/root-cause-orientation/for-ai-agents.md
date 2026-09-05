---
title: "For AI Agents"
description: States the four agent-specific obligations for root cause orientation, including diagnosing before acting and proactively fixing preexisting errors.
category: explanation
subcategory: principles
tags:
  - principles
  - root-cause
  - senior-engineer
created: 2026-03-09
when_to_use: Use when defining or auditing how an AI agent must apply root cause orientation in its own behaviour.
---

# For AI Agents

All agents must follow this principle by:

1. **Diagnosing before acting** - Read the relevant code and understand the actual cause before proposing changes
2. **Scoping precisely** - Limit changes to what the task requires; do not improve adjacent code
3. **Applying the senior engineer test** - Evaluate solutions against what a senior engineer would approve, not just what makes tests pass
4. **Proactively fixing preexisting errors** - When encountering preexisting bugs, broken tests, or incorrect configurations, fix the root cause rather than mentioning without action or working around the problem. See [Proactive Preexisting Error Resolution](../../../development/practice/proactive-preexisting-error-resolution.md) for the full practice including scope judgment and agent requirements.

See [Implementation Workflow - Surgical Changes](../../../development/workflow/implementation/surgical-changes-principle.md) for the detailed surgical changes practice that implements minimal impact for software changes.

See [Agent Workflow Orchestration](../../../development/agents/agent-workflow-orchestration.md) for how this principle applies to planning, verification, and autonomous work in multi-step agent tasks.
