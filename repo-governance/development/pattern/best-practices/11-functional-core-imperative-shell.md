---
title: "Practice 10: Functional Core, Imperative Shell"
description: "Keep pure logic in a core and push side effects to an imperative shell at the boundaries."
category: explanation
subcategory: development
tags: []
created: 2026-05-12
when_to_use: "Use when structuring code that mixes business logic with database, network, or other I/O calls."
---

# Practice 10: Functional Core, Imperative Shell

**Principle**: Pure logic in core, side effects at boundaries.

**Good Example:**

```typescript
// Pure core
function validateUser(user: User): ValidationResult {
  // Pure validation logic
}

// Imperative shell
async function saveUser(user: User): Promise<void> {
  const result = validateUser(user); // Pure
  if (result.isValid) {
    await db.save(user); // Side effect at boundary
  }
}
```

**Bad Example:**

```typescript
// Mixed concerns
function validateAndSaveUser(user: User): void {
  // Validation mixed with database access
  if (user.email && user.name) {
    db.save(user); // Side effect in validation logic!
  }
}
```

**Rationale:**

- Clear separation of pure and impure code
- Easier to test core logic
- Side effects isolated and controlled
- Better code organization
