<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: E2E Scenario Coverage Gap Detector

Append one entry per generalizable learning as it surfaces during execution, using the shape below.
Sanitize per the secret/sensitivity gate before writing. Triage all entries in Phase 7's Knowledge
Capture section (before archival-in-PR) before archival.

<!--
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized)
- **Why it might generalize**: the litmus reasoning
- **Terminal state**: routed inline to <path> / filed as plans/backlog/<slug> / discarded — <reason>
-->

## Execution evidence to record here

- Exact unbound-scenario count captured into `apps/ayokoding-www-fe-e2e/e2e-coverage-baseline.json`
  (Phase 5, expected ~104).
- Synthetic-gap verification output (the FAIL naming the injected scenario, and the PASS after revert).
- Manual CLI verification: pass-case and fail-case output of `specs:e2e:coverage`.
