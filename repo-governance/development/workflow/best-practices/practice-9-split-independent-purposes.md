---
title: "Practice 9: Split Independent Concerns"
description: Split independently reviewable purposes, while keeping required cross-domain completion artifacts together.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use after commit authorization when a change set contains more than one potentially independent purpose.
---

# Practice 9: Split Independent Concerns

**Principle**: File domain does not decide the boundary. Split independently reviewable and
revertible purposes; keep API, UI, tests, docs, specs, references, migrations, and generated files
together when they complete one coherent change.

**Good Example:**

```bash
git commit -m "feat(api): add documented user endpoints"
git commit -m "feat(ui): add tested user profile page"
```

**Bad Example:**

```bash
git commit -m "feat: add user functionality and optimize billing queries"
# Independent user and billing purposes are bundled
```

**Rationale:**

- Easier to review
- Easier to revert specific changes
- Clear history by coherent purpose
- Better git log navigation
