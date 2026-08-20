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

The `ayokoding-learning-path-*` plans deliver one programme. Each plan is **self-contained**: the
shared programme decisions (the `R*`/`A*` ids) are folded into each plan's own `tech-docs.md` under a
`## Programme decisions` section, and each plan's README carries its scope, course count, gates, and
dependency edges. **Renumbered 2026-08-01** (see
[`plan-decision-integrity-hardening`](../ideas/q1-urgent-important/plan-decision-integrity-hardening.md)'s
retrofit rationale): plans `05` through `07` originally each delivered more than the 5-15-course
governance band allows (`04` alone scoped 90 courses; `05-manifests` scoped all four path manifests
at once; `06`/`07` scoped 24 and 30 courses respectively). Every resulting plan is now split along its
own natural theme/stage boundaries. **Waves 1-2 have left this backlog**:
`01-url-restructure`, `02-schema-and-prerequisite-dag`, `03-navigation-ui`, and
[`04-course-authoring`](../done/2026-08-02__ayokoding-learning-path-04-course-authoring/README.md)
are done; 04 delivered its 21-course retained scope (a documented exception to the 5-15 rule — real
execution history, not new backlog scoping). The remaining plans execute as one linear chain:
`05 → 06 → 07 → 09 → 10 → 11 → 12 → 13 → 14 → 15 → 16 → 17 → 18`. Each backlog plan has
exactly one direct prerequisite: its immediate predecessor. Each uses one full-slug worktree and one
content-only PR; local secret inspection, the pre-push gate, and the PR quality gate are required,
while a PR-review cycle is not.

**Course-authoring backlog** (the remaining 55 of `04`'s original Bands 3-9 + course-surgery
contracts; Plan 04's retained baseline and [Plan 05](../done/2026-08-04__ayokoding-learning-path-05-course-authoring-platform-and-concurrency/README.md)
are complete. Plan 05's archived folder on `origin/main` is the sole direct-predecessor proof that
Plan 06 needs):

**Careers manifests** (splits old `05-manifests`; Plan 04's retained baseline is complete):

**Skills — accounting** (splits old `06-skills-accounting`'s 24 courses; strict sequential chain):

— 8 courses (#12-19, follows plan 14): reporting, consolidation, architecture —
`conventional-accounting` terminates here.

— 5 courses (#20-24, follows plan 15): the Sharia-specific extension — `sharia-accounting`
terminates here.

**Demoted to two-pagers 2026-08-05**: every standalone plan that once sat here — the Ruff config, the
bulk-link concurrency fix, merge-queue adoption, the `ayokoding-www` cost reduction, the
`reuseExistingServer` audit, the Vitest glob guard, the app-shell tap targets, the Vercel steady-state
grading, and plan-decision-integrity hardening — was reduced to a single-file idea brief in
[`../ideas/`](../ideas/README.md).

**Governance follow-ups from `repo-rules-sweep`** (filed 2026-08-18 by that plan's Knowledge Capture
phase, which routes code-bearing learnings straight to a backlog plan rather than through a
two-pager — both arrived plan-ready, with the defect reproduced and the fix designed):

- [oxlint-upgrade-and-lint-reproducibility](./oxlint-upgrade-and-lint-reproducibility/README.md) —
  every lint target resolved `npx oxlint@latest` at run time, so oxlint 1.79.0 turned CI red on a
  branch that had passed two hours earlier without touching the file it named; `repo-rules-sweep`
  pinned 1.78.0 as a blocker fix, and this plan takes the upgrade deliberately, fixes the real
  `set-state-in-effect` defect it found, and enumerates what else resolves unpinned.
- [declare-vite-peer-dependency](./declare-vite-peer-dependency/README.md) — ten packages run their
  tests through a `vite*.config.*` that imports a `vite` none of them declares; it resolves only
  because npm auto-installs `vitest`'s peer and hoists it to the root. Declaring does not relocate it
  (tried, and CI failed identically), so this is manifest hygiene plus the gate that would have named
  the gap before an ose-private runner-cache change made it unreadable.
- [rhino-cli-governance-tooling-defects](./rhino-cli-governance-tooling-defects/README.md) — three
  `rhino-cli` tools that exit 0 while doing less than the caller believes: the vendor audit mis-pairs
  a wrapped inline code span, `harness bindings validate` hard-codes `.claude/agents` instead of
  reading the registry, and `readme-index rewrite-paths` matches by basename and reads only `.md`.
- [file-naming-convention-rework](./file-naming-convention-rework/README.md) — WS-B, declared but
  unspecified by `repo-rules-sweep` and now specified from its learnings: `file-naming.md` documents
  two of eleven enforced exemptions, its scope clause cannot be evaluated, and the ordinal convention
  contradicts its own worked example.

**Follow-ups from `update-harness-support`** (filed 2026-08-19 by that plan's Knowledge Capture
phase, which routes code-bearing learnings straight to a backlog plan — both arrived plan-ready, with
each defect observed and its fix designed):

- [harness-mirror-and-test-isolation-defects](./harness-mirror-and-test-isolation-defects/README.md)
  — three trees treated as uniform when they are not: OpenCode loads `.opencode/agents/README.md` as
  an agent named `README`, `rhino-cli`'s generate smoke tests share one process working directory so
  adding a test flakes a sibling, and 47 dangling anchors sat unmeasured under `.claude/skills/`
  while a prefix-keyed link exemption hid them.
- [ci-workflow-scope-and-build-resilience](./ci-workflow-scope-and-build-resilience/README.md) — a
  red check whose cause is outside the diff: `repo-config.yml` in an app workflow's `paths:` filter
  drags a full BeaverNest pipeline onto every governance PR, two CI network fetches retry never and
  are bounded only by the job timeout, and a seven-case assertion fails without naming its case.

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
