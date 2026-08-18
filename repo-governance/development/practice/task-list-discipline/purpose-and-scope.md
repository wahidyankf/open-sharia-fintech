---
title: "Task List Discipline — Purpose and Scope"
description: The two failure modes (lost context, invisible drift) a live task list prevents, and exactly what qualifying work this practice covers and does not cover
category: explanation
subcategory: development
tags:
  - task-management
  - planning
  - execution
  - ai-agents
  - discipline
created: 2026-06-23
when_to_use: Use when deciding whether a specific piece of work qualifies for this practice.
---

# Purpose and Scope

## Purpose

Two failure modes emerge when task lists are absent or stale:

1. **Lost context**: Multi-step work involves dozens of intermediate decisions. Without a live task list, an agent that loses context mid-task (due to compaction, interruption, or session restart) has no recoverable map of what was done, what is in progress, and what remains. Recovery requires re-reading output artifacts and reconstructing intent — slow and error-prone.

2. **Invisible drift**: An agent that marks work done before it is finished, or that does work without marking it started, produces a list that no longer reflects reality. Anyone reading the list — human or agent — receives incorrect information about task state. Decisions made on incorrect task state compound into larger problems.

A live, continuously-synced task list prevents both failures by making progress observable and recoverable at every step.

## Scope

### What This Practice Covers

- Any work with **3 or more distinct steps** across one or more files or systems
- Any task that spans **multiple files or phases** regardless of step count
- Both harness TaskCreate/TaskUpdate tasks and plan delivery checklists when used as a live working list during execution

### What This Practice Does NOT Cover

- Trivial single-step work (e.g., "fix this typo", "rename this variable")
- Purely conversational work with no file changes
- Plan-file delivery checklists at rest (those are governed by the [Plans Convention](../../../conventions/structure/plans.md))
