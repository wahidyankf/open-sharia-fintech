# live — organiclever-be Gherkin Domain

Scenarios whose public messaging boundary needs a real NATS/JetStream broker. They retain mandatory
in-process Unit proof through injected ports and are E2E-tested by `organiclever-be-e2e`. The
owner's static coverage includes this directory recursively; scenario-level Integration exemptions
document why the zero-network Integration boundary cannot express the broker interaction.

## Feature Files

- **[nats-connect.feature](./nats-connect.feature)** — NATS connection on startup (1 scenario)
- **[jetstream-demo.feature](./jetstream-demo.feature)** — JetStream durable publish/consume
  demo (1 scenario)

## Related

- [Parent gherkin README](../README.md)
