# OrganicLever App Web — Specification Corpus

Audience: engineers and technical product managers working on
[`apps/organiclever-app-web`](../../../../apps/organiclever-app-web/README.md) — the local-first
life journal.

This corpus is the single source of truth for what the app does. A scenario here defines what a
user sees, what is written to the in-browser database, and what survives a reload.

## Contents

- [Architecture](./architecture.md) — the current as-built system: its context, the container it
  deploys, its feature contexts, and the constraints that bind them.
- [Routes and screens](./routes-and-screens.md) — the URL surface and the screen each route renders.
- [Design system](./design-system.md) — palette, typography, dark mode, and the shared components
  the screens are built from.
- [Behaviours](./behaviours/README.md) — the recursive Gherkin corpus, grouped by feature context.

## Related

- [`apps/organiclever-app-web/README.md`](../../../../apps/organiclever-app-web/README.md) — the implementing project.
- [OrganicLever BE](../be/README.md) — the sibling corpus for the backend this app calls for diagnostics.
