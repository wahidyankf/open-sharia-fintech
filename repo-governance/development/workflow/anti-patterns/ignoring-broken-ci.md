---
title: "Anti-Pattern: Ignoring Broken CI"
description: Pushing code that breaks CI and deferring the fix blocks the whole team.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when CI fails after a push and there's a temptation to defer the fix.
---

# Anti-Pattern: Ignoring Broken CI

**Problem**: Pushing code that breaks CI and not fixing immediately.

**Bad Example:**

```bash
git push origin main
# CI fails with test failures

# "I'll fix it later" (BLOCKS EVERYONE!)
# Team can't deploy for hours/days
```

**Solution:**

```bash
git push origin main
# CI fails

# Fix immediately OR revert
git revert HEAD
git push origin main
# CI green again - team unblocked
```

**Rationale:**

- Broken main blocks everyone
- Fast feedback required
- Team productivity
- Quality gate
