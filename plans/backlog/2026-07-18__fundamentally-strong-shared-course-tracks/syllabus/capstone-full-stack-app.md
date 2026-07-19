# Capstone: Full-Stack App (Desktop-boundary milestone, TypeScript + Python)

**Course ID**: `capstone-full-stack-app` · **Kind**: Full-stack milestone · **Language**: TypeScript +
Python.

**Scope note**: the capstone that closes **Phase 2 · Multi-Platform Productivity**'s Desktop sub-phase.
It builds one complete, deployable **full-stack web application** — a typed frontend
(`frontend-essentials`, `advanced-frontend`) connected to an async backend (`backend-essentials`,
`async-python-and-fastapi-services`) over HTTP (`networking-essentials`), persisted in SQL
(`sql-essentials`), designed per `api-design` — and **self-hosts it** using `self-hosting-essentials`,
tying the web and cloud sub-phases together. It sits after the mobile and desktop sub-phases as the
phase's integrative closer; the mobile and desktop tracks stand on their own and are not folded into
this web capstone.

## Why this exists · the big idea

- **The problem before the solution**: Phase 2 covers many platforms in a linear march (web → cloud →
  mobile → desktop). Without an integrative capstone, the reader has breadth but no proof they can take
  one platform's stack from empty repo to a running, reachable, deployed product.
- **Keep-this-if-you-forget-everything**: shipping is the whole loop — build the vertical slice, then
  put it on the internet reproducibly. A full-stack app that only runs on `localhost` is half-finished.
- **Big ideas touched**: `abstraction-and-its-cost` (the deployment substrate is another layer to see
  through), `correctness-vs-pragmatism` (a deployed, modest app beats an elaborate local one).

## Prerequisites

- **Prior courses**: the Web sub-phase courses through `advanced-frontend`, the Cloud/backend-at-scale
  sub-phase starting with `self-hosting-essentials` (see [README.md](./README.md) for the full course
  catalog), and `sql-essentials`; `capstone-first-working-software` as the smaller precursor.
- **Tools & environment**: a macOS/Linux terminal; the Python async service stack + a TypeScript
  frontend toolchain + SQL; a single VM/box or a git-push PaaS from `self-hosting-essentials`; `git`,
  `curl` — pinned CVE-clean at authoring.
- **Assumed knowledge**: building each layer (frontend, async API, SQL) and self-hosting one service.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-18 — `[Needs Verification]`: pin the exact CVE-clean versions of the frontend toolchain, the
  async service stack, the DB, and the reverse proxy/PaaS at authoring; the frontend ↔ API ↔ SQL slice
  and the self-host-it deployment path are stable patterns.

## Concepts integrated

This capstone integrates prior courses' concepts; it introduces none of its own:

- [ ] A typed UI with loading/error/empty states (`frontend-essentials`, `advanced-frontend`).
- [ ] `fetch` to the API over HTTP with correct CORS (`networking-essentials`).
- [ ] Async backend endpoints with validation + a `response_model` (`backend-essentials`,
      `async-python-and-fastapi-services`, `api-design`).
- [ ] SQL persistence with a normalized schema (`sql-essentials`).
- [ ] A basic UI test + an API integration test (depth deferred to `software-testing`).
- [ ] Self-hosted deployment: `systemd` + reverse proxy + TLS on a domain, or a git-push PaaS
      (`self-hosting-essentials`).

## Ordered steps

1. `capstone-full-stack-app/code/backend/` — the async service (`backend-essentials`/
   `async-python-and-fastapi-services`) with a CORS-safe read/write API over a SQL schema
   (`sql-essentials`). Verify `curl` returns JSON from the DB and a write persists.
2. `capstone-full-stack-app/code/frontend/` — a typed UI (`frontend-essentials`/`advanced-frontend`)
   that lists data with loading/error/empty states and a create/update form posting to the API. Verify
   the UI shows live data and a UI action persists to the DB (reflected after refetch).
3. Add a Testing-Library UI test + an API integration test. Verify both pass.
4. Deploy the whole app — either self-hosted (`systemd` + TLS reverse proxy on a domain) or via a
   git-push PaaS (`self-hosting-essentials`), with config/secrets out-of-band. Verify the app is
   reachable at an HTTPS URL with no committed secrets.

## Acceptance criteria

- A reader runs the backend + frontend locally, performs a create/read/update from the UI, confirms the
  change landed in the SQL database, and passes both the UI test and the API integration test; then
  deploys the app to a reachable HTTPS URL (self-hosted or PaaS) with no committed secrets — the whole
  stack works together and is on the internet. Security hardening and the full test pyramid remain
  deferred to the deepening arc.

## Done bar

Runnable end-to-end (full vertical slice, deployed to a reachable HTTPS URL) + web-verified.

## In which paths

- `job-seeking-software-engineer` — Phase 2 · Multi-Platform Productivity (web → cloud → mobile →
  desktop) — Desktop sub-phase.
- `software-engineer` — Stage 2 · One language end-to-end, then BUILD A REAL APP FIRST (the
  "immediately effective" payoff).

---

← Back to [README.md — course library catalog](./README.md)
