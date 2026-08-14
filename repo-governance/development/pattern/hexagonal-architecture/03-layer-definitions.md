---
title: "Layer Definitions"
description: "What belongs and what is forbidden in each hexagonal layer - domain, application, infrastructure, and inbound adapters."
category: explanation
subcategory: development
tags:
  - architecture
  - hexagonal
  - ports-and-adapters
  - dependency-rule
created: 2026-05-26
when_to_use: "Use when deciding whether a piece of code belongs in the domain, application, infrastructure, or inbound-adapter layer."
---

# Layer Definitions

## Domain Layer

**Belongs here:**

- Business entities and aggregate roots
- Value objects (immutable, equality by value)
- Domain events
- Pure domain logic and invariants
- Domain error types (no HTTP status codes — those belong in the API adapter)

**Forbidden:**

- Framework imports (Axum, Next.js, Clap, Tokio I/O)
- Database imports (SQLx, Diesel, Entity Framework, Dapper)
- HTTP client imports
- Logging frameworks (use return values or domain events instead)
- Network protocol types

## Application Layer

**Belongs here:**

- Use-case / service orchestration functions
- Inbound port definitions (service interfaces that adapters call)
- Outbound port definitions (repository and external-service interfaces)
- Application-level error types
- DTOs or command/query objects that cross the application boundary
- In web apps: `application/index.ts` barrel — the sole public API surface per context

**Forbidden:**

- Direct database driver calls
- HTTP framework types (request/response objects)
- Direct filesystem access
- Concrete infrastructure implementations

## Infrastructure Layer (Outbound Adapters)

**Belongs here:**

- Concrete outbound adapter implementations (repository, cache, external HTTP)
- Database connection setup
- ORM/query-builder configuration
- External service SDK wrappers

**Forbidden:**

- Business logic (move invariants to domain)
- Inbound adapter code (route handlers, CLI argument parsing)
- Domain entity instantiation that bypasses invariants

## Inbound Adapter Layer

**Belongs here:**

- HTTP route handlers and middleware
- CLI command handlers and argument parsing
- GraphQL resolvers
- Message queue consumers
- Schema validation at the boundary (before passing to application)
- Error-to-response mapping (translates domain errors to HTTP status codes or CLI exit codes)

**Forbidden:**

- Business logic (move to domain)
- Direct database access (must go through outbound port)
- Importing domain entities directly — access only through application layer
