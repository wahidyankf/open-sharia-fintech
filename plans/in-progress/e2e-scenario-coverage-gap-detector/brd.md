# Business Requirements: E2E Scenario Coverage Gap Detector

## Business Goal

Make an unbound `@e2e`-tagged Gherkin scenario a **visible, mechanical, actionable signal** — a
failing quality gate that names the offending feature file and scenario — instead of a silent
`test.fixme`. Do this without immediately breaking CI on the repo's known pre-existing debt.

## Problem

`playwright-bdd`'s `missingSteps: "skip-scenario"` config converts any Gherkin scenario without a
bound step definition into `test.fixme` instead of failing `bddgen` or CI `[Repo-grounded:
apps/ayokoding-www-fe-e2e/playwright.config.ts]`. A scenario can be added to a `.feature` file,
tagged `@e2e`, and simply never run — with zero signal to the author, reviewer, or CI. The only
mitigation today is a code comment documenting the tradeoff, which has already failed once to prevent
a fresh, unrelated gap from being introduced in the same PR that documented it `[Repo-grounded:
plans/done/2026-07-16__ayokoding-resizable-docs-sidebar, plans/ideas.md]`.

## Business Impact

- **Silent coverage gaps erode "green CI = E2E-verified" confidence.** A regression in an unbound
  scenario's behavior would not be caught by the E2E suite at all `[Judgment call]`.
- **The gap is a recurring, known category of risk, not a one-off.** The repo already carries ~104
  pre-existing unbound scenarios tracked informally in `plans/ideas.md` `[Repo-grounded]`; the same
  root cause recurred twice within a single PR `[Repo-grounded: plans/ideas.md ayokoding-www-fe-e2e
note]`.
- **Manual detection does not scale and has already missed cases.** Reviewers (human or AI) currently
  must run `bddgen` and hand-count bound vs. declared scenarios per feature file; cycle 3 of the
  resizable-docs-sidebar PR review caught a 7-scenario gap that cycle 1's own documented awareness did
  not prevent `[Repo-grounded]`.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears these hats, and these agents consume
the artifacts:

- **Contributor hat**: adds new Gherkin scenarios to any playwright-bdd `*-e2e` project; wants a
  fast local signal (pre-push) when a new `@e2e` scenario ships unbound.
- **Reviewer hat / `pr-review-maker` / `ci-checker`**: consume the `specs:e2e:coverage` gate result
  as a mechanical, reviewer-visible signal in the PR CI run `[Repo-grounded: .claude/agents/ci-checker.md,
.claude/agents/pr-review-maker.md]`.
- **Toolchain-maintainer hat**: owns `rhino-cli` and its byte-identity obligation across
  `ose-public` / `ose-primer` / `ose-infra` `[Repo-grounded: docs/reference/sdlc-gate-standard.md]`.

## Business-Level Success Metrics

- **A newly-added unbound `@e2e` scenario is caught before merge** by an automated gate rather than by
  a human hand-counting — measured by the reproducible acceptance scenarios in `prd.md` passing
  `[Judgment call: the gate either fires on a new gap or it does not; the acceptance tests make this
observable]`.
- **Zero disruption to the existing ~104-scenario backlog** — the validator ships without requiring
  any pre-existing gap to be fixed first (baseline-aware) `[Judgment call]`.
- **No new manual step for reviewers** — the signal appears in the gate reviewers already read
  (`test:quick` → `test:specs` at pre-push/PR/main), requiring no separately-remembered command
  `[Repo-grounded: nx-targets.md §All-Four-Gates Rule]`.

## Business-Scope Non-Goals

- Not switching `missingSteps` to `"fail-on-gen"` outright — that would immediately break CI on the
  ~104 pre-existing gap scenarios and needs its own migration plan.
- Not auto-generating missing step definitions.
- Not burning down the existing ~104-scenario backlog (separate `plans/ideas.md` follow-up).

## Business Risks and Mitigations

| Risk                                                                                      | Likelihood | Mitigation                                                                                                                                      |
| ----------------------------------------------------------------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| Baseline manifest becomes a rubber-stamp — contributors keep growing it instead of fixing | Medium     | Baseline lists **specific scenario titles**, not a raw count, so each addition is a reviewable diff line in the PR `[Judgment call]`            |
| Running `bddgen` at pre-push slows the fast gate                                          | Low        | `bddgen` is codegen-only (no browser, no server, sub-second); only the expensive Playwright execution stays CRON-only `[Judgment call]`         |
| `rhino-cli` change breaks byte-identity across the three sibling repos                    | Medium     | Dedicated parity phase propagates identical `src/` + specs to `ose-primer`/`ose-infra` before archival `[Repo-grounded: sdlc-gate-standard.md]` |
| Validator gives false confidence on `fail-on-gen` projects (which already hard-fail)      | Low        | Documented in `tech-docs.md`: on `fail-on-gen` projects the validator is belt-and-suspenders; its primary value is on `skip-scenario` projects  |

## Related

- [prd.md](./prd.md) — the testable acceptance scenarios that operationalize these goals.
- [Knowledge Capture Convention](../../../repo-governance/development/quality/knowledge-capture.md)
- [SDLC Gate Standard — rhino-cli Byte-Identity Boundary](../../../docs/reference/sdlc-gate-standard.md#rhino-cli-byte-identity-boundary)
