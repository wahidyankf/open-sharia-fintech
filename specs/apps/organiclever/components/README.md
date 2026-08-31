# OrganicLever — Components (C4 L3)

Audience: Engineers, Technical Product/Project Managers

Component-level specifications for OrganicLever — what lives inside each container,
sliced by surface (backend, frontend).

## Children

- `be/` — Backend (F#/Giraffe — F# language on the Giraffe HTTP framework) component specs.
  - `component-be.md` — moved from `c4/` in Phase 2A.
  - `README.md` — moved from legacy flat-root `be/README.md` in Phase 2A.
  - `api.md` — API endpoints, env vars, architecture tree. Authored in Phase 3.
- `app-web/` — Frontend (Next.js 16) component specs.
  - `component-web.md` — moved from `c4/` in Phase 2A.
  - `README.md` — moved from legacy flat-root `web/README.md` in Phase 2A.
  - `architecture.md` — feature-context tree and layer rules. Authored in Phase 3.
  - `routes-and-screens.md` — routes/screens/entry-flows tables. Authored in Phase 3.
  - `design-system.md` — palette, typography, dark mode, tokens. Authored in Phase 3.

## Related

- [`../system-context/`](../system-context/README.md) — C4 L1
- [`../containers/`](../containers/README.md) — C4 L2
- [`../behavior/`](../behavior/README.md) — Gherkin scenarios that exercise the components
- [OrganicLever Frontend App Specs](./app-web/README.md)
- [OrganicLever Backend API Specs](./be/README.md)
- [OrganicLever Marketing Web — Component Specs](./web/README.md)
