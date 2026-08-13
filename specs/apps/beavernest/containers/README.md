# BeaverNest — Containers (C4 L2)

Container-level specifications for the BeaverNest foundation.

## BeaverNest Foundation

- [container.md](./container.md) — container list (see this README)
- [contracts/](./contracts/README.md) — OpenAPI 3.1 contract spec (`beavernest-contracts` Nx
  project) defining the two `beavernest-be` routes `beavernest-app` consumes

Production ships **one** combined runtime container: `beavernest-be` (F#/Giraffe, port 19300) serves
the pre-built `beavernest-app` Flutter Web static assets same-origin — no FE/BE network boundary or
separate frontend development server exists. A dedicated `container.md` diagram and `deployment.md`
topology doc are deferred until later phases land further runtimes — see
[product/](../product/README.md) for the deferred-scope list.

## Related

- [system-context/](../system-context/README.md) — C4 L1
- [components/](../components/README.md) — C4 L3
- [behavior/](../behavior/README.md) — Gherkin scenarios
