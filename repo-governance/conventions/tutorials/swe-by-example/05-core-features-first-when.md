---
title: "Core Features First: When to Introduce Dependencies"
description: "Defines the permitted exceptions for introducing external dependencies/abstractions and how to mark and justify them when they appear."
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - education
  - code-first
created: 2025-12-25
when_to_use: "Read when deciding at which coverage level (beginner/intermediate/advanced) an external dependency is finally permitted and how to introduce it."
---

# Core Features First: When to Introduce Dependencies

## When to Introduce External Dependencies/Abstractions

**Permitted exceptions** - Introduce external dependencies/abstractions only when:

1. **Critical production pattern cannot be demonstrated with core features**:
   - **Languages**: Web frameworks (Spring Boot, FastAPI) for teaching REST API architecture, ORMs (Hibernate, SQLAlchemy) for database persistence patterns
   - **React**: Complex async state management (React Query) for server caching patterns
   - **Spring**: Spring Boot for microservices deployment patterns (after understanding Core DI)
   - **Node.js**: Express for middleware architecture (after understanding http.createServer)

2. **The external tool is industry-standard and unavoidable**:
   - **Languages**: JUnit for Java testing (after teaching assertion basics), pytest for Python testing (after teaching unittest)
   - **React**: React Router for multi-page apps (after understanding component navigation)
   - **Vue**: Pinia for complex state (after understanding reactive primitives)

3. **Core features lack essential capability**:
   - **Languages**: Async HTTP in languages without built-in async HTTP client, advanced parsing where standard library is insufficient
   - **Frameworks**: Features genuinely missing from framework primitives

**When introducing external dependencies/abstractions**:

- **Mark it explicitly**: "Note: This example uses external library X (requires installation)" OR "Note: This uses abstraction Y built on primitive Z"
- **Explain why core features insufficient**: "While React's `useState` handles local state, Redux provides global state needed for..." OR "While `java.net.http` handles basic HTTP, Spring WebClient provides reactive streaming needed for..."
- **Show installation/setup step**: Include dependency declaration and installation command
- **Reference primitive foundation**: "This builds on `useState` (Example 10) by adding global state management"
- **Prefer intermediate/advanced sections**: Keep beginner content focused on core features
