# Learnings — Rhino speccoverage multi-line scenario scan

<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->
<!-- Entry shape:
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — no secrets/hostnames)
- **Why it might generalize**: the litmus reasoning
-->

## Phase 0 baseline (recorded, all green)

- `npx nx run rhino-cli:test:unit` — PASS (4 features, 26 scenarios, 102 steps, all passed).
- `npx nx run rhino-cli:specs:behavior:coverage` — PASS ("Spec coverage valid! 57 specs, 316
  scenarios, 1313 steps — all covered.").
- `npx nx run web-ui:specs:behavior:coverage` — PASS ("Spec coverage valid! 21 specs, 118
  scenarios, 311 steps — all covered." — expected green since the `// prettier-ignore` hacks this
  plan removes in Phase 2 are still present).
- No preexisting failures found; nothing to resolve before Phase 1.
