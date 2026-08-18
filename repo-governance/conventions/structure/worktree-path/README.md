---
title: "Worktree Path Convention"
description: "Defines the worktree directory structure, naming convention, and gitignore requirements for claude --worktree routing"
when_to_use: "Read this index to find the right Worktree Path Convention child document."
---

# Worktree Path Convention

- [Worktree Path: Principles, Purpose, Relationship to Delivery Mode, and Scope](./principles-purpose-relationship-to-delivery-mode-and-scope.md) — The principles this convention implements, why it exists, how it relates to the Delivery Mode concept, and what it covers versus delegates elsewhere Read this when you need the rationale for the worktree path convention, how it relates to Delivery Mode, or whether a worktree topic falls inside its scope.
- [Worktree Path: Standards and Examples](./standards-and-examples.md) — The required worktree directory structure, hook routing mechanism, naming and gitignore requirements, plus PASS/FAIL examples for hook registration, worktree paths, and hook file naming Read this when creating or reviewing a WorktreeCreate hook, choosing a worktree path, or checking a worktree/hook filename against PASS/FAIL examples.
- [Platform Binding Compatibility and Industry Convention](./platform-binding-compatibility-and-industry-convention.md) — How the WorktreeCreate hook stays platform-agnostic across coding agent platforms, and why this convention deliberately departs from the industry-standard sibling-directory worktree placement Read this when checking cross-platform hook compatibility, or when you need the rationale for placing worktrees inside the repo instead of as sibling directories.
- [Worktree Path: Cleanup, Multiple Worktrees, Tools, and References](./worktree-cleanup-multiple-worktrees-tools-and-references.md) — The worktree removal procedure and AI/HUMAN tagging rule, the multiple-concurrent-worktrees layout, the tools that interact with this convention, and related convention/documentation links Read this when removing a worktree, tagging worktree-related delivery checklist steps, or looking up a related convention or reference.
