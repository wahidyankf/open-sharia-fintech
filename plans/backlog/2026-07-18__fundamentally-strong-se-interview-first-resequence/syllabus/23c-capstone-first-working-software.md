# Capstone · First Working Software (Phase 2 web boundary)

**Mapping row** (frozen [tech-docs §Canonical Mapping Table](../tech-docs.md#canonical-mapping-table)):
inter-topic capstone · anchored after N=23 · folder weight **335** (`105 + 10 × 23`) · Python + TypeScript.
**Re-anchored per DN-5** (was the Pass-1 boundary capstone in the sibling plan; now cements the first
complete working web application at the end of the Phase 2 web sub-phase).

**Scope note**: the milestone bundle that proves the reader can **ship one small, complete, working web
application** by integrating Phase 1 fundamentals with the Phase 2 web sub-phase — clean Python
([N=4](./README.md)) with a Bash setup script ([N=5](./README.md)) under git ([N=6](./README.md)), an
OO domain model ([N=11](./README.md)) over a normalized SQL database ([N=13](./README.md)), served by an
async HTTP JSON API ([N=19](./README.md), [N=20](./20-async-python-and-fastapi-services.md)) designed
per [N=22 API Design](./README.md), consumed over HTTP ([N=21](./README.md)) by a typed frontend
([N=17](./README.md), [N=18](./README.md)). **Deferred to Phase 3**: security hardening
([N=91](./README.md)) and the full test pyramid ([N=102](./README.md)) — this capstone is "it works end
to end," not "it is hardened and exhaustively tested."

## Why this exists · the big idea

- **The problem before the solution**: the reader has learned each web layer separately — a language, a
  database, an API, a frontend. Nothing yet proves they can assemble those layers into one running
  system that a person can actually use. Integration is a distinct skill from any single layer.
- **Keep-this-if-you-forget-everything**: a working application is a **vertical slice** — a request
  travels from a UI, over HTTP, into an API, through a domain model, to a database, and back — and being
  able to build and reason about that whole path is the threshold of productivity.
- **Big ideas touched**: `abstraction-and-its-cost` (each layer hides the one below; the slice makes the
  whole stack legible), `taming-state` (the database is the system's durable state, mediated by the API).

## Prerequisites

- **Prior topics**: Phase 1 ([N=4](./README.md)–[N=16](./16-behavioral-and-leadership-interviews.md))
  and the Phase 2 web sub-phase ([N=17](./README.md)–[N=23](./README.md)), especially
  [N=19 Backend Essentials](./README.md) and
  [N=20 Async Python & FastAPI Services](./20-async-python-and-fastapi-services.md).
- **Tools & environment**: a macOS/Linux terminal; Python 3.x + `uv` + an ASGI server; SQLite or
  PostgreSQL; Node + a TypeScript frontend toolchain; `git`; `curl`/`httpx` — pinned CVE-clean at
  authoring.
- **Assumed knowledge**: writing an async endpoint, modeling data in SQL, and rendering data in a typed
  UI, each individually.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (DD-28 convention).

- 2026-07-18 — `[Needs Verification]`: pin the exact CVE-clean versions of the Python service stack
  (from [N=20](./20-async-python-and-fastapi-services.md)), the DB, and the frontend toolchain at
  authoring; the integration pattern (UI → HTTP → API → domain → DB) is stable.

## Concepts integrated

This capstone integrates prior topics' concepts; it introduces none of its own:

- [ ] Clean Python + a Bash setup/run script + git hygiene ([N=4](./README.md), [N=5](./README.md),
      [N=6](./README.md)).
- [ ] Apt data structures + an OO domain model ([N=7](./README.md), [N=11](./README.md)).
- [ ] A normalized SQL schema with parameterized access ([N=13](./README.md)).
- [ ] An async HTTP JSON API with validation, designed per REST conventions
      ([N=19](./README.md), [N=20](./20-async-python-and-fastapi-services.md), [N=22](./README.md)).
- [ ] A typed frontend consuming the API over HTTP with loading/error/empty states
      ([N=17](./README.md), [N=18](./README.md), [N=21](./README.md)).
- [ ] Basic tests where the reader can write them (full pyramid deferred to [N=102](./README.md)).

## Ordered steps

1. `capstone-first-working-software/code/` — scaffold the service ([N=19](./README.md)/[N=20](./20-async-python-and-fastapi-services.md))
   - schema/migrations ([N=13](./README.md)) + a `setup.sh` ([N=5](./README.md)). Verify `./setup.sh`
     boots the app and `curl /health` returns 200.
2. Implement the domain model ([N=11](./README.md)) + core CRUD with parameterized DB access
   ([N=7](./README.md)/[N=13](./README.md)) + request validation ([N=22](./README.md)). Verify `curl`
   round-trips every resource and invalid input yields a structured 422.
3. Build a typed frontend ([N=17](./README.md)/[N=18](./README.md)) that lists and creates resources
   over HTTP ([N=21](./README.md)) with loading/error/empty states. Verify a UI action persists to the
   DB and the list reflects it after refetch.
4. Add a basic happy-path + edge-case test on the API and a smoke test on the UI. Verify they pass.
   (Depth and security hardening are explicitly deferred to Phase 3.)

## Acceptance criteria

- A reader on a clean machine runs `./setup.sh`, opens the frontend, performs a create/read from the UI,
  confirms the change landed in the SQL database, exercises every API endpoint with `curl` (including a
  422 on bad input), and passes the basic test suite — one complete, runnable web application, end to
  end, with no hidden setup. Security hardening and the full test pyramid are recorded as deferred to
  Phase 3, not silently skipped.

## Done bar

Runnable end-to-end (clean-machine reproduction of the full vertical slice) + web-verified.

---

← Previous: N=23 `advanced-frontend` ([index](./README.md)) · Next: N=24
[`self-hosting-essentials`](./24-self-hosting-essentials.md) →
