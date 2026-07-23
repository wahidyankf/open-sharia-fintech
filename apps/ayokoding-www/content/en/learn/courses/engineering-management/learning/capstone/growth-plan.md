---
title: "Growth Plan: Noor Rahman"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 2
---

> Everline Platform team -- growth plan for Noor Rahman, six months after joining (Worked Scenario 1
> introduced Noor's first 1:1). Everline, Priya Kapoor, and Noor Rahman are fictional; every quote,
> score, and evaluation below is an illustrative, constructed example written to teach this topic's
> techniques, not a real performance record.

## Feedback frame (SBI)

**Situation**: over the last two months, Noor has owned the alert-batching change end to end --
from the original design note through implementation, review, and rollout.

**Behavior**: Noor proposed the batching-window approach in writing before coding it, incorporated
Jordan's review feedback on a race-condition edge case without needing it re-explained twice, and
wrote a rollback plan into the rollout PR without being asked to.

**Impact**: the change shipped with zero incidents, and the rollback plan meant the on-call
engineer that week (Dana) knew exactly what to do if something had gone wrong, without paging Noor.

## Strengths (keep doing)

- Writes a design note before coding on anything beyond a small fix -- already a habit, not
  something Priya has to prompt.
- Incorporates review feedback precisely the first time, without needing points re-explained.
- Thinks about the failure path (the rollback plan) without being asked -- most engineers at Noor's
  current level only think about the happy path unprompted.

## Gaps mapped to next-level behaviors

- **Gap**: Noor's design notes are strong on approach but rarely name more than one alternative
  considered -- the trade-off section usually reads as "here's what I'll do," not "here's what I
  considered and why I picked this." **Next-level behavior** (per the Senior Engineer ladder rung):
  "proposes a design approach for a multi-day task before writing code, and can defend a trade-off
  in it" -- Noor meets the "proposes before coding" half consistently; the "defend a trade-off"
  half needs at least one named alternative and a stated reason it lost.
- **Gap**: Noor has not yet reviewed another engineer's PR unprompted -- all review activity so far
  has been receiving feedback, not giving it. **Next-level behavior**: "reviews at least 2-3 PRs a
  week beyond assigned ones, catching design issues, not just style" -- this is the one rung gap
  furthest from being met.

## Next steps

- For the next design note (the on-call-noise-reduction work under Worked Scenario 20's Bet 3),
  Noor writes at least one explicitly rejected alternative and states why it lost, before bringing
  it to review.
- Starting next sprint, Noor reviews at least one PR a week outside her own assigned work,
  practicing the specific next-level behavior named above -- starting with Alex's PRs, since Alex
  (per Worked Scenario 23) is also building judgment and a peer review adds a second perspective
  beyond Priya's.

## Verify

Every gap above maps to an observable behavior quoted from the Senior Engineer ladder rung, not a
vague trait -- and the feedback frame names a specific situation, an observed behavior, and a stated
impact, satisfying co-03, co-05, and co-06's rule.
