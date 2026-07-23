---
title: "Artifact: A Postmortem's Root Cause Becomes a Tracked Debt Item"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 90
---

> ex-50 &middot; exercises co-23, co-16 &middot; the follow-up item traces to the exact postmortem
> line that justified it.

**Postmortem excerpt** (INC-0104, blameless, per Example 43's rewrite):

```text
Root cause: the ops-toggle script had no built-in guard against re-applying a change that was
already in effect, and no confirmation step surfaced the flag's current state before running.
```

**Tracked debt item, filed the same day**:

```text
## DEBT-052: ops-toggle scripts lack a pre-run state confirmation guard

Logged: 2026-07-18
Owner: @dev-platform-team
Quadrant: RECKLESS + INADVERTENT (nobody chose to skip this -- it was simply never built)
Source: INC-0104 postmortem, "Root cause" section (quoted above verbatim)

Follow-up: audit every ops-toggle script for the same missing guard; add a confirmation prompt to
each (this incident's own toggle script already fixed same-day; the audit covers the rest).
```

**Verify**: the debt item's `Source` line quotes the postmortem's `Root cause` section verbatim,
directly tracing the follow-up item back to the specific line that justified it, satisfying co-23's
and co-16's combined rule.

**Key takeaway**: a postmortem that ends at "root cause identified" loses its own value the moment
everyone moves on -- the tracked debt item is what carries the finding forward into the backlog
where it can actually get prioritized (Example 29's friction-ranking applies to it too).

**Why It Matters**: without an explicit trace from postmortem to backlog item, a root cause gets
identified, discussed once in a review meeting, and then quietly forgotten -- exactly the kind of
un-actioned finding that lets the same failure mode recur under a different incident number.
