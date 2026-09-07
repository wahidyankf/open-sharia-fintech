---
description: Record active user-established repository-rule decisions and restore them before resumed work.
when_to_use: Use when a user establishes a rule decision or when work resumes from compacted or handed-off state.
---

# Standard 7 — Preserve Continuation State

The task list or its durable continuation record must carry every active user-established
repository-rule decision constraining the work. Record the operative statement, scope, source, and
status immediately; reproduce active entries in every compaction summary and handoff.

Before the first resumed action, re-read canonical instructions and reconcile the record under
[Continuation-State Integrity](../../agents/agent-workflow-orchestration/continuation-state-integrity.md).
Do not mark an entry superseded without naming its superseding source. An unresolved conflict stops
execution and is reported instead of silently weakening either statement.

The [file-touch ledger](../file-touch-discipline.md) remains a separate required record. Preserve and
cross-link it; do not reconstruct ownership from the task list or incoming Git changes.
