---
title: "Example 3: Java — Correct Separation"
description: A worked example contrasting an ayokoding-www Optional-for-null-safety lesson with the corresponding docs/explanation/ OSE Platform mandatory-Optional-usage rule
when_to_use: Read this when you need a concrete Java-based illustration of how educational and repository-specific content should be split.
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

# Example 3: Java - Correct Separation

**ayokoding-www** (`apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/java/by-example/intermediate.md`):

````markdown
# Java By Example - Intermediate

Educational content covering Java intermediate concepts (40-75% coverage).

## Optional for Null Safety

Java's `Optional<T>` prevents null pointer exceptions:

```java
Optional<String> optional = Optional.of("value");

// Check presence
if (optional.isPresent()) {
    String value = optional.get();
}

// Provide default
String value = optional.orElse("default");

// Map transformation
Optional<Integer> length = optional.map(String::length);
```
````

Key takeaway: Use `Optional<T>` to explicitly represent absence, never return null.

````

**docs/explanation/** (`docs/explanation/software-engineering/programming-languages/java/type-safety.md`):

```markdown
# Java Type Safety - OSE Platform Standards

**Prerequisite**: Complete [ayokoding-www Java By Example](https://ayokoding.com/en/learn/software-engineering/programming-languages/java/by-example/).

## Mandatory Optional Usage

In OSE Platform Java code, `Optional<T>` is **REQUIRED** for:

1. **Domain entity optional fields**:

```java
public class ZakatPayment {
    private final UUID id;
    private final Decimal amount;
    private final Optional<String> referenceNumber; // REQUIRED: Use Optional
    private final Optional<Instant> completedAt;   // REQUIRED: Use Optional
}
````

1. **Repository query methods**:

```java
public interface ZakatPaymentRepository {
    Optional<ZakatPayment> findById(UUID id);        // REQUIRED
    Optional<ZakatPayment> findByReference(String ref); // REQUIRED
}
```

**FORBIDDEN patterns**:

```java
// ❌ FORBIDDEN: Returning null
ZakatPayment findById(UUID id) {
    return null; // Violates Explicit Over Implicit
}

// ✅ REQUIRED: Return Optional
Optional<ZakatPayment> findById(UUID id) {
    return Optional.empty(); // Explicit absence
}
```

**Rationale**: Aligns with [Explicit Over Implicit principle](../../principles/software-engineering/explicit-over-implicit.md) — absence is explicit, checked at compile-time.

```

**Why this works**:

- **Separation**: ayokoding-www teaches `Optional<T>` API (generic), docs/explanation/ mandates OSE Platform usage
- **Prerequisite**: docs/explanation/ explicitly links to ayokoding-www
- **No duplication**: Generic `Optional` usage in ayokoding-www, mandatory patterns in docs/explanation/
- **Clear scope**: ayokoding-www = Java `Optional` education, docs/explanation/ = OSE Platform enforcement
```
