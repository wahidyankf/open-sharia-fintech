---
title: "Husky - Git Hooks"
description: "How Husky wires git hooks in this repository."
category: explanation
subcategory: development
tags:
  - development
  - code-quality
  - prettier
  - husky
  - lint-staged
  - git-hooks
  - automation
created: 2026-05-12
when_to_use: "Use when configuring or debugging a Husky git hook."
---

# Husky - Git Hooks

**Purpose**: Manage git hooks to run automated checks at specific points in the git workflow.

**Hooks Configured**:

- `.husky/pre-commit` - Runs before commit is created
- `.husky/commit-msg` - Runs after commit message is entered
- `.husky/pre-push` - Runs before pushing to remote

**Why Husky**: Ensures all developers have the same git hooks configured automatically after running `npm install`. Hooks are stored in the repository (`.husky/` directory) for version control.
