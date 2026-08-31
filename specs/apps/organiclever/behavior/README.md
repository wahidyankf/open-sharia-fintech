# OrganicLever — Behavior

Audience: Engineers, Technical Product/Project Managers

Behavior specifications for OrganicLever — Gherkin scenarios that exercise the product
through both the backend HTTP surface and the frontend UI surface. Sliced by surface so
each project can wire its step implementations against the right glob.

## Children

- `organiclever-be/` — Backend Gherkin scenarios (HTTP semantic).
- `organiclever-app-web/` — App-client Gherkin scenarios (UI semantic).
- `organiclever-www/` — Public marketing site Gherkin scenarios (UI semantic).
- `organiclever-www-be/` — Marketing site BE E2E slot (structural placeholder; no real backend API).

## Surfaces

One row per product-surface. Each surface dir named `<product>-<perspective>` per the
flat product-surface convention.

| Surface                | Perspective                             | Background                 | Consumed by                                         |
| ---------------------- | --------------------------------------- | -------------------------- | --------------------------------------------------- |
| `organiclever-be`      | HTTP-semantic (GET, POST, status codes) | `Given the API is running` | `apps/organiclever-be` (F#/Giraffe)                 |
| `organiclever-app-web` | UI-semantic (clicks, types, sees)       | `Given the app is running` | `apps/organiclever-app-web` (Next.js 16)            |
| `organiclever-www`     | UI-semantic (clicks, types, sees)       | —                          | `apps/organiclever-www-fe-e2e` (Playwright FE E2E)  |
| `organiclever-www-be`  | Structural placeholder (no backend API) | —                          | `apps/organiclever-www-be-e2e` (Playwright BE slot) |

## Gherkin coverage

### `organiclever-be/gherkin/`

| Domain | Feature                       | Scenarios |
| ------ | ----------------------------- | --------- |
| health | `health/health-check.feature` | 2         |

### `organiclever-app-web/gherkin/`

Organized by feature context (one folder per product area).

| Feature Context | Features                                   | Count  |
| --------------- | ------------------------------------------ | ------ |
| app-shell       | `entry-loggers`, `navigation`              | 2      |
| health          | `system-status-be`                         | 1      |
| journal         | `home-screen`, `journal-mechanism`         | 2      |
| routine         | `routine-management`                       | 1      |
| routing         | `app-routes`, `disabled-routes`            | 2      |
| settings        | `dark-mode`, `language`, `settings-screen` | 3      |
| stats           | `history-screen`, `progress-screen`        | 2      |
| workout-session | `workout-session`                          | 1      |
| **Total**       |                                            | **14** |

### `organiclever-www/gherkin/`

Greenfield-simple marketing surface (no feature-context layering).

| Domain        | Features        | Count |
| ------------- | --------------- | ----- |
| home          | `home`          | 1     |
| accessibility | `accessibility` | 1     |
| env-loader    | `env-loader`    | 1     |
| **Total**     |                 | **3** |

## Related

- [`../components/`](../components/README.md) — C4 L3 components that the scenarios exercise
- [`../containers/contracts/`](../containers/contracts/README.md) — OpenAPI contract the
- [organiclever-app-web — Behavior Surface](./organiclever-app-web/README.md)
- [organiclever-be — Behavior Surface](./organiclever-be/README.md)
- [organiclever-www-be — Behavior Surface](./organiclever-www-be/README.md)
- [organiclever-www — Behavior Surface](./organiclever-www/README.md)
  backend scenarios assert against (moved from legacy `contracts/` in Phase 2A.7)
