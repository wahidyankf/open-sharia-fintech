---
title: Hexagonal Architecture
description: Core hexagonal architecture pattern — ports, adapters, dependency rule, and app-type specializations
category: explanation
subcategory: development
tags:
  - architecture
  - hexagonal
  - ports-and-adapters
  - dependency-rule
created: 2026-05-26
when_to_use: "Use when structuring a backend or CLI app's layers, or deciding whether code belongs in domain, application, infrastructure, or an adapter."
---

# Hexagonal Architecture

Hexagonal architecture (also called Ports and Adapters) organizes code so that business logic never depends
on delivery mechanisms or infrastructure. The domain sits at the centre; everything else adapts to it. This
pattern applies across CLIs and backend services in this monorepo, with specializations per app type
documented in child pages below.

## Contents

- [Principles and Conventions](./hexagonal-architecture/principles-and-conventions.md) — The core principles and conventions this pattern implements - explicitness, pure functions, simplicity, and immutability. Use when you need to trace a hexagonal-architecture rule back to the principle or convention it implements.
- [Overview and Core Concepts](./hexagonal-architecture/overview-and-core-concepts.md) — The four concentric zones of hexagonal architecture, plus the core concepts of ports, inbound adapters, outbound adapters, and the domain model. Use when orienting to hexagonal architecture's zones and core vocabulary before applying it to a specific app.
- [Layer Definitions](./hexagonal-architecture/layer-definitions.md) — What belongs and what is forbidden in each hexagonal layer - domain, application, infrastructure, and inbound adapters. Use when deciding whether a piece of code belongs in the domain, application, infrastructure, or inbound-adapter layer.
- [Dependency Rule, App-Type Specializations, and Related](./hexagonal-architecture/dependency-rule-app-type-specializations-and-related.md) — The inward-only dependency rule diagram, links to per-app-type specializations, and related pattern documentation. Use when verifying the dependency-rule direction, or finding the CLI/backend specialization for a given app type.

Next.js **web apps** deliberately do **not** use hexagonal architecture; they use the simpler
[Functional Core / Imperative Shell — Web Apps](../pattern/functional-core-imperative-shell-web.md) pattern instead.
