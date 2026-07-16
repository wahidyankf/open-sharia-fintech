# Business Requirements: E2E Scenario Coverage Gap Detector

## Problem

`playwright-bdd`'s `missingSteps: skip-scenario` config (used project-wide across E2E suites)
converts any Gherkin scenario without a bound step definition into `test.fixme` instead of failing
`bddgen` or CI. This means a scenario can be added to a `.feature` file, tagged `@e2e`, and simply
never run — with zero signal to the author, reviewer, or CI. The only mitigation today is a code
comment documenting the tradeoff, which has already failed once to prevent a fresh, unrelated gap
from being introduced in the same PR that documented it.

## Business Impact

- Silent coverage gaps erode confidence that "green CI" means "E2E-verified." A regression in an
  unbound scenario's behavior would not be caught by the E2E suite at all.
- The repo already carries ~104 pre-existing gap scenarios tracked informally in `plans/ideas.md`
  for this exact reason (per `apps/ayokoding-www-fe-e2e/playwright.config.ts`'s existing
  in-comment justification) — the gap is a known, recurring, and growing category of risk, not a
  one-off.
- Reviewers (human or AI) currently must manually run `bddgen` and hand-count bound vs. declared
  scenarios per feature file to catch this — that does not scale and has already been proven to
  miss cases (cycle 3 of the resizable-docs-sidebar PR review caught a 7-scenario gap that cycle
  1's own documented awareness did not prevent).

## Goals

- Make an unbound `@e2e`-tagged Gherkin scenario a **visible, actionable signal** (CI failure or
  clearly surfaced report) rather than a silent `test.fixme`.
- Preserve the existing, intentional ~104-scenario backlog gap (tracked in `plans/ideas.md`) as a
  known baseline, rather than immediately failing CI for pre-existing debt.
- Give reviewers (pr-review-maker, ci-checker, or a human) a mechanical way to see "N scenarios
  declared, M bound" per E2E project without manually running `bddgen`.

## Non-Goals

- Not proposing to switch `missingSteps` to `fail-on-gen` outright — that would immediately break
  CI on the ~104 pre-existing gap scenarios and needs its own migration plan.
- Not attempting to auto-generate missing step definitions.

## Stakeholders

- Contributors adding new Gherkin scenarios to any `*-e2e` project.
- `pr-review-maker` / `ci-checker` — consumers of whatever signal this produces.
