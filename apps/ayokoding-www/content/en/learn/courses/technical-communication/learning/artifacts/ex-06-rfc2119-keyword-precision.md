---
title: "Artifact: RFC 2119 Contract — Shipment Event Schema"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 46
---

> Shipment Event Schema contract, rewritten with RFC 2119 keywords -- exercises co-13.

Every event MUST carry a globally unique `event_id`. Consumers MUST implement idempotent processing
keyed on `event_id`, because the underlying queue provides at-least-once delivery, not
exactly-once. Consumers MUST NOT assume the payload's field list is closed -- new optional fields MAY
be added in the future, and a conformant consumer SHOULD ignore fields it does not recognize rather
than rejecting the event.
