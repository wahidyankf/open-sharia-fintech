---
title: "Standard Library First Principle"
description: The core standard-library-first principle, why it matters, the progression pattern, and the first half of the topic progression table.
when_to_use: Use when you need the rationale for teaching standard-library approaches before frameworks, or the topic progression table.
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - in-the-field
  - education
  - production-ready
created: 2026-02-04
---

# Standard Library First Principle

**Core Principle**: In-the-field tutorials MUST teach standard library/built-in approaches first, THEN introduce production frameworks with clear rationale.

**Why this matters**:

- **Foundation understanding**: Know primitives before abstractions
- **Informed framework selection**: Understand problems frameworks solve
- **Problem awareness**: See manual implementation complexity
- **Framework independence**: Core knowledge transfers across tools
- **Trade-off comprehension**: Recognize when frameworks add value vs overhead
- **Debugging capability**: Understand what frameworks do under the hood
- **Optimization skills**: Recognize performance bottlenecks and optimization opportunities
- **Production disaster prevention**: Avoid N+1 queries, connection leaks, CPU thrashing from framework misuse

**Progression pattern**:

1. **Show standard library approach** - Demonstrate built-in capabilities
2. **Identify limitations** - Explain why standard approach insufficient for production
3. **Introduce framework** - Show how framework addresses limitations
4. **Compare trade-offs** - Discuss complexity, learning curve, maintenance

**Comprehensive Topic Progression Table**

| Topic                    | Standard Library            | Limitations                                          | Production Framework               | When Framework Justified                 |
| ------------------------ | --------------------------- | ---------------------------------------------------- | ---------------------------------- | ---------------------------------------- |
| **Testing**              | `assert` keyword            | No test organization, no reporting, manual execution | JUnit 5                            | Always (test automation essential)       |
| **HTTP Client**          | `java.net.http.HttpClient`  | No retry, no circuit breaker, limited interceptors   | OkHttp, Spring WebClient           | Resilience needed (production APIs)      |
| **JSON**                 | `javax.json`                | Manual binding, limited type safety                  | Jackson, Gson                      | Complex domains (>10 types)              |
| **Database**             | JDBC                        | Manual mapping, no caching, connection leaks         | JPA/Hibernate                      | Complex domains, relationships           |
| **Connection Pool**      | `DriverManager`             | One connection per request, no pooling               | HikariCP                           | Production (>100 req/sec)                |
| **Build**                | `javac` + `jar`             | No dependencies, manual classpath                    | Maven, Gradle                      | External libraries needed                |
| **Containers**           | `java -jar`                 | No isolation, dependency conflicts                   | Docker                             | Production deployment                    |
| **Orchestration**        | Manual process management   | No auto-scaling, no health checks                    | Kubernetes                         | High availability (>1 instance)          |
| **Logging**              | `System.out.println`        | No levels, no rotation, no structured logs           | SLF4J + Logback                    | Production (log aggregation)             |
| **Configuration**        | Hardcoded values            | No externalization, no secrets management            | Spring Config, Dotenv              | Multiple environments (dev/staging/prod) |
| **Async**                | `Thread`, `ExecutorService` | Manual thread management, callback hell              | Project Reactor, CompletableFuture | High-throughput (>1K req/sec)            |
| **Dependency Injection** | Manual constructor wiring   | Verbose, error-prone lifecycle management            | Spring Framework, Guice            | Complex apps (>20 classes)               |
