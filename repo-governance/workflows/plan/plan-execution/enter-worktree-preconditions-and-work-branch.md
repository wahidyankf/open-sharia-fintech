---
title: "Enter the Designated Worktree — Preconditions and Work Branch"
description: Defines the backlog-promotion precondition and the three-tier precedence for selecting the plan's work branch.
when_to_use: Use when resolving which branch or worktree a plan executes on before any implementation work begins.
---

# 0. Enter the Designated Worktree (Sequential, Hard Gate)

**Precondition — backlog promotion already resolved `plan-path`**: if the plan being executed
originally resolved inside `plans/backlog/`, the delivery-mode-aware
[Starting Work procedure](../../../conventions/structure/plans/starting-and-completing-work.md#starting-work)
MUST have landed the pure move on `origin/main` before this step begins. `worktree-to-pr` completes
and merges the move from its dedicated worktree; `main-to-pr` does so from the synced primary
checkout. A direct push is valid only under a permitted selected direct-push mode. `plan-path` now
resolves to `plans/in-progress/`. A direct caller, including
[`multi-plans-execution.md`](../multi-plans-execution.md) with an `all-backlog` selector, MUST
perform that same procedure for each backlog plan first. See
[Execute Plan from Backlog](./example-usage-and-iteration-example.md#execute-plan-from-backlog) for the full worked example.

Plan execution happens on the plan's **work branch**, synced to the latest `origin/main`. The work branch is chosen by precedence: (1) a branch the **user explicitly specifies at invocation** — a dedicated worktree, the `main` checkout, or any other existing branch — wins; (2) if the user specifies nothing, the **plan docs win** — the plan's `## Worktree` section (or declared work branch) governs, and absent any override that defaults to a dedicated worktree provisioned from `origin/main`. Whichever branch is selected, the executor's **default first action is to pull the latest `origin/main` into that work branch** before any implementation, to minimize merge collisions later at push time. Executing a plan from a **stale** work branch — one not synced to the latest `origin/main` — is forbidden.
