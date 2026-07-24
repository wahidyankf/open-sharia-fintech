# Business Requirements: Harden `ayokoding-www-fe-e2e` Bulk-Link-Check Concurrency

## Problem Statement

`ayokoding-www-fe-e2e:test:e2e` is a required affected-suite target — it runs on every PR touching
`ayokoding-www` (or its e2e project) and on `main-ci`'s scheduled sweep. Two of its step files check
every internal/course link on a page by firing an unbounded `Promise.all` of concurrent HTTP
requests against a single local `next start` server. Observed this session: 4 failures in 7 runs,
each a distinct sub-test, each a network-layer symptom (not a functional break — the pages resolve
correctly when checked in isolation or on a less-loaded run).

## Impact

- **False-negative noise**: a genuinely green PR can show a red `test:e2e` check, forcing a
  re-run (or, worse, manual investigation that reaches the same "it's flaky" conclusion every time).
- **Erodes trust in the gate**: repeated unexplained flakiness in a _required_ CI check trains
  contributors to re-run-until-green rather than investigate — the opposite of what a quality gate
  should train.
- **Masks real regressions**: once a check is known-flaky, a genuine new failure in the same test
  file is more likely to be dismissed as "probably the usual flake" rather than investigated.
- **Compounds under this repo's own concurrency-heavy workflow**: `nx affected` and Nx's own
  parallel task execution mean this suite frequently runs alongside other CPU/network-heavy tasks —
  exactly the condition that triggers the flake.

## Success Metrics

- The two affected step files no longer fail with a network-layer error (`ECONNRESET`,
  `apiRequestContext.get` timeout) across repeated runs under representative concurrent load.
- No change to what the tests actually assert — page-resolution correctness must remain caught with
  the same strictness (a genuine 404/missing-content regression must still fail the test).

## Risks

- **Over-broadening scope**: this plan touches only the two identified step files' request-issuing
  pattern, not `ayokoding-www`'s product code, not other e2e projects' step files (even if they share
  a superficially similar pattern — a separate learning/backlog item if found).
- **Masking a real timeout with a longer client-side timeout alone**: raising `timeout: 10000` without
  also bounding concurrency would only shift the threshold, not fix the underlying contention: still
  in scope to consider, but the primary mechanism is bounding concurrency (see tech-docs.md).
