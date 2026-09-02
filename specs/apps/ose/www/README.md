# OSE Web — Specification Corpus

Audience: engineers and technical product managers working on
[`apps/ose-www`](../../../../apps/ose-www/README.md) — the OSE platform's public site.

This corpus is the single source of truth for what a visitor sees and what the site's in-process API
returns.

## Contents

- [Architecture](./architecture.md) — the current as-built system: its context, the one container it
  deploys, its feature contexts, and the constraints that bind them.
- [Frontend components](./frontend-components.md) — the pages, layout, renderers, search, and theme
  a visitor interacts with.
- [API components](./api-components.md) — the tRPC router, its procedures, and the content pipeline
  behind them.
- [Behaviors](./behaviors/README.md) — the recursive Gherkin corpus, split by the perspective a
  scenario takes.

## Related

- [`apps/ose-www/README.md`](../../../../apps/ose-www/README.md) — the implementing project.
- [OSE App Web](../app-web/README.md) — the product this site introduces.
