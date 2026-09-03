# messaging — organiclever-be Gherkin Domain

Scenarios for the OrganicLever backend NATS/JetStream messaging infrastructure. Scenarios that
need a live NATS/JetStream broker live under `live/`, kept out of
`organiclever-be:specs:behavior:coverage`'s unit-scoped drift scan; `nats-config.feature` is pure
logic and unit-covered directly here.

## Feature Files

- **[nats-config.feature](./nats-config.feature)** — Messaging configuration validation
  (1 scenario)

## Related

- [Parent gherkin README](../README.md)

- [live](./live/README.md) — organiclever-be Gherkin Domain
