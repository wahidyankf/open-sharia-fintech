---
title: "Artifact: PR Description — Carrier Adapter Retry-with-Backoff"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 44
---

> Retry-with-backoff PR description -- what/why/how-verified/where-to-look -- exercises co-09.

**What**: adds exponential backoff (3 retries, 200ms/400ms/800ms) to `CarrierAdapter.get_status()`,
the function that calls ParcelLink's `/tracking` endpoint.

**Why**: ParcelLink's API returns transient 503s under their own load spikes (roughly 2% of calls
during their peak hours, per their own status page's historical incident log). Today those 503s
propagate straight to the customer-facing shipment-status page as an error; a short retry absorbs
almost all of them.

**How verified**: added a test that mocks ParcelLink returning two 503s then a 200, confirming the
adapter retries and eventually returns the successful result; ran the existing adapter test suite
unchanged (all passing).

**Where to look first**: `carrier_adapter/retry.py`, the backoff-and-retry loop itself -- everything
else in the diff is unchanged call sites threading the new `retries=3` parameter through.
