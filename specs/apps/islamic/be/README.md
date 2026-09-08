# Islamic BE — Specification Corpus

Audience: engineers and technical product managers working on `apps/islamic-be` — the
Sharia-compliance API.

This corpus is the single source of truth for what the service answers. A scenario here defines a
route's status code, its response body, and how the process resolves its own configuration.

## Contents

- [Architecture](./architecture.md) — the current as-built system: its context, the process it
  deploys, its bounded contexts, and the constraints that bind them.
- [Behaviours](./behaviours/README.md) — the recursive Gherkin corpus, grouped by bounded context.
- [Contracts](./contracts/README.md) — the OpenAPI 3.1 specification the service and its clients
  generate from.

## Related

- `apps/islamic-be` — the implementing project, created in DU3.
- `apps/islamic-be-e2e` — the E2E project that drives this corpus against the real process,
  created in DU4.

Both are named rather than linked: this corpus lands before either project exists, and the
`md-links` gate scans the whole tree rather than only the current change. The DU that creates each
project adds the link in both directions.
