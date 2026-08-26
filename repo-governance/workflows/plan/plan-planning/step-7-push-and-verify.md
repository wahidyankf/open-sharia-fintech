---
title: "Step 7 — Push and Verify"
description: Describes the commit, push, CI-monitoring, and worktree-removal sequence that finishes plan-establishment.
when_to_use: Use when pushing a finished plan to its confirmed target and monitoring CI before removing the worktree.
---

# Step 7. Push and Verify (Sequential)

Commit and push the plan to the confirmed target, then remove the worktree.

**Orchestrator action**:

1. From inside the worktree (`worktrees/<identifier>/`), stage all plan files:
   `git add <plan-dir>`
2. Commit inside the worktree: `chore(plans): establish <identifier> plan` (for
   `target-stage=backlog`, use `chore(plans): add <identifier> to backlog`)
3. Push from the worktree to the confirmed target (default `origin main`):
   `git push <confirmed-target> HEAD:main`
4. Monitor GitHub Actions: `gh run list --limit 5` — verify all workflows triggered by the push
   complete with `completed/success` conclusion.
5. If a CI workflow fails: diagnose root cause, fix, push a follow-up commit, re-monitor
6. After CI passes, resolve the exact worktree path from the plan's Provisioned Worktree Identity and
   reconcile it with `git worktree list --porcelain`. Inventory every plan-created and current branch.
   Continue only if the identity matches, the exact worktree is clean and idle, no inventoried branch
   is unpushed, and each direct-push delivery reached `origin/main` with no open PR. Do not use
   `origin/main` ancestry for a squash-merged PR branch. When every check passes, remove the exact
   path immediately, without a further prompt, using non-force removal:

   ```bash
   git worktree remove <exact-plan-worktree-path>
   ```

   Then follow canonical branch cleanup. If any check or removal fails, retain the worktree,
   surface the evidence, and escalate; never force removal.

7. Emit a user-visible summary: plan path, quality gate status, push target, CI status

**Output**: `plan-path`, `final-status`, `final-report`.

**On push failure**: Surface the error. Do NOT retry automatically — conflicts require human
resolution.
