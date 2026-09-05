---
title: "Step 6 — Quality Gate"
description: Describes invoking plan-quality-gate at strict mode and the success criteria and retry behaviour.
when_to_use: Use when running the plan-quality-gate workflow as Step 6 of plan-establishment.
---

# Step 6. Quality Gate (Sequential)

Run the `plan-quality-gate` workflow at `strict` mode.

Follow the [plan-quality-gate workflow](../plan-quality-gate.md) with:

- **Input** `scope`: the resolved `<plan-dir>`
- **Input** `mode`: `strict`
- **Output**: `final-status`, `final-report`

**Success criteria**: `plan-quality-gate` returns `pass` (zero CRITICAL/HIGH/MEDIUM on two
consecutive checks).

**On `partial` or `fail`**: Investigate the final report. Apply targeted fixes. Re-run
`plan-quality-gate` up to 2 additional times. If still not `pass`, terminate with status
`partial` and surface the final report.
