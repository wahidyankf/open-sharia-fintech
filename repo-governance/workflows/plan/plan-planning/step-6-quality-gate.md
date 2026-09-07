---
title: "Step 6 — Quality Gate"
description: Invokes the plan-quality-gate governance gate and defines how each terminal verdict is handled.
when_to_use: Use when running the plan-quality-gate workflow as Step 6 of plan-establishment.
---

# Step 6. Quality Gate (Sequential)

Run the [plan-quality-gate](../plan-quality-gate.md) governance gate. This step is one of the gate's three
**named pre-authorizations**: no workflow outside that list may invoke it without the user naming
it explicitly.

Follow the workflow with:

- **Input** `plan-path`: the resolved `<plan-dir>`
- **Input** `checkpoint`: `pre-execution`
- **Output**: `verdict`, `ledger`

The gate takes no `mode`: it has no severity threshold, and every admitted ledger row must be
closed.

**Success criteria**: the gate returns `PASS`.

**On any `BLOCKED_*` verdict**: read the returned ledger. `BLOCKED_INPUT_CHANGED` means an input
moved under the run — re-establish the snapshot and invoke the gate once more.
`BLOCKED_NON_CONVERGENT` and `BLOCKED_TOOLING` are terminal for this step: do not re-run the gate in
a loop hoping for a different verdict. Terminate plan-establishment with status `partial`, surface
the ledger, and name the external change required.

## Related Documents

- [Plan Quality Gate](../plan-quality-gate.md) — the gate this step invokes.
- [Governance Gate Class](../../meta/workflow-identifier/governance-gate-class.md) — why there is no mode and no iteration.
