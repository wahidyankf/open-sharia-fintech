---
title: "Artifact: Technical-Debt Log Entry"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 68
---

> ex-28 &middot; exercises co-16 &middot; a shortcut, logged with an owner, a rationale, and its
> Fowler quadrant.

```text
## DEBT-041: gift-card redemption skips concurrent-redemption locking

Logged: 2026-07-18
Owner: @dev-checkout-team
Quadrant: PRUDENT + DELIBERATE (Fowler's technical-debt quadrant)

Context: shipped without a row-level lock on card balance during redemption, to hit the holiday
launch date. Two simultaneous redemptions on the SAME card could theoretically both read the
balance before either writes it back, over-redeeming the card.

Why this is PRUDENT: the team discussed the trade-off explicitly and chose it deliberately --
double-redemption on the same card within the same second is rare (estimated <0.01% of
redemptions) and the launch date was fixed. This is not an accidental gap; it's a KNOWN, chosen
one.

Why this is DELIBERATE: the exact fix (a `SELECT ... FOR UPDATE` row lock) is already scoped and
estimated (~1 day), just not done before launch.

Follow-up: add the row lock before Black Friday traffic (DEBT-041, owner @dev-checkout-team,
target: next sprint).
```

**Verify**: the entry names its specific quadrant (prudent + deliberate, not reckless or
inadvertent) and justifies the classification with the actual trade-off reasoning, not just a label.

**Key takeaway**: a debt item is not "bad code" by default -- prudent-deliberate debt is a
conscious, reasonable trade against a real constraint (the launch date), logged so it does not
silently become permanent.

**Why It Matters**: an unlogged shortcut disappears into "we'll get to it," while a logged one with
an owner and a Fowler quadrant becomes a real, prioritizable backlog item -- Example 29 shows exactly
how that prioritization works once several debt items compete for the same sprint.
