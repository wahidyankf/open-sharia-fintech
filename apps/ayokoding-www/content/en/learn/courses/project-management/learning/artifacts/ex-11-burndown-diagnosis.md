---
title: "Artifact: Burndown Diagnosis — Sprint 2"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 51
---

> Aurora Checkout Redesign -- burndown diagnosis -- exercises co-09.

| Day | Remaining points | Note                                                             |
| --- | ---------------- | ---------------------------------------------------------------- |
| 4   | 8                | On pace.                                                         |
| 5   | 8                | Flatline begins.                                                 |
| 6   | 8                | Flatline continues.                                              |
| 7   | 8                | Flatline continues -- three full days with zero progress logged. |
| 8   | 5                | Resumes dropping.                                                |

**Cause**: the shared staging environment was down for two of the three flatlined days, waiting on a
security patch from the platform team. No individual story looked "blocked" until someone actually
needed to deploy and test against staging on day 6.

**Corrective action**: add "is the staging environment healthy" as a standing standup check-in item,
and escalate infrastructure issues within four working hours of discovery instead of waiting for them
to visibly block a specific story.
