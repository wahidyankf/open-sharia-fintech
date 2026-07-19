# Capstone · Full-Stack App (Phase 2 boundary)

**Mapping row** (frozen [tech-docs §Canonical Mapping Table](../tech-docs.md#canonical-mapping-table)):
inter-topic capstone · anchored after N=39 · folder weight **495** (`105 + 10 × 39`) · TypeScript +
Python. **Re-anchored per DN-5** (was a cross-cutting Pass-1 capstone in the sibling plan; now closes
the entire Phase 2 Multi-Platform Productivity phase).

**Scope note**: the capstone that closes **Phase 2 · Multi-Platform Productivity**. It builds one
complete, deployable **full-stack web application** — a typed frontend ([N=18](./README.md),
[N=23](./README.md)) connected to an async backend ([N=19](./README.md),
[N=20](./20-async-python-and-fastapi-services.md)) over HTTP ([N=21](./README.md)), persisted in SQL
([N=13](./README.md)), designed per [N=22 API Design](./README.md) — and **self-hosts it** using
[N=24 Self-Hosting Essentials](./24-self-hosting-essentials.md), tying the web and cloud sub-phases
together. It sits after the mobile and desktop sub-phases as the phase's integrative closer; the mobile
and desktop tracks stand on their own and are not folded into this web capstone.

## Why this exists · the big idea

- **The problem before the solution**: Phase 2 covers many platforms in a linear march (web → cloud →
  mobile → desktop). Without an integrative capstone, the reader has breadth but no proof they can take
  one platform's stack from empty repo to a running, reachable, deployed product.
- **Keep-this-if-you-forget-everything**: shipping is the whole loop — build the vertical slice, then
  put it on the internet reproducibly. A full-stack app that only runs on `localhost` is half-finished.
- **Big ideas touched**: `abstraction-and-its-cost` (the deployment substrate is another layer to see
  through), `correctness-vs-pragmatism` (a deployed, modest app beats an elaborate local one).

## Prerequisites

- **Prior topics**: the Phase 2 web sub-phase ([N=17](./README.md)–[N=23](./README.md)), the cloud
  sub-phase ([N=24](./24-self-hosting-essentials.md)–[N=29](./README.md)), and
  [N=13 SQL Essentials](./README.md); the
  [first-working-software capstone](./23c-capstone-first-working-software.md) as the smaller precursor.
- **Tools & environment**: a macOS/Linux terminal; the Python async service stack + a TypeScript
  frontend toolchain + SQL; a single VM/box or a git-push PaaS from
  [N=24](./24-self-hosting-essentials.md); `git`, `curl` — pinned CVE-clean at authoring.
- **Assumed knowledge**: building each layer (frontend, async API, SQL) and self-hosting one service.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (DD-28 convention).

- 2026-07-18 — `[Needs Verification]`: pin the exact CVE-clean versions of the frontend toolchain, the
  async service stack, the DB, and the reverse proxy/PaaS at authoring; the frontend ↔ API ↔ SQL slice
  and the self-host-it deployment path are stable patterns.

## Concepts integrated

This capstone integrates prior topics' concepts; it introduces none of its own:

- [ ] A typed UI with loading/error/empty states ([N=18](./README.md), [N=23](./README.md)).
- [ ] `fetch` to the API over HTTP with correct CORS ([N=21](./README.md)).
- [ ] Async backend endpoints with validation + a `response_model`
      ([N=19](./README.md), [N=20](./20-async-python-and-fastapi-services.md), [N=22](./README.md)).
- [ ] SQL persistence with a normalized schema ([N=13](./README.md)).
- [ ] A basic UI test + an API integration test (depth deferred to [N=102](./README.md)).
- [ ] Self-hosted deployment: `systemd` + reverse proxy + TLS on a domain, or a git-push PaaS
      ([N=24](./24-self-hosting-essentials.md)).

## Ordered steps

1. `capstone-full-stack-app/code/backend/` — the async service ([N=19](./README.md)/[N=20](./20-async-python-and-fastapi-services.md))
   with a CORS-safe read/write API over a SQL schema ([N=13](./README.md)). Verify `curl` returns JSON
   from the DB and a write persists.
2. `capstone-full-stack-app/code/frontend/` — a typed UI ([N=18](./README.md)/[N=23](./README.md)) that
   lists data with loading/error/empty states and a create/update form posting to the API. Verify the UI
   shows live data and a UI action persists to the DB (reflected after refetch).
3. Add a Testing-Library UI test + an API integration test. Verify both pass.
4. Deploy the whole app — either self-hosted (`systemd` + TLS reverse proxy on a domain) or via a
   git-push PaaS ([N=24](./24-self-hosting-essentials.md)), with config/secrets out-of-band. Verify the
   app is reachable at an HTTPS URL with no committed secrets.

## Acceptance criteria

- A reader runs the backend + frontend locally, performs a create/read/update from the UI, confirms the
  change landed in the SQL database, and passes both the UI test and the API integration test; then
  deploys the app to a reachable HTTPS URL (self-hosted or PaaS) with no committed secrets — the whole
  stack works together and is on the internet. Security hardening and the full test pyramid remain
  deferred to Phase 3.

## Done bar

Runnable end-to-end (full vertical slice, deployed to a reachable HTTPS URL) + web-verified.

---

← Previous: N=39 `building-production-cli-tools` ([index](./README.md)) · Next: N=40
`computer-science-foundations` ([index](./README.md)) →
