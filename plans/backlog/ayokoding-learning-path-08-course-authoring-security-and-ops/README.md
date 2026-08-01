# Learning Path — Course Authoring: Security, Ops & Delivery (Band 7)

## Delivery amendment — one final PR

All 11 courses remain within one plan branch and one delivery unit. The sole draft PR opens only in
Phase 7, after verification and Knowledge Capture, and carries the archival move, review cycle, CI,
merge, and deploy. Earlier cohort or delivery-boundary PR wording is superseded.

Author the **eleven course bodies** of Band 7 — "Security, ops, quality & delivery" — of the shared
course library: `it-and-application-security`, `offensive-security`, `defensive-security`,
`detection-engineering-and-siem-operations`, `vulnerability-management-and-assessment`,
`it-governance-grc`, `bare-metal-virtualization`, `self-managed-kubernetes-and-gitops`,
`platform-engineering-and-devex`, `site-reliability-engineering`, and
`analytics-and-experimentation`. **Eleven authored course bundles** in total, landing under
`apps/ayokoding-www/content/en/learn/courses/`.

This plan is a **further split of Band 7 out of**
[`ayokoding-learning-path-04-course-authoring`](../../in-progress/ayokoding-learning-path-04-course-authoring/README.md)
(itself Wave 2 of the five-way split of the closed
[`shared-course-library-and-learning-paths`](../../done/2026-07-21__shared-course-library-and-learning-paths/README.md)
plan). Band 7 held eleven course bodies as a former phase of plan 04's own delivery checklist — plan
04's delivery.md has since been trimmed and no longer carries that phase heading; the carve-out is now
documented in
[plan 04's own Successor plans table](../../in-progress/ayokoding-learning-path-04-course-authoring/README.md#successor-plans);
that phase's scope is carved out into this standalone folder so the band can be delivered, reviewed,
and archived independently of plan 04's remaining bands. **Eleven courses fits the repo's 5-15-course
plan-sizing rule as-is** — no further merging or splitting is needed within this band.

> **Cross-plan source of truth** — the authoritative per-course specs live in
> `plans/done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/`. Do
> not copy them; do not author from any other source. Every course body in this plan is authored
> **from** its
> [`syllabus/courses/<course-id>.md`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md)
> spec file — never from a fresh judgment call.
>
> **Provenance note — this plan authors while its immediate ancestor is still `in-progress`.** At the
> time this plan was authored, `ayokoding-learning-path-04-course-authoring` had not yet archived to
> `plans/done/YYYY-MM-DD__…`. Every cross-plan link to it in this plan's own files therefore currently
> points at
> `../../in-progress/ayokoding-learning-path-04-course-authoring/`. [delivery.md Phase 0](./delivery.md#phase-0-environment-setup--baseline)
> resolves the actual path at execution time (the same `git ls-files`-based pattern plan 04 itself used
> for its own upstream schema-plan reference) and re-points every reference in this plan's own files
> before authoring begins, rather than guessing a completion date now.

## The manifest ownership invariant (binding — read before anything else)

> **This plan never edits a manifest file.** Every file under
> `apps/ayokoding-www/src/features/course-paths/manifests/` is owned by
> [`ayokoding-learning-path-12-careers-se-manifests`](../ayokoding-learning-path-12-careers-se-manifests/README.md). A step
> in this plan that creates, appends to, reorders, or re-verifies a `.yaml` manifest is a **boundary
> violation**, not a convenience. This is the identical invariant plan 04 carries, reproduced here
> because this plan is now the one authoring Band 7's bodies.

When Band 7 lands, this plan records **one band-completion signal** in its own
[`delivery.md`](./delivery.md) and the manifest plan performs the growth. The signal is the entire
handoff contract; see [Band-completion signal contract](#band-completion-signal-contract) below.

```mermaid
%% Which artefacts this plan may write, and which it may only signal about.
%% Node SHAPE encodes ownership: rectangle = written here, hexagon = written by the manifest plan.
%% Edge STYLE encodes permission: solid = this plan writes it, dotted = signal only, never a write.
flowchart LR
    SPEC["syllabus/courses/&lt;id&gt;.md<br/>(read-only; owned by<br/>schema-and-prerequisite-dag)"]:::readonly
    BODY["courses/&lt;course-id&gt;/<br/>page bundle (11 bodies)<br/>WRITTEN HERE"]:::owned
    CAT["tech-docs Course Library<br/>Catalog rows (11)<br/>WRITTEN HERE"]:::owned
    SIG["Band-completion signal<br/>in this plan's delivery.md<br/>WRITTEN HERE"]:::owned
    MAN{{"manifests/**/*.yaml<br/>NEVER WRITTEN HERE"}}:::forbidden

    SPEC -->|"authored from"| BODY
    BODY -->|"recorded in"| CAT
    BODY -->|"band lands"| SIG
    SIG -.->|"notifies; the manifest plan<br/>performs every growth"| MAN

    classDef owned fill:#0173B2,stroke:#000000,color:#FFFFFF
    classDef readonly fill:#CA9161,stroke:#000000,color:#000000
    classDef forbidden fill:#DE8F05,stroke:#000000,color:#000000,stroke-width:4px,stroke-dasharray: 6 4
```

**Accessibility note.** Write permission is carried by node **shape** and by explicit label text
(`WRITTEN HERE` / `NEVER WRITTEN HERE` / `read-only`), and edge kind by **line style** plus edge
labels — never by fill colour alone. The forbidden node additionally carries a dashed thick border.
Fills use the verified accessible palette per the
[Color Accessibility Convention](../../../repo-governance/conventions/formatting/color-accessibility.md).

## Position in the split

```mermaid
%% This plan's position relative to plan 04 and the manifest plan.
%% Node SHAPE encodes role: rectangle = upstream baseline, stadium = this plan, hexagon = downstream composer.
flowchart LR
    P04(["course-authoring (plan 04)<br/>Band 1 + Band 2 +<br/>Phase 1 AI (21 bodies)"]):::upstream
    THIS(["THIS PLAN<br/>Band 7 only (11 bodies)"]):::this
    P12{{"manifests (plan 12)<br/>composes all bands' IDs"}}:::downstream
    VFR["vercel-function-cost-reduction<br/>(hard, new dependency)"]:::upstream

    P04 -->|"carves out Band 7;<br/>merged/archived first"| THIS
    VFR -->|"static-rendering fix must land<br/>before more content pages ship"| THIS
    THIS -->|"11 authored bodies<br/>band-completion signal"| P12

    classDef upstream fill:#0173B2,stroke:#000000,color:#FFFFFF
    classDef this fill:#DE8F05,stroke:#000000,color:#000000,stroke-width:4px
    classDef downstream fill:#029E73,stroke:#000000,color:#FFFFFF
```

**Accessibility note.** Role is carried by node **shape** (rectangle = upstream, stadium = this plan,
hexagon = downstream) and by explicit `THIS PLAN` label text; colour is redundant. Fills use the
verified accessible palette.

## Band-completion signal contract

The manifest plan cannot act on a vague signal. This plan's single band-completion signal, recorded
in [`delivery.md`](./delivery.md) at the close of Phase 2, MUST carry all five fields below, verbatim,
in a fenced `text` block:

| Field               | Content                                                                           |
| ------------------- | --------------------------------------------------------------------------------- |
| `BAND`              | `Band 7 — Security, ops, quality & delivery`                                      |
| `PLAN`              | `ayokoding-learning-path-08-course-authoring-security-and-ops`                    |
| `LANDED_COURSE_IDS` | all eleven course IDs, one per line, in this plan's own listing order             |
| `GROW_MANIFESTS`    | every manifest the manifest plan must grow, by **full path** under `<MANIFESTS>`  |
| `MERGED_COMMIT`     | the `origin/main` merge commit SHA of the delivery boundary that completes Band 7 |

`GROW_MANIFESTS` is the load-bearing field, and for this band it is fixed: derived by elimination from
plan 04's own routing notes (Band 9 grows two manifests; Bands 5 and 8 grow four), every other band,
including Band 7, defaults to three. **Band 7 grows exactly the three `software-engineer`-role
manifests**:

- `<MANIFESTS>careers/interview-ready/software-engineer.yaml`
- `<MANIFESTS>careers/immediately-effective/software-engineer.yaml`
- `<MANIFESTS>careers/fundamentally-strong/software-engineer.yaml`

The fourth manifest, `<MANIFESTS>careers/immediately-effective/ai-engineer.yaml`, is **not** grown by
this band — it grows only for Bands 5 and 8 (the AI/harness cluster and the capstones that assemble
it), neither of which is this plan's scope.

**Adaptation note — one signal covering two delivery-boundary PRs.** Unlike plan 04's smaller bands
(each landing as a single PR), this plan splits Band 7's eleven bodies into **two** delivery-boundary
PRs (a five-course cohort and a six-course cohort — see
[§Delivery Mode](#delivery-mode-worktree-to-pr) below), inheriting plan 04's own five-course cohort
cadence. The single band-completion signal is still recorded only **once**, at the close of Phase 2
(after both cohorts have merged): `LANDED_COURSE_IDS` lists all eleven IDs from both cohorts, and
`MERGED_COMMIT` names the **second** cohort's merge commit — the commit that completes the band. A
signal that names manifests loosely, splits into two partial signals, or omits `MERGED_COMMIT` is
incomplete and the receiving plan must reject it rather than guess.

## Delivery Mode: worktree-to-pr

`worktree-to-pr`, inherited from `ayokoding-learning-path-04-course-authoring` (tier-2 plan-field
precedence, same programme): work in
`worktrees/ayokoding-learning-path-08-course-authoring-security-and-ops/`, open a draft PR at each
**delivery boundary** named in
[delivery.md's `### Delivery Boundaries` table](./delivery.md#delivery-boundaries) against `main`
(Phase 0 opens none), run the PR-Review Maker→Fixer Cycle (3 sequential CI-gated cycles), then `[AI]`
merges automatically once the review and all quality gates are green — no `[HUMAN]` merge gate is
declared. `ayokoding-www` is deployed to `prod-ayokoding-www` after every merge.

**Inherited sequential-cohort cadence.** Following plan 04's 2026-07-31 execution amendment, courses
are authored, checked, and committed **one at a time**, but a draft PR opens only once a full cohort
is complete. Eleven courses split as **one five-course cohort (courses 1–5) plus one six-course
cohort (courses 6–11)** — the plan's own natural in-order split, not an arbitrary 5+5+1: courses 1–5
are the security-core cluster (`it-and-application-security` through
`vulnerability-management-and-assessment`, all consuming `security-essentials` and/or
`networking-essentials`, and `detection-engineering-and-siem-operations` directly extending
`defensive-security`), while courses 6–11 are the governance/ops/analytics cluster
(`it-governance-grc` through `analytics-and-experimentation`). Keeping the security cluster in one
cohort lets `defensive-security` and `detection-engineering-and-siem-operations` — whose distinctness
is a locked, cross-checked contract (DL-9/DD-12 below) — land inside the same review cycle.
[Judgment call — a 5+6 split was chosen over 5+5+1 because the eleventh course
(`analytics-and-experimentation`) has no natural third-cohort partner and a lone-course final PR adds
process overhead the ops/governance cluster does not need.]

## Depends-on

| Direction     | Plan (full folder name)                                                                                                                                           | Nature                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **blockedBy** | `ayokoding-learning-path-01-url-restructure`                                                                                                                      | **transitive hard** — via plan 04's own hard dependency; not independently re-verified here beyond plan 04's completion (see Phase 0)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **blockedBy** | `ayokoding-learning-path-02-schema-and-prerequisite-dag`                                                                                                          | **transitive hard** — via plan 04's own hard dependency; the `syllabus/courses/` specs this plan authors from are consumed the same way                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **blockedBy** | `ayokoding-learning-path-04-course-authoring`                                                                                                                     | **hard, baseline** — carves this band out of plan 04; Band 7 must not be authored twice                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| **blockedBy** | `vercel-function-cost-reduction`                                                                                                                                  | **hard, new** — see [§Why the cost-reduction dependency is hard](#why-the-cost-reduction-dependency-is-hard) below                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| _(sibling)_   | [`ayokoding-learning-path-05-course-authoring-platform-and-concurrency`](../ayokoding-learning-path-05-course-authoring-platform-and-concurrency/README.md)       | none — same programme, independent band scope, no shared file                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| _(sibling)_   | [`ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness`](../ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness/README.md) | none — same programme, independent band scope, no shared file                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| _(sibling)_   | [`ayokoding-learning-path-07-course-authoring-low-level-systems`](../ayokoding-learning-path-07-course-authoring-low-level-systems/README.md)                     | none — same programme, independent band scope, no shared file                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| _(sibling)_   | [`ayokoding-learning-path-09-course-authoring-interview-technique`](../ayokoding-learning-path-09-course-authoring-interview-technique/README.md)                 | none — same programme, independent band scope, no shared file                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **blocks**    | [`ayokoding-learning-path-11-course-authoring-capstones`](../ayokoding-learning-path-11-course-authoring-capstones/README.md)                                     | hard — its capstones `capstone-secure-service`, `capstone-build-your-own-pentest-engine`, `capstone-real-world-delivery`, `capstone-concurrency-and-systems`, and `capstone-lead-at-altitude` need this band's security/ops bodies as prerequisites. **Correction (2026-08-01)**: this row originally also named `capstone-data-pipeline`, following plan 04's general "Band 7 → Band 8" ordering-rationale note; `ayokoding-learning-path-11-course-authoring-capstones`'s own per-capstone dependency audit (direct read of `syllabus/courses/defensive-security.md` lines 368-395, the embedded `capstone-data-pipeline` spec) found its "Integrates topics" list names only SQL/Advanced-SQL/Backend-at-Scale/Data-Engineering/AI-Powered-Apps — no Band-7 topic — so `capstone-data-pipeline` is corrected out of this row and `capstone-real-world-delivery` + `capstone-concurrency-and-systems` (both confirmed by the same audit to need this band's `defensive-security`/`site-reliability-engineering`) are corrected in |
| **blocks**    | [`ayokoding-learning-path-12-careers-se-manifests`](../ayokoding-learning-path-12-careers-se-manifests/README.md)                                                 | hard — the three `software-engineer` manifests' `courseOrder` entries for these 11 IDs resolve only after this plan lands; consumes the band-completion signal                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |

### Why the cost-reduction dependency is hard

[`vercel-function-cost-reduction`](../../in-progress/vercel-function-cost-reduction/README.md) found
that `apps/ayokoding-www` prerenders **zero** of its ~2,068 content pages — every page view executes a
serverless function, none is CDN-cached — and that this is 65% of a metered-usage overrun that would
otherwise push the site's invoice above the flat $20/month Pro subscription. Landing eleven more
content pages **before** that fix ships would add eleven more always-dynamic, always-billed routes to
an already-overrun bill; landing them **after** the fix means they are served statically from day one,
at zero incremental function-invocation cost. This plan's business risk table
([brd.md](./brd.md#business-risks-and-mitigations)) restates this concretely.

**Concrete checkable signal** (from that plan's actual Phase 1 and Phase 3 changes, not a promise):

- Phase 1 (Cause A — the root layout's `await headers()` call) promotes
  `apps/ayokoding-www/src/app/[locale]/layout.tsx` to the app's root layout and **deletes**
  `apps/ayokoding-www/src/app/layout.tsx` entirely.
- Phase 3 (middleware elimination) **deletes** `apps/ayokoding-www/src/middleware.ts`.

Both are used as this plan's Phase 0 precondition check (see [delivery.md](./delivery.md#phase-0-environment-setup--baseline)):
`test ! -f apps/ayokoding-www/src/app/layout.tsx` and
`test ! -f apps/ayokoding-www/src/middleware.ts` both exiting 0.

## Rule-15 three-tester retest — exemption recorded

**Exempt, with reasons stated (not silently omitted)**, for the identical reasons plan 04 already
recorded for its own 90 bodies. The
[User-Facing Delivery Hardening Convention](../../../repo-governance/development/quality/user-facing-delivery-hardening.md)
Rule 15 mandates a near-end `web-exploratory-tester` + `web-usability-tester` + `web-design-tester`
round for **web-UI feature-change** plans. This plan is not one:

1. **It ships no screen and no component.** Every artefact is a markdown page bundle under
   `apps/ayokoding-www/content/en/learn/courses/`. The screens that render those pages (`PathRail`,
   `PathLanding`, `PathCard`, the paths hub) are owned by
   `ayokoding-learning-path-03-navigation-ui`, which already carried the mandatory retest.
2. **Its output surface is already covered by dedicated checkers.** Every authored body passes
   `apps-ayokoding-www-{by-example,annotated-concept,primer,general}-checker`,
   `apps-ayokoding-www-facts-checker`, and `apps-ayokoding-www-link-checker` — content-domain checkers
   strictly stronger, for prose correctness, than a generalist live-site UX triad.
3. **The retest would test the other plan's surface.** Pointing the triad at a course page exercises
   the navigation plan's rendering layer, producing findings this plan cannot act on.

**This is an exemption, not an omission**, and it is **narrow**: manual behavioural verification via
Playwright MCP is **still mandatory and still performed** (see [delivery.md](./delivery.md) Phase 4) —
a sample of this plan's own eleven authored course pages is opened at all three breakpoints in the
`en` content locale, with committed screenshot evidence. Only the three-tester triad is waived.

## Locale scope

This plan's content is authored **`en`-only**. Per plan 04's own Business-Scope Non-Goals (inherited),
an Indonesian mirror of the section content is explicitly **deferred**, and the deferral is a recorded
decision rather than an omission. Every manual-verification step in this plan exercises `en` and
states the deferral inline; fabricating an `id` walk-through for content that does not exist is
forbidden.

## Navigation

- [Business Requirements (brd.md)](./brd.md) — WHY these 11 bodies exist, who they serve, the business
  risks of authoring them, and what "done" means in business terms.
- [Product Requirements (prd.md)](./prd.md) — personas, user stories, the Gherkin acceptance criteria
  this plan owns, and product scope.
- [Technical Docs (tech-docs.md)](./tech-docs.md) — the authoring architecture, the reproduced
  cross-cutting design decisions that directly govern this band, the Course Library Catalog rows for
  all eleven bodies, and the manifest-ownership diagram.
- [Delivery Checklist (delivery.md)](./delivery.md) — the phased, executable checklist.
- [Learnings (learnings.md)](./learnings.md) — knowledge-capture running log.
- **Cross-plan**:
  [`syllabus/` source of truth](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md)
  ·
  [`syllabus/courses/` catalog](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md)
  · [`ayokoding-learning-path-04-course-authoring` (baseline)](../../in-progress/ayokoding-learning-path-04-course-authoring/README.md)
  · [`ayokoding-learning-path-12-careers-se-manifests` (downstream)](../ayokoding-learning-path-12-careers-se-manifests/README.md)
  · [`vercel-function-cost-reduction` (hard dependency)](../../in-progress/vercel-function-cost-reduction/README.md)

## Provenance

This plan carves **Phase 9 (Band 7 — Security, ops, quality & delivery, 11 bodies)** out of what was,
at authoring time, a phase of
[`ayokoding-learning-path-04-course-authoring`'s own delivery checklist](../../in-progress/ayokoding-learning-path-04-course-authoring/delivery.md).
Plan 04's `delivery.md` was concurrently trimmed and that phase heading no longer exists there; the
carve-out is now documented in
[plan 04's own Successor plans table](../../in-progress/ayokoding-learning-path-04-course-authoring/README.md#successor-plans),
which is itself Wave 2 of the five-way split of the closed
`plans/done/2026-07-21__shared-course-library-and-learning-paths/` plan. A sibling agent is trimming
plan 04's own `README.md`, `tech-docs.md`, and `delivery.md` concurrently with this plan's authoring to
remove Band 7's scope from its checklist and hand it to this folder instead — the two edits are
independent (this plan touches only its own new folder; plan 04's trim touches only plan 04's folder).

**The `DD-34` / `DD-35` / `DD-39` tokens are not this split's decisions**, exactly as plan 04 notes for
itself: they are FS-SE-inherited tokens carrying unrelated meanings in `syllabus/courses/**`, and travel
with `syllabus/` into the schema plan. `DD-36`, `DD-37`, and `DD-38` are unused. **Do not renumber to
close the apparent gap.**
