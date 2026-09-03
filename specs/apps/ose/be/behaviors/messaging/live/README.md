# live — ose-be Gherkin Domain

Scenarios that need a live NATS/JetStream broker, e2e-tested by `ose-be-e2e` and excluded from
`ose-be:specs:behavior:coverage`'s unit-scoped drift scan via `--exclude-dir live`.

## Feature Files

- **[nats-connect.feature](./nats-connect.feature)** — NATS connection on startup (1 scenario)
- **[jetstream-demo.feature](./jetstream-demo.feature)** — JetStream durable publish/consume
  demo (1 scenario)

## Related

- [Parent gherkin README](../README.md)
