---
description: States that worktree creation, commit-and-push, and worktree removal are always [AI]-tagged, never [HUMAN], absent an explicit user request otherwise.
when_to_use: Use when tagging a worktree-provisioning, push, or worktree-removal step in delivery.md.
---

# Executor Tagging — Git-Mechanical Steps Are [AI]

Continues [Executor Tagging — Tags and Bias](./executor-tagging-tags-and-bias.md).

**Bias to `[AI]` (HARD RULE)**: prefer `[AI]` as much as possible and use `[HUMAN]` as little as possible. Tag a step `[HUMAN]` ONLY when it is genuinely inevitable — physically impossible for an agent, unsafe, or requiring real-world authority or credentials an agent must not hold — OR when the plan author or user has explicitly asked for `[HUMAN]` on that step. Before tagging `[HUMAN]`, first try to engineer a sanctioned `[AI]` path (for example, a scripted action through an approved guard). When both an `[AI]` and a `[HUMAN]` path would accomplish the step, choose `[AI]`.

**Git-mechanical steps are `[AI]` — worktree and push are never `[HUMAN]` by default (HARD RULE)**: three recurring lifecycle steps are routinely mis-tagged `[HUMAN]` even though an agent performs them directly with plain git commands. Tag each `[AI]`:

- **Create / provision the worktree** — `git worktree add worktrees/<id> -b <id>` is an ordinary git command the executor runs; the [plan-execution workflow](../../../workflows/plan/plan-execution.md) Step 0 gate even auto-provisions it. Tag `[AI]`, never `[HUMAN]`.
- **Commit and push** — the push target follows the plan's Delivery Mode (see [Delivery Mode](./delivery-mode-the-four-modes.md#delivery-mode) below), but the push itself is always `[AI]`. Under the repo-wide default `worktree-to-pr`, write the step as `- [ ] [AI] Commit and push to origin <pr-branch>`; under the direct-push modes (`worktree-to-origin-main`, `main-to-origin-main`), write `- [ ] [AI] Commit and push to origin main`. See the [Git Push Default Convention](../../../development/workflow/git-push-default.md). There is **no** `[HUMAN]` "review the diff and approve push" gate in either case — pushing to a PR branch is not a merge, and exact-head PR CI plus the hardened merge preconditions gate integration. Drop any approve-push gate unless the user or plan explicitly asked for an out-of-band sign-off on that change.
- **Remove the worktree after archival** — `git worktree remove worktrees/<id>` is mechanical; the executor self-confirms the safety preconditions (nothing uncommitted or unpushed), verifies that the exact path is this plan's own worktree, then removes it immediately without a confirmation prompt. Tag `[AI]`, never `[HUMAN]`.

Any of these three steps becomes `[HUMAN]` or `[AI+HUMAN]` ONLY when the user or plan explicitly requested an out-of-band approval or sign-off for that specific change. Absent that explicit request, all three are `[AI]`.
