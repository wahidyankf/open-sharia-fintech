---
title: "Artifact: Prioritization Decision Record — Platform Team Q2"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 50
---

> A team prioritization/trade-off decision record for competing demands -- exercises co-10, co-14.
> Everline and every name here are fictional; every quote and number is an illustrative,
> constructed example.

**Options considered**: (1) ship the dashboard-alerts feature first, delaying the ETL rewrite and
on-call work; (2) rewrite the fragile ETL script first, delaying the feature by a full quarter;
(3) split effort three ways, delivering all three slowly.

**Trade-off**: option 3 was ruled out first -- splitting a 7-person team three ways on already-tight
capacity means none of the three lands well, and the ETL script's failure mode (silent
data-quality incidents) actively gets worse the longer it's deferred. Between options 1 and 2, the
team chose a modified option 2: rewrite the highest-risk third of the ETL script this quarter (the
part causing 80% of the incidents), and ship a scoped-down version of the dashboard-alerts feature
in parallel with the remaining capacity, deferring the full feature scope to Q3.

**Decision**: partial ETL rewrite (highest-risk portion) plus a scoped dashboard-alerts MVP, this
quarter. On-call load reduction is explicitly deferred to next quarter's prioritization pass.

**Communication plan**: Priya tells product directly (not via a status doc) that the
dashboard-alerts feature ships scoped-down this quarter, full scope Q3, and why (data-quality risk
won out over full feature scope); she tells the team in the next planning meeting, with the
incident-rate reasoning attached so the decision doesn't read as arbitrary.
