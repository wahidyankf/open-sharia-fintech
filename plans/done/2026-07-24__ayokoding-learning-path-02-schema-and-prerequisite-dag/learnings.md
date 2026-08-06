<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: ayokoding-learning-path-02-schema-and-prerequisite-dag

## Learning: `ayokoding-www`'s `test:integration` and `test:e2e` are `echo` no-op stubs

- **Context**: authoring this plan's Testing and Verification Strategy and its per-phase quality
  gates, which originally claimed both tiers were "run to prove no regression".
- **Observation**: `apps/ayokoding-www/project.json` defines `test:integration` as
  `echo 'no-op: integration tier not used for this content app'` and `test:e2e` as
  `echo 'no-op: target not applicable for this project'`. Both always exit 0, so any acceptance
  clause resting on them is vacuous — a false green. This plan's one shipped-code change is a URL
  emitter (`content-url.ts`), and E2E is precisely the tier that would catch a cross-page URL
  regression.
- **Why it might generalize**: any plan citing an Nx target as evidence should read
  `project.json`'s `options.command` first; a target name is not proof that a target does anything.
- **Terminal state**: **resolved, no code gap** — Phase 5's affected-suite investigation confirmed
  `ayokoding-www` already has real E2E coverage via the dedicated `ayokoding-www-fe-e2e` project
  (759 real Playwright tests, independently exercised multiple times this session), which is exactly
  the intended pattern documented in
  [`nx-targets.md`'s dedicated-`*-e2e`-runner convention](../../../repo-governance/development/infra/nx-targets.md#mandatory-targets-by-project-type)
  ("E2E tests live in dedicated `*-e2e` runner projects; non-e2e projects declare
  `test:e2e: echo`"). `ayokoding-www:test:e2e`/`test:integration` being no-op stubs is the
  _correct_, documented pattern, not a gap — the original "repo-wide half" framing above was based
  on an incomplete picture at authoring time. The plan-doc half (this plan's own mis-citation of the
  no-op targets as evidence) was already fixed inline (the "to prove no regression" framing was
  removed from `tech-docs.md`, `brd.md` and `delivery.md`). No backlog plan filed — there is nothing
  to fix.

## Learning: `ayokoding-www-fe-e2e`'s bulk-link-check scenarios flake under concurrent load

- **Context**: Phase 5's integration verification re-ran the full affected suite multiple times
  against integrated `main`.
- **Observation**: `ayokoding-www-fe-e2e:test:e2e` (759 tests) failed in 4 of 7 runs this session,
  each time a _different_ single sub-test, each a network-layer symptom (`ECONNRESET`, or a
  Playwright-side 10s timeout where the server's own response log shows `200 OK` arriving just
  after) inside `ia-navigation-revamp.steps.ts` / `course-rehome-redirects.steps.ts` — neither file
  touched by this plan's diff. Both files fire an **unbounded** `Promise.all` of concurrent
  `page.request.get()` calls against a single local `next start` server; a prior, unrelated commit
  (`c61084bca`) already parallelized one of them once before to fix a _sequential_-timeout problem,
  so this is the flip side of that same tension.
- **Why it might generalize**: a future contributor or plan will hit this exact same flake on this
  exact same suite, and a required/scheduled CI check flaking erodes trust in the gate and can mask
  a real regression next time. The system would catch this automatically once the check itself is
  hardened (bounded concurrency + single retry) — this passes the litmus test.
- **Terminal state**: **filed as backlog (code, mandatory)** —
  [`plans/ideas/harden-ayokoding-www-fe-e2e-bulk-link-concurrency.md`](../../ideas/q4-not-urgent-not-important/harden-ayokoding-www-fe-e2e-bulk-link-concurrency.md).
  NOT landed inline in this plan's PR — the fix touches test step files under `apps/`, a code home,
  per the code-routing rule.

<!--
Entry shape — append one block per generalizable learning, the moment it surfaces:

## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — see the secret/sensitivity gate)
- **Why it might generalize**: the litmus reasoning
- **Terminal state**: routed inline to <path> / filed as plans/backlog/<slug>/ / discarded — <reason>

If execution surfaces nothing generalizable, replace "None yet." above with:
`No generalizable learnings — <one-line reason>`
-->
