# Path Manifest — `job-seeking-software-engineer` (interview-first)

The **ordered manifest** for the interview-first path: an ordered list of **course IDs** over the
[shared course library](./README.md). This is the authoritative reading order for this path; a course
page under `?path=job-seeking-software-engineer` follows it for prev/next + breadcrumb. Delivered
**first** (Group B). Persona: an **experienced engineer re-entering the job market**.

This file is the **human-readable mirror** of the manifest. The **machine-consumed source of truth**
is the standalone data file
`apps/ayokoding-www/src/features/course-paths/manifests/job-seeking-software-engineer.yaml` (RESOLVED,
OQ-2 — a standalone YAML/JSON data file in the `course-paths` feature, NOT `courseOrder` frontmatter on
any `_index.md`). Order rationale:
[tech-docs §Path `job-seeking-software-engineer`](../tech-docs.md#path-job-seeking-software-engineer-interview-first).

## Prologue · Editor Foundations (skippable for the experienced)

1. `just-enough-nvim`
2. `just-enough-lua`
3. `extending-neovim`
4. `capstone-forge-ready`

## Phase 1 · Interview Preparation (through senior)

1. `just-enough-python`
2. `just-enough-bash`
3. `version-control-and-git`
4. `data-structures-and-algorithms-essentials`
5. `advanced-algorithms`
6. `coding-interview` **NEW** — hosts the 2026 senior interview-loop-map
7. `take-home-and-live-coding` **NEW**
8. `object-oriented-programming-essentials`
9. `object-oriented-design-and-patterns`
10. `sql-essentials`
11. `system-design-interview` **NEW**
12. `technical-communication`
13. `behavioral-and-leadership-interviews` **NEW** — layoff/employment-gap narrative
14. `capstone-interview-loop` **NEW**

## Phase 2 · Multi-Platform Productivity (web → cloud → mobile → desktop)

Web sub-phase:

1. `just-enough-typescript`
2. `frontend-essentials`
3. `backend-essentials`
4. `async-python-and-fastapi-services` **NEW**
5. `networking-essentials`
6. `api-design`
7. `advanced-frontend`
8. `capstone-first-working-software`

Cloud / backend-at-scale sub-phase:

1. `self-hosting-essentials` **NEW** — light on-ramp, strictly below clusters/IaC
2. `backend-at-scale`
3. `containers-and-orchestration`
4. `cloud-and-iac`
5. `cicd-and-release-engineering`
6. `build-automation-and-task-runners`

Mobile sub-phase:

1. `just-enough-kotlin`
2. `android-app-development`
3. `just-enough-swift`
4. `ios-app-development`
5. `just-enough-dart`
6. `hybrid-app-development`

Desktop sub-phase:

1. `just-enough-csharp`
2. `windows-app-development`
3. `linux-app-development`
4. `building-production-cli-tools`
5. `capstone-full-stack-app`

## Phase 3 · Deepening (shallow → deep)

Theory foundations:

1. `computer-science-foundations`
2. `computer-architecture`
3. `programming-paradigms`
4. `functional-programming`

Concurrency:

1. `concurrency-and-parallelism`
2. `just-enough-go`
3. `csp-style-concurrency`
4. `just-enough-elixir`
5. `actor-model-concurrency`

Data depth:

1. `advanced-networking`
2. `advanced-sql-and-query-performance`
3. `data-access-orms-and-query-builders`
4. `build-your-own-orm-and-query-builder`
5. `nosql-databases`
6. `graph-databases`
7. `database-internals-and-storage-engines`
8. `data-engineering`
9. `search-and-information-retrieval`

Architecture & distributed:

1. `software-architecture`
2. `domain-driven-design`
3. `system-design`
4. `event-driven-architecture`
5. `distributed-systems`
6. `build-your-own-web-framework`
7. `build-your-own-reactive-ui`

AI & harness engineering (marquee build-your-own track):

1. `software-engineering-practices`
2. `agentic-coding`
3. `creating-ai-powered-apps`
4. `agentic-ai`
5. `browser-automation-with-cdp` **NEW**
6. `the-agent-loop` **NEW**
7. `agent-tools-and-mcp` **NEW**
8. `agent-context-and-memory` **NEW**
9. `agent-permissions-and-sandboxing` **NEW**
10. `agent-orchestration-subagents-and-observability` **NEW**
11. `capstone-build-your-own-coding-agent` **NEW**

Low-level systems:

1. `just-enough-c`
2. `just-enough-cpp` **NEW**
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

Security suite:

1. `security-essentials`
2. `it-and-application-security`
3. `offensive-security`
4. `defensive-security`
5. `detection-engineering-and-siem-operations` **NEW**
6. `vulnerability-management-and-assessment`
7. `it-governance-grc`
8. `capstone-build-your-own-pentest-engine` **NEW**

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

## Smoothness notes (RD-16)

- **Prereq-chaining** holds; two documented in-context language forward-references (SF-1
  `computer-architecture` uses C before `just-enough-c`; SF-2 `building-production-cli-tools` uses
  Go/Rust before their primers) are softened + bridged **in the course bodies**, never reordered.
- **Phase-boundary bridges**: C-1 (Phase 2 productivity → Phase 3 CS theory) and C-2 (into the
  low-level systems sub-cluster) each carry a bridge paragraph on the path landing narrative.
- **Skip / fast-path**: the prologue is skippable; Phase 1 stands alone; primers are skippable
  ("if you already know X, jump to Y"); the four interview courses use the refresh register.

See [tech-docs §Smoothness Architecture](../tech-docs.md#smoothness-architecture-per-path).
