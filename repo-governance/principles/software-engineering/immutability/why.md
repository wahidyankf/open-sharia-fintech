---
description: Lists the benefits of immutability, the problems mutability causes, and when immutability should and should not be used.
when_to_use: Use when justifying a choice to use (or avoid) immutable data structures in a design discussion or code review.
---

# Why

## Benefits of Immutability

1. **Predictability**: Same input always produces same output, no hidden state changes
2. **Concurrency Safety**: No race conditions when multiple threads access immutable data
3. **Easier Debugging**: State doesn't change unexpectedly, simpler to trace bugs
4. **Time Travel**: Previous states are preserved, enabling undo/replay functionality
5. **Simpler Reasoning**: Don't need to track when/where/how data might change
6. **Caching Friendly**: Immutable values can be safely cached and reused

## Problems with Mutability

1. **Race Conditions**: Multiple threads modifying same data leads to unpredictable results
2. **Action at a Distance**: Changing data in one place affects code far away
3. **Hard to Debug**: State changes throughout execution, difficult to track down bugs
4. **Lost History**: Previous states overwritten, can't trace how we got to current state
5. **Coupling**: Code becomes tightly coupled through shared mutable state
6. **Unexpected Side Effects**: Functions may modify inputs, breaking assumptions

## When to Use Immutability

**Use immutability when**:

- PASS: Building concurrent or parallel systems
- PASS: Implementing business logic with multiple calculations
- PASS: Creating audit trails or event logs
- PASS: Handling user input or external data
- PASS: Working with complex state management

**Mutability acceptable when**:

- Performance profiling shows immutability is bottleneck (rare)
- Building performance-critical inner loops (games, video processing)
- Interfacing with mutable libraries (use at boundaries only)
- Managing large datasets where copying is prohibitive
