---
title: "Starting Work — Promotion Recovery"
description: "Defines authoritative state reconciliation and resume behavior for backlog-to-in-progress promotion."
when_to_use: "Use before mutating a plan promotion, or when resuming an interrupted promotion."
---

# Starting Work — Promotion Recovery

Before any promotion mutation, fetch `origin` and reconcile the plan path, intended promotion
branch, and matching pull request against remote truth. Classify exactly one state:

1. **Unstarted** — `origin/main` contains only the backlog path, and no matching remote branch or
   pull request exists. Begin the pure move from the resolved mode's declared work location.
2. **Branch pushed** — one matching remote branch contains the expected pure move, with no pull
   request. Verify its base and diff, then open the pull request; do not recreate the branch.
3. **Pull request open** — one matching open pull request contains the expected pure move. Resume
   its review, CI, and merge path; do not open another pull request.
4. **Merged and verified** — `origin/main` contains only the in-progress path and the matching
   merged pull request or permitted direct-push commit is reachable from `origin/main`. Skip the
   mutation and continue with implementation provisioning.
5. **Anomalous** — both lifecycle paths exist, neither exists, remote artifacts disagree with the
   expected pure diff or base, duplicate branches or pull requests match, or a reported merge is
   not reachable from `origin/main`. Stop and request reconciliation; never guess or replay.

For `worktree-to-pr`, resolve the plan's declared repository-relative route against the selected
repository root in every resumable state. Reuse it only when `git worktree` registers the resulting
runtime path on the verified matching branch, its upstream
matches the verified remote branch where one exists, no duplicate checkout claims the branch, and
the worktree is clean and conflict-free. In the unstarted state, create that path from the fetched
base when it does not exist. In branch-pushed or pull-request-open state, restore a missing runtime
path from the verified matching remote branch, then resume there. A mismatched path, branch,
upstream, dirty tree, conflict, or duplicate checkout is anomalous and stops recovery; never force,
delete, or guess. Merged-and-verified needs no promotion worktree and proceeds to implementation
provisioning.

For `main-to-pr`, sync and remain in the primary checkout; never create or enter a worktree.
Direct-push modes likewise use their declared work location. After every push, pull-request open,
merge, or direct push, fetch and classify again before continuing.

This reconciliation precedes the move itself on both first entry and resume. Local branch state,
conversation history, and a missing backlog path are not evidence that the remote transition is
complete.
