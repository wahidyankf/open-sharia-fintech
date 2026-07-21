# Path Manifest — `interview-ready/software-engineer` (interview-first)

The **ordered manifest** for the interview-first path: a **curated, prerequisite-consistent** ordered list of
**course IDs** over the [shared course library](../courses/README.md). This is the authoritative reading
order for this path; a course page under `?path=interview-ready/software-engineer` follows it for prev/next + breadcrumb.
Persona: an **experienced engineer re-entering the job market** (interview/job prep first).

This file is the **human-readable mirror** of the manifest. The **machine-consumed source of truth** is
the standalone data file
`apps/ayokoding-www/src/features/course-paths/manifests/interview-ready/software-engineer.yaml` (RESOLVED, OQ-2 — a standalone
YAML/JSON data file in the `course-paths` feature, NOT `courseOrder` frontmatter on any `_index.md`).
Path landing served at `/en/c/learn/paths/interview-ready/software-engineer`. Order rationale:
[tech-docs §Path `interview-ready/software-engineer`](../../tech-docs.md#path-interview-readysoftware-engineer-interview-first).

## Composition (curated + converge, LOCKED 2026-07-19)

A **curated spine** — interview + core + production — with an explicit optional **Go deeper** tail. The spine gets an experienced engineer interview-ready and production-effective fast; the deep-systems / OS / kernel / compilers / internals-builds / niche courses are **omitted from the required spine** and presented as an optional tail that still converges on the same deep endpoint (harness cluster, distributed systems, internals builds, security capstone).

- **Spine** (required): `Prologue` + `Phase 1 · Interview preparation` + `Phase 2 · Production-effective`.
- **Go deeper** (optional tail): theory, low-level systems, concurrency/JVM breadth, data depth, architecture/distributed/internals, mobile/CLI, AI & harness, security, and ops/quality — reachable but never required for interview-readiness.
- **Genuinely omitted** (curriculum judgment — present only in `fundamentally-strong`): `lisp`, `windows-os`, `just-enough-csharp`, `windows-app-development`, `linux-app-development`. None is a prerequisite of any included course, so the manifest stays prerequisite-closed.
- **Created**: the four interview courses + `capstone-interview-loop` (Group B); the rest reuse existing library courses by ID. **Prerequisite-consistent** (machine-verified).
- **Composition total**: **116 of the 121 software-engineer-role courses** (114 + the 7 DD-20 inter-topic
  capstones, minus the 5 genuinely-omitted above = 121 − 5 = 116). This denominator is the
  **software-engineer-role baseline**, not the **127-course library** total: the six AI-engineer-role
  courses this plan added are outside this path's scope and compose only the fourth,
  `immediately-effective/software-engineer-to-ai-engineer` path (per-role convergence, D2).
- **DD-20 addendum (2026-07-19)**: the seven DD-20 inter-topic capstones are all included (none is
  genuinely omitted), placed at their earliest prerequisite-safe position in the Go-deeper tail —
  `capstone-concurrency-showdown` (end of "Go deeper · Concurrency, JVM & languages"),
  `capstone-solid-core` (end of "Go deeper · AI & harness engineering"),
  `capstone-real-world-delivery`/`capstone-secure-service`/`capstone-data-pipeline` ("Go deeper ·
  Security suite", right after `defensive-security`), `capstone-concurrency-and-systems` ("Go deeper ·
  Ops, platform, quality & product", right after `site-reliability-engineering`), and
  `capstone-lead-at-altitude` (the manifest's final item, closing that same last section). See
  [tech-docs DD-20](../../tech-docs.md#design-decisions).

> **Surgery forward-reference ([surgery.md §S1](../courses/surgery.md#s1--extract-evals-into-a-single-owner))**:
> [`creating-ai-powered-apps`](../courses/creating-ai-powered-apps.md),
> [`agentic-ai`](../courses/agentic-ai.md), and
> [`agent-orchestration-subagents-and-observability`](../courses/agent-orchestration-subagents-and-observability.md)
> — all carried in the "Go deeper · AI & harness engineering" section below — are the three eval donors
> S1 trims. Once S1 lands, their scattered evaluation material is extracted into the two new eval courses
> ([`evaluating-ai-output-essentials`](../courses/evaluating-ai-output-essentials.md),
> [`evaluating-ai-systems-in-depth`](../courses/evaluating-ai-systems-in-depth.md)), which this
> software-engineer-role path does **not** compose (per-role scoping, D2). The **composition count is
> unchanged by S1** — the donors stay in this manifest; no course is added or removed — but this path
> then ships **without dedicated eval-depth coverage**, the accepted, documented consequence recorded in
> S1's blast-radius table (S1 flags this as its sharpest risk for the interview-ready manifest).
> Re-verify prerequisite consistency here after S1 executes.

## Prologue · Editor foundations (skippable for the experienced)

1. `just-enough-nvim`
2. `just-enough-lua`
3. `extending-neovim`
4. `just-enough-python`
5. `just-enough-bash`
6. `version-control-and-git`
7. `capstone-forge-ready`

## Phase 1 · Interview preparation (through senior)

1. `data-structures-and-algorithms-essentials`
2. `advanced-algorithms`
3. `coding-interview`
4. `take-home-and-live-coding`
5. `object-oriented-programming-essentials`
6. `object-oriented-design-and-patterns`
7. `sql-essentials`
8. `backend-essentials`
9. `networking-essentials`
10. `system-design-interview`
11. `technical-communication`
12. `behavioral-and-leadership-interviews`
13. `capstone-interview-loop`

## Phase 2 · Production-effective (web → cloud)

1. `just-enough-typescript`
2. `frontend-essentials`
3. `advanced-frontend`
4. `api-design`
5. `security-essentials`
6. `software-testing`
7. `concurrency-and-parallelism`
8. `async-python-and-fastapi-services`
9. `capstone-first-working-software`
10. `capstone-full-stack-app`
11. `self-hosting-essentials`
12. `backend-at-scale`
13. `containers-and-orchestration`
14. `cloud-and-iac`
15. `cicd-and-release-engineering`
16. `build-automation-and-task-runners`

## Go deeper · Theory & low-level systems

1. `computer-science-foundations`
2. `just-enough-c`
3. `computer-architecture`
4. `programming-paradigms`
5. `functional-programming`
6. `just-enough-cpp`
7. `linux-os`
8. `system-programming`
9. `just-enough-rust`
10. `modern-system-programming`

## Go deeper · Concurrency, JVM & languages

1. `just-enough-go`
2. `csp-style-concurrency`
3. `just-enough-elixir`
4. `actor-model-concurrency`
5. `just-enough-java`
6. `enterprise-java-and-the-jvm`
7. `just-enough-fsharp`
8. `type-systems`
9. `compilers-parsers-and-transpilers`
10. `capstone-concurrency-showdown` (DD-20 — prereqs `csp-style-concurrency`/`actor-model-concurrency`, both earlier in this section)

## Go deeper · Data depth

1. `advanced-networking`
2. `advanced-sql-and-query-performance`
3. `data-access-orms-and-query-builders`
4. `build-your-own-orm-and-query-builder`
5. `nosql-databases`
6. `graph-databases`
7. `database-internals-and-storage-engines`
8. `data-engineering`
9. `search-and-information-retrieval`

## Go deeper · Architecture, distributed & internals builds

1. `software-architecture`
2. `domain-driven-design`
3. `system-design`
4. `event-driven-architecture`
5. `distributed-systems`
6. `build-your-own-web-framework`
7. `build-your-own-reactive-ui`
8. `build-your-own-git`
9. `build-your-own-database`
10. `build-your-own-raft`

## Go deeper · Mobile & CLI platforms

1. `just-enough-kotlin`
2. `android-app-development`
3. `just-enough-swift`
4. `ios-app-development`
5. `just-enough-dart`
6. `hybrid-app-development`
7. `building-production-cli-tools`

## Go deeper · AI & harness engineering

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
12. `capstone-solid-core` (DD-20 — prereqs `capstone-first-working-software` (Phase 2),
    `object-oriented-design-and-patterns` (Phase 1), `functional-programming`/`concurrency-and-parallelism`
    (earlier Go-deeper sections/Phase 2), `advanced-sql-and-query-performance` (Go deeper · Data depth),
    `software-engineering-practices` (this section) — placed here so it precedes the Security suite
    section, where its downstream dependent `capstone-real-world-delivery` needs it)

## Go deeper · Security suite

1. `it-and-application-security`
2. `offensive-security`
3. `defensive-security`
4. `capstone-real-world-delivery` (DD-20 — prereqs `capstone-solid-core` (above), `system-design`/`event-driven-architecture` ("Go deeper · Architecture..."), `containers-and-orchestration`/`cloud-and-iac`/`cicd-and-release-engineering` (Phase 2 spine), `defensive-security` (above))
5. `capstone-secure-service` (DD-20 — prereqs `security-essentials`/`backend-essentials` (Phase 2/1 spine), `it-and-application-security`/`offensive-security`/`defensive-security` (above))
6. `capstone-data-pipeline` (DD-20 — prereqs `sql-essentials` (Phase 1 spine), `advanced-sql-and-query-performance`/`data-engineering` ("Go deeper · Data depth"), `creating-ai-powered-apps` ("Go deeper · AI & harness engineering"))
7. `detection-engineering-and-siem-operations`
8. `vulnerability-management-and-assessment`
9. `it-governance-grc`
10. `capstone-build-your-own-pentest-engine`

## Go deeper · Ops, platform, quality & product

1. `bare-metal-virtualization`
2. `self-managed-kubernetes-and-gitops`
3. `platform-engineering-and-devex`
4. `site-reliability-engineering`
5. `capstone-concurrency-and-systems` (DD-20 — prereqs `csp-style-concurrency`/`actor-model-concurrency` ("Go deeper · Concurrency, JVM & languages"), `containers-and-orchestration` (Phase 2 spine), `site-reliability-engineering` (immediately above))
6. `debugging-and-profiling`
7. `analytics-and-experimentation`
8. `information-architecture-and-seo`
9. `software-product-engineering`
10. `engineering-management`
11. `project-management`
12. `capstone-lead-at-altitude` (DD-20 — whole-journey capstone; prereqs `capstone-concurrency-and-systems`/`capstone-real-world-delivery` (both above), `site-reliability-engineering`, `software-product-engineering`/`engineering-management` (all above) — this manifest's final item)

## Smoothness notes (RD-16)

- **Spine stands alone**: a reader can stop at the end of Phase 2 fully interview-ready and
  production-effective; the entire **Go deeper** tail is optional.
- **Prereq-chaining holds** (machine-verified): `system-design-interview` follows its
  `backend-essentials` / `networking-essentials` / `sql-essentials` prerequisites in Phase 1;
  `computer-architecture` is preceded by `just-enough-c` at the head of the Go-deeper tail;
  `software-engineering-practices` (Go deeper · AI & harness) follows `software-testing` (Phase 2 spine).
- **Convergence**: the Go-deeper tail ends at the same deep endpoint as the other two paths — the
  AI/harness cluster (`capstone-build-your-own-coding-agent`), internals builds, distributed systems,
  and the security capstone (`capstone-build-your-own-pentest-engine`).
- **Skip / fast-path**: the prologue is skippable; primers are skippable ("if you already know X, jump
  to Y"); the four interview courses use the refresh register.

See [tech-docs §Smoothness Architecture](../../tech-docs.md#smoothness-architecture-per-path).
