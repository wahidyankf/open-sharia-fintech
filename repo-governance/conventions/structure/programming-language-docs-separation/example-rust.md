---
description: A worked example contrasting an ayokoding-www By Example variables lesson with the corresponding docs/explanation/ OSE Platform naming-conventions page
when_to_use: Read this when you need a concrete Rust-based illustration of how educational and repository-specific content should be split.
---

# Example 1: Rust - Correct Separation

**ayokoding-www** (a Rust By Example beginner lesson):

````markdown
# Rust By Example - Beginner

Educational content covering Rust fundamentals (0-40% coverage).

## Variables

Rust bindings are immutable unless you opt in:

```rust
// Immutable by default
let name: &str = "Alice";

// Type inference
let age = 30; // Type: i32

// Opt into mutation
let mut counter = 0;
counter += 1;
```
````

Key takeaway: Rust infers types, and `mut` is an explicit opt-in rather than the default.

````

**docs/explanation/** (`docs/explanation/software-engineering/programming-languages/rust/best-practices.md`):

```markdown
# Rust Best Practices - OSE Platform

**Prerequisite**: Complete the ayokoding-www Rust By Example tutorial.

## Naming Conventions

OSE Platform Rust code follows these conventions:

### Type Naming

- **Domain entities**: `UpperCamelCase` structs (`ZakatPayment`, `WaqfDonation`)
- **Repository methods**: prefix with the entity (`get_zakat_payment`, `save_waqf_donation`)
- **Service functions**: business-operation verbs (`calculate_zakat`, `process_donation`)

### Module Naming

- **Domain modules**: single word, singular (`zakat`, `waqf`, `murabaha`)
- **Infrastructure modules**: technical function (`repository`, `handler`, `middleware`)

**Rationale**: Aligns with [Explicit Over Implicit principle](../../../principles/software-engineering/explicit-over-implicit.md) — names clearly indicate Islamic finance domain concepts.
````

**Why this works**:

- **Separation**: ayokoding-www teaches Rust bindings (generic), docs/explanation/ defines OSE Platform naming
- **Prerequisite**: docs/explanation/ explicitly links to ayokoding-www
- **No duplication**: binding syntax in ayokoding-www, naming conventions in docs/explanation/
- **Clear scope**: ayokoding-www = education, docs/explanation/ = OSE Platform standards
