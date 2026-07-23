---
title: "Artifact: Design Doc Open Questions — Shipment ETA Recalculation"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 54
---

> ETA-recalculation design doc, decided and undecided items kept explicitly separate -- exercises
> co-04.

**Decision**: recalculation runs synchronously on every shipment status update -- not on a schedule --
because ETA staleness between updates is the exact problem this doc exists to fix.

**Open Questions**:

- What's the fallback if ParcelLink's own ETA field is missing for a shipment? (undecided -- proposal:
  fall back to a static origin-to-destination average, but this needs the data team's input on whether
  that average is even tracked today.)
