---
description: Applies the minimal-sufficiency test to lasting mechanisms, completion, and mandatory safeguards.
when_to_use: Use when choosing an implementation or deciding when work is complete.
---

# Implementation Guidelines

## Smallest Responsible Change

Apply the canonical [Minimal Sufficiency Test](./minimal-sufficiency-test.md#minimal-sufficiency-test).
Start from the outcome and applicable rules, inspect existing mechanisms, and add only what the
responsible solution requires.

**Core Rules:**

1. **No features beyond what was asked**
   - Don't add "nice to have" functionality
   - Don't anticipate future requirements
   - Don't build flexibility that wasn't requested

2. **No abstractions for single-use code**
   - Three similar lines are better than premature abstraction
   - Don't create helpers for one-time operations
   - Don't design for hypothetical reuse

3. **No unnecessary lasting mechanisms**
   - Don't add configuration options that weren't requested
   - Reuse an existing dependency, validator, workflow, automation, or infrastructure path when it
     satisfies the need
   - Name the concrete requirement or demonstrated risk before adding a new mechanism

4. **No error handling for impossible scenarios**
   - Trust internal code and framework guarantees
   - Only validate at system boundaries (user input, external APIs)
   - Don't add defensive code for scenarios that can't happen

5. **Length as a smell**
   - If you write 200 lines and it could be 50, rewrite it
   - More code = more bugs, more maintenance
   - Brevity is a virtue when clarity is maintained

## Completion and Safeguards

- Treat the requested outcome plus applicable rules as the completion boundary
- Keep verification proportional to the change and its risk
- Stop when that outcome is achieved and every required check passes
- Do not expand a one-off change into generalized machinery without a demonstrated recurring need
- Never use minimal sufficiency to skip TDD, specifications, regression tests, accessibility,
  security, documentation, governance propagation, or required quality gates

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
- Work continuing after the outcome and required checks are complete
- A new lasting mechanism whose concrete need cannot be named
