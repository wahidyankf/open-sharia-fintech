# AyoKoding — Behavior

Audience: Engineers, Technical Product/Project Managers

Behavior specifications for AyoKoding — Gherkin scenarios that exercise the product through
two perspectives: the tRPC HTTP API surface (`api`) and the browser UI surface (`web`).
Sliced by perspective so each test runner can wire its step implementations against the
right glob.

## Product-surface distinction

AyoKoding ships **one deployable container**: `web` (Next.js 16). The behavior tree splits
along **perspective**, not deployable-container boundary:

- `ayokoding-www/` — UI-semantic scenarios (DOM, navigation, accessibility, locale).
- `ayokoding-be/` — tRPC HTTP-semantic scenarios (procedure shapes, error codes, locale).
- `ayokoding-cli/` — CLI-semantic scenarios for `ayokoding-cli`.
- `ayokoding-build-tools/` — build-time tooling (index generation, etc.).

The `ayokoding-be` slug is a **perspective slug**, not a container. tRPC procedures run
inside the same `web` container's Next.js server. The surface exists so specs can talk
about API contract behavior without conflating it with UI behavior.

## Children

- `ayokoding-www/gherkin/` — Browser UI Gherkin scenarios.
- `ayokoding-be/gherkin/` — tRPC API Gherkin scenarios (HTTP semantic).
- `ayokoding-cli/` — CLI-semantic scenarios for `ayokoding-cli`.
- `ayokoding-build-tools/` — Build-time tooling scenarios.

## Surfaces

| Surface                 | Background                          | Step style                                     | Consumed by                              |
| ----------------------- | ----------------------------------- | ---------------------------------------------- | ---------------------------------------- |
| `ayokoding-www`         | `Given the app is running`          | `clicks`, `types`, `sees`, `navigates`         | `apps/ayokoding-www-fe-e2e` (Playwright) |
| `ayokoding-be`          | `Given the API is running`          | `the client calls`, response shape, error code | `apps/ayokoding-www-be-e2e` (Playwright) |
| `ayokoding-cli`         | `Given the CLI binary is available` | `runs`, exit code, output assertions           | `apps/ayokoding-cli` (Go test + godog)   |
| `ayokoding-build-tools` | build-time                          | index generation assertions                    | `apps/ayokoding-www` (unit tests)        |

## Gherkin coverage

### `ayokoding-www/gherkin/` — UI perspective

Organized by bounded context (one folder per BC, matching the DDD registry).

| Bounded Context | Features                                                           | Count |
| --------------- | ------------------------------------------------------------------ | ----- |
| app-shell       | `responsive`, `accessibility`                                      | 2     |
| content         | `content-rendering`                                                | 1     |
| search          | `search`                                                           | 1     |
| i18n            | `i18n`                                                             | 1     |
| navigation      | `navigation`, `architecture-cases-routes`, `learn-reorg-redirects` | 3     |
| **Total**       |                                                                    | **8** |

### `ayokoding-be/gherkin/` — tRPC API perspective

| Bounded Context | Features         | Count |
| --------------- | ---------------- | ----- |
| content         | `content-api`    | 1     |
| search          | `search-api`     | 1     |
| navigation      | `navigation-api` | 1     |
| i18n            | `i18n-api`       | 1     |
| health          | `health-check`   | 1     |
| **Total**       |                  | **5** |

## Related

- [`../components/`](../components/README.md) — C4 L3 components that the scenarios exercise
- [ayokoding-be — Behavior Surface](./ayokoding-be/README.md)
- [ayokoding-build-tools — Behavior Surface](./ayokoding-build-tools/README.md)
- [ayokoding-cli — Behavior Surface](./ayokoding-cli/README.md)
- [ayokoding-www — Behavior Surface](./ayokoding-www/README.md)
- `../ddd/` — DDD registry + glossaries that own the vocabulary
