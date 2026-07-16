---
title: "Artifact: Skimmable Design Note — Shipment-Delayed Notification Type"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 43
---

> `shipment_delayed` notification-type proposal -- passes the thirty-second skim test -- exercises
> co-03.

Raw document text, as the author would ship it:

```markdown
## Proposal: add a `shipment_delayed` notification type

**Decision: add a new notification type, `shipment_delayed`, sent once a shipment's ETA slips more
than 24 hours past its original estimate.**

### Why now

Customer support tickets tagged "where is my order" have grown 30% quarter over quarter, and manual
review shows the majority come from shipments with a stale ETA the customer had no visibility into.

### What changes

The Notification Worker gains one new event type and one new template; the Shipment API emits the
event when ETA recalculation detects a 24-hour-plus slip.

**Next action: Notification Worker owner (Priya) reviews the template copy by Friday.**
```
