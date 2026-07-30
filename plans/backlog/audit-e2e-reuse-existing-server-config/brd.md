# Business Requirements: Audit `reuseExistingServer` Across `*-e2e` Playwright Configs

## Problem Statement

A stale, unrelated dev server silently absorbing an e2e run produces a "wall of unrelated-looking
failures" that costs debugging time disproportionate to the actual defect (a config gate), and —
worse — can mask a real regression by exercising the wrong build entirely.

## Impact

**Affected roles**: any engineer or AI agent running `*-e2e` suites locally on a machine with a
long-lived dev server already listening on the target port; potentially CI if runners are shared
rather than ephemeral (the open question this investigation resolves).

## Success Metrics

Zero `*-e2e` Playwright configs that hardcode `reuseExistingServer: true` unconditionally once the
audit's chosen remedy (config gate, doc caveat, or automated check) lands — gut-based, no
fabricated KPI.

## Risks

- **Undecided CI-runner persistence could stall the remedy choice.** The Phase 1 investigation must
  determine whether CI runners are ephemeral-per-job or shared/persistent before Phase 2 can choose
  between a config gate, a doc caveat, or both.
- **Scope creep into the six configs' e2e test scenarios.** This plan's remedy is limited to the
  `reuseExistingServer` setting itself — not the test scenarios or assertions those configs drive.
