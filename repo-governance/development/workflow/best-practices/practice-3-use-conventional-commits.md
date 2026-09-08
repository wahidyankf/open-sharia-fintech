---
description: Follow conventional commit format for clear, parseable history.
when_to_use: Use when writing a commit message and choosing its type/scope/subject format.
---

# Practice 3: Use Conventional Commits

**Principle**: Follow conventional commit format for clear, parseable history.

**Good Example:**

```bash
git commit -m "feat(api): add user registration endpoint"
git commit -m "fix(ui): resolve button alignment issue"
git commit -m "docs(readme): update installation instructions"
git commit -m "refactor(auth): extract validation logic"
```

**Bad Example:**

```bash
git commit -m "updates"
git commit -m "fix stuff"
git commit -m "WIP"
git commit -m "asdf"
```

**Rationale:**

- Clear commit purpose
- Automated changelog generation
- Easy to search history
- Semantic versioning support
