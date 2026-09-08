# Islamic BE — Specification Corpus

Audience: engineers and technical product managers working on
[`apps/islamic-be`](../../../../apps/islamic-be/README.md) — the
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

- [`apps/islamic-be`](../../../../apps/islamic-be/README.md) — the implementing project.
- `apps/islamic-be-e2e` — the E2E project that drives this corpus against the real process,
  created in DU4.

`islamic-be-e2e` is named rather than linked because it does not exist yet: the `md-links` gate
scans the whole tree rather than only the current change, so a link to a project DU4 has not created
would fail every push. DU4 adds it, in both directions — exactly as DU3 did for `islamic-be` above.
