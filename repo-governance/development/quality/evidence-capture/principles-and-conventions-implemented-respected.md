---
title: "Principles and Conventions Implemented/Respected"
description: "Principles and conventions this convention implements."
category: explanation
subcategory: development
tags:
  - evidence
  - testing
  - screenshots
  - plans
  - verification
  - locale
  - manual-testing
created: 2026-06-20
when_to_use: "Use when tracing this convention to the principles/conventions behind it."
---

# Principles and Conventions Implemented/Respected

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Evidence
  makes verification visible and checkable. "I tested it" is implicit; a screenshot and a curl response
  in the delivery notes are explicit.
- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: When a defect surfaces
  post-archival, evidence lets the investigator reconstruct what the state was at delivery time — a root
  cause investigation tool, not just a bureaucratic artifact.
- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: Capturing
  evidence forces the tester to actually observe the system, not just trust that tests passed. The act of
  taking a screenshot and recording the curl output is itself the deliberate observation step.

## Conventions Implemented/Respected

- **[Manual Behavioural Verification](.././manual-behavioural-verification.md)**: Evidence capture is the
  persistent record of manual verification. The two conventions are complementary: this one defines the
  storage structure; the other defines the verification actions.
- **[Plans Organization Convention](../../../conventions/structure/plans.md)**: The `evidence/` subfolder
  sits inside the plan folder and moves with it through the lifecycle (`backlog/` → `in-progress/` →
  `done/`).
- **[Temporary Files Convention](../../infra/temporary-files.md)**: `local-tmp/` is for ephemeral scratch
  work. Evidence that should survive across sessions and be committed belongs in the plan's `evidence/`
  folder, not in `local-tmp/`.
