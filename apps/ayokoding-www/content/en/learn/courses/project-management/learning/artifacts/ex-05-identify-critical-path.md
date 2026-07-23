---
title: "Artifact: Critical Path — Checkout Redesign"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 45
---

> Aurora Checkout Redesign -- critical path -- exercises co-04.

| Path                                           | Sum (days)         |
| ---------------------------------------------- | ------------------ |
| **2.1 -> 2.2 -> 3.1 -> 3.2 -> 3.3 (critical)** | 4+3+5+3+2 = **17** |
| 1.1 -> 3.1 -> 3.2 -> 3.3                       | 3+5+3+2 = 13       |
| 1.2 -> 3.1 -> 3.2 -> 3.3                       | 3+5+3+2 = 13       |
| 1.3 -> 3.1 -> 3.2 -> 3.3                       | 2+5+3+2 = 12       |
| 2.1 -> 2.2 -> 2.3                              | 4+3+2 = 9          |

**Critical path**: 2.1 Cart persistence rework -> 2.2 Order summary UI -> 3.1 E2E test suite -> 3.2
Load test -> 3.3 Feature-flag rollout, **17 working days, zero slack**. Every other path carries
slack relative to this one; delaying any task on the critical path by one day delays the project by
one day.
