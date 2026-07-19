# Syllabus — Fundamentally Strong SE, Interview-First Resequence

The **per-topic detail layer** for the resequenced section. Start with
**[overview.md](./overview.md)** — it defines the new canonical arc, the legend, the cross-cutting
authoring guarantees, the capstone policy, and the per-topic file template. The
[frozen tech-docs §Canonical Mapping Table](../tech-docs.md#canonical-mapping-table) is the single
source of truth for topic set, order, slug, short summary, language, format, and weight.

**Columns** — `N` (1-based order in the new arc), `Topic` (slug; linked when a full-detail file
exists in this folder), `Weight` (folder `_index.md` weight = `100 + 10 × N`; capstones carry the
explicit weight `105 + 10 × anchorN`), `Language(s)` and `Short summary` (verbatim from the frozen
table), `Prereqs` (immediate prior-topic dependency in the new arc; the three Addition-4 rows carry
the prereqs recorded in the frozen table).

> **Detail-file status**: the **fourteen NEW modules** and **six capstones** this plan authors have
> full-detail files in this folder (linked below and flagged **NEW** / **capstone**). The **94
> existing topics** keep their subject content from the sibling plan; their lightweight pointer files
> are a **later task** and are therefore listed by slug here without a link.

## Prologue · Editor Foundations (topics 1–3, skippable for the experienced)

| N   | Topic                                                                  | Weight | Language(s)          | Short summary                                         | Prereqs      |
| --- | ---------------------------------------------------------------------- | ------ | -------------------- | ----------------------------------------------------- | ------------ |
| 1   | `just-enough-nvim`                                                     | 110    | Neovim (ex-commands) | Modal editing, motions, buffers, terminal text        | none — entry |
| 2   | `just-enough-lua`                                                      | 120    | Lua                  | Lua fundamentals as Neovim's scripting language       | N=1          |
| 3   | `extending-neovim`                                                     | 130    | Lua                  | Neovim config, plugins, LSP, keymaps in Lua           | N=2          |
| —   | **[`capstone-forge-ready`](./03c-capstone-forge-ready.md)** — capstone | 135    | multi                | Reproducible personal dev forge (nvim + lua + extend) | N=1–3        |

## Phase 1 · Interview Preparation (topics 4–16, through senior)

| N   | Topic                                                                                            | Weight | Language(s)                         | Short summary                                       | Prereqs          |
| --- | ------------------------------------------------------------------------------------------------ | ------ | ----------------------------------- | --------------------------------------------------- | ---------------- |
| 4   | `just-enough-python`                                                                             | 140    | Python                              | Python syntax, types, structures, idioms            | — (Phase 1 head) |
| 5   | `just-enough-bash`                                                                               | 150    | Bash/shell                          | Shell scripting, pipes, redirection, composition    | N=4              |
| 6   | `version-control-and-git`                                                                        | 160    | Git                                 | Version control, branching, merging, history        | —                |
| 7   | `data-structures-and-algorithms-essentials`                                                      | 170    | Python                              | Core data structures and algorithms, complexity     | N=4              |
| 8   | `advanced-algorithms`                                                                            | 180    | Python                              | Graphs, dynamic programming, advanced techniques    | N=7              |
| 9   | **[`coding-interview`](./09-coding-interview.md)** — NEW                                         | 190    | Python (patterns language-agnostic) | Coding-interview patterns, strategy, narration      | N=7, N=8         |
| 10  | **[`take-home-and-live-coding`](./10-take-home-and-live-coding.md)** — NEW                       | 200    | Python                              | Take-home + live/pair-coding technique              | N=9              |
| 11  | `object-oriented-programming-essentials`                                                         | 210    | Python                              | Classes, inheritance, encapsulation, polymorphism   | N=4              |
| 12  | `object-oriented-design-and-patterns`                                                            | 220    | Python                              | SOLID, design patterns, refactoring toward them     | N=11             |
| 13  | `sql-essentials`                                                                                 | 230    | SQL + Python (SQLite)               | Relational modeling, joins, querying with SQL       | N=4              |
| 14  | **[`system-design-interview`](./14-system-design-interview.md)** — NEW                           | 240    | — (concept, no code)                | System-design interview format, rubric, drills      | N=11–13          |
| 15  | `technical-communication`                                                                        | 250    | — (concept, no code)                | Clear docs, proposals, reviews, technical prose     | —                |
| 16  | **[`behavioral-and-leadership-interviews`](./16-behavioral-and-leadership-interviews.md)** — NEW | 260    | — (concept, no code)                | STAR + senior rounds; layoff/gap narrative          | N=15             |
| —   | **[`capstone-interview-loop`](./16c-capstone-interview-loop.md)** — capstone (NEW)               | 265    | Python + prose                      | Full mock loop: coding + system-design + behavioral | N=4–16           |

## Phase 2 · Multi-Platform Productivity (topics 17–39, strict market-demand linear)

### Web sub-phase (17–23)

| N   | Topic                                                                                        | Weight | Language(s)         | Short summary                                        | Prereqs   |
| --- | -------------------------------------------------------------------------------------------- | ------ | ------------------- | ---------------------------------------------------- | --------- |
| 17  | `just-enough-typescript`                                                                     | 270    | TypeScript          | TypeScript types, tooling, idioms for typed JS       | N=4       |
| 18  | `frontend-essentials`                                                                        | 280    | TypeScript          | Interactive web UIs with components and state        | N=17      |
| 19  | `backend-essentials`                                                                         | 290    | Python (PostgreSQL) | HTTP backends with persistence, routing              | N=4, N=13 |
| 20  | **[`async-python-and-fastapi-services`](./20-async-python-and-fastapi-services.md)** — NEW   | 300    | Python              | Async Python, FastAPI, Pydantic, uv/ruff/pyright     | N=19      |
| 21  | `networking-essentials`                                                                      | 310    | Python              | TCP/IP, HTTP, DNS, sockets from first principles     | N=4       |
| 22  | `api-design`                                                                                 | 320    | Python              | REST, versioning, contracts, pragmatic design        | N=19      |
| 23  | `advanced-frontend`                                                                          | 330    | TypeScript          | State management, performance, frontend architecture | N=18      |
| —   | **[`capstone-first-working-software`](./23c-capstone-first-working-software.md)** — capstone | 335    | Python + TS         | First complete secure, tested working web app        | N=4–23    |

### Cloud / backend-at-scale sub-phase (24–29)

| N   | Topic                                                                  | Weight | Language(s)                      | Short summary                                                            | Prereqs                               |
| --- | ---------------------------------------------------------------------- | ------ | -------------------------------- | ------------------------------------------------------------------------ | ------------------------------------- |
| 24  | **[`self-hosting-essentials`](./24-self-hosting-essentials.md)** — NEW | 340    | — (ops/config, minimal app code) | Run one box/VM, self-host a service, reverse proxy, PaaS git-push deploy | N=19 (prereq); strictly below N=26/27 |
| 25  | `backend-at-scale`                                                     | 350    | Python                           | Caching, sharding, queues, scaling backends                              | N=19                                  |
| 26  | `containers-and-orchestration`                                         | 360    | YAML/CLI                         | Docker containers and Kubernetes orchestration                           | N=19, N=24                            |
| 27  | `cloud-and-iac`                                                        | 370    | HCL/YAML                         | Provisioning cloud infrastructure declaratively                          | N=26                                  |
| 28  | `cicd-and-release-engineering`                                         | 380    | YAML + Python                    | Pipelines, artifacts, deployment, release                                | N=26                                  |
| 29  | `build-automation-and-task-runners`                                    | 390    | multi-tool                       | Build systems, task runners, build graphs                                | —                                     |

### Mobile sub-phase (30–35)

| N   | Topic                     | Weight | Language(s) | Short summary                                  | Prereqs |
| --- | ------------------------- | ------ | ----------- | ---------------------------------------------- | ------- |
| 30  | `just-enough-kotlin`      | 400    | Kotlin      | Kotlin syntax, null safety, coroutines         | N=4     |
| 31  | `android-app-development` | 410    | Kotlin      | Native Android apps with Kotlin and the SDK    | N=30    |
| 32  | `just-enough-swift`       | 420    | Swift       | Swift syntax, optionals, value-oriented idioms | —       |
| 33  | `ios-app-development`     | 430    | Swift       | Native iOS apps with Swift and the SDK         | N=32    |
| 34  | `just-enough-dart`        | 440    | Dart        | Dart syntax, async, idioms for Flutter         | —       |
| 35  | `hybrid-app-development`  | 450    | Dart        | Cross-platform apps from one Dart codebase     | N=34    |

### Desktop sub-phase (36–39)

| N   | Topic                                                                        | Weight | Language(s) | Short summary                                 | Prereqs                           |
| --- | ---------------------------------------------------------------------------- | ------ | ----------- | --------------------------------------------- | --------------------------------- |
| 36  | `just-enough-csharp`                                                         | 460    | C#          | C# syntax, LINQ, async, .NET idioms           | —                                 |
| 37  | `windows-app-development`                                                    | 470    | C#          | Native Windows desktop applications in C#     | N=36                              |
| 38  | `linux-app-development`                                                      | 480    | Python      | Native Linux desktop applications, packaging  | N=4                               |
| 39  | `building-production-cli-tools`                                              | 490    | Go + Rust   | Robust, distributable CLI tools in Go/Rust    | N=4 (Go/Rust deepened at N=45/80) |
| —   | **[`capstone-full-stack-app`](./39c-capstone-full-stack-app.md)** — capstone | 495    | TS + Python | Typed frontend ↔ backend ↔ SQL vertical slice | N=10, N=13, N=18, N=19            |

## Phase 3 · Deepening (topics 40–108, shallow → deep)

### Theory foundations (40–43)

| N   | Topic                          | Weight | Language(s) | Short summary                                     | Prereqs |
| --- | ------------------------------ | ------ | ----------- | ------------------------------------------------- | ------- |
| 40  | `computer-science-foundations` | 500    | Python      | Automata, computability, complexity, foundations  | —       |
| 41  | `computer-architecture`        | 510    | C           | CPU, memory, caches, instruction execution        | —       |
| 42  | `programming-paradigms`        | 520    | Python      | Imperative, functional, logic, declarative survey | N=4     |
| 43  | `functional-programming`       | 530    | Python      | Pure functions, immutability, composition, HOFs   | N=42    |

### Concurrency (44–48)

| N   | Topic                         | Weight | Language(s) | Short summary                                         | Prereqs |
| --- | ----------------------------- | ------ | ----------- | ----------------------------------------------------- | ------- |
| 44  | `concurrency-and-parallelism` | 540    | Python      | Threads, async, locks, coordinating work              | N=4     |
| 45  | `just-enough-go`              | 550    | Go          | Go syntax, tooling, goroutines, idioms                | N=4     |
| 46  | `csp-style-concurrency`       | 560    | Go          | Channels, goroutines, CSP-style concurrency           | N=45    |
| 47  | `just-enough-elixir`          | 570    | Elixir      | Elixir syntax, pattern matching, functional idioms    | —       |
| 48  | `actor-model-concurrency`     | 580    | Elixir      | Actors, supervision trees, fault-tolerant concurrency | N=47    |

### Data depth (49–57)

| N   | Topic                                    | Weight | Language(s)               | Short summary                                   | Prereqs |
| --- | ---------------------------------------- | ------ | ------------------------- | ----------------------------------------------- | ------- |
| 49  | `advanced-networking`                    | 590    | Python                    | Load balancing, proxies, TLS, performance       | N=21    |
| 50  | `advanced-sql-and-query-performance`     | 600    | SQL + Python (PostgreSQL) | Query plans, indexing, tuning SQL               | N=13    |
| 51  | `data-access-orms-and-query-builders`    | 610    | Python                    | Using ORMs and query builders safely            | N=13    |
| 52  | `build-your-own-orm-and-query-builder`   | 620    | Python                    | Implementing a small ORM and query builder      | N=51    |
| 53  | `nosql-databases`                        | 630    | Python                    | Document, key-value, column stores              | —       |
| 54  | `graph-databases`                        | 640    | Cypher + Python           | Modeling and querying connected data            | —       |
| 55  | `database-internals-and-storage-engines` | 650    | Python                    | B-trees, LSM-trees, WAL, storage                | —       |
| 56  | `data-engineering`                       | 660    | Python                    | Pipelines, batch/stream processing, warehousing | N=13    |
| 57  | `search-and-information-retrieval`       | 670    | Python                    | Inverted indexes, ranking, full-text search     | —       |

### Architecture & distributed (58–64)

| N   | Topic                          | Weight | Language(s) | Short summary                                   | Prereqs |
| --- | ------------------------------ | ------ | ----------- | ----------------------------------------------- | ------- |
| 58  | `software-architecture`        | 680    | Python      | Architectural styles, tradeoffs, structuring    | —       |
| 59  | `domain-driven-design`         | 690    | Python      | Bounded contexts, ubiquitous language, modeling | N=58    |
| 60  | `system-design`                | 700    | Python      | Designing systems for scale, availability       | N=58    |
| 61  | `event-driven-architecture`    | 710    | Python      | Events, message brokers, event-driven design    | N=60    |
| 62  | `distributed-systems`          | 720    | Python      | Consensus, replication, partitions, CAP         | N=60    |
| 63  | `build-your-own-web-framework` | 730    | Python      | Routing, middleware, a web framework core       | N=22    |
| 64  | `build-your-own-reactive-ui`   | 740    | TypeScript  | Reactive UI library with a virtual DOM          | N=23    |

### AI & harness engineering (65–74, marquee build-your-own track)

| N   | Topic                                                                                                                  | Weight | Language(s)         | Short summary                                                        | Prereqs          |
| --- | ---------------------------------------------------------------------------------------------------------------------- | ------ | ------------------- | -------------------------------------------------------------------- | ---------------- |
| 65  | `software-engineering-practices`                                                                                       | 750    | Python              | Code review, CI, quality gates, team practice                        | —                |
| 66  | `agentic-coding`                                                                                                       | 760    | polyglot            | Driving AI coding agents to plan, generate, verify                   | N=65             |
| 67  | `creating-ai-powered-apps`                                                                                             | 770    | Python              | Integrating LLMs, embeddings, RAG into apps                          | N=4              |
| 68  | `agentic-ai`                                                                                                           | 780    | Python              | Autonomous agents with tools, memory, planning                       | N=67             |
| 69  | **[`browser-automation-with-cdp`](./69-browser-automation-with-cdp.md)** — NEW                                         | 790    | Python (CDP client) | Chrome DevTools Protocol browser automation                          | N=20             |
| 70  | **[`the-agent-loop`](./70-the-agent-loop.md)** — NEW                                                                   | 800    | Python              | LLM tool-use loop, read-eval-act, streaming, stops                   | N=68             |
| 71  | **[`agent-tools-and-mcp`](./71-agent-tools-and-mcp.md)** — NEW                                                         | 810    | Python              | Tool/function schemas; MCP server + client                           | N=70             |
| 72  | **[`agent-context-and-memory`](./72-agent-context-and-memory.md)** — NEW                                               | 820    | Python              | Context budgeting, compaction, retrieval, memory                     | N=70             |
| 73  | **[`agent-permissions-and-sandboxing`](./73-agent-permissions-and-sandboxing.md)** — NEW                               | 830    | Python              | Approval models, sandboxed execution, guardrails                     | N=70             |
| 74  | **[`agent-orchestration-subagents-and-observability`](./74-agent-orchestration-subagents-and-observability.md)** — NEW | 840    | Python              | Sub-agents, background tasks, hooks/skills, TUI, tracing             | N=71, N=72, N=73 |
| —   | **[`capstone-build-your-own-coding-agent`](./74c-capstone-build-your-own-coding-agent.md)** — capstone (NEW)           | 845    | Python              | Build a working agentic coding tool (optional browser-driving bonus) | N=69–74          |

### Low-level systems (75–81)

| N   | Topic                                                  | Weight | Language(s)    | Short summary                                      | Prereqs                                |
| --- | ------------------------------------------------------ | ------ | -------------- | -------------------------------------------------- | -------------------------------------- |
| 75  | `just-enough-c`                                        | 850    | C              | C syntax, pointers, memory, manual management      | N=4                                    |
| 76  | **[`just-enough-cpp`](./76-just-enough-cpp.md)** — NEW | 860    | C++            | C++ syntax, RAII, templates, STL, smart pointers   | N=75 (prereq); difficulty intermediate |
| 77  | `linux-os`                                             | 870    | C + shell      | Processes, syscalls, filesystems, kernel interface | N=75                                   |
| 78  | `windows-os`                                           | 880    | C + PowerShell | Windows internals, the API, PowerShell             | N=75                                   |
| 79  | `system-programming`                                   | 890    | C              | Memory, files, processes, OS-level programming     | N=75                                   |
| 80  | `just-enough-rust`                                     | 900    | Rust           | Rust syntax, ownership, borrowing, type system     | N=75                                   |
| 81  | `modern-system-programming`                            | 910    | Rust           | Safe, high-performance systems programming         | N=80                                   |

### JVM & languages (82–87)

| N   | Topic                               | Weight | Language(s)          | Short summary                                     | Prereqs |
| --- | ----------------------------------- | ------ | -------------------- | ------------------------------------------------- | ------- |
| 82  | `just-enough-java`                  | 920    | Java                 | Java syntax, the JVM, collections, idioms         | —       |
| 83  | `enterprise-java-and-the-jvm`       | 930    | Java                 | Spring, the JVM ecosystem, enterprise patterns    | N=82    |
| 84  | `lisp`                              | 940    | Scheme + Clojure     | Lisp, macros, homoiconic programming              | —       |
| 85  | `just-enough-fsharp`                | 950    | F#                   | F# syntax, discriminated unions, functional-first | —       |
| 86  | `type-systems`                      | 960    | OCaml + Haskell + F# | Algebraic types, inference, ML-family type theory | N=85    |
| 87  | `compilers-parsers-and-transpilers` | 970    | F#                   | Lexers, parsers, ASTs, compilers/transpilers      | N=85    |

### Internals builds (88–90)

| N   | Topic                     | Weight | Language(s) | Short summary                                   | Prereqs    |
| --- | ------------------------- | ------ | ----------- | ----------------------------------------------- | ---------- |
| 88  | `build-your-own-git`      | 980    | Python      | Implementing Git's object model and plumbing    | N=4        |
| 89  | `build-your-own-database` | 990    | Python      | A database with storage, indexing, transactions | N=55       |
| 90  | `build-your-own-raft`     | 1000   | Go          | Raft consensus and a replicated key-value store | N=45, N=62 |

### Security suite (91–97)

| N   | Topic                                                                                                            | Weight | Language(s)                 | Short summary                                                                                 | Prereqs                                |
| --- | ---------------------------------------------------------------------------------------------------------------- | ------ | --------------------------- | --------------------------------------------------------------------------------------------- | -------------------------------------- |
| 91  | `security-essentials`                                                                                            | 1010   | Python                      | Common vulnerabilities, auth, secrets, defaults                                               | N=19                                   |
| 92  | `it-and-application-security`                                                                                    | 1020   | Python                      | Enterprise security controls, identity, hardening                                             | N=91                                   |
| 93  | `offensive-security`                                                                                             | 1030   | Python + shell              | Penetration testing, exploitation, attacker techniques                                        | N=91                                   |
| 94  | `defensive-security`                                                                                             | 1040   | Python + shell              | Detection, monitoring, incident response (concept)                                            | N=91                                   |
| 95  | **[`detection-engineering-and-siem-operations`](./95-detection-engineering-and-siem-operations.md)** — NEW       | 1050   | XML/rules + config + Python | Detection principles: decoders, correlation rules, log parsing, FP tuning, dashboards, triage | N=94 (prereq); difficulty intermediate |
| 96  | `vulnerability-management-and-assessment`                                                                        | 1060   | Python                      | Scanning, triaging, remediating vulnerabilities                                               | N=91                                   |
| 97  | `it-governance-grc`                                                                                              | 1070   | — (concept, no code)        | Governance, risk, compliance, audit frameworks                                                | —                                      |
| —   | **[`capstone-build-your-own-pentest-engine`](./97c-capstone-build-your-own-pentest-engine.md)** — capstone (NEW) | 1075   | TypeScript                  | Build an agentic pentest engine (security sibling of the coding-agent capstone)               | N=68, N=93, N=95                       |

### Ops & platform (98–101)

| N   | Topic                                | Weight | Language(s)          | Short summary                                          | Prereqs |
| --- | ------------------------------------ | ------ | -------------------- | ------------------------------------------------------ | ------- |
| 98  | `bare-metal-virtualization`          | 1080   | HCL/YAML/shell       | Bare-metal hosts and hypervisors below cloud (Proxmox) | N=24    |
| 99  | `self-managed-kubernetes-and-gitops` | 1090   | YAML/CLI             | Self-hosted Kubernetes with GitOps                     | N=26    |
| 100 | `platform-engineering-and-devex`     | 1100   | — (concept, no code) | Internal platforms, golden paths, DevEx                | —       |
| 101 | `site-reliability-engineering`       | 1110   | Python               | SLOs, observability, incident response                 | —       |

### Quality / product / delivery (102–108)

| N   | Topic                              | Weight | Language(s)          | Short summary                                  | Prereqs |
| --- | ---------------------------------- | ------ | -------------------- | ---------------------------------------------- | ------- |
| 102 | `software-testing`                 | 1120   | Python + TypeScript  | Unit, integration, end-to-end testing          | N=4     |
| 103 | `debugging-and-profiling`          | 1130   | Python + native      | Systematic debugging and performance profiling | —       |
| 104 | `analytics-and-experimentation`    | 1140   | Python               | Metrics, A/B testing, product experimentation  | —       |
| 105 | `information-architecture-and-seo` | 1150   | HTML                 | Structuring content, optimizing for search     | —       |
| 106 | `software-product-engineering`     | 1160   | — (concept, no code) | Turning engineering into shipped products      | —       |
| 107 | `engineering-management`           | 1170   | — (concept, no code) | Leading engineers, teams, delivery, direction  | —       |
| 108 | `project-management`               | 1180   | — (concept, no code) | Scoping, planning, estimating, tracking work   | —       |

## Inter-topic capstone index

| Capstone slug                            | Kind               | Anchor (after N) | Weight | File                                                                                             |
| ---------------------------------------- | ------------------ | ---------------- | ------ | ------------------------------------------------------------------------------------------------ |
| `capstone-forge-ready`                   | Prologue boundary  | N=3              | 135    | [03c-capstone-forge-ready.md](./03c-capstone-forge-ready.md)                                     |
| `capstone-interview-loop`                | Phase 1 boundary   | N=16             | 265    | [16c-capstone-interview-loop.md](./16c-capstone-interview-loop.md)                               |
| `capstone-first-working-software`        | Phase 2 web        | N=23             | 335    | [23c-capstone-first-working-software.md](./23c-capstone-first-working-software.md)               |
| `capstone-full-stack-app`                | Phase 2 boundary   | N=39             | 495    | [39c-capstone-full-stack-app.md](./39c-capstone-full-stack-app.md)                               |
| `capstone-build-your-own-coding-agent`   | Phase 3 (harness)  | N=74             | 845    | [74c-capstone-build-your-own-coding-agent.md](./74c-capstone-build-your-own-coding-agent.md)     |
| `capstone-build-your-own-pentest-engine` | Phase 3 (security) | N=97             | 1075   | [97c-capstone-build-your-own-pentest-engine.md](./97c-capstone-build-your-own-pentest-engine.md) |

---

← Previous: [overview.md](./overview.md)
