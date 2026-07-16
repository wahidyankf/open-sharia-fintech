---
title: "Artifact: ADR-0001 — UTC Timestamps for Shipment Events"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 49
---

> One-decision ADR, UTC timestamp storage -- exercises co-06.

**ADR-0001: Store All Shipment Event Timestamps in UTC**

**Status**: Accepted

**Context**: Shipment events originate from warehouses across three US time zones. Storing each
event's timestamp in the warehouse's local time made cross-zone comparisons (e.g., "did this shipment
leave before it arrived") unreliable -- a shipment briefly appeared to arrive before it shipped when
compared across a time-zone boundary.

**Decision**: every shipment event's timestamp is stored and transmitted in UTC. Display-layer code
(customer-facing SMS/email, the Warehouse Ops Portal) converts to local time only at render time,
never before storage.

**Consequences**: all existing event-producing code paths need a one-time audit to confirm they
already emit UTC (two did not, and were fixed as part of this change). Every future producer must
follow the same rule -- documented here so a reviewer can point to this ADR in code review instead of
re-litigating the question.
