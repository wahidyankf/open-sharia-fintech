# Delivery Checklist Validation, Part 2 (Scope 4)

- **Gherkin-tagged TDD steps (one scenario per cycle)**: every behavior RED→GREEN→REFACTOR cycle
  targets exactly one Gherkin scenario — RED carries a single-scenario `**Gherkin (binds) →**`
  tag plus the verbatim inline scenario. **HIGH** a multi-scenario `binds` tag, a missing tag, or a
  non-verbatim inline block. Exceptions (keep multi-scenario `;`-lists): pure-core
  `**Gherkin (underpins) →**` unit tests, and aggregate BDD binders consuming a whole `.feature`.
  Pure refactors and docs/governance-only steps exempt. See
  [Gherkin-Tagged Delivery Steps](../../../../repo-governance/development/workflow/test-driven-development/gherkin-tagged-delivery-steps.md#gherkin-tagged-delivery-steps).
- **UI-design-funnel completeness (UI-bearing plans)**: plans adding/changing user-facing
  screens/components need the design-funnel artefacts (≥2 named low-fi alternatives, 2 hi-fi
  `.excalidraw.png` finalists, named selection, rationale, grounding/prior-art note, responsive
  strategy across mobile/tablet/desktop). Full detail in
  `reference/18-rule17-ui-design-funnel-completeness.md` (Step 5k). Pure-refactor/no-UI/
  governance-only plans exempt. See
  [UI Mockups in Plan Docs convention](../../../../repo-governance/conventions/formatting/diagrams/ui-mockups-principles-and-scope.md#ui-mockups-in-plan-docs-principles-in-practice-and-scope).
- **Manual-assertion locale and evidence completeness (UI/API plans)**: manual-assertion steps must
  cover all supported locales on a multi-locale app and capture committed evidence (screenshots to
  `evidence/`, curl responses inlined). Full detail in
  `reference/10-rule9-manual-behavioral-assertion-validation.md` items 4-5 (Step 5c). Single-locale
  coverage, or no evidence-capture step, is **HIGH**. See
  [Evidence Capture Convention](../../../../repo-governance/development/quality/evidence-capture.md).
- **Rule-15 three-tester retest (web-UI feature-change plans)**: a near-end step runs the
  [`web-ux-test-fixing-planning`](../../../../repo-governance/workflows/web/web-ux-test-fixing-planning.md)
  triad (`web-exploratory-tester`, `web-usability-tester`, `web-design-tester`) across all supported
  locales, with every EWT/UWT/DWT defect finding folded into `delivery.md` as an unchecked checkbox
  fixed before archival (deferral needs explicit user permission, only when genuinely impossible;
  SG-###/USS-### proposals may be triaged/deferred). Unfixed defect checkbox at archival, missing
  step, or single-locale scope: **HIGH**. CLI/text-output and pure governance/agent-definition plans
  exempt. See
  [User-Facing Delivery Hardening](../../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
  Rule 15.
- **Rule-16 API exploratory retest (API feature-change plans)**: a near-end step runs
  `api-exploratory-tester` (`output-mode: delivery`) against the running endpoint(s), with every
  AET-### defect finding folded into `delivery.md` and fixed before archival (same deferral rule;
  SG-### proposals triageable). Unfixed defect checkbox, or missing step on an API feature-change
  plan: **HIGH**. Independent of Rule 15 (a plan changing both UI and API carries both retests).
  Frontend-only/CLI/governance-only plans exempt. See
  [User-Facing Delivery Hardening](../../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
  Rule 16.
- **Knowledge Capture phase presence**: every substantive plan's `delivery.md` carries a final
  Knowledge Capture phase (or explicit "none" record). Full detail in
  `reference/19-rule18-knowledge-capture-phase-presence.md` (Step 5l). Silent absence: **MEDIUM**;
  explicit "none": PASS. See
  [Knowledge Capture Convention](../../../../repo-governance/development/quality/knowledge-capture.md).

### Delivery Checklist Granularity Standard

- Each checkbox is a single, independently verifiable action — not a paragraph of actions.
- Multi-action items must split (e.g. "Install X, configure Y, and verify Z" → 3 checkboxes).
- Every item has a clear done-state.
- Phase transitions have explicit verification steps (e.g. "Verify `nx run app:typecheck` passes").
- Maximum nesting depth: 2 levels (top-level checkbox with sub-checkboxes, no deeper).
- Sub-items independently checkable — completing a parent doesn't auto-complete children.
