---
title: "Prioritization Decision Record: Platform Team Q3"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 3
---

> Everline Platform team -- Q3 prioritization decision record, following Worked Scenario 10's Q2
> record. Everline, Priya Kapoor, and every named engineer below are fictional; every quote and
> number is an illustrative, constructed example, not a real planning document.

## Competing demands this quarter

1. **The Ingestion/Serving reorg** (Worked Scenario 21): splitting the Platform team once it passes
   10 people, with a predicted system-boundary hardening between the two new sub-teams.
2. **The remaining two-thirds of the ETL rewrite** (Worked Scenario 10 covered only the
   highest-risk third in Q2; the rest still causes occasional data-quality incidents, just less
   often).
3. **Cross-team schema-registry contract testing** (Worked Scenario 20's Bet 2, and the shared
   incentive Worked Scenario 18 already established with Morgan's Data Science team).

## Options considered

- **Option A**: do the reorg first, then contract testing, then the rest of the ETL rewrite,
  sequentially.
- **Option B**: do contract testing first (before the reorg), then the reorg, then the ETL rewrite.
- **Option C**: run the ETL rewrite and contract testing in parallel this quarter, deferring the
  reorg to Q4.

## Trade-off

Option C was ruled out first: deferring the reorg doesn't remove the team-size pressure driving it,
and every quarter of delay means more work lands on the current, already-strained team shape before
the split happens. Between A and B, the deciding factor is Worked Scenario 21's own prediction: the
reorg will harden the Ingestion/Serving boundary either around a versioned, contract-tested format
or around whatever informal format happens to exist the day the split takes effect. Doing the reorg
before contract testing is in place risks hardening the boundary around the wrong thing --
permanently, since undoing a hardened boundary is far more expensive than establishing it correctly
the first time.

## Decision

**Option B**: contract testing first, then the reorg, then the remaining ETL rewrite. The ETL
rewrite absorbs the quarter's schedule risk -- it's the item with the most flexible timeline, since
its incident rate, while nonzero, is already down from Q2's highest-risk-third fix.

## Communication plan

- **To the Platform team**: presented in the next planning meeting with Worked Scenario 21's
  Conway's Law prediction attached, so the sequencing (contract testing before reorg) reads as
  deliberate, not arbitrary.
- **To product**: Priya tells product directly that the ETL rewrite's completion may slip later
  into Q3 than originally hoped, with the reasoning (reorg-boundary risk took priority) attached --
  the same trade-off-communication standard as Worked Scenario 15.
- **Cross-team influence component, to Morgan (Data Science team lead)**: contract testing needs
  Data Science's participation to be effective, and Morgan doesn't report to Priya. The ask is
  framed around the same shared incentive Worked Scenario 18 already established -- Data Science
  was paged twice last quarter for exactly the failure mode contract testing prevents -- rather than
  asking Morgan to prioritize Platform's roadmap over Data Science's own.

## Verify

The record states the options considered, the trade-off made, the decision, and the communication
plan (satisfying co-10 and co-14), and the cross-team component names a shared incentive Morgan's
team already holds rather than an appeal to authority or urgency (satisfying co-17).
