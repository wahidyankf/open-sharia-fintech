---
title: "RFC: Preventing Duplicate Shipment Notifications"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 2
---

**Status**: Accepted (2026-04-08)

## Problem

On 2026-04-02, a Notification Worker deployment restart triggered a Kafka consumer-group rebalance
that replayed already-processed messages. The worker has no way to tell a replayed message apart from
a new one, so every replay produced a duplicate customer-facing SMS or email. Full impact and timeline
are in the [postmortem](./postmortem.md). This RFC's job: decide the permanent fix.

## Context

The Notification Worker consumes shipment events from Kafka (ADR-0005, learning track) under an
at-least-once delivery guarantee -- Kafka's own contract, not a bug, and not something this RFC
proposes to change. "At-least-once" MUST be assumed by any consumer of this event bus; the gap is that
the Notification Worker's own processing logic was not built to tolerate it.

## Option A: Redis-backed idempotency cache

Check a cache keyed on each event's `event_id` before sending; skip sending if the key is already
present; write the key with a TTL after a successful send.

**Pros**: ships in roughly one sprint; reuses Redis infrastructure the Carrier Adapter already runs in
production; directly targets the exact failure mode (replay) that caused the 2026-04-02 incident.

**Cons**: adds a synchronous Redis round-trip to the send path (measured p99 impact in a load test:
+4ms, well within the Notification Worker's existing latency budget); does not address at-least-once
delivery anywhere else in the system, only at this one consumer.

## Option B: Transactional outbox with exactly-once processing

Rearchitect the Shipment API's write path to use a transactional outbox pattern, paired with
consumer-side offset coordination, so each event is guaranteed to be processed exactly once end to
end.

**Pros**: solves duplicate delivery structurally, for every current and future consumer of the event
bus, not just the Notification Worker.

**Cons**: requires rearchitecting the Shipment API's write path, not just the Notification Worker --
estimated at several sprints of cross-team work; introduces new failure modes of its own (outbox-table
growth, a new coordination protocol to operate and debug) that the team has no existing operational
experience with.

## Decisive trade-off

Time to mitigate versus completeness of the fix. Option B is the more architecturally complete
answer, but its multi-sprint, cross-team scope means the Notification Worker stays exposed to the
exact failure mode that already caused one customer-facing incident for weeks longer than Option A
requires. Option A does not solve duplicate delivery everywhere, but it solves it exactly where the
incident happened, at a fraction of the cost, and does not foreclose adopting Option B later for other
consumers if the pattern recurs elsewhere.

## Decision

Option A: a Redis-backed idempotency cache in the Notification Worker, keyed on `event_id`, with a
48-hour TTL.

## Open Questions

- **TTL value**: proposed 48 hours. **Resolved** during review -- accepted as-is; no replay window
  longer than a few minutes has ever been observed in this system's Kafka consumer-group history.
- **Redis capacity impact**: does the added key volume affect the Carrier Adapter's existing Redis
  usage? **Deferred** -- SRE capacity review scheduled for the sprint after this RFC's acceptance;
  tracked as a follow-up, not blocking the fix itself.

## Review log

- **Dinar (SRE)**: "Does this new Redis load risk the Carrier Adapter's existing rate-limit counters?"
  → **Deferred** to the capacity-review follow-up above; RFC proceeds to acceptance without blocking
  on it, since the measured load estimate is small relative to Redis's current headroom.
- **Priya (Notification Worker owner)**: "What happens if Redis itself is briefly unavailable --
  do we fail open or fail closed?" → **Resolved**: fail open (send the notification, log a
  `idempotency_check_unavailable` warning) rather than fail closed (block all sends) -- a rare,
  briefly duplicated notification is a better outcome than blocking all shipment notifications
  because of an unrelated Redis blip.
- **Bayu (tech lead)**: "Why not just fix the consumer-group rebalance behavior directly instead?" →
  **Resolved**: rebalance-triggered replay is expected, standard Kafka consumer-group behavior, not a
  bug to "fix" -- see Context above. The correct fix is making the consumer tolerant of it, which is
  exactly what this RFC proposes.

**Status: Accepted** (2026-04-08), with one item carried forward in Open Questions: the Redis
capacity-impact review.
