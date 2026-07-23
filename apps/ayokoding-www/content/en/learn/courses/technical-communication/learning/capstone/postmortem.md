---
title: "Postmortem: Duplicate Shipment Notifications"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 5
---

**TL;DR**: a deployment restart on 2026-04-02 caused the Notification Worker to send duplicate SMS
and email notifications to 340 customers. No shipment data was lost or corrupted; the fix (an
idempotency cache) is designed, decided, and implemented in this topic's [RFC](./rfc.md),
[ADR](./adr-0006-notification-worker-idempotency-cache.md), and [PR](./pr-description.md). This
document is blameless: every entry below describes a system behavior, never an individual's
performance. The system boundary referenced throughout is pictured in the
[C4 context diagram](./context.md).

## Timeline

All times UTC, 2026-04-02.

- **14:02** -- a routine deployment restarts the Notification Worker to roll out an unrelated template
  change.
- **14:02** -- the restart triggers a Kafka consumer-group rebalance; the new consumer instance
  resumes from the last committed offset, which is roughly 90 seconds behind the most recent
  successfully processed message.
- **14:02-14:04** -- the worker reprocesses roughly 340 already-sent shipment events from that 90-second
  window, sending a duplicate SMS or email for each one.
- **14:11** -- the first customer-support ticket referencing a duplicate notification arrives.
- **14:19** -- on-call correlates three similar tickets and confirms a pattern via the Notification
  Worker's send logs.
- **14:24** -- on-call confirms the affected window is closed (the rebalance was a one-time event at
  restart, not an ongoing condition) and no further duplicates are being sent.
- **14:40** -- an all-clear notice is posted to the Shipment Platform channel; incident is downgraded
  to a documentation-and-follow-up item.

## Impact

340 customers received one duplicate SMS or email notification each. No shipment data was lost,
corrupted, or delayed -- the underlying shipment records and their statuses were unaffected; only the
Notification Worker's outbound send behavior duplicated. 6 customers contacted support about the
duplicate; all 6 were informed via a follow-up message that no action was needed on their part.

## Root cause (5 whys)

1. Why did customers receive duplicate notifications? The Notification Worker reprocessed
   already-sent shipment events after a consumer-group rebalance.
2. Why did reprocessing produce duplicate sends? The worker has no check for whether a given event was
   already processed before sending.
3. Why does the worker lack that check? At-least-once delivery (Kafka's own contract, adopted in
   ADR-0005) was accounted for at the infrastructure level but not at the consumer-processing level --
   the worker was written assuming each message arrives once.
4. Why was that assumption never caught before shipping? No test in the Notification Worker's suite
   simulates a consumer-group rebalance replay; the test suite covers message content correctness but
   not delivery-guarantee edge cases.
5. Why does that test gap exist? The migration to Kafka (ADR-0005) added test coverage for the new
   consumer's basic functionality but did not add a dedicated test for at-least-once delivery's
   replay behavior specifically.

**Systemic root cause**: the Notification Worker's test suite has a structural gap -- no test
exercises Kafka's at-least-once delivery guarantee under a consumer-group rebalance -- not any
individual engineer's decision during the Kafka migration.

## Follow-ups

| Follow-up                                                                                                        | Owner | Done-signal                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------- | ----- | ------------------------------------------------------------------------------------------------------------- |
| Ship the idempotency-cache fix (RFC, ADR-0006, PR)                                                               | Bayu  | ADR-0006 accepted, PR merged, and the staging replay drill (described in the PR) shows zero duplicate sends.  |
| Add a dedicated test simulating a consumer-group rebalance replay to the Notification Worker's suite             | Priya | Test merged and passing in CI, covering the exact 90-second-window replay scenario observed in this incident. |
| Add "does this consumer tolerate at-least-once replay" as a required item on the Kafka-consumer launch checklist | Dinar | Checklist item added; confirmed present and checked off on the next Kafka-consuming service this team ships.  |
