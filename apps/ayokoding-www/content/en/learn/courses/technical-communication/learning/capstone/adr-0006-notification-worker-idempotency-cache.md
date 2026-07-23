---
title: "ADR-0006: Idempotency Cache for the Notification Worker"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 3
---

> File path: `services/notification-worker/docs/adr/0006-notification-worker-idempotency-cache.md`
> -- colocated with the Notification Worker's own code (co-08). Continues the numbering already
> established by ADR-0001 (Scenario 9), ADR-0002/0003 (Scenario 10), ADR-0004 (Scenario 11), and
> ADR-0005 (Scenario 24) in the same Harborlight repository. Distills the accepted RFC
> ([`./rfc.md`](./rfc.md)) into a single, durable decision record (co-06, ex-24's pattern).

**Status**: Accepted (2026-04-09)

## Context

On 2026-04-02, a Notification Worker deployment restart triggered a Kafka consumer-group rebalance
that replayed already-processed messages from each partition's last committed offset. The
Notification Worker had no check for whether a given event had already been processed, so every
replayed message produced a second, duplicate SMS or email to the customer. Full incident detail is in
the [postmortem](./postmortem.md); full options analysis is in the [RFC](./rfc.md).

## Decision

The Notification Worker MUST check a Redis-backed idempotency cache, keyed on each event's
`event_id`, before sending any customer notification. If `event_id` is already present in the cache,
the worker MUST skip the send and log a `duplicate_suppressed` event instead. On a successful send,
the worker MUST write `event_id` to the cache with a 48-hour TTL -- comfortably longer than any
plausible consumer-group replay window observed to date.

## Consequences

The Notification Worker gains a dependency on Redis (already run elsewhere in the Harborlight stack
for the Carrier Adapter's rate-limit counters, so this adds load to existing infrastructure rather
than introducing a new piece of infrastructure). A 48-hour TTL bounds the cache's memory footprint
without risking a legitimate re-send being incorrectly suppressed (no shipment event is expected to
replay more than 48 hours after its original processing). This decision does not address the
consumer-group rebalance itself -- Kafka's at-least-once delivery guarantee is expected and unchanged;
this ADR makes duplicate delivery safe to receive rather than attempting to prevent it at the source.

The full deliberation -- both options' pros and cons, the review log, and the TTL discussion -- lives
in the RFC (`./rfc.md`), linked here for historical record but not required reading to understand the
decision itself.
