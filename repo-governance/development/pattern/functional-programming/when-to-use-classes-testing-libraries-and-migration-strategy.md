---
title: "When to Use Classes, Testing, Libraries, and Migration Strategy"
description: "When classes are acceptable, how pure functions simplify testing, recommended functional libraries, and how to migrate an existing codebase incrementally."
category: explanation
subcategory: development
tags:
  - development
  - functional-programming
  - immutability
  - pure-functions
  - typescript
created: 2025-12-28
when_to_use: "Use when deciding whether a class is appropriate, or planning an incremental migration to functional patterns."
---

# When to Use Classes, Testing, Libraries, and Migration Strategy

## When to Use Classes

**Classes acceptable for**:

- Data containers without behaviour (DTOs)
- Framework requirements (React components, NestJS services)
- Interface boundaries (dependency injection)

**Prefer functions for**:

- Business logic
- Data transformations
- Calculations
- Validation

```typescript
// PASS: Class as data container (acceptable)
class CreateUserDTO {
  readonly name: string;
  readonly email: string;
  readonly password: string;

  constructor(name: string, email: string, password: string) {
    this.name = name;
    this.email = email;
    this.password = password;
  }
}

// PASS: Functions for business logic (preferred)
function validateUser(dto: CreateUserDTO): ValidationResult {
  // Pure validation
}

function hashPassword(password: string): string {
  // Pure transformation
}
```

## Testing Functional Code

**Pure functions are trivial to test**:

```typescript
describe("calculateZakat", () => {
  it("calculates 2.5% for wealth above nisab", () => {
    expect(calculateZakat(10000, 5000)).toBe(250);
  });

  it("returns 0 for wealth below nisab", () => {
    expect(calculateZakat(3000, 5000)).toBe(0);
  });

  it("handles edge case at nisab threshold", () => {
    expect(calculateZakat(5000, 5000)).toBe(125);
  });

  // No mocking, no setup, just inputs and outputs
});
```

## Functional Programming Libraries

**Recommended libraries**:

- **[Immer](https://immerjs.github.io/immer/)**: Immutable updates with mutation-like syntax
- **[Ramda](https://ramdajs.com/)**: Functional programming utilities
- **[fp-ts](https://gcanti.github.io/fp-ts/)**: Typed functional programming for TypeScript
- **[ts-pattern](https://github.com/gvergnaud/ts-pattern)**: Pattern matching for TypeScript

**Use sparingly**: Don't introduce unless clear benefit. Functional patterns often possible with vanilla JavaScript/TypeScript.

## Migration Strategy

**Introducing functional patterns to existing codebase**:

1. **Start with new code**: Write new features functionally
2. **Refactor incrementally**: Convert functions to pure when touching them
3. **Core logic first**: Convert business logic before infrastructure
4. **Test coverage**: Ensure tests before refactoring
5. **Document decisions**: Note why certain code remains imperative
