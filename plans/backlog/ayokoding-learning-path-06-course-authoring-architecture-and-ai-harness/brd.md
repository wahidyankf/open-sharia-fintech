# Business Requirements — Course Authoring: Architecture, Distributed & AI/Harness (Band 5)

## Business Goal

Fill the shared course library with **Band 5's 15 course bodies** — the architecture, distributed
systems, and complete AI/harness-engineering material — and lock the three **course-surgery scope
contracts** that constrain how those bodies are authored. Without this band, the library has no
architecture depth, no distributed-systems depth, and no AI/harness-engineering cluster at all: the
fourth path (`careers/immediately-effective/ai-engineer`) is stuck on its six-course smoke-test
spine, and every path that reaches architecture material hits a gap.

Concretely, this plan authors:

- **5 architecture-fundamentals courses** — `software-architecture`, `domain-driven-design`,
  `system-design`, `event-driven-architecture`, `distributed-systems`.
- **2 build-your-own framework courses** — `build-your-own-web-framework`,
  `build-your-own-reactive-ui`.
- **2 AI on-ramp courses** — `creating-ai-powered-apps` (use-an-LLM-in-an-app scope) and `agentic-ai`
  (a survey that forward-links, never re-teaches, the harness cluster).
- **1 automation course** — `browser-automation-with-cdp`.
- **5 harness-cluster courses** — `the-agent-loop`, `agent-tools-and-mcp`,
  `agent-context-and-memory`, `agent-permissions-and-sandboxing`,
  `agent-orchestration-subagents-and-observability` — the build-your-own-depth counterpart to the
  `agentic-ai` survey.
- **3 course-surgery scope contracts**, locked before their target bodies exist and applied by
  construction: the evals forward-link contract (so `creating-ai-powered-apps`, `agentic-ai`, and
  `agent-orchestration-subagents-and-observability` forward-link the deep-evals course rather than
  re-teaching it), the D9 naming-and-citation contract (context-engineering and
  harness-engineering lineage citations), and the D11 concept-additions contract (four
  research-verified concepts landing inside existing harness-cluster courses).

The business change here is **content**, not architecture: no schema, no route, no component, no
redirect, and — by binding invariant — **no manifest**.

## Why this band is split into its own plan

The parent plan, `ayokoding-learning-path-04-course-authoring`, originally authored all 90 bodies
across nine bands plus these three contracts inside one delivery checklist. Splitting Band 5 out
lets its 15 bodies — the entire AI/harness cluster among them — land, review, and merge on their own
schedule, independent of the other eight bands' progress. This mirrors the same reasoning that
produced the original five-way split of `shared-course-library-and-learning-paths`: narrower plans
review faster and fail more legibly than one 90-body mega-checklist.

## Why the bodies must be authored from spec, not generated ad hoc

The naive alternative is to let each authoring pass make its own judgment calls about scope, concept
coverage, worked-example volume, and prerequisite edges. That fails in a specific, expensive way
[Judgment call]:

- **Concept coverage drifts.** Each of these 15 courses already has a settled spec file with an
  enumerated `co-NN` concept list and an `ex-NN` worked-example inventory. Authoring "from a fresh
  judgment call" silently drops concepts nobody notices are missing until a reader hits the gap.
- **Prerequisite edges get invented.** A body that declares a prerequisite the spec never named adds
  an edge to the library's DAG. That failure does **not** surface here — it surfaces much later, in
  the manifest-growth plans, as an integrity failure with no traceable link back to the authoring
  decision that caused it.
- **The AI band's largest duplication risk re-appears.** Three courses independently teaching evals,
  and a survey course re-teaching what the harness cluster owns, is exactly the failure mode the
  parent plan's course-surgery contracts were designed to prevent. Only locking the contracts
  **before** the target bodies exist, and applying them by construction, closes this risk.

## Why the manifest ownership invariant is a business decision, not a technicality

Courses are **shared**. Any edit, split, or merge to a course ripples to every manifest carrying that
course ID. If this plan could also edit manifests, a single authoring pass could silently truncate a
path — an outcome that **looks correct** because integrity still passes over the narrowed set.

This plan can only **add bodies**. The band-completion signal — a five-field record naming exactly
which manifests must grow — is the entire handoff to the downstream manifest-growth plans. Vagueness
here is the one way this boundary fails, which is why the signal's shape is specified in `README.md`
rather than left to convention.

## Business Impact

**Pain points addressed**:

- Without this band, no path can reach architecture, distributed-systems, or build-your-own-framework
  depth — a gap every one of the four paths eventually hits.
- The fourth path (`careers/immediately-effective/ai-engineer`) is stuck at its six-course
  smoke-test spine until this band lands 8 of the 9 courses its full DD-35-governed manifest walks.
- `distributed-systems` is a hard prerequisite of `build-your-own-raft`
  (`ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`) — that plan cannot author
  its own capstone-adjacent course until this band lands.
- The library's evals material is triple-taught with no single owner until the forward-link contract
  is applied to the three donor courses this band authors.

**Expected benefits** (qualitative reasoning; no fabricated metrics):

- **One authoring investment, four products.** Each body is authored once, path-neutral, at one
  canonical URL. Every path that references it benefits from every later fix at zero marginal cost.
- **A curriculum that can be audited.** Because every body traces to a settled spec, "is this course
  complete?" is answerable by comparing the body against its `co-NN`/`ex-NN` enumeration.
- **Scope contracts locked before the material exists.** The evals / D9 / D11 contracts are recorded
  in this plan's own Phase 1, before their target courses are authored in Phases 2–4, so the surgery
  is applied **by construction** rather than as an expensive later retrofit.
- **A complete, working AI/harness cluster.** All five harness courses plus the two AI on-ramp courses
  land together, so a reader who reaches this band gets a coherent build-your-own-agent arc rather
  than a partial one.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns each course's scope boundary against its siblings, and the three
  course-surgery contracts.
- **Content author** (via the `apps-ayokoding-www-{by-example,annotated-concept}-maker` agents) —
  writes the 15 bodies.
- **Content reviewer** (via the matching checkers plus facts and link checkers) — validates every
  body before the plan's sole terminal PR merges.

Consuming agents [Repo-grounded]: `apps-ayokoding-www-by-example-maker`,
`apps-ayokoding-www-annotated-concept-maker`, and their matching checkers, plus
`apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker`, and `web-researcher` for the
accuracy pre-verification pass.

**Roles explicitly NOT worn by this plan**: frontend engineer (owned by
`ayokoding-learning-path-03-navigation-ui`), data/schema author (owned by
`ayokoding-learning-path-02-schema-and-prerequisite-dag`), path composer (owned by
`ayokoding-learning-path-12-careers-se-manifests` and `ayokoding-learning-path-13-careers-ai-manifest`,
the successor manifest-growth plans), IA/URL owner (owned
by `ayokoding-learning-path-01-url-restructure`), the other eight authoring bands (owned by the
parent plan and its sibling band-splits).

## Business-Level Success Metrics

Each metric below is an **observable check**, not a projected number.

- **15 authored bodies exist** (observable): every course ID in
  [README §Exact scope](./README.md#exact-scope-15-courses-in-order) resolves to a directory under
  `<COURSES>`. Falsifiable in both directions — before Phase 2, all 15 are absent; after Phase 4,
  none is.
- **Every body traces to its spec** (observable): each authored course's scope, concept coverage, and
  declared prerequisites match the `co-NN` / `ex-NN` / prerequisite-chain enumeration in its
  `syllabus/courses/<course-id>.md` spec. Verified per-course by its checker pass.
- **The three course-surgery contracts are applied by construction** (observable): each of the three
  evals-donor courses (`creating-ai-powered-apps`, `agentic-ai`,
  `agent-orchestration-subagents-and-observability`) forward-links `evaluating-ai-systems-in-depth`;
  `agent-context-and-memory` carries its context-engineering lineage citation; the harness cluster
  carries the harness-engineering citation; the four D11 concepts appear in their named target
  courses.
- **The AI-band scope-guard holds** (observable): `agentic-ai`'s overview names and forward-links all
  five harness-cluster courses, and no lesson in `agentic-ai/` builds a working
  loop / tool / memory / permission / orchestration implementation.
- **No manifest file changed in this plan's commits** (observable): the plan's own diff across all
  merged PRs touches zero paths under `<MANIFESTS>`.
- **One complete band signal emitted** (observable): the five-field band-completion signal, naming
  all four manifests by full path and carrying its merge commit SHA.
- **No regressions** (observable): `nx run ayokoding-www:build` renders green; markdownlint, link
  validation, and heading-hierarchy validation pass across the authored tree.

## Business-Scope Non-Goals

- **Editing any manifest file.** Binding invariant — owned by
  `ayokoding-learning-path-12-careers-se-manifests` and `ayokoding-learning-path-13-careers-ai-manifest`,
  the successor manifest-growth plans. Not a scope preference; a correctness requirement.
- **Building any part of the navigation UI.** Owned by `ayokoding-learning-path-03-navigation-ui`.
- **Authoring any course outside the 15 named in README §Exact scope.** The other eight bands (all 75
  remaining bodies) are owned by the parent plan and its sibling band-authoring splits.
- **Authoring `capstone-build-your-own-coding-agent`.** That capstone assembles this band's harness
  cluster but is authored by `ayokoding-learning-path-11-course-authoring-capstones` (Band 8).
- **Defining the `prerequisites` frontmatter contract.** This plan **consumes** the contract;
  `ayokoding-learning-path-02-schema-and-prerequisite-dag` owns its canonical shape.
- **Adding an Indonesian mirror of the course content** — deferred, recorded as a decision rather than
  an omission. Every course body in this plan is `en`-only.
- **Rewriting the pedagogy or depth of any topic outside this band's 15 courses.**

## Business Risks and Mitigations

| Risk                                                                                                                                                            | Mitigation                                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| A body is authored from a fresh judgment call instead of its settled spec, so concept coverage drifts.                                                          | Every authoring step names the exact cross-plan `syllabus/courses/<course-id>.md` path and makes "authored from that spec" an explicit acceptance criterion; the checker pass compares the body against the spec's `co-NN`/`ex-NN` enumeration.                                                                                                              |
| A step in this plan mutates a manifest, making the split unschedulable.                                                                                         | The manifest ownership invariant is stated in `README.md`, `tech-docs.md`, and `delivery.md`; the handoff is a five-field band-completion signal; every phase gate asserts the plan's diff touches zero paths under `<MANIFESTS>`.                                                                                                                           |
| AI-band courses duplicate the agent-loop / tools / MCP / memory / evals material.                                                                               | The AI-band scope-guard contract is baked into Phase 2–4 authoring steps as grep-checkable acceptance criteria: `agentic-ai` forward-links each primitive and stops short of build-your-own depth.                                                                                                                                                           |
| The evals material gains a fourth treatment instead of being extracted to a single owner.                                                                       | The evals forward-link contract is locked in Phase 1, **before** its donor courses are authored in Phases 2 and 4, and lands as an explicit acceptance criterion on each of the three donors' own authoring steps.                                                                                                                                           |
| Contested terminology ("harness engineering") is adopted as course structure.                                                                                   | The D9 contract cites the containment dispute as **unresolved** rather than adopting a side as course structure; no course is renamed; the unverified OpenAI attribution is excluded.                                                                                                                                                                        |
| Ninety-plus-body library authoring stalls because 15 bodies are authored serially.                                                                              | Bodies within a cohort are content-independent and pipeline concurrently through review, bounded by the in-force concurrency cap; each cohort is its own phase with its own safe stopping point.                                                                                                                                                             |
| A course body reproduces copyrighted material (programme A8).                                                                                                   | Six concrete hazards mapped to the authoring pipeline in [tech-docs.md §Licensing posture](./tech-docs.md#licensing-posture-programme-a8): code authored originally, docs prose restated with citation, figures authored (Mermaid) not lifted, structure derived from the course's own spec order, trademarks nominative only, datasets authored not lifted. |
| This plan starts authoring before its upstream preconditions (the parent plan's Phase 1, or `vercel-function-cost-reduction`'s Phases 1–4) are actually merged. | Phase 0 carries an explicit, checkable start precondition for all four `blockedBy` plans (see [README §Depends-on](./README.md#depends-on)); the plan does not start on a promise.                                                                                                                                                                           |
| A band lands but no downstream plan ever grows its manifests, leaving paths permanently truncated.                                                              | The band's gate requires a complete five-field signal naming every affected manifest by full path plus the merge commit SHA; an incomplete signal is rejected by the receiving plan(s) rather than guessed at.                                                                                                                                               |
