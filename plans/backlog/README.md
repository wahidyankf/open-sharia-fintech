# Backlog Plans

Full, ready-to-execute plans waiting to start. A plan lands here only when it has been **promoted
from a two-pager** in [`../ideas/`](../ideas/README.md) — i.e. its open questions have shrunk to ones
that genuinely need a full plan's depth to answer.

## Start here 🧭

This is the delivery queue, not the best first stop for learning what OSE is. If you are exploring
the product or setting up a checkout, begin with the [repository README](../../README.md) and
[documentation hub](../../docs/README.md). Come back here when you need to understand a proposed
piece of work: open its README for the why, scope, and dependencies, then use `delivery.md` for the
step-by-step execution record.

## Planned Projects

- [rewrite-rhino-cli-to-fsharp](./rewrite-rhino-cli-to-fsharp/README.md) — replace the Rust
  `rhino-cli` with a behavior-equivalent F# implementation across all 13 namespaces and 525 Gherkin
  scenarios, namespace by namespace behind a dispatch shim, then retire the Rust crate and tear down
  the Rust CI surface. Lands in both `ose-public` and `ose-private`. Authored directly at maintainer
  request rather than promoted from a two-pager. Carries **no kill gate** — the rewrite is the
  decision, and the nine-row before/after benchmark is a record rather than a gate. Thirteen phases,
  six waves, roughly 71 implementation PRs at one feature file per PR.

Everything else lives as a two-pager idea brief in [`../ideas/`](../ideas/README.md), sorted into
Eisenhower quadrants. Promote one here when it is ripe — when its open questions have shrunk to ones
only a full plan can answer.

Two waves emptied this queue before the entry above landed:

- **Demoted to two-pagers 2026-08-05** — the Ruff config, the bulk-link concurrency fix, merge-queue
  adoption, the `ayokoding-www` cost reduction, the `reuseExistingServer` audit, the Vitest glob
  guard, the app-shell tap targets, the Vercel steady-state grading, and plan-decision-integrity
  hardening.
- **Demoted to two-pagers 2026-08-21** — the five governance follow-ups filed by
  [`repo-rules-sweep`](../done/2026-08-18__repo-rules-sweep/README.md) and
  [`update-harness-support`](../done/2026-08-20__update-harness-support/README.md):
  [oxlint-upgrade-and-lint-reproducibility](../ideas/q1-urgent-important/oxlint-upgrade-and-lint-reproducibility.md),
  [rhino-cli-governance-tooling-defects](../ideas/q1-urgent-important/rhino-cli-governance-tooling-defects.md),
  [file-naming-convention-rework](../ideas/q1-urgent-important/file-naming-convention-rework.md),
  [harness-mirror-and-test-isolation-defects](../ideas/q1-urgent-important/harness-mirror-and-test-isolation-defects.md),
  and
  [declare-vite-peer-dependency](../ideas/q2-not-urgent-important/declare-vite-peer-dependency.md).

The `ayokoding-learning-path-*` programme, which once filled this queue, has completed: plans `01`
through `18` are archived in [`../done/`](../done/README.md).

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
