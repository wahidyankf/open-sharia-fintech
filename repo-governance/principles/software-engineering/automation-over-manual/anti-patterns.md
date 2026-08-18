---
title: "Anti-Patterns"
description: Four automation anti-patterns and why each is bad.
category: explanation
subcategory: principles
tags:
  - principles
  - automation
  - git-hooks
  - ai-agents
  - consistency
created: 2025-12-15
when_to_use: Use when reviewing a workflow for automation gaps.
---

# Anti-Patterns

## Manual Quality Checks

FAIL: **Problem**: Relying on humans to remember checks.

```bash
# FAIL: Manual checklist - often skipped
# Before committing:
# - Did I run Prettier? (maybe)
# - Did I check the commit message format? (probably not)
# - Did I validate the documentation? (forgot)
```

**Why it's bad**: Humans forget. Manual checklists are ignored when time is tight.

## No Validation Until PR

FAIL: **Problem**: Catching errors in code review instead of pre-commit.

```bash
# FAIL: Errors discovered in PR review
git commit -m "added feature"  # Invalid format
git push
# PR reviewer: "Please fix commit message format"
# Developer: *forces push with amended message*
```

**Why it's bad**: Wastes reviewer time. Disrupts workflow. Easy to automate.

## Inconsistent Tooling

FAIL: **Problem**: Different developers use different formatters.

```bash
# Developer A uses Prettier
# Developer B uses ESLint --fix
# Developer C manually formats
# Result: Inconsistent code style
```

**Why it's bad**: Inconsistency. Merge conflicts. Wasted time debating style.

## Manual Link Checking

FAIL: **Problem**: Clicking links manually to verify they work.

```bash
# FAIL: Manual link verification
# 1. Open each documentation file
# 2. Click every external link
# 3. Record which ones work
# 4. Repeat weekly
```

**Why it's bad**: Time-consuming. Error-prone. Unsustainable at scale.
