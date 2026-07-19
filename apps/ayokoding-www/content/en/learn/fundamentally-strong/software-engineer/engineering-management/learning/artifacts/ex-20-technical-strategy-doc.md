---
title: "Artifact: Technical Strategy Doc — Everline Platform Team"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 60
---

> A one-page technical strategy tying team bets to product outcomes with explicit trade-offs --
> exercises co-12, co-14. Everline and every name here are fictional; every number is an
> illustrative, constructed example.

**Bet 1 -- migrate the ETL pipeline from batch to streaming.** Ties to: reducing the
dashboard-alerts feature's data latency from ~15 minutes to under 1 minute, which is the specific
gap product has flagged as blocking a premium-tier alerting offer. **Trade-off**: streaming
infrastructure is more operationally complex than batch, meaning higher on-call learning curve for
at least one quarter while the team builds streaming-specific runbooks.

**Bet 2 -- adopt schema-registry contract testing across every producer/consumer boundary.** Ties
to: cutting cross-team schema-break incidents (2 last month alone) toward zero, protecting both
Platform's and Data Science's on-call load. **Trade-off**: every schema change gets a mandatory
contract-test gate, adding a small amount of friction to changes that used to ship immediately.

**Bet 3 -- reduce on-call noise by tuning alert thresholds and removing alerts with no actionable
runbook.** Ties to: engineer retention -- pager fatigue was the top cited reason in this quarter's
team survey for two people considering leaving the on-call rotation entirely. **Trade-off**: a small
number of real-but-rare issues will surface later (via the next day's dashboard check instead of a
page) rather than immediately.

**Explicitly not this year**: a full rewrite of the ingestion service in a different language --
real cost, no stated product outcome justifies it right now.
