---
title: "Artifact: Token-Usage-per-Turn Log"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 58
---

> A five-row table tracking token cost per turn against a stated budget ceiling -- exercises
> co-18.

| Turn | Tokens this turn | Cumulative | Budget ceiling |
| ---- | ---------------- | ---------- | -------------- |
| 1    | 3,200            | 3,200      | 50,000         |
| 2    | 5,800            | 9,000      | 50,000         |
| 3    | 4,100            | 13,100     | 50,000         |
| 4    | 12,600           | 25,700     | 50,000         |
| 5    | 8,900            | 34,600     | 50,000         |

**Verify**: the cumulative total after turn 5 (34,600) is checked directly against the stated
budget ceiling (50,000) -- 34,600 is under the ceiling, leaving roughly 15,400 tokens of headroom
-- satisfying ex-18's rule of checking the running total against a stated budget ceiling.
