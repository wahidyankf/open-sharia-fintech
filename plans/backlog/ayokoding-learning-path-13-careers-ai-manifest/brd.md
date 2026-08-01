# Business Requirements — Learning Path Manifest (AI-engineer)

## Business Goal

Turn a slice of the shared course library — plus its own six net-new AI-engineer-role courses and the
existing nine-course AI/harness cluster — into a single usable `careers/` product: the
**`careers/immediately-effective/ai-engineer`** path. This is a genuine **from-scratch**
AI-engineering path: it assumes **no** prior software-engineering competence, **includes** the shared
SWE-fundamentals prerequisite courses at the head of `courseOrder` rather than linking them out (no new
course body is authored for this — every included prerequisite is an existing library course), and
teaches **building** AI systems (models, agents, evals, inference serving), not driving them
(`agentic-coding` stays a separate, unrelated axis).

**This plan ships no course body and no rendering component.** It ships the composition layer: one
YAML manifest, one thin landing anchor, this plan's one-card slice of the paths-hub population, the
from-scratch smoothness audit, and the manifest's growth from its smoke-test-scoped starting
composition to its full, prerequisite-consistent walk of the AI/harness cluster.

## Why this plan is its own deliverable, split out from a four-manifest predecessor

The plan this split replaces authored all four `careers/` manifests, including this one, in a single
folder. This plan is split out because the AI-engineer manifest converges on a **distinct** endpoint
from the three software-engineer-role manifests, has its own independent nine-course growth track (the
AI/harness cluster), and is never part of any of the three cross-manifest checks that bind the
software-engineer manifests together (no-forked-body, Band-9 growth, the ownership-boundary sweep) —
see [the sibling plan's brd.md](../ayokoding-learning-path-12-careers-se-manifests/brd.md#why-this-plan-is-its-own-deliverable-split-out-from-a-four-manifest-predecessor)
for the shared reasoning behind the 3+1 shape.

## Why a manifest instead of a bespoke curriculum

The naive alternative — hand-author a bespoke AI-engineering curriculum with its own duplicated
SWE-fundamentals content — would fork material the shared library already teaches once, well, and
maintainably [Judgment call]. The manifest model avoids that:

- **A path is a lightweight ordered list of course IDs.** Including 11+ existing SWE-fundamentals
  courses at the head of `courseOrder` costs zero new authoring — it is a composition decision, not a
  content decision.
- **A fix propagates for free** to every path referencing the same shared course.
- **The prerequisite DAG keeps the path honest** — `courseOrder` is a valid topological entry,
  machine-checked at every phase gate.
- **Growth is additive.** As the AI/harness-cluster courses land (from two of the seven
  course-authoring successor plans), the manifest grows in place.

## Business Impact

**Pain points addressed**

- A reader with zero programming background who wants to become an AI engineer has no single, ordered,
  from-scratch path today — only a flat catalog with no entry point suited to their starting position.
- Without this plan, the six net-new AI-engineer-role courses and the nine-course AI/harness cluster
  have no composed, user-visible reading order.
- Without a single owner for this one manifest's mutation, its growth from two separate
  course-authoring successor plans' signals would either be skipped or duplicated.

**Expected benefits** (qualitative reasoning; no fabricated metrics)

- **One from-scratch AI-engineering product** assembled from mostly-existing library content plus six
  net-new courses — the marginal authoring cost is exactly those six courses, not a whole curriculum.
- **A checkable smoothness guarantee** — prerequisite-consistency turns "does this from-scratch order
  actually work for a beginner?" into a machine-verified invariant.
- **No silent truncation** — the growth phase closes the gap the smoke-test-scoped manifest
  deliberately leaves open at first publication, and the terminal gate asserts the full walk.
- **A clean seam with the sibling software-engineer-manifest plan** — because this plan's manifest and
  the sibling's three are separately owned, this plan's own growth pace (dependent on only two of the
  seven course-authoring successor plans) never blocks or is blocked by the sibling's growth pace
  (dependent on six of the seven).

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns this path's from-scratch arc and its curation.
- **Frontend engineer** — authors the one YAML data file.
- **Content author** (via `apps-ayokoding-www-general-maker`) — writes the one landing anchor and this
  plan's one-card hub slice.
- **Content reviewer** (via `apps-ayokoding-www-link-checker` and the facts checker).

Consuming agents: `apps-ayokoding-www-general-maker`, `web-researcher`, `apps-ayokoding-www-link-checker`,
`apps-ayokoding-www-deployer`, and the three live-site testers for the Rule-15 retest.

## Business-Level Success Metrics

Every metric below is an **observable check**, not a projected number.

- **The manifest is published, zero body duplication** (observable): `courseOrder` references courses
  by ID; the manifest passes integrity at every gate.
- **Prerequisite DAG consistency holds at every gate** (observable): `checkManifestIntegrity` +
  `checkPrerequisiteConsistency` exit 0.
- **The path is from-scratch, assumes-nothing-first** (observable): the manifest **includes** the
  SWE-fundamentals prerequisites at the head of `courseOrder`, so a reader with zero programming
  background can start at `courseOrder[0]` and finish.
- **The path walks, never links, the AI/harness cluster** (observable): all nine cluster courses appear
  in `courseOrder` once the growth phase completes.
- **Authoring priority #1 is honored** (observable, documentation-verified): this plan's Phase 1 begins
  immediately after the sibling plan's interview-ready delivery unit merges — before the sibling's
  other two manifests are composed.
- **No manifest ships permanently truncated** (observable): after the growth phase, all nine
  AI/harness-cluster course IDs are present, verified by an exact before/after entry-count delta, not a
  fabricated fixed total.
- **Progression smoothness verified** (observable): the from-scratch smoothness audit passes before
  archival.
- **No regressions** (observable): `npx nx run ayokoding-www:build`, the affected test tiers,
  `specs:behavior:coverage`, heading-hierarchy, markdownlint, and link validation all pass.

## Business-Scope Non-Goals

- **The three `software-engineer`-role manifests, their landings, and their hub cards.** Owned entirely
  by `ayokoding-learning-path-12-careers-se-manifests`.
- **The four-manifest "a shared course names every path" check and the terminal 127-course catalog
  assertion.** Both are the sibling plan's own final-phase responsibility — see
  [README §Recorded judgment calls, JC-5](./README.md#jc-5-this-plan-does-not-perform-its-own-four-manifest-check).
- **Authoring or editing any course body.** Owned by the seven course-authoring successor plans. This
  plan reads bodies and never writes one.
- **Building or changing any rendering component.** Owned by
  `ayokoding-learning-path-03-navigation-ui`.
- **Defining the `PathManifest` schema or the integrity gates.** Owned by
  `ayokoding-learning-path-02-schema-and-prerequisite-dag`.
- **Any URL, redirect, or IA change.** Owned by `ayokoding-learning-path-01-url-restructure`.
- **The `apps/ayokoding-www` root-layout/middleware rendering-mode work.** Owned by
  `vercel-function-cost-reduction`, treated here as a hard, already-merged precondition.
- **The `skills/` category's four manifests.** Disjoint category subtree, no shared file.
- **Adding an Indonesian mirror of the path content** — deferred; `id/belajar/` has zero courses and
  zero paths.
- **Path-level progress persistence, accounts, or bookmarking.**
- **A fifth `careers/` path, or renumbering the four-path `careers/` composition.** Locked.

## Business Risks and Mitigations

| Risk                                                                                                      | Mitigation                                                                                                                                                                                                                                                        |
| --------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| The manifest references a missing or renamed course ID.                                                   | `checkManifestIntegrity` verifies every `courseOrder` ID resolves to a bundle; runs at every gate.                                                                                                                                                                |
| The manifest orders a course before its declared prerequisite.                                            | `checkPrerequisiteConsistency` verifies a valid topological entry; a violation fails the gate.                                                                                                                                                                    |
| The manifest ships **narrowed** and is never grown.                                                       | A falsifiable before/after entry-count-delta check is written at publication time; a dedicated growth phase and terminal gate assert the full nine-course walk.                                                                                                   |
| This plan's growth is silently blocked because one of its two feeding course-authoring plans stalls.      | Growth is processed **as each of the two signals arrives**, independently — a stalled `06` does not block a landed `11`'s contribution being recorded, and vice versa; the final arc confirmation re-checks the complete composition regardless of arrival order. |
| The plan-12/plan-13 coupling is misread as circular.                                                      | Documented explicitly with a sequence diagram in both plans' READMEs; the two edges are stated as distinct nodes in the **sibling's own** phase sequence, never a single bidirectional edge between the two plans.                                                |
| This plan starts before the sibling's interview-ready phase has actually merged, producing a false start. | Phase 0's start condition is a literal `gh pr list --search ... --state merged` check, falsifiable both ways, not an assumption.                                                                                                                                  |
| Duplication creeps in — the path forks a shared SWE-fundamentals course body for its own framing.         | Framing is limited to an optional intro/outro callout (DL-5); the shared courses are referenced by ID, never copied.                                                                                                                                              |
| A course-authoring successor plan edits this manifest, or this plan edits a body.                         | The ownership invariant is stated in both this plan's and every course-authoring successor plan's own docs; this plan's own verification phase greps its manifest path's git history scope.                                                                       |
| Cross-plan `syllabus/` links break when the schema plan has already archived.                             | This plan's own pre-archival link-validation gate is scoped to its own folder.                                                                                                                                                                                    |
