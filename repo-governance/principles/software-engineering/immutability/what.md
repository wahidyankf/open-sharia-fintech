---
title: "What"
description: Defines immutability and mutability and contrasts their core characteristics.
category: explanation
subcategory: principles
tags:
  - principles
  - functional-programming
  - immutability
  - data-structures
  - concurrency
created: 2025-12-28
when_to_use: Use when clarifying the precise meaning of "immutable" versus "mutable" before applying the principle.
---

# What

**Immutability** means:

- Data cannot be changed after creation
- Modifications create new values instead of altering existing ones
- Original values remain unchanged
- State changes are explicit (new variables, new objects)
- Data flow is unidirectional and traceable

**Mutability** means:

- Data can be changed in place
- Modifications alter existing values
- Original values are lost
- State changes are implicit (same variable, different value)
- Data flow is bidirectional and harder to trace
