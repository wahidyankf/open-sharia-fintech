# Islamic BE — Gherkin Scenarios

Backend Gherkin scenarios for `islamic-be`. Consumed by Godog at the Unit layer, in
[`apps/islamic-be/internal/bdd`](../../../../../apps/islamic-be/internal/bdd), and by
`playwright-bdd` at the E2E layer, in
[`apps/islamic-be-e2e/steps`](../../../../../apps/islamic-be-e2e/README.md).

## Feature files

| Feature file                                                       | Domain |
| ------------------------------------------------------------------ | ------ |
| [health/health.feature](./health/health.feature)                   | health |
| [config/port-resolution.feature](./config/port-resolution.feature) | config |

- [config](./config/README.md) — islamic-be Gherkin Domain
- [health](./health/README.md) — islamic-be Gherkin Domain

## Adapters

Unit and E2E. There is no Integration adapter: the service owns no local resource boundary — no
database, no filesystem state, no broker — so every scenario resolves either in-process or across
the real HTTP boundary. Each scenario carries its own `Exemption(integration)` with an
alternative-proof naming the target that does prove it.
