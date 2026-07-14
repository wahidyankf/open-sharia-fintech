---
title: "Artifact: Risk Register Over Time"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 64
---

> Aurora Checkout Redesign -- risk register across three sprints -- exercises co-10, co-12.

| Risk                                             | Sprint 1                                | Sprint 2                                                                                                     | Sprint 3                                                                                                   |
| ------------------------------------------------ | --------------------------------------- | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------- |
| Apple Pay API breaking change (score 12)         | Open, mitigation in progress.           | Still open.                                                                                                  | **Retired** -- launch week passed safely; the pinned SDK version held.                                     |
| Load test cannot sustain 3x traffic (score 15)   | Open, mitigation scheduled.             | Downgraded to score 9 (impact 5 -> 3) after an early load-test dry run showed better-than-expected headroom. | Retired -- final load test passed at 3.4x peak traffic.                                                    |
| Bayu on scheduled leave (score 15)               | Open, walkthrough scheduled.            | **Retired** -- the walkthrough and runbook mitigation landed before leave started.                           | (Already retired.)                                                                                         |
| Holiday code-freeze shortens schedule (score 12) | Open.                                   | Still open.                                                                                                  | **Retired** -- the freeze date passed without incident; launch shipped ahead of the freeze window.         |
| Finance requests a 6th provider (score 9)        | Open, routed through change management. | Still open (formal decision pending finalization).                                                           | Retired -- the formal defer-to-Q1 decision closed the open question.                                       |
| Feature-flag rollback bug during 3.3 (new)       | -- not yet identified --                | **New**: discovered during rollout-plan implementation. Score 8 (likelihood 2, impact 4). Owner: Priya.      | Downgraded to score 3 after a partial fix landed; tracked into the Q1 follow-up work alongside Google Pay. |
