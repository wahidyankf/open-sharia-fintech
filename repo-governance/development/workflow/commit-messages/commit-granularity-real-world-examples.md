---
title: "Commit Granularity: Real-World Examples"
description: Three worked examples of splitting a feature, a refactor-and-fix, and a config change into properly granular commits.
category: explanation
subcategory: development
tags:
  - conventional-commits
  - git
  - development
  - code-quality
created: 2025-11-24
when_to_use: Use when you need a concrete example of correctly granular versus overly bundled commits.
---

# Commit Granularity: Real-World Examples

**Example 1: Adding a new feature**

```
PASS: Good:
1. feat(analytics): add event tracking system
2. docs(analytics): document event tracking API
3. test(analytics): add event tracking tests

FAIL: Bad:
1. feat(analytics): add event tracking with docs and tests
```

**Example 2: Refactoring and fixing**

```
PASS: Good:
1. refactor(parser): extract validation logic
2. fix(parser): handle edge case in validation

FAIL: Bad:
1. refactor(parser): extract validation and fix edge case
```

**Example 3: Configuration changes**

```
PASS: Good:
1. chore(deps): update eslint to v8.0.0
2. style: fix linting errors from eslint update

FAIL: Bad:
1. chore: update eslint and fix all linting errors
```
