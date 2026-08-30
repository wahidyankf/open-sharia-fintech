---
title: "When to Plan"
description: "Defines when an agent should produce an explicit plan before acting, the plan format, and how to re-plan when things go wrong."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - workflow
  - orchestration
created: 2025-11-23
when_to_use: Use when deciding whether a task needs an upfront plan before execution starts.
---

# When to Plan

Use the harness's native planning/task surface for any non-trivial task. A task is non-trivial if
it meets any of these criteria:

- Three or more distinct steps are required
- The task involves architectural decisions or file structure choices
- Multiple files or components will be changed
- The correct approach is not immediately obvious from the request

**When not to plan**: Simple, obvious fixes with a single step and no ambiguity. Documenting a plan for "fix this typo" wastes time without adding clarity.

## Task-Plan Format

Prefer the harness task list; use `local-tmp/todo.md` only when the harness lacks one. This internal
planning does not authorize a durable artifact under `plans/`. Create a repository plan only on a
literal user request under the
[Plan-Artifact Authorization rule](../../../conventions/structure/plans/plan-artifact-authorization-and-transition.md).
Each item should be independently verifiable.

```
## Plan: [Brief task description]

- [ ] Step 1 → verify: [how you will know this is done]
- [ ] Step 2 → verify: [how you will know this is done]
- [ ] Step 3 → verify: [how you will know this is done]

## Review

[Added after completion: what worked, what did not, what would change]
```

**Verify before starting implementation**: For significant architectural decisions, check in before executing. For straightforward multi-step tasks, proceed with the plan.

## Re-planning When Things Go Wrong

Stop and re-plan when the current approach is not working. The signal to re-plan is when:

- Multiple consecutive steps produce unexpected results
- A fundamental assumption in the plan turns out to be false
- The approach is technically feasible but increasingly complex

Do not keep pushing forward hoping the situation improves. Stopping to re-plan is faster than accumulating a chain of workarounds.
