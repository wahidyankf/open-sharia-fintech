---
description: "What pre-commit and pre-push do for markdown, and where configured."
when_to_use: "Use when a markdown git hook misbehaves or you need its config location."
---

# Git Hooks

## Pre-Commit Hook

Runs Prettier on staged markdown files via lint-staged.

**Location**: `.husky/pre-commit` (configured in `package.json` lint-staged)

**Action**: Automatically formats staged markdown files

## Pre-Push Hook

Runs markdownlint on all markdown files before pushing.

**Location**: `.husky/pre-push`

**Action**: Blocks push if any markdown violations detected

**To fix violations before push**:

```bash
npm run lint:md:fix
```
