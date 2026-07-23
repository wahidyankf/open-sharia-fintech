---
title: "Artifact: Build-Measure-Learn Decision — Kestrel Suggested Schedule"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 57
---

> Pivot-or-persevere decision after the greedy-scheduler MVP shipped -- exercises co-13. Kestrel
> is a fictional product; every quoted number, question, or finding here is an illustrative,
> constructed example, not real data or a real transcript.

**Hypothesis**: managers will trust and act on an auto-suggested schedule enough to keep it as a
starting point rather than deleting it and building from scratch.

**Measurement**: 65% of managers who saw a suggested schedule kept it and edited it rather than
discarding it; when separately asked whether they'd pay extra for the feature as a premium
add-on, only 20% said yes.

**Decision**: **persevere** on the suggestion mechanism itself -- 65% real usage confirms managers
do trust and act on it, so it stays and continues to improve. **Pivot** away from the premium-
add-on pricing model that was originally proposed alongside it -- 20% willingness-to-pay is too low
to justify gating it behind an upsell; instead, bundle the suggestion feature into the existing
plan as a retention driver, where its value is capturing managers who'd otherwise churn from
scheduling friction, not a new revenue line.
