---
title: "Artifact: Incident Timeline — Shipment API Connection-Pool Exhaustion"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 59
---

> Blameless, timestamped incident timeline -- exercises co-10.

**Incident timeline -- Shipment API 500s, 2026-03-11**

- **09:14 UTC** -- automated alert fires: Shipment API error rate exceeds 5% (threshold: 1%).
- **09:16 UTC** -- on-call acknowledges the alert; begins investigation.
- **09:19 UTC** -- `shipment_db` connection-pool metrics show the pool at 100% utilization; requests
  are queueing rather than failing immediately.
- **09:22 UTC** -- mitigation applied: connection-pool size temporarily raised from 20 to 40 via a
  config hot-reload, no deploy required.
- **09:26 UTC** -- error rate returns below 1% threshold; alert clears.
- **09:41 UTC** -- root-cause investigation begins.
