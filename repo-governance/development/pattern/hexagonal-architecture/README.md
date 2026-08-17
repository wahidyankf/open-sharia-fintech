---
title: "Hexagonal Architecture"
description: "Core hexagonal architecture pattern — ports, adapters, dependency rule, and app-type specializations"
when_to_use: "Read this index to find the right Hexagonal Architecture child document."
---

# Hexagonal Architecture

- [Principles and Conventions](./01-principles-and-conventions.md) — The core principles and conventions this pattern implements - explicitness, pure functions, simplicity, and immutability. Use when you need to trace a hexagonal-architecture rule back to the principle or convention it implements.
- [Overview and Core Concepts](./02-overview-and-core-concepts.md) — The four concentric zones of hexagonal architecture, plus the core concepts of ports, inbound adapters, outbound adapters, and the domain model. Use when orienting to hexagonal architecture's zones and core vocabulary before applying it to a specific app.
- [Layer Definitions](./03-layer-definitions.md) — What belongs and what is forbidden in each hexagonal layer - domain, application, infrastructure, and inbound adapters. Use when deciding whether a piece of code belongs in the domain, application, infrastructure, or inbound-adapter layer.
- [Dependency Rule, App-Type Specializations, and Related](./04-dependency-rule-app-type-specializations-and-related.md) — The inward-only dependency rule diagram, links to per-app-type specializations, and related pattern documentation. Use when verifying the dependency-rule direction, or finding the CLI/backend specialization for a given app type.
