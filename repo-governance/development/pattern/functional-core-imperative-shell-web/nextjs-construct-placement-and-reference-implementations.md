---
title: "Next.js Construct Placement and Reference Implementations"
description: "Where each Next.js construct (Server Components, Server Actions, route handlers, middleware) belongs, and the three reference apps that follow this pattern."
category: explanation
subcategory: development
tags:
  - architecture
  - functional-core-imperative-shell
  - nextjs
  - functional-programming
  - web
created: 2026-06-17
when_to_use: "Use when deciding whether a specific Next.js construct belongs in core/ or shell/, or looking for a reference implementation."
---

# Next.js Construct Placement and Reference Implementations

## Next.js Construct Placement

Next.js framework constructs are effects and belong in `shell/`:

| Construct                   | Placement | Notes                                                           |
| --------------------------- | --------- | --------------------------------------------------------------- |
| Server Components           | `shell/`  | Call `core/` functions directly for any logic                   |
| Client Components           | `shell/`  | Hold UI state; delegate decisions to `core/`                    |
| Server Actions              | `shell/`  | Thin wrappers that call `core/` and return serialisable values  |
| Route handlers (`route.ts`) | `shell/`  | Validate input (zod schema from `core/`), call `core/`, respond |
| Middleware                  | `shell/`  | Framework wiring                                                |
| tRPC routers / init         | `shell/`  | Server wiring                                                   |

## Reference Implementations

All three Next.js content apps follow this pattern identically:

- `apps/ose-www/` — content/landing/search/seo/rss-feed features, each split into `core/` (parsers, schemas, builders)
  and `shell/` (fs repositories, tRPC routers, React components)
- `apps/ayokoding-www/` — content/i18n/navigation/search features in the same split
- `apps/wahidyankf-www/` — portfolio features; pure CV/project/search data and helpers in `core/`, React UI in
  `shell/`
