---
title: "Common Violations"
description: Three before/after examples of common simplicity violations.
category: explanation
subcategory: principles
tags:
  - principles
  - simplicity
  - over-engineering
created: 2025-12-15
when_to_use: Use when identifying whether a behavior violates this principle.
---

# Common Violations

## Violation 1: Anticipating Future Requirements

```
FAIL: "I'll make this configurable in case you need different behavior later"
PASS: "Here's the solution for your current requirement. We can make it configurable if needed."
```

## Violation 2: Creating Abstractions Prematurely

```
FAIL: [Creates BaseRepository class and generic CRUD utilities for one model]
PASS: [Writes direct database calls. Extracts patterns after third similar implementation]
```

## Violation 3: Defensive Programming for Type-Safe Code

```
FAIL: if (typeof user.id === 'number') { ... } // TypeScript already guarantees this
PASS: const userId = user.id; // Trust the type system
```
