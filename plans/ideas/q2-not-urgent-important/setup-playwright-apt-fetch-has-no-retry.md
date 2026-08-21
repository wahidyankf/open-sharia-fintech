# `setup-playwright` fetches from a mirror with no retry and no step budget

One-line summary: the shared Playwright setup action shells out to `apt-get update` with no retry
and no step-level timeout, so one stalled Ubuntu mirror consumes the entire job budget and surfaces
as a bare cancellation with no named cause.

> Idea, filed 2026-08-21 while removing BeaverNest from this repo. It is the one surviving finding
> from the `ci-workflow-scope-and-build-resilience` backlog plan, whose other two workstreams
> (a `repo-config.yml` `paths:` filter on the BeaverNest workflow, and a seven-case F# assertion in
> `apps/beavernest-be`) died with the apps they described. That plan was deleted; this brief is
> what remains of it.

## Problem / context

`.github/actions/setup-playwright/action.yml`'s cache-hit branch runs `npx playwright install-deps`,
which shells out to `apt-get update` against `azure.archive.ubuntu.com`.

Observed: two consecutive runs (`32231836567`, job `96013835006`) were cancelled at their 35-minute
`timeout-minutes` while still inside that step, logging repeated `Ign:` lines and then 32 minutes of
silence. Nothing in the failure named the fetch. The only way to identify the step was the teardown
line `Terminate orphan process: pid (4377) (npm exec playwright install-deps)`.

The shape of the defect: a transient upstream condition becomes a red check on an unrelated PR, and
the log offers no way to tell that from a real failure. The fetch has no retry, and its only budget
is the whole job's.

## Rough scope & non-goals

In scope: giving the fetch three properties —

1. **Retry with backoff.** Three attempts is the usual shape; the count matters less than that a
   single transient failure is not terminal.
2. **A step-level timeout smaller than the job's.** A stall must exhaust the step, not the job, or
   the failure surfaces as a bare cancellation.
3. **A message naming the fetch**, rather than a `RUN` line and a process id.

Out of scope: the cache-miss branch's own install path if it does not share the defect; adding a
merge queue; the GitHub-hosted runner image contents.

## Risks & open questions

- Does the cache-miss branch reach the same `apt-get update`, or only the cache-hit branch?
- Is a step-level `timeout-minutes` enough, or does the orphaned `npm exec` process need an explicit
  kill so the runner does not wait on it during teardown?
- How often does this actually fire? Two occurrences on one branch is the only recorded evidence;
  a cheap first move is to add the naming and the budget, and let the retry count follow real data.

## See also

- `.github/actions/setup-playwright/action.yml` — the action carrying the defect.
- [`ci-blocker-resolution`](../../../repo-governance/development/quality/ci-blocker-resolution.md) —
  the standing rule that CI failures are investigated at the root cause, never bypassed.
