---
description: The architecture pattern for Next.js web apps — every feature module splits into a pure functional core and an effectful imperative shell under src/features/<name>/{core,shell}/
when_to_use: "Use when structuring or reviewing a Next.js feature module, or deciding whether a file belongs in core/ or shell/."
---

# Functional Core / Imperative Shell — Web Apps

Next.js web apps in this repo organise every feature as a **functional core / imperative shell** module
under `src/features/<name>/`. Each module splits into exactly two zones: a pure `core/` that holds all
logic and decisions, and an effectful `shell/` that performs IO, renders UI, and wires the framework. The
shell calls the core; the core never reaches back. This is **not** hexagonal architecture and **not** DDD —
that pattern is reserved for **backend** services.

## Contents

- [Principles and Conventions](./functional-core-imperative-shell-web/principles-and-conventions.md) — The core principles and conventions this pattern implements - pure functions, simplicity, immutability, explicitness, and functional programming practices. Use when you need to trace the core/shell split back to the principles and conventions it implements.
- [Directory Layout and Zone Responsibilities](./functional-core-imperative-shell-web/directory-layout-and-zone-responsibilities.md) — The features/<name>/{core,shell}/ directory layout and what belongs in each zone. Use when deciding which files in a feature module belong in core/ versus shell/.
- [The Dependency Rule](./functional-core-imperative-shell-web/the-dependency-rule.md) — The one-way dependency rule - shell/ may import core/, core/ must never import shell/ - and the forbidden-imports list that enforces it. Use when checking whether a core/ file has accidentally imported React, Next.js, or another effectful dependency.
- [Next.js Construct Placement and Reference Implementations](./functional-core-imperative-shell-web/nextjs-construct-placement-and-reference-implementations.md) — Where each Next.js construct (Server Components, Server Actions, route handlers, middleware) belongs, and the three reference apps that follow this pattern. Use when deciding whether a specific Next.js construct belongs in core/ or shell/, or looking for a reference implementation.

## Related

- **[Hexagonal Architecture](../pattern/hexagonal-architecture.md)** — Core dependency-rule idea shared with the backend pattern
- **[Hexagonal Architecture + DDD — Backend Apps](../pattern/hexagonal-architecture-be.md)** — The ports-and-adapters / DDD pattern used by backend services; explains why web apps deliberately use the simpler core/shell split instead
- **[Functional Programming Practices](../pattern/functional-programming.md)** — Pure-function and immutability conventions the core depends on
