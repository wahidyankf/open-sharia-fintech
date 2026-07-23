---
title: "Artifact: A #NoEstimates Alternative for a Chronically-Wrong Backlog"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 75
---

> ex-35 &middot; exercises co-19 &middot; slicing smaller and counting throughput, instead of
> estimating.

**Problem**: the last six sprints' estimates have missed actual delivery by 40-90% every time,
regardless of who estimated or how carefully.

**#NoEstimates-style proposal** (Woody Zuill's critique -- questions estimate VALUE, not a blanket
ban on ever sizing work):

```text
1. Slice every backlog item until it is small enough to ship in 1-2 days (no story gets an
   estimate -- it either fits the size band or it gets sliced again until it does).
2. Track ACTUAL throughput: how many sliced items shipped last week, the week before, etc.
3. Forecast a release date from throughput (e.g. "we ship ~6 items/week, 40 items left, so ~7
   weeks"), the same way a manufacturing line forecasts from a measured cycle time -- not from
   summed estimates.
```

**Verify**: the proposal removes the per-item estimate step entirely (step 1 explicitly has "no
story gets an estimate") while still producing a forecast (step 3, from measured throughput) --
satisfying co-19's rule that the alternative keeps the ability to forecast without keeping the
broken estimate step.

**Key takeaway**: forecasting from measured throughput of small, uniformly-sized items sidesteps the
question "how long will THIS take" entirely, answering "how long will everything left take" instead
-- which is usually the question that actually mattered.

**Why It Matters**: #NoEstimates is not "never plan" -- it is a specific bet that, for teams whose
estimates are chronically and unpredictably wrong, a measured historical rate forecasts the future
better than another round of guessing does, especially once items are small and uniform enough that
individual guess-error mostly cancels out across many of them.
