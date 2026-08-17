---
title: Software Engineering
description: How open-sharia-enterprise approaches architecture, development, languages, frameworks, testing, and licensing
category: explanation
subcategory: software-engineering
tags:
  - software-engineering
  - architecture
  - development
  - testing
  - index
created: 2026-01-20
---

# Software Engineering

This section explains the engineering ideas used across open-sharia-enterprise. It is a good starting point for product people who want to understand how a product decision becomes software, and for early engineers who need a map before opening implementation-focused guidance.

You do not need to read everything in order. Start with the question you have, then follow the links when you need more detail.

## Start with your question

| If you want to understand…                                                               | Start here                                                                                                         |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| How the parts of a system fit together                                                   | [Architecture](./architecture/README.md)                                                                           |
| How business language and rules shape a system                                           | [Domain-Driven Design (DDD)](./architecture/domain-driven-design-ddd/README.md)                                    |
| How an application can keep its core logic independent from delivery and storage details | [Hexagonal Architecture](./architecture/hexagonal-architecture/README.md)                                          |
| How a record or workflow moves through defined stages                                    | [Finite State Machine (FSM)](./architecture/finite-state-machine-fsm/README.md)                                    |
| How teams turn examples and acceptance criteria into reliable code                       | [Software Development Practices](./development/README.md)                                                          |
| Which language or web framework a part of the platform uses                              | [Programming Languages](./programming-languages/README.md) or [Libraries and Frameworks](./platform-web/README.md) |
| How browser behavior is checked automatically                                            | [Automation Testing](./automation-testing/README.md)                                                               |
| Why a dependency's license was accepted or needs care                                    | [Licensing](./licensing/README.md)                                                                                 |

## The engineering map

### Architecture: shape the system around the problem

[Architecture](./architecture/README.md) covers the boundaries, responsibilities, and vocabulary that make a system easier to discuss and change. These approaches solve different parts of the same problem:

- [C4 Architecture Model](./architecture/c4-architecture-model/README.md) helps people see a system from its broad context down to implementation-level components.
- [Domain-Driven Design (DDD)](./architecture/domain-driven-design-ddd/README.md) helps product and engineering participants model a complex business domain using shared language, bounded contexts, aggregates, and events.
- [Hexagonal Architecture](./architecture/hexagonal-architecture/README.md) explains how ports and adapters protect business logic from infrastructure choices.
- [DDD + Hexagonal in Practice](./architecture/ddd-hexagonal-in-practice/README.md) connects the domain-modeling and structural approaches used in platform services.
- [Finite State Machine (FSM)](./architecture/finite-state-machine-fsm/README.md) explains explicit lifecycle states and valid transitions for entities and workflows.

For a product conversation, DDD and C4 are usually the most useful entry points: DDD helps establish what the business means, while C4 helps show where that work lives in the wider system.

### Development: make behavior clear and verifiable

[Software Development Practices](./development/README.md) covers two complementary ways to build confidence before implementation becomes large or hard to change:

- [Behavior-Driven Development (BDD)](./development/behavior-driven-development-bdd/README.md) uses concrete examples and Gherkin scenarios to keep product intent, acceptance criteria, and automated checks aligned.
- [Test-Driven Development (TDD)](./development/test-driven-development-tdd/README.md) uses the Red-Green-Refactor cycle to guide small, well-tested design steps.

BDD is especially useful when a feature needs a shared business conversation; TDD is especially useful when implementing and refining the underlying code. They can be used together.

### Languages and frameworks: work idiomatically in the chosen stack

The platform uses more than one language and framework because its web applications, services, and repository tooling have different needs. The guidance in these sections explains the conventions and trade-offs for each supported stack:

- [Programming Languages](./programming-languages/README.md) — Language-specific idioms, best practices, and antipatterns
- [Libraries and Frameworks](./platform-web/README.md) — Documentation on libraries and frameworks for building scalable applications

Use these pages after you know the relevant application or library. They explain how to apply a language or framework well here; they are not a substitute for choosing a product boundary or defining the feature's behavior.

### Quality and operational confidence

- [Automation Testing](./automation-testing/README.md) — Why and where automated checks build confidence in open-sharia-enterprise
- [Licensing](./licensing/README.md) — License analysis and compliance decisions for open-source dependencies used in open-sharia-enterprise

## How this material relates to the rest of the documentation

These pages are **explanation**: they provide context, vocabulary, and the reasoning behind approaches. When you need to perform a concrete task, look for a how-to guide; when you need a precise rule or interface, use reference documentation. The [Explanation index](../README.md) describes how this fits within the project's [Diátaxis documentation structure](../../../repo-governance/conventions/structure/diataxis-framework.md).

Many linked pages also record repository-specific standards. Their mandatory language applies when working in this repository; this index is the place to orient yourself before using those detailed standards.

## Related reading

- [Software Design Reference](./software-design-reference.md) — Cross-reference index for software design documentation.
- [Functional Programming](../../../repo-governance/development/pattern/functional-programming.md) — The project's preference for immutability and pure functions.
- [Repository Governance Architecture](../../../repo-governance/repository-governance-architecture.md) — How technical practices connect to the wider governance model.
