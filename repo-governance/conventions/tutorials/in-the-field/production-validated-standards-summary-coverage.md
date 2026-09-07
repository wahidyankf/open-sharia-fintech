---
description: The validated guide-count and topic-coverage targets, and the diagram-density standard with its six progression diagram types.
when_to_use: Use when checking a guide set's coverage or diagram density against validated production standards.
---

# Production-Validated Standards Summary: Coverage

This convention reflects standards validated by production in-the-field content on ayokoding-www, enhanced with comprehensive examples matching swe-by-example.md quality standards:

**Guide Count**: 20-40 production guides (currently 31 for Java)

**Topic Coverage**:

- Development practices (TDD, BDD, design principles, best practices, anti-patterns)
- Build and deployment (build tools, CI/CD, Docker/Kubernetes, cloud-native patterns)
- Security (authentication, security practices, type safety)
- Data persistence (SQL databases, NoSQL databases)
- Integration (messaging, caching, web services, JSON/API integration)
- Patterns (DDD, dependency injection, reactive programming, finite state machines, functional programming, resilience patterns)
- Quality (performance, logging, linting/formatting)
- Application types (CLI apps)

**Diagram Density**: 10-20 total diagrams (25-50% of guides)

- **Enhanced convention includes 6 comprehensive progression diagrams**:
  1. TDD State Machine (Red-Green-Refactor)
  2. Authentication Flow Progression (Basic Auth → JWT → OAuth2)
  3. Database Persistence Progression (JDBC → HikariCP → JPA/Hibernate)
  4. Containerization Progression (JAR → Docker → Kubernetes)
  5. CI/CD Pipeline Flow (complete build-test-deploy-monitor)
  6. Messaging Patterns (Point-to-point → Pub/Sub → Kafka Partitions)
- Complex patterns: 2-3 diagrams (Docker/K8s, authentication, messaging, database)
- Simple patterns: 0-1 diagram (logging, configuration, linting)
- **Production diagrams now comprehensive**: All major topics have progression visualizations
