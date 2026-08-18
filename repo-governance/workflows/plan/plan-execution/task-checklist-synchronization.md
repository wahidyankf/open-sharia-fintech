---
title: "Task-Checklist Synchronization"
description: Establishes that the live Task list and on-disk delivery.md are two views of one state that must always agree, and states the strict 1:1 checkbox-to-task mapping.
when_to_use: Use when reconciling the harness Task list against delivery.md, or confirming every checkbox maps to exactly one task.
---

# Task-Checklist Synchronization

The live Task list (`TaskCreate` / `TaskUpdate`) and the on-disk delivery checklist (`delivery.md`) are two views of the same state. They MUST agree at every moment of execution. Disagreement is a bug the orchestrator MUST detect and fix immediately.

- **Task list** — ephemeral, in-conversation. Its role is **real-time progress visibility for the user**. A reader watching the Task list is watching execution happen.
- **Delivery checklist** — persistent, on-disk. Its role is **survival across conversations**. It is the source of truth for plan completion state.

## 1:1 Mapping (strict)

Every checkbox on disk has exactly ONE matching task in the live list. Every task has exactly ONE matching checkbox on disk. This includes nested `- [ ]` sub-bullets — each sub-bullet is its own task, not rolled into its parent. Task titles short-form the checkbox text so reader sees consistent wording in both views.

Forbidden: coarse tasks ("Execute Phase 2", "Update all agents"), bulk creation ("one task for every phase"), silent completion ("ticked three boxes in one Edit, one `TaskUpdate` at the end"). Each of these breaks the user's monitoring view.
