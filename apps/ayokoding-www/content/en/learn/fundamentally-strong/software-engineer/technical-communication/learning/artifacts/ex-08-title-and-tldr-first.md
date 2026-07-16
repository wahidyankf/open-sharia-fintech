---
title: "Artifact: Title + TL;DR — Historical Notification Backfill"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 48
---

> Historical-notification-backfill design note, with title and TL;DR first -- exercises co-01 and
> co-03.

Raw document text, as the author would ship it:

```markdown
# Backfill Historical Shipment Notifications

**TL;DR**: send a one-time, opt-out backfill SMS to the ~1,200 customers affected by last month's
notification-delivery bug, informing them their shipment already arrived. Shipping Thursday, pending
legal's sign-off on the message copy.

## Background

Last month's bug silently dropped the "shipped" notification for a subset of orders placed between
March 3-March 9, before the fix landed. Support tickets since then show these customers had no
visibility into their shipment status until it simply arrived.
```
