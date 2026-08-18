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
6. After CI passes, remove the worktree from the repo root:

   ```bash
   git worktree remove worktrees/<identifier>
   git branch -d <identifier>
   ```

7. Emit a user-visible summary: plan path, quality gate status, push target, CI status

**Output**: `plan-path`, `final-status`, `final-report`.

**On push failure**: Surface the error. Do NOT retry automatically — conflicts require human
resolution.
