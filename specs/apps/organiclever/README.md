# OrganicLever Application Specs

Platform-agnostic specifications for the OrganicLever fullstack application. The
application is rolling-release on `main` (Trunk Based Development): scope grows
incrementally rather than landing in numbered releases. Today the system ships a
marketing landing site, a system-status diagnostic page, and a `/api/v1/health` backend
endpoint — no authenticated screens, no remote sync. The application consists of an
F#/Giraffe backend REST API and a Next.js 16 frontend.

## Structure

```
specs/apps/organiclever/
├── README.md              # This file
├── product/               # Product framing (above C4)
│   └── README.md
├── system-context/        # C4 L1 — actors and external systems
│   ├── README.md
│   └── context.md
├── containers/            # C4 L2 — deployable units
│   ├── README.md
│   ├── container.md
│   └── contracts/         # OpenAPI 3.1 contract spec (consumed by codegen)
├── components/            # C4 L3 — per-container internals
│   ├── README.md
│   ├── be/                # F#/Giraffe backend component specs
│   │   ├── README.md
│   │   └── component-be.md
│   └── app-web/           # Next.js frontend component specs
│       ├── README.md
│       └── component-web.md
└── behavior/              # Gherkin scenarios (HTTP-semantic + UI-semantic)
    ├── README.md
    ├── organiclever-be/gherkin/        # Backend Gherkin scenarios
    └── organiclever-app-web/gherkin/   # Frontend Gherkin scenarios (per feature context)
```

## Containers

One row per deployable container (C4 L2). Container slug is canonical: it indexes
`components/<slug>/`, `behavior/<slug>/gherkin/`, the container README, and the Gherkin
glob. Adding a future container (e.g. `mobile`, `desktop`, a second backend) means adding
a row here, not changing the schema.

| Container | Perspective                             | Background                 | Scenarios                                                                                   | Domains                                                                        | Consumed by                                   |
| --------- | --------------------------------------- | -------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------------- |
| `be`      | HTTP-semantic (GET, POST, status codes) | `Given the API is running` | [behavior/organiclever-be/gherkin/](./behavior/organiclever-be/gherkin/README.md)           | health, journal, db, messaging                                                 | `apps/organiclever-be` (F#/Giraffe, TickSpec) |
| `app-web` | UI-semantic (clicks, types, sees)       | `Given the app is running` | [behavior/organiclever-app-web/gherkin/](./behavior/organiclever-app-web/gherkin/README.md) | app-shell, health, journal, routine, routing, settings, stats, workout-session | `apps/organiclever-app-web` (Next.js 16)      |
| `www`     | UI-semantic (clicks, types, sees)       | `Given the app is running` | [behavior/organiclever-www/gherkin/](./behavior/organiclever-www/gherkin/README.md)         | home, accessibility                                                            | `apps/organiclever-www` (Next.js 16)          |

The `app-web` container's system-status page consumes the `be` container's health endpoint.
Otherwise `app-web` is local-first today.

## Feature Contexts

Counts are Gherkin features per container. `--` means no features in that container today.

| Feature Context | `be` features | `app-web` features | `www` features | Description                                                    |
| --------------- | ------------- | ------------------ | -------------- | -------------------------------------------------------------- |
| app-shell       | --            | 2                  | --             | Navigation chrome, accessibility, entry-logging overlays       |
| db              | 1             | --                 | --             | Database schema migrations                                     |
| health          | 1             | 1                  | --             | Service health status (`be` probe + `app-web` diagnostic page) |
| home            | --            | --                 | 1              | Marketing landing page (organiclever-www)                      |
| accessibility   | --            | --                 | 1              | Accessibility compliance for marketing site                    |
| journal         | 1             | 2                  | --             | Append-only event log — system of record (PGlite)              |
| messaging       | 3             | --                 | --             | NATS/JetStream messaging infrastructure                        |
| routine         | --            | 1                  | --             | Workout routine management                                     |
| routing         | --            | 2                  | --             | App routing and disabled-route 404 guards                      |
| settings        | --            | 3                  | --             | User preferences — dark mode, language                         |
| stats           | --            | 2                  | --             | History and progress projections over journal events           |
| workout-session | --            | 1                  | --             | Active workout session FSM                                     |

## Spec Artifacts

- **[system-context/](./system-context/README.md)**, **[containers/](./containers/README.md)**,
  **[components/](./components/README.md)** — C4 architecture diagrams (L1/L2/L3)
- **[components/be/](./components/be/README.md)** — Backend API component specs
  ([Gherkin features](./behavior/organiclever-be/gherkin/README.md))
- **[components/app-web/](./components/app-web/README.md)** — Frontend component specs
  ([Gherkin features](./behavior/organiclever-app-web/gherkin/README.md))

## Spec Consumption

All backends consume the backend Gherkin specs at **all three test levels**:

- **`test:unit`** — steps call service functions with mocked dependencies; Gherkin spec paths
  are included in Nx cache inputs so cache invalidates when specs change
- **`test:quick`** — unit + coverage check; Gherkin spec paths included in Nx cache inputs
- **`test:integration`** — steps call service functions with real PostgreSQL; cache disabled

## For Product / Project Managers

**Audience note**: This folder is written for engineers and SWE-background TPMs (the
kind embedded with a developer-tools or productivity team — not non-technical PMs). The
C4 diagrams and feature-context vocabulary will be familiar if you have worked with system
diagrams and event-storming.

**Reading order**:

1. **[product/overview.md](./product/overview.md)** — Start here. Plain-language
   summary of what OrganicLever does, who it is for, what ships today, and what is deferred.
2. **[system-context/context.md](./system-context/context.md)** — Where OrganicLever
   sits in the broader technical landscape: actors, external systems, trust boundaries.
3. **[containers/container.md](./containers/container.md)** — The two deployable units:
   Next.js web app (Vercel) and F#/Giraffe backend (Kubernetes). How they connect.
   Also see [containers/deployment.md](./containers/deployment.md) for environments
   and Docker image details.
4. **[components/app-web/](./components/app-web/README.md)** — Frontend internals:
   feature-context architecture, routes and screens, design system.
   [components/be/api.md](./components/be/api.md) covers the backend API surface.
5. **[behavior/](./behavior/README.md)** — What the system is supposed to do, expressed
   as Gherkin (Given-When-Then) acceptance criteria per feature context. The same files
   drive automated tests.

**In plain language**:

- You log what you did (workout, reading, meal, focus). It remembers. You see it later.
- No account. No subscription. No data leaves your device.
- The streak badge is the only "game mechanic" today.

## Related

- [Three-Level Testing Standard](../../../repo-governance/development/quality/three-level-testing-standard.md)
- [BDD Spec-Test Mapping](../../../repo-governance/development/infra/bdd-spec-test-mapping.md)
- [BDD Standards](../../../docs/explanation/software-engineering/development/behavior-driven-development-bdd/README.md)
- [OrganicLever — Product](./product/README.md)
