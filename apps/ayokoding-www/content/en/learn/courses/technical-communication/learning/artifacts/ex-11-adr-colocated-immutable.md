---
title: "Artifact: ADR-0003 (Colocated, Immutable) — ParcelLink Webhooks"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 51
---

> Colocated, immutable ADR placement -- exercises co-08.

**File path**: `services/shipment-tracker/docs/adr/0003-parcellink-webhook-push.md`

**Frontmatter**: `Date: 2026-02-18` · `Status: Accepted`

The ADR lives inside `services/shipment-tracker/`, the same repository directory as the
`carrier_adapter/` code that implements ParcelLink integration -- not in a company wiki, and not in a
separate documentation repository. A `docs/adr/README.md` index in the same directory lists every ADR
in this service by number.

When the team later needs to add rate-limit backoff to the webhook receiver itself (a related but
distinct decision), that becomes ADR-0004 in the same directory -- ADR-0003's own file is never
reopened for editing after its acceptance date.
