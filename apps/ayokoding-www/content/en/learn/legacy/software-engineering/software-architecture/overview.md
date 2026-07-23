---
title: "Overview"
date: 2026-01-30T00:00:00+07:00
draft: false
weight: 10000000
---

Architecture patterns and methodologies provide structured approaches to designing complex software systems. This section covers fundamental architectural frameworks that help organize system components, manage complexity, and communicate design decisions effectively.

## 🧭 Software Architecture vs. System Design

This section is about **software architecture** — the structure **inside a single application** (or service). Patterns here organize classes, modules, layers, and code-level concerns: SOLID, layered architecture, hexagonal/clean architecture, DDD building blocks, GoF design patterns, FSMs.

The sibling [**System Design**](/en/learn/software-engineering/system-design) section covers a different layer: **how multiple services, databases, caches, and queues interact across machines and regions** — load balancing, sharding, CAP theorem, sagas, microservices, multi-region deployments.

Both disciplines complement each other. An e-commerce monolith primarily needs software architecture; a multi-region payment platform needs both. Use this section for in-app structure; cross to System Design when the scope expands beyond one service.

## 🎯 What You'll Learn

This section explores proven architectural methodologies used in modern software engineering:

- **By Example** (umbrella): 93 heavily annotated examples — 85 canonical + 5 FP-native extras (#86–90: ROP, Free Monads / Tagless Final, Reader, Kleisli, State) + 3 OOP-native extras (#91–93: Active Record, GRASP, Singleton-with-FP-counterexample). Available in three paradigm tracks with explicit paradigm-fit framing (Norvig/Seemann/Wlaschin/Hickey/Evans/Fowler/Pike citations):
  - **OOP** — Java, Kotlin, C#, TypeScript (inheritance-bearing class hierarchies)
  - **FP** — F#, Clojure, TypeScript, Haskell (ADTs, HOFs, Railway-Oriented Programming) — Rust also appears where the FP idiom translates one-to-one
  - **Procedural** (new) — Go (canonical), Rust, C (sidebar) — composition + structural typing + explicit data flow, without inheritance hierarchies. Authority: Pike ([Go at Google](https://go.dev/talks/2012/splash.article), 2012); Boyle ([_Domain-Driven Design with Golang_](https://www.oreilly.com/library/view/domain-driven-design-with/9781804613450/), 2022); Hoverbear ([Pretty State Machine Patterns in Rust](https://hoverbear.org/blog/rust-state-machine-pattern/)); Samek ([_Practical UML Statecharts in C/C++_](https://www.routledge.com/Practical-UML-Statecharts-in-CC-Event-Driven-Programming-for-Embedded-Systems/Samek/p/book/9780750687065))
- **C4 Model**: Hierarchical approach to visualizing software architecture at multiple levels of abstraction (Context, Containers, Components, Code)
- **Domain-Driven Design (DDD)**: Strategic and tactical patterns for modeling complex business domains and organizing code around business concepts
- **Hexagonal Architecture**: Ports-and-adapters approach that isolates the domain core from external concerns (databases, frameworks, UIs)
- **Finite State Machine (FSM)**: Mathematical model for designing systems with discrete states and well-defined transitions
- **Cases**: Production wiring tutorials that compose C4, DDD, Hexagonal Architecture, and FSM in real-world code (In FP and In OOP cases)

## 📐 Why Architecture Patterns Matter

Good architecture provides:

- **Clarity**: Clear structure makes systems easier to understand and maintain
- **Communication**: Shared vocabulary for discussing design decisions with teams
- **Scalability**: Proven patterns that support system growth and evolution
- **Quality**: Built-in best practices reduce bugs and technical debt
- **Flexibility**: Modular design enables easier changes and feature additions

## 🏗️ When to Use Each Pattern

**C4 Model**:

- Documenting system architecture for stakeholders at different technical levels
- Creating visual diagrams that balance detail with comprehension
- Onboarding new team members to existing systems

**Domain-Driven Design**:

- Complex business domains with rich behavior and business rules
- Large systems requiring clear boundaries and modular organization
- Teams needing shared language between developers and domain experts

**Finite State Machine**:

- Systems with clearly defined states (order processing, authentication flows, game logic)
- Workflow management and business process automation
- Protocol implementations and parsing

## 🌐 Architecture-First, Technology-Second

These patterns are **technology-agnostic**:

- Apply to any programming language (Java, Go, Python, TypeScript, etc.)
- Work with any framework or technology stack
- Focus on structural organization, not implementation details
- Principles remain constant as technologies evolve

## 📚 What's Included

Each architecture pattern section covers:

1. **Core Concepts**: Fundamental principles and terminology
2. **When to Use**: Scenarios where the pattern excels
3. **Key Components**: Main building blocks and their relationships
4. **Best Practices**: Proven approaches for successful implementation
5. **Common Pitfalls**: Mistakes to avoid and how to address them
6. **Real-World Examples**: Practical applications in production systems

## 🔗 Related Content

- [**System Design Cases**](/en/learn/software-engineering/system-design/by-example/cases) - See these patterns applied in real-world system designs

## Production Wiring

After the by-example tutorials for C4, DDD, Hexagonal Architecture, and FSM, the production cases show how the four families compose in real production code:

- Next step (production wiring): [In FP — F# / Giraffe / Npgsql, Clojure / Ring / next.jdbc, TypeScript / Hono / node-postgres, Haskell / Servant / postgresql-simple](/en/learn/software-engineering/software-architecture/by-example/cases/in-fp)
- Next step (production wiring): [In OOP — Java / Spring Boot 4, Kotlin / Spring Boot 4, C# / ASP.NET Core, TypeScript / NestJS](/en/learn/software-engineering/software-architecture/by-example/cases/in-oop)
- Next step (production wiring): [In Procedural — Go / chi / database/sql, Rust / axum / sqlx](/en/learn/software-engineering/software-architecture/by-example/cases/in-procedural)

## 🚀 Getting Started

Start with the pattern that best matches your current needs:

- **New to architecture?** Begin with **C4 Model** for visualization fundamentals
- **Complex business domain?** Explore **Domain-Driven Design** for domain modeling
- **State-driven systems?** Study **Finite State Machine** for state management

Each pattern complements the others - they're tools in your architectural toolkit, not mutually exclusive choices.
