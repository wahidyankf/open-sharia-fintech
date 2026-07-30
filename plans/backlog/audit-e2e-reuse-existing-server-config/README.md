# Audit `reuseExistingServer` Across `*-e2e` Playwright Configs

> **Status**: Backlog (not started). Filed from a Knowledge Capture learning surfaced during
> [`ayokoding-www-tools-ai-benchmark`](../../done/2026-07-30__ayokoding-www-tools-ai-benchmark/README.md)'s
> Phase 10 Rule-15 retest.

## Context

While running a scoped `ayokoding-www-fe-e2e` subset, a long-lived `next dev` process (started
hours earlier, before that session's code changes) was already listening on the app's port.
Playwright's `reuseExistingServer: true` found it and skipped running the configured
`webServer.command` entirely — so the e2e run silently exercised stale dev-mode code instead of the
production build the config actually specifies (`NODE_ENV: "production"`, a standalone server,
e2e-specific env vars such as `AYOKODING_WEB_MANIFESTS_DIR`). A later full e2e run against the same
stale server produced a wall of unrelated-looking failures, all traced back to the reused server
never having the e2e fixture manifests directory wired in.

A repo-wide grep of every `*-e2e` project's `playwright.config.ts` (2026-07-30) shows the setting is
hardcoded `true` unconditionally in six configs, not gated on `!process.env.CI`:

- `apps/ayokoding-www-fe-e2e/playwright.config.ts`
- `apps/ayokoding-www-be-e2e/playwright.config.ts`
- `apps/organiclever-www-fe-e2e/playwright.config.ts`
- `apps/wahidyankf-www-fe-e2e/playwright.config.ts`
- `apps/ose-www-fe-e2e/playwright.config.ts`
- `apps/ose-www-be-e2e/playwright.config.ts`

Only one config already gates it correctly:

- `apps/organiclever-app-web-e2e/playwright.config.ts` — `reuseExistingServer: !process.env.CI`

This is a Playwright-documented, common local-dev convenience setting: it silently reuses ANY
process already bound to the target port, including one from an unrelated earlier session/purpose,
with no warning that the configured `webServer.command` (and its env vars) was skipped.

## Scope

**In scope**: the six `playwright.config.ts` files listed above; a decision on whether
`reuseExistingServer` needs a CI-conditional gate, doc caveat, or automated check.

**Out of scope**: any change to the e2e test scenarios themselves; the already-fixed
`ayokoding-www-tools-ai-benchmark` incident this was filed from.

## Navigation

- [brd.md](./brd.md) — WHY: business rationale, impact, risk.
- [prd.md](./prd.md) — WHAT: user story, Gherkin acceptance criteria, product scope.
- [tech-docs.md](./tech-docs.md) — HOW: the proposed investigation and the open remedy decision the
  investigation phase resolves.
- [delivery.md](./delivery.md) — DO: phased, gated delivery checklist, quality gates, verification.
- [learnings.md](./learnings.md) — Knowledge Capture running log for this plan's own execution.

## Delivery Mode

`worktree-to-pr` (the repo default) — this is a config/tooling change spanning multiple `apps/`
projects, so it is filed as its own plan per the code-homed-learnings-are-never-landed-inline rule
rather than folded into any single app's plan.
