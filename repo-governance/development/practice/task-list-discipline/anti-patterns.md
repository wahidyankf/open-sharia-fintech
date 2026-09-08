---
description: Five common task-list failure patterns - starting without a list, marking done before verifying, deferred cleanup, recording discovered work without adding it, and monolithic tasks
when_to_use: Use when reviewing your own task-list behaviour for signs of one of these five failure patterns.
---

# Anti-Patterns

## Starting Without a Task List

**Problem**: The agent begins a multi-step task immediately, tracking progress in its internal context rather than an explicit list.

**Why it fails**: Context compaction or session interruption loses all implicit progress tracking. Recovery requires re-examining every output artifact to reconstruct state. Re-examination misses things.

**Fix**: Create the task list before the first edit or tool call.

---

## Marking Done Before Verifying

**Problem**: The agent marks a task completed as soon as it issues the write or edit — before confirming the outcome is correct.

**Why it fails**: The completed marker signals to any subsequent reader that the outcome was verified. If the write failed or the edit produced incorrect output, the list lies. Decisions made on a lying list compound into larger problems.

**Fix**: Verify the outcome (file exists, test passes, link resolves) before marking completed.

---

## Deferred Cleanup

**Problem**: The agent accumulates un-updated tasks throughout a batch, then does a single status sweep at the end to "clean up" the list.

**Why it fails**: During the batch, the list is stale. Any interruption — session restart, rate-limit timeout, stuck detection — leaves an unrecoverable state. The batch cannot be safely resumed because the list does not reflect actual progress.

**Fix**: Update each task's status immediately when its state changes.

---

## Recording Discovered Work Without Adding to List

**Problem**: The agent notices a follow-up fix is needed, mentions it in a response, but does not add it to the task list.

**Why it fails**: Mentioned-but-not-recorded tasks have the same lifecycle as all passively-mentioned problems: they get lost. The follow-up fix either never happens or requires the user to track it manually.

**Fix**: Add discovered tasks to the list immediately. See [Proactive Preexisting Error Resolution](../proactive-preexisting-error-resolution.md) for the complementary rule on handling discovered errors.

---

## Monolithic Tasks

**Problem**: The agent creates one task called "Implement feature X" that covers all sub-steps, then marks it in_progress at the start and completed at the end with no intermediate updates.

**Why it fails**: A monolithic task provides no progress signal during execution. At any interruption point, the state reads "in progress" — which says nothing about how far along the work is or where to resume.

**Fix**: Break the deliverable into component tasks. Each sub-step that has a verifiable outcome gets its own task entry.
