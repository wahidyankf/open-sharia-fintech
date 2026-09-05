---
title: "Principles and Conventions Implemented/Respected"
description: "Principles/conventions implemented."
category: explanation
subcategory: development
tags:
  - quality
  - planning
  - ui
  - verification
  - testing
  - deployment
created: 2026-06-19
when_to_use: "Use to trace this convention's rationale."
---

# Principles and Conventions Implemented/Respected

## Principles Implemented/Respected

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: The root cause
  of the incident was not weak tests — it was the absence of a human (or Playwright) observing the
  rendered result against the design before declaring the work done. These rules target that root
  cause, not its symptoms.
- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  Every rule converts an implicit assumption ("tests pass, so it must look and work right") into an
  explicit, checkable delivery step.
- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Visual
  and value-bearing verification forces deliberate observation of actual behaviour instead of trust
  in green checkmarks.

## Conventions Implemented/Respected

- **[Manual Behavioural Verification](.././manual-behavioural-verification.md)**: This convention
  extends it from "verify before done" to "verify against the design mockups, per breakpoint, per
  locale, before **archival**."
- **[Evidence Capture Convention](.././evidence-capture.md)**: The per-breakpoint, per-locale sign-off
  required by Rules 1 and 10 MUST leave a committed evidence trail — screenshots in the plan's
  `evidence/` subfolder, screenshot paths referenced from `delivery.md` implementation notes. A
  sign-off claimed without committed evidence is not a sign-off.
- **[Feature Change Completeness](.././feature-change-completeness.md)**: Completeness now includes
  per-breakpoint responsive deliverables and labelled outputs, not just specs+Gherkin parity.
- **[Test-Driven Development](../../workflow/test-driven-development.md)**: Sharpened by Rule 12
  (assertions must distinguish correct from buggy) and Rule 5 (value-bearing, not presence-only).
- **[UI Mockups in Plan Docs](../../../conventions/formatting/diagrams.md)**: Sharpened by Rules 2
  and 8 (name the design-system primitive; annotate mockup colors as theme tokens).
