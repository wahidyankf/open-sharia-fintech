---
description: Defines pure and impure functions and contrasts their determinism, side-effect, and referential-transparency characteristics.
when_to_use: Use when clarifying the precise meaning of "pure function" before applying the principle.
---

# What

**Pure functions** are functions that:

1. **Deterministic**: Same inputs always produce same outputs
2. **No side effects**: Don't modify external state (variables, databases, files, network)
3. **Referentially transparent**: Can replace function call with its return value without changing program behaviour

**Impure functions** (with side effects):

1. **Non-deterministic**: Same inputs may produce different outputs
2. **Side effects**: Modify external state or depend on it
3. **Not referentially transparent**: Replacing call with value would change behaviour
