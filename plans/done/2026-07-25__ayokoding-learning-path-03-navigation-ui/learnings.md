<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: ayokoding-learning-path-03-navigation-ui

## Learning: `gh api -f body=@file` posts the literal string, not the file's contents

- **Context**: `pr-review-fixer`'s cycle-1 run (PR #95) posted GitHub PR review-thread replies by
  piping reply text through a temp file and `gh api ... -f body=@/path/to/file`.
- **Observation**: `-f` treats `@/path/to/file` as a literal string value — only `-F` (capital)
  triggers `gh`'s `@file`-read behavior. The cycle-1 run posted a reply whose body was literally the
  string `@/path/to/file.md` before this was caught and corrected.
- **Why it might generalize**: every future PR-review cycle re-derives this the hard way unless the
  agent's own instructions carry the caution — the endpoint docs describe the reply flow in detail
  but never called out the `-f`/`-F` distinction.
- **Terminal state**: routed inline to `.claude/agents/pr-review-fixer.md` (small, non-code,
  `.claude/agents/` home) — added a caution + correct example next to the reply-endpoint section.

## Learning: zsh arrays are 1-indexed — a bash-style `${arr[$i-1]}` loop silently misposts

- **Context**: `pr-review-fixer`'s cycle-1 run (PR #95) wrote an ad-hoc shell loop to post one reply
  per unresolved thread, indexing into a bash-style 0-indexed array.
- **Observation**: this environment's shell is zsh, whose arrays are 1-indexed by default — the
  bash-style off-by-one compensation posted a reply to the wrong thread. Caught only by re-reading
  posted comment bodies via GraphQL afterward.
- **Why it might generalize**: any future maker/fixer agent that writes a multi-item posting loop in
  this environment (replies, resolutions, batch comments) is exposed to the same silent
  misattribution.
- **Terminal state**: routed inline to `.claude/agents/pr-review-fixer.md` (small, non-code,
  `.claude/agents/` home) — added a caution next to the reply-loop guidance.

## Learning: a many-project `nx affected -t test:e2e` run produces transient contention flakes

- **Context**: Phase 6's full affected-suite run (base `e740ec998`, head `0834ac1b7`, 25 projects,
  `--parallel=2`) showed 5 e2e-target "failures" on the first pass: an evicted/stale build artifact
  under concurrent builds (`ose-www-fe-e2e`, `wahidyankf-www-fe-e2e`, `organiclever-www-fe-e2e`,
  `organiclever-app-web-e2e` — each passed 100% once rebuilt fresh and re-run in isolation), and one
  concurrent-request timeout (`ayokoding-www-fe-e2e`'s `course-rehome-redirects.feature`, which fires
  many parallel HTTP requests via `Promise.all` against a single local server — 3/3 browsers passed
  clean in isolation).
- **Observation**: none of these were regressions from this plan's diff — every failure disappeared
  when the same target was rebuilt fresh and re-run alone, outside the 25-project parallel load.
- **Why it might generalize**: every plan's Phase-6-equivalent step (`repo-governance/workflows/plan/
plan-execution.md` §2b) runs this same broad affected suite after a delivery-unit merge, and will
  keep re-hitting this same class of false failure without a documented "rebuild + isolate before
  calling it a regression" heuristic.
- **Terminal state**: routed inline to `repo-governance/workflows/plan/plan-execution.md` (small,
  non-code, workflow doc) — added a caution paragraph after the `test:e2e`/`test:integration` step.
  The specific `course-rehome-redirects.feature` concurrency pattern is already tracked by the
  existing backlog plan
  [`harden-ayokoding-www-fe-e2e-bulk-link-concurrency`](../../ideas/harden-ayokoding-www-fe-e2e-bulk-link-concurrency.md) —
  no duplicate filing needed.

## Discarded: `ose-app-web-e2e:test:e2e` "connection refused" when run standalone

- **Context**: the same Phase 6 affected run showed `ose-app-web-e2e:test:e2e` failing with
  `net::ERR_CONNECTION_REFUSED` at `localhost:3300`.
- **Observation**: this project's `playwright.config.ts` has no `webServer` block and its own
  `apps/ose-app-web-e2e/README.md` already documents the required manual pre-step (`nx dev
ose-app-web` and `nx dev ose-be` before running `test:e2e`) — this is intentional (the app needs a
  live F# backend, unlike its statically-buildable sibling `organiclever-app-web-e2e`), not an
  undocumented gap.
- **Terminal state**: discarded — the durable surface (the project's own README) already catches
  this; the litmus test fails since nothing here would be caught differently next time. Not a
  regression from this plan (PR #95 never touched `ose-app-web`).

<!--
Entry shape (append one block per generalizable learning, sanitized before it is written):

## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — see the secret/sensitivity gate)
- **Why it might generalize**: the litmus reasoning
- **Terminal state**: routed inline to <path> / filed as plans/backlog/<slug>/ / discarded — <reason>
-->
