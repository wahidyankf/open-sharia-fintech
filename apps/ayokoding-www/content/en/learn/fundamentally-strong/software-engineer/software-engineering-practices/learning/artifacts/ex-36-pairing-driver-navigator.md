---
title: "Artifact: A Pairing Session Log -- Driver/Navigator, Timed Swap"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 76
---

> ex-36 &middot; exercises co-20 &middot; explicit roles, a timed switch, and both partners able to
> explain the diff.

```text
Session: implement compare_and_swap() for balance_store.py
Participants: Amara (starts as Driver), Jun (starts as Navigator)
Rule: swap roles every 15 minutes, timer-enforced

00:00  Amara (Driver) types the function signature; Jun (Navigator) reads the ADR aloud, flags the
       eventual-consistency edge case the signature needs to handle.
00:15  SWAP -- Jun now Driver, Amara now Navigator.
00:15  Jun implements the retry loop; Amara spots a missing bound on retry count, catches it before
       it's typed.
00:30  SWAP -- Amara now Driver, Jun now Navigator.
00:30  Amara writes the test for the stale-read race condition; Jun questions whether the test
       actually exercises the race or just the happy path -- they rewrite it together.
00:45  Session ends. Both Amara and Jun can independently explain every line of the final diff.
```

**Verify**: the log shows exactly three 15-minute intervals with an explicit role swap at each
boundary, and both participants can explain the resulting diff (the closing line states this
directly) -- satisfying co-20's rule.

**Key takeaway**: the timed swap is what keeps BOTH people actively engaged -- a navigator who never
drives silently checks out, and a driver who never navigates loses the second set of eyes that
catches the retry-count bug above before it ships.

**Why It Matters**: this session caught a missing retry bound and a happy-path-only test DURING
implementation, not in review -- exactly the "shared context, fewer defects" trade pairing makes
for high-risk work (co-20), worth the solo-throughput cost specifically because this code
(concurrent balance writes) is exactly the kind of work where a defect is expensive.
