---
title: "Artifact: Postmortem — Shipment API Connection-Pool Exhaustion"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 60
---

> Full postmortem: impact, systemic root cause, owned follow-ups -- exercises co-10.

**Impact**: 5% of Shipment API requests returned 500 for 12 minutes (09:14-09:26 UTC); no data loss;
affected customers who retried succeeded on the retry (Shipment API is idempotent for read
endpoints).

**Root cause (5 whys)**:

1. Why did requests 500? The connection pool was exhausted, so new requests timed out waiting for a
   connection.
2. Why was the pool exhausted? A Wednesday-morning order-ingestion burst (a known weekly pattern)
   combined with read traffic from a new dashboard feature launched the day before.
3. Why didn't the pool size account for the new dashboard's added read load? The dashboard's launch
   checklist did not include a connection-pool capacity review.
4. Why doesn't the launch checklist include that review? No launch checklist item currently exists
   for "new feature adds sustained read load to a shared connection pool."
5. Why does this gap exist? The checklist was written when Shipment API had one traffic source
   (mobile app); it was never revisited as more traffic sources were added.

**Systemic root cause**: the launch checklist has a structural gap -- no step verifies a new feature's
added load against shared-resource capacity -- not any individual engineer's oversight in shipping
the dashboard.

**Follow-ups**:

| Follow-up                                                                        | Owner | Done-signal                                                                   |
| -------------------------------------------------------------------------------- | ----- | ----------------------------------------------------------------------------- |
| Add "shared-resource capacity review" as a required launch checklist item        | Bayu  | Checklist template updated; confirmed present in the next 2 feature launches. |
| Add automated alerting on connection-pool utilization at 80% (before exhaustion) | Priya | Alert fires in a staging load test at 80% utilization within one sprint.      |
| Move `shipment_db` to a read-replica architecture                                | Dinar | Replicas live in production; dashboard reads routed to them.                  |
