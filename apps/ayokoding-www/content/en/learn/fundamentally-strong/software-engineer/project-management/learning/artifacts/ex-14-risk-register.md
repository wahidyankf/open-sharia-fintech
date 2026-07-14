---
title: "Artifact: Risk Register — Checkout Redesign"
date: 2026-07-14T00:00:00+07:00
draft: false
weight: 54
---

> Aurora Checkout Redesign -- risk register -- exercises co-10.

| #   | Risk                                                                                                      | Likelihood (1-5) | Impact (1-5) | Score | Mitigation                                                                                                                                        | Owner                 |
| --- | --------------------------------------------------------------------------------------------------------- | ---------------- | ------------ | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------- |
| 1   | Apple Pay API introduces a breaking change before launch                                                  | 3                | 4            | 12    | Pin the SDK version, subscribe to Apple's developer changelog, smoke-test weekly against the sandbox.                                             | Dinar (payments lead) |
| 2   | Load test reveals checkout cannot sustain 3x peak traffic                                                 | 3                | 5            | 15    | Run the load test three weeks before launch (not launch week), reserve autoscaling headroom, keep a feature-flag kill switch to the old checkout. | Priya (SRE)           |
| 3   | Bayu, the only engineer who knows the legacy cart-persistence code, is on scheduled leave during Sprint 2 | 5                | 3            | 15    | Pair a full walkthrough session before leave starts, document cart-persistence quirks in a runbook.                                               | Bayu (tech lead)      |
| 4   | Holiday code-freeze policy shortens the usable schedule by one week                                       | 4                | 3            | 12    | Confirm the exact freeze date with release management now, and build the week into the schedule buffer rather than discovering it late.           | Dinar                 |
| 5   | Finance requests a sixth payment provider mid-project (scope creep)                                       | 3                | 3            | 9     | Route any such request through the change-management decision process rather than silently absorbing it.                                          | PM (Aurora)           |
