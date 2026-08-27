---
title: "Finalization and Archival — Direct-Push Worktree Cleanup and PR-Mode Archival"
description: Defines safe direct-push cleanup and *-to-pr archival.
when_to_use: Use when cleaning up a plan's worktree after a direct push, or moving a plan folder to done/ inside a delivering PR.
---

1. **Worktree cleanup — immediate (after archival pushed)**: once the archival commit is confirmed
   on `origin/main` and CI is green, clean up a `worktree-to-origin-main` worktree in the same
   session. `main-to-origin-main` created no plan worktree, so this step is N/A for that mode.
   1. Resolve the exact path from the plan's Provisioned Worktree Identity and reconcile it with
      `git worktree list --porcelain`. Inventory every plan-created/current branch; the initial
      identity branch may differ after normal switching. Missing identity, path conflict, or
      unclassified branch blocks removal; never derive ownership from a familiar path.
   2. Apply the canonical
      [mandatory pre-removal checks](../../../development/workflow/worktree-and-artifact-cleanup/mandatory-pre-removal-checks.md):
      the exact worktree is clean and idle, every inventoried branch is pushed, and each direct-push
      delivery is present on `origin/main` with no open PR. For a PR-mode branch, its merged PR
      reviewed head must equal the inventory's recorded reviewed-head SHA, with either a matching
      current `origin/<branch>` or verified GitHub auto-deletion under enabled
      `delete_branch_on_merge`; retain and escalate any other missing/mismatched proof. A repository
      root, wildcard, missing identity, or another actor's worktree is never eligible.
   3. When every check passes, remove the exact path immediately without another confirmation
      prompt, from the repository root:

      ```bash
      git worktree remove <exact-plan-worktree-path>
      ```

      Use the non-force command only, then apply the canonical
      [branch cleanup](../../../development/workflow/worktree-and-artifact-cleanup/branch-cleanup.md)
      procedure to this plan's verified branches.

   4. If any check or removal fails, retain the worktree, surface the evidence, and escalate. Never
      force removal or silently discard dirty or unpushed work.

**`worktree-to-pr` / `main-to-pr` (`*-to-pr` modes)** — archival-in-PR: the plan-folder move lands
inside the delivering PR itself, followed by exact-current-head/base PR CI, before the merge
(`[AI]` by default; `[HUMAN]` only where the plan's own step says so):

1. Move entire plan folder from current location to `plans/done/` (same command as the direct-push
   path):

   ```bash
   git mv plans/in-progress/plan-name/ plans/done/YYYY-MM-DD__plan-name/
   ```

2. **Update `plans/in-progress/README.md`** — remove the plan entry from the list
3. **Update `plans/done/README.md`** — add the plan entry with completion date and brief summary
   (same format as above)
4. **Update any other READMEs** that reference this plan
5. **Search for orphaned references** to the old `plans/in-progress/[plan-name]` path and fix them
6. **Commit the archival and push to the PR branch** (never to `main` directly):

   ```
   chore(plans): move [plan-identifier] to done
   ```

7. **Verify the replacement `Quality gate` run** is green for the archival commit's exact PR head
   and current base. Confirm conversations are resolved, applicable finite surface gates pass, the
   secrets check is clean, and the archival commit is present. Semantic-review evidence is required
   only when the user explicitly requested that workflow for this PR.
