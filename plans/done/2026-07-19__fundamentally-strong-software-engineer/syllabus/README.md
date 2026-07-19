# Syllabus — The Fundamentally Strong Software Engineer

The **per-topic detail layer** for this section. Start with **[overview.md](./overview.md)** — it
defines how to read a topic file, the legend, the cross-cutting authoring guarantees, the capstone
policy, and the per-topic file template. The [prd table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks)
remains the single source of truth for topic set, order, slug, format, primary language, and weights;
this folder adds the concrete **Items**, **Worked examples**, **Capstone specs**, dated **Accuracy
notes**, and **Read more** references per topic.

One file per topic — `NN-<slug>.md`, `NN` = order of appearance (01..94). Ten inter-topic capstone
specs are appended inside their anchor topic files (see the
[Capstone Policy](./overview.md#capstone-policy-dd-27)).

## Pass 0 · Editor Foundations (topics 01–03)

| NN  | Topic            | File                                               |
| --- | ---------------- | -------------------------------------------------- |
| 1   | Just Enough Nvim | [01-just-enough-nvim.md](./01-just-enough-nvim.md) |
| 2   | Just Enough Lua  | [02-just-enough-lua.md](./02-just-enough-lua.md)   |
| 3   | Extending Neovim | [03-extending-neovim.md](./03-extending-neovim.md) |

Anchored inter-topic capstone: `capstone-forge-ready` (Pass-0 boundary, in `03-extending-neovim.md`).

## Pass 1 · Core Foundations (topics 04–18)

| NN  | Topic                                   | File                                                                                                 |
| --- | --------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 4   | Just Enough Python                      | [04-just-enough-python.md](./04-just-enough-python.md)                                               |
| 5   | Just Enough Bash                        | [05-just-enough-bash.md](./05-just-enough-bash.md)                                                   |
| 6   | Version Control & Git                   | [06-version-control-and-git.md](./06-version-control-and-git.md)                                     |
| 7   | Data Structures & Algorithms Essentials | [07-data-structures-and-algorithms-essentials.md](./07-data-structures-and-algorithms-essentials.md) |
| 8   | Object-Oriented Programming Essentials  | [08-object-oriented-programming-essentials.md](./08-object-oriented-programming-essentials.md)       |
| 9   | Project Management ▲                    | [09-project-management.md](./09-project-management.md)                                               |
| 10  | SQL Essentials                          | [10-sql-essentials.md](./10-sql-essentials.md)                                                       |
| 11  | Backend Essentials                      | [11-backend-essentials.md](./11-backend-essentials.md)                                               |
| 12  | Networking Essentials                   | [12-networking-essentials.md](./12-networking-essentials.md)                                         |
| 13  | Just Enough TypeScript                  | [13-just-enough-typescript.md](./13-just-enough-typescript.md)                                       |
| 14  | Frontend Essentials                     | [14-frontend-essentials.md](./14-frontend-essentials.md)                                             |
| 15  | Software Testing                        | [15-software-testing.md](./15-software-testing.md)                                                   |
| 16  | Debugging & Profiling                   | [16-debugging-and-profiling.md](./16-debugging-and-profiling.md)                                     |
| 17  | Security Essentials                     | [17-security-essentials.md](./17-security-essentials.md)                                             |
| 18  | Technical Communication                 | [18-technical-communication.md](./18-technical-communication.md)                                     |

Anchored inter-topic capstones (both in `17-security-essentials.md`): `capstone-first-working-software`
(Pass-1 boundary), `capstone-full-stack-app` (cross-cutting).

## Pass 2 · Depth, Design & Craft (topics 19–33)

| NN  | Topic                              | File                                                                                       |
| --- | ---------------------------------- | ------------------------------------------------------------------------------------------ |
| 19  | Computer Science Foundations       | [19-computer-science-foundations.md](./19-computer-science-foundations.md)                 |
| 20  | Computer Architecture              | [20-computer-architecture.md](./20-computer-architecture.md)                               |
| 21  | Object-Oriented Design & Patterns  | [21-object-oriented-design-and-patterns.md](./21-object-oriented-design-and-patterns.md)   |
| 22  | Programming Paradigms              | [22-programming-paradigms.md](./22-programming-paradigms.md)                               |
| 23  | Functional Programming             | [23-functional-programming.md](./23-functional-programming.md)                             |
| 24  | Concurrency & Parallelism          | [24-concurrency-and-parallelism.md](./24-concurrency-and-parallelism.md)                   |
| 25  | Advanced Algorithms                | [25-advanced-algorithms.md](./25-advanced-algorithms.md)                                   |
| 26  | Advanced SQL & Query Performance   | [26-advanced-sql-and-query-performance.md](./26-advanced-sql-and-query-performance.md)     |
| 27  | Data Access: ORMs & Query Builders | [27-data-access-orms-and-query-builders.md](./27-data-access-orms-and-query-builders.md)   |
| 28  | Build Your Own ORM & Query Builder | [28-build-your-own-orm-and-query-builder.md](./28-build-your-own-orm-and-query-builder.md) |
| 29  | Advanced Networking                | [29-advanced-networking.md](./29-advanced-networking.md)                                   |
| 30  | Software Engineering Practices     | [30-software-engineering-practices.md](./30-software-engineering-practices.md)             |
| 31  | Agentic Coding                     | [31-agentic-coding.md](./31-agentic-coding.md)                                             |
| 32  | Software Product Engineering ▲     | [32-software-product-engineering.md](./32-software-product-engineering.md)                 |
| 33  | Engineering Management             | [33-engineering-management.md](./33-engineering-management.md)                             |

Anchored inter-topic capstone: `capstone-solid-core` (Pass-2 boundary, in `33-engineering-management.md`).

## Pass 3 · Build for the Real World (topics 34–63)

| NN  | Topic                                    | File                                                                                             |
| --- | ---------------------------------------- | ------------------------------------------------------------------------------------------------ |
| 34  | NoSQL Databases                          | [34-nosql-databases.md](./34-nosql-databases.md)                                                 |
| 35  | Graph Databases                          | [35-graph-databases.md](./35-graph-databases.md)                                                 |
| 36  | Database Internals & Storage Engines     | [36-database-internals-and-storage-engines.md](./36-database-internals-and-storage-engines.md)   |
| 37  | Data Engineering                         | [37-data-engineering.md](./37-data-engineering.md)                                               |
| 38  | Search & Information Retrieval           | [38-search-and-information-retrieval.md](./38-search-and-information-retrieval.md)               |
| 39  | Backend at Scale                         | [39-backend-at-scale.md](./39-backend-at-scale.md)                                               |
| 40  | Build Your Own Web Framework             | [40-build-your-own-web-framework.md](./40-build-your-own-web-framework.md)                       |
| 41  | API Design                               | [41-api-design.md](./41-api-design.md)                                                           |
| 42  | Software Architecture                    | [42-software-architecture.md](./42-software-architecture.md)                                     |
| 43  | Domain-Driven Design                     | [43-domain-driven-design.md](./43-domain-driven-design.md)                                       |
| 44  | System Design                            | [44-system-design.md](./44-system-design.md)                                                     |
| 45  | Event-Driven Architecture                | [45-event-driven-architecture.md](./45-event-driven-architecture.md)                             |
| 46  | Distributed Systems                      | [46-distributed-systems.md](./46-distributed-systems.md)                                         |
| 47  | Advanced Frontend                        | [47-advanced-frontend.md](./47-advanced-frontend.md)                                             |
| 48  | Build Your Own Reactive UI               | [48-build-your-own-reactive-ui.md](./48-build-your-own-reactive-ui.md)                           |
| 49  | Information Architecture & SEO           | [49-information-architecture-and-seo.md](./49-information-architecture-and-seo.md)               |
| 50  | Containers & Orchestration               | [50-containers-and-orchestration.md](./50-containers-and-orchestration.md)                       |
| 51  | Cloud & IaC                              | [51-cloud-and-iac.md](./51-cloud-and-iac.md)                                                     |
| 52  | Bare-Metal Virtualization                | [52-bare-metal-virtualization.md](./52-bare-metal-virtualization.md)                             |
| 53  | Self-Managed Kubernetes & On-Prem GitOps | [53-self-managed-kubernetes-and-gitops.md](./53-self-managed-kubernetes-and-gitops.md)           |
| 54  | Build Automation & Task Runners          | [54-build-automation-and-task-runners.md](./54-build-automation-and-task-runners.md)             |
| 55  | CI/CD & Release Engineering              | [55-cicd-and-release-engineering.md](./55-cicd-and-release-engineering.md)                       |
| 56  | Creating AI-Powered Apps                 | [56-creating-ai-powered-apps.md](./56-creating-ai-powered-apps.md)                               |
| 57  | Agentic AI                               | [57-agentic-ai.md](./57-agentic-ai.md)                                                           |
| 58  | IT / Application Security                | [58-it-and-application-security.md](./58-it-and-application-security.md)                         |
| 59  | Offensive Security                       | [59-offensive-security.md](./59-offensive-security.md)                                           |
| 60  | Defensive Security                       | [60-defensive-security.md](./60-defensive-security.md)                                           |
| 61  | Vulnerability Management & Assessment    | [61-vulnerability-management-and-assessment.md](./61-vulnerability-management-and-assessment.md) |
| 62  | IT Governance, Risk & Compliance         | [62-it-governance-grc.md](./62-it-governance-grc.md)                                             |
| 63  | Analytics & Experimentation              | [63-analytics-and-experimentation.md](./63-analytics-and-experimentation.md)                     |

Anchored inter-topic capstones (all in `60-defensive-security.md`): `capstone-real-world-delivery`
(Pass-3 boundary), `capstone-secure-service` (cross-cutting), `capstone-data-pipeline` (cross-cutting).

## Pass 4 · Concurrency & Systems (topics 64–89)

| NN  | Topic                            | File                                                                                 |
| --- | -------------------------------- | ------------------------------------------------------------------------------------ |
| 64  | Just Enough Go                   | [64-just-enough-go.md](./64-just-enough-go.md)                                       |
| 65  | CSP-Style Concurrency            | [65-csp-style-concurrency.md](./65-csp-style-concurrency.md)                         |
| 66  | Just Enough Elixir               | [66-just-enough-elixir.md](./66-just-enough-elixir.md)                               |
| 67  | Actor-Model Concurrency          | [67-actor-model-concurrency.md](./67-actor-model-concurrency.md)                     |
| 68  | Just Enough Kotlin               | [68-just-enough-kotlin.md](./68-just-enough-kotlin.md)                               |
| 69  | Android App Development ◆        | [69-android-app-development.md](./69-android-app-development.md)                     |
| 70  | Just Enough Swift                | [70-just-enough-swift.md](./70-just-enough-swift.md)                                 |
| 71  | iOS App Development ◆            | [71-ios-app-development.md](./71-ios-app-development.md)                             |
| 72  | Just Enough Dart                 | [72-just-enough-dart.md](./72-just-enough-dart.md)                                   |
| 73  | Hybrid App Development ◆         | [73-hybrid-app-development.md](./73-hybrid-app-development.md)                       |
| 74  | Just Enough C#                   | [74-just-enough-csharp.md](./74-just-enough-csharp.md)                               |
| 75  | Windows App Development ◆        | [75-windows-app-development.md](./75-windows-app-development.md)                     |
| 76  | Linux App Development ◆          | [76-linux-app-development.md](./76-linux-app-development.md)                         |
| 77  | Building Production CLI Tools    | [77-building-production-cli-tools.md](./77-building-production-cli-tools.md)         |
| 78  | Just Enough C                    | [78-just-enough-c.md](./78-just-enough-c.md)                                         |
| 79  | Linux OS                         | [79-linux-os.md](./79-linux-os.md)                                                   |
| 80  | Windows OS                       | [80-windows-os.md](./80-windows-os.md)                                               |
| 81  | System Programming               | [81-system-programming.md](./81-system-programming.md)                               |
| 82  | Just Enough Rust                 | [82-just-enough-rust.md](./82-just-enough-rust.md)                                   |
| 83  | Modern System Programming        | [83-modern-system-programming.md](./83-modern-system-programming.md)                 |
| 84  | Just Enough Java                 | [84-just-enough-java.md](./84-just-enough-java.md)                                   |
| 85  | Enterprise Java & the JVM        | [85-enterprise-java-and-the-jvm.md](./85-enterprise-java-and-the-jvm.md)             |
| 86  | Lisp                             | [86-lisp.md](./86-lisp.md)                                                           |
| 87  | Just Enough F#                   | [87-just-enough-fsharp.md](./87-just-enough-fsharp.md)                               |
| 88  | Type Systems                     | [88-type-systems.md](./88-type-systems.md)                                           |
| 89  | Compilers, Parsers & Transpilers | [89-compilers-parsers-and-transpilers.md](./89-compilers-parsers-and-transpilers.md) |

Anchored inter-topic capstones (both in `89-compilers-parsers-and-transpilers.md`):
`capstone-concurrency-and-systems` (Pass-4 boundary), `capstone-concurrency-showdown` (cross-cutting).

## Pass 5 · Internals & Lead at Altitude (topics 90–94)

| NN  | Topic                                       | File                                                                           |
| --- | ------------------------------------------- | ------------------------------------------------------------------------------ |
| 90  | Build Your Own Git                          | [90-build-your-own-git.md](./90-build-your-own-git.md)                         |
| 91  | Build Your Own Database                     | [91-build-your-own-database.md](./91-build-your-own-database.md)               |
| 92  | Build Your Own Raft / Replicated KV         | [92-build-your-own-raft.md](./92-build-your-own-raft.md)                       |
| 93  | Platform Engineering & Developer Experience | [93-platform-engineering-and-devex.md](./93-platform-engineering-and-devex.md) |
| 94  | Site Reliability Engineering                | [94-site-reliability-engineering.md](./94-site-reliability-engineering.md)     |

Anchored inter-topic capstone: `capstone-lead-at-altitude` (whole-journey, in
`94-site-reliability-engineering.md`).

## Inter-topic capstone index

| Capstone slug                      | Kind            | Anchor file                               | Weight |
| ---------------------------------- | --------------- | ----------------------------------------- | ------ |
| `capstone-forge-ready`             | Pass-0 boundary | `03-extending-neovim.md`                  | 135    |
| `capstone-first-working-software`  | Pass-1 boundary | `17-security-essentials.md`               | 275    |
| `capstone-full-stack-app`          | cross-cutting   | `17-security-essentials.md`               | 276    |
| `capstone-solid-core`              | Pass-2 boundary | `33-engineering-management.md`            | 435    |
| `capstone-real-world-delivery`     | Pass-3 boundary | `60-defensive-security.md`                | 705    |
| `capstone-secure-service`          | cross-cutting   | `60-defensive-security.md`                | 706    |
| `capstone-data-pipeline`           | cross-cutting   | `60-defensive-security.md`                | 707    |
| `capstone-concurrency-and-systems` | Pass-4 boundary | `89-compilers-parsers-and-transpilers.md` | 995    |
| `capstone-concurrency-showdown`    | cross-cutting   | `89-compilers-parsers-and-transpilers.md` | 996    |
| `capstone-lead-at-altitude`        | whole-journey   | `94-site-reliability-engineering.md`      | 1045   |

Each inter-topic capstone weight slots immediately after its host topic's folder weight
(`(100 + 10 × NN) + 5`), so it sorts right after the topic that anchors it.
