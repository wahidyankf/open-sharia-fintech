---
description: "The features/<name>/{core,shell}/ directory layout and what belongs in each zone."
when_to_use: "Use when deciding which files in a feature module belong in core/ versus shell/."
---

# Directory Layout and Zone Responsibilities

## Directory Layout

```
src/
└── features/
    └── <name>/
        ├── core/      # PURE: logic, decisions, validation, transforms, schemas, types, constant data
        └── shell/     # EFFECTFUL: React components, hooks, fs/network/tRPC, Server Actions, route handlers, wiring
```

| Zone  | Path                     | Holds                                                                            |
| ----- | ------------------------ | -------------------------------------------------------------------------------- |
| Core  | `features/<name>/core/`  | Pure functions, immutable data, plain types/interfaces, zod schemas, data tables |
| Shell | `features/<name>/shell/` | React components, DOM hooks, fs readers, repositories, tRPC routers, route.ts    |

A feature that has no pure logic (UI-only) has only a `shell/`. A feature that has no effects has only a `core/`.
Create only the zones a feature actually needs — do not add empty placeholder directories or barrels.

## Zone Responsibilities

### core/ — Functional Core

- Pure functions: validation, transformation, derivation, ranking, formatting, calculation
- Immutable value types and plain TypeScript interfaces
- zod schemas (pure data validation)
- Constant data tables (e.g. i18n translation maps, static datasets)
- Shared interfaces that the shell implements (e.g. a repository interface) live here so the shell can depend on the
  core without the core ever depending on the shell

The core is fully unit-testable without a Next.js runtime, a DOM, a filesystem, or a network.

### shell/ — Imperative Shell

- Next.js Server Components and Client Components (`.tsx`)
- React hooks that touch the DOM or browser globals
- Filesystem readers, content repositories, search-index generators
- tRPC routers, tRPC init, root router (server wiring)
- Next.js middleware, route handlers (`route.ts`), Server Actions
- Any code performing IO, network, or framework wiring

The shell stays thin: it gathers inputs, calls the core for decisions, and applies the results as effects.
