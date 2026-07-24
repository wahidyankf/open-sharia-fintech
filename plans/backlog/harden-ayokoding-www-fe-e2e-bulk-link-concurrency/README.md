# Harden `ayokoding-www-fe-e2e` Bulk-Link-Check Concurrency

> **Status**: Backlog (not started). Filed from a Knowledge Capture learning surfaced during
> [`ayokoding-learning-path-02-schema-and-prerequisite-dag`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/README.md)'s
> Phase 5 integration verification, where `ayokoding-www-fe-e2e:test:e2e` flaked in 4 of 7 runs in
> one session.

## Context

Two Playwright step files in `apps/ayokoding-www-fe-e2e/src/steps/` each collect every internal link
on a rendered page and check them **all concurrently** via an unbounded `Promise.all`, against a
single local `next start` production server process:

- `ia-navigation-revamp.steps.ts` — checks every internal content link resolves without a redirect.
- `course-rehome-redirects.steps.ts` — checks every course-catalog entry resolves, not 404.

Both fire `page.request.get(href, { timeout: 10000 })` for every collected `href` at once. Across
one session's repeated runs of the full suite, this pattern produced 4 distinct failures in 7
attempts — each a _different_ single sub-test, each a network-layer symptom
(`ECONNRESET`, or a 10s client-side timeout where the response log shows the server answered
`200 OK` just after the client gave up) rather than a functional break. The suite passed cleanly
twice with zero code change (578/759 passed, 181 skipped, identical counts both times), which rules
out a deterministic regression — the underlying pages resolve correctly; the check harness is what's
fragile under concurrent load.

Notably, a prior commit (`c61084bca`, unrelated to this plan and predating it) already parallelized
`ia-navigation-revamp.steps.ts`'s link checks specifically **to fix a sequential-timeout problem** —
this backlog plan is the second half of that same tension: sequential was too slow, unbounded-parallel
is flaky. The fix is bounded concurrency (and/or a retry), not a return to sequential.

## Scope

**In scope**:

- A small, shared, bounded-concurrency + single-retry helper for the "fetch every href, assert not
  404" pattern used by both step files.
- Applying that helper to `ia-navigation-revamp.steps.ts` (two call sites) and
  `course-rehome-redirects.steps.ts` (one call site).
- A test that demonstrates the fix's reliability under concurrent load (see
  [tech-docs.md](./tech-docs.md) for the falsifiable-both-ways shape, given the underlying failure
  mode is inherently probabilistic).

**Out of scope**:

- Any change to `ayokoding-www`'s actual routes, redirects, or content — this is a test-harness
  hardening, not a product fix.
- The unrelated, already-adjudicated `ayokoding-www:test:e2e` / `test:integration` no-op-stub
  question from the same source plan's Knowledge Capture — investigation there confirmed the
  no-op stubs are the _correct_, documented pattern (`nx-targets.md`'s dedicated-`*-e2e`-runner
  convention), not a gap, so no backlog item was filed for it.

## Navigation

- [brd.md](./brd.md) — WHY: business rationale, impact, risk.
- [prd.md](./prd.md) — WHAT: user story, Gherkin acceptance criteria.
- [tech-docs.md](./tech-docs.md) — HOW: root cause, the bounded-concurrency/retry mechanism, the
  regression-test-mandate adjudication for a probabilistic failure mode.
- [delivery.md](./delivery.md) — DO: phased, gated delivery checklist.
- [learnings.md](./learnings.md) — Knowledge Capture running log for this plan's own execution.

## Delivery Mode

`worktree-to-pr` (the repo default).
