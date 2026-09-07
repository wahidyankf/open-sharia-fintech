---
title: "Hexagonal Architecture + DDD — Backend Apps"
description: "Hexagonal architecture with DDD bounded contexts for backend apps — F#/Giraffe directory layouts, language-specific idioms, and inter-context isolation rules"
when_to_use: "Read this index to find the right Hexagonal Architecture + DDD — Backend Apps child document."
---

# Hexagonal Architecture + DDD — Backend Apps

- [Overview and Directory Layout](./overview-and-directory-layout.md) — How bounded contexts and the api/ transport directory relate, plus the canonical F#/Giraffe directory layout. Use when scaffolding a new bounded context and need the canonical directory layout.
- [F#-Specific](./fsharp-specific.md) — F#-specific idioms for outbound ports, dependency injection, and mapping domain errors to HTTP responses at the API boundary. Use when implementing an F# outbound port interface, wiring DI in Program.fs, or mapping a domain error to an HTTP response.
- [DDD Integration, Forbidden Imports, and Related](./ddd-integration-forbidden-imports-and-related.md) — Bounded-context isolation rules, shared infrastructure placement, anti-corruption layers, the forbidden-imports table, and related pattern documentation. Use when two bounded contexts need to communicate, or checking whether a layer imports something it should not.
