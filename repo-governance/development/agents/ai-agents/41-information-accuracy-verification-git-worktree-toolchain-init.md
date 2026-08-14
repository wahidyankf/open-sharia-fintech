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

1. **Initialize the full toolchain in the root worktree after creating or entering a worktree — two steps, in order** — When an agent creates a worktree via `git worktree add`, the `EnterWorktree` tool, or an `isolation: "worktree"` configuration, or when an agent begins a session inside an existing worktree, it MUST immediately run BOTH of the following in the root repository worktree, in order: (a) `npm install` to keep `node_modules/` consistent with `package-lock.json` (ensures Nx task caching, builds, tests, and linting function correctly across all worktrees), and (b) `npm run doctor -- --fix` to actively converge the polyglot toolchains managed by `rhino-cli doctor` (Rust, .NET/F#, TypeScript/Node). Doing only the first step is NOT sufficient: `package.json`'s `postinstall` hook runs `npm run doctor || true`, and the trailing `|| true` deliberately swallows toolchain drift so that `npm install` can complete while the native toolchain is broken. The explicit `npm run doctor -- --fix` invocation is the only action that guarantees convergence. The rule is triggered by execution mode (any worktree entry), not by intent (even "docs-only" worktree sessions go through both steps, because the pre-push hook (`apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push`) can fan out to arbitrary language tasks via its affected-projects-scoped gates, e.g. `nx affected -t test:quick`, whose internal chain touches typecheck/lint/build/coverage per project). See [Worktree Toolchain Initialization](../../workflow/worktree-setup.md) for the full rationale, procedure, and relationship to [Native-First Toolchain Management](../../workflow/native-first-toolchain.md).
