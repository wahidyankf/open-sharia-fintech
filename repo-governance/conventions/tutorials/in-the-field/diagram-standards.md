---
description: How often diagrams should appear per guide and the color-blind-friendly palette they must use.
when_to_use: Use when deciding diagram frequency for a guide or picking diagram colors.
---

# Diagram Standards

## Diagram Frequency Target

**Guideline**: 10-20 diagrams total per in-the-field collection (25-50% of 20-40 guides)

**When to include diagrams**:

- Architecture patterns (microservices, event-driven, layered)
- Deployment topologies (Docker, Kubernetes, cloud)
- Data flow across systems (API → service → database)
- State machines (TDD Red-Green-Refactor, workflow states)
- Integration patterns (message queues, pub/sub, request/reply)
- Security flows (authentication, authorization, token validation)
- **Progression patterns** (standard library → framework → production)
- Database persistence patterns (JDBC → connection pools → ORMs)
- HTTP client evolution (basic → resilient → reactive)
- Containerization stages (JAR → Docker → Kubernetes)
- CI/CD pipeline flows (build → test → deploy → monitor)
- Messaging architecture (queue → pub/sub → partitioned streams)

**Enhanced convention examples** (reference diagrams in Part 4):

1. **TDD State Machine** - Red-Green-Refactor cycle visualization
2. **Authentication Flow Progression** - Basic Auth → JWT → OAuth2 OIDC
3. **Database Persistence Progression** - JDBC → HikariCP → JPA/Hibernate
4. **Containerization Progression** - JAR → Docker → Kubernetes
5. **CI/CD Pipeline Flow** - Complete build-test-deploy-monitor pipeline
6. **Messaging Patterns** - Point-to-point vs Pub/Sub vs Partitioned Kafka

**Current production state** (Java in-the-field):

- TDD guide: 1 diagram (Red-Green-Refactor state machine)
- Docker/Kubernetes guide: 3 diagrams (container architecture, K8s topology, scaling)
- Authentication guide: 2 diagrams (OAuth2 flow, JWT validation)
- **Enhanced with 6 comprehensive progression diagrams** showing standard library → framework → production evolution

**Rationale**: Production topics benefit from architecture and flow visualization. Each complex guide should have 1-2 diagrams. **Progression diagrams** are especially valuable for showing why frameworks solve problems that standard library approaches leave unaddressed.

## Color-Blind Friendly Palette

**Mandatory colors** (WCAG AA compliant):

- **Blue** #0173B2 - Primary elements, starting states
- **Orange** #DE8F05 - Secondary elements, processing states
- **Teal** #029E73 - Success states, outputs
- **Purple** #CC78BC - Alternative paths, options
- **Brown** #CA9161 - Neutral elements, helpers

**Forbidden colors**: Red, green, yellow (not color-blind accessible)
