---
title: "Task List Discipline"
description: For any non-trivial multi-step work (3+ distinct steps, or any task spanning multiple files or phases), maintain a live task list from the start and keep it continuously in sync with actual progress
category: explanation
subcategory: development
tags:
  - task-management
  - planning
  - execution
  - ai-agents
  - discipline
created: 2026-06-23
---

# Task List Discipline

For any non-trivial multi-step work, maintain a live task list from the start and keep it continuously in sync with actual progress. A task list that lags behind reality is a defect — not a detail.

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md)**: Creating a task list before starting multi-step work forces deliberate scoping. It surfaces assumptions, identifies dependencies, and reveals missing context before execution begins — not mid-way through.

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: A task list makes the work plan explicit and shared. Progress, remaining work, and newly discovered tasks are visible rather than held in the agent's context window as implicit state that degrades with distance.

- **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)**: Keeping the task list current using the harness Task tool (TaskCreate / TaskUpdate) automates progress tracking. It replaces ad-hoc mental bookkeeping with a durable, queryable record.

- **[Progressive Disclosure](../../principles/content/progressive-disclosure.md)**: A task list layers complexity appropriately: start with the known steps, then add newly-discovered follow-up tasks as they surface. Complexity accretes in the list, not in the agent's informal prose output.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Content Quality Principles](../../conventions/writing/quality.md)**: This document follows active voice, proper heading hierarchy, and accessible examples throughout.

- **[File Naming Convention](../../conventions/structure/file-naming.md)**: This document uses a lowercase kebab-case filename consistent with repository naming rules.

The following structural convention also informs this practice:

- **[Plans Convention](../../conventions/structure/plans.md)**: That convention governs plan-file delivery checklists (the checklist living inside `delivery.md` or a plan document). This practice governs the live working task list for everyday multi-step execution. Both require continuous sync; they serve different scopes.

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
- Plan-file delivery checklists at rest (those are governed by the [Plans Convention](../../conventions/structure/plans.md))

## Standards

### Standard 1 — Create the List Before Starting

For any qualifying task, the agent MUST create the task list **before** beginning execution. The list captures the known steps at the start. It is not necessary to enumerate every sub-step upfront — the list grows as work proceeds — but the primary phases or deliverables MUST be recorded before the first file edit or tool call.

**Tool**: Use the harness `TaskCreate` tool (or the plan's delivery checklist if the work lives inside an active plan). One task per concrete, actionable outcome.

### Standard 2 — Mark In Progress Before Starting

Before beginning any task, the agent MUST update its status to `in_progress`. This is non-negotiable. A task whose status reads `pending` while its underlying work has already started is a stale list — a defect, not a minor gap.

**Rationale**: The `in_progress` marker is the recovery anchor. If the session is interrupted, a reader can immediately identify where work was underway and what needs revalidation.

### Standard 3 — Mark Completed Immediately

The moment a task's concrete outcome is achieved and verified, the agent MUST update its status to `completed`. "Immediately" means in the same turn or the turn immediately following the concluding verification — not deferred to a cleanup pass at the end of the batch.

**What counts as completed**: The task's stated outcome exists and has been verified (e.g., file written and readable, test passing, link resolving). A task is not completed because the agent believes it should be done — only because the outcome is confirmed.

### Standard 4 — Add Newly-Discovered Tasks as They Surface

When execution reveals a task that was not in the original list — a dependency that must be resolved, a follow-up fix that must be made, a validation step that must be added — the agent MUST add it to the list immediately, before continuing. Discovered tasks that are not recorded are effectively invisible.

### Standard 5 — One Task Per Concrete Outcome

Each task entry MUST represent one concrete, actionable outcome. Bundling unrelated work into a single task obscures progress and makes status reporting unreliable.

**Good**: "Write parallel-by-default.md practice doc"
**Bad**: "Write both practice docs and update indexes and fix subagent cap"

Large deliverables that require multiple steps should be broken into the component steps as separate tasks.

### Standard 6 — Bounded Status-Update Cadence (3-5 Minutes, Not Faster)

While task-list items are active, give the user a progress update every **3-5 minutes — not faster**.

The bound runs in both directions, and both matter:

- **Not slower.** Long silent stretches leave the user unable to tell progress from a stall. The task
  list is the primary observability surface; if it goes quiet, there is nothing else to read.
- **Not faster.** A status update per micro-event is update-storming: it buries the signal that
  something actually changed under a stream of noise, which costs the user more attention than
  silence would. Batch the small stuff into the next scheduled update.

Anchor updates to **meaningful state changes** — a checkbox ticked, a gate turning green or red, a
phase boundary crossed, a blocker surfacing — rather than to a timer alone. The 3-5 minute window is
the pacing bound, not an instruction to emit an update on a schedule when nothing has changed.

## Anti-Patterns

### Starting Without a Task List

**Problem**: The agent begins a multi-step task immediately, tracking progress in its internal context rather than an explicit list.

**Why it fails**: Context compaction or session interruption loses all implicit progress tracking. Recovery requires re-examining every output artifact to reconstruct state. Re-examination misses things.

**Fix**: Create the task list before the first edit or tool call.

---

### Marking Done Before Verifying

**Problem**: The agent marks a task completed as soon as it issues the write or edit — before confirming the outcome is correct.

**Why it fails**: The completed marker signals to any subsequent reader that the outcome was verified. If the write failed or the edit produced incorrect output, the list lies. Decisions made on a lying list compound into larger problems.

**Fix**: Verify the outcome (file exists, test passes, link resolves) before marking completed.

---

### Deferred Cleanup

**Problem**: The agent accumulates un-updated tasks throughout a batch, then does a single status sweep at the end to "clean up" the list.

**Why it fails**: During the batch, the list is stale. Any interruption — session restart, rate-limit timeout, stuck detection — leaves an unrecoverable state. The batch cannot be safely resumed because the list does not reflect actual progress.

**Fix**: Update each task's status immediately when its state changes.

---

### Recording Discovered Work Without Adding to List

**Problem**: The agent notices a follow-up fix is needed, mentions it in a response, but does not add it to the task list.

**Why it fails**: Mentioned-but-not-recorded tasks have the same lifecycle as all passively-mentioned problems: they get lost. The follow-up fix either never happens or requires the user to track it manually.

**Fix**: Add discovered tasks to the list immediately. See [Proactive Preexisting Error Resolution](./proactive-preexisting-error-resolution.md) for the complementary rule on handling discovered errors.

---

### Monolithic Tasks

**Problem**: The agent creates one task called "Implement feature X" that covers all sub-steps, then marks it in_progress at the start and completed at the end with no intermediate updates.

**Why it fails**: A monolithic task provides no progress signal during execution. At any interruption point, the state reads "in progress" — which says nothing about how far along the work is or where to resume.

**Fix**: Break the deliverable into component tasks. Each sub-step that has a verifiable outcome gets its own task entry.

## For AI Agents

All agents doing qualifying multi-step work must follow this practice:

1. **Create the task list before execution** — use TaskCreate for the known primary tasks
2. **Mark each task `in_progress` before starting it** — never start work on a pending task without updating its status first
3. **Mark each task `completed` immediately after verification** — same turn or immediately following
4. **Add discovered tasks on the spot** — no deferring, no "I'll add it later"
5. **One task per concrete outcome** — split bundled tasks before starting them

### Relationship to Plans Delivery Checklists

The [Plans Convention](../../conventions/structure/plans.md) governs the delivery checklist inside plan documents (`delivery.md`). That checklist is the authoritative progress record for plan-mediated work. This practice governs the live working task list for everyday multi-step execution outside a plan document — and for the in-session tracking state during plan execution itself. Both require continuous sync. Neither exempts the other.

## Related Documentation

- [Plans Convention](../../conventions/structure/plans.md) - Governs plan-file delivery checklists; complementary scope to this practice
- [Proactive Preexisting Error Resolution](./proactive-preexisting-error-resolution.md) - Handling discovered errors during work; pairs with Standard 4 on adding discovered tasks
- [Agent Workflow Orchestration Convention](../agents/agent-workflow-orchestration.md) - Broader agent task management strategy including plan mode and verification loops
- [Deliberate Problem-Solving](../../principles/general/deliberate-problem-solving.md) - Think before acting; surface assumptions; do not proceed without a plan
- [Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md) - Explicit state over implicit context
