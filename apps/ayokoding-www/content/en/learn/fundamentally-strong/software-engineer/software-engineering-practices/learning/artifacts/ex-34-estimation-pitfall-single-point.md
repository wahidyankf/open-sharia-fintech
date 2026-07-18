---
title: "Artifact: An Hour Estimate vs. a Relative Estimate"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 74
---

> ex-34 &middot; exercises co-19 &middot; the same task, estimated two ways.

**Task**: "add multi-currency support to the gift-card redemption flow."

**Estimate 1 -- raw hours**: "14 hours."

**Estimate 2 -- relative, against a reference story**: "about the same size as
`add-partial-redemption` (a completed story, 5 points), maybe slightly larger because of the
currency-conversion-rate dependency -- call it 8 points."

**Verify**: the raw-hour estimate ("14 hours") implies a precision the team has no actual basis for
-- multi-currency work has never been done in this codebase before, so there is no historical data
to calibrate 14 hours against. The relative estimate anchors against a REAL, completed, comparably-
sized story, making its uncertainty visible (points, not hours) instead of hidden behind a false-
precise number.

**Key takeaway**: "14 hours" and "8 points, roughly like that other story" convey very different
amounts of actual confidence, even though both are single numbers -- one pretends to a precision
that does not exist, the other is honest about the comparison it is actually built on.

**Why It Matters**: a raw-hour estimate for genuinely novel work (no prior story to calibrate
against) gets treated as a commitment by everyone downstream (a sales date, a dependent team's own
plan) even though it was never more than a guess -- relative estimation against a known reference at
least makes the guess's basis visible and checkable.
