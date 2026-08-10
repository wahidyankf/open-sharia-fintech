# BeaverNest — Product

BeaverNest is a personal AI assistant and content operating layer, built
**walking-skeleton-first**: Phase 1 proves the engineering harness (specs, backend, frontend, CI,
agents) end-to-end with the smallest possible surface, before any real product capability is
designed.

## Hello-World Scope (Phase 1)

The entire product surface for this phase is:

- `beavernest-be` — a stateless F#/Giraffe REST API exposing exactly two `GET` routes
  (`/api/v1/health`, `/api/v1/hello`) and a 404 handler for anything else
- `beavernest-app-web` — a single Next.js landing page (`/`) that names the product and shows the
  greeting fetched live from `beavernest-be`

No other route, page, or capability exists yet. The greeting text is a hardcoded constant on the
backend; the frontend never hardcodes it — it fetches it over HTTP, so the FE → BE wiring is
genuinely exercised.

## Deferred Capabilities

Everything below is explicitly out of scope for Phase 1 and named here so later readers don't
mistake the hello-world quad for a foundation to build on directly:

- **Assistant Core** (Phase 2) — LLM integration, conversation memory, assistant-facing UI
- **Content Building** (Phase 3) — note capture, draft generation, persistence layer
- **Posting & Scheduling** (Phase 4) — multi-platform posting, scheduling, workflow automation
- Any form of authentication, multi-user concept, or write endpoint
- Any database or in-memory store — the greeting is a constant, not derived data
- Deploy provisioning — CI caller workflows ship wired but dormant; the first real deploy belongs
  to its own plan

See [ROADMAP.md](../../../../ROADMAP.md) for the full phase sequence.

## Related

- [overview.md](./overview.md) — one-page product overview
- [system-context/](../system-context/README.md) — C4 L1 actors and external systems
- [repo-governance/vision/beavernest.md](../../../../repo-governance/vision/beavernest.md) — why
  BeaverNest exists
