# ayokoding-www

Fullstack Next.js 16 application that serves the AyoKoding educational content platform. TypeScript stack: tRPC for type-safe API, Zod for validation, shadcn/ui for components, and FlexSearch for full-text search.

## Architecture

- **Framework**: Next.js 16 (App Router, React Server Components)
- **API**: tRPC with server caller (RSC) and HTTP endpoint (search)
- **Content**: Reads markdown from `content/` (co-located in the app)
- **Rendering**: Full SSG via `generateStaticParams` for SEO, client-side only for search/theme/tabs
- **Styling**: Tailwind CSS v4 + shadcn/ui + @tailwindcss/typography
- **Search**: FlexSearch with per-locale indexing
- **i18n**: English (`/en`) and Indonesian (`/id`) with segment mapping
- **Analytics**: Google Analytics GA4 via @next/third-parties

## Quick Start

```bash
# Development server (port 3101)
nx dev ayokoding-www

# Build
nx build ayokoding-www

# Run tests
nx run ayokoding-www:test:quick

# Typecheck
nx run ayokoding-www:typecheck

# Lint
nx run ayokoding-www:lint
```

## Docker

```bash
# Build and run with Docker Compose
cd infra/dev/ayokoding-www
docker compose up --build

# Health check
curl http://localhost:3101/api/trpc/meta.health
```

## Deployment

Deployed to Vercel via production branch `prod-ayokoding-www`.

```bash
# Vercel auto-builds when code is pushed to prod branch
git push origin main:prod-ayokoding-www
```

## Source Layout

`src/` is organized by **feature module** under `src/features/`. Each module splits its code
into two zones following the **functional core / imperative shell** convention:

- **`core/`** — the functional core. Pure only: pure functions, immutable data, derivations,
  validation, Zod schemas, plain TS types/interfaces, constant data tables, and pure
  transforms. `core/` files never import `react`, `next`, node builtins, `@trpc/server`
  wiring, or any IO/network client, and never import from `shell/`.
- **`shell/`** — the imperative shell. Everything effectful: React components, DOM/browser
  hooks, filesystem readers, repository adapters, tRPC routers and init wiring, and Next.js
  middleware. `shell/` may import from `core/`.

Classify each file by what it actually does, not by where it used to live. When in doubt (any
IO, React, or wiring) → `shell/`.

| Feature module | Zones present   | core (pure)                                                                                                                 | shell (IO + UI + wiring)                                                                                                                                                  |
| -------------- | --------------- | --------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `app-shell`    | `[shell]`       | —                                                                                                                           | tRPC root router + `trpc-init` + chrome (header, footer, mobile-nav, theme toggle)                                                                                        |
| `content`      | `[core, shell]` | schemas, types, repository interface, tree-builder, shortcodes, parser                                                      | tRPC `content.*` router + fs reader/repository-fs/repository-memory + service + index-generator + markdown rendering components                                           |
| `search`       | `[core, shell]` | search schemas                                                                                                              | tRPC `search.query` router + `generate-search-data` (fs) + search dialog/provider + `use-search` hook                                                                     |
| `i18n`         | `[core, shell]` | config, locale schema, translations                                                                                         | tRPC `meta.languages` router + Next middleware + locale switcher + `use-locale` hook                                                                                      |
| `navigation`   | `[core, shell]` | tree-node schema (+ locale re-export)                                                                                       | tRPC `content.getTree` router + sidebar/sidebar-tree/breadcrumb/prev-next/toc                                                                                             |
| `course-paths` | `[core, shell]` | `PathManifest`/prerequisite schemas, manifest-integrity + prerequisite-DAG checks, path-context parsing, arc-hue derivation | route wiring (`route-path-data`, `paths-route`) + fs manifest repository + hub/category/arc/path landing pages + path rail/banner/card + prerequisite list + sidebar host |
| `health`       | `[shell]`       | —                                                                                                                           | tRPC `meta.health` liveness probe                                                                                                                                         |

Other modules and pages import feature code directly from the file in `core/` or `shell/`
(e.g. `@/features/content/core/schemas`, `@/features/content/shell/service`). The cardinal
rule is one-directional: `shell/` may depend on `core/`, but `core/` must never depend on
`shell/`.

## Specs

Gherkin acceptance specs live at `specs/apps/ayokoding/` organized by **API perspective**:

- `behavior/ayokoding-www/gherkin/` — UI-semantic scenarios (clicks, sees, navigates), consumed by
  `ayokoding-www-fe-e2e`.
- `behavior/ayokoding-be/gherkin/` — tRPC HTTP-semantic scenarios (the client calls, response shape),
  consumed by `ayokoding-www-be-e2e`.

The slug `api` is a **perspective slug**, not a container — there is no separate API
container. Both perspectives execute inside this single `web` Next.js process. The slug
rename `be` → `api` reflects this (the `organiclever` peer keeps `be` because
`organiclever-be` is a real F#/Giraffe deployment).

## i18n entry redirects

Locale entry redirects live in `next.config.ts`. The root route redirects permanently to `/en`, and
the finite uppercase variants of `en` and `id` redirect to their lowercase canonical paths. Keeping
these rules in Next.js configuration avoids request-time middleware for every page view.

## Related

- [ayokoding-www-be-e2e](../ayokoding-www-be-e2e/) - Backend E2E tests (consumes `behavior/ayokoding-be/gherkin/`)
- [ayokoding-www-fe-e2e](../ayokoding-www-fe-e2e/) - Frontend E2E tests (consumes `behavior/ayokoding-www/gherkin/`)
- [specs/apps/ayokoding/](../../specs/apps/ayokoding/) - C4 + Gherkin specifications
