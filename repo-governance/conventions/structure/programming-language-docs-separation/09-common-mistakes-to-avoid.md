---
title: "Common Mistakes to Avoid"
description: Three worked FAIL/PASS pairs showing the most common ways teams accidentally duplicate educational content, omit prerequisites, or misplace repository-specific content
when_to_use: Read this when reviewing a docs/explanation/ or ayokoding-www draft for the most common content-separation mistakes before publishing.
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

# Common Mistakes to Avoid

## Mistake 1: Duplicating Educational Content

**FAIL: Duplicating in docs/explanation/**:

````markdown
# docs/explanation/.../rust/best-practices.md

## Variables in Rust

Rust bindings can be declared in several ways:

```rust
let x: i32 = 10;
let mut y = 20;
```
````

Use `let` for immutable bindings, `let mut` when you need mutation...

````

**Why it fails**: This is educational content about Rust syntax. Belongs in ayokoding-www, not docs/explanation/.

**PASS: Repository-specific convention**:

```markdown
# docs/explanation/.../rust/best-practices.md

**Prerequisite**: Complete the ayokoding-www Rust By Example tutorial.

## Naming in OSE Platform

OSE Platform Rust code follows these conventions:

- Domain entities: `ZakatPayment`, `WaqfDonation`
- Repository bindings: `zakat_repo`, `waqf_repo`
- Service bindings: `zakat_service`, `donation_service`

**Rationale**: Explicit domain terminology for Shariah compliance clarity.
````

**Why it passes**: Focuses on OSE Platform-specific naming, links to ayokoding-www for fundamentals.

## Mistake 2: Missing Prerequisite Statement

**FAIL: No prerequisite link**:

```markdown
# docs/explanation/.../typescript/README.md

# TypeScript

TypeScript is used for the web tier...

## Best Practices

Enable `strict` in tsconfig...
```

**Why it fails**: Doesn't tell developers where to learn TypeScript. Assumes knowledge.

**PASS: Explicit prerequisite**:

```markdown
# docs/explanation/.../typescript/README.md

# TypeScript

## Prerequisite Knowledge

**This documentation assumes you have completed the ayokoding-www TypeScript learning path**:

- [ayokoding-www TypeScript Overview](https://ayokoding.com/en/learn/.../typescript/)
- [By Example Tutorial](https://ayokoding.com/en/learn/.../typescript/by-example/)

If you're new to TypeScript, **start with ayokoding-www first**.

## What This Documentation Covers

OSE Platform-specific TypeScript conventions...
```

**Why it passes**: Explicit prerequisite statement, clear scope definition.

## Mistake 3: Repository-Specific Content in ayokoding-www

**FAIL: OSE Platform patterns in ayokoding-www**:

````markdown
# an ayokoding-www Rust in-practice error-handling lesson

## Error Handling

In OSE Platform, all errors must include request IDs and error codes:

```rust
tracing::error!(request_id = %req_id, error_code = "ERRZAKAT001",
    "operation failed");
```
````

````

**Why it fails**: This is OSE Platform-specific convention. Belongs in docs/explanation/, not ayokoding-www.

**PASS: Generic Rust error patterns**:

```markdown
# an ayokoding-www Rust in-practice error-handling lesson

## Error Handling in Rust

Rust returns fallibility in the type:

```rust
fn divide(a: i32, b: i32) -> Result<i32, DivideError> {
    if b == 0 {
        return Err(DivideError::ByZero);
    }
    Ok(a / b)
}

let result = divide(10, 2)?;
````

Key takeaway: handle `Result` explicitly, propagate with `?`, add context at the boundary.

```

**Why it passes**: Generic Rust error patterns, no OSE Platform-specific conventions.
```
