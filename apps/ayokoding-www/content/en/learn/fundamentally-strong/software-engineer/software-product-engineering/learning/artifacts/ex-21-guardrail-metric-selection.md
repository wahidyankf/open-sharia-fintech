---
title: "Artifact: Guardrail Metric Selection — Kestrel Checkout Speed"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 61
---

> Guardrails chosen for a checkout-speed experiment -- exercises co-15. Kestrel is a fictional
> product; every quoted number, question, or finding here is an illustrative, constructed example,
> not real data or a real transcript.

**Primary metric (OEC)**: checkout completion rate (% of teams that start the upgrade flow and
finish it).

**Guardrail 1 -- payment-failure rate**: must not increase. A faster flow that rushes people past
the payment-details step could increase mistyped card numbers or expiry dates, a cost the primary
conversion metric alone wouldn't reveal (a failed payment still counts as "started checkout").

**Guardrail 2 -- 48-hour refund-request rate**: must not increase. A too-frictionless checkout
risks buyer's-remorse upgrades -- a team that upgraded almost accidentally, without fully
registering the commitment, showing up a day or two later asking to downgrade.
