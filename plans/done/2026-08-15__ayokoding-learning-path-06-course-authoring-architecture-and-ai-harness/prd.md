# Product Requirements — Course Authoring: Architecture, Distributed & AI/Harness (Band 5)

## Product Overview

This plan authors **Band 5** of the shared course library — 15 page bundles under
`apps/ayokoding-www/content/en/learn/courses/`, each a standalone, path-neutral building block with a
stable course ID, a canonical URL, a declared prerequisite list, a learning track, and a drilling
track.

A **course** is the unit of reading. A **path** is an ordered manifest of course IDs. This plan owns
the former and never the latter. Every `careers/` path manifest that composes these 15 bodies is
owned by the successor manifest-growth plans
([`ayokoding-learning-path-12-careers-se-manifests`](../../backlog/ayokoding-learning-path-12-careers-se-manifests/README.md),
[`ayokoding-learning-path-13-careers-ai-manifest`](../../backlog/ayokoding-learning-path-13-careers-ai-manifest/README.md)).

The library body is **content**, exempt from `specs:coverage`; the navigation feature that renders it
is app code owned by
[`ayokoding-learning-path-03-navigation-ui`](../../done/2026-07-25__ayokoding-learning-path-03-navigation-ui/README.md).
The acceptance criteria below are **content-level** criteria, verified by the ayokoding content
checkers and by grep-checkable assertions on the authored bodies, not by application tests.

## Personas

Reproduced from the parent plan; all four path personas are carried, since every authored course is
reached by readers of all four paths.

- **A builder who wants to be effective fast** (`careers/immediately-effective/software-engineer`) —
  reaches architecture and distributed-systems depth after shipping a real app early.
- **A university-style, fundamentals-first learner**
  (`careers/fundamentally-strong/software-engineer`) — reaches this band's architecture and
  distributed-systems material as part of the deeper CS-and-systems arc.
- **An experienced engineer re-entering the job market**
  (`careers/interview-ready/software-engineer`) — reaches this band's `system-design` course as the
  depth sibling of the interview-technique `system-design-interview` course.
- **Someone entering AI engineering from scratch** (`careers/immediately-effective/ai-engineer`) —
  the north-star for 8 of this plan's 15 courses: wants to become immediately effective at
  **building** AI systems (models, agents, evals, inference serving), not at driving coding agents.
  Assumes no prior software-engineering competence; the path's prerequisite courses are included in
  its `courseOrder`, not linked out.
- **A reader who lands on a shared course by deep-link / share** — arrives at a course URL without a
  path context and must get a coherent standalone view (with its prerequisites surfaced).
- **Maintainer** (content strategist / content author / reviewer) — authors the 15 bodies via the
  ayokoding maker agents and owns the three course-surgery contracts.

## User Stories

Scoped to this plan's surface — the 15 course bodies and the three contracts.

- As a **reader reaching architecture depth**, I want `software-architecture`, `domain-driven-design`,
  `system-design`, `event-driven-architecture`, and `distributed-systems` authored from their settled
  specs, so that I get concept coverage and worked examples matching what the library committed to.
- As **someone entering AI engineering from scratch**, I want `creating-ai-powered-apps` and
  `agentic-ai` authored with an explicit use-an-LLM-vs-survey scope split, so that I know which course
  teaches "use an LLM in an app" and which previews the harness cluster without re-teaching it.
- As a **reader following the harness cluster**, I want `the-agent-loop`, `agent-tools-and-mcp`,
  `agent-context-and-memory`, `agent-permissions-and-sandboxing`, and
  `agent-orchestration-subagents-and-observability` to each ship runnable typed-Python worked
  examples, so that I finish with a working agent rather than a description of one.
- As a **reader of the `agentic-ai` survey**, I want it to preview and forward-link each harness
  primitive rather than re-teaching it, so that I know where the depth lives and do not read the same
  material twice.
- As a **reader of any of the three evals-donor courses** (`creating-ai-powered-apps`, `agentic-ai`,
  `agent-orchestration-subagents-and-observability`), I want each to forward-link the deep-evals
  course rather than re-teach evals, so that the library's evals material has a single owner.
- As a **reader of `agent-context-and-memory`**, I want the context-engineering naming/lineage
  citation present, so that I connect the material to current job-market vocabulary without the
  course adopting unsettled terminology as structure.
- As a **reader of the harness cluster or the coding-agent capstone**, I want the
  harness-engineering naming/lineage citation present, citing the containment dispute as unresolved,
  so that the material is durable regardless of which side of the naming debate eventually wins.
- As a **reader of `agent-tools-and-mcp`**, I want tool-count degradation and tool-result token
  efficiency covered as named concepts, so that I know when to split a tool surface across subagents
  and how a tool's result shape is a context-budget decision.
- As a **reader of `agent-permissions-and-sandboxing`**, I want the train-vs-production permission
  asymmetry covered as a named concept, so that I understand the distinction is about risk, not model
  capability.
- As the **maintainer**, I want every body authored **from** its settled spec file, so that concept
  coverage and prerequisite edges are transcribed rather than re-invented.
- As the **downstream manifest-growth plans**, I want a complete, explicit band-completion signal
  naming every manifest to grow, so that I never have to guess which paths this band affects.

## Acceptance Criteria (Gherkin)

Every scenario below uses exactly one primary `Given`, one `When`, and one `Then`, with all extras
chained via `And`/`But`, per the
[Acceptance Criteria Convention](../../../repo-governance/development/infra/acceptance-criteria/gherkin-format-and-step-keyword-cardinality.md#step-keyword-cardinality-hard-rule).

### AI on-ramp and harness cluster

```gherkin
Scenario: The agentic-ai survey forward-links each primitive without re-teaching it
  Given the agentic-ai survey course and the five harness-cluster courses are authored
  When a reader reads the agentic-ai survey
  Then it previews the agent loop, tools/MCP, memory/context, and evals and forward-links each to its cluster course
  And it does not re-teach any primitive at build-your-own depth
```

```gherkin
Scenario: The harness cluster builds a working agent from runnable code
  Given the five harness-engineering courses are authored
  When a reader builds an agent from them
  Then the agent loop, tools/MCP, memory, permissions, and orchestration each ship runnable typed-Python examples
  And each course names remotebrowser's bundled MCP or CDP browser only as an illustrative pickup
```

### Course-surgery contracts

```gherkin
Scenario: The three evals-donor courses forward-link the deep-evals course
  Given creating-ai-powered-apps, agentic-ai, and agent-orchestration-subagents-and-observability are authored
  When a reader reads each course's evals-adjacent material
  Then each forward-links evaluating-ai-systems-in-depth rather than re-teaching evals content
  And no donor course duplicates the deep-evals course's error-analysis or LLM-as-judge material
```

```gherkin
Scenario: The harness cluster cites context engineering and harness engineering without renaming a course
  Given agent-context-and-memory and the five harness-cluster courses are authored
  When a reader reads their overviews
  Then agent-context-and-memory names the context-engineering lineage citing Lütke, Karpathy, Willison, and Anthropic
  And the harness cluster names the harness-engineering lineage citing Anthropic and Böckeler/Thoughtworks as an unresolved naming dispute
```

```gherkin
Scenario: The four D11 concept additions land inside their named existing courses
  Given agent-context-and-memory, agent-tools-and-mcp, and agent-permissions-and-sandboxing are authored
  When a reader reads each course's concept coverage
  Then agent-context-and-memory covers cache-aware prefix ordering as a stable-before-variable principle
  And agent-tools-and-mcp covers tool-count degradation and tool-result token efficiency, and agent-permissions-and-sandboxing covers the train-vs-production permission asymmetry as a risk distinction
```

### Scoped build-green (this plan's own surface)

```gherkin
Scenario: The Band-5 course library builds and validates green
  Given all 15 course bodies this plan authors have landed under the courses bucket
  When the ayokoding-www build, markdownlint, link validation, and heading-hierarchy validation run
  Then the build succeeds over the authored tree
  And link, heading-hierarchy, and markdownlint validation report no errors across the 15 authored course bodies
```

## Scenario-to-delivery binding

| Scenario                                                                                        | Binds to                                                                                                                        |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| The agentic-ai survey forward-links each primitive without re-teaching it                       | Phase 3 (Cohort 2) · `agentic-ai` authoring step                                                                                |
| The harness cluster builds a working agent from runnable code                                   | Phase 4 (Cohort 3) · `agent-orchestration-subagents-and-observability` step (closes the cluster)                                |
| The three evals-donor courses forward-link the deep-evals course                                | Phase 1 (contract lock) + Phase 3/4 (donor authoring steps)                                                                     |
| The harness cluster cites context engineering and harness engineering without renaming a course | Phase 1 (contract lock) + Phase 4 (`agent-context-and-memory`, `the-agent-loop` steps)                                          |
| The four D11 concept additions land inside their named existing courses                         | Phase 1 (contract lock) + Phase 4 (`agent-context-and-memory`, `agent-tools-and-mcp`, `agent-permissions-and-sandboxing` steps) |
| The Band-5 course library builds and validates green                                            | Phase 5 · Section & Authored-Tree Verification                                                                                  |

## Course catalog (15 bodies, with prerequisites)

Full per-course concept/example/capstone detail lives in the cross-plan
[`syllabus/courses/` catalog](../../done/2026-07-24__ayokoding-learning-path-02-schema-and-prerequisite-dag/syllabus/courses/README.md).
The table below is drawn from the parent plan's own settled
[Course Library Catalog](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/tech-docs.md#course-library-catalog)
[Repo-grounded]. **Volume-target bands** (floor, not cap) are inherited unchanged from the parent
plan's own
[volume-target table](../../done/2026-08-02__ayokoding-learning-path-04-course-authoring/prd.md)
[Repo-grounded]: By Example ≥ 10 concepts / 75–85 examples; Annotated-concept, code-bearing ≥ 10
concepts / 45–60 worked examples.

| #   | Course ID                                         | Format            | Language     | Prerequisites                                                  | One-line scope                                                                |
| --- | ------------------------------------------------- | ----------------- | ------------ | -------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| 1   | `software-architecture`                           | Annotated-concept | Python       | `backend-essentials`, `object-oriented-design-and-patterns`    | Styles, tradeoffs, structuring                                                |
| 2   | `domain-driven-design`                            | By Example        | Python       | `object-oriented-design-and-patterns`, `software-architecture` | Bounded contexts, modeling                                                    |
| 3   | `system-design`                                   | Annotated-concept | Python       | `backend-at-scale`, `networking-essentials`                    | Designing for scale/availability (depth sibling of `system-design-interview`) |
| 4   | `event-driven-architecture`                       | By Example        | Python       | `software-architecture`, `backend-essentials`                  | Events, brokers, EDA                                                          |
| 5   | `distributed-systems`                             | By Example        | Python       | `networking-essentials`, `concurrency-and-parallelism`         | Consensus, replication, CAP                                                   |
| 6   | `build-your-own-web-framework`                    | By Example        | Python       | `backend-essentials`, `networking-essentials`                  | WSGI/ASGI, router, middleware (demystifies FastAPI)                           |
| 7   | `build-your-own-reactive-ui`                      | By Example        | TypeScript   | `advanced-frontend`                                            | Reactive UI lib + virtual DOM                                                 |
| 8   | `creating-ai-powered-apps`                        | By Example        | Python       | `backend-essentials`, `api-design`                             | **Use an LLM in an app**: RAG, tool-calling, MCP, evals (scope-guard head)    |
| 9   | `agentic-ai`                                      | By Example        | Python       | `creating-ai-powered-apps`                                     | **Survey** of agents; forward-links each primitive to the harness cluster     |
| 10  | `browser-automation-with-cdp`                     | By Example        | Python (CDP) | `just-enough-python`, `networking-essentials`                  | Chrome DevTools Protocol automation (`remotebrowser` skill)                   |
| 11  | `the-agent-loop`                                  | By Example        | Python       | `agentic-ai`                                                   | LLM read-eval-act loop, streaming, stops (build-your-own tier)                |
| 12  | `agent-tools-and-mcp`                             | By Example        | Python       | `the-agent-loop`                                               | Tool/function schemas; MCP server + client                                    |
| 13  | `agent-context-and-memory`                        | Annotated-concept | Python       | `the-agent-loop`                                               | Context budgeting, compaction, memory                                         |
| 14  | `agent-permissions-and-sandboxing`                | By Example        | Python       | `the-agent-loop`                                               | Approval models, sandboxing, guardrails                                       |
| 15  | `agent-orchestration-subagents-and-observability` | Annotated-concept | Python       | `agent-tools-and-mcp`, `agent-context-and-memory`              | Subagents, hooks/skills, evals, tracing                                       |

**Principle-first framing (HARD, inherited).** Every course teaches a durable **principle**; target
codebases (`remotebrowser`, the ose family) are **illustrative worked-examples**, never the subject.

## Product Scope

**In-scope**:

- Authoring **15 course page bundles** under
  `apps/ayokoding-www/content/en/learn/courses/<course-id>/`, each with `_index.md` (declaring
  `prerequisites`), `overview.md`, a `learning/` track, and a `drilling/` track in the fixed
  five-section order.
- Declaring each body's `prerequisites` in the contracted frontmatter shape, transcribed from its
  settled spec.
- Stating each body's **scope boundary** against any sibling course it could be confused with.
- Locking and applying the three **course-surgery contracts** (evals forward-link, D9
  naming/citation, D11 concept additions), including their four-path blast-radius statement, as this
  plan's own Phase 1.
- Adding this plan's 15 authored courses to the tracked
  [Course Library Catalog](./tech-docs.md#course-library-catalog-this-plans-15-rows) as real rows.
- Updating `<COURSES>_index.md` to list every authored course.
- Emitting one complete **band-completion signal** for Band 5.
- Manual behavioural verification of a sample of authored course pages via Playwright MCP, with
  committed screenshot evidence in `evidence/`.

**Out of scope**:

- **Any manifest file** under `<MANIFESTS>` — owned by `ayokoding-learning-path-12-careers-se-manifests`
  and `ayokoding-learning-path-13-careers-ai-manifest`, the successor manifest-growth plans. Binding
  invariant.
- **Any course outside the 15 named in [§Course catalog](#course-catalog-15-bodies-with-prerequisites)** —
  the other eight authoring bands.
- **`capstone-build-your-own-coding-agent`** — authored by
  `ayokoding-learning-path-11-course-authoring-capstones` (Band 8), which assembles this band's
  harness cluster.
- **Any path landing anchor or `course-paths` feature code** — owned by the manifest and
  navigation-UI plans.
- **The `prerequisites` frontmatter contract's definition** — consumed here, owned by the schema
  plan.
- **The `syllabus/` folder** — read-only from this plan; never copied.
- **Any Indonesian (`id`) course content** — explicitly deferred.
- **The UI design funnel** — this plan is not UI-bearing; see
  [tech-docs §UI-design-funnel exemption](./tech-docs.md#ui-design-funnel-exemption-not-ui-bearing).
- **The rule-15 three-tester retest** — exemption recorded with reasons in
  [README §Rule-15](./README.md#rule-15-three-tester-retest--exemption-recorded).

## Product-Level Risks

- **A body authored from judgment rather than its spec.** Concept coverage silently drops and
  prerequisite edges get invented. Mitigated by naming the exact cross-plan spec path in every
  authoring step.
- **Duplication creep in the AI band.** Mitigated by the AI-band scope-guard and the evals
  forward-link contract, both as grep-checkable acceptance criteria on the authoring steps.
- **Contested terminology adopted as course structure.** Mitigated by the D9 contract: cite the
  disagreement, rename nothing, add no course.
- **A manifest-mutating step reintroduced into this plan.** Mitigated by the invariant being stated
  in three documents plus a phase-gate check that the plan's diff touches zero `<MANIFESTS>` paths.
- **A vague band-completion signal.** Mitigated by the five-field signal contract, with an explicit
  rejection rule for incomplete signals.
- **This plan's cohorts author out of prerequisite order** (e.g. a harness-cluster course lands
  before `agentic-ai`, its prerequisite). Mitigated by the cohort ordering itself: `agentic-ai`
  (Cohort 2) precedes `the-agent-loop` (Cohort 3), and `the-agent-loop` precedes the other four
  Cohort-3 courses within that same cohort's authoring order.
