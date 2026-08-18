---
title: "When to Apply and References"
description: Where the three-stage workflow applies, its exceptions, and further reading on the underlying software-engineering ideas.
category: explanation
subcategory: development
tags:
  - development
  - workflow
  - implementation
  - optimization
  - refactoring
  - surgical-changes
  - goal-driven
  - test-driven
created: 2025-12-15
when_to_use: Use when deciding whether the full three-stage workflow applies to a task, or when looking for further reading.
---

# When to Apply and References

## When to Apply

### Apply This Workflow For

**New feature development**:

```
1. Make it work: Get feature functioning
2. Make it right: Clean up code, add tests
3. Make it fast: Optimize ONLY if performance requirements not met
```

**Bug fixes**:

```
1. Make it work: Fix the bug with simplest solution
2. Make it right: Refactor to prevent similar bugs
3. Make it fast: Usually not needed for bug fixes
```

**Refactoring**:

```
1. Already works: Start at Stage 2
2. Make it right: Improve structure and readability
3. Make it fast: Only if measurements show need
```

### Exceptions to the Workflow

**Security fixes**: Priority is "make it secure" (right), not "make it work"

```typescript
// Security fix: Correctness > Speed
function sanitizeInput(input: string): string {
  // Make it RIGHT first (secure), not just working
  return DOMPurify.sanitize(input, { SAFE_FOR_TEMPLATES: true });
}
```

**Production hotfixes**: Sometimes "make it work" is enough (fix immediately, refactor later)

```typescript
// Hotfix: Stop the bleeding first
function emergencyFix() {
  // Stage 1: Make it work (deploy immediately)
  if (data === null) return []; // Quick fix

  // Stage 2: Create ticket to "make it right" later
  // TODO: Refactor data handling (Ticket #123)
}
```

**Performance-critical code**: May need optimization from start (e.g., game engines, real-time systems)

```typescript
// Real-time video processing: Performance is a requirement
function processVideoFrame(frame: Frame): ProcessedFrame {
  // Even Stage 1 must consider performance
  // But still: work → right → fast
}
```

## References

**Software Engineering Principles**:

- [The Art of Computer Programming](https://en.wikipedia.org/wiki/The_Art_of_Computer_Programming) - Donald Knuth (premature optimization quote)
- [Refactoring: Improving the Design of Existing Code](https://martinfowler.com/books/refactoring.html) - Martin Fowler
- [Clean Code](https://www.oreilly.com/library/view/clean-code-a/9780136083238/) - Robert C. Martin

**Make It Work, Make It Right, Make It Fast**:

- [Kent Beck on Twitter](https://twitter.com/kentbeck) - Original "make it work, make it right, make it fast" attribution
- [Extreme Programming Explained](https://www.oreilly.com/library/view/extreme-programming-explained/0201616416/) - Kent Beck

**Performance Optimization**:

- [High Performance Browser Networking](https://hpbn.co/) - Ilya Grigorik
- [JavaScript Performance](https://developer.mozilla.org/en-US/docs/Web/Performance) - MDN Web Docs
- [Web Performance Optimization](https://web.dev/fast/) - Google Web Fundamentals
