---
title: "Artifact: Delegation Context Brief — Lookup-Table Caching"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 47
---

> A delegation brief handing off a decision with the what and why, but not the how -- exercises
> co-08. Everline and every name here are fictional; every quote and number is an illustrative,
> constructed example.

**Delegation brief -- lookup-table caching, owner: Jordan**

**What**: the lookup table gets read on every ingested event and is currently a database round trip
each time; we need this to stop being the ingestion path's slowest step.

**Why**: the event-ingestion service's p95 latency budget is 150ms end to end, and the lookup query
alone currently averages 80ms under peak load -- that's over half the budget on one step. The lookup
table itself changes rarely (a few times a day at most).

**Constraints that matter**: whatever you choose has to tolerate the lookup table changing without
ingestion serving stale data for more than a few minutes, and it can't add a new infrastructure
dependency the team doesn't already operate (no new cache cluster to run on-call for).

**Not specified on purpose**: whether that's an in-process cache with a TTL, a write-through cache
keyed on table version, or something else -- that choice is yours; bring it to Thursday's 1:1 if you
want a second opinion before committing.
