# Backlog Plans

Full, ready-to-execute plans waiting to start. A plan lands here only when it has been **promoted
from a two-pager** in [`../ideas/`](../ideas/README.md) — i.e. its open questions have shrunk to ones
that genuinely need a full plan's depth to answer.

## Planned Projects

The `ayokoding-learning-path-*` plans deliver one programme. Each plan is **self-contained**: the
shared programme decisions (the `R*`/`A*` ids) are folded into each plan's own `tech-docs.md` under a
`## Programme decisions` section, and each plan's README carries its scope, course count, gates, and
dependency edges. **Renumbered 2026-08-01** (see
[`plan-decision-integrity-hardening`](../in-progress/plan-decision-integrity-hardening/README.md)'s
retrofit rationale): plans `05` through `07` originally each delivered more than the 5-15-course
governance band allows (`04` alone scoped 90 courses; `05-manifests` scoped all four path manifests
at once; `06`/`07` scoped 24 and 30 courses respectively). Every one of them is now split along its
own natural theme/stage boundaries, and every resulting plan carries a hard `blockedBy` on
[`vercel-function-cost-reduction`](../in-progress/vercel-function-cost-reduction/README.md) (treated
as already merged), since it rewrites the same `apps/ayokoding-www` root layout/middleware every one
of these plans lands content or manifests into. **Waves 1-2 have left this backlog**:
`01-url-restructure`, `02-schema-and-prerequisite-dag`, and `03-navigation-ui` are done;
[`04-course-authoring`](../in-progress/ayokoding-learning-path-04-course-authoring/README.md) is
in-progress, trimmed to its 21 already-merged/in-flight courses (a documented exception to the
5-15 rule — real execution history, not new backlog scoping).

**Course-authoring remainder** (splits `04`'s original Bands 3-9 + course-surgery contracts; 69
courses total, `blockedBy 04`):

- [ayokoding-learning-path-05-course-authoring-platform-and-concurrency](./ayokoding-learning-path-05-course-authoring-platform-and-concurrency/README.md)
  — 14 courses (old Band 3 + Band 4 merged): mobile/desktop platforms paired with their language
  primers, plus the two concurrency languages.
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

**Careers manifests** (splits old `05-manifests`; needs all of `04`-`11` merged, `blockedBy` each as
its band-completion signal lands):

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
- [ayokoding-www-app-shell-tap-targets](./ayokoding-www-app-shell-tap-targets/README.md)
  — Fixes two shared `ayokoding-www` app-shell tap targets (the header's "Learn"/"Tools" nav links
  and the footer's "MIT" license link) measuring below the WCAG 2.5.8 24x24 CSS px minimum,
  deferred out of `ayokoding-www-ai-benchmark-responsive-overhaul`'s scope (Rule-15 `EWT-005`).
- [vercel-cost-steady-state-verification](./vercel-cost-steady-state-verification/README.md)
  — Grades whether [`vercel-function-cost-reduction`](../in-progress/vercel-function-cost-reduction/README.md)
  held its $30 invoice ceiling and hit its $20 target, once a full clean billing cycle has closed. Split out of that
  plan because the grading is calendar-gated (**earliest 2026-09-26**) while the engineering finishes
  in days. Hard `blockedBy` that plan; single-file structure.

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
