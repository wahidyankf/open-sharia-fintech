---
title: Worktree Toolchain Initialization
description: Practice for initializing the full polyglot toolchain (npm install + doctor --fix) in the root repository worktree after creating or entering a git worktree
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
when_to_use: Use immediately after creating or entering any git worktree, before running any Nx command in it.
---

# Worktree Toolchain Initialization

After creating or entering a git worktree in this repository, always initialize the full polyglot toolchain in the **root repository worktree** with a mandatory two-step sequence:

1. Run `npm install` in the root repository worktree.
2. Run `npm run doctor -- --fix` in the root repository worktree.

Both steps are required. The first ensures the Nx workspace and its Node/TypeScript dependencies remain functional; the second actively converges the polyglot toolchains (Rust, .NET/F#, TypeScript/Node) managed by `rhino-cli doctor` so that any language task the worktree's work touches resolves against a healthy toolchain.

## Contents

- [Principles and Conventions Implemented](./worktree-setup/01-principles-and-conventions-implemented.md) — Why this practice exists.
- [The Rule](./worktree-setup/02-the-rule.md) — The exact two-step command sequence, and the shared cargo cache it provisions.
- [Independent Drift Layers and the `postinstall` Hook](./worktree-setup/03-independent-drift-layers-and-the-postinstall-hook.md) — Why both steps are independently required.
- [Dependency Isolation, Language Breadth, and Idempotency](./worktree-setup/04-dependency-isolation-language-breadth-and-idempotency.md) — Why every worktree entry needs the init.
- [What Goes Wrong Without Both Steps](./worktree-setup/05-what-goes-wrong-and-nx-node-modules-dependency.md) — Build/test/lint/cache failure modes.
- [Per-Project Dependency Restoration](./worktree-setup/06-per-project-dependency-restoration.md) — The F#/.NET `dotnet restore` gap.
- [Sibling-Repo Relative Paths From Inside a Worktree](./worktree-setup/07-sibling-repo-relative-paths.md) — Correct path nesting in multi-repo plans.
- [Absolute Source Paths in Delivery-Checklist Commands](./worktree-setup/08-absolute-source-paths-in-delivery-checklist-commands.md) — Worktree copy vs. stale primary-checkout path.
- [When This Applies](./worktree-setup/09-when-this-applies.md) — The five triggering conditions.
- [Step-by-Step Procedure](./worktree-setup/10-step-by-step-procedure.md) — The five numbered steps.
- [Notes for AI Agents](./worktree-setup/11-notes-for-ai-agents.md) — The MUST-run-both-steps rule for agents.

## Related Documentation

- [Worktree Path Convention](../../conventions/structure/worktree-path.md) - Repo-root `worktrees/<name>/` override and the WorktreeCreate hook
- [Reproducible Environments](../workflow/reproducible-environments.md) - Volta pinning and lockfile management
- [Native-First Toolchain Management](../workflow/native-first-toolchain.md) - Native package managers and `rhino-cli doctor`
- [AI Agents Convention](../agents/ai-agents.md) - Git Worktree Awareness rules for agents
- [Trunk Based Development](../workflow/trunk-based-development/08-default-push-and-worktree-execution.md#default-push-and-worktree-execution) - The repo-wide default delivery mode is `worktree-to-pr`
- [Git Push Default Convention](../workflow/git-push-default.md) - The PR-branch-as-default push target
- [Nx Targets](../infra/nx-targets.md) - Canonical Nx target names and caching rules
