---
title: Hexagonal Architecture + DDD — Backend Apps
description: Hexagonal architecture with DDD bounded contexts for backend apps — F#/Giraffe directory layouts, language-specific idioms, and inter-context isolation rules
category: explanation
subcategory: development
tags:
  - architecture
  - hexagonal
  - ddd
  - fsharp
  - backend
created: 2026-05-26
when_to_use: "Use when structuring a backend bounded context, wiring F# dependency injection, or mapping a domain error to an HTTP response."
---

# Hexagonal Architecture + DDD — Backend Apps

Backend apps combine hexagonal architecture with Domain-Driven Design (DDD) bounded contexts. Each bounded
context lives under `contexts/<name>/` and owns its hexagonal layers independently. DDD applies **only** to
backend apps (`organiclever-be`, `ose-be`). Next.js web apps do not use hexagonal/DDD at all — see
[Functional Core / Imperative Shell — Web Apps](../pattern/functional-core-imperative-shell-web.md).

## Contents

- [Principles and Conventions](./hexagonal-architecture-be/principles-and-conventions.md) — The core principles and conventions this pattern implements - explicitness, pure functions, simplicity, immutability, and OpenAPI contract-first. Use when you need to trace a backend hexagonal/DDD rule back to the principle or convention it implements.
- [Overview and Directory Layout](./hexagonal-architecture-be/overview-and-directory-layout.md) — How bounded contexts and the api/ transport directory relate, plus the canonical F#/Giraffe directory layout. Use when scaffolding a new bounded context and need the canonical directory layout.
- [F#-Specific](./hexagonal-architecture-be/fsharp-specific.md) — F#-specific idioms for outbound ports, dependency injection, and mapping domain errors to HTTP responses at the API boundary. Use when implementing an F# outbound port interface, wiring DI in Program.fs, or mapping a domain error to an HTTP response.
- [DDD Integration, Forbidden Imports, and Related](./hexagonal-architecture-be/ddd-integration-forbidden-imports-and-related.md) — Bounded-context isolation rules, shared infrastructure placement, anti-corruption layers, the forbidden-imports table, and related pattern documentation. Use when two bounded contexts need to communicate, or checking whether a layer imports something it should not.
