---
title: "Task Management"
description: "Covers planning first, tracking progress, granular task items, using the Task tool for multi-step work, documenting results, and capturing lessons."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - workflow
  - orchestration
created: 2025-11-23
when_to_use: Use when managing the task list for a multi-step piece of work.
---

# Task Management

## Plan First

Write the plan before starting implementation. This is not optional for non-trivial tasks.

## Track Progress

Mark items complete as you go. An updated checklist shows what has been done and what remains. This matters when tasks are interrupted or when reporting progress.

## Use Granular Task Items

Each item in a task list or plan checklist must represent one independently completable unit of work. This applies to `local-tmp/todo.md` plans and to any checklist an agent produces in delivery plans.

**Rule**: One item = one concrete action. Never bundle multiple steps behind a single checkbox.

**Bad** (too coarse):

```markdown
- [ ] Add coverage merging with all formats and tests
```

**Good** (granular):

```markdown
- [ ] Create `internal/testcoverage/merge.go` with format-agnostic merge logic
- [ ] Implement `CoverageMap` type for normalized per-line data
- [ ] Add parsers to return `CoverageMap` from each format
- [ ] Write unit tests for merge logic (same format, cross-format, overlapping)
```

**Why this matters**:

- Progress visibility during long-running operations — each completed item is observable progress
- Resume capability when context is compacted — a granular list shows exactly where execution stopped
- Clear audit trail — coarse items leave ambiguity about what was actually done

**Test for granularity**: Can you verify the item is done without completing anything else on the list? If the answer is no, split it.

## Use the Task Tool for Multi-Step Work

When working on tasks with multiple steps, agents MUST use `TaskCreate` and `TaskUpdate` to track progress programmatically. This is in addition to updating markdown checklists.

- **TaskCreate**: Create a task for each granular work item before starting
- **TaskUpdate** (`in_progress`): Mark the task when you begin working on it
- **TaskUpdate** (`completed`): Mark the task when it is done

This provides real-time progress tracking that survives context compaction and makes the agent's work observable to the user without needing to read files.

## Document Results

Add a review section to `local-tmp/todo.md` after completing the task. The review captures:

- What the task accomplished
- Any significant decisions made during execution
- Anything that should inform future similar tasks

## Capture Lessons

After any correction, update `local-tmp/lessons.md`. This is the direct application of the self-improvement loop to task management.
