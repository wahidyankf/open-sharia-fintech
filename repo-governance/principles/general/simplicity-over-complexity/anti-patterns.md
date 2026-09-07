---
description: Four code-level anti-patterns - premature abstraction, config explosion, deep inheritance, over-generic code.
when_to_use: Use when reviewing code for these anti-patterns.
---

# Anti-Patterns

## Premature Abstraction

FAIL: **Problem**: Creating abstraction before third use.

```typescript
// First use - just write the code directly
function createUser(name: string) {
  return { name, createdAt: new Date() };
}

// FAIL: WRONG: Immediately abstracting
class EntityFactory<T> {
  create(data: Partial<T>): T {
    return {
      ...data,
      createdAt: new Date(),
    } as T;
  }
}
```

**Why it's bad**: Abstraction before proven need. YAGNI violation. Wait for third duplication.

## Configuration Explosion

FAIL: **Problem**: Too many configuration options.

```json
{
  "feature": {
    "enabled": true,
    "mode": "advanced",
    "submode": "experimental",
    "options": {
      "option1": true,
      "option2": false,
      "option3": {
        "suboption1": "value",
        "suboption2": 42
      }
    }
  }
}
```

**Why it's bad**: Combinatorial explosion. Most combinations never used. Impossible to test.

## Deep Inheritance Hierarchies

FAIL: **Problem**: Multi-level inheritance.

```typescript
class Entity {}
class User extends Entity {}
class AuthenticatedUser extends User {}
class PremiumUser extends AuthenticatedUser {}
class AdminUser extends PremiumUser {}
```

**Why it's bad**: Fragile base class. Changes ripple through hierarchy. Hard to understand behaviour.

## Over-Generic Code

FAIL: **Problem**: Solving problems you don't have.

```typescript
class GenericRepository<T, K extends keyof T, V extends T[K]> {
  find(key: K, value: V): T | undefined {
    // Complex generic implementation
  }
}
```

**Why it's bad**: Generic for genericity's sake. Harder to read. Probably simpler to write specific implementations.
