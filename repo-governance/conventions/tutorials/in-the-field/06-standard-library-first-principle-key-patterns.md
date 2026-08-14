---
title: "Standard Library First Principle: Key Patterns and Example"
description: Which topics always need a framework versus when the standard library suffices, plus a worked JSON-processing progression example.
when_to_use: Use when deciding whether a specific topic justifies introducing a production framework.
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

# Standard Library First Principle: Key Patterns and Example

**Key Patterns by Production Complexity**:

**Always Use Framework** (core production requirements):

- Testing: JUnit/TestNG (automation essential)
- Build: Maven/Gradle (dependency management)
- Logging: SLF4J (log levels, rotation)
- Security: BCrypt (proper hashing)

**Use Framework for Production Scale** (performance/resilience):

- HTTP: OkHttp (>100 req/sec, retry needed)
- Database: Hibernate (complex domains, >10 entities)
- Async: Reactor (>1K concurrent operations)
- Caching: Redis/Caffeine (high read load)

**Use Framework for Complex Systems** (orchestration/integration):

- DI: Spring (>20 classes, complex wiring)
- Messaging: Kafka (distributed, high throughput)
- Orchestration: Kubernetes (>1 instance, auto-scaling)
- Monitoring: Prometheus (production observability)

**Standard Library Sufficient** (simple use cases):

- HTTP: java.net.http (internal APIs, <100 req/sec)
- JSON: javax.json (<5 types, no polymorphism)
- Async: ExecutorService (CPU-bound tasks, <100 threads)
- Configuration: Properties files (single environment)

**Example progression** (JSON processing):

```markdown
## JSON Processing in Production

### Standard Library Approach (javax.json)

Java 11+ includes javax.json for basic JSON operations...

[Code example with javax.json]

**Limitations for production**:

- Manual binding to Java objects (verbose)
- Limited type safety (manual casting)
- No polymorphic deserialization
- Poor error messages

### Production Framework (Jackson)

Jackson addresses production JSON needs...

[Code example with Jackson annotations]

**Trade-offs**:

- Added dependency (2MB library)
- Learning curve (annotations, configuration)
- Justification: Worth it for complex domains with >10 types

### When to Use Each

- **javax.json**: Simple REST clients, <5 JSON types
- **Jackson**: Complex domains, polymorphic types, production APIs
```

**Validation**: Checkers verify standard library examples precede framework introductions.
