# wahidyankf-www — Gherkin Features

Audience: Engineers, Technical Product/Project Managers

UI-semantic Gherkin feature files for `wahidyankf-www`, organized by bounded context. Each
subfolder maps to one bounded context from the
bounded-context registry.

## Structure

```
specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/
├── app-shell/
│   ├── accessibility.feature
│   ├── responsive.feature
│   └── theme.feature
├── cv/
│   └── cv.feature
├── env-loader/            # APP_ENV tier env-file loader (build-time tooling)
│   └── env-loader.feature
├── home/
│   └── home.feature
├── personal-projects/
│   └── personal-projects.feature
└── search/
    ├── search.feature
    └── static-filterable-routes.feature
```

## Coverage

| Bounded Context     | Features                               |
| ------------------- | -------------------------------------- |
| `app-shell`         | `accessibility`, `responsive`, `theme` |
| `cv`                | `cv`                                   |
| `env-loader`        | `env-loader`                           |
| `home`              | `home`                                 |
| `personal-projects` | `personal-projects`                    |
| `search`            | `search`, `static-filterable-routes`   |

## Consumed by

| App                     | Level | Tool             |
| ----------------------- | ----- | ---------------- |
| `wahidyankf-www-fe-e2e` | E2E   | `playwright-bdd` |

## Related

- `../../../ddd/bounded-context-map.md` — context relationships
- `../../../ddd/ubiquitous-language/` — vocabulary
