---
title: "Finalization and Archival — PR Merge, Cleanup, and Final Status"
description: Defines the PR-mode merge and prompted worktree-cleanup steps, and the final pass/partial/fail status determination.
when_to_use: Use when merging a plan's delivering PR, cleaning up its worktree afterward, or determining the plan's final status.
---

1. **Merge — `[AI]` by default**: once the done-definition is fully satisfied and the hardened
   merge preconditions (a)-(e) hold, surface the PR URL and the done-definition checklist, then
   merge. A `[HUMAN]` merge gate applies only where the plan's own step says so explicitly — in
   that case, hand off the ready-to-merge PR and STOP instead of merging. The preconditions are
   identical in both cases; only the actor differs. See
   [Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode).
2. **Worktree cleanup — prompted (after the merge completes)**: once the PR is confirmed
   merged, offer to delete the plan's worktree, using the same safety preconditions and
   prompt mechanics as the direct-push path, but gated on merge completion instead of push
   completion:
   1. **Verify nothing unpushed and the merge landed** (safety precondition):

      ```bash
      git -C worktrees/<plan-identifier> status --porcelain   # must be empty
      git fetch origin
      git merge-base --is-ancestor "$(git -C worktrees/<plan-identifier> rev-parse HEAD)" origin/main   # must succeed, post-merge
      ```

      If either check fails, do NOT offer deletion — surface what is uncommitted or unmerged and keep the worktree.

   2. **Prompt the user** (interactive question — this is a sanctioned stop): `PR merged. Delete worktree worktrees/<plan-identifier>/ and its local branch?` NEVER delete the worktree without explicit user confirmation, and never before the merge is confirmed.
   3. **On approval**, from the repo root:

      ```bash
      git worktree remove worktrees/<plan-identifier>
      git worktree prune
      git branch -d <plan-identifier> 2>/dev/null || true   # safe delete; only succeeds when fully merged
      ```

      If `git worktree remove` refuses (unexpected dirty state), do NOT force — re-run the safety precondition and escalate to the user.

   4. **On decline**: keep the worktree and emit one line: `Worktree retained at worktrees/<plan-identifier>/ per user choice.`

- If status is `partial` or `fail`: Leave plan in current location, do NOT archive, and do NOT delete the worktree — in-flight work stays available for the next execution attempt

**Output**: `{final-status}`, `{iterations-completed}`, `{final-report}`

**Status determination**:

- PASS: **Success** (`pass`): Zero findings after validation, all requirements met, AND all infrastructure-apply steps in the delivery checklist (`terraform apply`, live Ansible converge, or equivalent) are verified-executed from the primary checkout — plan moved to `plans/done/`
- **Partial** (`partial`): Findings remain after max-iterations, OR an infrastructure-apply step (`terraform apply`, live Ansible converge, or equivalent per the Step 0 policy) remains unexecuted from the primary checkout — plan stays in current location
- FAIL: **Failure** (`fail`): Technical errors during execution or checking, plan stays in current location

**Depends on**: Reaching this step from step 4, 6, or 7
