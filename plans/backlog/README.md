# Backlog Plans

Full, ready-to-execute plans waiting to start. A plan lands here only when it has been **promoted
from a two-pager** in [`../ideas/`](../ideas/README.md) — i.e. its open questions have shrunk to ones
that genuinely need a full plan's depth to answer.

## Planned Projects

The `ayokoding-learning-path-*` plans deliver one programme. Each plan is **self-contained**: the
shared programme decisions (the `R*`/`A*` ids) are folded into each plan's own `tech-docs.md` under a
`## Programme decisions` section, and each plan's README carries its scope, course count, gates, and
dependency edges. **Renumbered 2026-08-01** (see
[`plan-decision-integrity-hardening`](../ideas/q1-urgent-important/plan-decision-integrity-hardening.md)'s
retrofit rationale): plans `05` through `07` originally each delivered more than the 5-15-course
governance band allows (`04` alone scoped 90 courses; `05-manifests` scoped all four path manifests
at once; `06`/`07` scoped 24 and 30 courses respectively). Every one of them is now split along its
own natural theme/stage boundaries, and every resulting plan carries a hard `blockedBy` on
[`vercel-function-cost-reduction`](../done/2026-08-02__vercel-function-cost-reduction/README.md) (treated
as already merged), since it rewrites the same `apps/ayokoding-www` root layout/middleware every one
of these plans lands content or manifests into. **Waves 1-2 have left this backlog**:
`01-url-restructure`, `02-schema-and-prerequisite-dag`, `03-navigation-ui`, and
[`04-course-authoring`](../done/2026-08-02__ayokoding-learning-path-04-course-authoring/README.md)
are done; 04 delivered its 21-course retained scope (a documented exception to the 5-15 rule — real
execution history, not new backlog scoping).

**Course-authoring backlog** (the remaining 55 of `04`'s original Bands 3-9 + course-surgery
contracts; Plan 04's retained baseline and [Plan 05](../done/2026-08-04__ayokoding-learning-path-05-course-authoring-platform-and-concurrency/README.md)
are complete; Plan 05's terminal delivery chain is [PR #133](https://github.com/wahidyankf/ose-public/pull/133),
reverted by direct-push commit [`919863f07`](https://github.com/wahidyankf/ose-public/commit/919863f07d8b51f9043ead5f6735f3759f6a2d49)
the same day, restored by [PR #136](https://github.com/wahidyankf/ose-public/pull/136); its downstream
signals require verifying PR #136 is merged, not merely that PR #133 was, since `gh pr view 133`
permanently reports `MERGED` regardless of the revert):

- [ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness](./ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness/README.md)
  — 15 courses (old Band 5 + the three course-surgery scope contracts): software architecture,
  distributed systems, and the AI/agent-harness cluster.
- [ayokoding-learning-path-07-course-authoring-low-level-systems](./ayokoding-learning-path-07-course-authoring-low-level-systems/README.md)
  — 7 courses (old Band 6, first half): C/C++/Rust, Linux/Windows OS, systems programming.
- [ayokoding-learning-path-08-course-authoring-security-and-ops](./ayokoding-learning-path-08-course-authoring-security-and-ops/README.md)
  — 11 courses (old Band 7): security, SRE, platform engineering, governance.
- [ayokoding-learning-path-09-course-authoring-interview-technique](./ayokoding-learning-path-09-course-authoring-interview-technique/README.md)
  — 5 courses (old Band 9): coding/system-design/behavioral interview prep + the interview capstone.
- [ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own](./ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own/README.md)
  — 9 courses (old Band 6, second half; `blockedBy 05, 06`): JVM languages, type systems, compilers,
  and the build-your-own-{git,database,raft} cluster.
- [ayokoding-learning-path-11-course-authoring-capstones](./ayokoding-learning-path-11-course-authoring-capstones/README.md)
  — 8 courses (old Band 8; `blockedBy 05, 06, 08`, the most dependency-heavy successor plan): the
  remaining cross-band synthesis capstones.

**Careers manifests** (splits old `05-manifests`; Plan 04's retained baseline is complete; needs the
`05`-`11` band-completion signals, `blockedBy` those plans as each lands):

- [ayokoding-learning-path-12-careers-se-manifests](./ayokoding-learning-path-12-careers-se-manifests/README.md)
  — the three `software-engineer`-role manifests (`interview-ready`, `immediately-effective`,
  `fundamentally-strong`) — grouped together because the no-forked-body and Band-9 checks bind
  across exactly these three.
- [ayokoding-learning-path-13-careers-ai-manifest](./ayokoding-learning-path-13-careers-ai-manifest/README.md)
  — the `immediately-effective/ai-engineer` manifest alone (a structurally independent growth track).

**Skills — accounting** (splits old `06-skills-accounting`'s 24 courses; strict sequential chain):

- [ayokoding-learning-path-14-skills-accounting-foundations](./ayokoding-learning-path-14-skills-accounting-foundations/README.md)
  — 11 courses (#1-11): foundations through the transactional/cost-accounting cycle.
- [ayokoding-learning-path-15-skills-accounting-enterprise-reporting](./ayokoding-learning-path-15-skills-accounting-enterprise-reporting/README.md)
  — 8 courses (#12-19, `blockedBy 14`): reporting, consolidation, architecture —
  `conventional-accounting` terminates here.
- [ayokoding-learning-path-16-skills-accounting-sharia-extension](./ayokoding-learning-path-16-skills-accounting-sharia-extension/README.md)
  — 5 courses (#20-24, `blockedBy 15`): the Sharia-specific extension — `sharia-accounting`
  terminates here.

**Skills — ERP** (splits old `07-skills-erp`'s 30 courses):

- [ayokoding-learning-path-17-skills-erp-foundations](./ayokoding-learning-path-17-skills-erp-foundations/README.md)
  — 15 courses (Stage A): both `conventional-erp` and `sharia-erp` publish here — a genuine,
  deployable checkpoint.
- [ayokoding-learning-path-18-skills-erp-enterprise-depth](./ayokoding-learning-path-18-skills-erp-enterprise-depth/README.md)
  — 15 courses (Stage B + C merged, `blockedBy 17`; soft-overall/hard-at-two-gates on `15`/`16` at
  stage granularity): conventional enterprise depth, then the Sharia-compliant design stage.

**Cross-repo consolidation** (direct-authored on maintainer request 2026-08-06, not promoted from a
two-pager — the problem statement and scope arrived fully formed, so the two-pager stage would have
added no decision value):

- [beaver-nest-repo-consolidation](./beaver-nest-repo-consolidation/README.md) — fold the BeaverNest
  product into `ose-public` as `apps/beavernest-be` / `apps/beavernest-app-web`, sweep four-repo
  terminology to three across `ose-public`, `ose-primer`, and `ose-private`, and archive
  `github.com/wahidyankf/beaver-nest`. Hard `blockedBy`
  [`sdlc-gate-registry-enforcement`](../in-progress/sdlc-gate-registry-enforcement/README.md), which
  scopes all four repos and needs `beaver-nest` live and writable.

**Demoted to two-pagers 2026-08-05**: every standalone plan that once sat here — the Ruff config, the
bulk-link concurrency fix, merge-queue adoption, the `ayokoding-www` cost reduction, the
`reuseExistingServer` audit, the Vitest glob guard, the app-shell tap targets, the Vercel steady-state
grading, and plan-decision-integrity hardening — was reduced to a single-file idea brief in
[`../ideas/`](../ideas/README.md).

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
