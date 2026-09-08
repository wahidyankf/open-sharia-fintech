---
description: Final pass, partial, fail, and lifecycle rules for one bounded API quality gate run.
when_to_use: Use when closing an API quality gate run.
---

# Step 5: Finalization

Preserve the lifecycle evidence ledger throughout the run. Missing or stale lifecycle evidence
stays `pending`; do not turn it into a domain finding or rerun the delegated check.

- **`pass`** — discovery is clean, or scoped verification resolves every original finding without
  regression.
- **`partial`** — an original finding remains or affected-API smoke exposes a regression.
- **`fail`** — discovery, fixing, build, deployment, verification, contract resolution, or evidence
  capture cannot complete.

Report the domain status above separately from `lifecycle-status` (`verified`, `pending`, or
`not-applicable`). A pending lifecycle owner does not change the domain result, but still blocks
delivery when its owning hook or CI gate runs. An applicable API gate is merge-ready only when
`final-status` is `pass` and lifecycle status is `verified` or `not-applicable`.

The workflow never starts another discovery, fix, rebuild, deployment, or verification pass. A
later attempt is a new explicitly started run with fresh inputs and evidence.
