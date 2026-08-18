---
title: "PASS: Best Practices"
description: Five best practices - start concrete, composition, flat over nested, one job per component, wait for pain.
category: explanation
subcategory: principles
tags:
  - principles
  - simplicity
  - yagni
created: 2025-12-15
when_to_use: Use when choosing how to structure new code.
---

# PASS: Best Practices

## 1. Start Concrete, Abstract Later

**First implementation** - write it directly:

```typescript
// First function - concrete implementation
function validateEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

**After third duplication** - extract pattern:

```typescript
// Third similar function - now abstract
function validateFormat(value: string, pattern: RegExp): boolean {
  return pattern.test(value);
}

function validateEmail(email: string): boolean {
  return validateFormat(email, /^[^\s@]+@[^\s@]+\.[^\s@]+$/);
}
```

## 2. Prefer Composition Over Inheritance

**Instead of inheritance**:

```typescript
FAIL: class AdminUser extends PremiumUser {}
```

**Use composition**:

```typescript
PASS: interface User {
  name: string;
  roles: Role[];
  subscription: Subscription;
}
```

## 3. Flat Over Nested

**For file structure, data, and organization**:

```
PASS: Flat:
libs/
  ts-validation/
  ts-auth/

FAIL: Nested:
libs/
  shared/
    core/
      validation/
```

## 4. One Job Per Component

**Single-purpose functions/agents**:

```typescript
PASS: function validateEmail(email: string): boolean {}
PASS: function sendEmail(to: string, subject: string): void {}

FAIL: function handleEmail(email: string, action: string): any {}
```

## 5. Wait for Pain Before Refactoring

**Don't refactor speculatively**:

- FAIL: "We might need this to be configurable someday"
- FAIL: "What if we need to support multiple databases?"
- PASS: "We're duplicating this in three places - time to abstract"
- PASS: "This function has 200 lines - time to split it"
