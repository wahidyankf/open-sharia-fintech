---
title: "Artifact: ADR-0002/0003 — Polling Superseded by Webhooks"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 50
---

> ADR status lifecycle -- an ADR superseded by a new one -- exercises co-07.

**ADR-0002: Poll ParcelLink for Shipment Status Every 5 Minutes** (original)

**Status**: Superseded by ADR-0003

**Context**: (original reasoning: polling was the simplest integration ParcelLink's older API
supported at the time.)

**Decision**: (original: poll every 5 minutes per in-transit shipment.)

**Consequences**: (original consequences, now superseded -- see ADR-0003.)

---

**ADR-0003: Use ParcelLink Webhook Push Notifications for Shipment Status**

**Status**: Accepted (supersedes ADR-0002)

**Context**: polling every in-transit shipment every 5 minutes (ADR-0002) now exceeds ParcelLink's
rate limit during peak shipping days, causing missed status updates exactly when customers check most
often.

**Decision**: subscribe to ParcelLink's webhook push API; a shipment's status updates the moment
ParcelLink has one, with no per-shipment polling.

**Consequences**: requires a publicly reachable webhook endpoint and signature verification on
incoming payloads; removes the rate-limit ceiling ADR-0002 hit.
