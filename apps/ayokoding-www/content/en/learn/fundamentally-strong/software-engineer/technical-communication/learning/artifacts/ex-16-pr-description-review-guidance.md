---
title: "Artifact: PR Description — Migrate Notification Worker to Kafka"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 56
---

> PR description with explicit review guidance for a large diff -- exercises co-09.

**What**: migrates `NotificationWorker` from the legacy in-process queue consumer to a Kafka consumer,
per ADR-0005.

**Why**: enables message replay after worker bugs instead of manual data reconciliation.

**How verified**: full existing Notification Worker test suite passes against a local Kafka instance;
ran a replay drill in staging (killed the consumer mid-batch, restarted, confirmed every message the
old queue would have delivered is still delivered, in order, under the new Kafka consumer).

**Where to review first**: `notification_worker/consumer.py`'s `handle_rebalance()` method --
everything else in this diff (import changes, config wiring, thirteen other files) is mechanical.
`handle_rebalance()` is the one place a consumer-group rebalance could replay already-processed
messages if the offset-commit logic has a bug; get this one function right and the rest of the diff
is low-risk by comparison.
