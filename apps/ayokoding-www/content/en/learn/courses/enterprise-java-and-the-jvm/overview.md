---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

This course assumes [Just Enough Java](../just-enough-java/overview.md) and
[Software Architecture](../software-architecture/overview.md). It teaches the enterprise Java
working set: explicit constructor injection, Spring Boot conventions, layered HTTP/persistence
services, validation and observability, then the JVM runtime behaviors a production service exposes.

## Scope boundary

This is Spring Boot and JVM-operating literacy, not a replacement for architecture design or a
catalog of every Spring module. It avoids framework magic where an explicit constructor, boundary,
or operational signal is clearer. Cold-start-sensitive programs and small scripts are often better
served by a lighter approach.

## Verified sources

Spring Boot 4.1.0 requires Java 17 or newer and documents Maven build support and starter
dependencies; this course uses its current documented starter names rather than a copied legacy
template. [System requirements](https://docs.spring.io/spring-boot/system-requirements.html)
and [build systems](https://docs.spring.io/spring-boot/reference/using/build-systems.html) support
that statement. Spring's [MockitoBean documentation](https://docs.spring.io/spring-framework/reference/testing/annotations/integration-spring/annotation-mockitobean.html)
documents context bean overrides used by slice tests.

The accompanying capstone is original course material and keeps version-sensitive runtime claims
behind official documentation links.
