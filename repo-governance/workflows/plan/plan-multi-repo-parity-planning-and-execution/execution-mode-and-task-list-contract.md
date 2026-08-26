---
title: "Execution Mode and Task List Contract"
description: States that direct orchestration is mandatory and defines the composite-wide granular Task list contract that keeps the live task list in sync with disk.
when_to_use: Use when starting the composite, to confirm orchestration mode and set up the live Task list correctly.
---

# Execution Mode and Task List Contract

**Direct Orchestration** — the calling context (the top-level assistant session) is the
orchestrator for the whole composite. This is mandatory, not preferred: plan-execution requires
calling-context orchestration so the live Task list stays visible to the user in real time.
Within the planning phase, the orchestrator delegates exactly as
plan-multi-repo-parity-planning specifies (`plan-maker`, `web-researcher`, `plan-checker`,
`plan-fixer` via the Agent tool). Within the execution phase, it delegates per-item work to
specialized agents exactly as plan-execution specifies, and invokes `plan-execution-checker` for
independent validation.

**How to Execute**:

```
User: "Run plan-multi-repo-parity-planning-and-execution for objective: standardize markdown gates"
```

## Granular Task List Contract (Composite-Wide, Non-Negotiable)

The harness Task list (`TaskCreate` / `TaskUpdate`) is the user's only real-time view of this
long-running composite. It MUST stay granular, current, and in sync from the first survey through
each repo's immediate, precondition-gated worktree cleanup.

**Composite-level tasks** (created at workflow start):

- `TaskCreate` exactly one task per composite step: each planning step (survey, matrix, first
  grill, research, second grill, authoring per repo, gate per plan, delivery), the phase gate,
  the pre-execution grill, one execution placeholder per repo, and cross-repo finalization.
- At most ONE task `in_progress` at any moment, across the entire composite.
- Mark a task `in_progress` BEFORE the first tool call advancing it; mark `completed` only when
  its output criterion is met.

**Execution-phase expansion (flattened delivery checklist)**: when the execution phase reaches
repo R, the orchestrator expands R's placeholder by reading R's `delivery.md` and appending the
delivery checklist to the live Task list as a **flattened** set of tasks — exactly as
[plan-execution §Task-Checklist Synchronization](../plan-execution/task-checklist-synchronization.md#task-checklist-synchronization)
mandates:

- One `TaskCreate` per remaining `- [ ]` checkbox, INCLUDING every nested sub-bullet — each
  sub-bullet is its own task, never rolled into its parent. Nesting on disk becomes a flat,
  reading-order sequence of tasks in the list (prefix titles with the repo name for parity runs,
  e.g., `ose-private: add markdownlint gate to CI`).
- Strict 1:1 mapping both directions: every checkbox has exactly one task; every task has exactly
  one checkbox. Verify `count(remaining checkboxes) == count(created tasks)` before starting.
- The Atomic Sync Ritual governs every completion: tick the checkbox on disk, persist
  implementation notes under it, `TaskUpdate completed` — all three together, never batched,
  never deferred. The on-disk checkbox state never lags more than one `Edit` call behind the
  task state.
- Disk is truth on resume: re-entering the composite rebuilds the Task list from each
  `delivery.md`, never from memory.

**Forbidden** (inherited verbatim from plan-execution Iron Rule 1): coarse tasks ("Execute
Phase 2", "Run repo B"), bulk creation, silent batch completion, speculative completion, title
rewriting. A violation triggers immediate stop, reconciliation (disk wins), and resume one
checkbox at a time.
