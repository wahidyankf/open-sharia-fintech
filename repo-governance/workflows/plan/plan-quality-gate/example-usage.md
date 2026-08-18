---
title: "Example Usage — Plan Quality Gate"
description: Worked examples of invoking plan-quality-gate against all plans, a plan folder, a single plan, and with explicit iteration bounds.
when_to_use: Use when writing an invocation of plan-quality-gate and needing a worked example of the scope/mode arguments.
---

# Example Usage

## Validate All Plans

```
User: "Run plan quality gate workflow for all plans"
```

The AI will invoke `plan-checker` and `plan-fixer` via the Agent tool:

- Validate all plan files (`plan-checker` delegated agent)
- Apply all fixes (`plan-fixer` delegated agent)
- Iterate until zero findings achieved

## Validate Specific Plan Folder

```
User: "Run plan quality gate workflow for plans/in-progress/"
```

The AI will invoke agents with scoped validation:

- Validate only in-progress plans
- Fix issues in those plans only
- Iterate until zero findings in scope

## Validate Single Plan

```
User: "Run plan quality gate workflow for plans/in-progress/new-feature/plan.md"
```

The AI will invoke agents with single-file scope:

- Validate specific plan file only
- Fix issues in that file
- Iterate until plan is clean

## With Iteration Bounds

```
User: "Run plan quality gate workflow for all plans with min-iterations=2 and max-iterations=10"
```

The AI will invoke agents with iteration controls:

- Require at least 2 check-fix cycles
- Cap at maximum 10 iterations
- Report final status after completion
