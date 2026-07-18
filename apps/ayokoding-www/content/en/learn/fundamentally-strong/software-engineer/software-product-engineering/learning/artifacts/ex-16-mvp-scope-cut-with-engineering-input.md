---
title: "Artifact: MVP Scope Cut — Kestrel Smart Scheduling Suite"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 56
---

> A 12-feature idea cut to an MVP, with a cheaper engineer-proposed alternative -- exercises
> co-12, co-06, co-26. Kestrel is a fictional product; every quoted number, question, or finding
> here is an illustrative, constructed example, not real data or a real transcript.

**Original 12-feature scope**: full ML-based constraint solver, historical-pattern learning,
multi-location optimization, staff-preference weighting, real-time re-optimization on
cancellations, and seven more sub-features.

**MVP, testing the riskiest assumption (value risk, now at real-usage scale, not a 5-manager
pilot)**: a single-location, rule-based "suggested schedule" that pre-fills the existing editable
grid using availability + max-hours constraints only, badged "Suggested" in the UI so managers know
it's a recommendation they can freely override.

**Engineer's cheaper, ~80%-value alternative**: instead of a full ML pipeline (an estimated 6
engineering-weeks), build a simple greedy constraint-satisfaction scheduler (an estimated 1
engineering-week) that respects the same availability and max-hours rules. It won't learn from
history or optimize across locations, but it captures most of the concierge pilot's demonstrated
value -- a pre-filled, editable starting point instead of a blank grid -- at roughly a sixth of the
cost.
