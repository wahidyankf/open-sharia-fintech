---
title: "Framework and Library Usage"
description: Which external dependencies are encouraged, how to introduce a framework, and how to declare dependencies in examples.
when_to_use: Use when introducing a new framework or dependency in a guide.
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

# Framework and Library Usage

## External Dependencies Encouraged

**Unlike by-example/by-concept**: In-the-field explicitly ENCOURAGES framework and library usage.

**Permitted frameworks/libraries**:

- Testing: JUnit 5, Mockito, AssertJ, Cucumber
- Build: Maven, Gradle
- Dependency Injection: Spring Framework, Guice
- Web: Spring Boot, JAX-RS, Vert.x
- Persistence: JPA/Hibernate, Spring Data, jOOQ
- Messaging: Spring JMS, Kafka clients, RabbitMQ
- Caching: Caffeine, Redis clients, Spring Cache
- Security: Spring Security, OWASP libraries
- Monitoring: Micrometer, OpenTelemetry
- Any production-grade library with clear value proposition

## Framework Introduction Requirements

When introducing a framework:

- PASS: **Standard library first**: Show built-in approach before framework
- PASS: **Problem identification**: Explain limitations standard library doesn't address
- PASS: **Justification**: Why this specific framework (not just "industry standard")
- PASS: **Installation steps**: Dependency declaration and version
- PASS: **Configuration**: How to configure for production use
- PASS: **Trade-offs**: Complexity vs capability, when simpler approaches suffice

## Dependency Declaration Standards

**Maven example**:

```xml
<dependency>
    <groupId>com.fasterxml.jackson.core</groupId>
    <artifactId>jackson-databind</artifactId>
    <version>2.16.1</version>  <!-- Use specific version, not LATEST -->
</dependency>
```

**Gradle example**:

```kotlin
implementation("com.fasterxml.jackson.core:jackson-databind:2.16.1")
```

**Requirements**:

- Specific version numbers (never LATEST or ranges)
- Justification in surrounding text
- Link to framework documentation
