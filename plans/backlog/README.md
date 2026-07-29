# Backlog Plans

Full, ready-to-execute plans waiting to start. A plan lands here only when it has been **promoted
from a two-pager** in [`../ideas/`](../ideas/README.md) — i.e. its open questions have shrunk to ones
that genuinely need a full plan's depth to answer.

## Planned Projects

The `ayokoding-learning-path-*` plans deliver one programme in three dependency waves. Each
plan is **self-contained**: the shared programme decisions (the `R*`/`A*` ids) are folded into each
plan's own `tech-docs.md` under a `## Programme decisions` section, and each plan's README carries its
scope, counts, gates, and local wave position. The three waves are: **Wave 1** — `01`, `02` (no
prerequisite); **Wave 2** — `03`, `04`, `06` (need both Wave 1 plans merged; `06` additionally
hard-depends on `03`'s renderer); **Wave 3** — `05`, `07` (each needs its own Wave 2 predecessor
merged). **Both Wave-1 plans have left this backlog**: `01-url-restructure` is
[complete](../done/2026-07-23__ayokoding-learning-path-01-url-restructure/README.md) and
`02-schema-and-prerequisite-dag` is
[complete](../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/README.md).
`03-navigation-ui` is
[complete](../done/2026-07-25__ayokoding-learning-path-03-navigation-ui/README.md). `04-course-authoring`
is now [in progress](../in-progress/ayokoding-learning-path-04-course-authoring/README.md).

- [ayokoding-learning-path-05-manifests](./ayokoding-learning-path-05-manifests/README.md)
  — **Wave 3, terminal for `careers/`.** Owns every `careers/` manifest and every step that touches
  one.
- [ayokoding-learning-path-06-skills-accounting](./ayokoding-learning-path-06-skills-accounting/README.md)
  — **Wave 2.** The `conventional-accounting` and `sharia-accounting` paths, their corpus and their
  manifests.
- [ayokoding-learning-path-07-skills-erp](./ayokoding-learning-path-07-skills-erp/README.md)
  — **Wave 3, terminal for `skills/`.** The `conventional-erp` and `sharia-erp` paths, their corpus
  and their manifests.

Standalone plans (outside the `ayokoding-learning-path-*` programme):

- [harden-ayokoding-www-fe-e2e-bulk-link-concurrency](./harden-ayokoding-www-fe-e2e-bulk-link-concurrency/README.md)
  — Bounds concurrency (and retries transient failures) in `ayokoding-www-fe-e2e`'s bulk-link-check
  helper, which currently fires every collected `href` at once.
- [merge-queue-adoption](./merge-queue-adoption/README.md)
  — Hardens merge-precondition (c) under concurrent integration; owns the merge-queue work deferred
  from `worktree-to-pr-hardening`.
- [ayokoding-www-cost-reduction](./ayokoding-www-cost-reduction/README.md)
  — Runtime-and-hosting cost reduction for `apps/ayokoding-www`: Pagefind migration, build-time
  Mermaid, `html-react-parser` removal, calculator lazy-load, Docker/trace narrowing, and a
  dependency modernization sweep bound to the repo's bump policy.
- [audit-e2e-reuse-existing-server-config](./audit-e2e-reuse-existing-server-config/README.md)
  — Audits whether `reuseExistingServer: true` (hardcoded unconditionally in six `*-e2e`
  `playwright.config.ts` files) risks silently reusing a stale, unrelated server, and applies a
  CI-conditional gate, doc caveat, or automated check depending on runner persistence.
- [vitest-glob-coverage-guard](./vitest-glob-coverage-guard/README.md)
  — Designs a durable, automated guard against test files landing outside every configured Vitest
  project's `include` glob, after an `ayokoding-www` regression test silently executed zero times
  due to exactly this gap.

Other candidate work lives as two-pager idea briefs in [`../ideas/`](../ideas/README.md); promote one
here when it is ripe.

## Instructions

**Idea Capture**: For ideas not ready for formal planning, write a two-pager in
[`../ideas/`](../ideas/README.md) — not here.

**Naming**: Plans in `backlog/` use NO date prefix — just the slug (e.g.,
`doc-command-existence-validation/`). A date prefix is applied only when a plan is archived to
`done/`, where it records the completion date.

When promoting a two-pager to a plan:

1. Create folder: `[project-identifier]/`
2. Add standard files: README.md, brd.md, prd.md, tech-docs.md, delivery.md — carrying the
   two-pager's problem, scope, and open questions forward
3. Add the plan to this list
4. Delete the two-pager from `../ideas/` and drop its line from `../ideas/README.md`
