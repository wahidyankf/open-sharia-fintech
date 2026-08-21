---
title: "Task List Discipline — Standards 1-5"
description: Create the list before starting, mark in-progress before starting a task, mark completed immediately after verification, add discovered tasks on the spot, and one task per concrete outcome
category: explanation
subcategory: development
tags:
  - task-management
  - planning
  - execution
  - ai-agents
  - discipline
created: 2026-06-23
when_to_use: Use when creating or updating task entries during multi-step execution.
---

# Standards 1-5

## Standard 1 — Create the List Before Starting

For any task, the agent MUST create or update the task list **before** beginning execution. This binds delegated agents exactly as it binds the main thread. The list captures the known steps at the start. It is not necessary to enumerate every sub-step upfront — the list grows as work proceeds — but the primary phases or deliverables MUST be recorded before the first file edit or tool call.

**Tool**: Use the harness's native task list (or the plan's delivery checklist if the work lives inside an active plan). One task per concrete, actionable outcome.

## Standard 2 — Mark In Progress Before Starting

Before beginning any task, the agent MUST update its status to `in_progress`. This is non-negotiable. A task whose status reads `pending` while its underlying work has already started is a stale list — a defect, not a minor gap.

**Rationale**: The `in_progress` marker is the recovery anchor. If the session is interrupted, a reader can immediately identify where work was underway and what needs revalidation.

## Standard 3 — Mark Completed Immediately

The moment a task's concrete outcome is achieved and verified, the agent MUST update its status to `completed`. "Immediately" means in the same turn or the turn immediately following the concluding verification — not deferred to a cleanup pass at the end of the batch.

**What counts as completed**: The task's stated outcome exists and has been verified (e.g., file written and readable, test passing, link resolving). A task is not completed because the agent believes it should be done — only because the outcome is confirmed.

## Standard 4 — Add Newly-Discovered Tasks as They Surface

When execution reveals a task that was not in the original list — a dependency that must be resolved, a follow-up fix that must be made, a validation step that must be added — the agent MUST add it to the list immediately, before continuing. Discovered tasks that are not recorded are effectively invisible.

## Standard 5 — One Task Per Concrete Outcome

Each task entry MUST represent one concrete, actionable outcome. Bundling unrelated work into a single task obscures progress and makes status reporting unreliable.

**Good**: "Write parallel-by-default.md practice doc"
**Bad**: "Write both practice docs and update indexes and fix subagent cap"

Large deliverables that require multiple steps should be broken into the component steps as separate tasks.
