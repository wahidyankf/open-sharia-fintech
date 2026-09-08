---
description: Lists the benefits of pure functions, the problems side effects cause, and when each applies.
when_to_use: Use when justifying a choice to isolate side effects and keep logic pure.
---

# Why

## Benefits of Pure Functions

1. **Easy to Test**: No mocking, no setup - just input and output
2. **Easy to Reason About**: No hidden dependencies, behaviour is obvious
3. **Cacheable**: Same inputs = same outputs, results can be memoized
4. **Parallelizable**: No shared state, safe to run concurrently
5. **Composable**: Combine pure functions to build complex logic
6. **Debugging**: Easier to trace bugs when functions don't affect each other

## Problems with Side Effects

1. **Hard to Test**: Require mocking external dependencies
2. **Hard to Understand**: Hidden dependencies on global state
3. **Not Cacheable**: Results may differ, can't safely memoize
4. **Concurrency Issues**: Shared state leads to race conditions
5. **Tight Coupling**: Functions depend on external context
6. **Debugging Nightmares**: Changes propagate unpredictably

## When to Use Pure Functions

**Use pure functions for**:

- PASS: Business logic and calculations
- PASS: Data transformations
- PASS: Validation rules
- PASS: Formatting and parsing
- PASS: Mathematical operations
- PASS: Filters, maps, reduces

**Side effects necessary for**:

- I/O operations (database, files, network)
- Logging and monitoring
- Random number generation
- Current time/date
- User interaction
- System state changes

**Best practice**: Use Functional Core, Imperative Shell pattern - pure functions for logic, side effects at boundaries.
