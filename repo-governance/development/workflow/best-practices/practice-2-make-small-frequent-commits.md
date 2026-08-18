---
title: "Practice 2: Make Small, Frequent Commits"
description: Break work into small, atomic commits multiple times per day.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when deciding how to batch changes into commits during a work session.
---

# Practice 2: Make Small, Frequent Commits

**Principle**: Break work into small, atomic commits multiple times per day.

**Good Example:**

```bash
# Day 1
git commit -m "feat(auth): add User model"
git commit -m "feat(auth): add password hashing utility"
git commit -m "test(auth): add User model tests"

# Day 2
git commit -m "feat(auth): add login endpoint"
git commit -m "test(auth): add login endpoint tests"
```

**Bad Example:**

```bash
# One massive commit after a week
git commit -m "feat(auth): complete authentication system"
# 5000 lines changed across 50 files!
```

**Rationale:**

- Easier code review
- Easier to revert if needed
- Clear history
- Faster feedback
