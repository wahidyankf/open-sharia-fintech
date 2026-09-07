---
description: "The four concentric zones of hexagonal architecture, plus the core concepts of ports, inbound adapters, outbound adapters, and the domain model."
when_to_use: "Use when orienting to hexagonal architecture's zones and core vocabulary before applying it to a specific app."
---

# Overview and Core Concepts

## Overview

Hexagonal architecture defines concentric zones:

| Zone              | Also Called        | Purpose                                                                    |
| ----------------- | ------------------ | -------------------------------------------------------------------------- |
| Domain            | Core               | Business entities and rules — no external imports                          |
| Application       | Use-case           | Orchestrates domain objects; defines ports (interfaces)                    |
| Inbound adapters  | Primary adapters   | Translate external input into application calls (HTTP, CLI, GraphQL)       |
| Outbound adapters | Secondary adapters | Implement application ports for infrastructure concerns (DB, HTTP clients) |

The domain has no knowledge of how it is invoked or where its data comes from. Adapters translate between external
protocols and the language of the domain.

## Core Concepts

### Ports (Interfaces)

A port is a named interface declared in the application layer. It defines what the application needs without specifying
how that need is fulfilled. Two kinds of ports exist:

- **Inbound ports** — define entry points into the application (service interfaces, use-case traits)
- **Outbound ports** — define dependencies the application requires (repository traits, email sender interfaces)

### Inbound Adapters

Inbound adapters sit outside the application and call into it through inbound ports. They translate external signals
(HTTP requests, CLI arguments, message queue events) into application calls. The application layer knows nothing about
HTTP verbs, CLI flags, or queue protocols.

Examples: HTTP route handlers, CLI command handlers, message consumers.

### Outbound Adapters

Outbound adapters implement outbound ports. They translate application calls into external operations (SQL queries,
HTTP client calls, file writes). The application layer uses the port interface only; it never instantiates or imports
the concrete adapter.

Examples: PostgreSQL repository implementations, external HTTP API clients, file-based caches.

### Domain Model

The domain model contains business entities, value objects, and pure business rules. It has zero dependencies on
frameworks, databases, or network libraries. It must compile and run in isolation from all adapters.
