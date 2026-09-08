---
description: The most common Commitlint rejection errors and how to fix each one.
when_to_use: Use when a commit is rejected by Commitlint and you need to fix the specific error shown.
---

# Common Errors and Fixes

## Error: "type may not be empty"

**Problem**: Missing commit type

```bash
FAIL: update documentation
```

**Fix**: Add a valid type

```bash
PASS: docs: update documentation
```

## Error: "subject may not be empty"

**Problem**: Missing description after colon

```bash
FAIL: feat:
```

**Fix**: Add description

```bash
PASS: feat: add login functionality
```

## Error: "header must not be longer than 100 characters"

**Problem**: Header line too long. The enforced limit is 100; the 50-character figure elsewhere in
these docs is a readability target, not what the hook rejects.

```bash
FAIL: feat(auth): add multi-provider authentication covering OAuth 2.0, SAML, API keys, and session refresh
```

**Fix**: Shorten description, add details to body

```bash
PASS: feat(auth): add multi-provider authentication

Supports OAuth 2.0, SAML, and API key authentication.
```

## Error: "type must be lowercase"

**Problem**: Type in wrong case

```bash
FAIL: Feat: add login
FAIL: FEAT: add login
```

**Fix**: Use lowercase

```bash
PASS: feat: add login
```

## Error: "body's lines must not be longer than 100 characters"

**Problem**: Body line exceeds character limit

**Fix**: Break into multiple lines

```bash
PASS: feat: add new feature

This is a longer explanation that has been broken into
multiple lines to ensure each line stays under 100
characters for better readability.
```
