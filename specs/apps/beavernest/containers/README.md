# BeaverNest — Containers (C4 L2)

Container-level specifications for the BeaverNest foundation.

## BeaverNest Foundation

- [container.md](./container.md) — container list (see this README)
- [contracts/](./contracts/README.md) — OpenAPI 3.1 contract spec (`beavernest-contracts` Nx
  project) defining the two `beavernest-be` routes `beavernest-app-web` consumes

Production ships **one** combined runtime container: `beavernest-be` (F#/Giraffe, port 19300) serves
the pre-built `beavernest-app-web` (Vite/React CSR) static assets same-origin — no FE/BE network
boundary exists in production. The "two processes" split (`beavernest-app-web` on port 19310 proxying
API calls to `beavernest-be` on port 19320) is local-development-only, via the Vite dev server's
proxy. A dedicated `container.md` diagram and `deployment.md` topology doc are deferred until later
phases land further runtimes — see [product/](../product/README.md) for the deferred-scope list.

## Related

- [system-context/](../system-context/README.md) — C4 L1
- [components/](../components/README.md) — C4 L3
- [behavior/](../behavior/README.md) — Gherkin scenarios
