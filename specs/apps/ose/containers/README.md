# OSE — Containers (C4 L2)

Container-level specifications for all OSE-family deployables.

## OSE Application (`ose-app-*`)

- [container.md](./container.md) — C4 container diagram (ose-app-web + ose-be + PostgreSQL + OpenRouter)
- [deployment.md](./deployment.md) — Deployment topology
- [contracts/](./contracts/) — OpenAPI 3.1 contract spec (`ose-contracts` Nx project)

## OSE Platform Web (`ose-web`)

`ose-web` deploys as ONE container (`web`). The tRPC API runs **inside** that same Next.js
process — no separate backend deployable. Behavior perspectives are `platform-web` (UI) and
`platform-be` (tRPC HTTP) — both describe the same single container.

- [container.md](./container.md) — single-container diagram

## Related

- [`../system-context/`](../system-context/README.md) — C4 L1
- [`../components/`](../components/README.md) — C4 L3
- [`../behavior/`](../behavior/README.md) — Gherkin scenarios
- [OSE Application API Contract](./contracts/README.md)
