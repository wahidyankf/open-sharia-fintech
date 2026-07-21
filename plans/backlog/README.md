# Backlog Plans

Full, ready-to-execute plans waiting to start. A plan lands here only when it has been **promoted
from a two-pager** in [`../ideas/`](../ideas/README.md) — i.e. its open questions have shrunk to ones
that genuinely need a full plan's depth to answer.

## Planned Projects

The five `ayokoding-learning-path-*` plans below are **one five-way split** of the retired
[`shared-course-library-and-learning-paths`](../done/2026-07-21__shared-course-library-and-learning-paths/README.md)
plan. Their `NN-` prefix **is the execution sequence**, and it encodes a three-wave dependency DAG:
Wave 1 (`01`, `02`) starts immediately and in parallel; Wave 2 (`03`, `04`) needs both Wave 1 plans
merged; Wave 3 (`05`) needs both Wave 2 plans merged. Each is a separate `worktree-to-pr` delivery
with its own PR.

- [ayokoding-learning-path-01-url-restructure](./ayokoding-learning-path-01-url-restructure/README.md)
  — **Wave 1.** Resolves everything under `/en/c/learn` to exactly three buckets (`paths/`,
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
  — **Wave 3, terminal.** Owns every `.yaml` manifest and every step that creates, appends to,
  reorders, or re-verifies one — the ownership invariant that breaks the authoring/manifest cycle.

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
