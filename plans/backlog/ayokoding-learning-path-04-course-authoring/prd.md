# Product Requirements — Learning Path Course Authoring

## Product Overview

This plan authors the **course bodies** of the shared course library — 90 page bundles under
`apps/ayokoding-www/content/en/learn/courses/`, each a standalone, path-neutral building block with a
stable course ID, a canonical URL, a declared prerequisite list, a learning track, and a drilling
track.

A **course** is the unit of reading. A **path** is an ordered manifest of course IDs. This plan owns
the former and never the latter. Four paths compose these bodies:

- **`interview-ready/software-engineer`** — the **interview/job-prep-first** arc for an experienced
  engineer re-entering the market: interview prep FIRST → production-effective → deeper.
- **`immediately-effective/software-engineer`** — the **immediately-effective** arc: editor/tooling →
  one language end-to-end → **build a real app first** → then deepen.
- **`fundamentally-strong/software-engineer`** — the **university-style, fundamentals-first** arc:
  CS foundations / theory first → deeper.
- **`immediately-effective/software-engineer-to-ai-engineer`** — the **immediately-effective** arc
  applied to a **role transition**: assumes an already-working software engineer; prerequisite courses
  are **linked, not included**; teaches **building** AI systems (models, agents, evals, inference
  serving), not driving them (`agentic-coding` stays a separate, unrelated axis).

The library body is **content**, exempt from `specs:coverage`; the navigation feature that renders it
is app code and carries its `specs/` Gherkin companion in
[`ayokoding-learning-path-03-navigation-ui`](../ayokoding-learning-path-03-navigation-ui/README.md).
The acceptance criteria below are therefore **content-level** criteria, verified by the ayokoding
content checkers and by grep-checkable assertions on the authored bodies, not by application tests.

## Personas

Reproduced verbatim from the source plan. All four path personas are carried, not just the ones this
plan's bodies serve most directly — every authored course is reached by readers of all four paths.

- **Experienced engineer re-entering the job market (north-star for the
  `interview-ready/software-engineer` path)** — recently laid off, returning from a gap/sabbatical, or
  an employed senior wanting to switch. Already owns the editor workflow and deep fundamentals; needs
  to **refresh breadth fast, relearn interview technique** at mid/senior/staff level, and handle a
  **layoff / employment-gap narrative** — without walking a from-scratch curriculum. Interview/job prep
  FIRST.
- **A builder who wants to be effective fast (north-star for the
  `immediately-effective/software-engineer` path)** — wants "immediately effective" SWE: set up the
  editor, learn one language end-to-end, **ship a real app early**, then deepen into CS fundamentals,
  DS&A, algorithms, and systems. Serves both a from-scratch learner and a mid-career switcher.
- **A university-style, fundamentals-first learner (north-star for the
  `fundamentally-strong/software-engineer` path)** — wants the rigorous bottom-up route: CS
  foundations, computer architecture, paradigms, and data structures & algorithms **before** building
  apps at scale. Prefers to understand the machine and the theory first, then apply it.
- **An already-working software engineer transitioning to AI engineering (north-star for the
  `immediately-effective/software-engineer-to-ai-engineer` path, added 2026-07-20)** — already owns the
  SWE fundamentals the other three paths teach; wants to become immediately effective at **building**
  AI systems (models, agents, evals, inference serving), not at driving coding agents. Prerequisite
  courses are **linked, not included** in this path's manifest. Converges on a distinct AI-engineering
  endpoint, not the other three paths' shared software-engineering endpoint.
- **A reader who lands on a shared course by deep-link / share** — arrives at a course URL without a
  path context and must get a coherent standalone view (with its prerequisites surfaced) plus an
  obvious way to enter a path.
- **Maintainer (content strategist / frontend engineer / content author / reviewer)** — owns the
  four-path architecture, builds the navigation feature, and authors the NEW courses via the ayokoding
  maker agents.

> The end-to-end **Learner Journey** walk-through is not duplicated here. It belongs to the two plans
> that build and populate that journey — see the
> [navigation-UI plan](../ayokoding-learning-path-03-navigation-ui/prd.md) and the
> [manifest plan](../ayokoding-learning-path-05-manifests/prd.md).

## User Stories

Scoped to this plan's surface — the course bodies themselves.

- As an **experienced engineer re-entering the market**, I want real interview-technique modules in a
  **refresh register** plus a layoff/gap-narrative section, so that I reload technique at my level
  instead of being taught concepts from zero.
- As an **already-working software engineer moving into AI engineering**, I want six AI-specific
  courses that teach me to **build** AI systems, so that I get an on-ramp that assumes the SWE
  competence I already have.
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

This plan owns **ten** scenarios routed from the source plan, plus **one** scoped build-green
scenario written to replace the source's composite, unassignable
`Scenario: The app builds and validates green` (which conjoined the navigation feature and the
interview-ready path in its `Given`, spanning two plans by construction — see
[README §Provenance](./README.md#provenance)).

Every scenario below uses exactly one primary `Given`, one `When`, and one `Then`, with all extras
chained via `And` / `But`, per the
[Acceptance Criteria Convention](../../../repo-governance/development/infra/acceptance-criteria.md#step-keyword-cardinality-hard-rule).

### Interview-technique courses

```gherkin
Scenario: The behavioral course covers the layoff and employment-gap narrative
  Given the behavioral-and-leadership-interviews course is authored
  When an experienced re-entrant reads its learning track
  Then it explicitly covers framing an employment gap, a layoff, or a re-entry story
  And it treats senior/staff/EM leadership rounds as core material
```

```gherkin
Scenario: Interview courses are written in a refresh register
  Given the four new interview-technique courses are authored
  When an experienced engineer reads them
  Then each assumes prior professional experience and focuses on interview technique and breadth refresh
  And none teaches core concepts from zero
```

### Productivity and self-hosting courses

```gherkin
Scenario: The light self-hosting course stays below clusters and IaC
  Given the self-hosting-essentials course is authored
  When a reader compares it with containers-and-orchestration and cloud-and-iac
  Then it teaches running one box, containerizing a service, a reverse proxy, and PaaS git-push deploy
  And its overview explicitly excludes clusters, Terraform/Packer/Ansible IaC, and Proxmox
```

### Harness-engineering cluster

```gherkin
Scenario: The harness cluster builds a working agent from runnable code
  Given the five harness-engineering courses are authored
  When a reader builds an agent from them
  Then the agent loop, tools/MCP, memory, permissions, and orchestration each ship runnable typed-Python examples
  And each course names remotebrowser's bundled MCP or CDP browser only as an illustrative pickup
```

```gherkin
Scenario: The agentic-ai survey forward-links each primitive without re-teaching it
  Given the agentic-ai survey course and the five harness-cluster courses are authored
  When a reader reads the agentic-ai survey
  Then it previews the agent loop, tools/MCP, memory/context, and evals and forward-links each to its cluster course
  And it does not re-teach any primitive at build-your-own depth
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

### Security and systems gap-closers

```gherkin
Scenario: Hands-on detection engineering stays distinct from generalist defensive security
  Given the detection-engineering-and-siem-operations course is authored
  When a reader compares it with the hands-on defensive-security course
  Then it has the reader author working Wazuh decoders, correlation rules, and a dashboard with false-positive tuning
  And defensive-security keeps the generalist Sigma/ELK breadth, IR, and hardening as its distinct scope
```

### Capstones

```gherkin
Scenario: The coding-agent capstone assembles the harness cluster into a working CLI
  Given the harness cluster and the build-your-own-coding-agent capstone are authored
  When a reader completes the capstone
  Then they have a runnable coding-agent CLI built from the agent loop, tools/MCP, memory, permissions, and orchestration courses
  And a disallowed action fails closed while every run emits a trace
```

```gherkin
Scenario: The pentest-engine capstone assembles the convergence track into a scoped engine
  Given the harness cluster, the CDP course, the security suite, and detection-engineering are authored
  When a reader completes the build-your-own-pentest-engine capstone
  Then they have a runnable engine from swarm orchestration, MCP tooling, CDP browser driving, and security-tool-chaining
  And scope enforcement refuses an out-of-scope target while the capstone uses vacti-pentest-engine only as an illustration
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

Every scenario above binds to a named delivery step. The five marked **newly bound** reached no
delivery step in the source plan and would have been silently dropped by the split; each now carries
a `**Gherkin (binds) →**` marker plus its verbatim fenced block on the named step in
[`delivery.md`](./delivery.md).

| Scenario                                                                         | Binds to                                                                                       | Status          |
| -------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- | --------------- |
| The light eval gate and deep evals course do not overlap                         | Phase 1 · `evaluating-ai-systems-in-depth` authoring step                                      | inherited bind  |
| The statistics-for-evals course stays scoped to what evals demand                | Phase 1 · `statistics-for-evaluation` authoring step                                           | inherited bind  |
| The light self-hosting course stays below clusters and IaC                       | Phase 4 (Band 2) · `self-hosting-essentials` authoring step                                    | inherited bind  |
| Hands-on detection engineering stays distinct from generalist defensive security | Phase 9 (Band 7) · `detection-engineering-and-siem-operations` step                            | inherited bind  |
| The behavioral course covers the layoff and employment-gap narrative             | Phase 11 (Band 9) · `behavioral-and-leadership-interviews` step                                | inherited bind  |
| The agentic-ai survey forward-links each primitive without re-teaching it        | Phase 7 (Band 5) · `agentic-ai` authoring step                                                 | **newly bound** |
| The harness cluster builds a working agent from runnable code                    | Phase 7 (Band 5) · `agent-orchestration-subagents-and-observability` step (closes the cluster) | **newly bound** |
| The coding-agent capstone assembles the harness cluster into a working CLI       | Phase 10 (Band 8) · `capstone-build-your-own-coding-agent` step                                | **newly bound** |
| The pentest-engine capstone assembles the convergence track into a scoped engine | Phase 10 (Band 8) · `capstone-build-your-own-pentest-engine` step                              | **newly bound** |
| Interview courses are written in a refresh register                              | Phase 11 (Band 9) · the four interview-technique authoring steps                               | **newly bound** |
| The authored course library builds and validates green                           | Phase 12 · Section and App Verification                                                        | new (scoped)    |

## NEW Course & Capstone Specifications

This plan authors **twenty NEW courses + eight NEW capstones** — the original fourteen (interview +
productivity/harness/security clusters) plus **six further NEW AI-specific courses** added 2026-07-20
for the `software-engineer-to-ai-engineer` path, plus eight capstones (two original plus six of the
seven DD-20 inter-topic capstones; the seventh, `capstone-solid-core`, is already live on disk and is
re-homed by `ayokoding-learning-path-01-url-restructure`, not authored here) — alongside the 61
transferred topics authored native.

Each course is a full page-bundle (learning track + drilling track) matching the sibling plan's
per-topic anatomy and inheriting its cross-cutting authoring guarantees verbatim: accuracy-verified
via `web-researcher` before authoring; follow-along-complete; typed-Python where Python; colocated
runnable `code/`; exhaustive `co-NN`/`ex-NN` enumeration; `prerequisites` metadata plus navigation.
Every course declares its `prerequisites` so it takes its place in the library's prerequisite DAG.

**Full per-course concept / example / capstone detail lives in the cross-plan
[`syllabus/courses/` catalog](../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md)**
(one file per course ID) — the specs below fix each course's purpose, register, and acceptance shape.
The catalog is the source of truth for authoring; these specs are not a substitute for it.

**Register.** The four interview-technique courses use a **refresh register** (assume prior
professional experience; reload technique, do not teach from zero). The ten productivity/harness/
security courses and the six AI-specific courses (2026-07-20) use the normal **first-learn By-Example
register**; `just-enough-cpp` is primer scope. The AI-specific courses additionally use the
**links-not-included** entry model: they assume the reader already has the SWE fundamentals the other
three paths teach (DD-24) — the courses themselves teach AI material only, they do not re-teach the
linked prerequisites.

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

### Interview-technique courses (refresh register)

- **`coding-interview`** (By Example · Python, patterns language-agnostic) — reload LeetCode-style
  pattern recognition + time-boxed problem-solving; hosts the 2026 senior interview-loop-map.
- **`take-home-and-live-coding`** (By Example · Python) — time-boxed take-home + observed live/pair
  technique: scope, test, README hygiene, thinking aloud.
- **`system-design-interview`** (Annotated-concept · no code) — the senior/staff system-design
  interview rubric + whiteboard flow; forward-links the depth course `system-design`.
- **`behavioral-and-leadership-interviews`** (Annotated-concept · no code) — STAR + senior/staff/EM
  rounds AND framing an **employment-gap / layoff / re-entry** narrative.

### Productivity & self-hosting courses (first-learn By-Example)

- **`async-python-and-fastapi-services`** (By Example · Python) — async Python, FastAPI/Uvicorn,
  Pydantic, `uv`/`ruff`/`pyright`/`pytest-asyncio` — the `remotebrowser` + FastAPI-backend stack.
  Scoped tightly to the concrete framework + toolchain: async _concepts_ stay in
  `concurrency-and-parallelism`, framework _internals_ in `build-your-own-web-framework` — cross-linked,
  not re-derived.
- **`self-hosting-essentials`** (By Example · ops/config) — **light** on-ramp: one box, containerize,
  reverse proxy + TLS, systemd/ports, env/secrets, backups, PaaS git-push. Strictly below
  `containers-and-orchestration` / `cloud-and-iac`; distinct from `bare-metal-virtualization`.
- **`browser-automation-with-cdp`** (By Example · Python) — Chrome DevTools Protocol browser
  automation (port 9222; nodriver/zendriver family) — the core `remotebrowser` skill. Distinct from
  `software-testing`'s Playwright E2E: raw CDP automation, not a test runner.

### Harness-engineering cluster (first-learn By-Example · Python)

The five build-your-own-agentic-coding-tool courses; the MCP built in `agent-tools-and-mcp` is the same
MCP `remotebrowser` exposes; all feed `capstone-build-your-own-coding-agent`. **AI-band scope-guard**:
these build the primitives at build-your-own depth; the survey course `agentic-ai` (57) previews and
**forward-links** each primitive here and does NOT re-teach at cluster depth, and
`creating-ai-powered-apps` (56) stays at the _use-an-LLM-in-an-app_ altitude.

- **`the-agent-loop`** — the LLM read-eval-act tool-use loop, streaming, stop conditions.
- **`agent-tools-and-mcp`** — tool/function schema design; an MCP server + client; resources/prompts.
- **`agent-context-and-memory`** (Annotated-concept) — context budgeting, compaction, retrieval,
  persistent memory.
- **`agent-permissions-and-sandboxing`** — approval models, sandboxed execution, guardrails,
  fail-closed defaults.
- **`agent-orchestration-subagents-and-observability`** (Annotated-concept) — subagents, background
  tasks, hooks/skills systems, a TUI, evals + tracing/telemetry.

### AI-engineering specialization courses (`software-engineer-to-ai-engineer` path, added 2026-07-20)

Six NEW courses for the fourth path, teaching **building** AI systems (not driving coding agents —
`agentic-coding` stays a separate axis, DD-21). Each is split into a **stable spine** (durable
principles) and **dated accuracy-note sidebars** (volatile SDK/model/pricing/framework specifics),
matching the pattern the existing AI-band courses already use (DD-28). **These six courses' specs are
now settled** — full concept (`co-NN`), worked-example (`ex-NN`), prerequisite-chain, and capstone
specs exist at
[`syllabus/courses/`](../ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/README.md)
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
  `syllabus/paths/manifest-immediately-effective-software-engineer-to-ai-engineer.md`).
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

### Security & systems gap-closers

- **`just-enough-cpp`** (Primer · C++) — systems-language principle on-ramp (RAII, templates/generics,
  STL, smart pointers, manual memory); prereq `just-enough-c`; Wazuh's C++ core is one illustration.
- **`detection-engineering-and-siem-operations`** (By Example · XML/rules + config + Python) —
  decoders, correlation rules, log parsing/normalization, FP tuning, dashboards, alert triage; Wazuh
  XML is the worked example. Distinct from `defensive-security` (which is **hands-on By-Example**
  generalist blue-team breadth — Sigma/ELK + IR + hardening, **not** concept-level); prereq
  `defensive-security`.

### NEW capstones

Capstones follow the sibling's capstone-policy shape (goal/outcome, concepts-exercised checklist,
ordered step outline, testable acceptance criteria, done bar = runnable end-to-end + web-verified).

- **`capstone-interview-loop`** (Python + prose) — a full mock interview loop (coding + system-design +
  behavioral incl. gap narrative), each round self-scored against its module rubric.
- **`capstone-build-your-own-coding-agent`** (Python) — assemble the harness cluster into a working
  minimal coding-agent CLI; bonus path drives `remotebrowser` over MCP.
- **`capstone-build-your-own-pentest-engine`** (TypeScript default) — assemble swarm orchestration +
  MCP tool arsenal + CDP browser driving + security-tool-chaining + evidence pipeline + scope
  enforcement + deterministic-prober-vs-AI-verifier into a working engine; `vacti-pentest-engine` is
  the illustration. **Lab-local, authorized-scope-only** — inherits `offensive-security`'s
  rules-of-engagement guard; the body must restate scope and authorization limits.

The six DD-20 inter-topic capstones authored here (`capstone-real-world-delivery`,
`capstone-secure-service`, `capstone-data-pipeline`, `capstone-concurrency-and-systems`,
`capstone-concurrency-showdown`, `capstone-lead-at-altitude`) have fully-specified specs embedded
inside their host course spec files under the cross-plan `syllabus/courses/` folder — see
[tech-docs DD-20](./tech-docs.md#design-decisions) for the host mapping.

## Product Scope

**In-scope**:

- Authoring **90 course page bundles** under `apps/ayokoding-www/content/en/learn/courses/<course-id>/`,
  each with `_index.md` (declaring `prerequisites`), `overview.md`, a `learning/` track (concepts,
  worked examples, colocated runnable `code/` where code-bearing, and `learning/capstone/`), and a
  `drilling/` track in the fixed five-section order.
- Declaring each body's `prerequisites` in the contracted frontmatter shape, transcribed from its
  settled spec.
- Stating each body's **scope boundary** against any sibling course it could be confused with.
- Locking and applying the three **course-surgery contracts** (evals forward-link, D9
  naming/citation, D11 concept additions), including their four-path blast-radius statement.
- Adding this plan's authored courses to the tracked
  [Course Library Catalog](./tech-docs.md#course-library-catalog) as real rows.
- Updating `<COURSES>_index.md` to list every authored course.
- Emitting one complete **band-completion signal** per band.
- Manual behavioural verification of a sample of authored course pages via Playwright MCP, with
  committed screenshot evidence in `evidence/`.

**Out of scope**:

- **Any manifest file** under `<MANIFESTS>` — creating, appending to, reordering, or re-verifying.
  Owned by `ayokoding-learning-path-05-manifests`. Binding invariant.
- **Any path landing anchor** under `<PATHS>` and the paths hub — owned by the manifest and
  navigation-UI plans.
- **Any `course-paths` feature code** (`core/` or `shell/`) — owned by the schema and navigation-UI
  plans.
- **Any redirect module or rule** — owned by `ayokoding-learning-path-01-url-restructure`.
- **The 33 shipped topics and the 4 existing capstones** (including `capstone-solid-core`) — re-homed,
  not authored, by `ayokoding-learning-path-01-url-restructure`.
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
- **Duplication creep in the AI band.** The band's largest historical risk: the survey re-teaching
  what the cluster owns, or a fourth evals treatment appearing. Mitigated by the AI-band scope-guard
  and the evals forward-link contract, both as grep-checkable acceptance criteria on the authoring
  steps themselves.
- **Volatile facts in the stable spine.** SDK, model, pricing, and framework specifics age within
  months. Mitigated by DD-28's durability constraint: volatile facts live only in dated accuracy-note
  sidebars, enforced per-course by the accuracy pre-verify step and re-checked by the facts checker.
- **Contested terminology adopted as course structure.** "Harness engineering" is young and disputed
  among named practitioners. Mitigated by DD-29: cite the disagreement, rename nothing, add no course.
- **An unsourced figure cited as fact.** Mitigated by DD-30's explicit do-not-cite ruling on the
  42%→78% scaffold-swing figure and by labelling the competence-floor reconciliation a synthesis no
  single source makes.
- **A natively-authored slug colliding with a not-yet-moved re-home slug.** Two courses would silently
  share one canonical URL. Mitigated by running the 23-new-slug collision check against a **populated**
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
- **Ninety bodies authored serially stalling the plan.** Mitigated by band-per-phase structure with
  independent safe stopping points and concurrent review pipelining bounded by the in-force cap.
  </content>
