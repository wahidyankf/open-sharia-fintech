---
title: "Artifact: Riskiest-Assumption Triage — Kestrel AI Suggestions"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 55
---

> The four big risks triaged for "AI auto-schedule suggestions" -- exercises co-06. Kestrel is a
> fictional product; every quoted number, question, or finding here is an illustrative,
> constructed example, not real data or a real transcript.

- **Value risk**: will managers actually want and trust a suggested schedule enough to act on it?
  Unconfirmed -- interviews so far only established the underlying pain (scheduling takes 40-60
  minutes), not demand for an AI-generated answer to it.
- **Usability risk**: can a manager understand and quickly edit a suggested schedule? Lower
  uncertainty -- Kestrel already has an editable schedule grid; a suggestion just needs to
  pre-populate it.
- **Feasibility risk**: can the team generate a legal, conflict-free, availability-respecting
  schedule automatically? Real but well-understood -- constraint-solving for shift scheduling is a
  known, solvable problem.
- **Business-viability risk**: does this justify its build cost given Kestrel's pricing model?
  Depends entirely on the answer to the value question above.

**Riskiest, chosen first**: value risk -- it's the most uncertain, and every other risk (and the
viability question) is downstream of it.

**Cheapest test**: a concierge (Wizard-of-Oz) pilot with 5 managers -- a human manually builds a
"suggested schedule" each week and presents it as if auto-generated, then tracks how many managers
actually use it versus rebuild from scratch. Costs a few hours a week for 5 managers, no ML
engineering required.
