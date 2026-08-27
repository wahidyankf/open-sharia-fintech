---
name: repo-maintaining-task-lists
description: The task-list obligation every agent carries — open the harness's native task list before any task, conversational ones included, and keep it in sync with actual progress. Auto-loads whenever work is about to begin.
when_to_use: Use before starting any piece of work, and whenever progress on that work changes.
---

# Maintaining Task Lists

Delegated agents do not inherit the canonical instruction file. This Skill is how the task-list
obligation reaches them, and it binds a delegated agent exactly as it binds the main thread.

## The Obligation

**Before any task — including a purely conversational one — create, update, or adjust the harness's
native task list.** The list is opened before the work starts, not reconstructed after it finishes.

There is no step-count threshold. A one-line edit, a rename, and a question answered in prose all
open or adjust an entry. A threshold would ask you to estimate the work before recording it, at
exactly the moment that estimate is least reliable.

## Standards

1. **Create before executing.** The primary phases are recorded before the first tool call. The
   list need not be exhaustive at the start — it grows as work proceeds.
2. **Mark in-progress before starting.** A task reading `pending` while its work is underway is a
   stale list, which is a defect rather than a minor gap.
3. **Mark completed immediately after verification.** Completion means the stated outcome exists
   and has been confirmed — not that it ought to be done by now.
4. **Add discovered tasks on the spot.** A follow-up that is not recorded is invisible.
5. **One task per concrete outcome.** Split bundled work before starting it.
6. **Preserve active rule decisions.** Immediately record every unsuperseded user-established
   repository-rule decision constraining the work with its operative statement, scope, source, and
   status. Reproduce active entries in every compaction summary and handoff. Before the first action
   after restored context or continuation, re-read canonical instructions and reconcile the record;
   stop and report any unresolved conflict.

## What Does Not Satisfy This

- A list written after the work, describing what already happened.
- Prose narration of progress in place of list entries.
- A list created at the start and never updated again.

## Harness Note

Use whatever native task mechanism your harness provides. Where the harness exposes task creation
and status-update tools, those tools are the list; the obligation is the same either way.

## Related

- [Task List Discipline](../../../repo-governance/development/practice/task-list-discipline.md) —
  the governing practice, including the status-update cadence and the anti-patterns catalog.
- [Continuation-State Integrity](../../../repo-governance/development/agents/agent-workflow-orchestration/continuation-state-integrity.md) —
  the durable active-decision record and before-resume reconciliation gate.
- `repo-understanding-shared-vocabulary` — what counts as one delivery unit when scoping entries.
