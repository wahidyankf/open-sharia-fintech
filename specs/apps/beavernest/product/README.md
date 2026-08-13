# BeaverNest — Product

BeaverNest is a personal AI assistant and content operating layer, built
**walking-skeleton-first**: Phase 1 proves the engineering harness (specs, backend, frontend, CI,
agents) end-to-end with the smallest possible surface, before any real product capability is
designed.

## Foundation Scope (Phase 1)

The entire product surface for this phase is:

- `beavernest-be` — a F#/Giraffe REST API, backed by SQLite, exposing exactly two `GET` routes
  (`/api/v1/health` for liveness, `/api/v1/readiness` for database/schema readiness) and a 404
  handler for anything else. The earlier `/api/v1/hello` greeting route is retired — it now returns
  404, verified by its own regression scenario.
- `beavernest-app` — a Flutter Web client that renders a same-origin Foundation status workspace,
  refreshes `beavernest-be`'s readiness endpoint in place, and exposes contract-safe diagnostics
  and online-only browser guidance.

No other route, page, or capability exists yet.

## Deferred Capabilities

Everything below is explicitly out of scope for Phase 1 and named here so later readers don't
mistake the foundation for a product to build on directly:

- **Assistant Core** (Phase 2) — LLM integration, conversation memory, assistant-facing UI
- **Content Building** (Phase 3) — note capture, draft generation, persistence layer
- **Posting & Scheduling** (Phase 4) — multi-platform posting, scheduling, workflow automation
- Any form of authentication, multi-user concept, or write endpoint
- Deploy provisioning — CI caller workflows ship wired but dormant; the first real deploy belongs
  to its own plan

## Related

- [overview.md](./overview.md) — one-page product overview
- [system-context/](../system-context/README.md) — C4 L1 actors and external systems
- [`repo-governance/vision/beavernest.md`](../../../../repo-governance/vision/beavernest.md) — why
  BeaverNest exists
