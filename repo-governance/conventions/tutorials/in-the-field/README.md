---
title: "In-the-Field Tutorial Convention"
description: "Standards for creating production-ready implementation guides building on by-example/by-concept foundations with frameworks, libraries, and enterprise patterns"
when_to_use: "Read this index to find the right In-the-Field Tutorial Convention child document."
---

# In-the-Field Tutorial Convention

- [Purpose](./01-purpose.md) — Why the In-the-Field tutorial type exists and its target
- [Structure Integration with General Tutorial Standards](./02-structure-integration-with-general-tutorial-standards.md) — How In-the-Field tutorials adapt the general tutorial structure, plus
- [Core Characteristics: Focus, Coverage, and Topic Count](./03-core-characteristics-focus-and-coverage.md) — The production-implementation focus, in-scope/out-of-scope coverage, and the 20-40 guide-count
- [Standard Library First Principle](./04-standard-library-first-principle.md) — The core standard-library-first principle, why it matters, the progression
- [Standard Library First Principle: Topic Progression Table (Continued)](./05-standard-library-first-principle-table-continued.md) — The second half of the standard-library-to-framework topic progression table
- [Standard Library First Principle: Key Patterns and Example](./06-standard-library-first-principle-key-patterns.md) — Which topics always need a framework versus when the
- [Guide Structure Overview](./07-guide-structure-overview-and-part1.md) — The six-part recommended guide structure and the requirements for
- [Guide Structure Part 2: Standard Library First — Testing Example](./08-guide-structure-part2-testing-example.md) — Part 2 requirements plus the worked standard-library testing example
- [Guide Structure Part 2: Standard Library First — HTTP Client Example](./09-guide-structure-part2-http-example.md) — The worked standard-library HTTP client example (java.net.http.HttpClient) and its
- [Guide Structure Part 2: Standard Library First — Database Example Setup](./10-guide-structure-part2-database-example-setup.md) — The worked standard-library JDBC database persistence example.
- [Guide Structure Part 2: Database Example Limitations](./11-guide-structure-part2-database-example-limitations.md) — The production limitations of the standard-library JDBC approach shown
- [Guide Structure Part 3: Introduction and Testing Framework Setup](./12-guide-structure-part3-intro-and-testing-setup.md) — Part 3 requirements for introducing a production framework, plus
- [Guide Structure Part 3: JUnit 5 Test Class Example](./13-guide-structure-part3-junit-test-class.md) — The worked production JUnit 5 test class example with
- [Guide Structure Part 3: Running Tests and JUnit 5 Benefits](./14-guide-structure-part3-running-tests-and-junit-benefits.md) — How to run JUnit 5 tests via Maven and
- [Guide Structure Part 3: OkHttp Client Setup](./15-guide-structure-part3-okhttp-client-setup.md) — The worked OkHttp production HTTP client example - imports,
- [Guide Structure Part 3: OkHttp GET Method and Benefits](./16-guide-structure-part3-okhttp-get-method-and-benefits.md) — The OkHttp client's get() method implementation and the rationale
- [Guide Structure Part 3: JPA Entity Example](./17-guide-structure-part3-jpa-entity-example.md) — The worked JPA/Hibernate @Entity class example mapping a User
- [Guide Structure Part 3: JPA Service Example](./18-guide-structure-part3-jpa-service-example.md) — The worked JPA/Hibernate @Service class example showing EntityManager-based find,
- [Guide Structure Part 3: JPA/Hibernate Benefits](./19-guide-structure-part3-jpa-service-benefits.md) — Why JPA/Hibernate is chosen over raw JDBC for production
- [Guide Structure Part 4: Diagram Guidance and Authentication Flow](./20-guide-structure-part4-diagram-guidance-and-auth-flow.md) — When to include Mermaid diagrams in a guide, plus
- [Guide Structure Part 4: OAuth and Database Flow Diagrams](./21-guide-structure-part4-oauth-and-database-flow.md) — Mermaid diagrams for OAuth2/OIDC authentication and the JDBC-to-HikariCP-to-JPA database
- [Guide Structure Part 4: Containerization and CI/CD Flow Diagrams](./22-guide-structure-part4-containerization-and-cicd-flow.md) — Mermaid diagrams for JAR/Docker/Kubernetes containerization progression and a full
- [Guide Structure Part 4: Messaging Flow Diagrams](./23-guide-structure-part4-messaging-flow.md) — Mermaid diagrams for point-to-point JMS messaging and Kafka pub/sub
- [Guide Structure Part 5-6: Production Patterns and Trade-offs](./24-guide-structure-part5-part6-patterns-and-tradeoffs.md) — Requirements for documenting enterprise patterns, test organization/naming/security considerations, and
- [Anti-Patterns: Testing Framework Without Foundation](./25-anti-patterns-testing.md) — Why the Anti-Patterns section exists, plus the consequences of
- [Anti-Pattern: ORM Without SQL Knowledge](./26-anti-patterns-database.md) — The production consequences (N+1 queries, connection pool exhaustion) of
- [Anti-Pattern: REST Framework Without HTTP Fundamentals](./27-anti-patterns-http.md) — The production consequences (wrong status codes, security holes) of
- [Anti-Pattern: Async Frameworks Without Threading Knowledge](./28-anti-patterns-async.md) — The production consequences (CPU thrashing, deadlocks) of using async
- [Anti-Pattern: Dependency Injection Frameworks Without Manual Wiring](./29-anti-patterns-dependency-injection.md) — The production consequences (circular dependencies, lifecycle confusion) of using
- [Anti-Patterns Summary: Standard Library First Prevents Production Disasters](./30-anti-patterns-summary.md) — The consolidated summary of why standard-library-first prevents the five
- [Production Code Quality Standards](./31-production-code-quality-standards.md) — Code completeness requirements and the 1.0-2.25 annotation-density target for
- [Framework and Library Usage](./32-framework-and-library-usage.md) — Which external dependencies are encouraged, how to introduce a
- [Diagram Standards](./33-diagram-standards.md) — How often diagrams should appear per guide and the
- [File Naming and Organization](./34-file-naming-and-organization.md) — The directory structure, file naming pattern, and topic-weight numbering
- [Topic Weight Layers 1-5](./35-topic-weight-layers-1-5.md) — The topic-weight numbering ranges for the Foundation, Quality Foundation,
- [Topic Weight Layers 6-10](./36-topic-weight-layers-6-10.md) — The topic-weight numbering ranges for the Integration Patterns, Advanced
- [Topic Weight Progression, Customization, and Java Example](./37-topic-weight-progression-and-example.md) — The pedagogical rationale behind the ten-layer progression, how to
- [Frontmatter Requirements](./38-frontmatter-requirements.md) — The required frontmatter fields for In-the-Field guide pages.
- [Quality Checklist](./39-quality-checklist.md) — The full pre-publish checklist covering production readiness, standard-library-first, code
- [Validation and Enforcement](./40-validation-and-enforcement.md) — The automated checks and quality-gate workflow that validate In-the-Field
- [Relationship to Other Tutorial Types](./41-relationship-to-other-tutorial-types.md) — How In-the-Field differs from and builds on By-Example, By-Concept,
- [Cross-Language Consistency](./42-cross-language-consistency.md) — How the In-the-Field convention's structure and standards stay consistent
- [Production-Validated Standards Summary: Coverage](./43-production-validated-standards-summary-coverage.md) — The validated guide-count and topic-coverage targets, and the diagram-density
- [Production-Validated Standards Summary: Quality and Anti-Pattern Coverage](./44-production-validated-standards-summary-quality.md) — The validated annotation-density, standard-library-first, code-quality, and anti-pattern-coverage standards with
- [Principles Implemented/Respected](./45-principles-implemented-respected.md) — The content principles - progressive disclosure, no time estimates,
- [Scope](./46-scope.md) — What the In-the-Field convention covers and does not cover,
- [Related Resources](./47-related-resources.md) — Related documentation, agents, workflows, and skills for creating and
