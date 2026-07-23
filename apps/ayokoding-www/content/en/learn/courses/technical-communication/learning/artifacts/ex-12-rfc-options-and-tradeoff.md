---
title: "Artifact: RFC — Event Bus for Shipment Notifications"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 52
---

> RFC with options and a decisive trade-off, event bus selection -- exercises co-04.

**RFC: Choosing an Event Bus for Shipment Notifications**

**Problem**: the current in-process queue between Shipment API and Notification Worker has no replay
capability -- a Notification Worker bug that drops messages cannot be recovered from without
re-triggering the original events, and there is no ordering guarantee per shipment.

**Option A: Kafka.** Pros: message replay from any offset, per-partition ordering (partitioned by
`shipment_id`), horizontal scale proven at far larger volume than Harborlight needs today. Cons: the
team has no existing Kafka operational experience; adds a new piece of infrastructure to run and
monitor.

**Option B: Amazon SQS + SNS fanout.** Pros: fully managed, zero new infrastructure to operate, the
team already runs other SQS queues. Cons: no message replay once a message is deleted from the queue;
no native per-key ordering guarantee (SQS FIFO queues offer ordering but cap throughput well below
Harborlight's peak volume).

**Decisive trade-off**: replay capability is the deciding factor -- the Shipment Platform team has now
shipped two Notification Worker bugs in the past year that would have been trivially recoverable with
replay, and both required a manual data-reconciliation effort without it. Kafka's operational cost is
real but bounded (one well-documented technology to learn); SQS's missing replay is a recurring cost
paid every time a future bug ships.

**Decision**: Kafka.

**Open Questions**: who owns Kafka cluster operations day to day (undecided -- SRE and Shipment
Platform are still discussing); retention period for replay (undecided -- proposal is 7 days, pending
a cost estimate).
