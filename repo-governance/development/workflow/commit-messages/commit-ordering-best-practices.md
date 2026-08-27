---
title: "Commit Ordering Best Practices"
description: Order already-independent thematic commits by dependency without creating incomplete intermediate states.
category: explanation
subcategory: development
tags:
  - conventional-commits
  - git
  - development
  - code-quality
created: 2025-11-24
when_to_use: Use when a change requires multiple commits and you need to decide what order to make them in.
---

# Commit Ordering Best Practices

After the thematic boundary test establishes multiple independent commits, order them logically:

1. **Dependencies first** — a later independent purpose may rely on an earlier one.
2. **Preserve validity** — every boundary builds, reviews, and reverts safely on its own.
3. **Order by purpose, not type** — Conventional Commit types describe commits; they do not create
   an artificial `feat` → `docs` → `test` sequence.

**Example of good commit ordering:**

```
1. feat(agents): add documented docs-link-checker agent  # Includes required index and tests
2. fix(docs): align unrelated frontmatter date           # Independent repair
```
