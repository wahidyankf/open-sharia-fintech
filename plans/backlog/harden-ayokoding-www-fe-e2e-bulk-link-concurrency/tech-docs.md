# Technical Design: Harden `ayokoding-www-fe-e2e` Bulk-Link-Check Concurrency

## Root Cause

Both step files collect every matching `href` on a rendered page, then fire one
`page.request.get(href, { timeout: 10000 })` per href **inside an unbounded `Promise.all`** — every
request goes out at once, against a single `next start` Node process. Under concurrent system load
(this repo's own `nx affected` runs many projects' tasks in parallel, and CI/local machines are
frequently busy with other work), the server's response latency for some requests exceeds the fixed
10s client timeout even though the server does eventually respond (confirmed in one observed
failure: the Playwright error log showed the request ultimately received `200 OK` after the client
had already timed out). A second observed failure mode was a raw `ECONNRESET`, consistent with the
OS/Node socket layer under connection-count pressure rather than an application-level rejection.

Evidence this is load/concurrency-sensitive, not a logic bug: the exact same suite passed cleanly
twice in one session with **zero code change** (578/759 passed, 181 skipped, identical counts both
times) and failed 4 times with a **different single sub-test each time** — inconsistent with a
deterministic regression, consistent with resource contention.

## Mechanism

Introduce a small shared helper, e.g. `checkLinksResolve(page, hrefs, opts)` in a new
`apps/ayokoding-www-fe-e2e/src/steps/support/check-links-resolve.ts` (or co-located with existing
step support, matching this project's current file layout), that:

1. **Bounds concurrency** — process `hrefs` in fixed-size batches (e.g. 8 in flight at a time)
   instead of firing all of them simultaneously. No new dependency is required — a small
   `for` loop with `Array.prototype.slice` batches plus `Promise.all` per batch is sufficient; avoid
   pulling in an external concurrency-limiter library for this narrow a need.
2. **Retries once on a network-layer error only** — catch `ECONNRESET`-class errors and Playwright's
   own request-timeout error specifically, retry that single request once, and only then let the
   failure surface. Do **not** retry on an assertion failure (e.g., an actual 404) — retries apply to
   the _transport_ layer, not the _assertion_.
3. **Preserves the exact same assertion** — `expect(response.status(), <message>).not.toBe(404)` (or
   the equivalent per call site) stays unchanged; only how the request is issued changes.

Both `ia-navigation-revamp.steps.ts` (two call sites) and `course-rehome-redirects.steps.ts` (one
call site) replace their local `Promise.all(hrefs.map(...))` block with a call to the shared helper.

## Regression-Test-Mandate Adjudication

The [Regression Test Mandate](../../../repo-governance/development/quality/regression-test-mandate.md)
requires a reproducing test (failing before, passing after) for every bug fix. The failure mode here
is **probabilistic** (network timing under load), so a literal "fails before, passes after" unit test
against a live network condition is not reliably constructible. The falsifiable-both-ways form this
plan uses instead:

- **Before** (simulated): a test double that fires N concurrent slow-responding fake requests
  (N greater than the chosen batch size) demonstrates the _old_ unbounded pattern exceeds a bounded
  in-flight-request-count expectation — call it as a Vitest unit test against the helper's own
  concurrency accounting, not against `ayokoding-www`'s real server.
- **After**: the same test, run against the new helper, demonstrates in-flight requests never exceed
  the configured batch size, and that a single injected transient failure is retried once before
  surfacing.

This keeps the test deterministic (no reliance on real network flakiness to reproduce) while still
proving the fix's actual mechanism.

## Open Decisions (resolve at execution)

- **Batch size**: start at 8 (an arbitrary, moderate value); tune against three constraints
  together — the largest observed `hrefs.length` across both call sites (`ayokoding-www`'s nav has
  dozens of internal links; the course catalog has ~37 course bundles per the sibling
  `ayokoding-learning-path-02` plan's own corpus count), the existing 10s per-request timeout, and
  Playwright's own default 30000ms per-test timeout (`apps/ayokoding-www-fe-e2e/playwright.config.ts`
  sets no test-level override, so the default applies) — the batch size should be small enough to
  meaningfully bound concurrency but not so small it reintroduces the sequential-timeout problem
  `c61084bca` originally fixed, **and** its worst-case sequential total
  (`ceil(hrefs.length / batchSize) * 10s`) must stay under the effective per-test timeout, or the
  per-test timeout must be raised in the same change with the tradeoff stated.
