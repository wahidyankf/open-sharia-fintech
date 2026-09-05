---
title: "Steps"
description: The seven steps for resolving scope, gathering per-repo state, and writing a handover document.
when_to_use: Use as the step-by-step procedure when actually writing a handover document.
---

# Steps

Continues [Notes and Execution Mode](./notes-and-execution-mode.md).

1. **Resolve the plan-identifier and date.** Same resolution rule as
   [`plan-takeover-execution.md` A0](../plan-takeover-execution.md):
   the plan folder's bare slug, no date prefix. Default `date` to the current date if not supplied.
2. **Gather current state, per repo touched this session.** For each: worktree path and branch (if
   any), its HEAD commit, whether it has uncommitted changes, any PR number/state/CI status, and the
   `delivery.md` checkbox counts as of now. Prefer state already known from this session's own work
   over re-probing — but if a claim would be stale or uncertain (e.g., "PR is green" from ten minutes
   ago), re-verify rather than assert from memory.
3. **State the concrete next step**, not just the current position — "resume `delivery.md` at
   _[named step]_", not merely "Phase 6 in progress". A handover that describes where things stand but
   not what to do next still forces the reader to re-derive the plan.
4. **Write the active user-established rule-decision record.** Include every unsuperseded decision
   constraining the current work with its operative statement, scope, source, and status. Then
   capture non-obvious learned constraints that are not already written into the plan's
   own chosen technical form and `learnings.md` — a surprising tool behaviour, a governance rule that only bites at
   a specific step, a decision the user made live that isn't yet reflected in the plan's committed
   docs. Write the _why_, not just the _what_, exactly as
   [Feedback memory guidance](../../../development/quality/knowledge-capture.md) already asks of
   `learnings.md` entries — a future reader needs to judge whether the gotcha still applies, not just
   that it once did. The decision record is mandatory; learned constraints do not substitute for it.
5. **Write the document** to `local-tmp/handovers/<date>__<plan-identifier>-implementation.md`.
   `local-tmp/` is gitignored — this is a **local, single-machine handoff artifact**, not a
   cross-clone or cross-machine one; it exists to accelerate the _next session on this same disk_, per
   the same same-machine assumption the
   [Agent Workflow Orchestration Convention](../../../development/agents/agent-workflow-orchestration/operating-budgets-parallelism-budget.md)
   already documents elsewhere. Do not rely on it surviving a fresh clone or a different machine.
6. **If a handover already exists for this plan-identifier from an earlier date, leave it in place.**
   Multiple dated handovers may accumulate; `plan-takeover-execution.md`'s read side picks the
   most recent by filename date. Do not delete or overwrite an older one — it is a historical record of
   what an earlier session believed, useful if a discrepancy ever needs tracing.
7. **Report the written path back** to the user or calling context, and confirm the file is non-empty.
