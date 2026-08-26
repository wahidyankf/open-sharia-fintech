---
title: "Finalization and Archival — PR Merge, Cleanup, and Final Status"
description: Defines the PR-mode merge and immediate safe worktree-cleanup steps, and the final pass/partial/fail status determination.
when_to_use: Use when merging a plan's delivering PR, cleaning up its worktree afterward, or determining the plan's final status.
---

1. **Merge — `[AI]` by default**: once the done-definition is fully satisfied and the hardened
   merge preconditions (a)-(e) hold, surface the PR URL and the done-definition checklist, then
   merge. A `[HUMAN]` merge gate applies only where the plan's own step says so explicitly — in
   that case, hand off the ready-to-merge PR and STOP instead of merging. The preconditions are
   identical in both cases; only the actor differs. See
   [Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode).
2. **Paired-repository terminal handoff (when applicable)**: after the source merge and after opening
   the successor PR, complete the
   [authenticated terminal-handoff procedure](./finalization-paired-repository-terminal-handoff.md)
   before any successor scout runs.

3. **Worktree cleanup — immediate (after the merge completes)**: once the PR is confirmed merged,
   clean up a `worktree-to-pr` worktree in the same session. `main-to-pr` created no plan worktree,
   so this step is N/A for that mode.
   1. Resolve the exact path from the plan's Provisioned Worktree Identity and reconcile it with
      `git worktree list --porcelain`. Inventory every plan-created and current branch; the initial
      identity branch may differ after normal delivery-unit branch switching. A missing identity,
      path conflict, or unclassified branch blocks removal; never derive ownership from a familiar
      path.
   2. Apply the canonical
      [mandatory pre-removal checks](../../../development/workflow/worktree-and-artifact-cleanup/mandatory-pre-removal-checks.md):
      GitHub reports every PR-mode branch merged (and every direct-push branch delivered with no
      open PR), the exact worktree is clean and idle, and no inventoried branch has an unpushed
      commit. Do not substitute commit ancestry for the PR merge check because these repositories
      squash-merge.
   3. When every check passes, remove the exact path immediately without another confirmation
      prompt, from the repository root:

      ```bash
      git worktree remove <exact-plan-worktree-path>
      ```

      Use the non-force command only, then apply the canonical
      [branch cleanup](../../../development/workflow/worktree-and-artifact-cleanup/branch-cleanup.md)
      procedure to this plan's verified branches.

   4. If any check or removal fails, retain the worktree, surface the evidence, and escalate. Never
      force removal or silently discard dirty, unpushed, unmerged, or another actor's work.

- If status is `partial` or `fail`: Leave plan in current location, do NOT archive, and do NOT delete the worktree — in-flight work stays available for the next execution attempt

**Output**: `{final-status}`, `{iterations-completed}`, `{final-report}`

**Status determination**:

- PASS: **Success** (`pass`): Zero findings after validation, all requirements met, AND all infrastructure-apply steps in the delivery checklist (`terraform apply`, live Ansible converge, or equivalent) are verified-executed from the primary checkout — plan moved to `plans/done/`
- **Partial** (`partial`): Findings remain after max-iterations, OR an infrastructure-apply step (`terraform apply`, live Ansible converge, or equivalent per the Step 0 policy) remains unexecuted from the primary checkout — plan stays in current location
- FAIL: **Failure** (`fail`): Technical errors during execution or checking, plan stays in current location

**Depends on**: Reaching this step from step 4, 6, or 7
