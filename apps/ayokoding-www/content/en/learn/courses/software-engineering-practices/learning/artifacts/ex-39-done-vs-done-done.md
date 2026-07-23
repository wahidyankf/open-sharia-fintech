---
title: "Artifact: 'Done' vs. 'Done-Done'"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 79
---

> ex-39 &middot; exercises co-21 &middot; two states a Definition of Done must tell apart.

```text
Definition of Done -- v2, split into two explicit states

"Done" (merged):
  - Every Example 38 checklist item checked.
  - PR merged to main.

"Done-done" (merged AND deployed AND monitored):
  - Everything in "Done", PLUS:
  - Deployed to production (not just merged to main).
  - The relevant dashboard/alert (e.g. redemption-error-rate) observed green for at least one
    full business day post-deploy.
  - Feature-flagged changes: flag flipped ON for the intended audience, not just merged disabled.
```

**Verify**: the two states are named explicitly and distinguished by concrete, checkable criteria
(merged vs. deployed-and-observed-green-for-a-day) rather than left as one fuzzy "done" -- satisfying
co-21's rule.

**Key takeaway**: "merged" and "shipped and working" are different facts, and a team that conflates
them under one word "done" loses the ability to ask "wait, is this actually live and healthy yet?"

**Why It Matters**: Example 40's feature-flag pattern makes this distinction unavoidable in
practice -- code can be "done" (merged, tests passing, flag off) for days before it is "done-done"
(flag on, serving real traffic, dashboards confirmed healthy), and a status report that says "done"
for both states misleads whoever is deciding whether the feature actually shipped.
