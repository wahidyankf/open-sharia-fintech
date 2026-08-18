---
title: "Why This Workflow Exists"
description: States the two documented failure modes — hidden uncommitted evidence and concurrent same-plan work in a different location — that motivate a discovery pass before plan-execution.md.
when_to_use: Use when explaining why skipping discovery and starting plan-execution.md cold risks re-implementing, abandoning, or orphaning work.
---

# Why This Workflow Exists

**Continued from** [When to Use, and Relationship to plan-execution.md](./when-to-use-and-relationship.md).

Two failure modes already documented elsewhere in this repo's governance motivate it directly:

- A plan's worktree can hold **uncommitted evidence a merged PR doesn't reveal** — a merged PR proves
  the branch landed, not that the working tree is empty (see the [Worktree and Artifact Cleanup
  Convention](../../../development/workflow/worktree-and-artifact-cleanup.md#mandatory-pre-removal-checks)'s
  second mandatory check). Starting `plan-execution.md` cold with a freshly-provisioned worktree over
  the same plan-identifier would silently discard that work instead of continuing it.
- Concurrent work on the **same plan-identifier from a different location** — a sibling repo, a
  different worktree, or the primary checkout — is exactly the same-machine assumption every other
  governance doc here treats as ambient truth (see the [No Destructive Git Operations
  Convention](../../../development/workflow/no-destructive-git-operations.md#the-same-machine-assumption)).
  `plan-execution.md`'s own Resume Reconciliation item 6 already handles "same repo, two locations
  (primary checkout vs. worktree)"; this workflow generalizes that to "same plan, N repos, unknown
  locations."

Skipping this discovery and starting `plan-execution.md` directly against a bare `plan-path` risks
three concrete outcomes this workflow exists to prevent: (1) **re-implementing** work that already
landed, wasting the effort and creating avoidable merge conflicts against it later; (2)
**abandoning** real uncommitted work in a stale worktree by provisioning a fresh one over it; (3)
**accumulating orphans** — worktrees, branches, and build output left behind by an earlier,
interrupted attempt that nobody ever closed the loop on.
