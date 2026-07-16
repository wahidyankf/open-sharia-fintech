---
title: "Artifact: Inverted-Pyramid Proposal — Shipment DB Read Replicas"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 42
---

> Read-replica proposal for `shipment_db` -- inverted-pyramid structure -- exercises co-02.

**Proposal: add two Postgres read replicas for `shipment_db`.** Read-heavy endpoints (`GET
/shipments/{id}`, `GET /shipments?customer_id=`) currently compete with order-ingestion writes for
the same connection pool and the same I/O, which is the direct cause of the p99 latency spike
documented in `ex-01-bluf-rewrite.md`. Routing reads to two replicas separates that contention with no
change to write behavior.

**What this costs**: replica lag (typically under 200ms in our load test, Appendix B) means a read
immediately following a write may occasionally see slightly stale data -- acceptable for shipment
status display, not acceptable for the order-confirmation write path, which stays on the primary.

**Appendix A: investigation notes** (a week of connection-pool and query-plan analysis, condensed
from the ex-01 investigation).

**Appendix B: load-test results** (replica lag measured at p50 40ms, p99 190ms under 3x peak read
traffic).
