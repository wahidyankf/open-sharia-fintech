---
description: Worked good and bad commit message examples across common change types.
when_to_use: Use when you need a concrete example commit message for a specific kind of change.
---

# Real-World Examples

## Good Examples

**Basic feature:**

```
feat(auth): add login functionality
```

**Bug fix with scope:**

```
fix(api): prevent race condition on startup
```

**Documentation update:**

```
docs: update API reference
```

**Refactoring with detailed scope:**

```
refactor(parser): extract common logic into utilities
```

**Performance improvement with body:**

```
perf(db): optimize user query

Reduce query time from 500ms to 50ms by adding index on
email field and using prepared statements.
```

**Breaking change with footer:**

```
feat(api): redesign authentication endpoint

BREAKING CHANGE: The /auth endpoint now requires OAuth 2.0
instead of API keys. Update all client applications.
```

**Bug fix with issue reference:**

```
fix(validation): handle empty strings correctly

Fixes #123
```

## Bad Examples

**Missing type:**

```
FAIL: Added new feature
PASS: feat: add new feature
```

**Wrong tense:**

```
FAIL: feat: added login
PASS: feat: add login
```

**Wrong case:**

```
FAIL: FEAT(AUTH): ADD LOGIN
PASS: feat(auth): add login
```

**Period at end:**

```
FAIL: feat: add login.
PASS: feat: add login
```

**Too long header:**

```
FAIL: feat: add a really complex and detailed authentication system with multiple providers
PASS: feat(auth): add multi-provider authentication
```

**Not imperative mood:**

```
FAIL: feat: adds login capability
FAIL: feat: adding login
PASS: feat: add login
```
