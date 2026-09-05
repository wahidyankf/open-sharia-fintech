# messaging — ose-be Gherkin Domain

Scenarios for the OSE Application backend NATS/JetStream messaging infrastructure. The owner
project's static coverage discovers this directory and `live/` recursively. Every scenario has
in-process Unit proof through injected messaging ports. Scenarios whose public boundary requires a
real NATS/JetStream broker are additionally implemented by `ose-be-e2e`; Integration is exempt only
where its zero-network boundary cannot express the scenario.

## Feature Files

- **[nats-config.feature](./nats-config.feature)** — Messaging configuration validation
  (1 scenario)

## Related

- [Parent gherkin README](../README.md)

- [live](./live/README.md) — ose-be Gherkin Domain
