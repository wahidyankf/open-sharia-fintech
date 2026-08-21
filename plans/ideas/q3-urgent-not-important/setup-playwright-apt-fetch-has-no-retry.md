# `setup-playwright` fetches from a mirror with no retry and no step budget

One-line summary: the shared Playwright setup action shells out to `apt-get update` with no retry
and no step-level timeout, so one stalled Ubuntu mirror consumes the entire job budget and surfaces
as a bare cancellation with no named cause.

> Idea, filed 2026-08-21 while removing BeaverNest from this repo. It is the one surviving finding
> from the `ci-workflow-scope-and-build-resilience` backlog plan, whose other two workstreams
> (a `repo-config.yml` `paths:` filter on the BeaverNest workflow, and a seven-case F# assertion in
> `apps/beavernest-be`) died with the apps they described. That plan was deleted; this brief is
> what remains of it.
> Reclassified from Q2 to Q3 and reshaped to the eight-section template on 2026-08-21 by
> plan-ideas-grooming.

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

## Why now

The evidence is fresh and cheap to act on, and it will not resurface on its own: the finding was
salvaged from a plan that was deleted with the apps it described, so if it is not carried here it is
simply lost. It is also the second instance of one class this repo has now met twice — a shared
`.github/actions/setup-*` composite action fetching from the network with no retry — which makes the
naming-and-budget half worth doing before a third instance arrives. What it is **not** is a live
blocker: two occurrences on one branch is the whole recorded evidence.

## Prior art / precedents

- [ci-setup-rust-toolchain-retry](../q2-not-urgent-important/ci-setup-rust-toolchain-retry.md) — the
  sibling brief and the same class in `setup-rust`: a shared composite action whose network fetch has
  no retry, measured at seven flakes in one phase. Kept separate deliberately (each has its own
  distinct promotion gate), but whichever lands first should set the retry/backoff shape the other
  reuses.
- [`ci-blocker-resolution`](../../../repo-governance/development/quality/ci-blocker-resolution.md) —
  the standing rule that CI failures are investigated at the root cause, never bypassed; a re-run
  habit is the symptom this brief proposes to remove.
- **The existing MSRV pre-install step in `setup-rust`** — the in-repo precedent for hardening a
  composite setup action against an infrastructure race, complete with a comment explaining the
  failure it prevents. Same tree, same shape, already solved once.
  [action.yml](../../../.github/actions/setup-rust/action.yml)
- **Retry-with-backoff around network fetches in CI** — standard practice (`curl --retry`,
  `nick-fields/retry`, package-manager retry flags); this applies a well-known pattern one step
  further down than it currently reaches.
- **`apt-get -o Acquire::Retries`** — the package manager's own built-in retry knob, which may make
  a wrapper unnecessary for this call site specifically.

## Proposed direction (sketch)

Give the fetch three properties, in increasing order of confidence:

1. **A message naming the fetch**, rather than a `RUN` line and a process id. This is the cheapest
   and least contentious part, and it is what turns the next occurrence from a 32-minute mystery into
   a one-line diagnosis.
2. **A step-level timeout smaller than the job's.** A stall must exhaust the step, not the job, or
   the failure surfaces as a bare cancellation.
3. **Retry with backoff.** Three attempts is the usual shape; the count matters less than that a
   single transient failure is not terminal. Prefer `apt-get`'s own retry knob over a wrapper if it
   covers the observed failure.

## Rough scope & non-goals

In scope: `.github/actions/setup-playwright/action.yml`'s cache-hit branch and whichever of its other
branches reach the same `apt-get update`; the step-level budget; the naming; and the retry shape.

Out of scope (for now):

- The cache-miss branch's own install path, if it turns out not to share the defect.
- `setup-rust` and every other composite action — the class is real but each instance carries its own
  evidence and its own promotion gate.
- Retrying every network step in CI indiscriminately.
- Adding a merge queue, or changing the GitHub-hosted runner image contents.

## Risks & open questions

- **Does the cache-miss branch reach the same `apt-get update`, or only the cache-hit branch?** This
  determines whether the fix is one place or two, and has not been checked. (open)
- **Is a step-level `timeout-minutes` enough, or does the orphaned `npm exec` process need an
  explicit kill** so the runner does not wait on it during teardown? The teardown line is direct
  evidence the process outlived the step. (open)
- **How often does this actually fire?** Two occurrences on one branch is the only recorded evidence.
  A cheap first move is the naming and the budget, letting the retry count follow real data rather
  than a guess. (open)
- Retries hide genuine breakage: an `apt-get` failing for a real reason would now fail slower with a
  noisier log. Attempt count and delay need choosing with that in mind.
- Whether the fault is upstream-wide or specific to this runner environment is unknown; if the
  latter, a retry is a workaround rather than a fix, and that should be recorded honestly.

## What success looks like + promotion signal

Success: a stalled mirror exhausts a bounded step rather than the whole job, the failure log names
the fetch that stalled, and a single transient failure no longer reddens an unrelated PR — with the
existing behaviour otherwise unchanged, so a genuine `apt-get` failure still fails the job.

Promotion signal: the cache-miss-branch question is answered. One read of
`.github/actions/setup-playwright/action.yml` settles whether this is a one-line-per-branch change or
a restructure of the action, and that is the only input the design is currently missing. If
`ci-setup-rust-toolchain-retry` is promoted first, fold this in as a second call site of that plan's
chosen retry shape instead of promoting it separately.
