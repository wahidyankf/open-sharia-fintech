# Path Manifest — `software-engineer` (shipping-first)

The **ordered manifest** for the shipping-first path: an ordered list of **course IDs** over the
[shared course library](./README.md). This is the authoritative reading order for this path; a course
page under `?path=software-engineer` follows it for prev/next + breadcrumb. Delivered **second**
(Group C), **reusing the same course bodies reordered** — zero body duplication. Persona: a **builder
who wants to be effective fast** ("immediately effective", then go deep).

This file is the **human-readable mirror** of the manifest. The **machine-consumed source of truth**
is the standalone data file
`apps/ayokoding-www/src/features/course-paths/manifests/software-engineer.yaml` (RESOLVED, OQ-2 — a
standalone YAML/JSON data file in the `course-paths` feature, NOT `courseOrder` frontmatter on any
`_index.md`). Order rationale:
[tech-docs §Path `software-engineer`](../tech-docs.md#path-software-engineer-shipping-first).

## Course selection for this path (RESOLVED, OQ-3)

- **No hard omission of the interview courses.** This path keeps the underlying **depth** courses
  inline (`data-structures-and-algorithms-essentials`, `object-oriented-*`, `system-design`,
  `technical-communication` — general SWE skill), and instead **ends with an optional "ready to
  job-hunt?" bridge tail** (see the final section) that links into the interview-technique courses for
  a learner who decides to job-hunt.
- **Created**: none — the shipping-first arc (and its bridge tail) reuses existing library courses by
  ID. **Zero new bodies** (Group C is pure manifest reuse over the library Group B already re-homed).

## Stage 1 · Editor & tooling (get set up fast)

1. `just-enough-nvim`
2. `just-enough-lua`
3. `extending-neovim`
4. `just-enough-python`
5. `just-enough-bash`
6. `version-control-and-git`
7. `capstone-forge-ready`

## Stage 2 · One language end-to-end, then BUILD A REAL APP FIRST (the "immediately effective" payoff)

1. `just-enough-typescript`
2. `frontend-essentials`
3. `backend-essentials`
4. `sql-essentials`
5. `api-design`
6. `advanced-frontend`
7. `async-python-and-fastapi-services`
8. `capstone-first-working-software` — ship a first real, secure, tested web app
9. `self-hosting-essentials`
10. `cicd-and-release-engineering`
11. `capstone-full-stack-app` — a deployed, tested, full-stack vertical slice

> **Stage-2 → Stage-3 bridge**: "you shipped a real app — now understand _why_ it worked." The reader
> has a deployed artifact before any pure-theory course; Stage 3 turns intuition into fundamentals.

## Stage 3 · Now go deep — CS fundamentals, DS&A, algorithms

1. `data-structures-and-algorithms-essentials`
2. `advanced-algorithms`
3. `object-oriented-programming-essentials`
4. `object-oriented-design-and-patterns`
5. `computer-science-foundations`
6. `computer-architecture`
7. `programming-paradigms`
8. `functional-programming`

## Stage 4 · Systems, data, architecture, security & ops depth (shallow → deep)

Concurrency:

1. `concurrency-and-parallelism`
2. `just-enough-go`
3. `csp-style-concurrency`
4. `just-enough-elixir`
5. `actor-model-concurrency`

Networking & data depth:

1. `networking-essentials`
2. `advanced-networking`
3. `advanced-sql-and-query-performance`
4. `data-access-orms-and-query-builders`
5. `build-your-own-orm-and-query-builder`
6. `nosql-databases`
7. `graph-databases`
8. `database-internals-and-storage-engines`
9. `data-engineering`
10. `search-and-information-retrieval`

Architecture & distributed:

1. `software-architecture`
2. `domain-driven-design`
3. `system-design`
4. `event-driven-architecture`
5. `distributed-systems`
6. `build-your-own-web-framework`
7. `build-your-own-reactive-ui`

Cloud / scale depth (heavier than the Stage-2 self-hosting on-ramp):

1. `backend-at-scale`
2. `containers-and-orchestration`
3. `cloud-and-iac`
4. `build-automation-and-task-runners`

AI & harness engineering (marquee build-your-own track):

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

Low-level systems:

1. `just-enough-c`
2. `just-enough-cpp`
3. `linux-os`
4. `windows-os`
5. `system-programming`
6. `just-enough-rust`
7. `modern-system-programming`

JVM & languages:

1. `just-enough-java`
2. `enterprise-java-and-the-jvm`
3. `lisp`
4. `just-enough-fsharp`
5. `type-systems`
6. `compilers-parsers-and-transpilers`

Internals builds:

1. `build-your-own-git`
2. `build-your-own-database`
3. `build-your-own-raft`

Mobile & desktop platforms:

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

Security suite:

1. `security-essentials`
2. `it-and-application-security`
3. `offensive-security`
4. `defensive-security`
5. `detection-engineering-and-siem-operations`
6. `vulnerability-management-and-assessment`
7. `it-governance-grc`
8. `capstone-build-your-own-pentest-engine`

Ops & platform:

1. `bare-metal-virtualization`
2. `self-managed-kubernetes-and-gitops`
3. `platform-engineering-and-devex`
4. `site-reliability-engineering`

Quality / product / delivery:

1. `software-testing`
2. `debugging-and-profiling`
3. `analytics-and-experimentation`
4. `information-architecture-and-seo`
5. `software-product-engineering`
6. `engineering-management`
7. `project-management`
8. `technical-communication`

## Optional tail · Ready to job-hunt? (bridge into the interview courses, RESOLVED OQ-3)

An **opt-in** tail for a shipping-first learner who decides to pursue a job. It references the **same
shared courses** the `job-seeking-software-engineer` path uses — **by ID, zero new bodies** — so the
learner flows straight into interview prep without leaving the path or duplicating content. The path
landing marks this section clearly optional; links carry `?path=software-engineer`.

1. `coding-interview`
2. `take-home-and-live-coding`
3. `system-design-interview`
4. `behavioral-and-leadership-interviews`
5. `capstone-interview-loop` — the full mock-loop capstone

> These five appear in **both** manifests (interview-first arc for `job-seeking-software-engineer`,
> optional job-hunt tail here). Both reference them by course ID — one canonical body, two orderings.

## Smoothness notes (RD-16)

- **Shipping-first ordering is deliberate**: editor/tooling → one language end-to-end → **build a real
  app** precedes all CS-theory. The reader has a deployed artifact before Stage 3.
- **Prereq-chaining** holds under this order — every language primer precedes its first use in this
  path's order (TypeScript before frontend; Python primer in Stage 1 before the async/backend courses;
  the systems and JVM primers precede their subject courses in Stage 4). The two inherited in-context
  language forward-references (SF-1/SF-2) are softened + bridged in the course bodies (shared with the
  interview path), never reordered.
- **Stage-2 → Stage-3 bridge** softens the shipping → theory transition (see above).
- **Skip / fast-path**: "already fluent in a language? jump straight to Stage 2 (build an app)"; the
  landing names the skip affordance.

See [tech-docs §Smoothness Architecture](../tech-docs.md#smoothness-architecture-per-path).
