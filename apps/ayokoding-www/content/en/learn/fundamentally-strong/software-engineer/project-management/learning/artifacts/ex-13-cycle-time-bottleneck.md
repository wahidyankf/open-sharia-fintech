---
title: "Artifact: Cycle-Time Bottleneck Diagnosis"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 53
---

> Helios platform team -- cumulative-flow diagnosis -- exercises co-09, co-08.

| Workflow stage | WIP, week 1 | WIP, week 2 | WIP, week 3 | Trend   |
| -------------- | ----------- | ----------- | ----------- | ------- |
| In Progress    | 4           | 5           | 4           | Flat    |
| Code Review    | 3           | 6           | 9           | Growing |
| Done           | 12          | 13          | 12          | Flat    |

**Bottleneck**: Code Review. A widening WIP band on a cumulative-flow diagram, with the stages on
either side flat, is the signature of a bottleneck at that one stage -- work enters at roughly the
same rate it always has, but leaves more slowly, so items pile up there instead of moving through.

**Recommended fix**: cap Code Review's WIP limit at 3 and add a second reviewer rotation.
