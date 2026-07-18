---
title: "Artifact: Pairing vs. Solo -- a Trade-off Memo"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 93
---

> ex-53 &middot; exercises co-20 &middot; two changes, two staffing choices, each justified by
> risk/familiarity.

```text
Change A: the card-balance datastore migration (ADR-0004) -- HIGH risk (touches every redemption
path, hard to reverse once traffic depends on it), UNFAMILIAR (nobody on the team has run a
zero-downtime datastore migration before).
  -> Staffing: PAIR (Amara + Jun). Shared context reduces the chance either engineer's blind spot
     ships unnoticed, and unfamiliarity means neither would move meaningfully faster solo anyway.

Change B: renaming `calc()`'s parameters for clarity (Example 25's refactor commit) -- LOW risk
(single-file, trivially revertible), FAMILIAR (a routine rename, done many times before).
  -> Staffing: SOLO. Neither the shared-context benefit nor the fewer-defects benefit pairing
     offers is worth much here, and pairing two engineers on a rename is a pure throughput loss.
```

**Verify**: each staffing choice cites the specific risk/familiarity property (high-risk +
unfamiliar for pairing; low-risk + familiar for solo) that drove it, not a blanket "pair on
everything" or "pair on nothing" policy, satisfying co-20's rule.

**Key takeaway**: pairing is a targeted response to risk and unfamiliarity, not a universal
staffing default -- applying it to Change B would cost throughput for no matching benefit.

**Why It Matters**: a team that always pairs pays the solo-throughput cost on every trivial change;
a team that never pairs skips the shared-context benefit on exactly the changes (like Change A)
where a solo engineer's blind spot is most expensive -- the memo's job is making that trade-off
visible and deliberate, change by change.
