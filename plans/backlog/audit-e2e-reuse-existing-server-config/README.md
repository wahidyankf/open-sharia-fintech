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

## Business Rationale (Condensed BRD)

**Why this matters**: a stale, unrelated dev server silently absorbing an e2e run produces a "wall
of unrelated-looking failures" that costs debugging time disproportionate to the actual defect (a
config gate), and — worse — can mask a real regression by exercising the wrong build entirely.
**Affected roles**: any engineer or AI agent running `*-e2e` suites locally on a machine with a
long-lived dev server already listening on the target port; potentially CI if runners are shared
rather than ephemeral (the open question this investigation resolves). **Success metric**: zero
`*-e2e` Playwright configs that hardcode `reuseExistingServer: true` unconditionally once the
audit's chosen remedy (config gate, doc caveat, or automated check) lands — gut-based, no
fabricated KPI.

## Product Requirements (Condensed PRD)

**User story**: As an engineer or AI agent running an `*-e2e` Playwright suite, I want
`reuseExistingServer` to never silently substitute an unrelated stale server for the suite's own
configured build, so that a passing (or failing) e2e run reflects the code under test rather than
whatever process happened to already be bound to the port.

**Gherkin acceptance criteria**:

```gherkin
Feature: reuseExistingServer audit and remedy

  Scenario: CI runners are confirmed ephemeral per job
    Given the availability investigation confirms CI runners are ephemeral per job
    When the audit concludes
    Then the remedy is a documentation caveat for local development, not a config change

  Scenario: CI runners are confirmed shared or persistent
    Given the availability investigation confirms CI runners are shared or persistent
    When the audit concludes
    Then each of the six hardcoded-true configs is gated to match
      "organiclever-app-web-e2e"'s "reuseExistingServer: !process.env.CI" pattern

  Scenario: A future *-e2e config is added
    Given the audit's chosen remedy includes an automated guard
    When a new "*-e2e" Playwright config sets "reuseExistingServer: true" unconditionally
    Then the guard flags it before merge
```

**Product scope**: covers the six `playwright.config.ts` files enumerated in Context; does not
cover the e2e test scenarios or assertions themselves.

## Technical Approach

**Proposed Investigation**:

- Confirm whether CI runners for the six hardcoded-`true` configs ever actually risk a port
  collision (fresh runner per job vs. a shared/reused runner where a stray process could persist).
- If CI runners are ephemeral per job, the risk is local-development-only — the fix might be
  documentation (a caveat on developers running e2e locally) rather than a config change.
- If CI runners are shared/persistent (self-hosted runners are used in this repo — see
  [`plans/done/2026-07-19__fundamentally-strong-software-engineer/learnings.md`](../../done/2026-07-19__fundamentally-strong-software-engineer/learnings.md#openapi-generator-cli-jar-download-race-is-a-second-concurrency-flake-class),
  which records a shared-tool-cache concurrency race on a co-triggered self-hosted runner and
  generalizes it as "any tool with a shared local cache, invoked by 2+ workflows the same push
  fires concurrently"), the six hardcoded configs should likely match `organiclever-app-web-e2e`'s
  `!process.env.CI` gate.
- Consider whether a lightweight guard (e.g. a `ci-checker` rule, or a comment convention) should
  flag any new `*-e2e` Playwright config that sets `reuseExistingServer: true` unconditionally.

## Worktree

Worktree path: `worktrees/audit-e2e-reuse-existing-server-config/`

Optional manual pre-provisioning (run from repo root):

```bash
claude --worktree audit-e2e-reuse-existing-server-config
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest
`origin/main` when missing, syncs with `origin/main` before implementing, and prompts before
deleting the worktree after the plan is archived and pushed.

## Delivery Checklist

`[AI]` = agent-executable step. `[HUMAN]` = requires a human decision or credential this repo's
agents may not exercise. No `[HUMAN]` step is anticipated for this plan — recorded for completeness
per the legend convention.

### Phase 1: CI Runner Persistence Investigation

- [ ] [AI] Determine whether each of the six configs' CI runners are ephemeral-per-job or
      shared/persistent (checking workflow YAML runner labels against this repo's self-hosted vs.
      GitHub-hosted runner usage)
- [ ] [AI] Record the availability/persistence matrix per config, with the evidence used for each
      verdict

### Phase 1 Gate

- [ ] [AI] Every one of the six configs has a recorded, evidenced ephemeral-or-persistent verdict

> **Pause Safety**: this plan is Backlog (not started) — no work has begun, so there is nothing to
> resume. Promotion to `in-progress/` re-reads this README from the top.

### Phase 2: Remedy Selection and Application

- [ ] [AI] Based on Phase 1's verdicts, choose the remedy per config: a `!process.env.CI` gate
      (matching `organiclever-app-web-e2e`), a documentation caveat, or both
- [ ] [AI] Apply the chosen remedy to each of the six configs
- [ ] [AI] Decide whether an automated guard (checker rule or comment convention) is warranted and,
      if so, add it

### Phase 2 Gate

- [ ] [AI] Every one of the six configs matches its chosen remedy; no config is left
      unconditionally hardcoded `true` without a documented, evidenced reason

> **Pause Safety**: work is only underway once Phase 1 completes; a partial Phase 2 leaves the
> matrix from Phase 1 as the resumption point.

## Quality Gates

Local: `npx nx affected -t typecheck lint test:quick` for every touched `*-e2e` project exits 0.
CI: the same targets green on the PR's own CI run before merge, per this repo's standard PR Merge
Protocol.

## Verification

The plan is complete when all six configs have a recorded, evidenced ephemeral-or-persistent
verdict and a remedy applied consistent with that verdict, and (if added) the automated guard
passes against the current repo state.

## Delivery Mode

`worktree-to-pr` (the repo default) — this is a config/tooling change spanning multiple `apps/`
projects, so it is filed as its own plan per the code-homed-learnings-are-never-landed-inline rule
rather than folded into any single app's plan.
