---
description: The two failure modes (lost context, invisible drift) a live task list prevents, and why the practice carries no step-count threshold
when_to_use: Use when deciding how this practice reaches a specific piece of work.
---

# Purpose and Scope

## Purpose

Two failure modes emerge when task lists are absent or stale:

1. **Lost context**: Multi-step work involves dozens of intermediate decisions. Without a live task list, an agent that loses context mid-task (due to compaction, interruption, or session restart) has no recoverable map of what was done, what is in progress, and what remains. Recovery requires re-reading output artifacts and reconstructing intent — slow and error-prone.

2. **Invisible drift**: An agent that marks work done before it is finished, or that does work without marking it started, produces a list that no longer reflects reality. Anyone reading the list — human or agent — receives incorrect information about task state. Decisions made on incorrect task state compound into larger problems.

A live, continuously-synced task list prevents both failures by making progress observable and recoverable at every step.

## Scope

### What This Practice Covers

- **Any task**, whatever its size — a one-line edit, a rename, a question answered in prose
- Purely conversational work, which opens or adjusts an entry like any other task
- Both the harness's native task list and plan delivery checklists when used as a live working list during execution

The threshold is deliberately absent. A step-count trigger asks the agent to estimate the work before recording it, and that estimate is made at exactly the moment it is least reliable.

## Enforcement Disposition

**Unenforced by decision.** This practice governs in-session behaviour that leaves no artifact in
the repository, so no gate can observe compliance: a task list lives in harness state, not in the
working tree, and a commit looks identical whether or not one was kept. Declaring a gate here would
produce a check that always passes.

The obligation is therefore carried by the instruction surface and by the
`repo-maintaining-task-lists` agent skill, which reach the main thread and delegated agents
respectively. Enforcement is review-time and human: a session that produced work with no
corresponding list entries is the violating observation.

### What This Practice Does NOT Cover

- Plan-file delivery checklists at rest (those are governed by the [Plans Convention](../../../conventions/structure/plans.md))
