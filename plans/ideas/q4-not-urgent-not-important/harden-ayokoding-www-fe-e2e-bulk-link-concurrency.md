# Bound the Bulk-Link-Check Concurrency in `ayokoding-www-fe-e2e`

One-line summary: Two Playwright step files check every internal link on a page through an unbounded
`Promise.all` against a single local `next start` server, producing network-layer flakes in a
required CI gate; bound the in-flight request count and retry transport errors once.

> Demoted 2026-08-05 from a full `backlog/` plan to this two-pager. The full plan carried the
> standard five documents — `README.md`, `brd.md`, `prd.md`, `tech-docs.md`, `delivery.md` — plus a
> `learnings.md` stub: a business-impact analysis, a persona and user story with three Gherkin
> acceptance scenarios, a root-cause and mechanism design with batch-size arithmetic, and a four-phase
> `worktree-to-pr` delivery checklist with TDD substeps and phase gates. Nothing was executed.

## Problem / context

`ayokoding-www-fe-e2e:test:e2e` is a required affected-suite target: it runs on every PR touching
`ayokoding-www` or its e2e project, and on `main-ci`'s scheduled sweep. Two of its step files collect
every matching `href` on a rendered page and then fire one `page.request.get(href, { timeout: 10000 })`
per href inside an unbounded `Promise.all` — `apps/ayokoding-www-fe-e2e/src/steps/ia-navigation-revamp.steps.ts`
at lines 79 and 105 (every internal content link resolves without a redirect), and
`apps/ayokoding-www-fe-e2e/src/steps/course-rehome-redirects.steps.ts` at line 24 (every
course-catalog entry resolves, not 404). All of those requests go out at once against a single
`next start` Node process.

In one session's repeated runs of the full suite, this produced **4 distinct failures in 7 attempts**
— a _different_ single sub-test each time, and each a network-layer symptom rather than a functional
break: either a raw `ECONNRESET`, or a 10s client-side timeout where Playwright's own log showed the
server answered `200 OK` just after the client gave up. The same suite passed cleanly twice in that
session with zero code change, at an identical **578/759 passed, 181 skipped** both times — a
different-sub-test-each-run pattern that is inconsistent with a deterministic regression and
consistent with resource contention. The pages themselves resolve correctly; the check harness is
what is fragile. The failure mode compounds under this repo's own workflow, since `nx affected` runs
many projects' tasks in parallel on the same machine — exactly the condition that triggers it.

The cost is the usual known-flake tax: a genuinely green PR shows a red required check, contributors
learn to re-run until green rather than investigate, and a real regression in the same file is more
likely to be waved off as "probably the usual flake".

## Why now

The flakiness sits in a **required** gate, so every affected PR pays for it, and the erosion of trust
compounds the longer it runs. There is also a closing-the-loop argument: commit `c61084bca`
(unrelated to this idea and predating it) already parallelized `ia-navigation-revamp.steps.ts`'s link
checks specifically to fix a _sequential-timeout_ problem. This is the second half of that same
tension — sequential was too slow, unbounded-parallel is flaky — and leaving it half-solved means the
next person to touch these steps is likely to swing the pendulum back rather than land on bounded
concurrency.

## Prior art / precedents

- Commit `c61084bca` — the earlier change that parallelized the same nav link checks to fix
  sequential timeouts; the direct precedent this idea completes rather than reverts.
- [`ayokoding-www-e2e-parallel-load-flake`](./ayokoding-www-e2e-parallel-load-flake.md) — the sibling
  two-pager on the same suite flaking under full-suite parallel-worker load; same "concurrent actors
  on one machine" family, different (non-link-check) scenarios.
- [Regression Test Mandate](../../../repo-governance/development/quality/regression-test-mandate.md) —
  the governing rule for how a bug fix proves itself, and the source of the adjudication problem
  below for a probabilistic failure mode.
- [Nx Targets convention](../../../repo-governance/development/infra/nx-targets.md) — the
  dedicated-`*-e2e`-runner convention that settled the adjacent no-op-stub question raised alongside
  this one (the stubs are the documented pattern, not a gap).
- [`ayokoding-learning-path-02-schema-and-prerequisite-dag`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/README.md)
  — the Phase 5 integration verification whose Knowledge Capture surfaced this observation.

## Proposed direction (sketch)

Introduce one small shared helper for the "fetch every href, assert not 404" pattern, used by both
step files, that does three things. It **bounds concurrency** by processing hrefs in fixed-size
batches instead of firing all of them at once — a plain loop over slices with `Promise.all` per
batch, no external concurrency-limiter dependency for this narrow a need. It **retries once on a
transport-layer error only** — `ECONNRESET`-class errors and Playwright's own request-timeout error —
and never on an assertion failure such as a real 404. And it **preserves the existing assertion
verbatim**, so only how the request is issued changes, not what counts as pass or fail. Both step
files then replace their local `Promise.all(hrefs.map(...))` blocks with a call to it.

Batch size is the one real design number. The prior analysis put the starting point at 20: at 10s per
request, `ceil(37/8) = 5` batches would already blow the 30s per-test budget, and `batchSize >= 19` is
the minimum that clears it for the course-catalog call site's ~37 course bundles. That arithmetic is
proven only for that bounded call site — the nav call site has an unmeasured "dozens of internal
links" estimate, so the same formula must be re-run against its actual measured `hrefs.length` before
20 is assumed to hold there. If a timeout raise is ever needed as a fallback, it should be a
per-test override scoped to the affected scenarios, never the project-wide default, which would
silently loosen tolerance for the ~104 other unrelated scenarios in that Playwright project.

## Rough scope & non-goals

In scope: the request-issuing pattern in the two named step files (three call sites total); the shared
bounded-concurrency plus single-retry helper; and a deterministic test demonstrating the fix's
mechanism.

Out of scope:

- Any change to `ayokoding-www`'s actual routes, redirects, or content — this is test-harness
  hardening, not a product fix.
- Any other e2e project's step files, even where they share a superficially similar pattern; a
  separate item if one is found.
- What counts as a passing versus failing link resolution — only how reliably the check completes.
- Retries on genuine content assertions (title matches, redirect-chain checks) beyond the network
  transport layer.
- The adjacent `ayokoding-www:test:e2e` / `test:integration` no-op-stub question raised by the same
  Knowledge Capture — already adjudicated as the correct documented pattern, no work item.
- Broader e2e coverage gaps, tracked in
  [`ayokoding-www-e2e-coverage-gaps`](../q3-urgent-not-important/ayokoding-www-e2e-coverage-gaps.md), and the non-link-check
  parallel-load flakes tracked in
  [`ayokoding-www-e2e-parallel-load-flake`](./ayokoding-www-e2e-parallel-load-flake.md).

## Risks & open questions

- **Open — the nav call site's actual `hrefs.length` was never measured.** The batch size of 20 is
  arithmetically justified only for the ~37-href course-catalog site. If nav exceeds ~19 hrefs at the
  same 10s-per-request cost, 20 stops clearing the 30s per-test timeout there and either the batch
  size or a scoped timeout override needs revisiting for that site specifically.
- **Open — how to satisfy the Regression Test Mandate for a probabilistic failure.** A literal
  "fails before, passes after" test against live network timing is not reliably constructible. The
  proposed substitute is a deterministic unit test against the helper's own concurrency accounting,
  using a fake slow-responding request function and an injected transient failure — falsifiable in
  both directions without depending on real flakiness. Whether that satisfies the mandate as written
  is not settled.
- **Open — does bounding concurrency reintroduce the sequential-timeout problem `c61084bca` fixed?**
  The batch size has to be small enough to bound contention and large enough to keep the worst-case
  `ceil(hrefs.length / batchSize) * 10s` under the effective per-test timeout.
- **Risk — masking rather than fixing.** Raising the 10s client timeout on its own would only shift
  the threshold, not remove the contention; and a retry, even scoped to transport errors, could in
  principle paper over a genuine intermittent server fault.
- **Risk — scope creep.** The temptation is to sweep every superficially similar `Promise.all` in the
  wider e2e corpus; the value here comes from fixing the three known-flaky call sites first.
- **Open — is the pattern even still there?** This has sat unexecuted; the call sites were confirmed
  present at lines 79/105 and 24 as of this writing, but that needs re-verification before any work
  starts, and the item closes as moot if it has already been fixed by other means.

## What success looks like + promotion signal

Success: repeated runs of `ayokoding-www-fe-e2e:test:e2e` under representative concurrent load
produce zero network-layer failures (`ECONNRESET`, `apiRequestContext.get` timeout) across the two
step files, at the same pass count as a clean baseline, with no change in what the tests assert — a
genuine 404 or drained location must still fail exactly as before.

Promotion signal: promote to a full `backlog/` plan once the nav call site's actual `hrefs.length` is
measured and a fresh 2-3 run flake baseline confirms the pattern still reproduces. Those two numbers
are what turn the batch size from an estimate into a decision, and they are the only inputs the
design is currently missing. If the re-verification finds the unbounded pattern already gone, close
this as moot instead.
