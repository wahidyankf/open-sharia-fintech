---
title: "Artifact: ADR-0005 — Kafka for the Shipment Event Bus"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 64
---

> Accepted RFC distilled into a durable ADR -- exercises co-04 and co-06.

**ADR-0005: Use Kafka for the Shipment Event Bus**

**Status**: Accepted

**Context**: the prior in-process queue between Shipment API and Notification Worker had no replay
capability, which caused two Notification Worker bugs to require manual data reconciliation instead
of a replay.

**Decision**: Kafka is the shipment event bus, partitioned by `shipment_id` for per-shipment
ordering, with 7-day message retention for replay.

**Consequences**: SRE owns Kafka cluster operations (on-call runbook: `docs/runbooks/kafka.md`);
Notification Worker consumes via a Kafka consumer group (see ADR-0003's webhook decision for the
upstream carrier-status side of this same event bus).

_(Full deliberation -- both options' pros/cons, the review log, and the retention-cost discussion --
lives in the RFC, `docs/rfcs/2026-02-event-bus.md`, linked here for historical record but not required
reading to understand the decision itself.)_
