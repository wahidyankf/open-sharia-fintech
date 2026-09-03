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

Captured build/test/coverage transcripts are a common miss: tools like `dotnet test` print each
resolved path as absolute, so a plan evidence file copied verbatim from `nx run <project>:test:unit`
output routinely carries the machine's absolute worktree path even though no one typed it by hand.
Run the grep above on any such captured-output file before staging it, not only on hand-written
commands, and normalize the repository-root prefix to a portable placeholder rather than leaving it
absolute.
