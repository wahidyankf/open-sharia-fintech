---
title: "Practice 2: Make Small, Frequent Commits"
description: Compose the fewest small, atomic commits that keep each authorized purpose build-valid and reviewable.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when deciding how to batch changes into commits during a work session.
---

# Practice 2: Make Small, Frequent Commits

**Principle**: After explicit authorization, compose the fewest small, atomic commits that each
remain build-valid, independently reviewable, and revertible. Keep required tests, documentation,
specifications, references, and generated artifacts with the purpose they complete.

**Good Example:**

```bash
# Day 1
git commit -m "feat(auth): add User model"
git commit -m "feat(auth): add password hashing utility"

# Day 2
git commit -m "feat(auth): add login endpoint"
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
- Faster feedback without incomplete intermediate commits
