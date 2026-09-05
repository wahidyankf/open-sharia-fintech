---
title: "Principles and Conventions Implemented/Respected"
description: "Principles/conventions implemented."
category: explanation
subcategory: development
tags:
  - testing
  - live-testing
  - usability
  - ux
  - quality
  - systematic
created: 2026-06-22
when_to_use: "Use to trace this practice's rationale."
---

# Principles and Conventions Implemented/Respected

## Principles Implemented/Respected

- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Sampling
  is implicit; enumeration is deliberate. Forcing-functions require the tester to observe every
  element on every surface rather than stopping when a representative sample has been checked.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  Each forcing-function states exactly what must be enumerated and what property must be asserted
  for each item. "I tested the controls" is implicit. "I exercised each of the N shared controls
  on each of the M tabs it appears on and asserted consistent behaviour" is explicit.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**:
  Where a systematic check can be automated -- computed-style tuples for visual consistency,
  URL round-trip scripts, declared-invariant scripts -- automation is preferred. Where human
  or agent judgment is required -- jargon scanning, discoverability probing, completeness
  criticism -- the forcing-function names the exact judgment to apply.

## Conventions Implemented/Respected

- **[User-Facing Delivery Hardening Convention](.././user-facing-delivery-hardening.md)**: Rule 15
  of that convention requires the three live-site testers to run a near-end retest before plan
  archival. This document defines what "thorough" means for those runs so the retest is
  systematic, not selective.

- **[Manual Behavioural Verification Convention](.././manual-behavioural-verification.md)**: That
  convention defines _what_ to verify (page renders, interactions, console errors, network
  requests, all locales, all breakpoints). This document defines _how_ to achieve completeness
  across all elements on all surfaces -- the enumeration discipline that complements the
  per-locale, per-breakpoint discipline.

- **[Evidence Capture Convention](.././evidence-capture.md)**: Each forcing-function that produces
  findings must be recorded as evidence: a defect list, a matrix of results, or a completeness
  assertion captured in the plan's findings or delivery notes.
