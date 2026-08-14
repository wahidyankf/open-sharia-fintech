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
# docs/explanation/.../golang/best-practices.md

## Variables in Go

Go variables can be declared in multiple ways:

```go
var x int = 10
y := 20
```
````

Use `:=` for local variables, `var` for package-level...

````

**Why it fails**: This is educational content about Go syntax. Belongs in ayokoding-www, not docs/explanation/.

**PASS: Repository-specific convention**:

```markdown
# docs/explanation/.../golang/best-practices.md

**Prerequisite**: Complete [ayokoding-www Golang By Example](https://ayokoding.com/en/learn/.../golang/by-example/).

## Variable Naming in OSE Platform

OSE Platform Go code follows these conventions:

- Domain entities: `ZakatPayment`, `WaqfDonation`
- Repository variables: `zakatRepo`, `waqfRepo`
- Service variables: `zakatService`, `donationService`

**Rationale**: Explicit domain terminology for Shariah compliance clarity.
````

**Why it passes**: Focuses on OSE Platform-specific naming, links to ayokoding-www for fundamentals.

## Mistake 2: Missing Prerequisite Statement

**FAIL: No prerequisite link**:

```markdown
# docs/explanation/.../python/README.md

# Python

Python is used for data processing...

## Best Practices

Follow PEP 8 standards...
```

**Why it fails**: Doesn't tell developers where to learn Python. Assumes knowledge.

**PASS: Explicit prerequisite**:

```markdown
# docs/explanation/.../python/README.md

# Python

## Prerequisite Knowledge

**This documentation assumes you have completed the ayokoding-www Python learning path**:

- [ayokoding-www Python Overview](https://ayokoding.com/en/learn/.../python/)
- [By Example Tutorial](https://ayokoding.com/en/learn/.../python/by-example/)

If you're new to Python, **start with ayokoding-www first**.

## What This Documentation Covers

OSE Platform-specific Python conventions...
```

**Why it passes**: Explicit prerequisite statement, clear scope definition.

## Mistake 3: Repository-Specific Content in ayokoding-www

**FAIL: OSE Platform patterns in ayokoding-www**:

````markdown
# apps/ayokoding-www/.../golang/in-practice/error-handling.md

## Error Handling

In OSE Platform, all errors must include request IDs and error codes:

```go
if err != nil {
    logger.Error("operation failed",
        "request_id", reqID,
        "error_code", "ERRZAKAT001")
}
```
````

````

**Why it fails**: This is OSE Platform-specific convention. Belongs in docs/explanation/, not ayokoding-www.

**PASS: Generic Go error patterns**:

```markdown
# apps/ayokoding-www/.../golang/in-practice/error-handling.md

## Error Handling in Go

Go uses explicit error returns:

```go
func divide(a, b int) (int, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

result, err := divide(10, 2)
if err != nil {
    return fmt.Errorf("divide failed: %w", err)
}
````

Key takeaway: Check errors explicitly, wrap with context using `%w`.

```

**Why it passes**: Generic Go error patterns, no OSE Platform-specific conventions.
```
