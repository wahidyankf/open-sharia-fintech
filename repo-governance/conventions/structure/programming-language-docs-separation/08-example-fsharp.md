---
title: "Example 3: F# — Correct Separation"
description: A worked example contrasting an ayokoding-www Option-for-null-safety lesson with the corresponding docs/explanation/ OSE Platform mandatory-Option-usage rule
when_to_use: Read this when you need a concrete F#-based illustration of how educational and repository-specific content should be split.
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

# Example 3: F# - Correct Separation

**ayokoding-www** (an F# By Example intermediate lesson):

````markdown
# F# By Example - Intermediate

Educational content covering F# intermediate concepts (40-75% coverage).

## Option for Null Safety

F#'s `Option<'T>` represents absence without null:

```fsharp
let optional = Some "value"

// Pattern match on presence
match optional with
| Some value -> printfn "%s" value
| None -> printfn "absent"

// Provide a default
let value = optional |> Option.defaultValue "default"

// Map transformation
let length = optional |> Option.map String.length
```
````

Key takeaway: use `Option<'T>` to represent absence explicitly, never return null.

````

**docs/explanation/** (`docs/explanation/software-engineering/programming-languages/f-sharp/type-safety-standards.md`):

```markdown
# F# Type Safety - OSE Platform Standards

**Prerequisite**: Complete the ayokoding-www F# By Example tutorial.

## Mandatory Option Usage

In OSE Platform F# code, `Option<'T>` is **REQUIRED** for:

1. **Domain record optional fields**:

```fsharp
type ZakatPayment =
    { Id: Guid
      Amount: decimal
      ReferenceNumber: string option   // REQUIRED: use option
      CompletedAt: DateTimeOffset option } // REQUIRED: use option
````

1. **Repository query functions**:

```fsharp
type IZakatPaymentRepository =
    abstract FindById: Guid -> ZakatPayment option              // REQUIRED
    abstract FindByReference: string -> ZakatPayment option     // REQUIRED
```

**FORBIDDEN patterns**:

```fsharp
// ❌ FORBIDDEN: returning a nullable reference
let findById (id: Guid) : ZakatPayment =
    Unchecked.defaultof<ZakatPayment> // Violates Explicit Over Implicit

// ✅ REQUIRED: return an option
let findById (id: Guid) : ZakatPayment option =
    None // Explicit absence
```

**Rationale**: Aligns with [Explicit Over Implicit principle](../../../principles/software-engineering/explicit-over-implicit.md) — absence is explicit, checked at compile-time.

```

**Why this works**:

- **Separation**: ayokoding-www teaches the `Option<'T>` API (generic), docs/explanation/ mandates OSE Platform usage
- **Prerequisite**: docs/explanation/ explicitly links to ayokoding-www
- **No duplication**: generic `Option` usage in ayokoding-www, mandatory patterns in docs/explanation/
- **Clear scope**: ayokoding-www = F# `Option` education, docs/explanation/ = OSE Platform enforcement
```
