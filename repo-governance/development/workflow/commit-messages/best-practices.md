---
title: "Best Practices"
description: Practical habits for clear descriptions, consistent scopes, single-purpose commits, useful bodies, issue references, and documenting breaking changes.
category: explanation
subcategory: development
tags:
  - conventional-commits
  - git
  - development
  - code-quality
created: 2025-11-24
when_to_use: Use when writing a commit message and want a habit-level checklist beyond the mechanical format rules.
---

# Best Practices

## Write Clear Descriptions

**Good:**

```
feat(auth): add password reset functionality
fix(api): prevent duplicate user registration
docs: add API authentication guide
```

**Avoid:**

```
feat: stuff
fix: bug
docs: updates
```

## Use Scopes Consistently

Define project-wide scopes and stick to them:

```
feat(auth): ...
feat(api): ...
feat(ui): ...
```

Not:

```
feat(authentication): ...
feat(endpoints): ...
feat(frontend): ...
```

## One Logical Change Per Commit

**Good:**

```
feat(auth): add login endpoint
feat(auth): add logout endpoint
```

**Avoid:**

```
feat: add login and logout and password reset and user profile
```

## Use the Body for Context

**Good:**

```
perf(db): optimize user query

Add composite index on (email, status) to reduce query
time from 500ms to 50ms. Tested with 1M user dataset.
```

**Avoid:**

```
perf(db): optimize user query
```

## Reference Issues

Link commits to issues when applicable:

```
fix(auth): prevent session hijacking

Fixes #456
```

## Explain Breaking Changes

Always document breaking changes:

```
feat(api): redesign authentication endpoint

BREAKING CHANGE: The /auth endpoint now requires OAuth 2.0
instead of API keys. See migration guide in docs/migration.md.
```
