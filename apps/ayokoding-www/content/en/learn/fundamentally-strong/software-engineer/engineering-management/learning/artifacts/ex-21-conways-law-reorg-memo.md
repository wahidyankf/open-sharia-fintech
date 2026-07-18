---
title: "Artifact: Conway's Law Reorg Memo — Ingestion/Serving Split"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 61
---

> A team-topology change proposal that predicts the resulting system-boundary shift -- exercises
> co-18. Everline and every name here are fictional; every detail is an illustrative, constructed
> example.

**Proposed split**: an "Ingestion" sub-team (owns event intake, validation, the streaming pipeline)
and a "Serving" sub-team (owns the query API and dashboard-facing data layer that consumes what
Ingestion produces).

**Conway's Law prediction**: per Conway's Law, the two teams' communication structure -- a hand-off
between two separate teams instead of one team owning the whole pipeline -- will produce a
correspondingly formal boundary in the system itself. Specifically, I predict the currently
informal, frequently-changed internal event format between ingestion and the query layer will
harden into a versioned, contract-tested API within two quarters, because two separate teams can no
longer coordinate an informal shared-format change with a same-day Slack message the way one team
could.

**Explicit acceptance of that trade-off**: this is a deliberate cost, not an accident -- a versioned
contract between the two layers is exactly the schema-registry discipline the team's technical
strategy already pushes toward, so the reorg accelerates a boundary the team wanted anyway.
