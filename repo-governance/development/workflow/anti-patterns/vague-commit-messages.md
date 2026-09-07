---
description: Commit messages that don't explain changes undermine searchable history and changelog automation.
when_to_use: Use when writing a commit message that doesn't clearly state what changed and why.
---

# Anti-Pattern: Vague Commit Messages

**Problem**: Unclear commit messages that don't explain changes.

**Bad Example:**

```bash
git commit -m "updates"
git commit -m "fix"
git commit -m "WIP"
git commit -m "changes"
git commit -m "asdf"
```

**Solution:**

```bash
git commit -m "feat(auth): add JWT token validation"
git commit -m "fix(ui): resolve button alignment on mobile"
git commit -m "docs(api): update authentication endpoints"
```

**Rationale:**

- Clear commit purpose
- Searchable history
- Automated changelog
- Better collaboration
