# OrganicLever BE — Specification Corpus

Audience: engineers and technical product managers working on
[`apps/organiclever-be`](../../../../apps/organiclever-be/README.md) — the F#/Giraffe REST API.

This corpus is the single source of truth for what the service answers. A scenario here defines a
route's status code, its response body, and the conditions under which it fails.

## Contents

- [Architecture](./architecture.md) — the current as-built system: its context, the one process it
  deploys, its handler layer, and the constraints that bind them.
- [API reference](./api.md) — every route the service exposes, with its status codes and bodies.
- [Behaviours](./behaviours/README.md) — the recursive Gherkin corpus, grouped by route domain.
- [Contracts](./contracts/README.md) — the OpenAPI 3.1 specification both this service and its
  callers generate from.

## Contract first

The OpenAPI document is the source, not a description written afterwards. `organiclever-be`
generates its models from the bundled contract, so adding a route means editing the contract in the
same delivery unit as the handler and the scenario.

## Related

- [`apps/organiclever-be/README.md`](../../../../apps/organiclever-be/README.md) — the implementing project.
- [OrganicLever App Web](../app-web/README.md) — the sibling corpus for the client that calls it.
