# BeaverNest — System Context (C4 L1)

The Phase 1 foundation has exactly one human actor and one internal call, no external
systems or third-party integrations.

```mermaid
%%{init: {'theme':'base', 'themeVariables': { 'primaryColor':'#0173B2', 'primaryTextColor':'#fff', 'primaryBorderColor':'#000', 'lineColor':'#029E73', 'secondaryColor':'#DE8F05', 'tertiaryColor':'#CC78BC'}}}%%
graph TB
    Browser["<b>Browser</b><br/><i>Maintainer</i>"]
    FE["<b>beavernest-app-web</b><br/>Vite/React CSR client<br/>port 19310"]
    BE["<b>beavernest-be</b><br/>F#/Giraffe REST API<br/>port 19320"]

    Browser -->|"HTTP GET /"| FE
    FE -->|"HTTP GET /api/v1/readiness"| BE

    style Browser fill:#CA9161,stroke:#000,stroke-width:2px,color:#000
    style FE fill:#0173B2,stroke:#000,stroke-width:2px,color:#fff
    style BE fill:#029E73,stroke:#000,stroke-width:2px,color:#fff
```

## Actors

- **Maintainer (browser)** — the only human actor in Phase 1. Navigates to `beavernest-app-web` in a
  browser; there is no authentication and no other user role.

## Systems

- **`beavernest-app-web`** — Vite/React client-side-rendered app. Renders one "Foundation status"
  panel that polls and displays the readiness state it fetches from `beavernest-be`.
- **`beavernest-be`** — F#/Giraffe REST API backed by SQLite. Exposes `GET /api/v1/health`
  (liveness), `GET /api/v1/readiness` (database/schema readiness, the call `beavernest-app-web`
  makes), and a 404 handler for any other route — including the retired `/api/v1/hello` greeting
  route.

## External Systems

None. Phase 1 is deliberately self-contained — no third-party API, no auth provider. SQLite is an
embedded, in-process store, not an external system.

## Related

- [context.md](./context.md) — C4 L1 detail (see this README)
- [product/](../product/README.md) — foundation scope
- [containers/](../containers/README.md) — C4 L2 deployable units
- [behavior/](../behavior/README.md) — Gherkin scenarios covering both HTTP calls above
