# Stabilize ayokoding-www-fe-e2e Under Parallel-Worker Load

One-line summary: The `ayokoding-www-fe-e2e` Playwright suite flakes under full-suite parallel-worker
load on the shared machine — isolated re-runs pass — so a genuinely-green deliverable can still show a
red aggregate e2e exit code.

> Surfaced 2026-07-23 during ayokoding-learning-path-01-url-restructure execution (Phases 2 and 4).

## Problem / context

Any content/IA change that makes `ayokoding-www-fe-e2e` affected drags the whole e2e suite into the CI
gate, and that suite is load-sensitive on this shared machine. Concrete data points: in Phase 2, one
scenario flaked (`tools/cost-of-living-calculator.feature` "Minimum-role tab is dual currency",
different browser each run; 0 failures isolated). In Phase 4, under heavier concurrent load (build +
typecheck + lint + test:unit running on the same machine), the flake set widened to **3** scenarios —
`course-rehome-redirects.feature` "resolves every re-homed course" (chromium),
`ia-navigation-revamp.feature` "RSS feed item links use bare content URLs" (firefox), and the
cost-of-living calculator spec (firefox) — with 575 passed / 139 skipped otherwise. Re-running exactly
those three isolated passed **9/9** (3 scenarios × chromium/firefox/webkit), and `git diff origin/main
HEAD` was empty, proving none was a regression. The aggregate e2e exit code is therefore an unreliable
gate signal here: it conflates "isolated re-run passes" (flake) with a real failure.

## Why now

The url-restructure family (plans 01–03) keeps making `ayokoding-www-fe-e2e` affected, so this flake
tax recurs every phase and forces manual "isolated re-run to confirm flake" triage before each merge —
exactly the kind of judgment that should not gate an otherwise-green deliverable.

## Prior art / precedents

- Playwright's own guidance on test isolation, workers, and retries —
  [Playwright test parallelism](https://playwright.dev/docs/test-parallel), [retries](https://playwright.dev/docs/test-retries).
- Known-flake quarantine / auto-retry patterns (e.g. Playwright `retries`, flaky-test dashboards).
- The repo's existing shared-machine contention notes (the Nx warm-cache flake and the CI rustup
  concurrency race are the same "concurrent actors on one machine" family).

## Proposed direction (sketch)

Decide the root cause bucket first — dev-server contention vs. worker isolation vs. genuine timing —
by reproducing under controlled load, then pick one of: bound the e2e worker count (or give the suite
its own dev-server instance) so it does not contend with unit/build workers; add a scoped retry/known-
flake policy for the load-sensitive specs; or quarantine the identified specs behind an explicit list
until stabilized. The goal is a trustworthy aggregate exit code, not per-run detective work.

## Rough scope & non-goals

In scope: the three identified load-flaky scenarios and whatever shares their root cause; the CI/Husky
invocation that runs the suite under concurrent load; a retry/quarantine policy if adopted.

Out of scope (for now): e2e _coverage_ gaps (tracked separately in
[`ayokoding-www-e2e-coverage-gaps`](./ayokoding-www-e2e-coverage-gaps.md)); rewriting the specs'
assertions; the broader shared-machine CI contention issues that are not e2e-specific.

## Risks & open questions

Is the root cause dev-server contention, Playwright worker isolation, or genuine app-timing under CPU
starvation? Does bounding workers cost too much wall-clock on CI? Is a blanket `retries: 1` masking a
real intermittent bug rather than pure infra flake? Should the fix live in the project's Playwright
config, the Nx target, or the Husky/CI orchestration?

## What success looks like + promotion signal

Success: the full `ayokoding-www-fe-e2e:test:e2e` suite passes deterministically under full-suite
parallel load (no isolated-re-run triage needed), or flakes are explicitly quarantined with a tracked
list. Promotion signal — ready to become a `backlog/` plan once the root-cause bucket (contention vs.
isolation vs. timing) is identified, since that determines whether the fix is a config change, a
worker-isolation change, or a per-spec repair.
