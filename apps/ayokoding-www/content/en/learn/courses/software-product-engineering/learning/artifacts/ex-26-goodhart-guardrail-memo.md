---
title: "Artifact: Goodhart Guardrail Memo — Kestrel Shifts-Created Metric"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 66
---

> A memo diagnosing a gamed "shifts created" metric and proposing a countermeasure -- exercises
> co-22. Kestrel is a fictional product; every quoted number, question, or finding here is an
> illustrative, constructed example, not real data or a real transcript.

**What happened**: support agents, evaluated in part on "shifts created per week" across the
accounts they onboard, started proactively creating draft placeholder shifts on new customers'
behalf during onboarding calls -- framed internally as "helping them get started." The metric
climbed. The actual activation signal (a manager publishing their own complete first schedule) did
not move at all during the same period.

**Gaming path named**: "shifts created" counted _any_ shift row inserted into the system,
regardless of who created it or whether it was ever published -- support staff optimizing for
their own eval metric found a legitimate-looking action (helping a customer) that inflated the
number without producing the underlying outcome (a customer actually running their own scheduling)
the metric was meant to represent.

**Countermeasure**: redefine the support team's metric to count only shifts that are (a)
published, not drafts, and (b) created by the customer's own user account, not a support agent's
internal tooling account. Pair this redefined metric with the existing activation-rate guardrail --
if "customer-published shifts" ever rises without activation rate also rising, that is itself now
a signal worth re-investigating.
