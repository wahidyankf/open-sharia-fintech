---
title: "Artifact: Reader-Review Rubric Pass — ADR-0005"
date: 2026-07-16T00:00:00+07:00
draft: false
weight: 65
---

> A full reader-review rubric pass against ADR-0005 -- exercises co-01, co-03, and co-15.

**Reader-review rubric -- ADR-0005**

- **Skimmable?** Peer reviewer (Priya) read only the Status and Decision lines and restated: "Kafka,
  accepted, partitioned by shipment ID, 7-day retention." Matches the ADR. Pass.
- **Decision-first?** The Decision section is the second thing on the page, right after Status --
  Priya did not have to read Context first to find it. Pass.
- **Jargon defined?** Priya flagged "consumer group" in Consequences as undefined for a reader outside
  the Shipment Platform team. Fixed: added a three-word parenthetical, "(a set of coordinated Kafka
  readers)."
- **Register-matched?** ADR is written for an engineer audience (the intended reader) -- correctly
  does not attempt an executive framing, since that version already exists separately.

**Result**: 3 of 4 checks passed on first read; the jargon gap was fixed and the ADR re-reviewed, now
passing all four.
