---
title: "Making Commits"
description: The three practical ways to make a commit — interactive one-liner, with a body flag, or multi-line in an editor.
category: explanation
subcategory: development
tags:
  - conventional-commits
  - git
  - development
  - code-quality
created: 2025-11-24
when_to_use: Use when you need the exact git commit invocation for a one-line, body-included, or multi-line commit message.
---

# Making Commits

## Interactive Workflow

```bash
# 1. Stage your changes
git add <files>

# 2. Commit with message
git commit -m "feat(auth): add login functionality"

# 3. If validation fails, fix and try again
git commit -m "feat(auth): add login functionality"
```

## Commit with Body

```bash
git commit -m "feat(auth): add login functionality" -m "Implements OAuth 2.0 authentication with support for Google and GitHub providers."
```

## Multi-line Commit in Editor

```bash
# Opens your default editor
git commit

# Write:
feat(auth): add login functionality

Implements OAuth 2.0 authentication with support for
Google and GitHub providers. Includes session management
and refresh token handling.

Closes #123
```
