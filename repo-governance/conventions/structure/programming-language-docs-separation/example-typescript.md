---
title: "Example 2: TypeScript — Correct Separation"
description: A worked example contrasting an ayokoding-www generic error-handling lesson with the corresponding docs/explanation/ OSE Platform domain error hierarchy
when_to_use: Read this when you need a concrete TypeScript-based illustration of how educational and repository-specific content should be split.
category: explanation
subcategory: conventions
tags:
  - documentation
  - programming-languages
  - style-guides
  - content-separation
  - dry-principle
created: 2026-02-04
---

# Example 2: TypeScript - Correct Separation

**ayokoding-www** (a TypeScript in-practice error-handling lesson):

````markdown
# Error Handling in TypeScript

Generic TypeScript error patterns.

## Try/Catch

TypeScript narrows a caught value before you can use it:

```typescript
try {
  const result = riskyOperation();
} catch (e: unknown) {
  if (e instanceof RangeError) {
    console.error(`Invalid value: ${e.message}`);
  } else {
    console.error("Unexpected error", e);
  }
} finally {
  cleanup();
}
```
````

Key takeaway: a caught value is `unknown` — narrow it before use, and always handle errors explicitly.

````

**docs/explanation/** (`docs/explanation/software-engineering/programming-languages/typescript/error-handling.md`):

```markdown
# TypeScript Error Handling - OSE Platform Standards

**Prerequisite**: Complete the ayokoding-www TypeScript error-handling lesson.

## OSE Platform Error Hierarchy

OSE Platform defines a domain error hierarchy for Shariah compliance:

```typescript
export class ShariaComplianceError extends Error {}

export class InterestViolationError extends ShariaComplianceError {
  constructor(
    readonly amount: bigint,
    readonly transactionId: string,
  ) {
    super(`Interest detected: ${amount} in ${transactionId}`);
  }
}

export class ProhibitedInvestmentError extends ShariaComplianceError {}
````

**Usage in services**:

```typescript
export function validateTransaction(tx: Transaction): void {
  if (tx.interestAmount > 0n) {
    throw new InterestViolationError(tx.interestAmount, tx.id);
  }
}
```

**Why**: Domain errors enable Shariah audit trails, compliance monitoring, and clear error semantics.

```

**Why this works**:

- **Separation**: ayokoding-www teaches TypeScript try/catch (generic), docs/explanation/ defines OSE Platform domain errors
- **Prerequisite**: docs/explanation/ explicitly links to ayokoding-www
- **No duplication**: generic try/catch in ayokoding-www, domain hierarchy in docs/explanation/
- **Clear scope**: ayokoding-www = TypeScript fundamentals, docs/explanation/ = Shariah compliance patterns
```
