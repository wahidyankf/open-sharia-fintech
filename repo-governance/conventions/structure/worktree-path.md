---
title: "Worktree Path Convention"
description: Defines the worktree directory structure, naming convention, and gitignore requirements for claude --worktree routing
when_to_use: Read this when creating, naming, or cleaning up a worktree, or configuring the WorktreeCreate hook.
category: explanation
subcategory: conventions
tags:
  - worktree
  - git
  - repository-structure
  - claude
  - hooks
created: 2026-05-03
---

# Worktree Path Convention

This convention establishes the worktree directory structure and routing convention for this repository, ensuring consistent worktree creation via `claude --worktree`.

## In This Convention

- [Principles, Purpose, Relationship to Delivery Mode, and Scope](./worktree-path/principles-purpose-relationship-to-delivery-mode-and-scope.md) — The principles this convention implements, why it exists, how it relates to the Delivery Mode concept...
- [Standards and Examples](./worktree-path/standards-and-examples.md) — required directory structure, hook routing mechanism, naming/gitignore requirements, and PASS/FAIL examples
- [Platform Binding Compatibility and Industry Convention](./worktree-path/platform-binding-compatibility-and-industry-convention.md) — cross-platform hook portability and why worktrees live inside the repo instead of as siblings
- [Cleanup, Multiple Worktrees, Tools, and References](./worktree-path/worktree-cleanup-multiple-worktrees-tools-and-references.md) — removal procedure, AI/HUMAN tagging rule, and related documentation
