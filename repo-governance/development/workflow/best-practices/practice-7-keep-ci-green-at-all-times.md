---
description: Never commit code that breaks CI, fix immediately if broken.
when_to_use: Use when CI fails after a push, to confirm the correct response is an immediate fix or revert.
---

# Practice 7: Keep CI Green at All Times

**Principle**: Never commit code that breaks CI, fix immediately if broken.

**Good Example:**

```bash
# Before pushing
npm test  # Verify tests pass
npm run lint  # Verify linting passes
npm run build  # Verify build succeeds

git push origin main

# If CI fails after push
git revert HEAD  # OR fix immediately
```

**Bad Example:**

```bash
git push origin main
# CI fails
# "I'll fix it later" (BLOCKS EVERYONE!)
```

**Rationale:**

- Broken main blocks everyone
- Fast feedback loop
- Team productivity
- Quality gate enforcement
