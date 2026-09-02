# OrganicLever Backend Gherkin Specs

Gherkin feature files for the OrganicLever backend service. 7 files, 13 scenarios across 5
domains.

## Feature Files

| Domain    | File                               | Scenarios |
| --------- | ---------------------------------- | --------- |
| health    | `health/health-check.feature`      | 2         |
| journal   | `journal/journal-crud.feature`     | 6         |
| db        | `db/migrations.feature`            | 1         |
| messaging | `messaging/nats-connect.feature`   | 1         |
| messaging | `messaging/nats-config.feature`    | 1         |
| messaging | `messaging/jetstream-demo.feature` | 1         |
| env       | `env/env-tier-loader.feature`      | 1         |

## Conventions

- **File naming**: `[domain-capability].feature` (kebab-case)
- **First Background step**: `Given the API is running`
- **Step language**: HTTP-semantic only — no framework or library names
- **User story block**: Every `Feature:` block opens with `As a … / I want … / So that …`

## Related

- **Parent**: [components/be/ specs](../architecture.md)
- **BDD Standards**: [behavior-driven-development-bdd/](../../../../../docs/explanation/software-engineering/development/behavior-driven-development-bdd/README.md)

- [db](./db/README.md) — organiclever-be Gherkin Domain
- [env](./env/README.md) — organiclever-be Gherkin Domain
- [health](./health/README.md) — organiclever-be Gherkin Domain
- [journal](./journal/README.md) — organiclever-be Gherkin Domain
- [messaging](./messaging/README.md) — organiclever-be Gherkin Domain
