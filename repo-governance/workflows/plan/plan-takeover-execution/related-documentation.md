---
title: "Related Documentation — Plan Takeover Execution"
description: Links to the write-side handover workflow, the workflows this one hands off to, and the conventions Phases C and D apply without modification.
when_to_use: Use when navigating from plan-takeover-execution to a workflow or convention it depends on.
---

# Related Documentation

- [Plan Handover Execution](../plan-handover-execution.md) — the write-side counterpart this
  workflow's Phase A0.5 reads from; produces the `local-tmp/handovers/` document that seeds a lead
  before Phase A's own ground-truth probes run.
- [Plan Execution](../plan-execution.md) — the workflow this one hands off to; owns everything about
  single-plan delivery once the worktree is resolved.
- [Multi-Plans Execution](../multi-plans-execution.md) — the sibling scheduling-layer workflow, for
  executing several distinct plans together rather than reconciling one plan's scattered state.
- [Worktree and Artifact Cleanup Convention](../../../development/workflow/worktree-and-artifact-cleanup.md) —
  the six-check pre-removal sequence and branch/build-artifact cleanup rules Phase D applies without
  modification.
- [No Destructive Git Operations Convention](../../../development/workflow/no-destructive-git-operations.md) —
  bounds every action Phase C and Phase D may take; the "verify, never assume idle" standard both
  phases inherit.
- [File-Touch Discipline](../../../development/practice/file-touch-discipline.md) — the ledger-rebuild
  method Phase C.3 applies.
- [Worktree Path Convention](../../../conventions/structure/worktree-path.md) — the
  `worktrees/<plan-identifier>/` layout Phase A's search and Phase C's adoption both depend on.
- [Related Repositories](../../../../docs/reference/related-repositories.md) — the sibling-repo set
  Phase A1's floor is drawn from.
- [Agent Workflow Orchestration Convention](../../../development/agents/agent-workflow-orchestration.md) —
  the N+1 model and same-machine assumption this workflow's cross-repo probing and cleanup both
  operate under.
- [Plans Organization Convention](../../../conventions/structure/plans.md) — plan folder structure,
  worktree specification, and delivery-mode definitions this workflow reads to resolve `plan-path`.
