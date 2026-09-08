---
description: "Covers planning first, tracking progress, granular task items, using the Task tool for multi-step work, documenting results, and capturing lessons."
when_to_use: Use when managing the task list for a multi-step piece of work.
---

# Task Management

## Plan First

Write the plan before starting implementation. This is not optional for non-trivial tasks.

## Track Progress

Mark items complete as you go. An updated checklist shows what has been done and what remains. This matters when tasks are interrupted or when reporting progress.

## Mirror Granular Delivery Actions

Each harness task represents one concrete, independently verifiable delivery action. A formal
plan's outcome section supplies shared context; every action checkbox—including separate RED,
GREEN, and REFACTOR actions—maps to its own task.

**Rule**: One task = one delivery checkbox. Split distinct actions; reject only mechanical
keystroke tasks with no separate observation.

**Bad** (activity without proof):

```markdown
- [ ] Add coverage merging with all formats and tests
```

**Good** (one verifiable action):

```markdown
- [ ] Add cross-format failing cases to `merge_test.go` and record the expected RED diagnostic
```

**Why this matters**:

- Progress visibility during long-running operations — each completed item is observable progress
- Resume capability when context is compacted — a granular list shows exactly where execution stopped
- Clear audit trail — coarse items leave ambiguity about what was actually done

**Granularity test**: Can the action be ticked without silently completing another distinct action?
If no, split it.

## Use the Task Tool for Multi-Step Work

For any task, agents MUST maintain the harness's native task list to track progress programmatically. This is in addition to updating markdown checklists.

- **TaskCreate**: Create a task for each granular work item before starting
- **TaskUpdate** (`in_progress`): Mark the task when you begin working on it
- **TaskUpdate** (`completed`): Mark the task when it is done

This provides real-time progress tracking that survives context compaction and makes the agent's work observable to the user without needing to read files.

## Preserve Active Rule Decisions

Immediately add every unsuperseded user-established repository-rule decision constraining the work
to durable task or continuation state. Record its operative statement, scope, source, and status;
reproduce active entries in every compaction summary and handoff. Before acting after continuation,
re-read canonical instructions and reconcile the restored entries under
[Continuation-State Integrity](./continuation-state-integrity.md).

## Document Results

Add a review section to `local-tmp/todo.md` after completing the task. The review captures:

- What the task accomplished
- Any significant decisions made during execution
- Anything that should inform future similar tasks

## Capture Lessons

After any correction, update `local-tmp/lessons.md`. This is the direct application of the self-improvement loop to task management.
