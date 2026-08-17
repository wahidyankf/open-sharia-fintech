# OSE — Behavior Specifications

Gherkin feature files for all OSE-family products, organized by flat product-surface.

## Surfaces

| Surface        | Product        | Perspective     | Gherkin path                     |
| -------------- | -------------- | --------------- | -------------------------------- |
| `be`           | ose-be         | REST API (HTTP) | `behavior/be/gherkin/`           |
| `app-web`      | ose-app-web    | Browser UI      | `behavior/app-web/gherkin/`      |
| `platform-be`  | ose-web (tRPC) | tRPC HTTP       | `behavior/platform-be/gherkin/`  |
| `platform-web` | ose-web (UI)   | Browser UI      | `behavior/platform-web/gherkin/` |
| `cli`          | ose-cli        | CLI             | `behavior/ose-cli/gherkin/`      |

## Naming Convention

Each surface directory is named `<product>-<surface>` where:

- `<product>` identifies the deployable (`app`, `platform`)
- `<surface>` identifies the perspective (`be`, `web`, `cli`)

This flat naming avoids nested `api/` or bare `be/` dirs and makes per-product Gherkin
paths unambiguous.

## Related

- [../containers/](../containers/README.md) — C4 L2
- [../components/](../components/README.md) — C4 L3
- [../ddd/](../ddd/README.md) — Domain model
- [app-web — Behavior Surface](./app-web/README.md)
- [ose-be — Behavior Surface](./be/README.md)
- [ose-cli — Behavior Surface](./ose-cli/README.md)
- [platform-be — Behavior Surface](./platform-be/README.md)
- [platform-web — Behavior Surface](./platform-web/README.md)
