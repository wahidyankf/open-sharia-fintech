---
title: "Artifact: Critical-Path Recovery Options — Aurora"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 62
---

> Aurora Checkout Redesign -- critical-path recovery -- exercises co-04, co-01.

Situation: 3.1 (checkout end-to-end test suite), on the critical path, runs three days longer than
planned. The 17-day critical path is now tracking three days late against the fixed November 15 date.

- **Crashing** (spends cost): add a second QA engineer, at contractor day rate, to close out 3.1's
  remaining test cases in parallel. Recovers time by paying for it directly; does not change the risk
  profile of the work itself.
- **Fast-tracking** (spends risk): start 3.2's environment setup and initial load-test ramp in
  parallel with 3.1's final regression pass, instead of strictly waiting for 3.1 to finish first.
  Recovers time by overlapping normally sequential work; accepts the risk that the load test begins
  against a not-yet-fully-validated build.

**Decision**: a blended recovery. Fast-track two of the three needed days (overlap 3.2's setup and
initial ramp with 3.1's tail end); crash the remaining one day (add a second QA engineer for one day
to close out 3.1's last test cases faster). This recovers all three days without moving the fixed
November 15 date or cutting scope.
