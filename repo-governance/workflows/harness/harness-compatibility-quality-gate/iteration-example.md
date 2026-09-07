---
description: Worked traces for pending lifecycle evidence and an out-of-scope external-drift finding.
when_to_use: Use when you want a concrete trace of how iterations, fixes, and re-validation play out.
---

# Iteration Example

Typical execution flow when domain checks are clean but delegated evidence is stale:

```
Step 0: Resolve lifecycle ownership
  Binding predicate → pending (evidence head is stale)

Step 1: Initial validation
  Unowned semantic parity and external drift → 0 domain findings

Step 4: Re-validate
  Iteration 2 → 0 findings (consecutive_zero: 1)

Step 5: Iteration control → loop to re-validate

Step 4: Re-validate
  Iteration 3 → 0 findings (consecutive_zero: 2 — double-zero confirmed)

Result: final-status PASS; lifecycle-status PENDING
```

Typical flow when out-of-scope findings are present:

```
Iteration 1:
  Check → 1 finding (new higher-precedence filename for a harness)
  Fix   → Flags as out-of-scope: human action required
Result: PARTIAL after 1 iteration; user must resolve before re-running.
```
