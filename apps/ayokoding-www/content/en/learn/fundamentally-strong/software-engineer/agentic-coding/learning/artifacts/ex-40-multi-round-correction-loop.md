---
title: "Artifact: A Three-Round Correction Loop, Converging"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 80
---

> Three feedback rounds on one diff, narrowing toward the acceptance bar -- exercises co-23.

**Acceptance bar**: the endpoint must (1) return `409 Conflict` if the shipment already shipped, (2)
return `404` if the shipment ID doesn't exist, (3) return `200` with the cancellation record on
success, (4) be idempotent -- a second cancel call on an already-cancelled shipment also returns
`200`, not an error.

**Round 1 diff**: implements criteria 1 and 3 only. **Feedback**: "criteria 2 and 4 are both
missing -- an unknown shipment ID currently falls through to a 500, and a second cancel call on an
already-cancelled shipment raises instead of returning 200."

**Round 2 diff**: adds a 404 check for unknown IDs (closes criterion 2) and adds an
already-cancelled check that raises a 409 (attempts criterion 4, but wrongly). **Feedback**:
"criterion 4 specifically requires a second cancel to return 200, not 409 -- 409 is reserved for
'shipment already shipped' (criterion 1). An already-cancelled shipment is a different case:
cancelling twice should be a no-op success, not a conflict."

**Round 3 diff**: adds a dedicated already-cancelled branch that returns `200` with the existing
cancellation record instead of re-raising 409, keeping the shipped-conflict check (criterion 1)
untouched. **Result**: all four criteria met; round 3 is accepted.

**Convergence table**:

| Round | Criteria met | Criteria still open   |
| ----- | ------------ | --------------------- |
| 1     | 1, 3         | 2, 4                  |
| 2     | 1, 2, 3      | 4 (wrong status code) |
| 3     | 1, 2, 3, 4   | none                  |
