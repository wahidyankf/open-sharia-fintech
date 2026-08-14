---
title: "Load Delivery Checklist and Materialize Task List"
description: Defines how the orchestrator reads the plan, reconciles prior-run state, and materializes the live Task list before implementation begins.
when_to_use: Use when starting or resuming plan execution and building the initial Task list from delivery.md.
---

# 1. Load Delivery Checklist and Materialize Task List (Sequential)

Read the plan in full, reconcile against any prior run's state, and build the live Task list to mirror disk truth — before any implementation work begins.

**Orchestrator action**:

- Read the plan at `{input.plan-path}` — all five docs if present (`README.md`, `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md`) or the legacy four-doc layout (`requirements.md` in place of `brd.md` + `prd.md`).
- Read `tech-docs.md`'s annotated `## File-Impact Analysis` tree before materializing tasks. Treat it
  as the plan's declared footprint: reconcile each delivery path against its `[E]`/`[N]`/`[D]`/`[G]`
  marker and surface a mismatch before touching an undeclared path. `### More Detail` supplies
  context only; it does not expand the footprint.
- Locate the delivery checklist — typically `delivery.md` adjacent to the plan, or embedded in a single-file plan's `README.md`.
- **Resume Reconciliation (Iron Rule 10)**: parse every checkbox top-to-bottom. For each `- [x]`, count it as done and skip it. For each `- [ ]`, queue it for task creation in reading order. If a stale Task list from a prior run disagrees with disk, delete it and rebuild.
- **Full granularity parsing (Iron Rule 1)**: identify every `- [ ]` AND every nested `- [ ]` sub-bullet. Nested sub-bullets are NOT rolled into their parent — each gets its own task.
- **`TaskCreate` one task per remaining checkbox**, in reading order. Task titles short-form the checkbox text for monitoring parity.
- **Verify 1:1 mapping** before moving on: `count(remaining - [ ] in delivery.md) == count(newly-created tasks)`. Diverging counts indicate a parsing bug — stop and reconcile.
- Do NOT call `TaskUpdate in_progress` yet; that happens at Step 2 when the loop actually begins on an item.

**Output**: Live Task list mirrors delivery.md remaining items 1:1, plan context loaded.

**On failure**: Terminate workflow with status `fail`.

**Notes**:

- Tasks map 1:1 to checkboxes, including nested sub-bullets — NEVER group multiple items into one task, NEVER roll sub-bullets into their parent.
- Tasks must be granular — one concrete action per task.
- Preserve the exact phase and item ordering from delivery.md in the Task list.
- Already-ticked items are skipped — the plan is resumable across conversations; disk is truth.
