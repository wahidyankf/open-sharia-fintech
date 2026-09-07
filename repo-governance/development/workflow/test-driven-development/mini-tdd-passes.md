---
description: Splitting a feature or bug fix into multiple small Red-Green-Refactor cycles instead of one large test.
when_to_use: Use when a delivery checklist item like "implement email validation" needs breaking into a sequence of small TDD cycles.
---

# Mini-TDD Passes

A single feature or bug fix does not require one large test up front. Split it into multiple small
Red→Green→Refactor cycles:

- Write the simplest scenario first (the happy path or the most constrained input).
- Pass it.
- Write the next scenario (an edge case, an error condition, a boundary).
- Pass it.
- Continue until all required behaviour is covered.

This keeps each cycle short, observable, and safe to commit. A delivery checklist item like
"implement email validation" becomes a sequence of mini-cycles:

```
Red:   test "empty string is invalid"     → Green → Refactor
Red:   test "string without @ is invalid" → Green → Refactor
Red:   test "valid address is accepted"   → Green → Refactor
Red:   test "address without domain is invalid" → Green → Refactor
```

Each mini-cycle is independently committable. Prefer granular commits over one large "implement
feature" commit.
