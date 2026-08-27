---
title: "When This Applies"
description: The creation triggers for the two-step worktree init, and that it applies regardless of stated task scope.
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
when_to_use: Use when deciding whether a worktree creation needs the two-step init.
---

# When This Applies

Run both steps from the new worktree's root after any of the following:

1. Running `rtk git worktree add` to create a new worktree.
2. Using the `EnterWorktree` tool in the coding agent, which creates a worktree automatically.
3. An AI agent with `isolation: "worktree"` spawning a new worktree for isolated work.
4. Any other mechanism that creates a worktree in this repository.

The rule is **triggered by creation, not by intent**. Even a new worktree for "small" or
"docs-only" work goes through the two-step init. Merely re-entering an existing worktree does not
trigger setup; missing dependencies discovered later are repaired as an observed environment
problem. This applies to both human developers and AI agents.
