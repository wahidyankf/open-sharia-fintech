---
title: "Task List Discipline — Standard 6: Bounded Status-Update Cadence"
description: The 5-minute generic / 3-minute CI-related progress-reporting cadence, how mixed batches take the tighter cadence, and how reporting cadence differs from polling cadence
category: explanation
subcategory: development
tags:
  - task-management
  - planning
  - execution
  - ai-agents
  - discipline
created: 2026-06-23
when_to_use: Use while any task-list item or background agent is in flight, to decide how often to give the user a progress update.
---

# Standard 6: Bounded Status-Update Cadence (5 Minutes Generic, 3 Minutes CI-Related)

While task-list items are active — or while any background agent is in flight — give the user a
progress update in the main thread on an interval set by the **kind of work being awaited**:

| Awaited work                                                                                  | Update interval     |
| --------------------------------------------------------------------------------------------- | ------------------- |
| **GitHub-CI-related** — Actions runs, PR checks, workflow conclusions, post-push verification | every **3 minutes** |
| **Generic** — everything else: subagent batches, refactors, doc sweeps, test runs             | every **5 minutes** |

**Mixed batches take the tighter cadence.** If any in-flight item is CI-related, the whole batch
reports at 3 minutes — the CI item is the one that can go red and block delivery.

This **assigns** the two ends of the former "3-5 minutes" range rather than leaving the choice open;
both values sit inside the old bound, so it is a refinement, not a reversal.

**Reporting cadence is not polling cadence.** This Standard governs how often the agent _speaks to
the user_. It changes nothing about how often it _checks_ anything: the never-faster-than-2-minutes
CI polling floor ([CI Monitoring Convention](../../workflow/ci-monitoring.md)) and the 3-minute
subagent stuck-detection poll ([Subagent Orchestration Convention](../../agents/subagent-orchestration.md))
both stand unchanged. Polling more often than you report is normal and expected.

The bound runs in both directions, and both matter:

- **Not slower.** Long silent stretches leave the user unable to tell progress from a stall. The task
  list is the primary observability surface; if it goes quiet, there is nothing else to read.
- **Not faster.** A status update per micro-event is update-storming: it buries the signal that
  something actually changed under a stream of noise, which costs the user more attention than
  silence would. Batch the small stuff into the next scheduled update.

Anchor updates to **meaningful state changes** — a checkbox ticked, a gate turning green or red, a
phase boundary crossed, a blocker surfacing — rather than to a timer alone. The 5-minute (generic)
and 3-minute (CI-related) intervals are the pacing bound, not an instruction to emit an update on a
schedule when nothing has changed.
