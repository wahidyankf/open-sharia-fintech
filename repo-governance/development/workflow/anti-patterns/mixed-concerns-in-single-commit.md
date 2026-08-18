---
title: "Anti-Pattern: Mixed Concerns in Single Commit"
description: Combining unrelated changes in one commit produces confusing, hard-to-revert history.
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: Use when a single commit would otherwise bundle unrelated changes across different domains.
---

# Anti-Pattern: Mixed Concerns in Single Commit

**Problem**: Combining unrelated changes in one commit.

**Bad Example:**

```bash
git commit -m "feat: add user dashboard and fix typos and update docs"
# Changed: API code, UI code, documentation, tests, configs
# All different domains in one commit!
```

**Solution:**

```bash
git commit -m "feat(api): add user endpoints"
git commit -m "feat(ui): add user dashboard"
git commit -m "docs(api): document user endpoints"
git commit -m "fix(docs): correct typos in README"
```

**Rationale:**

- Easier to review
- Easier to revert specific changes
- Clear history by domain
- Better git log
