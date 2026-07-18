---
title: "Artifact: One Falsifiable Hypothesis Before the Debugger"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 63
---

> ex-23 &middot; exercises co-13 &middot; expected-vs-actual, then exactly one hypothesis, checked
> once.

**Bug**: `apply_discount(100.0, 0.2)` returns `20.0`. **Expected**: `80.0`.

```text
Expected: apply_discount(100.0, 0.2) == 80.0  (a 20% discount KEEPS 80% of the total)
Actual:   apply_discount(100.0, 0.2) == 20.0

Hypothesis: the function returns `total * pct` (the DISCOUNT amount) instead of
`total * (1 - pct)` (the amount KEPT after the discount) -- i.e. the two quantities are swapped.

One check: read discount.py's return line directly.
  return total * pct     <- confirms the hypothesis exactly; no other check needed.
```

**Verify**: exactly one hypothesis is stated, and exactly one check (reading the single return line)
either confirms or refutes it -- no debugger session, no scattershot print statements across the
whole call stack, satisfying co-13's discipline.

**Key takeaway**: a hypothesis narrow enough to be wrong in one specific way needs only one check to
resolve -- the discipline is in narrowing the guess before looking, not in how the bug is eventually
found.

**Why It Matters**: undisciplined debugging (add a print statement everywhere, rerun, stare at the
output) finds bugs eventually but generates noise and rarely produces a reusable insight; one
falsifiable hypothesis, confirmed or refuted by exactly one targeted check, is the fastest path AND
leaves behind a clear, one-sentence explanation of what actually went wrong.
