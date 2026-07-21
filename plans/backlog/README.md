# Backlog Plans

Full, ready-to-execute plans waiting to start. A plan lands here only when it has been **promoted
from a two-pager** in [`../ideas/`](../ideas/README.md) — i.e. its open questions have shrunk to ones
that genuinely need a full plan's depth to answer.

## Planned Projects

The seven `ayokoding-learning-path-*` plans below deliver one programme. Plans `01`-`05` are the
**five-way split** of the retired
[`shared-course-library-and-learning-paths`](../done/2026-07-21__shared-course-library-and-learning-paths/README.md)
plan and cover the **`careers/`** category only; plans `06` and `07` add the **`skills/`** category,
which that retired plan never scoped. Their `NN-` prefix **is the execution sequence**, and it
encodes a three-wave dependency DAG: Wave 1 (`01`, `02`) starts immediately and in parallel; Wave 2
(`03`, `04`, `06`) needs both Wave 1 plans merged; Wave 3 (`05`, `07`) needs its own Wave 2
predecessor merged. Each is a separate `worktree-to-pr` delivery with its own PR.

The two category branches are independent after Wave 1 — nothing in `05` waits on `06`/`07`, and
nothing in `07` waits on `05`. The one cross-branch edge is `07`'s dependency on `06`, which is
**soft overall and hard at four wave gates**: ten of the ERP courses have no accounting prerequisite
at all and are authorable while `06` is still in flight.

- [ayokoding-learning-path-01-url-restructure](./ayokoding-learning-path-01-url-restructure/README.md)
  — **Wave 1.** Removes the `/c/` content namespace, then resolves everything under `/en/learn` to
  exactly three buckets (`paths/`,
  `courses/`, `legacy/`), re-homes 37 existing course slugs into the flat `courses/` namespace, and
  ships the per-course 308 redirect table.
- [ayokoding-learning-path-02-schema-and-prerequisite-dag](./ayokoding-learning-path-02-schema-and-prerequisite-dag/README.md)
  — **Wave 1.** The data layer: the `PathManifest` zod schema, the pure `course-paths` functional
  core, the course-prerequisite frontmatter contract, and custody of the 128-file `syllabus/` corpus.
- [ayokoding-learning-path-03-navigation-ui](./ayokoding-learning-path-03-navigation-ui/README.md)
  — **Wave 2.** The UI design funnel and every rendered surface: path landings, path cards, the
  manifest repository, and the `?path=` prev/next/breadcrumb wiring.
- [ayokoding-learning-path-04-course-authoring](./ayokoding-learning-path-04-course-authoring/README.md)
  — **Wave 2.** Authors 90 of the 127 course bodies, band by band, each from its `syllabus/` spec,
  emitting a five-field band-completion signal the manifest plan consumes.
- [ayokoding-learning-path-05-manifests](./ayokoding-learning-path-05-manifests/README.md)
  — **Wave 3, terminal for `careers/`.** Owns every `careers/` `.yaml` manifest and every step that
  creates, appends to, reorders, or re-verifies one — the ownership invariant that breaks the
  authoring/manifest cycle.
- [ayokoding-learning-path-06-skills-accounting](./ayokoding-learning-path-06-skills-accounting/README.md)
  — **Wave 2.** The first `skills/` path: 20 accounting courses on an immediately-effective ramp that
  reaches a working ledger by course 3, then deliberately slows — because this domain's
  characteristic failure is **silent** (a trial balance still balances when revenue is recognised in
  the wrong period). Owns its own manifest.
- [ayokoding-learning-path-07-skills-erp](./ayokoding-learning-path-07-skills-erp/README.md)
  — **Wave 3, terminal for `skills/`.** 20 ERP courses. Depends on `06` one-directionally — no
  accounting course cites an ERP course — with the hard edge first biting at `record-to-report`,
  since subledger-to-GL posting is meaningless without a balanced ledger. Owns its own manifest.

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
