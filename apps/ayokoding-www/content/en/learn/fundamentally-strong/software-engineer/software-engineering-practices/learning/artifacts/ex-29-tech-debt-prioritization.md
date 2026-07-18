---
title: "Artifact: Technical-Debt Prioritization by Friction"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 69
---

> ex-29 &middot; exercises co-16 &middot; ranking three logged debt items by ongoing friction, not
> recency.

| Debt item                                                 | Logged              | Ongoing friction                                                                                                    | Rank |
| --------------------------------------------------------- | ------------------- | ------------------------------------------------------------------------------------------------------------------- | ---- |
| DEBT-041: missing row lock on gift-card redemption        | 2026-07-18 (newest) | Low -- estimated <0.01% of redemptions affected, no reported incident yet                                           | 3rd  |
| DEBT-019: pricing logic duplicated across 4 files         | 2026-03-02          | High -- every pricing change now needs 4 coordinated edits, and 2 of the last 6 pricing bugs were a missed 4th file | 1st  |
| DEBT-027: test suite takes 22 minutes, no parallelization | 2026-05-14          | Medium-high -- slows every single PR's feedback loop, but has a known, scoped fix (pytest-xdist) already estimated  | 2nd  |

**Verify**: DEBT-019 (2nd-oldest) ranks 1st because it costs the MOST ongoing friction (a
recurring, measured defect source), not because it is the oldest -- and DEBT-041 (newest) ranks
last because its current friction is genuinely low, satisfying co-16's "rank by friction, not
recency" rule.

**Key takeaway**: age and friction are independent properties of a debt item -- the oldest item is
not automatically the most urgent, and the newest is not automatically the least.

**Why It Matters**: a backlog sorted by creation date silently promotes stale but low-impact debt
over recent, high-impact debt just because it has been sitting longer, which is exactly the kind of
"loudest ticket wins" prioritization a friction-based ranking is designed to prevent.
