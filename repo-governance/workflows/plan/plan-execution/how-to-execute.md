---
title: "How to Execute"
description: Lists the 12 top-level actions (0-11) the calling context performs when a user asks it to execute a plan.
when_to_use: Use when tracing the exact ordered actions plan execution performs, from backlog promotion through worktree cleanup.
---

# How to Execute

**Continues** [Execution Mode](./execution-mode.md).

**How to Execute**:

```
User: "Execute plan plans/in-progress/new-feature/plan.md"
```

The calling context will:

0. **Promote from `plans/backlog/` first, if needed**: if `plan-path` resolves inside
   `plans/backlog/`, this step runs on the local `main` checkout — never inside a worktree, since
   plan-folder promotion is plan-doc work, not implementation — BEFORE step 1 below: `git mv
plans/backlog/<slug>/ plans/in-progress/<slug>/` (no date prefix; `in-progress/` uses the same
   bare slug as `backlog/`), commit the move, and push directly to `origin main`. Only after that
   push lands does `plan-path` resolve to its new `plans/in-progress/` location and execution
   proceeds to step 1. This guarantees the plan's in-progress state is committed and visible on
   `origin main` before any implementation work begins — never execute directly out of
   `plans/backlog/`. See [Execute Plan from Backlog](./example-usage-and-iteration-example.md#execute-plan-from-backlog) below.
1. **Enter the work branch** (Step 0): the work branch is whatever the user specifies at invocation (a dedicated worktree, the `main` checkout, or any existing branch); if unspecified, the plan docs win (the `## Worktree` section, defaulting to a worktree provisioned from `origin/main`) — refuse to start only when neither the user nor the plan specifies one. Then, by default, pull the latest `origin/main` into the work branch first — before any implementation — to minimize merge collisions
2. Read the delivery checklist from the plan's `delivery.md` to understand all items
3. Create granular tasks using `TaskCreate` — one per remaining checkbox (including nested sub-bullets)
4. For each item: mark `in_progress`, **repo-ground its file paths and commands** (refuse-on-uncertainty if grounding fails), analyze it, **prefer the `_Suggested executor:_` annotation** if present (else fall back to Agent Selection heuristics), delegate to the chosen agent (or execute directly for trivial edits), verify the result
5. Perform the Atomic Sync Ritual after each item — tick `- [ ]` → `- [x]` in `delivery.md`, add implementation notes, `TaskUpdate completed`
6. Invoke `plan-execution-checker` via the Agent tool to validate the implementation
7. Iterate execution and validation until zero findings achieved
8. Move plan folder to plans/done/ using git mv
9. Show git status with modified files
10. Wait for user commit approval
11. After the final delivery for each repository is pushed or merged, run the exact-path worktree
    cleanup immediately. Verify the worktree is recorded as self-created for this plan, clean, and
    fully pushed/merged; then use non-force `git worktree remove <exact-path>` without a confirmation
    prompt. Never remove a repository root, wildcard path, or another actor's worktree.
