# Business Requirements — Course Authoring: Platform & Concurrency Languages

## Business Goal

Fill the shared course library with the **14 course bodies** plan04's Band 3 and Band 4 scoped but
had not yet authored, so that every path manifest that will eventually reference a mobile/desktop
platform course or a concurrency-language course has something to compose. A path manifest is an
ordered list of course IDs; an ID with no resolving body is an integrity failure, not a path. **This
plan turns two named-but-unwritten bands of plan04's architecture into readable curriculum.**

Concretely it authors, in five paired-and-standalone groups:

- **Four `just-enough-<language>` primer + native-platform pairs** — Kotlin/Android,
  Swift/iOS, Dart/hybrid (Flutter idioms), C#/Windows — each primer existing solely to unlock its
  paired platform course.
- **Two standalone platform courses** — `linux-app-development` (Python, native Linux desktop +
  packaging) and `building-production-cli-tools` (Go + Rust, distributable CLI tools) — neither pairs
  with a net-new primer here because their prerequisite primers (`just-enough-python`, `just-enough-go`,
  `just-enough-rust`) are delivered elsewhere in the programme; `just-enough-rust` is scheduled
  independently.
- **Two `just-enough-<language>` primer + concurrency-paradigm pairs** — Go/CSP-style channels,
  Elixir/actor-model supervision trees — the library's two concrete concurrency paradigms, each
  built on the shared `concurrency-and-parallelism` foundation course plan04 already authored.

The business change here is **content**, not architecture: no schema, no route, no component, no
redirect, and — by binding invariant, inherited unchanged from plan04 — **no manifest**.

## Why these 14 bodies, split from plan04, rather than left inside it

Plan04 originally scoped 90 bodies as one plan. Splitting Bands 3 and 4 out into their own plan (and
merging them, since both share the identical primer-plus-application authoring shape) lets this
narrower slice of work proceed and land independently of plan04's other seven bands — which plan04
itself records as "mutually content-independent" from this pair. The business benefit is
**parallelization without correctness risk**: this plan's 14 bodies share no prerequisite edge with
any band this plan does not touch (verified against plan04's own catalog rows), so authoring them here
instead of inside plan04 changes nothing about what a reader eventually sees, while letting the work
proceed in one dedicated worktree and one final review cycle, without coupling its delivery
schedule to plan04's other bands.

## Why the bodies must be authored from the settled spec, not generated ad hoc

The naive alternative is to let this authoring pass make its own judgment calls about scope, concept
coverage, worked-example volume, and prerequisite edges for each of the 14 courses. That fails in the
same specific, expensive way plan04's own `brd.md` already documents for its 90 bodies [Judgment call]:

- **Concept coverage drifts.** Each of the 14 courses already has a settled spec file with an
  enumerated `co-NN` concept list and an `ex-NN` worked-example inventory at
  `syllabus/courses/<course-id>.md`. Authoring "from a fresh judgment call" silently drops concepts
  nobody notices are missing until a reader hits the gap.
- **Prerequisite edges get invented.** A body that declares a prerequisite the spec never named adds
  an edge to the library's DAG. That failure does **not** surface here — it surfaces downstream, in
  the manifest-growth plan, as a manifest-integrity failure with no traceable link back to the
  authoring decision that caused it.
- **The primer/platform pairing collapses.** Each `just-enough-<language>` primer in this plan exists
  **because** its paired platform course needs it — a primer authored from a fresh judgment call
  risks teaching the wrong subset of the language (too much, too little, or the wrong idioms), leaving
  the paired platform course either duplicating primer content or assuming knowledge the primer never
  taught.

Authoring **from** the settled `syllabus/courses/<course-id>.md` spec removes all three failure modes
at their root, exactly as it does for plan04's other 76 bodies. This is why the spec folder is a hard
prerequisite of this plan and why copying it is forbidden — a copy forks the source of truth for 122
course specs, so a later spec correction lands in one copy only.

## Why the manifest ownership invariant is a business decision, not a technicality

Courses are **shared**. Any edit, split, or merge to a course ripples to every manifest carrying that
course ID. If this plan could also edit manifests, a single authoring pass could silently truncate a
path — an outcome that **looks correct** because integrity still passes over the narrowed set.
Separating the two responsibilities makes the failure loud instead of silent: this plan can only
**add bodies**, and the manifest-growth plan can only **compose IDs**. The handoff is the
**band-completion signal** — an explicit, five-field record naming exactly which manifests must grow
— identical in shape to the contract plan04 already established, reused here rather than re-invented.

## Business Impact

**Pain points addressed**:

- Without this plan, three of the four `careers/` paths (`interview-ready`, `immediately-effective`,
  `fundamentally-strong` — all three software-engineer-role paths) are permanently missing every
  mobile-development, desktop-development, and named-concurrency-paradigm course a reader might
  expect from a software-engineering curriculum that claims broad platform coverage.
- A reader who already knows general-purpose programming but wants to build for a specific platform —
  Android, iOS, cross-platform Flutter, Windows desktop, Linux desktop, or a distributable CLI tool —
  has no structured on-ramp. These 10 Band-3 bodies are that on-ramp.
- A reader who wants to understand a named concurrency paradigm rather than the language-agnostic
  `concurrency-and-parallelism` foundation has nowhere to go deeper. The two Band-4 pairs are that
  depth: CSP-style channel concurrency in Go, and the actor model with supervision trees in Elixir.
- `ayokoding-learning-path-10-course-authoring-jvm-and-build-your-own`'s own `build-your-own-raft`
  -adjacent work is blocked without `csp-style-concurrency` and `actor-model-concurrency` already
  landed — this plan's Band 4 is a genuine, not merely convenient, upstream dependency for that plan.

**Expected benefits** (qualitative reasoning; no fabricated metrics):

- **One authoring investment, four products.** Each of the 14 bodies is authored once, path-neutral,
  at one canonical URL. Every `careers/` path that eventually references it benefits from every later
  fix at zero marginal cost — the same economics plan04 already established for its 90 bodies.
- **A curriculum that can be audited.** Because every body traces to a settled spec, "is this course
  complete?" is answerable by comparing the body against its `co-NN`/`ex-NN` enumeration, rather than
  by a reviewer's impression.
- **Parallel authoring without correctness risk.** Splitting this content-independent pair of bands
  into its own plan lets it land on its own schedule without waiting on, or blocking, plan04's other
  seven bands.
- **Unblocks a named downstream plan.** `ayokoding-learning-path-10-...`'s concurrency-adjacent
  capstone work can proceed the moment this plan's Band 4 lands, rather than waiting on plan04's
  entire remaining 76-body backlog.

## Affected Roles

Solo-maintainer repo — no sign-off ceremony. The maintainer wears:

- **Content strategist** — owns each course's scope boundary against its siblings (e.g.
  `linux-app-development` against `just-enough-python`'s own scope, `building-production-cli-tools`
  against the two primers it depends on).
- **Content author** (via the `apps-ayokoding-www-primer-maker` and `apps-ayokoding-www-by-example-maker`
  agents) — writes the 14 bodies.
- **Content reviewer** (via the matching `apps-ayokoding-www-{primer,by-example}-checker` plus facts
  and link checkers) — validates every body before its PR merges.

Consuming agents [Repo-grounded]: `apps-ayokoding-www-primer-maker` (the four `just-enough-*` primers
plus `just-enough-go` and `just-enough-elixir`), `apps-ayokoding-www-by-example-maker` (the ten
By-Example platform and concurrency bodies), their matching checkers, plus
`apps-ayokoding-www-facts-checker`, `apps-ayokoding-www-link-checker`, and `web-researcher` for the
accuracy pre-verification pass.

**Roles explicitly NOT worn by this plan**: frontend engineer (owned by
`ayokoding-learning-path-03-navigation-ui`), data/schema author (owned by
`ayokoding-learning-path-02-schema-and-prerequisite-dag`), path composer (owned by the manifest-growth
plan), IA/URL owner (owned by `ayokoding-learning-path-01-url-restructure`).

## Business-Level Success Metrics

Each metric below is an **observable check**, not a projected number.

- **14 authored bodies exist** (observable): every one of the 14 slugs resolves to a directory under
  `<COURSES>`. Falsifiable in both directions — before Phase 1 all 14 are absent; after Phase 2 none
  is.
- **Every body traces to its spec** (observable): each authored course's scope, concept coverage, and
  declared prerequisites match the `co-NN` / `ex-NN` / prerequisite-chain enumeration in its
  `syllabus/courses/<course-id>.md` spec. Verified per-course by its checker pass.
- **Every body declares `prerequisites`** (observable): each `_index.md` carries a
  `prerequisites: [course-id, ...]` list in the contracted shape.
- **Every primer/platform pair resolves correctly** (observable): each platform course's declared
  prerequisite includes its paired primer's exact slug — `android-app-development` names
  `just-enough-kotlin`, `ios-app-development` names `just-enough-swift`, `hybrid-app-development`
  names `just-enough-dart`, `windows-app-development` names `just-enough-csharp`,
  `csp-style-concurrency` names `just-enough-go`, `actor-model-concurrency` names `just-enough-elixir`
  — each a grep-checkable assertion on the course's own `_index.md`.
- **Every body passes its content checkers** (observable): zero CRITICAL / HIGH / MEDIUM findings from
  the matching content checker, `apps-ayokoding-www-facts-checker`, and
  `apps-ayokoding-www-link-checker`.
- **No manifest file changed in this plan's commits** (observable): the plan's own diff across all
  merged PRs touches zero paths under `<MANIFESTS>`. This is the manifest ownership invariant
  expressed as a business check.
- **Both band signals are complete** (observable): one five-field band-completion signal per band,
  each naming its three manifests by full path and carrying its merge commit SHA.
- **No regressions** (observable): `nx run ayokoding-www:build` renders green; markdownlint, link
  validation, and heading-hierarchy validation pass across the authored tree.

## Business-Scope Non-Goals

- **Editing any manifest file.** Binding invariant — owned by the manifest-growth plan. Not a scope
  preference; a correctness requirement.
- **Building any part of the navigation UI.** Owned by `ayokoding-learning-path-03-navigation-ui`.
- **Re-homing any already-shipped course.** This plan authors only content that has no body yet.
- **Defining the `prerequisites` frontmatter contract.** This plan **consumes** the contract;
  `ayokoding-learning-path-02-schema-and-prerequisite-dag` owns its canonical shape.
- **Adding an Indonesian mirror of the course content** — deferred, recorded as a decision rather than
  an omission. Every course body in this plan is `en`-only.
- **Authoring any course outside the named 14.** No other band's content, no new capstone, no course
  surgery against an existing body — this plan's scope is exactly the 14 IDs named in `README.md`.
- **Growing the fourth (`ai-engineer`) path's manifest.** Bands 3 and 4 route to the three
  software-engineer-role manifests only, per plan04's own routing table — not to `ai-engineer`.

## Business Risks and Mitigations

| Risk                                                                                                                     | Mitigation                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| A body is authored from a fresh judgment call instead of its settled spec, so concept coverage drifts.                   | Every authoring step names the exact cross-plan `syllabus/courses/<course-id>.md` path and makes "authored from that spec" an explicit acceptance criterion; the checker pass compares the body against the spec's `co-NN`/`ex-NN` enumeration.                                                                                                                                                                                                          |
| The `syllabus/` specs are copied into this folder, forking the source of truth for 122 course specs.                     | A binding cross-plan reference rule: every reference uses the full relative path into the schema plan's folder, never a local copy. A pre-archival link-validation gate scoped to this plan's own paths catches a broken or re-pointed reference.                                                                                                                                                                                                        |
| A step in this plan mutates a manifest, making the split unschedulable.                                                  | The manifest ownership invariant is stated in `README.md`, `tech-docs.md`, and `delivery.md`; the handoff is a five-field band-completion signal; a phase gate asserts the plan's diff touches zero paths under `<MANIFESTS>`.                                                                                                                                                                                                                           |
| A natively-authored slug collides with an already-shipped or already-landed slug.                                        | The 14-slug collision check runs in Phase 0 against the populated `courses/` namespace — which is exactly why `ayokoding-learning-path-01-url-restructure` and `ayokoding-learning-path-04-course-authoring` are hard prerequisites.                                                                                                                                                                                                                     |
| Invented prerequisite edges break the DAG, surfacing far downstream with no traceable cause.                             | Each body's `prerequisites` are transcribed from its spec's declared chain, never re-derived; the declaration is an explicit per-course acceptance criterion at authoring time rather than a downstream discovery.                                                                                                                                                                                                                                       |
| A primer/platform pair is authored out of order, so the platform course's prerequisite check fails or reads confusingly. | Each pair is authored inside the same band-phase, primer before or alongside its paired platform course, per the fixed course-list order in `README.md`; the pairing is checked in each phase's gate.                                                                                                                                                                                                                                                    |
| This plan lands against a still-dynamic, still-middlewared `ayokoding-www` (the `vercel-function-cost-reduction` risk).  | Phase 0 hard-gates on the checkable precondition (`app/layout.tsx` and `src/middleware.ts` both absent) before any authoring begins; this plan does not proceed on a promise.                                                                                                                                                                                                                                                                            |
| `ayokoding-learning-path-10-...`'s `build-your-own-raft` is blocked because `just-enough-go` lands late or incompletely. | Band 4 is authored and structurally checked before the terminal archival PR; the plan-wide completion signal names `just-enough-go` among the four Band-4 IDs after that sole PR merges. (Corrected from an earlier draft of this risk that cited `csp-style-concurrency`/`actor-model-concurrency` as the needed courses — the verified DAG edge, confirmed against `ayokoding-learning-path-10-...`'s own dependency table, is `just-enough-go` only.) |
| A course body reproduces copyrighted material (programme `A8`, inherited from plan04's own reasoning verbatim).          | Same six concrete hazards mapped to the authoring pipeline as plan04: code examples authored originally, docs prose restated with citation, figures authored (Mermaid) not lifted, structure derived from the course's own spec order, trademarks used nominatively only, datasets authored not lifted.                                                                                                                                                  |
| Fourteen bodies authored serially stall the plan indefinitely.                                                           | Bodies within a band are content-independent (each writes only its own subtree) and pipeline concurrently through review, bounded by the in-force concurrency cap. Each band is its own phase with its own safe stopping point.                                                                                                                                                                                                                          |
