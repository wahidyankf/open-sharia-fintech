---
title: "PR Description: Notification Worker Idempotency Cache"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 4
---

**What**: adds a Redis-backed idempotency check to `NotificationWorker.send()`, per
[ADR-0006](./adr-0006-notification-worker-idempotency-cache.md). Before sending any customer
notification, the worker now checks whether the event's `event_id` is already present in Redis; if
so, it skips the send and logs `duplicate_suppressed` instead. On a successful send, it writes
`event_id` to Redis with a 48-hour TTL.

**Why**: on 2026-04-02, a deployment restart triggered a Kafka consumer-group rebalance that replayed
already-processed messages, and the worker sent every replay as a fresh notification -- see the
[postmortem](./postmortem.md) and the [RFC](./rfc.md) this PR implements. This change makes that
failure mode structurally safe: a replayed message is now detected and suppressed instead of resulting
in a duplicate customer-facing send.

**How verified**: added a unit test that sends the same event twice and confirms only one outbound
call to NotifyGate; added an integration test that simulates a consumer-group rebalance replay against
a local Kafka instance and confirms zero duplicate sends; ran a replay drill in staging (killed the
consumer mid-batch, forced a rebalance, restarted) and confirmed the `duplicate_suppressed` log line
appears for every replayed message with zero duplicate sends reaching NotifyGate.

**Where to review first**: `notification_worker/idempotency.py`, the `check_and_mark()` function --
this is the one function that decides send-or-skip, and it is the only place in this diff with new
logic. The Redis fail-open behavior (RFC Review Log, Priya's question) lives in this same function:
if Redis is unreachable, `check_and_mark()` returns `send=True` with a logged warning, rather than
blocking the send entirely. Everything else in this diff -- the Redis client wiring in
`notification_worker/config.py`, the two call-site changes in `notification_worker/consumer.py` -- is
mechanical plumbing around this one function.
