---
title: "Commit Separation"
description: "Why a CI-blocker fix must be its own commit."
category: explanation
subcategory: development
tags:
  - ci
  - quality-gates
  - root-cause
  - debugging
  - anti-pattern
  - preexisting-issues
created: 2026-04-04
when_to_use: "Use when a CI-blocker fix is bundled with unrelated changes."
---

# Commit Separation

Preexisting fixes MUST be committed separately from feature work. This serves multiple purposes:

- **Clear history**: The fix is visible as a distinct change, not buried in a feature commit.
- **Easy revert**: If the fix introduces a new problem, it can be reverted independently.
- **Accurate attribution**: The commit message accurately describes what changed and why.
- **Review clarity**: Reviewers can evaluate the fix on its own merits.

**Commit message patterns for preexisting fixes:**

```
fix(project-name): resolve preexisting lint violations in auth module
fix(shared-types): update type exports to match current API shape
chore(project-name): update test snapshots after dependency upgrade
fix(project-name): add missing Gherkin step definitions for existing commands
```
