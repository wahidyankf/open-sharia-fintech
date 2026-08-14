---
title: "Example 1: Golang — Correct Separation"
description: A worked example contrasting an ayokoding-www By Example variables lesson with the corresponding docs/explanation/ OSE Platform naming-conventions page
when_to_use: Read this when you need a concrete Golang-based illustration of how educational and repository-specific content should be split.
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

# Example 1: Golang - Correct Separation

**ayokoding-www** (`apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/golang/by-example/beginner.md`):

````markdown
# Go By Example - Beginner

Educational content covering Go fundamentals (0-40% coverage).

## Variables

Go variables are explicitly typed:

```go
// Explicitly typed
var name string = "Alice"

// Type inference
age := 30 // Type: int

// Multiple variables
var x, y int = 1, 2
```
````

Key takeaway: Go supports both explicit types and type inference via `:=`.

````

**docs/explanation/** (`docs/explanation/software-engineering/programming-languages/golang/best-practices.md`):

```markdown
# Go Best Practices - OSE Platform

**Prerequisite**: Complete [ayokoding-www Golang By Example](https://ayokoding.com/en/learn/software-engineering/programming-languages/golang/by-example/).

## Naming Conventions

OSE Platform Go code follows these conventions:

### Variable Naming

- **Domain entities**: CamelCase structs (`ZakatPayment`, `WaqfDonation`)
- **Repository methods**: Prefix with entity (`GetZakatPayment`, `SaveWaqfDonation`)
- **Service methods**: Business operation verbs (`CalculateZakat`, `ProcessDonation`)

### Package Naming

- **Domain packages**: Single word, singular (`zakat`, `waqf`, `murabaha`)
- **Infrastructure packages**: Technical function (`repository`, `handler`, `middleware`)

**Rationale**: Aligns with [Explicit Over Implicit principle](../../../principles/software-engineering/explicit-over-implicit.md) — names clearly indicate Islamic finance domain concepts.
````

**Why this works**:

- **Separation**: ayokoding-www teaches Go variables (generic), docs/explanation/ defines OSE Platform naming
- **Prerequisite**: docs/explanation/ explicitly links to ayokoding-www
- **No duplication**: Variable syntax in ayokoding-www, naming conventions in docs/explanation/
- **Clear scope**: ayokoding-www = education, docs/explanation/ = OSE Platform standards
