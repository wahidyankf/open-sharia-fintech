---
title: "Artifact: Roadmap Trade-off Memo — Multi-Currency Support"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 55
---

> A memo representing engineering cost and risk in a product roadmap negotiation -- exercises
> co-13, co-14. Everline and every name here are fictional; every number is an illustrative,
> constructed example.

**The trade-off being asked of product**: multi-currency support touches the same event-schema
tables the team is mid-migration on. Building it before the migration finishes means either (a)
building it twice -- once against the old schema, once against the new -- or (b) accepting real
data-integrity risk during the transition window while both schemas coexist.

**What we're proposing instead**: finish the schema migration first (3 weeks, already in flight) and
start multi-currency support immediately after, landing 2 weeks later than product's original ask
but built once, against the final schema, with no transition-window risk.

**What product is being asked to accept**: a 2-week slip against the original target date, in
exchange for not paying for the feature twice and not carrying data-integrity risk into the release.
