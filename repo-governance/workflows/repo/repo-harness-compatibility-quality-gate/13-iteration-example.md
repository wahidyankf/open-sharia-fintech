---
title: "Iteration Example"
description: Two worked traces — a typical sync-drift-only run reaching double-zero success, and an out-of-scope finding reaching partial.
when_to_use: Use when you want a concrete trace of how iterations, fixes, and re-validation play out.
---

# Iteration Example

Typical execution flow when the only outstanding issue is parity sync drift:

```
Step 1: Initial validation (Phase 0)
  Invariant 3 → 1 finding (sync drift)

Step 3: Apply fixes
  Fixer runs npm run generate:bindings → agents regenerated
  Stages .opencode/agents/<changed>.md

Step 4: Re-validate
  Iteration 2 → 0 findings (consecutive_zero: 1)

Step 5: Iteration control → loop to re-validate

Step 4: Re-validate
  Iteration 3 → 0 findings (consecutive_zero: 2 — double-zero confirmed)

Result: SUCCESS (3 iterations)
```

Typical flow when out-of-scope findings are present:

```
Iteration 1:
  Check → 1 finding (new higher-precedence filename for a harness)
  Fix   → Flags as out-of-scope: human action required
Result: PARTIAL after 1 iteration; user must resolve before re-running.
```
