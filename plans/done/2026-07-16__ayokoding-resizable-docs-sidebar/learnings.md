<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

## Learning: playwright-bdd's `missingSteps: skip-scenario` silently drops E2E scenario coverage with no build/test failure

- **Context**: PR-Review Maker→Fixer cycle 3 review of `resizable-panel.feature` found only 3 of
  its 10 scenarios had e2e step defs bound in `ayokoding-www-fe-e2e`; the other 7 (including
  drag-persist-at-end and Home/End keyboard-jump) silently became `test.fixme`. This is the
  **second** time the same root cause surfaced in this same PR — cycle 1 had already flagged an
  equivalent gap as a MEDIUM finding and "resolved" it via an in-comment justification in
  `apps/ayokoding-www-fe-e2e/playwright.config.ts` for keeping `missingSteps: skip-scenario`
  project-wide rather than switching to `fail-on-gen`.
- **Observation**: with `missingSteps: skip-scenario`, any Gherkin scenario lacking a step
  definition binds to `test.fixme` instead of failing `bddgen` or CI. Nothing in the pipeline
  compares "scenarios declared in a `.feature` file" against "scenarios actually bound" — the gap
  is only caught by manually running `bddgen` and counting. The repo already tracks ~104
  pre-existing gap scenarios informally in `plans/ideas.md` for this exact reason.
- **Why it might generalize**: the in-comment documentation from cycle 1 did not prevent a fresh,
  unrelated 7-scenario gap from being introduced later in the same PR — a documented awareness of
  the pattern was not sufficient to catch a recurrence. Any future contributor adding a new
  `@e2e`-tagged scenario to any `*-e2e` project can hit the identical silent gap.

**Litmus**: PASSES — a mechanical coverage-count validator (comparing Gherkin `Scenario:` count to
actually-bound step count per e2e project) would catch this automatically next time, unlike the
in-comment documentation that already failed to prevent recurrence once.

**Secret/sensitivity gate**: no secrets or sensitive values in this entry — pass.

**Repo-relevance gate**: pure repo-tooling/testing-infrastructure content, not infra-private —
belongs in the public repo(s); pass.

**Routing**: code home (a new coverage-gap validator, likely `rhino-cli` or a `ci-checker`
enhancement) — per the Code-Routing Downstream Rule, ALWAYS filed as a separate `plans/backlog/`
plan, NEVER landed inline. Filed at
`plans/backlog/2026-07-16__e2e-scenario-coverage-gap-detector/`. The immediate instance of the gap
(the 7 unbound `resizable-panel.feature` scenarios) was itself fixed inline in this plan's own PR
(commit `4f01636e6`) as a current-plan-blocker under Root Cause Orientation — only the systemic
prevention mechanism is deferred to the backlog plan above.

---

## Learning: jsdom's `cssstyle` package silently clears an element's entire `style` attribute when both `maskImage` and `WebkitMaskImage` are set

- **Context**: writing a regression test in `resizable-sidebar.test.tsx` to pin the UWT-002
  overflow-fade-gradient fix in `sidebar-tree.tsx` (a real HIGH finding from PR-Review cycle 3
  about missing test coverage, which was fixed inline in this plan).
- **Observation**: `sidebar-tree.tsx` sets both `style.maskImage` and `style.WebkitMaskImage` (for
  cross-browser mask-image support) on the same element. In jsdom's `cssstyle`-backed
  `HTMLElement.style`, setting both camelCase properties on the same element causes the entire
  `style` attribute to be silently cleared rather than throwing or applying either value —
  reproduced directly against raw `jsdom` (not React-specific). The regression test worked around
  this by asserting the `data-overflowing` boolean attribute (driven by the same underlying
  condition) instead of asserting on the mask-image style values directly.
- **Litmus**: DISCARDED — no durable surface in this repo would "automatically catch" a future
  instance of this narrow jsdom/`cssstyle` quirk; it only bites when a test asserts directly on
  dual-vendor-prefixed inline mask-image style values in jsdom, which is a narrow and now-avoided
  pattern (the existing test already routes around it via the `data-overflowing` attribute rather
  than needing a code fix). Not routed to a durable home — noting here for anyone who independently
  rediscovers the same jsdom behavior while debugging a similar style-attribute assertion.

**Routing**: discard — not generalizable enough to route to a durable home; the one call site
affected already uses a robust workaround (attribute-based assertion) and no other component in
this plan's scope sets dual vendor-prefixed mask properties in a way a test asserts on directly.
