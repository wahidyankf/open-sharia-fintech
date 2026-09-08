---
description: Committing large batches of changes infrequently makes review and revert difficult.
when_to_use: Use when about to commit a week's worth of changes in a single large commit instead of small incremental ones.
---

# Anti-Pattern: Large, Infrequent Commits

**Problem**: Committing large batches of changes infrequently.

**Bad Example:**

```bash
# Work for a week
# ... edit 100 files ...

# One massive commit
git add .
git commit -m "feat: implement entire user management system"
# 5000 lines changed!
```

**Solution:**

```bash
# Day 1
git commit -m "feat(user): add User model"
git commit -m "feat(user): add validation"

# Day 2
git commit -m "feat(user): add CRUD endpoints"
git commit -m "test(user): add integration tests"
```

**Rationale:**

- Small commits easier to review
- Clear history
- Easier to revert
- Faster feedback
