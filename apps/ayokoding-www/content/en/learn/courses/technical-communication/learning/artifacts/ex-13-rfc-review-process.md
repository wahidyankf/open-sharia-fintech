---
title: "Artifact: RFC Review Log — Event Bus for Shipment Notifications"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 53
---

> RFC review log, every open question resolved or deferred -- exercises co-05.

**Review log -- RFC: Choosing an Event Bus for Shipment Notifications**

- **Dinar (SRE)**: "Who's on call for Kafka if it goes down at 2am? We don't have Kafka runbooks
  today." → **Resolved**: on-call ownership added to Open Questions (still undecided, explicitly
  tracked, not silently dropped from the review).
- **Priya (Notification Worker owner)**: "Does this change the Notification Worker's consumer code
  much?" → **Resolved**: added a "Migration" section to the RFC describing the consumer-side change as
  a bounded, one-sprint effort.
- **Bayu (tech lead)**: "7-day retention -- have we priced that?" → **Deferred**: retention cost
  estimate tracked as a follow-up ticket, explicitly listed in Open Questions rather than blocking
  acceptance of the core Kafka-vs-SQS decision.

**Status: Accepted** (2026-02-24), with two items carried forward in Open Questions: Kafka
operational ownership, and final retention-period cost.
