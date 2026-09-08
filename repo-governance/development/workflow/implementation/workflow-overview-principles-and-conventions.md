---
description: The three-stage workflow at a glance, and the principles and conventions it implements/respects.
when_to_use: Use when orienting to the three-stage workflow's shape, or tracing it back to the principles and conventions it implements.
---

# Workflow Overview, Principles, and Conventions

## Workflow Overview

The implementation workflow follows three sequential stages:

1. **Make it work** - Get functionality working with the simplest solution
2. **Make it right** - Refactor for readability, maintainability, and clean code
3. **Make it fast** - Optimize performance ONLY if proven necessary by measurements

**Key principle**: Each stage is complete before moving to the next. Don't skip stages or combine them.

Additionally, this workflow includes two cross-cutting practices:

- **Surgical Changes** - Touch only what you must when editing existing code
- **Goal-Driven Execution** - Define success criteria, loop until verified

## Principles Implemented/Respected

This workflow respects three core principles:

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)** - Start with the simplest solution that works
- **[YAGNI (You Aren't Gonna Need It)](../../../principles/general/simplicity-over-complexity/why.md#kiss-and-yagni-principles)** - Don't optimize prematurely
- **[Progressive Disclosure](../../../principles/content/progressive-disclosure.md)** - Layer refinement gradually

## Conventions Implemented/Respected

**REQUIRED SECTION**: All development practice documents MUST include this section to ensure traceability from practices to documentation standards.

This practice implements/respects the following conventions:

- **[Code Quality Convention](../../quality/code.md)**: The "make it right" stage applies code quality standards (Prettier formatting, linting) before the "make it fast" stage to ensure clean code before optimization.

- **[Content Quality Principles](../../../conventions/writing/quality.md)**: Implementation workflow follows the same progressive layering philosophy - start simple (work), add structure and clarity (right), then refine performance (fast).

### Benefits of This Workflow

1. **Faster to Working Software**: Focus on functionality first gets you to a working state quickly
2. **Prevents Over-Engineering**: Avoid building unnecessary abstractions or optimizations
3. **Clearer Thinking**: Separating concerns (work vs right vs fast) reduces cognitive load
4. **Data-Driven Optimization**: Only optimize based on actual measurements, not guesses
5. **Better Code Quality**: Clean code before optimization prevents optimization of bad code

### Problems with Premature Optimization

1. **Wasted Effort**: Optimizing code that doesn't need to be fast
2. **Complex Code**: Optimized code is often harder to understand and maintain
3. **Wrong Optimizations**: Optimizing the wrong parts (not the bottleneck)
4. **Delayed Delivery**: Time spent optimizing instead of delivering features
5. **Technical Debt**: Rushing quality to add optimization creates maintainability issues

### The Famous Quote

> "Premature optimization is the root of all evil (or at least most of it) in programming."
> — Donald Knuth, "The Art of Computer Programming"
