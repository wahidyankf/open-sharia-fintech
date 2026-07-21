# Path Manifest — `fundamentally-strong/software-engineer` (fundamentals-first)

The **ordered manifest** for the fundamentals-first path: a **curated, prerequisite-consistent** ordered list of
**course IDs** over the [shared course library](../courses/README.md). This is the authoritative reading
order for this path; a course page under `?path=fundamentally-strong/software-engineer` follows it for prev/next + breadcrumb.
Persona: a **learner who wants university-style depth** — CS theory and fundamentals **first**, then breadth, then application, all the way to the same deep mastery the other two paths converge on.

This file is the **human-readable mirror** of the manifest. The **machine-consumed source of truth** is
the standalone data file
`apps/ayokoding-www/src/features/course-paths/manifests/fundamentally-strong/software-engineer.yaml` (RESOLVED, OQ-2 — a standalone
YAML/JSON data file in the `course-paths` feature, NOT `courseOrder` frontmatter on any `_index.md`).
Path landing served at `/en/c/learn/paths/fundamentally-strong/software-engineer`. Order rationale:
[tech-docs §Path `fundamentally-strong/software-engineer`](../../tech-docs.md#path-fundamentally-strongsoftware-engineer-theory-first).

## Composition (curated + converge, LOCKED 2026-07-19)

This is the **complete-mastery** path for the software-engineer role — it includes **all 121 software-engineer-role courses** in a **theory-first** ordering, and it is the only software-engineer-role path that omits none of them. It no longer "includes all library courses": the six **AI-engineer-role** courses this plan added (the eval split `evaluating-ai-output-essentials` / `evaluating-ai-systems-in-depth`, plus `statistics-for-evaluation`, `product-patterns-for-probabilistic-systems`, `inference-serving-and-model-deployment`, and `fine-tuning-and-adaptation`) are outside this path's role scope and compose only the fourth, `immediately-effective/software-engineer-to-ai-engineer` path — paths converge **per role, not globally** (D2). Its distinctive move is to front-load **CS theory and fundamentals** (foundations, architecture, paradigms, DS&A, OO design) before any application/product work — the university sequence. The two curated software-engineer paths (`interview-ready`, `immediately-effective`) reach the same deep endpoint through a smaller spine plus an optional tail / deepening band; this path teaches the whole software-engineer-role library in one arc.

- **Created**: none — a pure manifest ordering over the shared library. **Zero new bodies.**
- **Prerequisite-consistent**: a valid topological entry into the library's prerequisite DAG. Every course appears after all of its prerequisites (verified). `just-enough-c` is taught in Stage 1 so `computer-architecture` never forward-references C; the minimal web slice in Stage 5 (`backend-essentials`, `sql-essentials`, `api-design`) precedes the data-depth and architecture courses that declare it as a prerequisite.
- **DD-20 addendum (2026-07-19)**: seven inter-topic capstones reconciled into the catalog are placed
  here at their earliest prerequisite-safe position — `capstone-concurrency-showdown` (end of Stage 3),
  `capstone-concurrency-and-systems` (end of Stage 10, after `site-reliability-engineering`),
  `capstone-solid-core` (end of Stage 12), `capstone-real-world-delivery` /
  `capstone-secure-service` / `capstone-data-pipeline` (Stage 13, right after `defensive-security`),
  and `capstone-lead-at-altitude` (end of Stage 14, the manifest's whole-journey close). See
  [tech-docs DD-20](../../tech-docs.md#design-decisions).

> **Surgery forward-reference ([surgery.md §S1](../courses/surgery.md#s1--extract-evals-into-a-single-owner))**:
> [`creating-ai-powered-apps`](../courses/creating-ai-powered-apps.md),
> [`agentic-ai`](../courses/agentic-ai.md), and
> [`agent-orchestration-subagents-and-observability`](../courses/agent-orchestration-subagents-and-observability.md)
> — all carried in "Stage 12 · AI & harness engineering" below — are the three eval donors S1 trims. Once
> S1 lands, their scattered evaluation material is extracted into the two new eval courses
> ([`evaluating-ai-output-essentials`](../courses/evaluating-ai-output-essentials.md),
> [`evaluating-ai-systems-in-depth`](../courses/evaluating-ai-systems-in-depth.md)), which this
> software-engineer-role path does **not** compose (per-role scoping, D2). The **composition count is
> unchanged by S1** — the donors stay in this manifest; no course is added or removed — but this path
> then ships **without dedicated eval-depth coverage**, the accepted, documented consequence recorded in
> S1's blast-radius table (S1 flags a fundamentals-first path losing measurement rigor as the worst of
> the three). Re-verify prerequisite consistency here after S1 executes.

## Prologue · Editor & reproducible forge (skippable)

1. `just-enough-nvim`
2. `just-enough-lua`
3. `extending-neovim`
4. `just-enough-python`
5. `just-enough-bash`
6. `version-control-and-git`
7. `capstone-forge-ready`

## Stage 1 · CS theory & foundations (the university core, taught first)

1. `computer-science-foundations`
2. `just-enough-c`
3. `computer-architecture`
4. `programming-paradigms`
5. `functional-programming`

## Stage 2 · Data structures, algorithms & object-oriented design

1. `data-structures-and-algorithms-essentials`
2. `advanced-algorithms`
3. `object-oriented-programming-essentials`
4. `object-oriented-design-and-patterns`

## Stage 3 · Concurrency & language breadth

1. `concurrency-and-parallelism`
2. `just-enough-go`
3. `csp-style-concurrency`
4. `just-enough-elixir`
5. `actor-model-concurrency`
6. `just-enough-rust`
7. `just-enough-java`
8. `enterprise-java-and-the-jvm`
9. `lisp`
10. `just-enough-fsharp`
11. `type-systems`
12. `compilers-parsers-and-transpilers`
13. `capstone-concurrency-showdown` (DD-20 — inter-topic capstone; prereqs `csp-style-concurrency`,
    `actor-model-concurrency`, both earlier in this stage)

## Stage 4 · Systems programming & OS internals

1. `linux-os`
2. `windows-os`
3. `system-programming`
4. `modern-system-programming`
5. `just-enough-cpp`

## Stage 5 · Web foundations (the minimal application slice the depth courses build on)

1. `just-enough-typescript`
2. `frontend-essentials`
3. `sql-essentials`
4. `backend-essentials`
5. `api-design`

## Stage 6 · Databases & data depth

1. `advanced-sql-and-query-performance`
2. `data-access-orms-and-query-builders`
3. `build-your-own-orm-and-query-builder`
4. `nosql-databases`
5. `graph-databases`
6. `database-internals-and-storage-engines`
7. `data-engineering`
8. `search-and-information-retrieval`

## Stage 7 · Networking, architecture & distributed systems

1. `networking-essentials`
2. `advanced-networking`
3. `software-architecture`
4. `domain-driven-design`
5. `backend-at-scale`
6. `system-design`
7. `event-driven-architecture`
8. `distributed-systems`
9. `build-your-own-web-framework`

## Stage 8 · Internals builds (apply the fundamentals)

1. `build-your-own-git`
2. `build-your-own-database`
3. `build-your-own-raft`

## Stage 9 · Application & product development (build real things on the foundations)

1. `async-python-and-fastapi-services`
2. `advanced-frontend`
3. `build-your-own-reactive-ui`
4. `security-essentials`
5. `software-testing`
6. `capstone-first-working-software`
7. `capstone-full-stack-app`

## Stage 10 · Scale, cloud & platform ops

1. `self-hosting-essentials`
2. `containers-and-orchestration`
3. `cloud-and-iac`
4. `cicd-and-release-engineering`
5. `build-automation-and-task-runners`
6. `bare-metal-virtualization`
7. `self-managed-kubernetes-and-gitops`
8. `platform-engineering-and-devex`
9. `site-reliability-engineering`
10. `capstone-concurrency-and-systems` (DD-20 — inter-topic capstone; prereqs
    `csp-style-concurrency`/`actor-model-concurrency` (Stage 3), `containers-and-orchestration`
    (this stage), `site-reliability-engineering` (immediately above))

## Stage 11 · Mobile & desktop platforms

1. `just-enough-kotlin`
2. `android-app-development`
3. `just-enough-swift`
4. `ios-app-development`
5. `just-enough-dart`
6. `hybrid-app-development`
7. `just-enough-csharp`
8. `windows-app-development`
9. `linux-app-development`
10. `building-production-cli-tools`

## Stage 12 · AI & harness engineering (marquee build-your-own track)

1. `software-engineering-practices`
2. `agentic-coding`
3. `creating-ai-powered-apps`
4. `agentic-ai`
5. `browser-automation-with-cdp`
6. `the-agent-loop`
7. `agent-tools-and-mcp`
8. `agent-context-and-memory`
9. `agent-permissions-and-sandboxing`
10. `agent-orchestration-subagents-and-observability`
11. `capstone-build-your-own-coding-agent`
12. `capstone-solid-core` (DD-20 — inter-topic capstone; prereqs `capstone-first-working-software`
    (Stage 9), `object-oriented-design-and-patterns` (Stage 2), `functional-programming` (Stage 1),
    `concurrency-and-parallelism` (Stage 3), `advanced-sql-and-query-performance` (Stage 6),
    `software-engineering-practices` (this stage) — placed at the end of this stage so it precedes
    Stage 13, where its own downstream dependent `capstone-real-world-delivery` needs it)

## Stage 13 · Security suite

1. `it-and-application-security`
2. `offensive-security`
3. `defensive-security`
4. `capstone-real-world-delivery` (DD-20 — inter-topic capstone; prereqs `capstone-solid-core` (Stage
   12), `system-design`/`event-driven-architecture` (Stage 7), `containers-and-orchestration`/
   `cloud-and-iac`/`cicd-and-release-engineering` (Stage 10), `defensive-security` (above))
5. `capstone-secure-service` (DD-20 — inter-topic capstone; prereqs `security-essentials` (Stage 9),
   `backend-essentials` (Stage 5), `it-and-application-security`/`offensive-security`/
   `defensive-security` (above))
6. `capstone-data-pipeline` (DD-20 — inter-topic capstone; prereqs `sql-essentials` (Stage 5),
   `advanced-sql-and-query-performance`/`data-engineering` (Stage 6), `creating-ai-powered-apps`
   (Stage 12))
7. `detection-engineering-and-siem-operations`
8. `vulnerability-management-and-assessment`
9. `it-governance-grc`
10. `capstone-build-your-own-pentest-engine`

## Stage 14 · Quality, product, delivery & leadership

1. `debugging-and-profiling`
2. `analytics-and-experimentation`
3. `information-architecture-and-seo`
4. `technical-communication`
5. `software-product-engineering`
6. `engineering-management`
7. `project-management`
8. `capstone-lead-at-altitude` (DD-20 — whole-journey inter-topic capstone; prereqs
   `capstone-concurrency-and-systems` (Stage 10) or `capstone-real-world-delivery` (Stage 13),
   `site-reliability-engineering` (Stage 10), `software-product-engineering`/`engineering-management`
   (this stage) — closes this stage as the manifest's final required-library item, right before the
   optional interview tail)

## Optional tail · Ready to job-hunt? (bridge into the interview courses)

1. `coding-interview`
2. `take-home-and-live-coding`
3. `system-design-interview`
4. `behavioral-and-leadership-interviews`
5. `capstone-interview-loop`

> The five interview courses in the optional tail appear in **all three** manifests (the main
> interview-first arc in `interview-ready/software-engineer`; an optional job-hunt tail in
> `immediately-effective/software-engineer`; and this optional interview tail). Every path references
> them **by course ID** — one canonical body, three orderings.

## Smoothness notes (RD-16)

- **Fundamentals-first ordering is deliberate**: editor/tooling → CS theory & foundations → DS&A / OO
  design → language & systems breadth → a minimal web slice → data & architecture depth → internals
  builds → **then** the rest of application/product work, ops, mobile, AI/harness, and security. Theory
  precedes building, the inverse of the `immediately-effective` path.
- **Minimal application slice pulled forward (Stage 5)**: a handful of application courses
  (`backend-essentials`, `sql-essentials`, `api-design`, plus the TypeScript/frontend on-ramp) are
  taught before the deep data and architecture stages because several depth courses declare them as
  prerequisites (`data-engineering`, `system-design`, `software-architecture`, `creating-ai-powered-apps`).
  This keeps the ordering prerequisite-consistent without abandoning the theory-first spirit.
- **Prereq-chaining holds** end-to-end (machine-verified): every `just-enough-<lang>` primer precedes
  its first subject use, and `software-engineering-practices` (Stage 12) follows `software-testing`
  (Stage 9), which it depends on.
- **Skip / fast-path**: the editor prologue is skippable; a learner who already owns a
  `just-enough-<lang>` primer may skip it.

See [tech-docs §Smoothness Architecture](../../tech-docs.md#smoothness-architecture-per-path).
