# wahidyankf-www — Behavior

Audience: Engineers, Technical Product/Project Managers

Behavior specifications for wahidyankf-www — Gherkin scenarios that exercise the product
through the frontend UI surface. There is no backend API perspective today; if a server-side
rendering layer or API is added later, a `behavior/wahidyankf-be/gherkin/` folder would be added here.

## Children

- `web/` — Frontend Gherkin scenarios (UI semantic). Each sub-folder maps to one bounded
  context from the DDD registry.

## Containers

| Container | Perspective                       | Background                 | Consumed by                        |
| --------- | --------------------------------- | -------------------------- | ---------------------------------- |
| `web`     | UI-semantic (clicks, types, sees) | `Given the app is running` | `apps/wahidyankf-www` (Next.js 16) |

## Gherkin coverage

### `web/gherkin/`

| Bounded Context     | Features                               | Count |
| ------------------- | -------------------------------------- | ----- |
| `app-shell`         | `theme`, `responsive`, `accessibility` | 3     |
| `home`              | `home`                                 | 1     |
| `cv`                | `cv`                                   | 1     |
| `personal-projects` | `personal-projects`                    | 1     |
| `search`            | `search`                               | 1     |
| **Total**           |                                        | **7** |

## Related

- [`../components/`](../components/README.md) — C4 L3 components that the scenarios exercise
- [wahidyankf-www — Web Behavior](./wahidyankf-www/README.md)
- `../ddd/` — Ubiquitous language governing scenario vocabulary
