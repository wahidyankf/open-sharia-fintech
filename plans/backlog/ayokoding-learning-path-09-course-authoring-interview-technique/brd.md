# Business Requirements — Course Authoring: Interview-Technique Courses (Band 9)

## Business Goal & Rationale

Ship the 5 interview-technique course bodies (`coding-interview`, `take-home-and-live-coding`,
`system-design-interview`, `behavioral-and-leadership-interviews`, `capstone-interview-loop`) that the
`careers/interview-ready/software-engineer` and `careers/fundamentally-strong/software-engineer` paths
need to be content-complete. These 5 bodies are the last piece of the shared **127-course** library's `[Repo-grounded]` authored
content that this plan's split family (see
[README.md §Provenance](./README.md#provenance)) is responsible for — every other band either already
authored or is being authored by a sibling plan.

**Why this matters now.** DD-27 (see
[tech-docs.md §Design Decisions Consumed](./tech-docs.md#design-decisions-consumed)) deliberately
deferred this band out of the `interview-ready` MVP gate so that authoring effort could go to the
fourth (AI-engineer) path first. That trade-off was correct at the time it was made, but it is not a
decision to defer forever: the `interview-ready` path's own north-star persona — an experienced
engineer re-entering the job market — is the path's entire reason for existing, and that path cannot
be content-complete without its own namesake band. Landing Band 9 closes the deferral DD-27 opened.

## Business Impact

- **Pain point closed**: without these 5 bodies, `careers/interview-ready/software-engineer`'s
  `courseOrder` references course IDs with no resolving bundle — every attempt to grow that manifest
  (or the `fundamentally-strong` manifest, which also carries this band) is blocked on content that
  does not yet exist.
- **Expected benefit**: once this plan's PR merges, the two manifests this band feeds
  (`careers/interview-ready/software-engineer.yaml` and `careers/fundamentally-strong/software-engineer.yaml`)
  can grow to include the interview-technique band, unblocking
  `ayokoding-learning-path-12-careers-se-manifests`'s own work on those two manifests.
- **Scope discipline preserved**: authoring these 5 bodies in their own plan — rather than folding them
  back into the parent plan's remaining scope — keeps this plan's PR small, reviewable in one pass, and
  independent of the other bands' own review cadence, consistent with the repo's stated preference for
  maximized parallelization across worktrees and PRs.

## Affected Roles

Solo-maintainer repo — no sign-off or stakeholder ceremony. The "roles" below are hats the maintainer
wears, or agents the maintainer delegates to:

- **Content author** (delegated to `apps-ayokoding-www-by-example-maker` and
  `apps-ayokoding-www-annotated-concept-maker`) — authors the 5 bodies from their settled
  `syllabus/courses/<course-id>.md` specs.
- **Content reviewer** (delegated to the PR-Review Maker→Fixer Cycle's discipline specialists) —
  reviews the authored content for governance conformance, documentation quality, and business-logic
  correctness (interview-rubric accuracy, prerequisite-chain correctness).
- **Deployer** (delegated to `apps-ayokoding-www-deployer`) — pushes the merged content to
  `prod-ayokoding-www`.
- **Downstream manifest author** (the maintainer, via
  [`ayokoding-learning-path-12-careers-se-manifests`](../ayokoding-learning-path-12-careers-se-manifests/README.md))
  — consumes this plan's band-completion signal to grow the two named manifests.

## Business-Level Success Metrics

1. **Observable fact**: `for s in coding-interview take-home-and-live-coding system-design-interview behavioral-and-leadership-interviews capstone-interview-loop; do test -d "apps/ayokoding-www/content/en/learn/courses/$s" || echo "ABSENT $s"; done | grep -c .` returns `0` after this plan's PR merges (returns `5` before). This is the plan's own terminal assertion — see [delivery.md](./delivery.md) Phase 6.
2. **Observable fact**: one band-completion signal, naming exactly two manifests
   (`careers/interview-ready/software-engineer.yaml`,
   `careers/fundamentally-strong/software-engineer.yaml`), is recorded in this plan's `delivery.md`
   with a real `MERGED_COMMIT` SHA — verifiable by reading the file after archival.
3. **Judgment call**: closing this deferral removes the one remaining content gap blocking the
   `interview-ready` path's own manifest from reaching content-completeness. No baseline cycle-time
   measurement exists for "how long a manifest stays blocked on a missing band," so this is stated
   qualitatively rather than as a fabricated duration metric.

## Business-Scope Non-Goals

- **No manifest growth.** This plan records a band-completion signal; it never edits a `.yaml`
  manifest itself. That is `ayokoding-learning-path-12-careers-se-manifests`'s work (for the two named
  manifests) — see the [manifest ownership invariant](./README.md#the-manifest-ownership-invariant--this-band-is-the-special-case).
- **No Indonesian (`id`) mirror.** Per the parent plan's own Business-Scope Non-Goals, this plan's
  content is `en`-only. An `id` mirror of these 5 courses is explicitly deferred, not silently dropped.
- **No re-scoping of the 5 course specs.** The concept coverage, worked-example volume, prerequisite
  chain, and register (refresh, not first-learn) for all 5 bodies are **settled** in the cross-plan
  `syllabus/courses/<course-id>.md` files this plan authors from. This plan does not re-decide them.
- **No changes to `ayokoding-learning-path-04-course-authoring`'s own files.** This plan reads that
  folder for cross-reference only; it never edits it.
- **No changes to `apps/ayokoding-www/src/features/course-paths/`** (application code) or any file
  under `apps/ayokoding-www/src/features/course-paths/manifests/` (manifest data). This plan is
  content-only.

## Business Risks & Mitigations

| Risk                                                                                                                                                                                | Mitigation                                                                                                                                                                                                                                                                 |
| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A band-completion signal names the wrong manifest count (three instead of two), causing the downstream manifest plan to wrongly grow `immediately-effective/software-engineer`      | The signal's `GROW_MANIFESTS` field is written verbatim from the parent plan's own binding contract (quoted in [README.md](./README.md#the-manifest-ownership-invariant--this-band-is-the-special-case)), and Phase 1's gate asserts exactly two manifest paths, not three |
| This plan starts before `vercel-function-cost-reduction`'s Phase 1–4 fixes land, adding 5 more dynamically-rendered (uncached) pages to a site already over its Vercel usage budget | Phase 0's hard precondition gate checks for that plan's concrete Phase 1–4 file-level changes before any authoring begins — see [tech-docs.md §The `vercel-function-cost-reduction` precondition](./tech-docs.md#the-vercel-function-cost-reduction-precondition)          |
| This plan starts before the parent plan's own Phase 0 baseline (toolchain, upstream verification) is established, or before its `<COURSES>` namespace exists                        | Phase 0 re-verifies the same upstream chain (plans 01 and 02 merged) directly, rather than trusting an unverified claim about the parent plan's state                                                                                                                      |
| A course body is authored in the wrong register (first-learn instead of refresh), teaching concepts from zero to an audience that already has them                                  | Each course's authoring step carries a grep-checkable acceptance clause (the "assumes ... professional experience" phrase in `overview.md`), inherited verbatim from the parent plan's own Phase 11                                                                        |
| Licensing exposure — a worked example or diagram copied from an interview-prep book, blog, or paid course                                                                           | The programme-wide `A8` licensing posture (describe, cite, link; never reproduce) applies here exactly as it did in the parent plan — see [tech-docs.md §Programme decisions consumed](./tech-docs.md#programme-decisions-consumed)                                        |
| The manifest ownership invariant is accidentally violated — a course-authoring step touches a `.yaml` manifest                                                                      | Every phase's gate includes a zero-assertion `git diff --name-only ... -- 'apps/ayokoding-www/src/features/course-paths/manifests/' \| grep -c .` check, inherited from the parent plan's own pattern                                                                      |
