# `ayokoding-www-fe-e2e` flakes under concurrent load

One-line summary: two Playwright step files check every internal link on a page through an unbounded
`Promise.all` against a single local `next start` server, producing network-layer flakes in a
required CI gate — and a third, non-link-check scenario flakes under the same shared-machine load
without that mechanism, so the aggregate e2e exit code conflates "isolated re-run passes" with a real
failure.

> Demoted 2026-08-05 from a full `backlog/` plan to this two-pager. The full plan carried the
> standard five documents — `README.md`, `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md` — plus a
> `learnings.md` stub: a business-impact analysis, a persona and user story with three Gherkin
> acceptance scenarios, a root-cause and mechanism design with batch-size arithmetic, and a four-phase
> `worktree-to-pr` delivery checklist with TDD substeps and phase gates. Nothing was executed.
> Merged with `ayokoding-www-e2e-parallel-load-flake.md` (surfaced 2026-07-23 during
> `ayokoding-learning-path-01-url-restructure` Phases 2 and 4) on 2026-08-21 by plan-ideas-grooming.
> Renamed from `harden-ayokoding-www-fe-e2e-bulk-link-concurrency.md` on 2026-08-21 by
> plan-ideas-grooming.

## Problem / context

`ayokoding-www-fe-e2e:test:e2e` is a required affected-suite target: it runs on every PR touching
`ayokoding-www` or its e2e project, and on the scheduled sweep.

**The dominant mechanism is unbounded fan-out in two step files.** Both collect every matching `href`
on a rendered page and fire one `page.request.get(href, { timeout: 10000 })` per href inside an
unbounded `Promise.all` — `ia-navigation-revamp.steps.ts` at lines 79 and 105 (every internal content
link resolves without a redirect) and `course-rehome-redirects.steps.ts` at line 24 (every
course-catalog entry resolves, not 404). All of those requests go out at once against a single
`next start` Node process. In one session's repeated full-suite runs this produced **4 distinct
failures in 7 attempts** — a _different_ single sub-test each time, each a network-layer symptom
rather than a functional break: either a raw `ECONNRESET`, or a 10s client-side timeout where
Playwright's own log showed the server answered `200 OK` just after the client gave up. The same
suite passed cleanly twice in that session with zero code change, at an identical **578/759 passed,
181 skipped** both times.

**A third scenario flakes without that mechanism**, which is why bounding concurrency is necessary but
may not be sufficient. During `ayokoding-learning-path-01-url-restructure` Phase 2, one scenario
flaked — `tools/cost-of-living-calculator.feature` "Minimum-role tab is dual currency", a different
browser each run, 0 failures isolated. In Phase 4, under heavier concurrent load (build + typecheck +
lint + test:unit on the same machine), the flake set widened to **3** scenarios:
`course-rehome-redirects.feature` "resolves every re-homed course" (chromium),
`ia-navigation-revamp.feature` "RSS feed item links use bare content URLs" (firefox), and the
cost-of-living calculator spec (firefox) — with 575 passed / 139 skipped otherwise. Re-running exactly
those three in isolation passed **9/9** (3 scenarios × chromium/firefox/webkit), and
`git diff origin/main HEAD` was empty, proving none was a regression. Two of those three are the
unbounded-`Promise.all` step files; the calculator scenario is not, and no mechanism has been
identified for it.

The cost is the usual known-flake tax: a genuinely green PR shows a red required check, contributors
learn to re-run until green rather than investigate, and a real regression in the same file is more
likely to be waved off as "probably the usual flake". The failure mode compounds under this repo's own
workflow, since `nx affected` runs many projects' tasks in parallel on the same machine — exactly the
condition that triggers it.

## Why now

The flakiness sits in a **required** gate, so every affected PR pays for it and the erosion of trust
compounds the longer it runs. There is also a closing-the-loop argument: commit `c61084bca`
(unrelated to this idea and predating it) already parallelized `ia-navigation-revamp.steps.ts`'s link
checks specifically to fix a _sequential-timeout_ problem. This is the second half of that same
tension — sequential was too slow, unbounded-parallel is flaky — and leaving it half-solved means the
next person to touch these steps is likely to swing the pendulum back rather than land on bounded
concurrency.

## Prior art / precedents

- Commit `c61084bca` — the earlier change that parallelized the same nav link checks to fix
  sequential timeouts; the direct precedent this idea completes rather than reverts.
- [Playwright test parallelism](https://playwright.dev/docs/test-parallel) and
  [retries](https://playwright.dev/docs/test-retries) — the upstream guidance on workers, isolation,
  and known-flake retry policy; the reference for whichever of the three root-cause buckets wins.
- [Regression Test Mandate](../../../repo-governance/development/quality/regression-test-mandate.md) —
  the governing rule for how a bug fix proves itself, and the source of the adjudication problem
  below for a probabilistic failure mode.
- [Nx Targets convention](../../../repo-governance/development/infra/nx-targets.md) — the
  dedicated-`*-e2e`-runner convention that settled the adjacent no-op-stub question raised alongside
  this one (the stubs are the documented pattern, not a gap).
- [`ayokoding-learning-path-02-schema-and-prerequisite-dag`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/README.md)
  — the Phase 5 integration verification whose Knowledge Capture surfaced the unbounded-fan-out half.
- The repo's own shared-machine contention family — the Nx warm-cache flake and the CI rustup
  concurrency race are the same "concurrent actors on one machine" shape, and are the closest
  precedent for the calculator scenario that bounded concurrency will not explain.

## Proposed direction (sketch)

- **Bound the fan-out behind one shared helper.** A single helper for the "fetch every href, assert
  not 404" pattern, used by both step files, that processes hrefs in fixed-size batches (a plain loop
  over slices with `Promise.all` per batch — no external concurrency-limiter dependency for this
  narrow a need), retries **once on a transport-layer error only** (`ECONNRESET`-class and
  Playwright's own request-timeout error, never an assertion failure such as a real 404), and
  preserves the existing assertion verbatim so only _how_ the request is issued changes.
- **Settle the batch size by measurement.** The prior analysis put the starting point at 20: at 10s
  per request, `ceil(37/8) = 5` batches would already blow the 30s per-test budget, and
  `batchSize >= 19` is the minimum that clears it for the course-catalog site's ~37 course bundles.
  That arithmetic is proven only for that bounded call site — the nav site has an unmeasured "dozens
  of internal links" estimate, so re-run the formula against its actual measured `hrefs.length` before
  assuming 20 holds there. If a timeout raise is ever needed as a fallback it must be a per-test
  override scoped to the affected scenarios, never the project-wide default, which would silently
  loosen tolerance for the ~104 other unrelated scenarios in that Playwright project.
- **Then classify the residual.** For whatever still flakes after bounding — the calculator scenario
  at minimum — decide the root-cause bucket by reproducing under controlled load: dev-server
  contention, Playwright worker isolation, or genuine app timing under CPU starvation. Each implies a
  different fix (its own dev-server instance, a bounded worker count, or a per-spec repair), and a
  scoped quarantine list is the acceptable interim if none is cheap.

## Rough scope & non-goals

In scope: the request-issuing pattern in the two named step files (three call sites total); the shared
bounded-concurrency plus single-retry helper; a deterministic test demonstrating the fix's mechanism;
the residual non-link-check flakes and the CI/Husky invocation that runs the suite under concurrent
load; and a retry or quarantine policy if one is adopted.

Out of scope (for now):

- Any change to `ayokoding-www`'s routes, redirects, or content — this is test-harness hardening, not
  a product fix — and no rewriting of the specs' assertions.
- Any other e2e project's step files, even where they share a superficially similar pattern.
- What counts as a passing versus failing link resolution — only how reliably the check completes.
- Retries on genuine content assertions (title matches, redirect-chain checks) beyond the transport
  layer.
- The adjacent `ayokoding-www:test:e2e` / `test:integration` no-op-stub question raised by the same
  Knowledge Capture — already adjudicated as the correct documented pattern, no work item.
- Broader e2e coverage gaps, tracked in
  [`ayokoding-www-e2e-coverage-gaps`](./ayokoding-www-e2e-coverage-gaps.md).
- Shared-machine CI contention that is not e2e-specific.

## Risks & open questions

- **The nav call site's actual `hrefs.length` was never measured.** The batch size of 20 is
  arithmetically justified only for the ~37-href course-catalog site. If nav exceeds ~19 hrefs at the
  same 10s-per-request cost, 20 stops clearing the 30s per-test timeout there. (open)
- **What explains the calculator scenario?** It carries no unbounded `Promise.all`, so bounding
  concurrency cannot be assumed to fix it, and no root-cause bucket has been assigned. (open)
- **How to satisfy the Regression Test Mandate for a probabilistic failure.** A literal "fails before,
  passes after" test against live network timing is not reliably constructible. The proposed
  substitute is a deterministic unit test against the helper's own concurrency accounting, using a
  fake slow-responding request function and an injected transient failure — falsifiable in both
  directions without depending on real flakiness. Whether that satisfies the mandate as written is not
  settled. (open)
- **Does bounding concurrency reintroduce the sequential-timeout problem `c61084bca` fixed?** The
  batch size has to be small enough to bound contention and large enough to keep the worst-case
  `ceil(hrefs.length / batchSize) * 10s` under the effective per-test timeout. (open)
- **Is the pattern even still there?** This has sat unexecuted; the call sites were confirmed present
  at lines 79/105 and 24 as of writing, and the flake evidence is from July and early August. Both
  need re-verification before any work starts, and the item closes as moot if already fixed. (open)
- **Risk — masking rather than fixing.** Raising the 10s client timeout alone would shift the
  threshold, not remove the contention; a retry, even scoped to transport errors, could in principle
  paper over a genuine intermittent server fault, and a blanket `retries: 1` certainly would.
- **Risk — scope creep.** The temptation is to sweep every superficially similar `Promise.all` in the
  wider e2e corpus; the value comes from fixing the three known-flaky call sites first.

## What success looks like + promotion signal

Success: repeated runs of `ayokoding-www-fe-e2e:test:e2e` under representative concurrent load produce
zero network-layer failures (`ECONNRESET`, `apiRequestContext.get` timeout) across the two step files,
at the same pass count as a clean baseline, with no change in what the tests assert — a genuine 404 or
drained location must still fail exactly as before — and the aggregate exit code becomes a trustworthy
signal, with any residual flake either fixed or on an explicit quarantine list rather than resolved by
per-run detective work.

Promotion signal: two numbers turn the design from estimate into decision — the nav call site's actual
measured `hrefs.length`, and a fresh 2-3 run flake baseline confirming the pattern still reproduces.
Promote once both exist. If the re-verification finds the unbounded pattern already gone and the suite
stable, close this as moot instead.
