---
description: Rebuilds and redeploys once, then verifies original findings and smoke-tests affected API behaviour.
when_to_use: Use when verifying a fix after Step 3 has been applied.
---

# Step 4: Verification

Rebuild and redeploy the service once. A build or deployment error ends the run with `fail`.

Invoke `api-exploratory-tester` once in scoped verification mode against the **current** build. Pass
`quality-gate-phase: verification`, the original in-threshold finding IDs and reproduction steps,
and `affected-operations`. Verify each original finding, then run a regression smoke over affected
operations, authorization boundaries, payload shapes, and error behaviour. Do not repeat the full
discovery sweep or expand into unrelated endpoints.

Preserve Step 0's delegation set; invalid lifecycle evidence remains pending instead of being rerun.
Unresolved original findings or regressions produce `partial`. A tester or evidence-capture error
produces `fail`. A clean verification produces `pass`. No outcome starts another pass automatically.
