---
title: "Notes for AI Agents"
description: The MUST-run-both-steps rule for agents, and why re-running the init (not re-provisioning) is the correct response to missing worktree dependencies mid-session.
category: explanation
subcategory: development
tags:
  - development
  - git
  - worktree
  - npm
  - nx
  - dependencies
  - toolchain
  - doctor
created: 2026-03-28
when_to_use: Use when an agent creates or enters a worktree, or discovers missing dependencies/build output mid-session.
---

# Notes for AI Agents

Agents that create or enter worktrees via `git worktree add`, the `EnterWorktree` tool, or an `isolation: "worktree"` configuration MUST run BOTH `npm install` AND `npm run doctor -- --fix` in the root repository worktree as immediate follow-up steps, in that order. Doing only one of the two steps is not sufficient and is treated as a rule violation.

Re-run both steps whenever a worktree's dependencies or build output turn out to be missing mid-session. The [Build-Artifact Sweeper Convention](../../infra/build-artifact-sweeper.md) makes that an expected occurrence — the worktree itself is intact, so the response is re-running this two-step init (plus any needed `nx build`), never re-provisioning the worktree or investigating a defect.

The root worktree path is available from the environment context or can be confirmed with `git worktree list`. See the [Git Worktree Awareness](../../agents/ai-agents/information-accuracy-verification-git-worktree-awareness.md) section of the AI Agents Convention for the full set of rules governing agent behavior in worktrees.
