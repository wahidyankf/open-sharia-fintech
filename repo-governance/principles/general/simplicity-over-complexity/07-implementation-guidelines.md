---
title: "Implementation Guidelines"
description: Five rules for minimum code with maximum clarity, plus the senior engineer test.
category: explanation
subcategory: principles
tags:
  - principles
  - simplicity
  - over-engineering
created: 2025-12-15
when_to_use: Use when writing new code and avoiding speculative features.
---

# Implementation Guidelines

## Minimum Code, Maximum Clarity

Write the minimum code that solves the problem. Nothing speculative.

**Core Rules:**

1. **No features beyond what was asked**
   - Don't add "nice to have" functionality
   - Don't anticipate future requirements
   - Don't build flexibility that wasn't requested

2. **No abstractions for single-use code**
   - Three similar lines are better than premature abstraction
   - Don't create helpers for one-time operations
   - Don't design for hypothetical reuse

3. **No unnecessary configurability**
   - Don't add configuration options that weren't requested
   - Hard-code when appropriate
   - Avoid feature flags for non-existent use cases

4. **No error handling for impossible scenarios**
   - Trust internal code and framework guarantees
   - Only validate at system boundaries (user input, external APIs)
   - Don't add defensive code for scenarios that can't happen

5. **Length as a smell**
   - If you write 200 lines and it could be 50, rewrite it
   - More code = more bugs, more maintenance
   - Brevity is a virtue when clarity is maintained

## The Senior Engineer Test

**Ask yourself**: "Would a senior engineer say this is overcomplicated?"

If yes, simplify. Keep asking until the answer is no.

**Warning signs of over-engineering:**

- Helper functions used once
- Configuration for scenarios that don't exist
- Abstractions that obscure rather than clarify
- Error handling for impossible conditions
- "Flexibility" that adds complexity without clear benefit
- Code doing more than requested
