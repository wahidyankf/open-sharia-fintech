# Business Requirements — Learning Path Course Authoring: Capstones (Band 8)

## Business Goal and Rationale

The shared course library's 127-course catalog reaches its complete, learner-facing shape only once
every capstone exists — a capstone is the artefact a learner actually points to as evidence of
capability, and every one of the three `software-engineer`-role manifests (`interview-ready`,
`immediately-effective`, `fundamentally-strong`) and the `ai-engineer` manifest end on one. Band 8's
eight capstones are the **synthesis layer**: each assembles two or more prior bands' course content
into one working, end-to-end system — a coding agent, a pentest engine, a secured HTTP service, a
data pipeline, a deployed-as-code system, two concurrency builds, and the whole-journey leadership
capstone that closes every path. Authoring them completes the library's most visible, most-referenced
content, and unblocks the two manifest-growth plans (`ayokoding-learning-path-12-careers-se-manifests`
and `ayokoding-learning-path-13-careers-ai-manifest`) that need this band's completion signal before
they can finish composing their respective manifests.

This plan exists as a standalone folder, rather than remaining inside
`ayokoding-learning-path-04-course-authoring`, because Band 8 is genuinely separable review-and-merge
work: it touches only its own eight `<COURSES><course-id>/` subtrees, shares no file with any other
band, and — per the repo's plan-sizing convention — a single 90-course plan was too large to execute
and review coherently. Splitting Band 8 out lets it be authored, reviewed, and merged on its own
schedule once its (numerous) prerequisites land, rather than blocking or being blocked by the other
eight bands' unrelated review cycles.

## Business Impact

**Pain point being solved.** Without this band, the library's `fundamentally-strong/software-engineer`
manifest has no whole-journey closing capstone (`capstone-lead-at-altitude`), the `ai-engineer`
manifest's harness-cluster spine has no assembling capstone
(`capstone-build-your-own-coding-agent`) to prove the five harness courses compose into a working
system, and the security/data/concurrency deepening tracks each lack the flagship milestone that
demonstrates their content transfers to a real build. Every downstream manifest-growth plan that
would otherwise reference these eight course IDs in a `courseOrder` currently has no body to resolve
against.

**Expected benefit.** Once this band lands, all four manifests can complete their `courseOrder`
composition (subject to their own remaining prerequisites), and the library's 127-course catalog
total becomes assertable in full — the manifest plans' own terminal handoff signal.

## Affected Roles

This is a solo-maintainer repository; "roles" here are hats the maintainer wears plus the AI agents
that consume this plan's artefacts, not external stakeholder sign-off:

- **The maintainer**, as the eventual reader/reviewer of the eight capstone course bodies and the PR
  reviews that gate their merge.
- **The course-authoring executor agents** (`apps-ayokoding-www-by-example-maker`,
  `apps-ayokoding-www-annotated-concept-maker`, their checkers and fixers, `web-researcher`) that
  produce and validate the content.
- **The two downstream manifest-growth plans**
  (`ayokoding-learning-path-12-careers-se-manifests`, `ayokoding-learning-path-13-careers-ai-manifest`),
  which consume this plan's band-completion signal as their own precondition.
- **A future learner** on any of the four `careers/` paths, who eventually reaches one of these eight
  capstones as a milestone.

## Business-Level Success Metrics

- **Observable fact**: `find apps/ayokoding-www/content/en/learn/courses -maxdepth 1 -type d -name 'capstone-*'`
  intersected with this plan's own 8-slug register returns all 8 present, zero absent, at plan
  completion (see [delivery.md](./delivery.md) Phase 0's baseline and the terminal handoff check).
- **Observable fact**: zero CRITICAL/HIGH/MEDIUM findings outstanding across the matching content
  checkers (`apps-ayokoding-www-by-example-checker`, `apps-ayokoding-www-annotated-concept-checker`,
  `apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker`) for all eight bodies at merge
  time.
- **Observable fact**: the band-completion signal recorded in `delivery.md` carries all five required
  content fields (`BAND`, `PLAN`, `LANDED_COURSE_IDS`, `GROW_MANIFESTS`) per the
  [Band-completion signal contract](./README.md#band-completion-signal-contract).
- _Judgment call_: completing this band is expected to meaningfully de-risk the two downstream
  manifest-growth plans' own scheduling, since they no longer need to track Band 8's authoring
  progress as an open dependency; no baseline cycle-time has been measured for this specific claim.

## Business-Scope Non-Goals

- **No manifest editing.** This plan never creates, appends to, reorders, or re-verifies any file
  under `apps/ayokoding-www/src/features/course-paths/manifests/`. That is the two downstream
  manifest-growth plans' exclusive property.
- **No re-ordering, re-scoping, or re-authoring of any other band.** This plan touches only its own
  eight `<COURSES>` subtrees.
- **No editing of any other plan folder.** Even where this plan finds a cross-plan documentation
  discrepancy (see [tech-docs.md §Confirmed per-capstone dependency map](./tech-docs.md#confirmed-per-capstone-dependency-map)),
  it flags the discrepancy for reconciliation rather than editing the other plan's files directly.
- **No Indonesian-locale mirror.** `en`-only, per plan 04's own Business-Scope Non-Goals (inherited).
- **No new UI, route, component, or redirect.** Every artefact is a markdown page bundle.
- **No re-litigating which courses belong in Band 8.** The eight-course list is fixed by plan 04's own
  DD-20 reconciliation ruling and this plan's own authoring brief; this plan authors exactly those
  eight, no more, no fewer.

## Business Risks and Mitigations

| Risk                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Mitigation                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **This plan has the most inbound cross-plan dependencies of any course-authoring successor plan (four sibling plans plus `vercel-function-cost-reduction`).** If any one of them slips, this plan cannot start any course that depends on it.                                                                                                                                                                                                                                  | Phase 0 checks each of the five hard preconditions independently and explicitly, rather than optimistically starting on a promise. A capstone whose specific prerequisite courses are not yet present is not started; the plan's own Pause Safety notes make this an explicit, auditable stop rather than a silent partial start.                                                                                                                                             |
| **A capstone authored before its true prerequisite content exists would cite courses that do not yet resolve**, producing a body whose cross-references are dead until the upstream plan lands.                                                                                                                                                                                                                                                                                | Every per-course authoring step's own acceptance clause includes a `test -d <COURSES>/<prerequisite-id>` check for each of that specific capstone's confirmed prerequisites, not just the plan-level precondition — see [delivery.md](./delivery.md)'s per-course convention.                                                                                                                                                                                                 |
| **Two cross-plan documentation discrepancies were found during verification** (`ayokoding-learning-path-05-...`'s own README misattributed a Band-4→capstone dependency to plan 10 instead of this plan; `ayokoding-learning-path-08-...`'s own README asserted a Band-7 dependency for `capstone-data-pipeline` that the actual syllabus spec does not support). Left unreconciled, either could have caused a future reader to misjudge this plan's true dependency surface. | Both are recorded explicitly, with citations, in [tech-docs.md §Confirmed per-capstone dependency map](./tech-docs.md#confirmed-per-capstone-dependency-map). **Both are now reconciled** — plan 05's and plan 08's own `README.md` files were each corrected in place (2026-08-01) to match this plan's audit findings; this plan's own dependency claims were, and remain, grounded in the syllabus specs directly, not in the other plans' original unverified assertions. |
| **`capstone-lead-at-altitude` is the single intra-band ordering constraint** — authoring it before `capstone-concurrency-and-systems` and `capstone-real-world-delivery` land would leave it referencing artefacts that do not exist.                                                                                                                                                                                                                                          | Cohort B is explicitly ordered (`capstone-concurrency-and-systems` and `capstone-real-world-delivery` first, `capstone-lead-at-altitude` last) and the per-course authoring convention's acceptance clause checks for both prior bodies before `capstone-lead-at-altitude`'s own authoring step begins.                                                                                                                                                                       |
| **`vercel-function-cost-reduction` changes the exact app/route tree this plan's 8 new pages render into.** Authoring against the pre-fix dynamic-rendering shape risks the new pages inheriting the cost problem that plan is actively fixing.                                                                                                                                                                                                                                 | Treated as a hard precondition with a concrete, falsifiable checkable signal (root layout promoted, middleware deleted, no server-side `searchParams` read remaining) rather than a soft "should probably land first" assumption — see [README.md §Why the cost-reduction dependency is hard](./README.md#why-the-cost-reduction-dependency-is-hard).                                                                                                                         |
| **Licensing exposure** (programme `A8`) — the security capstones in particular (`capstone-build-your-own-pentest-engine`, `capstone-secure-service`) touch offensive-security material where copied exploit code or lifted vendor documentation would be a real hazard.                                                                                                                                                                                                        | The same `A8` licensing discipline plan 04 established binds here unchanged: describe, cite, and link; never reproduce. Every capstone's worked code is authored originally, and the pentest capstone's own syllabus spec already states its own hard authorization/scope rule as non-negotiable — see [tech-docs.md](./tech-docs.md).                                                                                                                                        |
