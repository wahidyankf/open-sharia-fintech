---
title: "Artifact: BLUF Status Update — Shipment API Latency"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 41
---

> Shipment API p99 latency spike -- BLUF status update -- exercises co-01.

**Decision needed today: approve raising `shipment_db`'s connection-pool size from 20 to 40.** Root
cause of this morning's p99 latency spike: the pool maxes out during the 09:00-10:00 order-ingestion
burst, so requests queue for a free connection instead of failing fast or running normally. DB query
plan and the ParcelLink carrier lookup are both ruled out -- neither shows any regression.

**Investigation notes** (for reference): checked `EXPLAIN ANALYZE` on the main query first (indexes
in use, no regression); checked ParcelLink's status page for a carrier-side incident (none reported);
found the connection-pool metrics maxing out during the ingestion burst.
