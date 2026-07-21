# Path Manifest — `careers/immediately-effective/software-engineer` (shipping-first)

The **ordered manifest** for the shipping-first path: a **curated, prerequisite-consistent** ordered list of
**course IDs** over the [shared course library](../courses/README.md). This is the authoritative reading
order for this path; a course page under `?path=careers/immediately-effective/software-engineer` follows
it for prev/next + breadcrumb. Persona: a **builder who wants to be effective fast** — editor → one
language → **build a real app first** → then deepen.

This file is the **human-readable mirror** of the manifest. The **machine-consumed source of truth** is
the standalone data file
`apps/ayokoding-www/src/features/course-paths/manifests/careers/immediately-effective/software-engineer.yaml`
(RESOLVED, OQ-2 — a standalone YAML/JSON data file in the `course-paths` feature, NOT `courseOrder`
frontmatter on any `_index.md`). Per
[tech-docs §Variable-depth `pathId`](../../tech-docs.md#variable-depth-pathid-careers-vs-skills--r2-r8),
the manifest also carries an explicit `arc: immediately-effective` field (R8). Path landing served at
`/en/learn/paths/careers/immediately-effective/software-engineer`. Order rationale:
[tech-docs §Path `careers/immediately-effective/software-engineer`](../../tech-docs.md#path-careersimmediately-effectivesoftware-engineer-build-fast-first).

## Composition (curated + converge, LOCKED 2026-07-19)

A **build-first spine** followed by a **Deepening band**. The spine gets a builder shipping a real, deployed app as fast as possible; the heavy theory (`computer-science-foundations`, `type-systems`, `advanced-algorithms`, `programming-paradigms`, `computer-architecture`, and the rest of the CS/systems depth) is **deferred out of the early spine** into a later Deepening band, so intuition from shipping precedes the fundamentals that explain it.

- **Spine** (required): `Stage 1 · Editor & tooling` + `Stage 2 · One language end-to-end, then build a real app first`.
- **Deepening band** (deferred, not in the early spine): CS fundamentals & DS&A, concurrency/systems/JVM breadth, data depth, architecture/distributed/internals, scale/ops, mobile/desktop, AI & harness, security, and quality/product — plus an optional interview tail.
- **Genuinely omitted** (curriculum judgment — present only in `fundamentally-strong`): `lisp`, `windows-os`. Neither is a prerequisite of any included course, so the manifest stays prerequisite-closed.
- **Created**: none — pure manifest reuse over the library. **Prerequisite-consistent** (machine-verified).
- **Composition total**: **119 of the 121 software-engineer-role courses** (114 + the 7 DD-20 inter-topic
  capstones, minus the 2 genuinely-omitted above = 121 − 2 = 119). This denominator is the
  **software-engineer-role baseline**, not the **127-course library** total: the six AI-engineer-role
  courses this plan added are outside this path's scope and compose only the fourth,
  `careers/immediately-effective/ai-engineer` path (per-role convergence, D2).
- **DD-20 addendum (2026-07-19)**: the seven DD-20 inter-topic capstones are all included (none is
  genuinely omitted), placed at their earliest prerequisite-safe position in the Deepening band —
  `capstone-concurrency-showdown` (end of "Deepening band · Concurrency & language breadth"),
  `capstone-concurrency-and-systems` (end of "Deepening band · Scale, cloud & platform ops"),
  `capstone-solid-core` (end of "Deepening band · AI & harness engineering"),
  `capstone-real-world-delivery`/`capstone-secure-service`/`capstone-data-pipeline` ("Deepening band ·
  Security suite", right after `defensive-security`), and `capstone-lead-at-altitude` (the end of
  "Deepening band · Quality, product, delivery & leadership", right before the optional interview
  tail). See [tech-docs DD-20](../../tech-docs.md#design-decisions).

> **Surgery forward-reference ([surgery.md §S1](../courses/surgery.md#s1--extract-evals-into-a-single-owner))**:
> [`creating-ai-powered-apps`](../courses/creating-ai-powered-apps.md),
> [`agentic-ai`](../courses/agentic-ai.md), and
> [`agent-orchestration-subagents-and-observability`](../courses/agent-orchestration-subagents-and-observability.md)
> — all carried in the "Deepening band · AI & harness engineering" section below — are the three eval
> donors S1 trims. Once S1 lands, their scattered evaluation material is extracted into the two new eval
> courses ([`evaluating-ai-output-essentials`](../courses/evaluating-ai-output-essentials.md),
> [`evaluating-ai-systems-in-depth`](../courses/evaluating-ai-systems-in-depth.md)), which this
> software-engineer-role path does **not** compose (per-role scoping, D2). The **composition count is
> unchanged by S1** — the donors stay in this manifest; no course is added or removed — but this path
> then ships **without dedicated eval-depth coverage**, the accepted, documented consequence recorded in
> S1's blast-radius table. Re-verify prerequisite consistency here after S1 executes.

## Stage 1 · Editor & tooling (get set up fast)

1. `just-enough-nvim`
2. `just-enough-lua`
3. `extending-neovim`
4. `just-enough-python`
5. `just-enough-bash`
6. `version-control-and-git`
7. `capstone-forge-ready`

## Stage 2 · One language end-to-end, then BUILD A REAL APP FIRST

1. `just-enough-typescript`
2. `frontend-essentials`
3. `sql-essentials`
4. `backend-essentials`
5. `api-design`
6. `advanced-frontend`
7. `networking-essentials`
8. `security-essentials`
9. `software-testing`
10. `concurrency-and-parallelism`
11. `async-python-and-fastapi-services`
12. `capstone-first-working-software`
13. `self-hosting-essentials`
14. `containers-and-orchestration`
15. `cicd-and-release-engineering`
16. `cloud-and-iac`
17. `capstone-full-stack-app`

## Deepening band · CS fundamentals, DS&A & algorithms

1. `data-structures-and-algorithms-essentials`
2. `advanced-algorithms`
3. `object-oriented-programming-essentials`
4. `object-oriented-design-and-patterns`
5. `computer-science-foundations`
6. `just-enough-c`
7. `computer-architecture`
8. `programming-paradigms`
9. `functional-programming`

## Deepening band · Concurrency & language breadth

1. `just-enough-go`
2. `csp-style-concurrency`
3. `just-enough-elixir`
4. `actor-model-concurrency`
5. `just-enough-cpp`
6. `linux-os`
7. `system-programming`
8. `just-enough-rust`
9. `modern-system-programming`
10. `just-enough-java`
11. `enterprise-java-and-the-jvm`
12. `just-enough-fsharp`
13. `type-systems`
14. `compilers-parsers-and-transpilers`
15. `capstone-concurrency-showdown` (DD-20 — prereqs `csp-style-concurrency`/`actor-model-concurrency`, both earlier in this section)

## Deepening band · Data depth

1. `advanced-networking`
2. `advanced-sql-and-query-performance`
3. `data-access-orms-and-query-builders`
4. `build-your-own-orm-and-query-builder`
5. `nosql-databases`
6. `graph-databases`
7. `database-internals-and-storage-engines`
8. `data-engineering`
9. `search-and-information-retrieval`

## Deepening band · Architecture, distributed & internals builds

1. `software-architecture`
2. `domain-driven-design`
3. `backend-at-scale`
4. `system-design`
5. `event-driven-architecture`
6. `distributed-systems`
7. `build-your-own-web-framework`
8. `build-your-own-reactive-ui`
9. `build-your-own-git`
10. `build-your-own-database`
11. `build-your-own-raft`

## Deepening band · Scale, cloud & platform ops

1. `build-automation-and-task-runners`
2. `bare-metal-virtualization`
3. `self-managed-kubernetes-and-gitops`
4. `platform-engineering-and-devex`
5. `site-reliability-engineering`
6. `capstone-concurrency-and-systems` (DD-20 — prereqs `csp-style-concurrency`/`actor-model-concurrency` ("Deepening band · Concurrency & language breadth"), `containers-and-orchestration` (Stage 2 spine), `site-reliability-engineering` (immediately above))

## Deepening band · Mobile & desktop platforms

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

## Deepening band · AI & harness engineering (marquee build-your-own track)

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
12. `capstone-solid-core` (DD-20 — prereqs `capstone-first-working-software` (Stage 2 spine), `object-oriented-design-and-patterns`/`functional-programming` ("Deepening band · CS fundamentals..."), `concurrency-and-parallelism` (Stage 2 spine), `advanced-sql-and-query-performance` ("Deepening band · Data depth"), `software-engineering-practices` (this section) — placed here so it precedes the Security suite section, where its downstream dependent `capstone-real-world-delivery` needs it)

## Deepening band · Security suite

1. `it-and-application-security`
2. `offensive-security`
3. `defensive-security`
4. `capstone-real-world-delivery` (DD-20 — prereqs `capstone-solid-core` (above), `system-design`/`event-driven-architecture` ("Deepening band · Architecture..."), `containers-and-orchestration`/`cloud-and-iac`/`cicd-and-release-engineering` (Stage 2 spine), `defensive-security` (above))
5. `capstone-secure-service` (DD-20 — prereqs `security-essentials`/`backend-essentials` (Stage 2 spine), `it-and-application-security`/`offensive-security`/`defensive-security` (above))
6. `capstone-data-pipeline` (DD-20 — prereqs `sql-essentials` (Stage 2 spine), `advanced-sql-and-query-performance`/`data-engineering` ("Deepening band · Data depth"), `creating-ai-powered-apps` ("Deepening band · AI & harness engineering"))
7. `detection-engineering-and-siem-operations`
8. `vulnerability-management-and-assessment`
9. `it-governance-grc`
10. `capstone-build-your-own-pentest-engine`

## Deepening band · Quality, product, delivery & leadership

1. `debugging-and-profiling`
2. `analytics-and-experimentation`
3. `information-architecture-and-seo`
4. `technical-communication`
5. `software-product-engineering`
6. `engineering-management`
7. `project-management`
8. `capstone-lead-at-altitude` (DD-20 — whole-journey capstone; prereqs `capstone-concurrency-and-systems`/`capstone-real-world-delivery` (both above), `site-reliability-engineering`, `software-product-engineering`/`engineering-management` (all above) — closes this section right before the optional interview tail)

## Optional tail · Ready to job-hunt? (bridge into the interview courses)

1. `coding-interview`
2. `take-home-and-live-coding`
3. `system-design-interview`
4. `behavioral-and-leadership-interviews`
5. `capstone-interview-loop`

> **Stage 2 → Deepening bridge**: "you shipped a real app — now understand _why_ it worked." The reader
> has a deployed artifact before any pure-theory course; the Deepening band turns intuition into
> fundamentals.
>
> The five interview courses in the optional tail appear in **all three** manifests. Every path
> references them **by course ID** — one canonical body, three orderings.

## Smoothness notes (RD-16)

- **Shipping-first ordering is deliberate**: editor/tooling → one language end-to-end → **build a real
  app** precedes all CS-theory. The reader has a deployed artifact before the Deepening band.
- **Prereq-chaining holds** (machine-verified): every language primer precedes its first use;
  `concurrency-and-parallelism` is taught in the Stage-2 spine before `async-python-and-fastapi-services`
  (which depends on it); `backend-at-scale` precedes `system-design` in the Deepening band.
- **Convergence**: the Deepening band ends at the same deep endpoint as the other two paths — the
  AI/harness cluster, internals builds, distributed systems, and the security capstone.
- **Skip / fast-path**: "already fluent in a language? jump straight to Stage 2 (build an app)"; the
  landing names the skip affordance.

See [tech-docs §Smoothness Architecture](../../tech-docs.md#smoothness-architecture-per-path).
