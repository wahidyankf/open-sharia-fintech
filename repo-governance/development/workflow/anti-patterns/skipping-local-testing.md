---
description: Relying on CI alone to discover test failures wastes time that local testing would have saved.
when_to_use: Use when about to push changes without first running tests and lint locally.
---

# Anti-Pattern: Skipping Local Testing

**Problem**: Relying on CI to discover test failures.

**Bad Example:**

```bash
# Make changes
# ... edit files ...

# Skip testing locally
git commit -m "feat: add feature"
git push

# Wait 5 minutes for CI to fail
# Realize simple test failure could have been caught locally
```

**Solution:**

```bash
# Make changes
# ... edit files ...

# Test locally FIRST
npm test
npm run lint

# All green - commit
git commit -m "feat: add feature"
git push
```

**Rationale:**

- Fast feedback (seconds vs minutes)
- Respect team's time
- Catch simple issues early
- Higher quality commits
