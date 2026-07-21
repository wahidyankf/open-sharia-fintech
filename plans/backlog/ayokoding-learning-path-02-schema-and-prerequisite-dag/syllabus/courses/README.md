# Course Library Catalog — Fundamentally Strong Shared Course Library

The **per-course-block detail layer**: the index of the **127-course catalog** and the folder that
holds one **`<course-id>.md`** detail file per course. Start with the
**[syllabus root README](../README.md)** for the shared-library-plus-three-paths architecture, the
legend, the authoring guarantees, the capstone policy, and the per-course file template. The
[tech-docs §Course Library Catalog](../../tech-docs.md#course-library-catalog) is the single source of
truth for the course set, IDs, format, language, and short summary. **Order is NOT a catalog
property** — it lives in the three [path manifests](../paths/README.md):

- **[interview-ready/software-engineer](../paths/manifest-interview-ready-software-engineer.md)** — the
  interview-first ordered manifest (ships first).
- **[immediately-effective/software-engineer](../paths/manifest-immediately-effective-software-engineer.md)**
  — the shipping-first ordered manifest.
- **[fundamentally-strong/software-engineer](../paths/manifest-fundamentally-strong-software-engineer.md)**
  — the university-style, fundamentals-first ordered manifest.

Every manifest reuses the same course bodies reordered — **zero body duplication**.

**Columns** — `Course ID` (stable slug; linked to its detail file), `Format`, `Language(s)`,
`Short summary`. NEW = a course this plan authors; the rest are re-homed existing courses.

> **Detail-file status**: the **twenty NEW courses** and **five capstones** (the three NEW capstones
> and the two existing capstones with substantial integration content) have full-content, standalone
> `capstone-*.md` files in this folder (linked below and flagged **NEW** / **capstone**). The **95
> existing courses** (94 existing topics and `capstone-forge-ready`) carry full-content, non-pointer
> files inherited verbatim from the sibling plan, linked by course ID. **Seven additional inter-topic
> capstones** (`capstone-solid-core`, `capstone-real-world-delivery`, `capstone-secure-service`,
> `capstone-data-pipeline`, `capstone-concurrency-and-systems`, `capstone-concurrency-showdown`,
> `capstone-lead-at-altitude`) do **not** have a standalone `capstone-*.md` file — each is a
> full-detail spec (goal, integrated-concepts checklist, ordered steps, acceptance criteria, done bar)
> embedded inside its host topic's file (`engineering-management.md`, `defensive-security.md` ×3,
> `compilers-parsers-and-transpilers.md` ×2, `site-reliability-engineering.md`); see
> [DD-20](../../tech-docs.md#design-decisions) for the reconciliation ruling.

## Editor & tooling foundations

| Course ID                                                 | Format     | Language(s)          | Short summary                                    |
| --------------------------------------------------------- | ---------- | -------------------- | ------------------------------------------------ |
| [`just-enough-nvim`](./just-enough-nvim.md)               | Primer     | Neovim (ex-commands) | Modal editing, motions, buffers, terminal text   |
| [`just-enough-lua`](./just-enough-lua.md)                 | Primer     | Lua                  | Lua fundamentals as Neovim's scripting language  |
| [`extending-neovim`](./extending-neovim.md)               | By Example | Lua                  | Neovim config, plugins, LSP, keymaps in Lua      |
| [`just-enough-python`](./just-enough-python.md)           | Primer     | Python               | Python syntax, types, structures, idioms         |
| [`just-enough-bash`](./just-enough-bash.md)               | Primer     | Bash/shell           | Shell scripting, pipes, redirection, composition |
| [`version-control-and-git`](./version-control-and-git.md) | By Example | Git                  | Version control, branching, merging, history     |

## Coding, DS&A & interview technique

| Course ID                                                                                     | Format            | Language(s)          | Short summary                                     |
| --------------------------------------------------------------------------------------------- | ----------------- | -------------------- | ------------------------------------------------- |
| [`data-structures-and-algorithms-essentials`](./data-structures-and-algorithms-essentials.md) | By Example        | Python               | Core data structures and algorithms, complexity   |
| [`advanced-algorithms`](./advanced-algorithms.md)                                             | By Example        | Python               | Graphs, dynamic programming, advanced techniques  |
| **[`coding-interview`](./coding-interview.md)** — NEW                                         | By Example        | Python (agnostic)    | Coding-interview patterns, strategy, narration    |
| **[`take-home-and-live-coding`](./take-home-and-live-coding.md)** — NEW                       | By Example        | Python               | Take-home + live/pair-coding technique            |
| [`object-oriented-programming-essentials`](./object-oriented-programming-essentials.md)       | By Example        | Python               | Classes, inheritance, encapsulation, polymorphism |
| [`object-oriented-design-and-patterns`](./object-oriented-design-and-patterns.md)             | By Example        | Python               | SOLID, design patterns, refactoring toward them   |
| [`sql-essentials`](./sql-essentials.md)                                                       | By Example        | SQL + Python         | Relational modeling, joins, querying with SQL     |
| **[`system-design-interview`](./system-design-interview.md)** — NEW                           | Annotated-concept | — (concept, no code) | System-design interview format, rubric, drills    |
| [`technical-communication`](./technical-communication.md)                                     | Annotated-concept | — (concept, no code) | Clear docs, proposals, reviews, technical prose   |
| **[`behavioral-and-leadership-interviews`](./behavioral-and-leadership-interviews.md)** — NEW | Annotated-concept | — (concept, no code) | STAR + senior rounds; layoff/gap narrative        |

## Web & platform productivity

| Course ID                                                                               | Format            | Language(s)                      | Short summary                                        |
| --------------------------------------------------------------------------------------- | ----------------- | -------------------------------- | ---------------------------------------------------- |
| [`just-enough-typescript`](./just-enough-typescript.md)                                 | Primer            | TypeScript                       | TypeScript types, tooling, idioms for typed JS       |
| [`frontend-essentials`](./frontend-essentials.md)                                       | By Example        | TypeScript                       | Interactive web UIs with components and state        |
| [`backend-essentials`](./backend-essentials.md)                                         | By Example        | Python (PostgreSQL)              | HTTP backends with persistence, routing              |
| **[`async-python-and-fastapi-services`](./async-python-and-fastapi-services.md)** — NEW | By Example        | Python                           | Async Python, FastAPI, Pydantic, uv/ruff/pyright     |
| [`networking-essentials`](./networking-essentials.md)                                   | By Example        | Python                           | TCP/IP, HTTP, DNS, sockets from first principles     |
| [`api-design`](./api-design.md)                                                         | By Example        | Python                           | REST, versioning, contracts, pragmatic design        |
| [`advanced-frontend`](./advanced-frontend.md)                                           | By Example        | TypeScript                       | State management, performance, frontend architecture |
| **[`self-hosting-essentials`](./self-hosting-essentials.md)** — NEW                     | By Example        | — (ops/config, minimal app code) | Run one box/VM, self-host a service, PaaS deploy     |
| [`backend-at-scale`](./backend-at-scale.md)                                             | By Example        | Python                           | Caching, sharding, queues, scaling backends          |
| [`containers-and-orchestration`](./containers-and-orchestration.md)                     | By Example        | YAML/CLI                         | Docker containers and Kubernetes orchestration       |
| [`cloud-and-iac`](./cloud-and-iac.md)                                                   | Annotated-concept | HCL/YAML                         | Provisioning cloud infrastructure declaratively      |
| [`cicd-and-release-engineering`](./cicd-and-release-engineering.md)                     | By Example        | YAML + Python                    | Pipelines, artifacts, deployment, release            |
| [`build-automation-and-task-runners`](./build-automation-and-task-runners.md)           | By Example        | multi-tool                       | Build systems, task runners, build graphs            |

## Mobile & desktop platforms

| Course ID                                                             | Format     | Language(s) | Short summary                                  |
| --------------------------------------------------------------------- | ---------- | ----------- | ---------------------------------------------- |
| [`just-enough-kotlin`](./just-enough-kotlin.md)                       | Primer     | Kotlin      | Kotlin syntax, null safety, coroutines         |
| [`android-app-development`](./android-app-development.md)             | By Example | Kotlin      | Native Android apps with Kotlin and the SDK    |
| [`just-enough-swift`](./just-enough-swift.md)                         | Primer     | Swift       | Swift syntax, optionals, value-oriented idioms |
| [`ios-app-development`](./ios-app-development.md)                     | By Example | Swift       | Native iOS apps with Swift and the SDK         |
| [`just-enough-dart`](./just-enough-dart.md)                           | Primer     | Dart        | Dart syntax, async, idioms for Flutter         |
| [`hybrid-app-development`](./hybrid-app-development.md)               | By Example | Dart        | Cross-platform apps from one Dart codebase     |
| [`just-enough-csharp`](./just-enough-csharp.md)                       | Primer     | C#          | C# syntax, LINQ, async, .NET idioms            |
| [`windows-app-development`](./windows-app-development.md)             | By Example | C#          | Native Windows desktop applications in C#      |
| [`linux-app-development`](./linux-app-development.md)                 | By Example | Python      | Native Linux desktop applications, packaging   |
| [`building-production-cli-tools`](./building-production-cli-tools.md) | By Example | Go + Rust   | Robust, distributable CLI tools in Go/Rust     |

## CS foundations, paradigms & concurrency

| Course ID                                                           | Format            | Language(s) | Short summary                                         |
| ------------------------------------------------------------------- | ----------------- | ----------- | ----------------------------------------------------- |
| [`computer-science-foundations`](./computer-science-foundations.md) | Annotated-concept | Python      | Automata, computability, complexity, foundations      |
| [`computer-architecture`](./computer-architecture.md)               | By Example        | C           | CPU, memory, caches, instruction execution            |
| [`programming-paradigms`](./programming-paradigms.md)               | By Example        | Python      | Imperative, functional, logic, declarative survey     |
| [`functional-programming`](./functional-programming.md)             | By Example        | Python      | Pure functions, immutability, composition, HOFs       |
| [`concurrency-and-parallelism`](./concurrency-and-parallelism.md)   | By Example        | Python      | Threads, async, locks, coordinating work              |
| [`just-enough-go`](./just-enough-go.md)                             | Primer            | Go          | Go syntax, tooling, goroutines, idioms                |
| [`csp-style-concurrency`](./csp-style-concurrency.md)               | By Example        | Go          | Channels, goroutines, CSP-style concurrency           |
| [`just-enough-elixir`](./just-enough-elixir.md)                     | Primer            | Elixir      | Elixir syntax, pattern matching, functional idioms    |
| [`actor-model-concurrency`](./actor-model-concurrency.md)           | By Example        | Elixir      | Actors, supervision trees, fault-tolerant concurrency |

## Data depth

| Course ID                                                                               | Format            | Language(s)               | Short summary                                   |
| --------------------------------------------------------------------------------------- | ----------------- | ------------------------- | ----------------------------------------------- |
| [`advanced-networking`](./advanced-networking.md)                                       | Annotated-concept | Python                    | Load balancing, proxies, TLS, performance       |
| [`advanced-sql-and-query-performance`](./advanced-sql-and-query-performance.md)         | By Example        | SQL + Python (PostgreSQL) | Query plans, indexing, tuning SQL               |
| [`data-access-orms-and-query-builders`](./data-access-orms-and-query-builders.md)       | By Example        | Python                    | Using ORMs and query builders safely            |
| [`build-your-own-orm-and-query-builder`](./build-your-own-orm-and-query-builder.md)     | By Example        | Python                    | Implementing a small ORM and query builder      |
| [`nosql-databases`](./nosql-databases.md)                                               | By Example        | Python                    | Document, key-value, column stores              |
| [`graph-databases`](./graph-databases.md)                                               | By Example        | Cypher + Python           | Modeling and querying connected data            |
| [`database-internals-and-storage-engines`](./database-internals-and-storage-engines.md) | By Example        | Python                    | B-trees, LSM-trees, WAL, storage                |
| [`data-engineering`](./data-engineering.md)                                             | Annotated-concept | Python                    | Pipelines, batch/stream processing, warehousing |
| [`search-and-information-retrieval`](./search-and-information-retrieval.md)             | By Example        | Python                    | Inverted indexes, ranking, full-text search     |

## Architecture, distributed & AI/harness

| Course ID                                                                                                           | Format            | Language(s)          | Short summary                                       |
| ------------------------------------------------------------------------------------------------------------------- | ----------------- | -------------------- | --------------------------------------------------- |
| [`software-architecture`](./software-architecture.md)                                                               | Annotated-concept | Python               | Architectural styles, tradeoffs, structuring        |
| [`domain-driven-design`](./domain-driven-design.md)                                                                 | By Example        | Python               | Bounded contexts, ubiquitous language, modeling     |
| [`system-design`](./system-design.md)                                                                               | Annotated-concept | Python               | Designing systems for scale, availability           |
| [`event-driven-architecture`](./event-driven-architecture.md)                                                       | By Example        | Python               | Events, message brokers, event-driven design        |
| [`distributed-systems`](./distributed-systems.md)                                                                   | By Example        | Python               | Consensus, replication, partitions, CAP             |
| [`build-your-own-web-framework`](./build-your-own-web-framework.md)                                                 | By Example        | Python               | Routing, middleware, a web framework core           |
| [`build-your-own-reactive-ui`](./build-your-own-reactive-ui.md)                                                     | By Example        | TypeScript           | Reactive UI library with a virtual DOM              |
| [`software-engineering-practices`](./software-engineering-practices.md)                                             | Annotated-concept | Python               | Code review, CI, quality gates, team practice       |
| [`agentic-coding`](./agentic-coding.md)                                                                             | Annotated-concept | polyglot             | Driving AI coding agents to plan, generate, verify  |
| [`creating-ai-powered-apps`](./creating-ai-powered-apps.md)                                                         | By Example        | Python               | Integrating LLMs, embeddings, RAG into apps         |
| [`agentic-ai`](./agentic-ai.md)                                                                                     | By Example        | Python               | Autonomous agents with tools, memory, planning      |
| **[`browser-automation-with-cdp`](./browser-automation-with-cdp.md)** — NEW                                         | By Example        | Python (CDP client)  | Chrome DevTools Protocol browser automation         |
| **[`the-agent-loop`](./the-agent-loop.md)** — NEW                                                                   | By Example        | Python               | LLM tool-use loop, read-eval-act, streaming, stops  |
| **[`agent-tools-and-mcp`](./agent-tools-and-mcp.md)** — NEW                                                         | By Example        | Python               | Tool/function schemas; MCP server + client          |
| **[`agent-context-and-memory`](./agent-context-and-memory.md)** — NEW                                               | Annotated-concept | Python               | Context budgeting, compaction, retrieval, memory    |
| **[`agent-permissions-and-sandboxing`](./agent-permissions-and-sandboxing.md)** — NEW                               | By Example        | Python               | Approval models, sandboxed execution, guardrails    |
| **[`agent-orchestration-subagents-and-observability`](./agent-orchestration-subagents-and-observability.md)** — NEW | Annotated-concept | Python               | Sub-agents, background tasks, hooks/skills, tracing |
| **[`evaluating-ai-output-essentials`](./evaluating-ai-output-essentials.md)** — NEW                                 | Annotated-concept | Python               | Light eval gate: dataset, scorers, pass rate        |
| **[`evaluating-ai-systems-in-depth`](./evaluating-ai-systems-in-depth.md)** — NEW                                   | By Example        | Python               | Error analysis, validated judges, CI eval gating    |
| **[`statistics-for-evaluation`](./statistics-for-evaluation.md)** — NEW                                             | Annotated-concept | Python               | Agreement, sampling, intervals, significance        |
| **[`product-patterns-for-probabilistic-systems`](./product-patterns-for-probabilistic-systems.md)** — NEW           | Annotated-concept | — (concept, no code) | UX for uncertainty, human review, ship/rollback     |
| **[`inference-serving-and-model-deployment`](./inference-serving-and-model-deployment.md)** — NEW                   | By Example        | Python               | KV cache, batching, GPU capacity, self-hosting      |
| **[`fine-tuning-and-adaptation`](./fine-tuning-and-adaptation.md)** — NEW                                           | By Example        | Python               | SFT, LoRA/PEFT, datasets, when to avoid it          |

## Low-level systems, JVM & languages, internals builds

| Course ID                                                                     | Format     | Language(s)          | Short summary                                      |
| ----------------------------------------------------------------------------- | ---------- | -------------------- | -------------------------------------------------- |
| [`just-enough-c`](./just-enough-c.md)                                         | Primer     | C                    | C syntax, pointers, memory, manual management      |
| **[`just-enough-cpp`](./just-enough-cpp.md)** — NEW                           | Primer     | C++                  | C++ syntax, RAII, templates, STL, smart pointers   |
| [`linux-os`](./linux-os.md)                                                   | By Example | C + shell            | Processes, syscalls, filesystems, kernel interface |
| [`windows-os`](./windows-os.md)                                               | By Example | C + PowerShell       | Windows internals, the API, PowerShell             |
| [`system-programming`](./system-programming.md)                               | By Example | C                    | Memory, files, processes, OS-level programming     |
| [`just-enough-rust`](./just-enough-rust.md)                                   | Primer     | Rust                 | Rust syntax, ownership, borrowing, type system     |
| [`modern-system-programming`](./modern-system-programming.md)                 | By Example | Rust                 | Safe, high-performance systems programming         |
| [`just-enough-java`](./just-enough-java.md)                                   | Primer     | Java                 | Java syntax, the JVM, collections, idioms          |
| [`enterprise-java-and-the-jvm`](./enterprise-java-and-the-jvm.md)             | By Example | Java                 | Spring, the JVM ecosystem, enterprise patterns     |
| [`lisp`](./lisp.md)                                                           | By Example | Scheme + Clojure     | Lisp, macros, homoiconic programming               |
| [`just-enough-fsharp`](./just-enough-fsharp.md)                               | Primer     | F#                   | F# syntax, discriminated unions, functional-first  |
| [`type-systems`](./type-systems.md)                                           | By Example | OCaml + Haskell + F# | Algebraic types, inference, ML-family type theory  |
| [`compilers-parsers-and-transpilers`](./compilers-parsers-and-transpilers.md) | By Example | F#                   | Lexers, parsers, ASTs, compilers/transpilers       |
| [`build-your-own-git`](./build-your-own-git.md)                               | By Example | Python               | Implementing Git's object model and plumbing       |
| [`build-your-own-database`](./build-your-own-database.md)                     | By Example | Python               | A database with storage, indexing, transactions    |
| [`build-your-own-raft`](./build-your-own-raft.md)                             | By Example | Go                   | Raft consensus and a replicated key-value store    |

## Security, ops, quality & delivery

| Course ID                                                                                               | Format            | Language(s)                 | Short summary                                          |
| ------------------------------------------------------------------------------------------------------- | ----------------- | --------------------------- | ------------------------------------------------------ |
| [`security-essentials`](./security-essentials.md)                                                       | By Example        | Python                      | Common vulnerabilities, auth, secrets, defaults        |
| [`it-and-application-security`](./it-and-application-security.md)                                       | Annotated-concept | Python                      | Enterprise security controls, identity, hardening      |
| [`offensive-security`](./offensive-security.md)                                                         | By Example        | Python + shell              | Penetration testing, exploitation, attacker techniques |
| [`defensive-security`](./defensive-security.md)                                                         | By Example        | Python + shell              | Detection, monitoring, incident response (concept)     |
| **[`detection-engineering-and-siem-operations`](./detection-engineering-and-siem-operations.md)** — NEW | By Example        | XML/rules + config + Python | Decoders, correlation rules, FP tuning, dashboards     |
| [`vulnerability-management-and-assessment`](./vulnerability-management-and-assessment.md)               | By Example        | Python                      | Scanning, triaging, remediating vulnerabilities        |
| [`it-governance-grc`](./it-governance-grc.md)                                                           | Annotated-concept | — (concept, no code)        | Governance, risk, compliance, audit frameworks         |
| [`bare-metal-virtualization`](./bare-metal-virtualization.md)                                           | By Example        | HCL/YAML/shell              | Bare-metal hosts and hypervisors (Proxmox)             |
| [`self-managed-kubernetes-and-gitops`](./self-managed-kubernetes-and-gitops.md)                         | By Example        | YAML/CLI                    | Self-hosted Kubernetes with GitOps                     |
| [`platform-engineering-and-devex`](./platform-engineering-and-devex.md)                                 | Annotated-concept | — (concept, no code)        | Internal platforms, golden paths, DevEx                |
| [`site-reliability-engineering`](./site-reliability-engineering.md)                                     | Annotated-concept | Python                      | SLOs, observability, incident response                 |
| [`software-testing`](./software-testing.md)                                                             | By Example        | Python + TypeScript         | Unit, integration, end-to-end testing                  |
| [`debugging-and-profiling`](./debugging-and-profiling.md)                                               | By Example        | Python + native             | Systematic debugging and performance profiling         |
| [`analytics-and-experimentation`](./analytics-and-experimentation.md)                                   | By Example        | Python                      | Metrics, A/B testing, product experimentation          |
| [`information-architecture-and-seo`](./information-architecture-and-seo.md)                             | Annotated-concept | HTML                        | Structuring content, optimizing for search             |
| [`software-product-engineering`](./software-product-engineering.md)                                     | Annotated-concept | — (concept, no code)        | Turning engineering into shipped products              |
| [`engineering-management`](./engineering-management.md)                                                 | Annotated-concept | — (concept, no code)        | Leading engineers, teams, delivery, direction          |
| [`project-management`](./project-management.md)                                                         | Annotated-concept | — (concept, no code)        | Scoping, planning, estimating, tracking work           |

## Capstones (each a course/building block)

| Course ID                                                                                         | Kind                 | Language(s)    | Short summary                                       |
| ------------------------------------------------------------------------------------------------- | -------------------- | -------------- | --------------------------------------------------- |
| [`capstone-forge-ready`](./capstone-forge-ready.md)                                               | Prologue milestone   | multi          | Reproducible dev forge (nvim + lua + extend)        |
| **[`capstone-interview-loop`](./capstone-interview-loop.md)** — NEW                               | Interview milestone  | Python + prose | Full mock loop: coding + system-design + behavioral |
| [`capstone-first-working-software`](./capstone-first-working-software.md)                         | Web milestone        | Python + TS    | First complete secure, tested working web app       |
| [`capstone-full-stack-app`](./capstone-full-stack-app.md)                                         | Full-stack milestone | TS + Python    | Typed frontend ↔ backend ↔ SQL vertical slice       |
| **[`capstone-build-your-own-coding-agent`](./capstone-build-your-own-coding-agent.md)** — NEW     | Harness milestone    | Python         | Build a working agentic coding tool                 |
| **[`capstone-build-your-own-pentest-engine`](./capstone-build-your-own-pentest-engine.md)** — NEW | Security milestone   | TypeScript     | Build an agentic pentest engine                     |

**Seven DD-20 inter-topic capstones** (added 2026-07-19; specs embedded in their host topic's file,
no standalone `capstone-*.md`):

| Course ID                                                                                                                                                          | Kind                    | Language(s)       | Short summary                                                     |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------- | ----------------- | ----------------------------------------------------------------- |
| [`capstone-solid-core`](./engineering-management.md#capstone-spec--inter-topic-capstone-solid-core-pass-2-boundary) — **live**                                     | Pass-boundary milestone | Python + TS       | Re-engineer the Pass-1 app to a SOLID/functional-core baseline    |
| **[`capstone-real-world-delivery`](./defensive-security.md#capstone-spec--inter-topic-capstone-real-world-delivery-pass-3-boundary)** — NEW                        | Full-stack milestone    | Python + TS + IaC | Deploy-as-code, secured, observable delivery of the Pass-2 app    |
| **[`capstone-secure-service`](./defensive-security.md#capstone-spec--inter-topic-capstone-secure-service-cross-cutting)** — NEW                                    | Security milestone      | Python + shell    | End-to-end secured HTTP service, red/blue-team validated          |
| **[`capstone-data-pipeline`](./defensive-security.md#capstone-spec--inter-topic-capstone-data-pipeline-cross-cutting)** — NEW                                      | Data milestone          | SQL + Python      | Medallion pipeline → governed warehouse → RAG-grounded interface  |
| **[`capstone-concurrency-and-systems`](./compilers-parsers-and-transpilers.md#capstone-spec--inter-topic-capstone-concurrency-and-systems-pass-4-boundary)** — NEW | Systems milestone       | Go or Elixir + C  | Concurrent, containerized, SRE-instrumented service               |
| **[`capstone-concurrency-showdown`](./compilers-parsers-and-transpilers.md#capstone-spec--inter-topic-capstone-concurrency-showdown-cross-cutting)** — NEW         | Comparison milestone    | Go + Elixir       | Same problem solved CSP-Go vs actor-Elixir, compared head-to-head |
| **[`capstone-lead-at-altitude`](./site-reliability-engineering.md#capstone-spec--inter-topic-capstone-lead-at-altitude-whole-journey)** — NEW                      | Whole-journey milestone | polyglot + prose  | Whole-journey leadership synthesis: SLOs, strategy, retrospective |

See [DD-20](../../tech-docs.md#design-decisions) for the reconciliation ruling and placement rationale.

## Path manifests (orderings over this library)

The [path manifests](../paths/README.md) each impose one ordering over this catalog. The three
software-engineer-role paths order the software-engineer-role courses; the AI-engineer-transition
path composes a short AI-specific spine (linked prerequisites, not included):

- **[interview-ready/software-engineer](../paths/manifest-interview-ready-software-engineer.md)** —
  interview-first order (ships first).
- **[immediately-effective/software-engineer](../paths/manifest-immediately-effective-software-engineer.md)**
  — shipping-first order (build a real app first, then deepen).
- **[fundamentally-strong/software-engineer](../paths/manifest-fundamentally-strong-software-engineer.md)**
  — fundamentals-first, university-style order.
- **[immediately-effective/software-engineer-to-ai-engineer](../paths/manifest-immediately-effective-software-engineer-to-ai-engineer.md)**
  — AI-engineer transition spine (converges on the AI-engineer endpoint, per-role, not the
  software-engineer one).

Zero body duplication — every manifest references the same course IDs reordered.

## How to read a course file

Each `<course-id>.md` carries these sections in order:

1. **Header** — title, course ID, format, language, scope note. **No single order index** (order is
   per-path; see the path manifests).
2. **Why this exists · the big idea** — the problem before the solution, the keep-forever mental model,
   the cross-cutting big ideas.
3. **Prerequisites** — prior **courses** (by ID) this builds on, tools & environment, assumed knowledge.
   (Prereqs are course-level, not path-level; a path's order must respect them.)
4. **Accuracy notes** — dated `web-researcher` findings; version-sensitive items `[Needs Verification]`.
5. **Concepts** — the numbered `co-NN` enumeration (floor, not cap).
6. **Tensions & trade-offs + Lineage** — judgment courses only.
7. **Worked examples** — the numbered `ex-NN` enumeration; each cites the `co-NN` it demonstrates.
8. **Capstone spec** — the course's intra-course capstone (and, in the six standalone capstone files
   plus the seven DD-20 host-topic files, the full inter-course capstone spec).
9. **In which paths** — which path manifests list this course, and where (order is path-dependent).

## Legend (format markers)

- **Primer** — a _Just Enough_ language on-ramp (fluency, not judgment).
- **By Example** — worked-code subject course (Beginner / Intermediate / Advanced bands).
- **Annotated-concept** — concept-centric course; code where it fits, prose + WCAG-accessible Mermaid
  where it does not.
- **— (concept, no code)** — leadership / governance / format courses: prose, worked scenarios,
  artifacts, no runnable code.

## Cross-cutting authoring guarantees

- **Coverage is a floor, not a cap** — the `co-NN` / `ex-NN` counts are the minimum a course must reach
  at authoring time; a maker may add more, never fewer, reaching the per-format volume band in
  [prd.md §Volume-target bands](../../prd.md#new-course--capstone-specifications).
- **Raw-form-first tooling** — Neovim + terminal build/run/test/debug/git on a macOS/Linux-compatible
  environment; IDE-mandatory app domains called out in place.
- **Free-to-use-and-teachable-first materials**; **CVE-free dependencies** pinned to exact clean
  versions; **follow-along completeness**; **principle-first, not tutorial-first**.

## Capstone policy

Every subject course ships an **intra-course capstone**. The library additionally holds **thirteen
inter-course capstones**: six with standalone files (`capstone-forge-ready`, `capstone-interview-loop`,
`capstone-first-working-software`, `capstone-full-stack-app`, `capstone-build-your-own-coding-agent`,
`capstone-build-your-own-pentest-engine`) and seven DD-20 inter-topic capstones whose specs are
embedded in a host topic's file (`capstone-solid-core`, `capstone-real-world-delivery`,
`capstone-secure-service`, `capstone-data-pipeline`, `capstone-concurrency-and-systems`,
`capstone-concurrency-showdown`, `capstone-lead-at-altitude`) — each a course in its own right (a
building block with a stable ID), placed by each path's manifest at the appropriate boundary. Each
capstone spec states (a) goal/outcome, (b) a concepts-exercised checklist, (c) an ordered step outline
(file + code + verify command), (d) testable acceptance criteria, and (e) the done bar = **runnable
end-to-end + web-verified**.

## Per-course file template

```markdown
# <Title> (<Format>, <Language>)

**Course ID**: `<course-id>` · **Format**: <Format> · **Language**: <Language>.

**Scope note**: <what this course covers; what it defers to a deeper course>.

## Why this exists · the big idea

- **The problem before the solution**: …
- **Keep-this-if-you-forget-everything**: …
- **Big ideas touched**: …

## Prerequisites

- **Prior courses**: <course-ids this builds on, or "none — entry point">.
- **Tools & environment**: <pinned toolchain + OS/platform assumption>.
- **Assumed knowledge**: …

## Accuracy notes

- <YYYY-MM-DD> — <finding, flagged [Needs Verification] until the pre-authoring sweep runs>.

## Concepts

1. **co-01 · <slug>** — <one-line claim>. … (floor ≥ 10 subject / ≥ 8 primer|leadership)

## Worked examples

1. **ex-01 · <slug>** — <one-line spec> — verify <observable>. (co-NN) … (contiguous)

## Capstone spec — intra-course (<kind>)

- **Goal**: … · **Concepts exercised**: [ ] … · **Ordered steps**: 1. `<file>` — <code> — verify `<cmd>`
- **Acceptance criteria**: … · **Done bar**: runnable end-to-end + web-verified.

## In which paths

- `interview-ready/software-engineer` — <phase/position>. (Omit this bullet entirely if the course is
  genuinely omitted from this path's manifest — see the actual course files for the established
  convention.)
- `immediately-effective/software-engineer` — <stage/position>. (Omit if genuinely omitted.)
- `fundamentally-strong/software-engineer` — <stage/position>. (Never omitted — the complete-mastery
  path includes every course.)
```

---

← Back to the [syllabus root README](../README.md)
