---
title: "Artifact: Sprint 2 Retrospective — Tracked Actions"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 63
---

> Aurora Checkout Redesign -- retrospective actions -- exercises co-12.

| #   | Raw observation                                                     | Tracked action                                                                                                             | Owner | Done-signal                                                                                                                |
| --- | ------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- | ----- | -------------------------------------------------------------------------------------------------------------------------- |
| 1   | Nobody noticed the staging outage for a day.                        | Add a staging-environment health check as a standing standup item.                                                         | Priya | Appears as a standing standup line item, confirmed present for two consecutive sprints.                                    |
| 2   | The deploy pipeline broke twice.                                    | Add an automated smoke test as the first stage of the deploy pipeline, so breakage is caught before reaching later stages. | Bayu  | The pipeline dashboard shows the new smoke-test stage green on the next three consecutive deploys.                         |
| 3   | Pairing on the cart-persistence code helped a lot.                  | Continue pairing specifically for any story touching legacy cart-persistence code (not team-wide pairing).                 | PM    | The next legacy-touching backlog story is explicitly paired, confirmed on the sprint board.                                |
| 4   | Planning poker took too long because half the team wasn't prepared. | Send a standing "read these stories before the session" note the day before every planning-poker session.                  | PM    | The next session finishes in 30 minutes or less for a similarly sized slice (baseline: the prior session took 55 minutes). |
