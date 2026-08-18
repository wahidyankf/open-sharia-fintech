---
title: "When This Applies"
description: The five triggering conditions for the two-step worktree init, and that it applies regardless of stated task scope.
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
when_to_use: Use when deciding whether a given worktree entry needs the two-step init.
---

# When This Applies

Run both steps in the root worktree after any of the following:

1. Running `git worktree add` to create a new worktree.
2. Using the `EnterWorktree` tool in the coding agent, which creates a worktree automatically.
3. An AI agent with `isolation: "worktree"` spawning a new worktree for isolated work.
4. A human `cd`-ing into an existing worktree to continue or resume work in a new session.
5. Any other mechanism that creates or re-enters a worktree in this repository.

The rule is **triggered by execution mode, not by intent**. Even "small" or "docs-only" worktree entries go through the two-step init. This step applies to both human developers and AI agents operating in this repository.
