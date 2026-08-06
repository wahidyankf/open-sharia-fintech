# AyoKoding www e2e coverage gaps

One-line summary: implement the missing Playwright step definitions so `ayokoding-www-fe-e2e` can
revert from `skip-scenario` back to the safer `fail-on-gen` default.

> Surfaced 2026-07-15 during ayokoding-resizable-docs-sidebar execution; expanded 2026-07-03 during CI-flake triage.

## Problem / context

`apps/ayokoding-www-fe-e2e/playwright.config.ts` runs with `missingSteps: "skip-scenario"` because
~104 scenarios across `navigation.feature` / `content-rendering.feature` / `search.feature` and others
have no step definitions — they are marked `test.fixme` and never run. Separately,
`cost-of-living-calculator.feature` has **83** missing step definitions (country-filter interaction,
ASEAN-region grouping, qualifying/non-qualifying divider rows, minimum-role-rank thresholds) — a
genuine ~2-week-old content gap, not work-in-progress.

## Why now

`skip-scenario` is a project-wide safety compromise: any newly-added uncovered scenario **silently
skips** instead of failing the suite. The safer `fail-on-gen` default cannot return until the backlog
of uncovered scenarios is burned down.

## Prior art / precedents

- **Playwright test annotations** — `test.fixme`/`test.skip` is the exact mechanism marking the
  uncovered scenarios that this idea burns down. [Playwright](https://playwright.dev/docs/test-annotations)
- **Gherkin step definitions (Cucumber)** — the `.feature`-to-step-definition model whose missing
  bindings are the coverage gap. [Cucumber](https://cucumber.io/docs/gherkin/)
- **Specs & Gherkin Completeness convention** — the repo rule requiring companion Gherkin coverage that
  this backlog violates. [feature-change-completeness](../../../repo-governance/development/quality/feature-change-completeness.md)

## Proposed direction (sketch)

- Implement the missing step defs against the running app (`nx run ayokoding-www:serve` + browser
  automation), not by authoring blind from the `.feature` files.
- Burn down the ~104 general + 83 calculator scenarios.
- Flip `missingSteps` back to `fail-on-gen` once the suite is green.

## Rough scope & non-goals

In scope: step-definition implementation for the existing uncovered scenarios and the config flip.

Out of scope (for now): adding new feature scenarios; rewriting the `.feature` files themselves.

## Risks & open questions

- How many of the ~104 are genuinely unimplemented vs. already covered or stale/wrong? (open — needs
  an audit pass)
- The cost-of-living logic (country/region filtering, savings thresholds) needs live UI verification;
  writing 83 steps blind risks encoding the wrong behaviour. (open)

## What success looks like + promotion signal

Success: `missingSteps: "fail-on-gen"` is restored with a green `test:e2e`. Ready to promote to a
`backlog/` plan when someone can dedicate a session with the app serving + browser automation — the
work is verification-heavy, not design-heavy.
