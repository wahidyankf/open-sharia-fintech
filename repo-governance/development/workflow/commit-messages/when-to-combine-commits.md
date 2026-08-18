---
title: "When to Combine Commits"
description: The two cases where multiple files belong in one atomic commit — a single logical change, and tightly coupled changes.
category: explanation
subcategory: development
tags:
  - conventional-commits
  - git
  - development
  - code-quality
created: 2025-11-24
when_to_use: Use when deciding whether related changes across multiple files should land in one commit instead of several.
---

# When to Combine Commits

Combine related changes into a single commit when:

**Single logical change** - Multiple files that together form one atomic feature or fix:

```
PASS: Good:
1. feat(auth): add two-factor authentication
   (includes: auth.js, auth.test.js, auth.md, routes.js)

FAIL: Bad:
1. feat(auth): add auth.js
2. feat(auth): add auth.test.js
3. feat(auth): add auth.md
4. feat(auth): update routes.js
```

**Tightly coupled changes** - Changes that don't make sense separately or would break the build if separated:

```
PASS: Good:
1. refactor(api): rename getUserData to fetchUserProfile
   (includes renaming function definition and all call sites)

FAIL: Bad:
1. refactor(api): rename function definition
2. refactor(api): update call sites
   (This would break the build between commits)
```
