---
title: "Information Accuracy and Verification — Git Worktree Awareness: Toolchain Initialization Rule"
description: "States the two-step npm install and npm run doctor -- --fix toolchain-initialization rule that applies after entering or creating a worktree."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - standards
created: 2025-11-23
when_to_use: Use when an agent has just created or entered a git worktree and needs to converge the polyglot toolchain before running any gated task.
---

# Information Accuracy and Verification — Git Worktree Awareness: Toolchain Initialization Rule

1. **Initialize each worktree at its own root — two steps, in order** — After creating with
   `rtk git worktree add` (or entering by another supported mechanism),
   immediately run `rtk npm install` and then `rtk npm run doctor -- --fix` from its
   root. The install creates its ignored `node_modules/` and runs `prepare`, activating Husky hooks;
   another checkout's install is not a substitute. The explicit doctor call converges native
   toolchains because `postinstall` deliberately tolerates doctor drift. This applies to every
   session, including docs-only work, because commit and pre-push hooks still execute repository
   tooling. See [Worktree Toolchain Initialization](../../workflow/worktree-setup.md) for the full
   procedure and [Native-First Toolchain Management](../../workflow/native-first-toolchain.md).
