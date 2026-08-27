---
title: "Commit Granularity: Real-World Examples"
description: Three worked examples of choosing the fewest build-valid, reviewable, and revertible thematic commits.
category: explanation
subcategory: development
tags:
  - conventional-commits
  - git
  - development
  - code-quality
created: 2025-11-24
when_to_use: Use after explicit commit authorization when you need a concrete example of applying the thematic boundary test.
---

# Commit Granularity: Real-World Examples

Each example assumes the user explicitly authorized the named change set. Authorization remains a
prerequisite; these examples only decide its boundaries.

**Example 1: One complete feature**

```
PASS: Good:
1. feat(analytics): add event tracking
   (includes implementation, tests, specification, and API documentation)

FAIL: Bad:
1. feat(analytics): add event tracking implementation
2. test(analytics): add event tracking tests
3. docs(analytics): document event tracking API
   (the earlier commits are incomplete boundaries)
```

**Example 2: Independent purposes**

```
PASS: Good:
1. refactor(parser): extract validation logic
2. fix(time): handle daylight-saving transition

FAIL: Bad:
1. refactor: extract parser validation and fix daylight-saving transition
   (the purposes can be reviewed and reverted independently)
```

**Example 3: Dependency update and required fallout**

```
PASS: Good:
1. chore(deps): update eslint
   (includes lockfile, configuration, and required lint fixes)

FAIL: Bad:
1. chore(deps): update eslint and lockfile
2. style: fix lint failures caused by eslint update
   (the first commit does not pass its required checks)
```
