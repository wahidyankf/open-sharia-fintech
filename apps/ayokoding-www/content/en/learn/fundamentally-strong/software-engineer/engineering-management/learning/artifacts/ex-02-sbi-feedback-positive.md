---
title: "Artifact: SBI Feedback, Positive — Jordan's Incident Catch"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 42
---

> Reinforcing SBI feedback for a senior engineer's incident-response catch -- exercises co-03.
> Everline and every name here are fictional; every quote is an illustrative, constructed example.

**Situation**: During Tuesday's deploy of the new currency-conversion service, you noticed the
staging smoke test's output looked one decimal place off, even though the test itself passed.

**Behavior**: You paused the rollout, traced the discrepancy to a silent floating-point rounding
difference between the staging and production currency tables, and wrote a fix plus a regression
test before resuming the deploy -- about 40 minutes added to the rollout.

**Impact**: That 40 minutes prevented a currency-rounding bug from reaching every customer invoice
generated that week -- the kind of bug that's expensive and embarrassing to unwind after the fact,
and nearly invisible if it ships quietly.
