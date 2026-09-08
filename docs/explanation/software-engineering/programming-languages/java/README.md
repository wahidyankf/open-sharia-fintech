---
title: Java
description: OSE Platform authoritative Java coding standards and framework stack (Java 25 LTS / Spring Boot 4)
category: explanation
subcategory: prog-lang
tags:
  - java
  - programming-languages
  - coding-standards
  - framework-stack
  - spring-boot
  - gradle
  - java-25
principles:
  - automation-over-manual
  - explicit-over-implicit
  - immutability
  - pure-functions
  - reproducibility
created: 2026-09-08
---

# Java

**This is THE authoritative reference** for Java coding standards in OSE Platform.

All Java code written for the OSE Platform MUST comply with the standards documented here. These standards are mandatory, not optional. Non-compliance blocks code review and merge approval.

## Scope: Active for the LMS Backend Only

Java is **not** the default language for new OSE Platform backends. F# remains the default; see the [languages README](../README.md) for the selection table.

Java is active for exactly one project — `ose-lms-be`, the Learning Management System backend — because the LMS targets an ecosystem where Spring Boot is the incumbent. Introducing a Java service elsewhere is a decision that needs its own record, not an appeal to this document.

## Prerequisite Knowledge

**REQUIRED**: You MUST understand Java fundamentals from the [AyoKoding Java Learning Path](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/programming-languages/java/_index.md) before using these standards.

- [Java By Example](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/programming-languages/java/by-example/) — annotated code examples
- [Java In the Field](../../../../../apps/ayokoding-www/content/en/learn/legacy/software-engineering/programming-languages/java/in-the-field/) — production patterns

**This document is OSE Platform-specific**, not a Java tutorial. We define HOW to apply Java in THIS codebase, not WHAT Java is.

**What this documentation does NOT cover**: Java syntax, language fundamentals, generic patterns, or framework tutorials (those are in ayokoding-www).

**See**: [Programming Language Documentation Separation Convention](../../../../../repo-governance/conventions/structure/programming-language-docs-separation.md)

## Framework Stack

OSE Platform Java applications MUST use the following stack:

**Language and Runtime**:

- **Java 25 (LTS)** — the current LTS at adoption. Non-LTS feature releases are not used.
- **Eclipse Temurin** — the distribution both local development and CI install.

**Web Framework**:

- **Spring Boot 4** — application framework, dependency injection, and the embedded HTTP server
- **Spring Boot Actuator** — operational endpoints, exposed narrowly (see below)

**Build**:

- **Gradle** with the Kotlin DSL (`build.gradle.kts`) — declarative, and the toolchain block pins the JDK independently of whatever JDK invoked the build
- **The Gradle wrapper**, committed with a pinned distribution checksum

**Testing**:

- **Cucumber-JVM** with `cucumber-spring` and `cucumber-junit-platform-engine` — the Unit adapter that binds this repository's Gherkin corpus
- **MockMvc** — in-process HTTP assertions without binding a port
- **JaCoCo** — line-coverage verification, enforced in the build rather than reported for information

**Quality Tools**:

- **Spotless** with **google-java-format** — the formatter (MANDATORY — zero negotiation)

Exact pinned versions live in each project's `build.gradle.kts`, not here; a version repeated in prose is a version that will drift.

## Software Engineering Principles

Java code in this repository is measured against the [Principles Index](../../../../../repo-governance/principles/README.md). Four apply with particular force:

- **[Explicit over implicit](../../../../../repo-governance/principles/software-engineering/explicit-over-implicit.md)** — Spring's autoconfiguration is convenient and invisible. Where a behaviour matters, declare it: exposure lists, ports, and content types are configuration, not defaults inherited by accident.
- **[Immutability](../../../../../repo-governance/principles/software-engineering/immutability.md)** — prefer `record` types and `final` fields. Java will not stop you from mutating; the standard does.
- **[Pure functions](../../../../../repo-governance/principles/software-engineering/pure-functions.md)** — logic worth testing is logic worth extracting from the framework. See `PortResolver` in `ose-lms-be`: a pure resolver with no Spring dependency, testable without a context.
- **[Reproducibility](../../../../../repo-governance/principles/software-engineering/reproducibility.md)** — the Gradle wrapper, the pinned distribution checksum, and the toolchain block exist so that a build on a laptop and a build in CI resolve the same JDK and the same dependencies.

## Documentation Structure

- [Java Coding Standards](./coding-standards.md) — Authoritative OSE Platform Java coding standards: naming, package layout, records, controllers, and configuration. Read this when writing or reviewing any Java source file in this repository.
- [Java Testing Standards](./testing-standards.md) — Authoritative OSE Platform Java testing standards: the Cucumber Unit adapter, MockMvc boundaries, and JaCoCo coverage enforcement. Read this when binding a scenario, choosing a test boundary, or changing a coverage floor.
- [Java Error Handling Standards](./error-handling-standards.md) — Authoritative OSE Platform Java error-handling standards: exception boundaries, fail-fast startup, response shape, and what is never returned to a client. Read this when adding a failure path or shaping an error response.

This is a deliberately small set. The `c-sharp/` and `typescript/` guides are much larger because they document patterns that exist in this repository's C# and TypeScript code. Java standards are written against Java code that exists; concurrency, DDD, and performance guides arrive with the code they would describe, not before it.

## Related Documentation

- [Programming Languages Overview](../README.md) — language selection and platform guidance
- [Behaviour-Driven Development](../../../../../repo-governance/development/behaviour-driven-development.md) — the adapter contract Java projects satisfy
- [Nx Target Standards](../../../../../repo-governance/development/infra/nx-targets.md) — the target names every project exposes
