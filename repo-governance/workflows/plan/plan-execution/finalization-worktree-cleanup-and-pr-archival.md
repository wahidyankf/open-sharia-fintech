---
title: "Finalization and Archival — Direct-Push Worktree Cleanup and PR-Mode Archival"
description: Defines the prompted worktree-cleanup flow for direct-push modes and the archival-in-PR steps for *-to-pr modes.
when_to_use: Use when cleaning up a plan's worktree after a direct push, or moving a plan folder to done/ inside a delivering PR.
---

1. **Worktree cleanup — prompted (after archival pushed)**: once the archival commit is pushed to `origin main` and CI is green, offer to delete the plan's worktree so worktrees do not accumulate:
   1. **Verify nothing unpushed** (safety precondition — both checks MUST pass before offering deletion):

      ```bash
      git -C worktrees/<plan-identifier> status --porcelain   # must be empty
      git fetch origin
      git merge-base --is-ancestor "$(git -C worktrees/<plan-identifier> rev-parse HEAD)" origin/main   # must succeed
      ```

      If either check fails, do NOT offer deletion — surface what is uncommitted or unpushed and keep the worktree.

   2. **Prompt the user** (interactive question — this is a sanctioned stop): `Plan complete and pushed to origin main. Delete worktree worktrees/<plan-identifier>/ and its local branch?` NEVER delete the worktree without explicit user confirmation.
   3. **On approval**, from the repo root:

      ```bash
      git worktree remove worktrees/<plan-identifier>
      git worktree prune
      git branch -d <plan-identifier> 2>/dev/null || true   # safe delete; only succeeds when fully merged
      ```

      If `git worktree remove` refuses (unexpected dirty state), do NOT force — re-run the safety precondition and escalate to the user.

   4. **On decline**: keep the worktree and emit one line: `Worktree retained at worktrees/<plan-identifier>/ per user choice.`

**`worktree-to-pr` / `main-to-pr` (`*-to-pr` modes)** — archival-in-PR: the plan-folder move lands
inside the delivering PR itself, gated by the PR-Review Maker→Fixer Cycle, before the merge
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

7. **Run or complete the PR-Review Maker→Fixer Cycle** against the PR (see the gate above) — because
   each cycle's reviewer pipeline (`pr-review-scout-maker` → nine specialists → `pr-review-synthesis-maker`) reviews the full
   current state of the PR, its final pass also covers this archival commit. Confirm all four done-definition items are satisfied: N cycles
   complete, every comment answered, all gates GREEN (including CI on this last push), and the
   archival commit present on the PR branch.
