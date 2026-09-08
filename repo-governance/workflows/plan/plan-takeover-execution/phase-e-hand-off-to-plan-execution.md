---
description: Describes the final handoff step — invoking plan-execution.md per resolved repo, fanning out multi-repo handoffs, and closing the takeover-report.
when_to_use: Use when a repo's takeover target (or fresh start) is resolved and ready to hand off to plan-execution.md.
---

# Phase E — Hand Off to plan-execution.md (Sequential)

1. For each repo with a resolved Bucket-3 target (or a fresh Bucket-1 start), invoke
   [`plan-execution.md`](../plan-execution.md) with `plan-path` set to that repo's plan folder and the
   work branch/worktree already entered per Phase C. This satisfies its Step 0 entirely — the
   worktree gate has already passed and the freshness gate has already been applied — so execution
   begins directly at its [Step 1 (Load Delivery Checklist and Materialize Task
   List)](../plan-execution.md#1-load-delivery-checklist-and-materialize-task-list-sequential), which
   performs its own Resume Reconciliation against the now-current `delivery.md`.
2. If more than one repo resolved to Bucket 3 (or Bucket 1), run each repo's `plan-execution.md`
   invocation as an independent branch of work — the same DAG-first, N+1-bounded fan-out
   `plan-execution.md` and `multi-plans-execution.md` already use, since each repo's execution is
   independent of the others' once its own worktree is adopted.
3. Close the takeover-report with a final summary: repos probed, buckets assigned, worktrees/branches
   adopted, worktrees/branches/artifacts removed, and any anomalies escalated together with their
   resolution (if resolved during this run). This report is this workflow's terminal deliverable,
   alongside whatever `plan-execution.md` itself produces per repo handed off.
