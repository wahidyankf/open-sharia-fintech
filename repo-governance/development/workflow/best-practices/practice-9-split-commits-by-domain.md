---
title: "Practice 9: Split Commits by Domain"
description: Separate concerns in different commits instead of bundling API, UI, and docs together.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when a change spans multiple domains (API, UI, docs) and needs to be split into separate commits.
---

# Practice 9: Split Commits by Domain

**Principle**: Separate concerns in different commits.

**Good Example:**

```bash
git commit -m "feat(api): add user endpoints"
git commit -m "feat(ui): add user profile page"
git commit -m "docs(api): document user endpoints"
```

**Bad Example:**

```bash
git commit -m "feat: add user functionality"
# 1000 lines: API + UI + docs + tests all in one commit
```

**Rationale:**

- Easier to review
- Easier to revert specific changes
- Clear history by domain
- Better git log navigation
