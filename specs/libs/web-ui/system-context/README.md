# System Context — web-ui

C4 Level 1 system context for `web-ui`.

## Actors and consumers

- **Frontend developers** — import components directly from `@open-sharia-enterprise/web-ui`.
- **Consuming apps** — every TypeScript frontend that renders shared UI (`ayokoding-www`,
  `organiclever-www`, `organiclever-app-web`, `ose-www`, `ose-app-web`).
- **Storybook** — hosts an isolated visual catalogue of every component for manual review.

`web-ui` has no runtime dependency on any backend; it is a pure presentation-layer library.

See [context.md](./context.md) for the C4 context diagram placeholder.
