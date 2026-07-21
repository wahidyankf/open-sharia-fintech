# Business Requirements — Learning Path Course Authoring

## Business Goal

Fill the shared course library with the **90 course bodies** it does not yet have, so that the
four-path product the split delivers has something to compose. A path manifest is an ordered list of
course IDs; an ID with no resolving body is an integrity failure, not a path. **This plan is the one
that turns an architecture into a curriculum.**

Concretely it authors:

- **6 net-new AI-engineering courses** — the light eval gate, statistics for evals, deep evals,
  product patterns for probabilistic systems, inference serving and model deployment, and fine-tuning
  and adaptation — the spine of the fourth path
  (`careers/immediately-effective/ai-engineer`), and **authoring priority #1** under the
  locked build order (DD-27).
- **61 transferred topics** (FS-SE topics 34–94), authored **native** into `courses/` — no legacy
  home, therefore no re-home and no redirect.
- **10 remaining new courses** the productivity, harness, and security clusters need.
- **8 remaining capstones** — 2 original plus 6 of the 7 DD-20 inter-topic capstones.
- **5 deferred interview-technique bodies** (Band 9) — the four interview courses plus
  `capstone-interview-loop`, deliberately deferred out of the architecture-smoke-test MVP gate so
  they never blocked the AI path's authoring start.
- **3 course-surgery scope contracts** — the evals forward-link contract, the D9 naming-and-citation
  contract, and the D11 concept-addition contract — locked once and applied by construction when
  their target bodies are authored, rather than retrofitted later.

The business change here is **content**, not architecture: no schema, no route, no component, no
redirect, and — by binding invariant — **no manifest**.

## Why the bodies must be authored, not generated ad hoc

The naive alternative is to let each authoring pass make its own judgment calls about scope, concept
coverage, worked-example volume, and prerequisite edges. That fails in a specific, expensive way
[Judgment call]:

- **Concept coverage drifts.** Each of the 121 courses already has a settled spec file with an
  enumerated `co-NN` concept list and an `ex-NN` worked-example inventory. Authoring "from a fresh
  judgment call" silently drops concepts nobody notices are missing until a reader hits the gap.
- **Prerequisite edges get invented.** A body that declares a prerequisite the spec never named adds
  an edge to the library's DAG. The DAG stops being topologically consistent — and that failure does
  **not** surface here. It surfaces much later, in
  `ayokoding-learning-path-05-manifests`, as a manifest-integrity failure with no traceable link
  back to the authoring decision that caused it.
- **Scope boundaries collapse.** The library's largest historical duplication risk is the AI band:
  three courses independently teaching evals, and a survey course re-teaching what the harness
  cluster owns. Only an explicit, pre-locked scope contract prevents a fourth treatment appearing.

Authoring **from** the settled `syllabus/courses/<course-id>.md` spec removes all three failure modes
at their root. This is why the spec folder is a hard prerequisite of this plan and why copying it is
forbidden — a copy forks the source of truth for 121 course specs, so a later spec correction lands
in one copy only.

## Why the manifest ownership invariant is a business decision, not a technicality

Courses are **shared**. Any edit, split, or merge to a course ripples to every manifest carrying that
course ID. If this plan could also edit manifests, a single authoring pass could silently truncate a
path — an outcome that **looks correct** because integrity still passes over the narrowed set.

Separating the two responsibilities makes the failure loud instead of silent:

- This plan can only **add bodies**. A missing body fails the downstream manifest-integrity gate
  hard and visibly.
- The manifest plan can only **compose IDs**. It cannot paper over a missing body by narrowing the
  path, because it does not own the authoring pass that would have to be skipped.

The handoff is the **band-completion signal** — an explicit, five-field record naming exactly which
manifests must grow. Vagueness here is the one way this boundary fails, which is why the signal's
shape is specified in `README.md` rather than left to convention.

## Business Impact

**Pain points addressed**:

- The library today holds 37 bodies' worth of shipped material and a catalog target of 127. Without
  this plan, three of the four paths are permanently truncated and the fourth has a six-course spine
  where its design calls for fifteen.
- There is no interview-technique material at all — the single highest-time-pressure use of the whole
  curriculum (an experienced engineer days-to-weeks from a senior loop) has nothing to read.
- An already-working software engineer moving into AI engineering has no structured on-ramp into
  **building** AI systems. The six net-new AI courses are that on-ramp.
- The library's evals material is triple-taught with no single owner, and its agent primitives risk
  being taught twice (once as survey, once at build-your-own depth). Both are duplication the
  shared-library model exists to prevent.
- FS-SE's Passes 3–5 scope (topics 34–94) has no home since that plan closed. It is absorbed here.

**Expected benefits** (qualitative reasoning; no fabricated metrics):

- **One authoring investment, four products.** Each body is authored once, path-neutral, at one
  canonical URL. Every path that references it benefits from every later fix at zero marginal cost.
- **A curriculum that can be audited.** Because every body traces to a settled spec, "is this course
  complete?" is answerable by comparing the body against its `co-NN`/`ex-NN` enumeration, rather than
  by a reviewer's impression.
- **Scope contracts locked before the material exists.** The evals / D9 / D11 contracts are recorded
  before their target courses are authored, so the surgery is applied **by construction** — authored
  correctly from the start — rather than as an expensive later retrofit across six bodies.
- **Durable content in a volatile domain.** Every AI-band body is split into a **stable spine**
  (durable principles) and **dated accuracy-note sidebars** (volatile SDK / model / pricing /
  framework specifics), so the curriculum ages at the rate of its principles rather than its vendors.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns each course's scope boundary against its siblings, and the three
  course-surgery contracts.
- **Content author** (via the `apps-ayokoding-www-*-maker` agents) — writes the 90 bodies.
- **Content reviewer** (via the `apps-ayokoding-www-*-checker` plus facts and link checkers) —
  validates every body before its PR merges.

Consuming agents [Repo-grounded]: `apps-ayokoding-www-by-example-maker`,
`apps-ayokoding-www-annotated-concept-maker`, `apps-ayokoding-www-primer-maker`,
`apps-ayokoding-www-general-maker` and their matching checkers, plus
`apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker`, and `web-researcher` for the
accuracy pre-verification pass.

**Roles explicitly NOT worn by this plan**: frontend engineer (owned by
`ayokoding-learning-path-03-navigation-ui`), data/schema author (owned by
`ayokoding-learning-path-02-schema-and-prerequisite-dag`), path composer (owned by
`ayokoding-learning-path-05-manifests`), IA/URL owner (owned by
`ayokoding-learning-path-01-url-restructure`).

## Business-Level Success Metrics

Each metric below is an **observable check**, not a projected number. Where a claim rests on
judgment rather than a check, it is labelled.

- **90 authored bodies exist** (observable): every slug listed in
  `evidence/authored-body-slugs.txt` resolves to a directory under `<COURSES>`. Falsifiable in both
  directions — before Phase 1 all 90 are absent; after Band 9 none is.
- **Every body traces to its spec** (observable): each authored course's scope, concept coverage,
  and declared prerequisites match the `co-NN` / `ex-NN` / prerequisite-chain enumeration in its
  `syllabus/courses/<course-id>.md` spec. Verified per-course by its checker pass.
- **Every body declares `prerequisites`** (observable): each `_index.md` carries a
  `prerequisites: [course-id, ...]` list in the contracted shape, so the library's prerequisite DAG
  stays complete as it grows. A missing declaration is caught downstream as an integrity failure —
  the point of asserting it here is to catch it at authoring time instead.
- **Every body passes its content checkers** (observable): zero CRITICAL / HIGH / MEDIUM findings
  from the matching learning checker, `apps-ayokoding-www-facts-checker`, and
  `apps-ayokoding-www-link-checker`.
- **Scope boundaries are stated, not merely respected** (observable): the light eval gate and deep
  evals each name the other; `statistics-for-evaluation` names `analytics-and-experimentation`;
  `detection-engineering-and-siem-operations` names `defensive-security`; `self-hosting-essentials`
  names the cluster and IaC courses it stays below. Each is a grep-checkable assertion on the
  course's own `overview.md`.
- **The AI-band scope-guard holds** (observable): `agentic-ai`'s overview names and forward-links all
  five harness-cluster courses, and no lesson in `agentic-ai/` builds a working
  loop / tool / memory / permission / orchestration implementation.
- **The three course-surgery contracts are applied by construction** (observable): each of the three
  evals-donor courses forward-links `deep-evals`; `agent-context-and-memory` carries its
  context-engineering lineage citation; the harness cluster and the coding-agent capstone carry the
  harness-engineering citation; the four D11 concepts appear in their named target courses.
- **No manifest file changed in this plan's commits** (observable): the plan's own diff across all
  merged PRs touches zero paths under `<MANIFESTS>`. This is the manifest ownership invariant
  expressed as a business check.
- **Every band emitted a complete signal** (observable): one five-field band-completion signal per
  band, each naming its manifests by full path and carrying its merge commit SHA.
- **No regressions** (observable): `nx run ayokoding-www:build` renders green; markdownlint, link
  validation, and heading-hierarchy validation pass across the authored tree.

## Business-Scope Non-Goals

- **Editing any manifest file.** Binding invariant — owned by
  `ayokoding-learning-path-05-manifests`. Not a scope preference; a correctness requirement.
- **Building any part of the navigation UI.** The path rail, banner, breadcrumb, prerequisite-list
  component, path landings, and paths hub belong to `ayokoding-learning-path-03-navigation-ui`.
- **Re-homing the 33 shipped topics or the 4 existing capstones.** Those bodies already exist; moving
  them is `ayokoding-learning-path-01-url-restructure`'s work. This plan authors only what has no
  body yet — which is why `capstone-solid-core` is absent from its 90 despite being a DD-20 capstone.
- **Defining the `prerequisites` frontmatter contract.** This plan **consumes** the contract;
  `ayokoding-learning-path-02-schema-and-prerequisite-dag` owns its canonical shape.
- **Adding an Indonesian mirror of the course content** — deferred, recorded as a decision rather
  than an omission. Every course body in this plan is `en`-only.
- **Rewriting the pedagogy or depth of any existing topic.** The 61 transferred topics are authored
  native from their settled specs; they are not re-conceived.
- **Promoting legacy material into real courses.** Later work, tracked under Q-A by the
  URL-restructure plan; this plan files no per-page migration backlog.
- **Interactive or JS flashcards.** Drilling tracks stay static markdown, matching the sibling plan.
- **Enumerating speculative course variants.** A distinct-pedagogy variant is authored on demand
  only, never pre-enumerated (DD-8).
- **Adding any course beyond the locked list.** The net-new AI course list is locked at exactly six
  (DD-32); the naming, citation, and concept work of DD-29 through DD-31 adds **zero** courses.

## Business Risks and Mitigations

| Risk                                                                                                     | Mitigation                                                                                                                                                                                                                                                          |
| -------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A body is authored from a fresh judgment call instead of its settled spec, so concept coverage drifts.   | Every authoring step names the exact cross-plan `syllabus/courses/<course-id>.md` path and makes "authored from that spec" an explicit acceptance criterion; the checker pass compares the body against the spec's `co-NN`/`ex-NN` enumeration.                     |
| The `syllabus/` specs are copied into this folder, forking the source of truth for 121 course specs.     | A binding cross-plan reference rule: every reference uses the full relative path into the schema plan's folder, never a local copy. A pre-archival link-validation gate scoped to this plan's own paths catches a broken or re-pointed reference.                   |
| A step in this plan mutates a manifest, making the wave order unschedulable.                             | The manifest ownership invariant is stated in `README.md`, `tech-docs.md`, and `delivery.md`; the handoff is a five-field band-completion signal; a phase gate asserts the plan's diff touches zero paths under `<MANIFESTS>`.                                      |
| A natively-authored slug collides with a not-yet-moved re-home slug, silently sharing one canonical URL. | The 23-new-slug collision check runs in Phase 0 **against a populated `courses/` namespace** — which is exactly why the URL-restructure plan is a hard prerequisite. Against an empty namespace the check passes vacuously and proves nothing.                      |
| Invented prerequisite edges break the DAG, surfacing far downstream with no traceable cause.             | Each body's `prerequisites` are transcribed from its spec's declared chain, never re-derived; the declaration is an explicit per-course acceptance criterion at authoring time rather than a downstream discovery.                                                  |
| AI-band courses duplicate the agent-loop / tools / MCP / memory / evals material.                        | The AI-band scope-guard contract (DD-11 / DL-10) is baked into the Band 5 authoring steps as grep-checkable acceptance criteria: `agentic-ai` forward-links each primitive and stops short of build-your-own depth.                                                 |
| The evals material gains a fourth treatment instead of being extracted to a single owner.                | The evals forward-link contract is locked **before** its donor courses are authored, and lands as an explicit acceptance criterion on each of the three donors' own authoring steps — applied by construction, never retrofitted.                                   |
| `detection-engineering-and-siem-operations` and `defensive-security` overlap.                            | Explicit scope lines in both bodies: `defensive-security` (re-labelled hands-on By-Example) keeps generalist Sigma/ELK breadth, IR, and hardening; the detection course owns deep Wazuh decoder/rule/dashboard SIEM-ops and declares `defensive-security` a prereq. |
| Volatile AI/SDK/model/pricing facts are written into the stable spine and age the curriculum badly.      | DD-28's durability constraint is an authoring requirement, not polish: volatile facts sit **only** in dated accuracy-note sidebars. Enforced per-course by the accuracy pre-verify step and re-checked by `apps-ayokoding-www-facts-checker`.                       |
| Unsourced or contested claims are written as settled fact (the harness-engineering naming dispute).      | DD-29 cites the containment dispute as **unresolved** rather than adopting a side as course structure; DD-30 labels the competence-floor reconciliation a synthesis no single source makes and marks the 42%→78% figure an explicit do-not-cite.                    |
| Ninety bodies authored serially stall the plan indefinitely.                                             | Bodies are content-independent (each writes only its own subtree) and pipeline concurrently through review, bounded by the in-force concurrency cap. Each band is its own phase with its own safe stopping point, so partial delivery is always a coherent state.   |
| Q-A is ruled after authoring begins, forcing a rewrite of 90 `overview.md` files.                        | Authoring proceeds without the supersession line and records the pending obligation; the supersession sweep is one bounded conditional pass over only the courses whose subject a legacy page covers, not a per-course rewrite.                                     |
| A band lands but the manifest plan never grows its manifests, leaving paths permanently truncated.       | Each band's gate requires a complete five-field signal naming every affected manifest by full path plus the merge commit SHA; an incomplete signal is rejected by the receiving plan rather than guessed at.                                                        |

</content>
