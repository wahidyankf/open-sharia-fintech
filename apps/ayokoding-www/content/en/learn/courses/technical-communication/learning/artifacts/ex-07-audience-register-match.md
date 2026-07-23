---
title: "Artifact: Two-Register Update — Notification Duplicate Incident"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 47
---

> Duplicate-notification incident, written for two audiences -- exercises co-15.

**Executive version**: Last quarter, a subset of customers received duplicate shipment notifications
after a routine worker restart. No data was lost and no customer action was required, but it eroded
trust in our SMS/email channel. We are adding a safeguard (an idempotency check) that makes this
class of failure structurally impossible going forward, shipping this sprint, at no added
infrastructure cost.

**Engineer version**: The Notification Worker consumes from an at-least-once queue and processes each
message without checking whether it already ran -- a consumer-group rebalance during a deployment
restart replayed roughly 340 already-processed messages, and every one fired a duplicate SMS/email.
The fix: a Redis-backed idempotency cache keyed on the event's `event_id`, with a 48-hour TTL
comfortably longer than any plausible replay window. See this topic's capstone ADR and RFC for the
full design.
