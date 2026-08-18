---
title: "Step 5: Double-Zero Confirmation"
description: Why a single zero-finding pass does not terminate the API quality gate loop and what a second clean pass confirms.
when_to_use: Use when a re-test comes back with zero in-threshold findings and you need to decide whether the loop can terminate.
---

# Step 5: Double-Zero Confirmation

A single zero-finding pass does not terminate the loop. When step 4 returns zero in-threshold
findings, run **one more** full test pass against the same deployed build:

- Still zero → the double-zero holds; proceed to step 6 with status `pass`.
- Findings appeared → the first zero was a false negative; return to step 3.

This mirrors the [UI Quality Gate](../../ui/ui-quality-gate.md) and is mandated by the
[Workflow Identifier Convention](../../meta/workflow-identifier.md): a gate
terminates on two consecutive clean validations, never one.
