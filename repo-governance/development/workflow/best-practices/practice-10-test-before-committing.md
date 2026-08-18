---
title: "Practice 10: Test Before Committing"
description: Run tests locally before every commit rather than waiting for CI.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use immediately before committing, to confirm tests and lint were run locally first.
---

# Practice 10: Test Before Committing

**Principle**: Run tests locally before every commit.

**Good Example:**

```bash
# Make changes
# ... edit files ...

# Test before committing
npm test
npm run lint

# All green - commit
git commit -m "feat(api): add validation"
```

**Bad Example:**

```bash
# Make changes
git commit -m "feat: add stuff"
git push

# Wait for CI to tell you tests failed (SLOW FEEDBACK!)
```

**Rationale:**

- Fast feedback loop
- Catch issues early
- Respect team's time
- Green CI
