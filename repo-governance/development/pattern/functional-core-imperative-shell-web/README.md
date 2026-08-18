---
title: "Functional Core / Imperative Shell — Web Apps"
description: "The architecture pattern for Next.js web apps — every feature module splits into a pure functional core and an effectful imperative shell under src/features/<name>/{core,shell}/"
when_to_use: "Read this index to find the right Functional Core / Imperative Shell — Web Apps child document."
---

# Functional Core / Imperative Shell — Web Apps

- [Principles and Conventions](./principles-and-conventions.md) — The core principles and conventions this pattern implements - pure functions, simplicity, immutability, explicitness, and functional programming practices. Use when you need to trace the core/shell split back to the principles and conventions it implements.
- [Directory Layout and Zone Responsibilities](./directory-layout-and-zone-responsibilities.md) — The features/<name>/{core,shell}/ directory layout and what belongs in each zone. Use when deciding which files in a feature module belong in core/ versus shell/.
- [The Dependency Rule](./the-dependency-rule.md) — The one-way dependency rule - shell/ may import core/, core/ must never import shell/ - and the forbidden-imports list that enforces it. Use when checking whether a core/ file has accidentally imported React, Next.js, or another effectful dependency.
- [Next.js Construct Placement and Reference Implementations](./nextjs-construct-placement-and-reference-implementations.md) — Where each Next.js construct (Server Components, Server Actions, route handlers, middleware) belongs, and the three reference apps that follow this pattern. Use when deciding whether a specific Next.js construct belongs in core/ or shell/, or looking for a reference implementation.
