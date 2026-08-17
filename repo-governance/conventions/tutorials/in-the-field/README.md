---
title: "In-the-Field Tutorial Convention"
description: "Standards for creating production-ready implementation guides building on by-example/by-concept foundations with frameworks, libraries, and enterprise patterns"
when_to_use: "Read this index to find the right In-the-Field Tutorial Convention child document."
---

# In-the-Field Tutorial Convention

- [Purpose](./01-purpose.md) — You need the rationale and target audience for In-the-Field tutorials.
- [Structure Integration with General Tutorial Standards](./02-structure-integration-with-general-tutorial-standards.md) — Structuring a new In-the-Field guide or verifying it inherits the right general-tutorial requirements.
- [Core Characteristics](./03-core-characteristics-focus-and-coverage.md) — The production-implementation focus, in-scope/out-of-scope coverage, and the 20-40 guide-count target for In-the-Field content.
- [Standard Library First Principle](./04-standard-library-first-principle.md) — You need the rationale for teaching standard-library approaches before frameworks, or the topic progression table.
- [Standard Library First Principle](./05-standard-library-first-principle-table-continued.md) — The second half of the standard-library-to-framework topic progression table (Web Framework through Service Discovery).
- [Standard Library First Principle](./06-standard-library-first-principle-key-patterns.md) — Deciding whether a specific topic justifies introducing a production framework.
- [Guide Structure Overview](./07-guide-structure-overview-and-part1.md) — The six-part recommended guide structure and the requirements for Part 1, which establishes production relevance.
- [Testing Example](./08-guide-structure-part2-testing-example.md) — Writing the standard-library testing example for a Part 2 section.
- [HTTP Client Example](./09-guide-structure-part2-http-example.md) — Writing the standard-library HTTP client example for a Part 2 section.
- [Database Example Setup](./10-guide-structure-part2-database-example-setup.md) — The worked standard-library JDBC database persistence example.
- [Guide Structure Part 2](./11-guide-structure-part2-database-example-limitations.md) — Documenting why the JDBC standard-library approach is insufficient for production.
- [Guide Structure Part 3](./12-guide-structure-part3-intro-and-testing-setup.md) — Part 3 requirements for introducing a production framework, plus the JUnit 5 dependency setup.
- [Guide Structure Part 3](./13-guide-structure-part3-junit-test-class.md) — Writing a JUnit 5 production test class example.
- [Guide Structure Part 3](./14-guide-structure-part3-running-tests-and-junit-benefits.md) — Documenting how to run tests or justifying JUnit 5 over the standard library.
- [Guide Structure Part 3](./15-guide-structure-part3-okhttp-client-setup.md) — Writing the setup/configuration half of an OkHttp production example.
- [Guide Structure Part 3](./16-guide-structure-part3-okhttp-get-method-and-benefits.md) — Writing the request/response half of an OkHttp example or justifying OkHttp's use.
- [Guide Structure Part 3](./17-guide-structure-part3-jpa-entity-example.md) — The worked JPA/Hibernate @Entity class example mapping a User to a database table.
- [Guide Structure Part 3](./18-guide-structure-part3-jpa-service-example.md) — The worked JPA/Hibernate @Service class example showing EntityManager-based find, save, and update operations.
- [Guide Structure Part 3](./19-guide-structure-part3-jpa-service-benefits.md) — Justifying JPA/Hibernate's use over standard-library JDBC.
- [Guide Structure Part 4](./20-guide-structure-part4-diagram-guidance-and-auth-flow.md) — Deciding whether a guide needs a diagram, or building a TDD/authentication-flow diagram.
- [Guide Structure Part 4](./21-guide-structure-part4-oauth-and-database-flow.md) — Building an OAuth2 authentication or database-persistence-progression diagram.
- [Guide Structure Part 4](./22-guide-structure-part4-containerization-and-cicd-flow.md) — Building a containerization-progression or CI/CD-pipeline diagram.
- [Guide Structure Part 4](./23-guide-structure-part4-messaging-flow.md) — Mermaid diagrams for point-to-point JMS messaging and Kafka pub/sub progression with partitioning.
- [Guide Structure Part 5-6](./24-guide-structure-part5-part6-patterns-and-tradeoffs.md) — Writing the best-practices or trade-offs sections of a guide.
- [Anti-Patterns: Testing Framework Without Foundation](./25-anti-patterns-testing.md) — Explaining the risk of teaching a testing framework before its standard-library basis.
- [Anti-Pattern: ORM Without SQL Knowledge](./26-anti-patterns-database.md) — Explaining the risk of teaching an ORM before SQL/JDBC fundamentals.
- [Anti-Pattern: REST Framework Without HTTP Fundamentals](./27-anti-patterns-http.md) — Explaining the risk of teaching a REST framework before HTTP basics.
- [Anti-Pattern: Async Frameworks Without Threading Knowledge](./28-anti-patterns-async.md) — Explaining the risk of teaching async frameworks before threading basics.
- [Anti-Pattern: Dependency Injection Frameworks Without Manual Wiring](./29-anti-patterns-dependency-injection.md) — Explaining the risk of teaching a DI framework before manual dependency wiring.
- [Anti-Patterns Summary](./30-anti-patterns-summary.md) — You need the closing summary argument for the standard-library-first principle.
- [Production Code Quality Standards](./31-production-code-quality-standards.md) — Checking whether a guide's code examples meet production completeness and annotation-density standards.
- [Framework and Library Usage](./32-framework-and-library-usage.md) — Introducing a new framework or dependency in a guide.
- [Diagram Standards](./33-diagram-standards.md) — Deciding diagram frequency for a guide or picking diagram colors.
- [File Naming and Organization](./34-file-naming-and-organization.md) — Creating or naming a new In-the-Field guide file and assigning it a topic weight.
- [Topic Weight Layers 1-5](./35-topic-weight-layers-1-5.md) — Assigning a topic weight to a guide in the Foundation-through-Data-Management range.
- [Topic Weight Layers 6-10](./36-topic-weight-layers-6-10.md) — Assigning a topic weight to a guide in the Integration-Patterns-through-Meta-Topics range.
- [Topic Weight Progression, Customization, and Java Example](./37-topic-weight-progression-and-example.md) — Adapting the topic-weight scheme to a new language or reviewing a complete worked example.
- [Frontmatter Requirements](./38-frontmatter-requirements.md) — Writing frontmatter for a new In-the-Field guide page.
- [Quality Checklist](./39-quality-checklist.md) — A final checklist before publishing an In-the-Field guide.
- [Validation and Enforcement](./40-validation-and-enforcement.md) — The automated checks and quality-gate workflow that validate In-the-Field guides.
- [Relationship to Other Tutorial Types](./41-relationship-to-other-tutorial-types.md) — Deciding whether content belongs in In-the-Field versus another tutorial type.
- [Cross-Language Consistency](./42-cross-language-consistency.md) — Applying the In-the-Field convention to a new programming language.
- [Production-Validated Standards Summary](./43-production-validated-standards-summary-coverage.md) — Checking a guide set's coverage or diagram density against validated production standards.
- [Production-Validated Standards Summary](./44-production-validated-standards-summary-quality.md) — The validated annotation-density, standard-library-first, code-quality, and anti-pattern-coverage standards with quality enhancement history.
- [Principles Implemented/Respected](./45-principles-implemented-respected.md) — You need the rationale for why the In-the-Field convention is designed the way it is.
- [Scope](./46-scope.md) — You need to confirm whether a question about production guides falls inside this convention's scope.
- [Related Resources](./47-related-resources.md) — Related documentation, agents, workflows, and skills for creating and validating In-the-Field content.
