---
description: Combining independently reviewable purposes in one commit produces confusing, hard-to-revert history.
when_to_use: Use after explicit authorization when a commit would bundle independently reviewable and revertible purposes.
---

# Anti-Pattern: Mixed Concerns in Single Commit

**Problem**: Combining independent purposes in one commit, or splitting one purpose merely because
its completion artifacts cross file domains.

**Bad Example:**

```bash
git commit -m "feat: add user dashboard and fix typos and update docs"
# Changed: one dashboard feature plus unrelated README typo fixes
# Two independently reviewable purposes are bundled.
```

**Solution:**

```bash
git commit -m "feat(user): add user dashboard"
# Includes its API, UI, tests, and documentation.
git commit -m "fix(docs): correct typos in README"
```

**Rationale:**

- Keeps each boundary build-valid and complete
- Easier to review and revert an independent purpose
- Keeps required tests, docs, specs, references, migrations, and mirrors with their change
- Better git log

Use the [thematic boundary test](../commit-messages/commit-granularity-and-when-to-split-commits.md)
to choose the fewest qualifying commits. File type, directory, scope, or Conventional Commit type
does not independently require a split.
