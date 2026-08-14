# organiclever-www — Core Concepts and Directory Structure

## Core Concepts

### App Overview

**organiclever-www** (`apps/organiclever-www/`):

- **Framework**: Next.js 16 with App Router
- **Architecture**: DDD bounded contexts (`domain` / `application` / `infrastructure` / `presentation`)
- **Storage**: PGlite (Postgres-WASM, IndexedDB-backed) — local-first, no backend required
- **Effects**: Effect TS for typed functional effects in infrastructure layer
- **State machines**: XState for UI FSMs (app-shell, workout-session)
- **URL**: https://www.organiclever.com/
- **Role**: Landing page + full life-journal app under `/app/`
- **Deployment**: Vercel (`prod-organiclever-www` branch)

### Tech Stack Details

| Layer      | Technology                                |
| ---------- | ----------------------------------------- |
| Framework  | Next.js 16 (App Router)                   |
| UI Runtime | React 19                                  |
| Styling    | TailwindCSS + OL warm OKLCH design tokens |
| Components | `@open-sharia-enterprise/web-ui`          |
| Storage    | PGlite (Postgres-WASM, IndexedDB)         |
| Effects    | Effect TS (infrastructure layer only)     |
| State      | XState v5 (app-shell, workout-session)    |
| BDD tests  | `@amiceli/vitest-cucumber` + Vitest       |
| Deployment | Vercel (auto-detected)                    |

## Directory Structure

```
apps/organiclever-www/
├── src/
│   ├── app/                        # Next.js App Router (thin wrappers only)
│   │   ├── app/                    # /app/* routes (home, history, progress, settings, workout…)
│   │   └── system/status/be/       # Server-rendered diagnostic page
│   ├── contexts/                   # Bounded-context implementations
│   │   ├── app-shell/              # Navigation chrome, i18n, entry-logging overlays
│   │   ├── health/                 # Backend health diagnostic (dormant BE client)
│   │   ├── journal/                # Event log — system of record (PGlite)
│   │   ├── landing/                # Marketing landing page
│   │   ├── routine/                # Workout routine management (PGlite)
│   │   ├── routing/                # 404 guards (disabled routes)
│   │   ├── settings/                # User preferences — dark mode, language (PGlite)
│   │   ├── stats/                  # History + progress projections (read-only from journal)
│   │   └── workout-session/        # Active workout session FSM (XState)
│   ├── shared/                     # Cross-context utilities
│   │   ├── runtime/                # PgliteService Tag, AppRuntime, shared tagged errors
│   │   └── utils/                  # format-relative-time, fmt
│   ├── generated-contracts/        # Auto-generated from OpenAPI spec (gitignored)
│   └── test/                       # Test helpers and fixtures
├── test/unit/steps/                # Vitest-cucumber step implementations (per bounded context)
├── docs/explanation/               # Architecture docs (bounded-context map)
└── project.json                    # Nx project configuration
```
