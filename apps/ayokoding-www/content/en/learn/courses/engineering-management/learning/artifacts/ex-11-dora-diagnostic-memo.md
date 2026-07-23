---
title: "Artifact: DORA Diagnostic Memo — Platform Team Quarterly Numbers"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 51
---

> A DORA-metrics-based diagnostic memo naming where to invest next -- exercises co-11. Everline and
> every name here are fictional; every number is an illustrative, constructed example.

**This quarter's numbers**: deployment frequency -- 3 deploys/week (healthy for this team's size);
change-failure rate -- 8% (healthy, below the team's own 10% target); failed-deployment recovery
time -- 40 minutes (healthy); lead time for changes -- 6 days from first commit to production (the
outlier -- every other metric is solid).

**Diagnosis**: the team isn't shipping recklessly (change-failure rate is fine) and isn't slow to
recover when something does break (recovery time is fine) -- the bottleneck is specifically how long
a change sits before it ships at all. Looking at where the 6 days actually goes: roughly 4 of them
are PR review turnaround, not implementation time.

**Recommendation**: invest in review turnaround specifically -- a same-day review SLA and
designating two rotating "review-first" engineers per week -- not a generic "let's move faster" push
on implementation speed, which isn't where the time is actually going.
