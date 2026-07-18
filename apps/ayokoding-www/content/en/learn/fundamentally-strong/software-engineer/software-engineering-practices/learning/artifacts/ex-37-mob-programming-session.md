---
title: "Artifact: A Mob/Ensemble Programming Session Log"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 77
---

> ex-37 &middot; exercises co-20 &middot; one hard problem, one shared keyboard, a full rotation.

```text
Session: design the card-balance migration strategy (PostgreSQL -> document store, zero downtime)
Participants: Amara, Jun, Priya, Sam (4 engineers, one shared keyboard/screen)
Rule: "driver" rotates every 10 minutes; everyone else is navigator; the WHOLE mob decides direction

00:00  Priya (Driver) sketches the dual-write approach on the shared screen; the mob debates
       read-path consistency during the migration window.
00:10  SWAP -- Sam now Driver, drafts the cutover runbook while the mob catches a missed rollback
       step (what happens if the document store write succeeds but PostgreSQL's fails).
00:20  SWAP -- Jun now Driver, writes the reconciliation script the mob just agreed the runbook
       needs.
00:30  SWAP -- Amara now Driver, the mob reviews the whole plan together, end to end.
00:40  Session ends. Every one of the four can independently explain why dual-write (not a
       big-bang cutover) was chosen, and why the reconciliation script exists.
```

**Verify**: the closing line confirms every participant, not only the person who happened to be
typing at each moment, can explain the final solution -- satisfying co-20's rule that mobbing spreads
understanding across the whole team, not just the keyboard-holder.

**Key takeaway**: the rotating driver role is a mechanism for keeping the WHOLE team's understanding
current, not a mechanism for producing code faster than one person typing alone would.

**Why It Matters**: a zero-downtime migration strategy designed by one person and reviewed
asynchronously by three others routinely misses an edge case exactly like the rollback step Sam's
mob caught live, at design time, because four people actively navigating the same problem
simultaneously surface objections a sequential review pass tends to miss.
