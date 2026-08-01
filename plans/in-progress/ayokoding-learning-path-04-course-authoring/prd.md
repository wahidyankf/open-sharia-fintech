# Product Requirements — Learning Path Course Authoring

## Product Overview

This plan authors **21 course bodies** of the shared course library — page bundles under
`apps/ayokoding-www/content/en/learn/courses/`, each a standalone, path-neutral building block with a
stable course ID, a canonical URL, a declared prerequisite list, a learning track, and a drilling
track. (This plan originally scoped 90 bodies; the remaining 69, plus the three course-surgery scope
contracts, are now carried by seven successor plans — see
[README §Successor plans](./README.md#successor-plans).)

A **course** is the unit of reading. A **path** is an ordered manifest of course IDs. This plan owns
the former and never the latter. Four **`careers/`** paths compose these bodies — the two
**`skills/`** domains and their corpora belong to the entry-point plans
[`ayokoding-learning-path-14-skills-accounting-foundations`](../../backlog/ayokoding-learning-path-14-skills-accounting-foundations/README.md)
(accounting, first of a 3-plan chain: 14 → 15 → 16) and
[`ayokoding-learning-path-17-skills-erp-foundations`](../../backlog/ayokoding-learning-path-17-skills-erp-foundations/README.md)
(ERP, first of a 2-plan chain: 17 → 18), and are explicitly **not** authored here:

- **`careers/interview-ready/software-engineer`** — the **interview/job-prep-first** arc for an
  experienced engineer re-entering the market: interview prep FIRST → production-effective → deeper.
- **`careers/immediately-effective/software-engineer`** — the **immediately-effective** arc:
  editor/tooling → one language end-to-end → **build a real app first** → then deepen.
- **`careers/fundamentally-strong/software-engineer`** — the **university-style, fundamentals-first**
  arc: CS foundations / theory first → deeper.
- **`careers/immediately-effective/ai-engineer`** — the **immediately-effective** arc aimed at a
  **distinct AI-engineering endpoint**. It teaches **building** AI systems (models, agents, evals,
  inference serving), not driving them (`agentic-coding` stays a separate, unrelated axis).

  > **Amended 2026-07-21 — this path is now from-scratch, not a role transition.** It previously
  > assumed an already-working software engineer and **linked** its prerequisite courses rather than
  > including them. That is overturned: the path assumes **no** prior software-engineering
  > competence, and its prerequisites are **included** in `courseOrder`. The consequence for this
  > plan is bounded — the included prerequisites are **existing library courses**, so no additional
  > body is authored here; the growth lands in the path's manifest, which
  > [`ayokoding-learning-path-13-careers-ai-manifest`](../../backlog/ayokoding-learning-path-13-careers-ai-manifest/README.md) owns.
  > **DD-24** ("fourth path's entry point: linked, not included, prerequisites") is superseded by
  > this amendment.

The library body is **content**, exempt from `specs:coverage`; the navigation feature that renders it
is app code and carries its `specs/` Gherkin companion in
[`ayokoding-learning-path-03-navigation-ui`](../../done/2026-07-25__ayokoding-learning-path-03-navigation-ui/README.md).
The acceptance criteria below are therefore **content-level** criteria, verified by the ayokoding
content checkers and by grep-checkable assertions on the authored bodies, not by application tests.

## Personas

Reproduced verbatim from the source plan. All four path personas are carried, not just the ones this
plan's bodies serve most directly — every authored course is reached by readers of all four paths.

- **Experienced engineer re-entering the job market (north-star for the
  `careers/interview-ready/software-engineer` path)** — recently laid off, returning from a gap/sabbatical, or
  an employed senior wanting to switch. Already owns the editor workflow and deep fundamentals; needs
  to **refresh breadth fast, relearn interview technique** at mid/senior/staff level, and handle a
  **layoff / employment-gap narrative** — without walking a from-scratch curriculum. Interview/job prep
  FIRST.
- **A builder who wants to be effective fast (north-star for the
  `careers/immediately-effective/software-engineer` path)** — wants "immediately effective" SWE: set up the
  editor, learn one language end-to-end, **ship a real app early**, then deepen into CS fundamentals,
  DS&A, algorithms, and systems. Serves both a from-scratch learner and a mid-career switcher.
- **A university-style, fundamentals-first learner (north-star for the
  `careers/fundamentally-strong/software-engineer` path)** — wants the rigorous bottom-up route: CS
  foundations, computer architecture, paradigms, and data structures & algorithms **before** building
  apps at scale. Prefers to understand the machine and the theory first, then apply it.
- **Someone entering AI engineering from scratch (north-star for the
  `careers/immediately-effective/ai-engineer` path, added 2026-07-20, re-scoped 2026-07-21)** — wants
  to become immediately effective at **building** AI systems (models, agents, evals, inference
  serving), not at driving coding agents. **Assumes no prior software-engineering competence**: the
  prerequisite courses are **included** in this path's `courseOrder`, not linked out, so the path
  stands alone. Converges on a distinct AI-engineering endpoint, not the other three paths' shared
  software-engineering endpoint. (Before 2026-07-21 this persona was an _already-working software
  engineer transitioning_ to AI engineering, with prerequisites linked rather than included; the
  re-scoping widened the audience and lengthened the manifest, but changed nothing this plan authors.)
- **A reader who lands on a shared course by deep-link / share** — arrives at a course URL without a
  path context and must get a coherent standalone view (with its prerequisites surfaced) plus an
  obvious way to enter a path.
- **Maintainer (content strategist / frontend engineer / content author / reviewer)** — owns the
  four-path architecture, builds the navigation feature, and authors the NEW courses via the ayokoding
  maker agents.

> The end-to-end **Learner Journey** walk-through is not duplicated here. It belongs to the three plans
> that build and populate that journey — see the
> [navigation-UI plan](../../done/2026-07-25__ayokoding-learning-path-03-navigation-ui/prd.md), the
> [SE manifests plan](../../backlog/ayokoding-learning-path-12-careers-se-manifests/prd.md), and the
> [AI manifest plan](../../backlog/ayokoding-learning-path-13-careers-ai-manifest/prd.md).

## User Stories

Scoped to this plan's surface — the course bodies themselves.

- As an **experienced engineer re-entering the market**, I want real interview-technique modules in a
  **refresh register** plus a layoff/gap-narrative section, so that I reload technique at my level
  instead of being taught concepts from zero.
- As **someone entering AI engineering from scratch**, I want six AI-specific courses that teach me
  to **build** AI systems (models, agents, evals, inference serving), so that I get an on-ramp to an
  AI-engineering endpoint that assumes no prior software-engineering competence. (Re-scoped
  2026-07-21; the entry assumption changed, the six courses did not. The prerequisites that make the
  path stand alone are **existing library courses** included in its `courseOrder` — the manifest
  grows, but this plan authors no additional body for them.)
- As a **reader of any AI-band course**, I want each course to state its scope boundary against the
  sibling it could be confused with, so that I never read a fourth treatment of material another
  course owns.
- As a **reader following the harness cluster**, I want each course to ship runnable typed-Python
  worked examples, so that I finish with a working agent rather than a description of one.
- As a **reader of the `agentic-ai` survey**, I want it to preview and forward-link each primitive
  rather than re-teaching it, so that I know where the depth lives and do not read the same material
  twice.
- As a **reader targeting an AI-agent-infra or security codebase**, I want the async-Python/FastAPI,
  CDP, MCP/harness, C++, and detection-engineering courses in the library, so that any path can lead
  me to the stack skills those codebases need.
- As a **security-track reader**, I want hands-on detection engineering to stay distinct from
  generalist defensive security, so that I can tell which course teaches breadth and which teaches
  the deep SIEM-ops tier.
- As a **reader who wants to self-host**, I want a light on-ramp course that explicitly says what it
  does **not** cover, so that I know when to graduate to clusters and IaC.
- As a **capstone reader**, I want each capstone to assemble named prerequisite courses into a
  runnable artefact with testable acceptance criteria, so that "done" is a thing I can run.
- As a **reader in a fast-moving domain**, I want volatile SDK/model/pricing specifics confined to
  dated accuracy-note sidebars, so that the course's durable spine stays correct as vendors change.
- As the **maintainer**, I want every body authored **from** its settled spec file, so that concept
  coverage and prerequisite edges are transcribed rather than re-invented.
- As the **maintainer**, I want course surgery (update / merge / split / create) to state its blast
  radius across all four manifests before it is applied, so that the library stays coherent as it
  grows without silently breaking another path.
- As the **downstream manifest author**, I want a complete, explicit band-completion signal naming
  every manifest I must grow, so that I never have to guess which paths a landed band affects.

## Acceptance Criteria (Gherkin)

This plan owns **four** scenarios: three routed from the source plan (covering Phase 1's AI-evals
courses and Band 2's self-hosting course), plus **one** scoped build-green scenario written to
replace the source's composite, unassignable `Scenario: The app builds and validates green` (which
conjoined the navigation feature and the interview-ready path in its `Given`, spanning two plans by
construction — see [README §Provenance](./README.md#provenance)).

> **Seven scenarios moved out with their content (removed from this section by this revision).** The
> interview-technique scenarios (behavioral course layoff/gap narrative; interview refresh register,
> Band 9), the harness-engineering-cluster scenarios (working agent from runnable code; agentic-ai
> forward-linking, Band 5), the detection-engineering-vs-defensive-security scenario (Band 7), and the
> two capstone scenarios (coding-agent; pentest-engine, Band 8) all describe content that is no longer
> authored by this plan. Each moved with its target band to the owning successor plan —
> `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness` (harness-cluster
> scenarios), `ayokoding-learning-path-08-course-authoring-security-and-ops` (detection-engineering
> scenario), `ayokoding-learning-path-09-course-authoring-interview-technique` (interview scenarios),
> and `ayokoding-learning-path-11-course-authoring-capstones` (capstone scenarios) — which restates
> the scenario verbatim in its own `prd.md` and binds it to its own `delivery.md`.

Every scenario below uses exactly one primary `Given`, one `When`, and one `Then`, with all extras
chained via `And` / `But`, per the
[Acceptance Criteria Convention](../../../repo-governance/development/infra/acceptance-criteria.md#step-keyword-cardinality-hard-rule).

### Productivity and self-hosting courses

```gherkin
Scenario: The light self-hosting course stays below clusters and IaC
  Given the self-hosting-essentials course is authored
  When a reader compares it with containers-and-orchestration and cloud-and-iac
  Then it teaches running one box, containerizing a service, a reverse proxy, and PaaS git-push deploy
  And its overview explicitly excludes clusters, Terraform/Packer/Ansible IaC, and Proxmox
```

### AI-engineering specialization courses

```gherkin
Scenario: The light eval gate and deep evals course do not overlap
  Given the light-eval-gate course and the deep-evals course are authored
  When a reader compares their overviews
  Then each overview states an explicit scope boundary against the other
  And neither course re-teaches the material the other owns
```

```gherkin
Scenario: The statistics-for-evals course stays scoped to what evals demand
  Given the statistics-for-evals course is authored
  When a reader compares it with analytics-and-experimentation
  Then it covers judge concordance and significance testing for evals only
  And it does not re-teach general product A/B testing, which stays analytics-and-experimentation's scope
```

### Scoped build-green (this plan's own surface)

```gherkin
Scenario: The authored course library builds and validates green
  Given every course body this plan authors has landed under the courses bucket
  When the ayokoding-www build, markdownlint, link validation, and heading-hierarchy validation run
  Then the build succeeds over the authored tree
  And link, heading-hierarchy, and markdownlint validation report no errors across the authored course bodies
```

## Scenario-to-delivery binding

Every scenario above binds to a named delivery step, in this plan's own [`delivery.md`](./delivery.md).

| Scenario                                                          | Binds to                                                    | Status         |
| ----------------------------------------------------------------- | ----------------------------------------------------------- | -------------- |
| The light eval gate and deep evals course do not overlap          | Phase 1 · `evaluating-ai-systems-in-depth` authoring step   | inherited bind |
| The statistics-for-evals course stays scoped to what evals demand | Phase 1 · `statistics-for-evaluation` authoring step        | inherited bind |
| The light self-hosting course stays below clusters and IaC        | Phase 4 (Band 2) · `self-hosting-essentials` authoring step | inherited bind |
| The authored course library builds and validates green            | Phase 5 · Section and Authored-Tree Verification            | new (scoped)   |

## NEW Course & Capstone Specifications

This plan authors **eight NEW courses + zero NEW capstones** — two Band-2 productivity courses
(`async-python-and-fastapi-services`, `self-hosting-essentials`) plus the **six NEW AI-specific
courses** for the `careers/immediately-effective/ai-engineer` path — alongside Band 1's **5**
transferred topics and Band 2's remaining **8** transferred topics (13 transferred total). The
original twenty-NEW-course figure (interview + productivity/harness/security clusters) and all nine
NEW capstones now belong to the successor plans named in
[README §Successor plans](./README.md#successor-plans): twelve of the twenty NEW courses (the four
interview courses, the five harness-cluster courses, `browser-automation-with-cdp`, `just-enough-cpp`,
and `detection-engineering-and-siem-operations`) and all nine NEW capstones moved out with Bands
5–9.

Each course is a full page-bundle (learning track + drilling track) matching the sibling plan's
per-topic anatomy and inheriting its cross-cutting authoring guarantees verbatim: accuracy-verified
via `web-researcher` before authoring; follow-along-complete; typed-Python where Python; colocated
runnable `code/`; exhaustive `co-NN`/`ex-NN` enumeration; `prerequisites` metadata plus navigation.
Every course declares its `prerequisites` so it takes its place in the library's prerequisite DAG.

**Full per-course concept / example / capstone detail lives in the cross-plan
[`syllabus/courses/` catalog](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md)**
(one file per course ID) — the specs below fix each course's purpose, register, and acceptance shape.
The catalog is the source of truth for authoring; these specs are not a substitute for it.

**Register.** This plan's two Band-2 NEW productivity courses and the six AI-specific courses
(2026-07-20) use the normal **first-learn By-Example register**. (The four interview-technique
courses' refresh register, and `just-enough-cpp`'s primer scope, describe content that moved out with
Bands 9 and 6 respectively — see the successor plans' own `prd.md` files.) Each AI-specific course
teaches **AI material only** and never re-teaches the SWE fundamentals the other three paths own — but
that scope boundary is a **body-level** rule, not an entry assumption about the reader. DD-24's
**links-not-included** entry
model is **superseded** by the 2026-07-21 re-scoping recorded above (see
[Product Overview](#product-overview)): the fourth path assumes **no** prior software-engineering
competence and **includes** its prerequisite courses in `courseOrder`. Those prerequisites are
existing library courses reached before the AI band begins, so the bodies authored here are
unchanged by the supersession.

**Principle-first framing (HARD).** Every course teaches a durable **principle**; target codebases
(`remotebrowser`, `wazuh`, `vacti*`, the ose family) are **illustrative worked-examples**, never the
subject.

**Volume-target bands** (inherited from the sibling; floor not cap):

| Course shape                                  | Concept floor (`co-NN`) | Worked-example band (`ex-NN`)         |
| --------------------------------------------- | ----------------------- | ------------------------------------- |
| By Example                                    | ≥ 10                    | 75–85 code examples                   |
| Primer (_Just Enough X_)                      | ≥ 8                     | 75–85 code examples (By-Example pace) |
| Annotated-concept, code-bearing               | ≥ 10                    | 45–60 worked examples                 |
| Annotated-concept, no-code (refresh register) | ≥ 8                     | 30–60 worked scenarios                |

> **Three specification sections moved out with their bands (removed from this section by this
> revision).** The interview-technique courses (Band 9), the harness-engineering cluster (Band 5,
> including `browser-automation-with-cdp`, which the source catalog places in Band 5 alongside the
> cluster rather than in Band 2), and the security & systems gap-closers (`just-enough-cpp` is
> Band 6; `detection-engineering-and-siem-operations` is Band 7) are no longer authored by this plan.
> Their specs move with their bands to
> `ayokoding-learning-path-09-course-authoring-interview-technique`,
> `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness`,
> `ayokoding-learning-path-07-course-authoring-low-level-systems`, and
> `ayokoding-learning-path-08-course-authoring-security-and-ops` respectively, each restating the
> relevant spec verbatim in its own `prd.md`. The NEW capstones section below is similarly removed in
> full — all nine NEW capstones are Band 8 or Band 9, neither owned here.

### Productivity & self-hosting courses (first-learn By-Example) — Band 2

- **`async-python-and-fastapi-services`** (By Example · Python) — async Python, FastAPI/Uvicorn,
  Pydantic, `uv`/`ruff`/`pyright`/`pytest-asyncio` — the `remotebrowser` + FastAPI-backend stack.
  Scoped tightly to the concrete framework + toolchain: async _concepts_ stay in
  `concurrency-and-parallelism`, framework _internals_ in `build-your-own-web-framework` — cross-linked,
  not re-derived.
- **`self-hosting-essentials`** (By Example · ops/config) — **light** on-ramp: one box, containerize,
  reverse proxy + TLS, systemd/ports, env/secrets, backups, PaaS git-push. Strictly below
  `containers-and-orchestration` / `cloud-and-iac`; distinct from `bare-metal-virtualization`.

### AI-engineering specialization courses (`careers/immediately-effective/ai-engineer` path, added 2026-07-20)

Six NEW courses for the fourth path, teaching **building** AI systems (not driving coding agents —
`agentic-coding` stays a separate axis, DD-21). Each is split into a **stable spine** (durable
principles) and **dated accuracy-note sidebars** (volatile SDK/model/pricing/framework specifics),
matching the pattern the existing AI-band courses already use (DD-28). **These six courses' specs are
now settled** — full concept (`co-NN`), worked-example (`ex-NN`), prerequisite-chain, and capstone
specs exist at
[`syllabus/courses/`](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md)
(one 295-425-line file per course); the format/language/prerequisite summaries below are drawn from
those settled files, not first-pass guesses. Author each course body **from** its
`syllabus/courses/<id>.md` spec (per DD-27's build order, this is authoring priority #1 behind the
interview-ready MVP).

- **Light eval gate** (`evaluating-ai-output-essentials` — Annotated-concept, Python) — a small, early
  course sitting right after the first working LLM call and before RAG/agents; answers "how will you
  know this works?" (DD-25).
- **Statistics for evals** (`statistics-for-evaluation` — Annotated-concept, code-bearing, Python) —
  scoped tightly to what evals demand (judge concordance, significance testing), not a general
  statistics survey; `analytics-and-experimentation` (classical product A/B testing) stays a scope
  mismatch and a candidate sibling/prerequisite rather than a merge target (DD-26). Declared a **hard
  prerequisite** of deep evals, so it is authored/placed before that course (see the manifest mirror at
  `syllabus/paths/manifest-immediately-effective-ai-engineer.md`).
- **Deep evals** (`evaluating-ai-systems-in-depth` — By Example, Python) — sits after agents; error
  analysis, task-specific criteria, LLM-as-judge with measured human agreement, CI gating, judge-scope
  reliability. Absorbs the three scattered evals treatments in `creating-ai-powered-apps`, `agentic-ai`,
  and `agent-orchestration-subagents-and-observability`, which are trimmed to forward-links rather than
  duplicating a fourth treatment (DD-25, DD-28).
- **Product patterns for probabilistic systems** (`product-patterns-for-probabilistic-systems` —
  Annotated-concept, no code) — product design patterns for systems whose outputs are probabilistic
  rather than deterministic; no course owns this today (DD-28).
- **Inference serving and model deployment** (`inference-serving-and-model-deployment` — By Example,
  Python) — vLLM/TGI, KV-cache, batching, GPU considerations; entirely absent from the library today
  (DD-28).
- **Fine-tuning and adaptation** (`fine-tuning-and-adaptation` — By Example, Python) —
  fine-tuning/LoRA/PEFT versus RAG as a foil; `fine-tun*` appears once library-wide today, as a RAG
  comparison point, never its own course (DD-28).

The scope boundary between the light eval gate and deep evals is stated explicitly in both courses'
overviews, in the style of the existing AI-band scope-guard (DD-10/DD-11), to avoid reproducing that
cluster's overlap problem.

## Product Scope

**In-scope**:

- Authoring **21 course page bundles** under `apps/ayokoding-www/content/en/learn/courses/<course-id>/`,
  each with `_index.md` (declaring `prerequisites`), `overview.md`, a `learning/` track (concepts,
  worked examples, colocated runnable `code/` where code-bearing, and `learning/capstone/`), and a
  `drilling/` track in the fixed five-section order.
- Declaring each body's `prerequisites` in the contracted frontmatter shape, transcribed from its
  settled spec.
- Stating each body's **scope boundary** against any sibling course it could be confused with.
- Adding this plan's authored courses to the tracked
  [Course Library Catalog](./tech-docs.md#course-library-catalog) as real rows.
- Updating `<COURSES>_index.md` to list every authored course.
- Emitting one complete **band-completion signal** per band (three total: Phase 1, Band 1, Band 2).
- Manual behavioural verification of a sample of authored course pages via Playwright MCP, with
  committed screenshot evidence in `evidence/`.

**Out of scope**:

- **Any manifest file** under `<MANIFESTS>` — creating, appending to, reordering, or re-verifying.
  Owned by `ayokoding-learning-path-12-careers-se-manifests` and its sibling
  `ayokoding-learning-path-13-careers-ai-manifest`. Binding invariant.
- **Any path landing anchor** under `<PATHS>` and the paths hub — owned by the manifest and
  navigation-UI plans.
- **Any `course-paths` feature code** (`core/` or `shell/`) — owned by the schema and navigation-UI
  plans.
- **Any redirect module or rule** — owned by `ayokoding-learning-path-01-url-restructure`.
- **The 33 shipped topics and the 4 existing capstones** (including `capstone-solid-core`) — re-homed,
  not authored, by `ayokoding-learning-path-01-url-restructure`.
- **Bands 3–9 (69 course bodies) and the three course-surgery contracts** — carried by the seven
  successor plans; see [README §Successor plans](./README.md#successor-plans).
- **The `prerequisites` frontmatter contract's definition** — consumed here, owned by the schema plan.
- **The `syllabus/` folder** — read-only from this plan; never copied.
- **Any Indonesian (`id`) course content** — explicitly deferred.
- **The UI design funnel** (Screens 0–4) — this plan is not UI-bearing; see
  [tech-docs §UI-design-funnel exemption](./tech-docs.md#ui-design-funnel-exemption-not-ui-bearing).
- **The rule-15 three-tester retest** — exemption recorded with reasons in
  [README §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded).

## Product-Level Risks

- **A body authored from judgment rather than its spec.** Concept coverage silently drops and
  prerequisite edges get invented. Mitigated by naming the exact cross-plan spec path in every
  authoring step and making "authored from that spec" an explicit acceptance criterion.
- **A prerequisite edge invented at authoring time.** The failure does not surface here — it surfaces
  in the manifest plan as an integrity failure with no trace back. Mitigated by transcribing the
  declared chain rather than re-deriving it.
- **Volatile facts in the stable spine.** SDK, model, pricing, and framework specifics age within
  months. Mitigated by DD-28's durability constraint: volatile facts live only in dated accuracy-note
  sidebars, enforced per-course by the accuracy pre-verify step and re-checked by the facts checker.
  (This still applies to Phase 1's six AI-specific courses, authored here.)
- **A natively-authored slug colliding with a not-yet-moved re-home slug.** Two courses would silently
  share one canonical URL. Mitigated by running the 29-new-slug collision check against a **populated**
  namespace — which is why the URL-restructure plan is a hard prerequisite.
- **A manifest-mutating step reintroduced into this plan.** Makes the wave order unschedulable.
  Mitigated by the invariant being stated in three documents plus a phase-gate check that the plan's
  diff touches zero `<MANIFESTS>` paths.
- **A vague band-completion signal.** The manifest plan cannot act on it and either stalls or guesses.
  Mitigated by the five-field signal contract, with an explicit rejection rule for incomplete signals.
- **Q-A ruled late, forcing a supersession sweep.** Mitigated by proceeding without the supersession
  line, recording the pending obligation, and scoping the sweep to only the courses a legacy page
  covers.
- **Per-role convergence confusion.** A reader of this plan alone could read "course surgery
  permitted" (DD-28) as "body forking permitted". Mitigated by DD-28's copy here restating DD-7's
  surviving half and carrying a working cross-plan link to DD-7 in the manifest plan — see
  [tech-docs DD-28](./tech-docs.md#design-decisions).
- **Twenty-one bodies authored serially stalling the plan.** Mitigated by band-per-phase structure
  with independent safe stopping points and concurrent review pipelining bounded by the in-force cap.

> Three risks moved out with Band 5 (removed from this list by this revision): duplication creep in
> the AI band (survey re-teaching the harness cluster, or a fourth evals treatment), contested
> "harness engineering" terminology (DD-29), and the unsourced 42%→78% scaffold-swing figure (DD-30).
> `ayokoding-learning-path-06-course-authoring-architecture-and-ai-harness` restates the equivalent
> risks in its own `prd.md`.
