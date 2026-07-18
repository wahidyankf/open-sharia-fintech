---
title: "Artifact: Manager-vs-Maker Catch — Priya's Bad Week"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 49
---

> A diagnosis of a week where a manager coded on the critical path and missed two 1:1s -- exercises
> co-20, co-01. Everline and every name here are fictional; every quote is an illustrative,
> constructed example.

**What happened**: a production data-quality incident hit Thursday morning. Instead of assigning it
and coaching from the side, I opened the code myself and fixed it directly -- it was faster in the
moment, and I was the person who knew the ingestion pipeline best. I then spent Friday finishing the
fix's test coverage myself instead of handing it off, and cancelled both Thursday and Friday 1:1s to
do it.

**The bottleneck this created**: nobody else on the team got closer to being able to handle the next
pipeline incident alone -- I was, again, the single person who could diagnose and fix this class of
bug fastest, which is exactly the bottleneck my promotion was supposed to remove. Two reports also
went a full extra week without their 1:1, right when one of them needed a follow-up on a feedback
conversation.

**Corrective habit change**: for the next production incident, I pair with whoever's closest to
ready on that part of the system and narrate my diagnosis out loud instead of silently fixing it --
slower during the incident itself, but it's the only path that makes the team less dependent on me
being available next time. 1:1s move only if the report agrees, never unilaterally.
