---
title: "Step 6: Iteration Control"
description: The final pass/partial/fail status rules for the API quality gate loop and the iteration-5 escalation warning.
when_to_use: Use when determining the API quality gate's final status after repeated test-fix cycles.
---

# Step 6: Iteration Control

Repeat steps 1-5 until the double-zero holds, or `max-iterations` is reached. Warn at
iteration 5 that the loop is approaching its ceiling.

- **`pass`** — zero in-threshold findings on **two consecutive** re-tests against the current build.
- **`partial`** — findings remain but iterations are exhausted.
- **`fail`** — the service could not be reached, or the contract could not be resolved.
