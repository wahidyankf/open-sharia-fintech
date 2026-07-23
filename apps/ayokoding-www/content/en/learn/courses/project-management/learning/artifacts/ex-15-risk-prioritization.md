---
title: "Artifact: Risk Prioritization — Top Three This Sprint"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 55
---

> Aurora Checkout Redesign -- risk prioritization -- exercises co-10.

| Rank | Risk                                                   | Score | Rationale for this rank                                                                                                                                                                                       |
| ---- | ------------------------------------------------------ | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Load test reveals checkout cannot sustain 3x traffic   | 15    | Highest impact (5) of any risk -- a launch-blocking failure discovered late.                                                                                                                                  |
| 2    | Key engineer (Bayu) on scheduled leave during Sprint 2 | 15    | Tied on score; the leave date is fixed and near-term, so its mitigation window is the tightest of any risk on the list.                                                                                       |
| 3    | Apple Pay API breaking change before launch            | 12    | Tied with the code-freeze risk at 12; ranked above it because a third-party API change is outside the team's control entirely, while the freeze date is knowable in advance with one confirming conversation. |

Risks not in the top three (holiday code-freeze, scope-creep) remain on the register with their
existing mitigations assigned, without dedicated attention this sprint.
