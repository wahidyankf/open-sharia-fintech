---
description: Read every newly integrated commit's full diff and reconcile its impact before the next task action.
when_to_use: Use immediately after a rebase, pull, merge, cherry-pick, or fast-forward introduces commits not previously on the current branch.
---

# Integration Diff Review Convention

Any Git integration that introduces commits not previously present on the current branch changes the
ground under the active task. Branch membership, not authorship, defines an incoming commit. A clean
integration with zero textual conflicts does not prove that the incoming changes are irrelevant.
Before the next task action, identify the incoming range, read its full diff, and reconcile its effect
on the current task, whole plan, active assumptions, file-touch ledger, and verification state.

## Contents

- [Principles and Conventions Implemented](./integration-diff-review/principles-and-conventions-implemented.md) — Why this convention exists and its companion conventions.
- [The Rule and Reading Checklist](./integration-diff-review/the-rule-and-reading-checklist.md) — The five-step rule, and what to look for in the diff.
- [Commands and Agent Responsibilities](./integration-diff-review/commands-and-agent-responsibilities.md) — The exact commands per operation, and who is responsible.
- [Forbidden Actions and Examples](./integration-diff-review/forbidden-actions-and-examples.md) — What violates this convention, with worked pass/fail examples.

## Related Documentation

- [No Destructive Git Operations Convention](../workflow/no-destructive-git-operations.md) — the
  companion convention for which local git operations are safe to run at all.
- [Agent Workflow Orchestration](../agents/agent-workflow-orchestration.md) — the same-machine
  assumption that makes concurrent, unreviewed integration events likely.
- [CI Post-Push Verification Convention](../workflow/ci-post-push-verification.md) — the parallel
  post-push discipline: verify after you push out, review after you pull in.

## Enforcement Disposition

**Unenforced by decision.** Git can expose the incoming range, but a repository-local check cannot
observe whether a contributor understood its semantic impact or adjusted every affected assumption,
plan step, ledger boundary, and verification claim. Review and workflow checkpoints enforce this
judgment obligation.
