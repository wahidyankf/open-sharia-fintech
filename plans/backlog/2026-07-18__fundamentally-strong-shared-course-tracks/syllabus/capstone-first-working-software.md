# Capstone: First Working Software (Web milestone, Python + TypeScript)

**Course ID**: `capstone-first-working-software` · **Kind**: Web milestone · **Language**: Python +
TypeScript.

**Scope note**: the milestone bundle that proves the reader can **ship one small, complete, working web
application** by integrating earlier fundamentals with the web-productivity courses — clean Python
(`just-enough-python`) with a Bash setup script (`just-enough-bash`) under git
(`version-control-and-git`), an OO domain model (`object-oriented-programming-essentials`) over a
normalized SQL database (`sql-essentials`), served by an async HTTP JSON API (`backend-essentials`,
`async-python-and-fastapi-services`) designed per `api-design`, consumed over HTTP
(`networking-essentials`) by a typed frontend (`just-enough-typescript`, `frontend-essentials`).
**Deferred to the deepening arc**: security hardening (`security-essentials`) and the full test pyramid
(`software-testing`) — this capstone is "it works end to end," not "it is hardened and exhaustively
tested."

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

- **Prior courses**: `just-enough-python`, `just-enough-bash`, `version-control-and-git`, and the Web
  sub-phase courses through `advanced-frontend` (see [README.md](./README.md) for the full course
  catalog), especially `backend-essentials` and `async-python-and-fastapi-services`.
- **Tools & environment**: a macOS/Linux terminal; Python 3.x + `uv` + an ASGI server; SQLite or
  PostgreSQL; Node + a TypeScript frontend toolchain; `git`; `curl`/`httpx` — pinned CVE-clean at
  authoring.
- **Assumed knowledge**: writing an async endpoint, modeling data in SQL, and rendering data in a typed
  UI, each individually.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (per this plan's Anti-Hallucination verification recipe).

- 2026-07-18 — `[Needs Verification]`: pin the exact CVE-clean versions of the Python service stack
  (from `async-python-and-fastapi-services`), the DB, and the frontend toolchain at authoring; the
  integration pattern (UI → HTTP → API → domain → DB) is stable.

## Concepts integrated

This capstone integrates prior courses' concepts; it introduces none of its own:

- [ ] Clean Python + a Bash setup/run script + git hygiene (`just-enough-python`, `just-enough-bash`,
      `version-control-and-git`).
- [ ] Apt data structures + an OO domain model (`data-structures-and-algorithms-essentials`,
      `object-oriented-programming-essentials`).
- [ ] A normalized SQL schema with parameterized access (`sql-essentials`).
- [ ] An async HTTP JSON API with validation, designed per REST conventions (`backend-essentials`,
      `async-python-and-fastapi-services`, `api-design`).
- [ ] A typed frontend consuming the API over HTTP with loading/error/empty states
      (`just-enough-typescript`, `frontend-essentials`, `networking-essentials`).
- [ ] Basic tests where the reader can write them (full pyramid deferred to `software-testing`).

## Ordered steps

1. `capstone-first-working-software/code/` — scaffold the service (`backend-essentials`/
   `async-python-and-fastapi-services`)
   - schema/migrations (`sql-essentials`) + a `setup.sh` (`just-enough-bash`). Verify `./setup.sh`
     boots the app and `curl /health` returns 200.
2. Implement the domain model (`object-oriented-programming-essentials`) + core CRUD with parameterized
   DB access (`data-structures-and-algorithms-essentials`/`sql-essentials`) + request validation
   (`api-design`). Verify `curl` round-trips every resource and invalid input yields a structured 422.
3. Build a typed frontend (`just-enough-typescript`/`frontend-essentials`) that lists and creates
   resources over HTTP (`networking-essentials`) with loading/error/empty states. Verify a UI action
   persists to the DB and the list reflects it after refetch.
4. Add a basic happy-path + edge-case test on the API and a smoke test on the UI. Verify they pass.
   (Depth and security hardening are explicitly deferred to the deepening arc.)

## Acceptance criteria

- A reader on a clean machine runs `./setup.sh`, opens the frontend, performs a create/read from the UI,
  confirms the change landed in the SQL database, exercises every API endpoint with `curl` (including a
  422 on bad input), and passes the basic test suite — one complete, runnable web application, end to
  end, with no hidden setup. Security hardening and the full test pyramid are recorded as deferred to
  the deepening arc, not silently skipped.

## Done bar

Runnable end-to-end (clean-machine reproduction of the full vertical slice) + web-verified.

## In which paths

- `job-seeking-software-engineer` — Phase 2 · Multi-Platform Productivity (web → cloud → mobile →
  desktop) — Web sub-phase.
- `software-engineer` — Stage 2 · One language end-to-end, then BUILD A REAL APP FIRST (the
  "immediately effective" payoff).

---

← Back to [README.md — course library catalog](./README.md)
