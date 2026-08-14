---
title: "Verifying a Commit Before Pushing"
description: "The grep command to scan staged changes for common machine-specific patterns before committing."
category: explanation
subcategory: development
tags:
  - git
  - commits
  - security
  - portability
  - environment
  - quality
created: 2026-03-24
when_to_use: "Use before pushing a commit that adds test fixtures, configuration, or script output containing paths."
---

# Verifying a Commit Before Pushing

Before committing, inspect staged changes for common machine-specific patterns:

```bash
git diff --cached | grep -i "/Users/\|/home/\|/opt/homebrew\|localhost.*password\|127\.0\.0"
```

The output should be empty. Any match is a signal to review that line and either replace it with an environment variable reference or confirm it is intentional test data.

Run this check whenever you stage new test fixtures, configuration files, or script output containing paths.
